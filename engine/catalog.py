"""Téléchargement du catalogue public de l'Apify Store.

L'API publique `GET /v2/store` ne demande ni compte ni jeton. On ne garde que
les champs utiles à l'analyse, dans un fichier JSONL (une ligne par Actor).
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable, Iterator

STORE_URL = "https://api.apify.com/v2/store"
PAGE_SIZE = 1000
MAX_OFFSET = 15000  # limite observée de l'API le 10 novembre 2026
SORTS = ("popularity", "newest", "lastUpdate")
USER_AGENT = "catalog-analysis/1.0"

Fetch = Callable[[str], dict]


def http_get_json(url: str, retries: int = 4, timeout: int = 60) -> dict:
    """GET avec reprises bornées et attente croissante (2, 4, 8, 16 s)."""
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code < 500 and exc.code != 429:
                raise
            last = exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
        if attempt < retries:
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"échec après {retries + 1} tentatives : {url}") from last


def primary_price_usd(pricing: dict | None) -> float | None:
    """Prix en dollars pour 1 000 résultats, quand il est déductible."""
    if not pricing:
        return None
    model = pricing.get("pricingModel")
    if model == "PRICE_PER_DATASET_ITEM":
        price = pricing.get("pricePerUnitUsd")
        return round(price * 1000, 4) if price is not None else None
    if model == "PAY_PER_EVENT":
        events = (pricing.get("pricingPerEvent") or {}).get("actorChargeEvents") or {}
        for event in events.values():
            if not event.get("isPrimaryEvent"):
                continue
            price = event.get("eventPriceUsd")
            if price is None:
                tiers = event.get("eventTieredPricingUsd") or {}
                tier = tiers.get("FREE") or next(iter(tiers.values()), {})
                price = tier.get("tieredEventPriceUsd")
            return round(price * 1000, 4) if price is not None else None
    return None


def slim(item: dict) -> dict:
    """Réduit une fiche du catalogue aux champs utilisés par l'analyse."""
    stats = item.get("stats") or {}
    runs = stats.get("publicActorRunStats30Days") or {}
    pricing = item.get("currentPricingInfo") or {}
    return {
        "id": f"{item.get('username')}/{item.get('name')}",
        "title": item.get("title") or "",
        "description": (item.get("description") or "")[:300],
        "categories": [c for c in (item.get("categories") or []) if c],
        "users_total": stats.get("totalUsers") or 0,
        "users_30d": stats.get("totalUsers30Days") or 0,
        "users_7d": stats.get("totalUsers7Days") or 0,
        "runs_30d": runs.get("TOTAL") or 0,
        "runs_ok_30d": runs.get("SUCCEEDED") or 0,
        "runs_failed_30d": (runs.get("FAILED") or 0) + (runs.get("TIMED-OUT") or 0),
        "rating": stats.get("actorReviewRating") or 0,
        "reviews": stats.get("actorReviewCount") or 0,
        "last_run": stats.get("lastRunStartedAt"),
        "pricing_model": pricing.get("pricingModel") or "FREE",
        "price_per_1000_usd": primary_price_usd(pricing),
        "notice": item.get("notice") or "NONE",
    }


def iter_slice(fetch: Fetch, params: dict, page_size: int = PAGE_SIZE,
               pause: float = 0.3) -> Iterator[dict]:
    """Parcourt une tranche du catalogue (un tri, éventuellement une catégorie).

    L'API filtre des fiches après pagination : une page peut être incomplète
    sans que la tranche soit finie, donc on avance toujours d'une page entière.
    Elle ne renvoie plus rien au-delà de `MAX_OFFSET`, d'où le découpage en
    tranches fait par `download`.
    """
    offset = 0
    while offset < MAX_OFFSET:
        query = urllib.parse.urlencode({**params, "limit": page_size, "offset": offset})
        data = fetch(f"{STORE_URL}?{query}").get("data") or {}
        yield from data.get("items") or []
        offset += page_size
        if offset >= (data.get("total") or 0):
            return
        time.sleep(pause)


def slices(categories: list[str]) -> list[dict]:
    """Tranches à parcourir : chaque tri, globalement puis par catégorie."""
    out = [{"sortBy": sort} for sort in SORTS]
    out += [{"sortBy": sort, "category": cat} for cat in categories for sort in SORTS]
    return out


def download(path: Path, fetch: Fetch = http_get_json, pause: float = 0.3) -> dict:
    """Écrit le catalogue allégé dans `path`. Écriture atomique, sans doublon.

    Renvoie le nombre d'Actors enregistrés et le total annoncé par l'API, pour
    que la couverture réelle soit connue.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    seen: set[str] = set()
    categories: list[str] = []
    announced = 0
    with tmp.open("w", encoding="utf-8") as out:
        def consume(params: dict) -> None:
            nonlocal announced
            def counting_fetch(url: str) -> dict:
                nonlocal announced
                payload = fetch(url)
                if "category" not in params:
                    announced = max(announced, (payload.get("data") or {}).get("total") or 0)
                return payload
            for item in iter_slice(counting_fetch, params, pause=pause):
                row = slim(item)
                for cat in row["categories"]:
                    if cat not in categories:
                        categories.append(cat)
                if row["id"] in seen:
                    continue
                seen.add(row["id"])
                out.write(json.dumps(row, ensure_ascii=False) + "\n")

        for params in slices([]):
            consume(params)
        for params in slices(sorted(categories))[len(SORTS):]:
            consume(params)
    tmp.replace(path)
    return {"saved": len(seen), "announced_total": announced}


def load(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "data/catalog.jsonl")
    result = download(target)
    print(f"{result['saved']} Actors enregistrés dans {target} "
          f"(total annoncé par l'API : {result['announced_total']})")
