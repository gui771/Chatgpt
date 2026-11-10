import unittest

from engine import gaps


def row(actor_id, users, title=None, runs=0, failed=0, notice="NONE"):
    return {"id": actor_id, "title": title or actor_id.split("/")[1], "users_30d": users,
            "runs_30d": runs, "runs_failed_30d": failed, "notice": notice}


class DistributionTest(unittest.TestCase):
    def test_usage_shares(self):
        rows = [row(f"a/n{i}", 1) for i in range(9)] + [row("b/big", 91)]
        dist = gaps.usage_distribution(rows)
        self.assertEqual(dist["share_actors_at_most"]["1"], 0.9)
        self.assertEqual(dist["share_of_usage_top_10pct"], 0.91)

    def test_empty_catalog(self):
        self.assertEqual(gaps.usage_distribution([])["users_30d_total"], 0)
        self.assertEqual(gaps.percentile([], 0.5), 0)

    def test_authors_sum_their_actors(self):
        rows = [row("a/x", 3), row("a/y", 4), row("b/z", 1)]
        self.assertEqual(gaps.author_distribution(rows)["totals_desc"], [7, 1])

    def test_official_account_excluded(self):
        rows = [row("apify/instagram-scraper", 999), row("a/x", 1)]
        self.assertEqual([r["id"] for r in gaps.community(rows)], ["a/x"])


class RevenueTest(unittest.TestCase):
    def test_users_needed_and_authors_reaching(self):
        rows = [row("a/x", 600), row("b/y", 300), row("c/z", 100)]
        est = gaps.revenue_estimate(rows, monthly_payout_usd=2000)
        self.assertEqual(est["usd_per_user_month"], 2.0)
        self.assertEqual(est["targets"]["1000"]["users_30d_needed"], 500)
        self.assertEqual(est["targets"]["1000"]["authors_reaching"], 1)
        self.assertEqual(est["targets"]["100"]["authors_reaching"], 3)


class TargetTest(unittest.TestCase):
    def test_target_key_skips_generic_words(self):
        self.assertEqual(gaps.target_key("Fast Free SEC EDGAR Scraper"), "sec")
        self.assertIsNone(gaps.target_key("Best Free Scraper 2026"))

    def test_restricted_platforms_matched_on_word_boundaries(self):
        self.assertTrue(gaps.is_restricted(row("a/x", 1, "LinkedIn Jobs Scraper")))
        self.assertFalse(gaps.is_restricted(row("a/x", 1, "Googleplex Tour Finder")))

    def test_targets_group_and_count_serious_competitors(self):
        rows = [row("a/s1", 90, "SEC Filings"), row("b/s2", 2, "SEC Scraper"),
                row("c/o", 5, "Other Thing")]
        out = gaps.targets(rows, min_users=80)
        self.assertEqual(len(out), 1)
        self.assertEqual((out[0]["target"], out[0]["actors"], out[0]["serious_actors"],
                          out[0]["leader"]), ("sec", 2, 1, "a/s1"))

    def test_fragile_leaders_need_usage_and_failures(self):
        rows = [row("a/broken", 500, "Jobs Feed", runs=200, failed=100),
                row("b/fine", 500, "Jobs Feed", runs=200, failed=2),
                row("c/tiny", 5, "Jobs Feed", runs=200, failed=200),
                row("d/maint", 300, "Reddit Lite", runs=200, notice="UNDER_MAINTENANCE")]
        out = gaps.fragile_leaders(rows)
        self.assertEqual([r["id"] for r in out], ["a/broken", "d/maint"])
        self.assertEqual([r["restricted"] for r in out], [False, True])

    def test_report_runs_on_small_catalog(self):
        rep = gaps.report([row("a/x", 10, "Thing", runs=5)])
        self.assertEqual(rep["usage"]["actors"], 1)
        self.assertNotIn("totals_desc", rep["authors"])


if __name__ == "__main__":
    unittest.main()
