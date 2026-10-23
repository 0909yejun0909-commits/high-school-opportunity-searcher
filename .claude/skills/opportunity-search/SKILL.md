---
name: opportunity-search
description: >
  Finds internships, research opportunities and summer programs for a high school student,
  verifies each against the official page, dedups across runs, and returns a ranked list.
  Triggers on: find programs, summer programs, research opportunities, internships for me,
  what should I apply to, /search
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3 tools/opps.py:*), Bash(python tools/opps.py:*), Bash(python3 tools/posting_guard.py:*), Bash(python3 tools/fetch_page.py:*), WebFetch, WebSearch, Agent, AskUserQuestion
---

# Opportunity Search

## Inputs
- `.claude/skills/opportunity-assistant/profile.md` - the student
- `.claude/skills/opportunity-assistant/evaluation.md` - gates and scoring
- `search-queries.md` (this folder; written by `/setup`, git-ignored) - saved queries; if missing or
  still a template, build them from the profile
- `sources.md` (this folder) - where to look
- `data/programs_seed.json` via `python3 tools/opps.py seed ...` - curated leads

Never read `data/seen.json` or `data/tracker.csv` directly; use `tools/opps.py`.

## Optional arguments
- a focus: `/search biology`, `/search paid internships`, `/search local`, `/search math`
- `broad` - all categories and a wider net (also programs one grade ahead, for planning)
- `next-year` - plan for the summer after next (for 9th/10th graders mapping a path)

## Steps

### 1. Frame the search
From the profile work out: **target summer** (the next summer that hasn't started; today's date
decides this), grade at application time, age on June 1 of that summer, region, budget,
citizenship, travel. State these in one line so the student can correct them.

### 2. Gather candidates (aim for 25-50 raw)
a. Seed: `python3 tools/opps.py seed --grade <grade> --cost <...> [--field ...] --json`
   (run once per main interest; `--cost no-paid` if budget is "free only" or needs income).
b. Web: run the saved queries plus 6-12 new ones drawn from `sources.md` sections that match
   the profile - always including **local** queries for the student's city/region and at least
   one query per opportunity type the student wants. Add the target-summer year to queries.
   Never include the student's name, school, or other identifying details in a query.
c. Dedup: `python3 tools/opps.py seen check <url> <url> ...` - drop `tracked`; keep `seen` only
   if this is a `broad` run or the student asked to re-check; keep all `new`.

### 3. Verify each candidate (parallel)
Dispatch `opportunity-fetcher` agents (batches of ~6 URLs each, in parallel) to read each
**official** page and return: name, org, official URL, current-cycle deadline (or "not posted
yet - usual month X"), dates, cost & aid, eligibility (grade, age, citizenship, location),
format, application components, AI policy if stated, guard verdict, and red flags.
Drop candidates that turn out to be: undergrad-only, discontinued, not found, or listicle pages
with no official source.

### 4. Evaluate
Apply the **quick** version of `evaluation.md`: all gates, legitimacy, the five scores, overall,
bucket. Gate FAILs go to a separate "Not eligible" list with the quoted reason - don't hide them,
the student may know something the page doesn't say.

### 5. Save
Pipe the evaluated list to `python3 tools/opps.py seen add` as JSON objects with at least
`url, name, org, category, deadline, overall, bucket, gates` so the next run dedups.

### 6. Present
```
## Opportunities for summer 20XX - <date>
Searched as: grade 10 → applying as 10th grader, age 16 next June, Austin TX, free/aid only, US citizen

### Apply soon (deadline ≤ 30 days)
| # | Program | Type | Deadline | Cost | Overall | Bucket |

### Top matches
| # | Program | Type | Deadline | Cost | Overall | Bucket | Why |

### Local / likely options
...

### Not eligible (and why)
...

### Opens later - set a reminder
(programs whose applications aren't posted yet, with usual month)
```
Keep "Why" to one honest line. Then suggest the next step: `/apply <#>` for one, adding several
to the tracker (`python3 tools/opps.py track add ... --status interested`, ask first), or
`/deadlines` for the calendar.

## Rules
- Every deadline shown must be marked **verified** (read on the official page for this cycle) or
  **usual month** (not yet posted). Never present last year's date as this year's.
- Balance: if fewer than 3 "Likely" options turned up, run extra local searches before presenting.
- Don't pad the list. Twelve real, eligible opportunities beat forty maybes.
