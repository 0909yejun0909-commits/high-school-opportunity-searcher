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
from the *decision-critical* fields and ask only for those: school year, age at the next long
break, city/region/country, citizenship/residency, break dates, open to going abroad, travel,
budget, needs income, interests, goal for the break.

**Interview:** ask in small batches (2-4 questions per message), in this order, and dig for
specifics - hours, results, what they actually did:
1. Country, city and region; school year *as their school names it* (Grade 10, Year 12, S5,
   JC1...) and graduation year; age at the start of their next long break; school type.
   Work out the **US-equivalent grade** yourself (UK Year 12 = 11; Australian/Canadian grades
   match US numbers; for other systems count years before university: the last year = 12) and
   confirm it with the student. Record the country as an ISO code (US, UK, CA, IN, SG...).
2. **When is your main school break?** Don't assume June-August: Australia, New Zealand,
   southern Africa and much of South America have their long break around December-February,
   and some countries split it. Every date in the search is planned around this.
3. Citizenship(s) and residency status (explain why: US federal labs usually need US citizenship,
   many UK programs need UK residency or a state school, programs abroad may need a visa).
   Optional background flags - explain that several free programs prioritize first-gen,
   low-income, or underrepresented students, and that it's entirely their choice to include.
4. **Open to programs abroad?** Which countries/regions, which languages they could study in,
   whether a passport/visa is an issue, and whether they'd need travel funding.
5. Interests: which subjects/fields excite them, and the story of *how* they got interested.
6. Classes: strongest subjects, advanced courses (AP, IB, A-levels, national curriculum...),
   grades as the school reports them, test scores if any (including English tests if English
   isn't their first language).
7. Activities, clubs, sports, jobs, volunteering - for each: role, years, hours/week, what they did.
8. Projects or research they've done on their own (code, experiments, writing, art, a business).
9. Competitions and awards.
10. Skills: programming languages, lab skills, tools, spoken languages.
11. Logistics: can they live away from home? for how long? hours during the school year?
    driver's license/transit? budget (in their currency)? do they need to earn money?
12. What they want from their next long break; deal-breakers.
13. Teachers or mentors who know them well (name + subject) - for recommendation planning.
14. Ask for a paragraph they've written (any school essay) to capture their writing voice -
    note 3-5 observations in **Writing voice**, don't store the essay in the profile.

## Step 2: Confirm and write

Show a compact summary of the profile and the inferred **target break** (the next long school
break that hasn't started - e.g. "summer 2027" or "Dec 2026-Jan 2027 holidays") and **grade at
application time**. Apply corrections, then write `profile.md` -
replace placeholders with facts, leave unknown fields as `[PLACEHOLDER]`, remove the empty
example bullets for sections that have real entries.

## Step 3: Generate search queries

Rewrite `search-queries.md` from its template:
- profile summary line
- the `opps.py seed` command(s) with the right `--grade`, `--home`, `--cost` and `--field` values
  (plus an `--abroad` line if they're open to going abroad)
- 4-8 queries per category (research, internships, holiday programs, local, and abroad if
  wanted), built from interests × type × region × year. Use the student's **local terms**
  (sixth form, Year 12, secondary school, lycée, JC, "school holidays", "work experience",
  "pre-university") and, where useful, their **local language** - an English-only search
  misses most programs in Germany, Korea, Brazil or Japan. Use `sources.md` for ideas.
  Never include name or school.
  Examples: `"high school summer research program" neuroscience 2027`,
  `"high school internship" Austin TX 2027 paid`, `"Year 12" "work experience" engineering Manchester 2027`,
  `"summer school" "secondary school students" physics Europe 2027`,
  `Schülerakademie Physik 2027`

## Step 4: Next steps

Tell the student:
- `/search` to find opportunities now
- `/deadlines` to see what usually opens soon (many deadlines are 4-8 months before the program -
  e.g. US programs for June often close November-February; Australia's NYSF for January closes
  around July - earlier than most students expect)
- Add `documents/` material any time and re-run `/setup`
