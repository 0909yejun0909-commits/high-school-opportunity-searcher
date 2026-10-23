# /setup - Build the Student Profile

Fill in `.claude/skills/opportunity-assistant/profile.md` and generate
`.claude/skills/opportunity-search/search-queries.md`. Safe to re-run: it updates, never wipes.

Both files are personal and git-ignored. If `profile.md` doesn't exist yet, start from a copy of
`profile.template.md` in the same folder; same for `search-queries.template.md`. Never write
personal details into the `.template.md` files - those are committed and public.

## Step 0: Choose a path

Check `documents/` (Glob). Then ask with AskUserQuestion:
- **Read my documents** (only if files exist) - transcript, activities list, resume, old essays,
  award certificates in `documents/`
- **Paste a resume / activities list** in chat
- **Interview me** - about 10 minutes of questions

Mention: you can skip any question; nothing leaves this computer except search queries, which
never include your name or school.

## Step 1: Gather

**Documents / paste:** extract every fact into the profile structure. Then list what's missing
from the *decision-critical* fields and ask only for those: grade, age next summer,
state/country, citizenship/residency, travel, budget, needs income, interests, summer goal.

**Interview:** ask in small batches (2-4 questions per message), in this order, and dig for
specifics - hours, results, what they actually did:
1. Grade, graduation year, age next June, city/state/country, school type.
2. Citizenship/residency (explain why: federal and many university programs require it).
   Optional background flags - explain that several free programs prioritize first-gen,
   low-income, or underrepresented students, and that it's entirely their choice to include.
3. Interests: which subjects/fields excite them, and the story of *how* they got interested.
4. Classes: strongest subjects, advanced courses, GPA (as the school reports it), test scores if any.
5. Activities, clubs, sports, jobs, volunteering - for each: role, years, hours/week, what they did.
6. Projects or research they've done on their own (code, experiments, writing, art, a business).
7. Competitions and awards.
8. Skills: programming languages, lab skills, tools, spoken languages.
9. Logistics: can they live away from home? for how long? summer dates available? hours during
   the school year? driver's license/transit? budget? do they need to earn money?
10. What they want from next summer; deal-breakers.
11. Teachers or mentors who know them well (name + subject) - for recommendation planning.
12. Ask for a paragraph they've written (any school essay) to capture their writing voice -
    note 3-5 observations in **Writing voice**, don't store the essay in the profile.

## Step 2: Confirm and write

Show a compact summary of the profile and the inferred **target summer** (next summer that hasn't
started) and **grade at application time**. Apply corrections, then write `profile.md` -
replace placeholders with facts, leave unknown fields as `[PLACEHOLDER]`, remove the empty
example bullets for sections that have real entries.

## Step 3: Generate search queries

Rewrite `search-queries.md` from its template:
- profile summary line
- the `opps.py seed` command(s) with the right `--grade`, `--cost` and `--field` values
- 4-8 queries per category (research, internships, summer programs, local), built from interests
  × type × region × next-summer year. Use `sources.md` for ideas. Never include name or school.
  Example: `"high school summer research program" neuroscience 2027`,
  `"high school internship" Austin TX 2027 paid`, `site:.edu "high school" "summer research" "Texas"`

## Step 4: Next steps

Tell the student:
- `/search` to find opportunities now
- `/deadlines` to see what usually opens soon (some deadlines are in **November-December**, e.g.
  Navy SEAP, NSLI-Y, RSI, MIT PRIMES - earlier than most students expect)
- Add `documents/` material any time and re-run `/setup`
