import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from engine import catalog


def item(user, name, users=0, **extra):
    base = {"username": user, "name": name, "title": name.title(),
            "stats": {"totalUsers30Days": users,
                      "publicActorRunStats30Days": {"TOTAL": 10, "SUCCEEDED": 7,
                                                    "FAILED": 2, "TIMED-OUT": 1}},
            "categories": ["JOBS", None]}
    base.update(extra)
    return base


class FakeStore:
    """Imite l'API : pages incomplètes, page vide, plafond de décalage."""

    def __init__(self, pages, total):
        self.pages, self.total, self.calls = pages, total, []

    def __call__(self, url):
        params = {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}
        self.calls.append(params)
        key = (params.get("category"), params["sortBy"], int(params["offset"]))
        return {"data": {"total": self.total, "items": self.pages.get(key, [])}}


class SlimTest(unittest.TestCase):
    def test_keeps_usage_and_failures(self):
        row = catalog.slim(item("bob", "jobs", users=12))
        self.assertEqual(row["id"], "bob/jobs")
        self.assertEqual(row["users_30d"], 12)
        self.assertEqual(row["runs_failed_30d"], 3)
        self.assertEqual(row["categories"], ["JOBS"])
        self.assertEqual(row["pricing_model"], "FREE")

    def test_missing_stats_do_not_crash(self):
        row = catalog.slim({"username": "a", "name": "b"})
        self.assertEqual((row["users_30d"], row["runs_30d"], row["title"]), (0, 0, ""))


class PriceTest(unittest.TestCase):
    def test_flat_event_price(self):
        pricing = {"pricingModel": "PAY_PER_EVENT", "pricingPerEvent": {"actorChargeEvents": {
            "start": {"eventPriceUsd": 0.003},
            "row": {"isPrimaryEvent": True, "eventPriceUsd": 0.004}}}}
        self.assertEqual(catalog.primary_price_usd(pricing), 4.0)

    def test_tiered_event_price_uses_free_tier(self):
        pricing = {"pricingModel": "PAY_PER_EVENT", "pricingPerEvent": {"actorChargeEvents": {
            "row": {"isPrimaryEvent": True, "eventTieredPricingUsd": {
                "FREE": {"tieredEventPriceUsd": 0.002}, "GOLD": {"tieredEventPriceUsd": 0.001}}}}}}
        self.assertEqual(catalog.primary_price_usd(pricing), 2.0)

    def test_unknown_or_missing_price(self):
        self.assertIsNone(catalog.primary_price_usd(None))
        self.assertIsNone(catalog.primary_price_usd({"pricingModel": "FLAT_PRICE_PER_MONTH"}))
        self.assertIsNone(catalog.primary_price_usd(
            {"pricingModel": "PAY_PER_EVENT", "pricingPerEvent": {"actorChargeEvents": {}}}))


class PaginationTest(unittest.TestCase):
    def test_incomplete_and_empty_pages_do_not_stop_the_slice(self):
        store = FakeStore({(None, "newest", 0): [item("a", "one")],
                           (None, "newest", 1000): [],
                           (None, "newest", 2000): [item("a", "two")]}, total=2500)
        got = list(catalog.iter_slice(store, {"sortBy": "newest"}, pause=0))
        self.assertEqual([i["name"] for i in got], ["one", "two"])
        self.assertEqual([c["offset"] for c in store.calls], ["0", "1000", "2000"])

    def test_stops_at_api_offset_cap(self):
        store = FakeStore({}, total=10**6)
        list(catalog.iter_slice(store, {"sortBy": "newest"}, pause=0))
        self.assertEqual(len(store.calls), catalog.MAX_OFFSET // catalog.PAGE_SIZE)


class DownloadTest(unittest.TestCase):
    def test_deduplicates_across_slices_and_reports_coverage(self):
        pages = {(None, "popularity", 0): [item("a", "one", 5), item("b", "two")],
                 (None, "newest", 0): [item("a", "one", 5)],
                 ("JOBS", "lastUpdate", 0): [item("c", "three")]}
        store = FakeStore(pages, total=40)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sub" / "catalog.jsonl"
            result = catalog.download(path, fetch=store, pause=0)
            rows = catalog.load(path)
            self.assertFalse(path.with_suffix(".jsonl.tmp").exists())
        self.assertEqual(result, {"saved": 3, "announced_total": 40})
        self.assertEqual(sorted(r["id"] for r in rows), ["a/one", "b/two", "c/three"])
        self.assertIn("JOBS", {c.get("category") for c in store.calls})

    def test_failure_keeps_previous_file(self):
        def broken(url):
            raise RuntimeError("réseau coupé")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.jsonl"
            path.write_text(json.dumps({"id": "old/one"}) + "\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                catalog.download(path, fetch=broken, pause=0)
            self.assertEqual(catalog.load(path), [{"id": "old/one"}])


if __name__ == "__main__":
    unittest.main()
