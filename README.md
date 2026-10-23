<h1 align="center">High School Opportunity Searcher</h1>

<p align="center">
  <b>Find internships, research opportunities, and summer programs that you can actually get into, at home or abroad, and stop missing the deadlines.</b>
</p>

<p align="center">
  <a href="https://github.com/0909yejun0909-commits/high-school-opportunity-searcher/actions/workflows/ci.yml"><img src="https://github.com/0909yejun0909-commits/high-school-opportunity-searcher/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT license">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/built%20for-Claude%20Code-d97757" alt="Built for Claude Code">
</p>

<p align="center">
  <a href="#install-5-minutes">Install</a> ·
  <a href="docs/GUIDE.md"><b>How to use it (guide)</b></a> ·
  <a href="#commands">Commands</a> ·
  <a href="#when-to-start">When to start</a> ·
  <a href="#privacy--safety">Privacy</a> ·
  <a href="#faq">FAQ</a>
</p>

---

Finding a good summer opportunity in high school is hard. The best programs are scattered across
hundreds of university, lab and nonprofit websites. Each has its own rules about grade, age,
citizenship and where you live. Deadlines come as early as **November**. Lists online mix free,
highly selective programs with expensive camps that accept almost everyone, and many good
research spots are never posted at all.

**High School Opportunity Searcher** turns [Claude Code](https://claude.com/product/claude-code)
into a personal opportunity counselor. You tell it about yourself once. Then it:

- 🔎 **Searches** a curated list of well-known programs *and* the live web (universities, national labs and research
  institutes, hospitals, museums, city youth programs near you), in your country's terms and language
- 🌍 **Works in any country**, and can look abroad: international summer schools, research institutes overseas,
  and fully funded exchanges, with checks for visas, language, and whether financial aid covers international students
- ✅ **Checks every result on the program's official website** for this year's deadline, cost, and who can apply,
  and labels anything it couldn't confirm
- 🎯 **Tells you honestly** which ones you're eligible for, how well each one fits, and which are reach / target / likely
- 📅 **Keeps track of deadlines** and exports them to your calendar with reminders
- ✍️ **Helps you apply**: dated checklist, one-page activities resume, recommendation-request emails,
  and coaching on essays *you* write
- 📧 **Gets you research positions that aren't posted** by finding labs near you and helping you email professors

It works for **research programs, internships (paid and volunteer), summer programs, math camps,
writing workshops, exchanges, and more**, in any subject. It also works wherever you live:
the curated list covers the US, UK, Canada, Europe, Israel, Australia and Singapore, and the
live search covers everywhere else.

## What it looks like

Here's part of a real `/opp-search` result for a **made-up** 10th grader in Austin, TX
interested in biology (test run, October 2026; your results will depend on your profile):

> **Searched as:** 10th grader now (a rising junior in summer 2027), age 16 next June, Austin TX, free or need-based aid only, US citizen.
>
> **The main finding:** most of the best-known biology research programs only take students who are **juniors when they apply**.
> Your realistic options this year are local research, a few programs that accept sophomores, and research you set up yourself.
>
> | # | Program | Type | Deadline | Cost | Fit | Bucket |
> |---|---|---|---|---|---|---|
> | 2 | UT Austin High School Research Academy | 5-week lab research, commute | March 2027 (month posted, no day yet) | $4,500, limited need-based scholarships | 77 | Target |
> | 4 | Welch Summer Scholar Program | 5-week residential lab research | Apr 4, 2027 (verified) | Free | 67 | Target |
> | 7 | Navy SEAP | 8-week lab apprenticeship | Nov 30, 2026 (verified) | $4,000 stipend | 57 | Reach |
>
> **Not eligible (and why):** Summer Science Program, *"open only to high school juniors"* → apply in 2028 ...
>
> **Next step:** start with `/opp-apply HSRA` and `/opp-outreach` for a UT lab.

It also listed local options (a paid city internship program, emailing nearby labs, the regional
science fair), explained *why* more than a dozen programs were out of reach this year, and said when to
come back for them.

## Install (5 minutes)

**You need:**
1. **Claude Code**: [install guide](https://code.claude.com/docs/en/setup). It requires a paid Claude plan or Anthropic API credits.
2. **Python 3.10 or newer**: already on most Macs and Linux machines (check with `python3 --version`), or [download it](https://www.python.org/downloads/). Nothing else to install.
3. **Git**: to download this project (or use GitHub's green **Code → Download ZIP** button instead).

**Then:**

```bash
# 1. Download it to a permanent place. Your profile and applications will live here.
git clone https://github.com/0909yejun0909-commits/high-school-opportunity-searcher.git ~/high-school-opportunity-searcher

# 2. Make the commands work from any folder (recommended)
python3 ~/high-school-opportunity-searcher/install.py

# 3. Start Claude Code anywhere and set up your profile
claude
```
Then type **`/opp-setup`** inside Claude Code. That's it.

> Skipped step 2? Open Claude Code *inside* the folder (`cd ~/high-school-opportunity-searcher && claude`)
> and use the short names (`/setup`, `/search`, `/apply`, ...). Everything else is the same.

## Your first 20 minutes

| Step | Type | What happens |
|---|---|---|
| 1 | `/opp-setup` | About 10 minutes of questions: grade, age, location, citizenship, interests, classes, activities, budget, whether you can travel. Skip anything you want. |
| 2 | `/opp-search` | Searches, checks official pages, and gives you a ranked list (takes a few minutes). |
| 3 | `/opp-deadlines ics` | Shows what's due soon and makes a calendar file with reminders a week before each deadline. |
| 4 | `/opp-apply 2` | Pick a result by number. You get an eligibility and fit check, then a dated plan for applying. |

**Full walkthrough with examples, tips and troubleshooting: [docs/GUIDE.md](docs/GUIDE.md)**

## Commands

| Command | Use it to... |
|---|---|
| `/opp-setup` | Build or update your profile (interview, paste a resume, or read files you drop in `documents/`) |
| `/opp-search [focus]` | Find opportunities. Try `biology`, `paid internships`, `local`, `math`, `abroad`, `international`, `Germany`, `next-year` |
| `/opp-apply <# / name / link>` | Get a full fit check, then an application plan, activities resume, essay coaching, rec-request emails, and a review |
| `/opp-deadlines [days] [ics]` | See what's due and what usually opens soon, and export a calendar file |
| `/opp-outreach <topic or professor>` | Find labs near you and write a short email asking to do research |
| `/opp-outcome <program> <result>` | Record submitted / interview / accepted / rejected, and get the right follow-up email |
| `/opp-interview <program>` | Get a prep sheet and a mock interview |

You can also just talk to it: *"find me free summer programs for engineering,"*
*"am I eligible for RSI?,"* or *"what research programs in Europe can I apply to from India?"* work too.

## When to start

Many students start looking in March, when most deadlines have already passed. A typical
year for **US summer programs** looks like this:

| When | What's due | What to do |
|---|---|---|
| **Aug-Nov** | Earliest deadlines: Navy SEAP, NSLI-Y (study abroad), some research programs | `/opp-setup`, `/opp-search`, ask teachers about recommendations |
| **Dec-Jan** | RSI, MIT PRIMES, TASS, YYGS, many research programs | Apply. Email labs (`/opp-outreach`) over winter break |
| **Feb-Mar** | The biggest wave: most university summer programs, internships, MITES, SSP | Keep `/opp-deadlines` handy |
| **Mar-Apr** | Math camps (Ross, PROMYS, Mathcamp), writing workshops, local internships | Problem sets, writing samples |
| **Apr-May** | Decisions arrive | `/opp-outcome` to track results, accept, decline, or join waitlists |

**Outside the US?** The pattern is the same, but measured from *your* long break: deadlines
usually fall 4-8 months before it. Australia's NYSF, which runs in January, closes around July.
UK summer schools mostly close January-April. Exchanges such as CBYX and YES Abroad close
around November for the *following* school year. Programs abroad also need time for a visa,
so start a month or two earlier.

**9th and 10th graders:** many top programs are for juniors. Run `/opp-search next-year` to plan
ahead and use this year to build the skills and projects those programs look for.

## How it decides what's a good fit

Every opportunity goes through the same steps, defined in
[`evaluation.md`](.claude/skills/opportunity-assistant/evaluation.md):

1. **Eligibility checks** (pass/fail, quoted from the official page): grade, age, citizenship and
   residency, deadline, dates and travel, cost after financial aid
2. **Legitimacy check**: flags pay-to-play "honors" programs, mail-in "nominations",
   companies that use a university's name, and internships that ask for money or an SSN early
3. **Fit score** (0-100): interest, readiness, value, odds of getting in, logistics
4. **Bucket**: Reach / Target / Likely. It aims for a balanced list with a backup plan you
   control (like emailing labs), so your summer doesn't depend on one admissions decision

## Privacy & safety

This was built with the fact that most users are minors in mind.

- 🔒 **Your data stays on your computer.** Your profile, tracker, documents and applications are
  *git-ignored*, so they're never uploaded, even if you push changes to a fork.
- 🙈 **Searches never include your name or school.** It searches by interest, grade and region only.
- ✋ **It never submits, sends, or fills in anything.** Claude drafts; you (and a parent or
  guardian where it matters) review and send.
- 🧑‍🤝‍🧑 **It tells you to involve a parent or guardian** for overnight programs, travel, and in-person meetings with adults.
- 🛡️ **Web pages are treated as untrusted.** Each page is scanned for hidden text and instructions aimed at AI before Claude reads it.

## Your essays stay yours

Many programs **ban AI-written application essays**, and admissions readers can tell. So this tool
**coaches** instead of writing: it helps you pick a strong story, asks questions that bring out the
details, outlines with you, and gives feedback on *your* draft. Before you start, it looks up each
program's AI policy and tells you what it says. Factual materials (activities resume, emails,
checklists) it drafts directly, using only facts from your profile.

## FAQ

**Is it free?** The project is free and open source. Claude Code needs a paid Claude plan or API credits.

**I don't live in the US. Does it work for me?** Yes. Tell `/opp-setup` your country, your
school year as your school names it (Year 12, JC1, lycée...), and when your long break is
(December-February in the southern hemisphere). It searches with your local terms and language.
It only lists programs you're actually allowed to apply to: for example, it knows most US
government labs are citizens-only, UK programs like UNIQ are UK-state-school only, and PROMYS
Europe is for students living in Europe. The curated list is strongest for the US and UK, so
for other countries the live web search does most of the work. Additions from your country are
very welcome.

**Can it find programs abroad?** Yes: `/opp-search abroad`, `/opp-search international`, or
`/opp-search Japan`. It checks whether international students are accepted, whether financial aid
covers them (often it doesn't), the language of instruction, visa needs, and the real total cost
including travel. It also finds fully funded exchanges like CBYX and YES Abroad.

**How accurate are the deadlines?** Anything marked *verified* was read on the official site during that
search. The built-in list only stores the *usual* month, and the tool never presents last year's
date as this year's. Still double-check before you submit. Programs change every year.

**Can my counselor or parent use it with me?** Yes. It's a good thing to do together, especially
the budget, travel and "which ones should I apply to" parts.

**Will it apply for me?** No, on purpose. You submit everything yourself.

**More questions?** See the [troubleshooting section of the guide](docs/GUIDE.md#troubleshooting).

## Project layout

```
CLAUDE.md                              ground rules Claude follows (safety, honesty, essays)
docs/GUIDE.md                          how to use every command
install.py                             adds the /opp-* commands to every folder
.claude/commands/                      the commands: setup, search, apply, deadlines, outreach, outcome, interview
.claude/skills/opportunity-search/     search workflow, where to look, your saved queries
.claude/skills/opportunity-assistant/  profile template, evaluation framework, writing guide
.claude/agents/                        page checker (opportunity-fetcher), application reviewer (opportunity-reviewer)
data/programs_seed.json                curated list of ~55 programs in 8 countries + exchanges (starting points, not final facts)
tools/opps.py                          tracker, deadlines, calendar export, dedup
tools/posting_guard.py & friends       safe page fetching (from ai-job-search)

Created as you use it (git-ignored, private):
.claude/skills/opportunity-assistant/profile.md   your profile
data/tracker.csv, data/seen.json                  your applications and search history
applications/<program>/                           plans, resumes, essay outlines/drafts, emails
documents/                                        files you give /opp-setup
```

## Contributing

The most valuable help is **keeping the program list accurate**. Add a program that runs most
years, fix one whose rules changed, or add programs from your state or country. **Programs
outside the US are especially wanted.** Edit
[`data/programs_seed.json`](data/programs_seed.json) (set `host_country` and who can apply in `eligible_from`; the file's `_about` explains the fields), link the official page in your pull
request, and run the tests:

```bash
python3 -m unittest discover -s tests
```

Bug reports and ideas: [open an issue](https://github.com/0909yejun0909-commits/high-school-opportunity-searcher/issues).

## Credits & license

Adapted from [ai-job-search](https://github.com/ai-job-search-dev/ai-job-search) by Mads Lorentzen,
a Claude Code framework for job seekers. The safe-fetching tools come from that project.
This project rebuilds the workflow for high school students.

MIT licensed. Not affiliated with Anthropic or with any program listed here.
