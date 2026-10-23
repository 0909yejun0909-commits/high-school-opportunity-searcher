#!/usr/bin/env python3
"""State and tracker helper for the high school opportunity search.

Keeps the growing files (seen list, tracker) out of the conversation: the slash
commands call this tool instead of reading them whole. Stdlib only.

Subcommands:
  seed      Filter data/programs_seed.json by grade, field, cost, category.
  seen      check URLs against data/seen.json, or add/update entries (JSON on stdin).
  track     add / update / list rows in data/tracker.csv.
  deadlines Upcoming deadlines from the tracker, plus seed programs that usually
            open soon and are not tracked yet. --ics writes a calendar file.

Examples:
  python3 tools/opps.py seed --grade 10 --field biology --cost no-paid
  python3 tools/opps.py seen check https://example.org/a https://example.org/b
  echo '[{"url": "...", "name": "...", "fit": 78}]' | python3 tools/opps.py seen add
  python3 tools/opps.py track add --program "SSP" --org "Summer Science Program" \\
      --url https://summerscience.org --deadline 2027-02-15 --status interested
  python3 tools/opps.py track update --program "SSP" --status submitted
  python3 tools/opps.py deadlines --days 90 --ics deadlines.ics
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = DATA / "programs_seed.json"
SEEN = DATA / "seen.json"
TRACKER = DATA / "tracker.csv"

TRACKER_FIELDS = ["date_added", "program", "org", "category", "url", "deadline", "status", "notes"]
STATUSES = [
    "interested",   # on the list, not started
    "preparing",    # working on materials
    "submitted",
    "interview",
    "accepted",
    "waitlisted",
    "rejected",
    "declined",     # student turned down an offer
    "withdrawn",
    "missed",       # deadline passed without applying
]
CLOSED = {"accepted", "rejected", "declined", "withdrawn", "missed"}
COST_PAID = {"paid", "paid_with_aid"}
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def today() -> dt.date:
    return dt.date.today()


# ---------------------------------------------------------------- keys / csv

def url_key(url: str) -> str:
    """Normalize a URL so the same page from two searches dedups: no scheme,
    no www., no query/fragment, no trailing slash, lowercase host."""
    url = url.strip()
    if "://" not in url:
        url = "https://" + url
    parts = urlsplit(url)
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = parts.path.rstrip("/")
    return f"{host}{path}"


def csv_safe(value: str) -> str:
    """Stop spreadsheet apps from running a cell as a formula."""
    value = "" if value is None else str(value)
    if value and value[0] in "=+-@\t\r":
        return "'" + value
    return value


def parse_date(value: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(value.strip())
    except (ValueError, AttributeError):
        return None


# ---------------------------------------------------------------- seed

def load_seed() -> list[dict]:
    return json.loads(SEED.read_text(encoding="utf-8"))["programs"]


def filter_seed(programs, grade=None, fields=(), cost="any", category=None):
    out = []
    for p in programs:
        if grade is not None and grade not in p.get("grades", []):
            continue
        if category and p.get("category") != category:
            continue
        if cost == "free" and p.get("cost") != "free":
            continue
        if cost == "no-paid" and p.get("cost") in COST_PAID:
            continue
        if fields:
            hay = " ".join(p.get("fields", []) + [p.get("name", "")]).lower()
            if not any(f.lower() in hay for f in fields) and "varies" not in hay:
                continue
        out.append(p)
    return out


def cmd_seed(args):
    hits = filter_seed(load_seed(), args.grade, args.field or (), args.cost, args.category)
    if args.json:
        print(json.dumps(hits, indent=1, ensure_ascii=False))
        return 0
    for p in hits:
        month = MONTHS[p["deadline_month"]] if p.get("deadline_month") else "rolling"
        print(f"{p['id']}\t{p['name']}\t{p['category']}\t{p['cost']}\t~{month}\t{p['url']}")
    print(f"({len(hits)} programs)", file=sys.stderr)
    return 0


# ---------------------------------------------------------------- seen

def load_seen() -> dict:
    if SEEN.exists():
        return json.loads(SEEN.read_text(encoding="utf-8"))
    return {}


def save_seen(seen: dict) -> None:
    DATA.mkdir(exist_ok=True)
    SEEN.write_text(json.dumps(seen, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def tracked_keys() -> set[str]:
    return {url_key(r["url"]) for r in read_tracker() if r.get("url")}


def cmd_seen(args):
    seen = load_seen()
    if args.action == "check":
        tracked = tracked_keys()
        for url in args.urls:
            k = url_key(url)
            state = "tracked" if k in tracked else ("seen" if k in seen else "new")
            print(f"{state}\t{url}")
        return 0
    # add: JSON list of objects with at least "url"; other fields are kept as-is
    try:
        items = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"error: stdin is not JSON ({e})", file=sys.stderr)
        return 2
    if isinstance(items, dict):
        items = [items]
    added = updated = 0
    for item in items:
        if not isinstance(item, dict) or not item.get("url"):
            print(f"skip: entry without url: {item!r}", file=sys.stderr)
            continue
        k = url_key(item["url"])
        if k in seen:
            seen[k].update(item)
            updated += 1
        else:
            seen[k] = {"first_seen": today().isoformat(), **item}
            added += 1
        seen[k]["last_seen"] = today().isoformat()
    save_seen(seen)
    print(f"added={added} updated={updated} total={len(seen)}")
    return 0


# ---------------------------------------------------------------- tracker

def read_tracker() -> list[dict]:
    if not TRACKER.exists():
        return []
    with TRACKER.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_tracker(rows: list[dict]) -> None:
    DATA.mkdir(exist_ok=True)
    with TRACKER.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=TRACKER_FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: csv_safe(r.get(k, "")) for k in TRACKER_FIELDS})


def find_row(rows, program):
    matches = [r for r in rows if r["program"].lower() == program.lower()]
    if not matches:
        matches = [r for r in rows if program.lower() in r["program"].lower()]
    return matches


def cmd_track(args):
    rows = read_tracker()
    if args.action == "list":
        shown = [r for r in rows if args.all or r["status"] not in CLOSED]
        shown.sort(key=lambda r: r["deadline"] or "9999")
        for r in shown:
            print(f"{r['deadline'] or '—':<10}  {r['status']:<10}  {r['program']}  ({r['org']})")
        print(f"({len(shown)} of {len(rows)} rows)", file=sys.stderr)
        return 0

    if args.status and args.status not in STATUSES:
        print(f"error: status must be one of: {', '.join(STATUSES)}", file=sys.stderr)
        return 2
    if args.deadline and not parse_date(args.deadline):
        print("error: --deadline must be YYYY-MM-DD", file=sys.stderr)
        return 2

    if args.action == "add":
        if not args.program:
            print("error: --program is required", file=sys.stderr)
            return 2
        if any(r["program"].lower() == args.program.lower() for r in rows):
            print(f"error: '{args.program}' is already tracked; use 'track update'", file=sys.stderr)
            return 1
        rows.append({
            "date_added": today().isoformat(), "program": args.program, "org": args.org or "",
            "category": args.category or "", "url": args.url or "", "deadline": args.deadline or "",
            "status": args.status or "interested", "notes": args.notes or "",
        })
        write_tracker(rows)
        print(f"added: {args.program}")
        return 0

    # update
    matches = find_row(rows, args.program or "")
    if len(matches) != 1:
        names = ", ".join(r["program"] for r in matches) or "none"
        print(f"error: need exactly one match for '{args.program}', found: {names}", file=sys.stderr)
        return 1
    row = matches[0]
    for field in ("org", "category", "url", "deadline", "status"):
        val = getattr(args, field)
        if val:
            row[field] = val
    if args.notes:
        row["notes"] = f"{row['notes']} | {args.notes}".strip(" |") if row["notes"] else args.notes
    write_tracker(rows)
    print(f"updated: {row['program']} -> {row['status']}")
    return 0


# ---------------------------------------------------------------- deadlines

def upcoming(rows, days, ref=None):
    ref = ref or today()
    out = []
    for r in rows:
        d = parse_date(r.get("deadline", ""))
        if not d or r["status"] in CLOSED or r["status"] == "submitted":
            continue
        delta = (d - ref).days
        if delta <= days:
            out.append((delta, d, r))
    out.sort(key=lambda t: t[0])
    return out


def seed_heads_up(programs, tracked_names, tracked_urls, days, ref=None):
    """Seed programs whose usual deadline month falls inside the window and that
    the student has not added to the tracker yet."""
    ref = ref or today()
    end = ref + dt.timedelta(days=days)
    months = set()
    d = ref.replace(day=1)
    while d <= end:
        months.add(d.month)
        d = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    out = []
    for p in programs:
        m = p.get("deadline_month") or 0
        if m in months and p["name"].lower() not in tracked_names and url_key(p["url"]) not in tracked_urls:
            out.append(p)
    # sort by how soon the month comes up, starting from this month
    out.sort(key=lambda p: (p["deadline_month"] - ref.month) % 12)
    return out


def ics_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def write_ics(items, path: Path) -> None:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//hs-opportunity-search//EN", "CALSCALE:GREGORIAN"]
    for _, d, r in items:
        uid = f"{url_key(r.get('url') or r['program'])}-{d.isoformat()}@hs-opportunity-search"
        lines += [
            "BEGIN:VEVENT",
            f"UID:{ics_escape(uid)}",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(d + dt.timedelta(days=1)).strftime('%Y%m%d')}",
            f"SUMMARY:{ics_escape('Deadline: ' + r['program'])}",
            f"DESCRIPTION:{ics_escape((r.get('url') or '') + ' ' + (r.get('notes') or ''))}",
            "BEGIN:VALARM", "ACTION:DISPLAY", "TRIGGER:-P7D", f"DESCRIPTION:{ics_escape(r['program'] + ' due in 1 week')}", "END:VALARM",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    path.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8")


def cmd_deadlines(args):
    rows = read_tracker()
    items = upcoming(rows, args.days)
    print(f"## Deadlines in the next {args.days} days (from tracker)")
    if not items:
        print("none")
    for delta, d, r in items:
        flag = "OVERDUE" if delta < 0 else ("THIS WEEK" if delta <= 7 else f"in {delta} days")
        print(f"{d.isoformat()}  [{flag}]  {r['program']}  status={r['status']}")
    if not args.no_seed:
        names = {r["program"].lower() for r in rows}
        urls = {url_key(r["url"]) for r in rows if r.get("url")}
        heads = seed_heads_up(load_seed(), names, urls, args.days)
        print(f"\n## Usually due in this window, not tracked yet (verify dates on the official site)")
        if not heads:
            print("none")
        for p in heads:
            print(f"~{MONTHS[p['deadline_month']]}  {p['name']}  ({p['cost']}, grades {p['grades']})  {p['url']}")
    if args.ics:
        write_ics([i for i in items if i[0] >= 0], Path(args.ics))
        print(f"\nwrote {args.ics}")
    return 0


# ---------------------------------------------------------------- main

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("seed")
    s.add_argument("--grade", type=int, help="grade the student is in NOW (9-12); programs list grades at time of applying")
    s.add_argument("--field", action="append", help="interest keyword; repeatable")
    s.add_argument("--cost", choices=["any", "free", "no-paid"], default="any")
    s.add_argument("--category", choices=["research", "summer_program", "internship", "math"])
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_seed)

    s = sub.add_parser("seen")
    s.add_argument("action", choices=["check", "add"])
    s.add_argument("urls", nargs="*")
    s.set_defaults(func=cmd_seen)

    s = sub.add_parser("track")
    s.add_argument("action", choices=["add", "update", "list"])
    for f in ("program", "org", "category", "url", "deadline", "status", "notes"):
        s.add_argument(f"--{f}")
    s.add_argument("--all", action="store_true", help="list: include closed rows")
    s.set_defaults(func=cmd_track)

    s = sub.add_parser("deadlines")
    s.add_argument("--days", type=int, default=60)
    s.add_argument("--ics", help="also write upcoming tracker deadlines to this .ics file")
    s.add_argument("--no-seed", action="store_true")
    s.set_defaults(func=cmd_deadlines)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
