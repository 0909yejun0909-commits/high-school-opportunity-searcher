"""tools/opps.py keeps the seen list and tracker out of the conversation.

The slash commands rely on it for dedup, status tracking and deadline
warnings, so a silent bug here means a missed deadline.
"""
import contextlib
import datetime as dt
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
import opps  # noqa: E402


def run(*argv, stdin=None):
    out, err = io.StringIO(), io.StringIO()
    old_stdin = sys.stdin
    if stdin is not None:
        sys.stdin = io.StringIO(stdin)
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = opps.main(list(argv))
    finally:
        sys.stdin = old_stdin
    return code, out.getvalue(), err.getvalue()


class TempData(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self._saved = (opps.DATA, opps.SEEN, opps.TRACKER)
        opps.DATA, opps.SEEN, opps.TRACKER = d, d / "seen.json", d / "tracker.csv"

    def tearDown(self):
        opps.DATA, opps.SEEN, opps.TRACKER = self._saved
        self.tmp.cleanup()


class UrlKey(unittest.TestCase):
    def test_same_page_variants_collapse(self):
        variants = [
            "https://www.Example.org/programs/ssp/",
            "http://example.org/programs/ssp",
            "example.org/programs/ssp?utm_source=x#apply",
        ]
        self.assertEqual(len({opps.url_key(v) for v in variants}), 1)

    def test_different_paths_stay_distinct(self):
        self.assertNotEqual(opps.url_key("https://a.org/x"), opps.url_key("https://a.org/y"))


class Seed(unittest.TestCase):
    def test_seed_file_is_well_formed(self):
        programs = opps.load_seed()
        self.assertGreater(len(programs), 20)
        ids = [p["id"] for p in programs]
        self.assertEqual(len(ids), len(set(ids)), "duplicate seed ids")
        for p in programs:
            for key in ("name", "org", "category", "url", "grades", "cost", "deadline_month",
                        "host_country", "eligible_from"):
                self.assertIn(key, p, f"{p['id']} missing {key}")
            self.assertTrue(p["url"].startswith("https://"), p["id"])
            self.assertIn(p["cost"], {"free", "stipend", "paid", "paid_with_aid", "check"}, p["id"])
            self.assertIn(p["category"], opps.CATEGORIES, p["id"])
            self.assertTrue(0 <= p["deadline_month"] <= 12, p["id"])
            self.assertTrue(set(p["grades"]) <= {8, 9, 10, 11, 12}, p["id"])
            allowed = p["eligible_from"]
            if allowed is not None:
                self.assertTrue(allowed, f"{p['id']}: eligible_from is empty; use null if unknown")
                for code in allowed:
                    self.assertTrue(code in {"*", "EUROPE"} or (len(code) == 2 and code.isupper()),
                                    f"{p['id']}: bad eligible_from code {code!r}")

    def test_seed_covers_more_than_the_us(self):
        hosts = {p["host_country"] for p in opps.load_seed()}
        self.assertTrue({"UK", "CA", "AU"} <= hosts, hosts)

    def test_no_paid_filter_drops_tuition_programs(self):
        hits = opps.filter_seed(opps.load_seed(), cost="no-paid")
        self.assertTrue(hits)
        self.assertFalse([p for p in hits if p["cost"] in opps.COST_PAID])

    def test_grade_and_field_filter(self):
        hits = opps.filter_seed(opps.load_seed(), grade=11, fields=["genomics"])
        self.assertTrue(hits)
        for p in hits:
            self.assertIn(11, p["grades"])


class Countries(unittest.TestCase):
    PROGRAMS = [
        {"id": "us-only", "host_country": "US", "eligible_from": ["US"], "grades": [11]},
        {"id": "anyone", "host_country": "US", "eligible_from": ["*"], "grades": [11]},
        {"id": "europe", "host_country": "UK", "eligible_from": ["EUROPE"], "grades": [11]},
        {"id": "uk-only", "host_country": "UK", "eligible_from": ["UK"], "grades": [11]},
        {"id": "us-abroad", "host_country": "DE", "eligible_from": ["US"], "grades": [11]},
        {"id": "unknown-us", "host_country": "US", "eligible_from": None, "grades": [11]},
        {"id": "online", "host_country": "ONLINE", "eligible_from": ["*"], "grades": [11]},
    ]

    def ids(self, **kw):
        return [p["id"] for p in opps.filter_seed(self.PROGRAMS, **kw)]

    def test_home_country_keeps_only_eligible(self):
        self.assertEqual(self.ids(home="US"), ["us-only", "anyone", "us-abroad", "unknown-us", "online"])
        self.assertEqual(self.ids(home="FR"), ["anyone", "europe", "online"])
        self.assertEqual(self.ids(home="IN"), ["anyone", "online"])

    def test_uk_aliases(self):
        self.assertEqual(self.ids(home="GB"), self.ids(home="uk"))
        self.assertIn("uk-only", self.ids(home="GB"))

    def test_unrecorded_eligibility_is_unverified_at_home_and_hidden_abroad(self):
        p = self.PROGRAMS[5]
        self.assertEqual(opps.eligibility(p, "US"), "unverified")
        self.assertEqual(opps.eligibility(p, "CA"), "no")

    def test_abroad_excludes_home_and_online(self):
        self.assertEqual(self.ids(home="US", abroad=True), ["us-abroad"])
        self.assertEqual(self.ids(home="FR", abroad=True), ["anyone", "europe"])

    def test_international_flag(self):
        self.assertEqual(self.ids(international=True), ["anyone", "online"])

    def test_mediterranean_counts_as_europe(self):
        self.assertEqual(opps.eligibility(self.PROGRAMS[2], "EG"), "yes")

    def test_cli_abroad_requires_home(self):
        code, _, err = run("seed", "--abroad")
        self.assertEqual(code, 2)
        self.assertIn("--home", err)

    def test_real_seed_uk_student_sees_uk_programs(self):
        ids = {p["id"] for p in opps.filter_seed(opps.load_seed(), grade=11, home="UK")}
        self.assertTrue({"uniq", "sutton-trust", "promys-europe"} <= ids, ids)
        self.assertNotIn("nasa-ostem", ids)


class Seen(TempData):
    def test_add_then_check(self):
        code, out, _ = run("seen", "add", stdin=json.dumps([{"url": "https://www.a.org/p/", "name": "A"}]))
        self.assertEqual(code, 0)
        self.assertIn("added=1", out)
        _, out, _ = run("seen", "check", "http://a.org/p", "https://b.org/q")
        self.assertIn("seen\thttp://a.org/p", out)
        self.assertIn("new\thttps://b.org/q", out)

    def test_re_add_updates_not_duplicates(self):
        run("seen", "add", stdin=json.dumps({"url": "https://a.org/p", "fit": 50}))
        _, out, _ = run("seen", "add", stdin=json.dumps({"url": "https://a.org/p/", "fit": 80}))
        self.assertIn("added=0 updated=1 total=1", out)
        self.assertEqual(json.loads(opps.SEEN.read_text())["a.org/p"]["fit"], 80)

    def test_tracked_beats_seen(self):
        run("track", "add", "--program", "A", "--url", "https://a.org/p")
        _, out, _ = run("seen", "check", "https://a.org/p")
        self.assertTrue(out.startswith("tracked"))

    def test_bad_json_is_an_error(self):
        code, _, err = run("seen", "add", stdin="not json")
        self.assertEqual(code, 2)


class Tracker(TempData):
    def test_add_update_list(self):
        self.assertEqual(run("track", "add", "--program", "SSP", "--deadline", "2027-02-15")[0], 0)
        code, out, _ = run("track", "update", "--program", "ssp", "--status", "submitted", "--notes", "sent")
        self.assertEqual(code, 0)
        row = opps.read_tracker()[0]
        self.assertEqual((row["status"], row["notes"]), ("submitted", "sent"))

    def test_duplicate_add_refused(self):
        run("track", "add", "--program", "SSP")
        self.assertEqual(run("track", "add", "--program", "ssp")[0], 1)

    def test_invalid_status_and_date_refused(self):
        self.assertEqual(run("track", "add", "--program", "X", "--status", "maybe")[0], 2)
        self.assertEqual(run("track", "add", "--program", "X", "--deadline", "Feb 1")[0], 2)
        self.assertFalse(opps.TRACKER.exists())

    def test_ambiguous_update_refused(self):
        run("track", "add", "--program", "MIT PRIMES")
        run("track", "add", "--program", "MIT PRIMES USA")
        self.assertEqual(run("track", "update", "--program", "PRIMES", "--status", "preparing")[0], 1)

    def test_formula_cells_neutralized(self):
        run("track", "add", "--program", "X", "--notes", "=HYPERLINK(\"http://evil\")")
        raw = opps.TRACKER.read_text()
        self.assertIn("'=HYPERLINK", raw)


class Deadlines(TempData):
    def test_upcoming_window_and_closed_rows(self):
        ref = dt.date(2026, 10, 23)
        rows = [
            {"program": "Soon", "deadline": "2026-11-01", "status": "interested", "url": ""},
            {"program": "Late", "deadline": "2027-06-01", "status": "interested", "url": ""},
            {"program": "Done", "deadline": "2026-11-02", "status": "submitted", "url": ""},
            {"program": "Gone", "deadline": "2026-11-03", "status": "rejected", "url": ""},
            {"program": "Past", "deadline": "2026-10-01", "status": "preparing", "url": ""},
        ]
        names = [r["program"] for _, _, r in opps.upcoming(rows, 60, ref)]
        self.assertEqual(names, ["Past", "Soon"])

    def test_seed_heads_up_skips_tracked(self):
        ref = dt.date(2026, 10, 23)
        programs = [
            {"name": "Nov One", "url": "https://a.org/n", "deadline_month": 11},
            {"name": "Dec One", "url": "https://a.org/d", "deadline_month": 12},
            {"name": "Mar One", "url": "https://a.org/m", "deadline_month": 3},
            {"name": "Rolling", "url": "https://a.org/r", "deadline_month": 0},
        ]
        heads = opps.seed_heads_up(programs, {"dec one"}, set(), 45, ref)
        self.assertEqual([p["name"] for p in heads], ["Nov One"])

    def test_heads_up_wraps_year_end(self):
        ref = dt.date(2026, 12, 10)
        programs = [{"name": "Jan", "url": "https://a.org/j", "deadline_month": 1},
                    {"name": "Dec", "url": "https://a.org/d", "deadline_month": 12}]
        heads = opps.seed_heads_up(programs, set(), set(), 40, ref)
        self.assertEqual([p["name"] for p in heads], ["Dec", "Jan"])

    def test_ics_output(self):
        ics = Path(self.tmp.name) / "d.ics"
        items = [(5, dt.date(2026, 11, 1), {"program": "Navy SEAP, 2027", "url": "https://x.org", "notes": ""})]
        opps.write_ics(items, ics)
        text = ics.read_text()
        self.assertIn("DTSTART;VALUE=DATE:20261101", text)
        self.assertIn("SUMMARY:Deadline: Navy SEAP\\, 2027", text)
        self.assertTrue(text.startswith("BEGIN:VCALENDAR") and text.rstrip().endswith("END:VCALENDAR"))


if __name__ == "__main__":
    unittest.main()
