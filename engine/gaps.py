"""Mesure de la demande et de la concurrence dans le catalogue Apify.

Entrée : le fichier JSONL produit par `engine.catalog`. Toutes les mesures
portent sur les Actors de la communauté (hors compte officiel `apify`).
« Utilisateurs » désigne les utilisateurs uniques sur 30 jours d'un Actor ;
un même client compte une fois par Actor utilisé.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from engine.catalog import load

# Plateformes dont les conditions d'utilisation interdisent la collecte
# automatisée ou qui la combattent activement. Liste indicative, non juridique.
RESTRICTED = (
    "instagram tiktok linkedin facebook twitter x.com youtube google amazon reddit "
    "indeed threads telegram whatsapp pinterest snapchat zillow airbnb booking "
    "tripadvisor yelp glassdoor apollo zoominfo shopify ebay walmart aliexpress "
    "alibaba 1688 taobao douyin xiaohongshu rednote trustpilot"
).split()
_RESTRICTED_RE = re.compile(r"\b(" + "|".join(map(re.escape, RESTRICTED)) + r")\b")

# Mots trop génériques pour désigner la cible d'un Actor.
STOPWORDS = set(
    "scraper scrapers scraping api apis data extractor extract crawler tool tools and "
    "the for with by to of in a an pro fast free cheap best no login search results "
    "result export actor mcp server ai all get finder monitor tracker leads lead email "
    "emails from your new only real time realtime bulk advanced simple easy ultimate "
    "premium official unofficial lite plus full super smart universal global any every "
    "my our us usa uk eu".split()
)


def community(rows: list[dict]) -> list[dict]:
    return [r for r in rows if not r["id"].startswith("apify/")]


def percentile(sorted_desc: list[int], q: float) -> int:
    """Valeur au quantile `q` d'une liste triée par ordre décroissant."""
    if not sorted_desc:
        return 0
    return sorted_desc[min(len(sorted_desc) - 1, int(len(sorted_desc) * (1 - q)))]


def usage_distribution(rows: list[dict]) -> dict:
    users = sorted((r["users_30d"] for r in rows), reverse=True)
    total = sum(users) or 1
    n = len(users) or 1
    return {
        "actors": len(users),
        "users_30d_total": sum(users),
        "share_actors_at_most": {
            str(t): round(sum(1 for u in users if u <= t) / n, 4) for t in (1, 10, 50, 200)},
        "share_of_usage_top_1pct": round(sum(users[: max(1, n // 100)]) / total, 4),
        "share_of_usage_top_10pct": round(sum(users[: max(1, n // 10)]) / total, 4),
    }


def author_distribution(rows: list[dict]) -> dict:
    per_author: dict[str, int] = defaultdict(int)
    for r in rows:
        per_author[r["id"].split("/")[0]] += r["users_30d"]
    totals = sorted(per_author.values(), reverse=True)
    return {
        "authors": len(totals),
        "users_30d_percentiles": {
            str(q): percentile(totals, q) for q in (0.5, 0.75, 0.9, 0.95, 0.99)},
        "totals_desc": totals,
    }


def revenue_estimate(rows: list[dict], monthly_payout_usd: float, targets=(100, 500, 1000)) -> dict:
    """Ordre de grandeur : versement mensuel déclaré / usage mesuré.

    Très grossier : les comptes gratuits ne paient rien et le revenu par
    utilisateur varie fortement d'un Actor à l'autre.
    """
    authors = author_distribution(rows)
    total = sum(authors["totals_desc"]) or 1
    per_user = monthly_payout_usd / total
    out = {"usd_per_user_month": round(per_user, 2), "targets": {}}
    for target in targets:
        needed = target / per_user
        reaching = sum(1 for t in authors["totals_desc"] if t >= needed)
        out["targets"][str(target)] = {
            "users_30d_needed": round(needed),
            "authors_reaching": reaching,
            "share_of_authors": round(reaching / (authors["authors"] or 1), 4),
        }
    out["median_author_usd_month"] = round(per_user * authors["users_30d_percentiles"]["0.5"], 2)
    out["p75_author_usd_month"] = round(per_user * authors["users_30d_percentiles"]["0.75"], 2)
    out["p90_author_usd_month"] = round(per_user * authors["users_30d_percentiles"]["0.9"], 2)
    return out


def is_restricted(row: dict) -> bool:
    return bool(_RESTRICTED_RE.search(f"{row['title']} {row['id']}".lower()))


def restricted_share(rows: list[dict]) -> dict:
    total = sum(r["users_30d"] for r in rows) or 1
    hit = [r for r in rows if is_restricted(r)]
    return {
        "share_of_actors": round(len(hit) / (len(rows) or 1), 4),
        "share_of_usage": round(sum(r["users_30d"] for r in hit) / total, 4),
    }


def target_key(title: str) -> str | None:
    """Cible d'un Actor : premier mot significatif de son titre."""
    for word in re.findall(r"[a-z0-9][a-z0-9.]*", title.lower()):
        if word not in STOPWORDS and len(word) > 2 and not word.isdigit():
            return word
    return None


def failure_rate(row: dict) -> float:
    return row["runs_failed_30d"] / row["runs_30d"] if row["runs_30d"] else 0.0


def targets(rows: list[dict], min_users: int = 80) -> list[dict]:
    """Par cible : nombre d'Actors, concurrents sérieux, demande et leader."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        key = target_key(r["title"])
        if key:
            groups[key].append(r)
    out = []
    for key, members in groups.items():
        users = sum(r["users_30d"] for r in members)
        if users < min_users:
            continue
        top = max(members, key=lambda r: r["users_30d"])
        out.append({
            "target": key,
            "actors": len(members),
            "serious_actors": sum(1 for r in members if r["users_30d"] >= 10),
            "users_30d": users,
            "leader": top["id"],
            "leader_users_30d": top["users_30d"],
            "leader_failure_rate": round(failure_rate(top), 2),
            "restricted": any(is_restricted(r) for r in members[:1]) or key in RESTRICTED,
        })
    return sorted(out, key=lambda t: -t["users_30d"])


def fragile_leaders(rows: list[dict], min_users: int = 100, min_runs: int = 100,
                    min_failure: float = 0.25) -> list[dict]:
    """Actors très utilisés mais défaillants : la seule place vraiment à prendre."""
    out = []
    for r in rows:
        if r["users_30d"] < min_users or r["runs_30d"] < min_runs:
            continue
        rate = failure_rate(r)
        if rate >= min_failure or r["notice"] != "NONE":
            out.append({"id": r["id"], "users_30d": r["users_30d"],
                        "failure_rate": round(rate, 2), "notice": r["notice"],
                        "restricted": is_restricted(r)})
    return sorted(out, key=lambda r: -r["users_30d"])


def report(rows: list[dict], monthly_payout_usd: float = 1_700_000) -> dict:
    rows = community(rows)
    authors = author_distribution(rows)
    authors.pop("totals_desc")
    all_targets = targets(rows)
    return {
        "usage": usage_distribution(rows),
        "authors": authors,
        "revenue_estimate": revenue_estimate(rows, monthly_payout_usd),
        "restricted_platforms": restricted_share(rows),
        "crowded_open_data": [t for t in all_targets
                              if t["actors"] >= 100 and t["leader_users_30d"] <= 30][:15],
        "fragile_leaders": fragile_leaders(rows),
        "fragile_leaders_allowed": [r for r in fragile_leaders(rows) if not r["restricted"]],
    }


if __name__ == "__main__":
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "data/catalog.jsonl")
    print(json.dumps(report(load(source)), ensure_ascii=False, indent=2))
