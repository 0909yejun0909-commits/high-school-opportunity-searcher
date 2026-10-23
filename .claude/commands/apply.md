# /apply - Evaluate and Prepare an Application

Input (`$ARGUMENTS`): a program URL, a program name, a number from the last `/search` table, or
pasted program text. Load the `opportunity-assistant` skill files first: `profile.md`,
`evaluation.md`, `writing.md`.

## Step 0: Identify and fetch
- Name only → WebSearch for the official page. Number → take it from the last `/search` table.
- Dispatch one `opportunity-fetcher` agent for the official page(s) (overview, eligibility,
  how-to-apply, FAQ). Pasted text: run it through
  `python3 tools/posting_guard.py --text --json <<'PAGE' ... PAGE` and still find the official page.
- Show the guard verdict line.

## Step 1: Evaluate (full)
Run all gates, the legitimacy check, and scoring from `evaluation.md`; present the full output
format. If a gate FAILs, stop there - explain and suggest similar programs the student *is*
eligible for. If URGENT (≤14 days), say what's realistically doable in the time left.

Ask: **Prepare the application?** (Yes / Yes, but just the plan / No)

## Step 2: Application plan
Slug = lowercase-hyphenated program name. Create `applications/<slug>/plan.md`:
- Official link, deadline (verified/unverified), decision date, program dates, cost/aid
- **Checklist** of every component with an owner and a due date working backward from the
  deadline: recommendations asked ≥4 weeks before, essay draft 1 ≥3 weeks before, final review
  ≥3 days before, submit ≥1 day before (portals crash on deadline day)
- Fee and fee-waiver info; whether a parent/guardian signature or form is needed
- AI policy (quoted) or "not stated - assume essays must be your own"

Then record it: `python3 tools/opps.py track add --program "<name>" --org "<org>" --category <cat>
--url <official url> --deadline <YYYY-MM-DD if verified> --status preparing` (if already tracked,
use `track update --status preparing`).

## Step 3: Materials
Follow `writing.md`:
- **Activities resume** → `applications/<slug>/resume.md` + `resume.html` (drafted directly,
  tailored to this program, profile facts only). Only if the program accepts/asks for one, or the
  student wants one for recs.
- **Activities list** (if the form has short activity fields) → `applications/<slug>/activities.md`
  formatted to the form's character limits.
- **Essays** → for each prompt: unpack it, offer 3-4 angles from the profile, ask the digging
  questions, agree an outline → `applications/<slug>/essays/<n>-outline.md`. Then **the student
  writes the draft**. When they paste it, save it and give feedback (coach mode). Do not draft
  the essay unless the student explicitly asks and the program's policy allows it.
- **Recommendation request emails** → `applications/<slug>/rec-requests.md`, one per recommender
  from the profile's list (student chooses who).
- **Problem sets** (math programs): hints and questions only, never solutions.

## Step 4: Review
When the student has drafts ready (this session or later), dispatch the `opportunity-reviewer`
agent with: program name, official URL, the paths of all materials, and `profile.md`. Present its
top 3 changes and any ungrounded claims. Apply resume/email fixes directly; for essays, pass the
feedback to the student to revise.

## Step 5: Wrap up
Show: files created, checklist with dates, and the next concrete action ("Ask Ms. Lee for a rec by
Friday"). Offer `/deadlines --ics` to get the dates into their calendar. Remind: **the student
submits the application themselves** - Claude never logs in or submits.
