# High School Opportunity Searcher

*Find internships, research opportunities, and summer programs, then actually apply to them.*

A Claude Code workspace for high school students, adapted from
[ai-job-search](https://github.com/ai-job-search-dev/ai-job-search) (MIT). Same idea: fill in
your profile once, let Claude search, check fit honestly, and help you apply. It's rebuilt for
how high school opportunities work: eligibility by grade, age and citizenship, deadlines that
come as early as November, cost and financial aid, recommendation letters, essays you write
yourself, and research positions you get by emailing a professor.

```
/setup          /search                 /apply <program>
  |                |                         |
Your profile   Seed list + web search   Eligibility gates + fit score
(interview or  -> verify official pages  -> plan & checklist with dates
 documents/)   -> rank: reach/target/    -> activities resume
                  likely                 -> essay coaching (your words)
                   |                     -> rec-request emails
               /deadlines                -> reviewer pass
               (+ .ics calendar)              |
                                         /outcome  /interview
                    /outreach  (cold-email labs for research)
```

## Requirements
- [Claude Code](https://claude.com/claude-code) (needs a Claude subscription or API credits)
- Python 3.10+ (no packages needed)

## Install

**1. Clone it** somewhere permanent. Your profile and applications will live in this folder.
```bash
git clone https://github.com/0909yejun0909-commits/high-school-opportunity-searcher.git ~/high-school-opportunity-searcher
```

**2. Make the commands work in every folder** (optional, recommended):
```bash
python3 ~/high-school-opportunity-searcher/install.py
```
This adds `/opp-setup`, `/opp-search`, `/opp-apply`, `/opp-deadlines`, `/opp-outreach`,
`/opp-outcome` and `/opp-interview` to Claude Code everywhere (in `~/.claude/skills/` and
`~/.claude/agents/`). They are small pointers back to the cloned folder, so your data stays in
one place whichever folder you run them from. Asking in plain words ("find me summer research
programs") also works. Re-run the installer if you move the folder;
`python3 install.py --uninstall` removes it. It never touches files it didn't create.

**3. Start:** open Claude Code anywhere (`claude`) and run:
```
/opp-setup          # ~10 minutes, or drop files in documents/ first
/opp-search         # or: /opp-search biology, /opp-search paid internships, /opp-search local
/opp-apply 3        # pick a result number, a URL, or a program name
/opp-deadlines ics  # what's due + a calendar file with 1-week reminders
```
Skipped step 2? Run `claude` inside the cloned folder and use the short names: `/setup`,
`/search`, `/apply`, `/deadlines`, ...

**Updating:** `git -C ~/high-school-opportunity-searcher pull`. Your profile, tracker, documents and
applications are git-ignored, so pulling never overwrites them, and they never get committed if
you push changes to a fork.

## Commands

| Command | What it does |
|---|---|
| `/setup` | Builds your profile: grade, age, location, citizenship, interests, activities, budget, travel |
| `/search [focus]` | Searches a curated list of ~40 well-known programs + the web (directories, universities, national labs, local orgs). Verifies every result on its official page, checks eligibility, ranks by fit, and sorts into reach / target / likely |
| `/apply <program>` | Full eligibility + fit evaluation, a dated checklist, activities resume, essay brainstorm → outline → feedback on *your* draft, recommendation-request emails, and a second-agent review |
| `/deadlines [days] [ics]` | Tracked deadlines plus programs that usually open soon; exports to your calendar |
| `/outreach <topic or professor>` | Finds labs near you, explains their work simply, and helps you write a short cold email asking about research |
| `/outcome <program> <result>` | Updates the tracker; drafts thank-yous, waitlist letters, or declines |
| `/interview <program>` | Prep sheet + mock interview |

## What's different from the job-search version

| ai-job-search | This version |
|---|---|
| Danish job boards | Seed list of US programs + web search (Pathways to Science, universities, NASA/NIH/DoD/DOE labs, local museums/hospitals/city youth programs) |
| CV + cover letter in LaTeX | One-page activities resume (Markdown + print-to-PDF HTML) |
| Writes the cover letter | **Coaches** essays: brainstorms, outlines, gives feedback. Your essays stay your own - many programs forbid AI-written essays, and `/apply` checks each program's policy |
| Salary benchmark | Cost, financial aid, stipend; "needs income" prioritizes paid options |
| Work-permit gate | Grade / age / citizenship / location gates, read from the official page |
| - | Legitimacy check for pay-to-play "honors" programs and sketchy internships |
| - | Cold-email workflow for research positions that are never posted |
| - | Deadline calendar with reminders |

## Safety
- Claude never submits applications, sends emails, or fills in forms. You (and a parent/guardian
  where it matters) do that.
- Searches never include your name or school.
- Your profile, documents, and tracker stay on your computer and are git-ignored.
- Web pages are treated as untrusted and scanned for hidden instructions before Claude reads them
  (`tools/posting_guard.py`, from the original project).

## A note on the seed list
`data/programs_seed.json` lists programs that run most years, with their *usual* deadline month.
Programs change and get cancelled, so `/search` and `/apply` always confirm details on the
official page for the current cycle and label anything unconfirmed. Got a program to add? Add an
entry and run `python3 -m unittest discover -s tests`.

## Files
```
CLAUDE.md                              ground rules for Claude
.claude/commands/                      setup, search, apply, deadlines, outreach, outcome, interview
.claude/skills/opportunity-search/     search workflow, sources, query template
.claude/skills/opportunity-assistant/  profile template, evaluation framework, writing guide
                                       (your filled-in profile.md is created here, git-ignored)
.claude/agents/                        opportunity-fetcher (verifies pages), opportunity-reviewer
install.py                             global /opp-* commands for every folder
data/programs_seed.json                curated programs (leads, not facts)
data/tracker.csv, data/seen.json       your tracker and search history (created on first use)
applications/<program>/                plans, resumes, essay outlines/drafts, emails
documents/                             your source files for /setup
tools/opps.py                          seed filter, dedup, tracker, deadlines, .ics
tools/posting_guard.py, fetch_page.py, robots_check.py, page_decode.py   safe fetching (upstream)
```

## Contributing
The most useful contribution is keeping `data/programs_seed.json` accurate: add a program that
runs most years, or fix one whose rules changed (link the official page in your PR). Run
`python3 -m unittest discover -s tests` before opening a PR. Programs outside the US are welcome.

## License
MIT. Includes tools from ai-job-search, © 2026 Mads Lorentzen.
