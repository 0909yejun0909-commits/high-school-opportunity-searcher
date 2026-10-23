# How to Use High School Opportunity Searcher

A complete guide to every command, with examples, tips, and fixes for common problems.
New here? Install first ([README → Install](../README.md#install-5-minutes)), then read
**[Getting started](#getting-started)** and skim the rest as you need it.

**Contents**
- [Getting started](#getting-started)
- [The basics of talking to it](#the-basics-of-talking-to-it)
- Commands:
  [/opp-setup](#opp-setup-build-your-profile) ·
  [/opp-search](#opp-search-find-opportunities) ·
  [/opp-apply](#opp-apply-evaluate-and-apply) ·
  [/opp-deadlines](#opp-deadlines-never-miss-a-date) ·
  [/opp-outreach](#opp-outreach-email-a-lab-about-research) ·
  [/opp-outcome](#opp-outcome-record-what-happened) ·
  [/opp-interview](#opp-interview-prepare-for-an-interview)
- [Plans for different situations](#plans-for-different-situations)
- [Where your files are](#where-your-files-are)
- [Using the tracker directly](#using-the-tracker-directly-optional)
- [Troubleshooting](#troubleshooting)

---

## Getting started

1. Open a terminal and type `claude` to start Claude Code. Any folder works if you ran `install.py`.
2. Type `/opp-setup` and answer the questions (about 10 minutes).
3. Type `/opp-search` and wait a few minutes while it searches and checks websites.
4. Read the results, pick one, and type `/opp-apply <number>`.
5. Type `/opp-deadlines ics` and import the calendar file it makes.

Come back to it whenever something changes: you join a new activity, get a result, or want to
search again.

> **Command names:** if you ran `install.py`, the commands start with `opp-` (`/opp-search`)
> and work in any folder. If you open Claude Code *inside* the project folder, the short names
> (`/search`) also work. They do exactly the same thing. This guide uses the `opp-` names.

## The basics of talking to it

- **Commands are shortcuts, not the only way in.** You can type normally: *"Find me paid
  biology internships near Chicago,"* *"Am I eligible for SSP?,"* *"Help me answer this essay
  prompt."* It understands.
- **Correct it.** If it gets something wrong about you ("I'm actually a junior"), just say so.
  To make the change permanent, run `/opp-setup` again.
- **Ask why.** "Why is this a reach?" or "Why did you mark me not eligible?" It will quote the
  rule from the program's website.
- **No permission pop-ups.** If you installed with `install.py`, everything the commands need is
  pre-approved: the project's scripts, files inside the project folder, web search, and checking
  program websites. You won't be interrupted. (Used `--no-permissions`, or running inside the
  folder without installing? Then choose **"Yes, and don't ask again"** when asked.)
- **It will never** submit an application, send an email, or fill in a website form. When
  something is ready, it tells you what to do next.

---

## /opp-setup: build your profile

**When:** first thing, and again whenever something important changes (new activity, new
award, new grade, new interests).

**What to type:** `/opp-setup`

**What happens:** it offers three ways in:

| Option | Best if... |
|---|---|
| **Interview me** | You're starting from scratch. It asks 2-4 questions at a time. |
| **Paste a resume / activities list** | You already have one somewhere |
| **Read my documents** | You put files in the `documents/` folder first: transcript (an unofficial one is fine), activities list, awards, an essay you wrote |

It asks about:
- **Basics:** your country and city, your school year *as your school calls it* (Grade 10, Year 12, S5, JC1...), graduation year, age, citizenship(s) or residency
- **Your long break:** when it is. Not everyone's is June-August: in Australia, New Zealand, southern Africa and much of South America it's around December-February
- **Going abroad:** whether you'd consider programs in other countries, which ones, and which languages you could study in
- **Interests:** what you're curious about *and how you got into it*. Real stories here become essay material later.
- **School:** strongest subjects, advanced classes, GPA, test scores (optional), competitions
- **Activities, projects, jobs, volunteering:** with hours per week and what you actually did
- **Logistics:** can you stay away from home? for how long? budget (in your currency), do you need to earn money?
- **Recommenders:** teachers or mentors who know you well (it never contacts them)
- **Writing voice:** it asks for a paragraph you wrote, so its feedback keeps your essays sounding like you

**Why it asks about citizenship and background:** many programs have hard rules (US federal labs
usually require US citizenship; UK programs like UNIQ are for UK state-school students; some
programs only take local students; programs abroad may need a visa). Several free programs
also give priority to first-generation, low-income, or underrepresented students. Sharing
background details is **completely optional**. Skip any question you want.

**What you get:** your profile saved privately in
`.claude/skills/opportunity-assistant/profile.md` and search queries tailored to you.

**Tip:** be specific. *"Science Olympiad, anatomy event, 5 hrs/week, 2nd at regionals"* is
much more useful than *"Science Olympiad member."*

---

## /opp-search: find opportunities

**When:** after setup, then every few weeks (new programs appear all year), and whenever you
want to explore something new.

**What to type:**

| Type | To get |
|---|---|
| `/opp-search` | A general search based on your profile |
| `/opp-search biology` | Focus on one field |
| `/opp-search paid internships` | Only things that pay |
| `/opp-search local` | Things you can commute to: labs, hospitals, museums, city programs |
| `/opp-search math` | Math camps and research (these have problem-set applications) |
| `/opp-search broad` | A wider net, including ones it showed you before |
| `/opp-search next-year` | Plan ahead for the break after next (great for 9th/10th graders) |
| `/opp-search abroad` | Only opportunities outside your country: summer schools, research institutes, exchanges |
| `/opp-search international` | Programs anywhere that accept students from any country |
| `/opp-search Germany` (any country or region) | Opportunities held there that you're allowed to apply to |

**What happens (it takes a few minutes):**
1. It tells you how it's searching ("10th grader now, age 16 next June, Austin TX, free/aid only")
   so you can correct it.
2. It gathers 25-50 candidates from the curated list plus web searches.
3. Helper agents open each program's **official** site and read this year's deadline, cost, dates,
   and eligibility rules.
4. It checks each one against your profile and scores the fit.
5. It saves what it found, so the next search only shows new things.

**What you get:**
- **Apply soon:** deadlines in the next 30 days
- **Top matches:** ranked, with fit score, Reach/Target/Likely, and a one-line honest reason
- **Local / likely options:** your safety net
- **Not eligible (and why):** with the exact rule quoted and when you *can* apply
- **Abroad** (if you're open to it): country, total cost *including travel*, whether financial aid
  covers international students, and visa notes
- **Opens later:** programs whose applications aren't posted yet, with the usual month

**Applying from outside the program's country?** It also checks the program's international
page. That page often has a different (earlier) deadline, an English test requirement, separate
aid rules ("international students welcome" doesn't always mean "aid for international students"),
and visa guidance. Many US summer programs that aren't for college credit use a visitor visa or
ESTA rather than a student visa, but follow each program's own instructions.

**How to read a deadline:**
- **verified**: it read this date on the official site during this search
- **usual month / not posted yet**: based on past years. Check back later, and don't plan around an exact day yet.

**How to read the buckets:**
- **Reach:** very selective (often under 10% get in), or you're missing something they expect.
  Worth applying to a few, but never count on them.
- **Target:** competitive, but your profile is solid.
- **Likely:** open, local, rolling, or you clearly meet the bar.

A good list has a few reaches, several targets, and some likely options, plus something you
control, like emailing labs.

**After a search, say things like:** *"Add 2, 4 and 6 to my tracker,"* *"Tell me more about
#3,"* *"Why am I not eligible for Clark?,"* or `/opp-apply 2`.

---

## /opp-apply: evaluate and apply

**When:** you've found something you're interested in.

**What to type:** any of these:
```
/opp-apply 2                                       # a number from your last search
/opp-apply Summer Science Program                  # a name
/opp-apply https://www.example.edu/summer-research # the program's link
```

**Step 1: the honest evaluation.** It reads the program's website and shows:
- **Eligibility checks:** grade/age, citizenship, deadline, logistics, budget. Each is PASS, FAIL,
  FLAG, or UNVERIFIED, quoted from the official site.
- **Legitimacy:** Established / Unclear / Caution, with the reasons.
- **Fit scores:** interest, readiness, value, odds, logistics, plus an overall score and a bucket.
- **What the application needs:** essays (number and word limits), recommendations, transcript,
  test scores, problem sets, fee and fee waiver.
- **Recommendation:** Apply / Apply as a reach / Skip.

If you're not eligible, it stops and suggests similar programs you *can* apply to.

**Step 2: the plan.** If you say yes, it creates `applications/<program>/plan.md` with a
checklist that counts back from the deadline:
- ask for recommendations **4+ weeks before**
- first essay draft **3 weeks before**
- final review **3 days before**
- submit **at least 1 day early** (application websites often crash on deadline day)

It also adds the program to your tracker.

**Step 3: the materials.**

| Material | How it helps |
|---|---|
| **Activities resume** | Drafts a one-page resume tailored to this program, using only facts from your profile. You get `resume.md` and `resume.html`. Open the HTML in a browser and use **Print → Save as PDF**. |
| **Activities list** | Formats your activities to fit the application form's character limits |
| **Essays** | **Coaches you** (see below) |
| **Recommendation emails** | Drafts a short email for each teacher you pick, with the program, deadline, how to submit, and what you hope they'll mention |
| **Math problem sets** | Gives hints and questions only, never solutions. Programs check for this, and getting caught means rejection. |

**How essay coaching works:**
1. It looks up the program's **AI policy** and tells you what it says.
2. It explains what the prompt is *really* asking.
3. It suggests 3-4 angles based on real things in your profile.
4. It asks follow-up questions to bring out details. This is where the good material comes from.
5. You agree on an outline together.
6. **You write the draft** and paste it in.
7. It gives feedback: the 2-3 biggest improvements first, then where to add concrete examples,
   generic phrases to cut, word count, and grammar suggestions. It keeps your voice.
8. Repeat until you're happy.

If you explicitly ask for a sample paragraph *and* the program allows AI help, it can write one,
labeled as an example to rewrite in your own words. By default it doesn't, because
your essay is supposed to show who *you* are.

**Step 4: the review.** When your drafts are ready, a second agent reads everything as an
admissions reader would. It checks that every claim matches your profile, that each essay answers
the prompt, that the writing is specific, that it explains why *this* program, and that it still
sounds like you. You get the top 3 changes to make.

**Step 5: wrap-up.** You get a list of files, your checklist with dates, and the next concrete action.

---

## /opp-deadlines: never miss a date

**When:** once a week during application season (Nov-Mar).

**What to type:**
```
/opp-deadlines          # next 60 days
/opp-deadlines 30       # next 30 days
/opp-deadlines ics      # also make a calendar file
/opp-deadlines 90 ics
```

**What you get:**
- **Tracked deadlines:** overdue items first, then this week, then the rest, with your next step for each
- **Usually due soon, not tracked:** well-known programs that usually close in this window,
  filtered to ones you're eligible for. Say *"check the real dates for these"* and it will verify them.
- **Rec letter warnings:** any deadline within 4 weeks where you haven't asked for recommendations yet

**Adding to your calendar:** `ics` creates `deadlines.ics` in the project folder. Double-click
it (Apple Calendar or Outlook) or, in Google Calendar, go to **Settings → Import & export → Import**.
Each deadline gets a reminder one week before. Re-import after adding new programs.

---

## /opp-outreach: email a lab about research

Many high school research positions are **never posted**. Students get them by emailing
professors. It's normal to email 10-20 labs and hear back from a few.

**What to type:**
```
/opp-outreach computational neuroscience near Houston   # find labs
/opp-outreach Dr. Jane Smith, University of Michigan    # a specific professor
/opp-outreach https://smithlab.example.edu              # a lab's website
```

**What happens:**
1. **Finding labs** (topic search): 5-10 labs near you (or remote-friendly computational labs)
   with what they study and whether they mention taking high school students. You pick.
2. **Understanding the lab:** it reads the lab's site and recent papers and explains one in plain
   language. It asks what *genuinely* interests you about it. That becomes the heart of your email.
3. **The email** (under 150 words): who you are, the specific thing that interests you, 1-2
   relevant skills, and a small, clear request, such as a short conversation about whether you could help this summer.
4. **A follow-up email** for 7-10 days later if you don't hear back.

Saved in `applications/outreach/<professor>/`.

**Safety:** you send the emails yourself. Meetings should happen at the university or on video,
and a parent or guardian should know about any in-person arrangement. Real labs will send you
through their university's process for minors in labs, so expect some paperwork.

---

## /opp-outcome: record what happened

**What to type:**
```
/opp-outcome Navy SEAP submitted
/opp-outcome BWSI interview next Tuesday
/opp-outcome SSP accepted
/opp-outcome RSI rejected
/opp-outcome status            # see everything that's still open
```

**What it does after each result:**

| Result | Follow-up |
|---|---|
| submitted | Updates the tracker and notes the date |
| interview | Offers `/opp-interview` |
| accepted | Lists what to do and by when (reply date, forms, deposit); helps compare offers; drafts thank-you notes to your recommenders |
| waitlisted | Drafts a short letter of continued interest, if the program accepts them |
| rejected | A bit of perspective (these programs often take a few percent), then your next-best open option |
| declined | Drafts a polite note so your spot goes to someone else quickly |

---

## /opp-interview: prepare for an interview

**What to type:** `/opp-interview Summer Science Program` (add the date and format if you know them)

**What you get** (saved as `applications/<program>/interview.md`):
- What the program values and the interview format, if they publish it
- Likely questions (*"Tell me about a project you're proud of," "What would you research?,"
  "Why this program?"*), each with talking points from **your** real experiences.
  These are bullet points, not a script to memorize.
- 2-3 good questions for you to ask the interviewer
- A logistics checklist

Then say **"let's do a mock interview."** It asks one question at a time, waits for your
answer, and gives quick feedback before the next one.

---

## Plans for different situations

**"I'm in 9th or 10th grade and just exploring."**
`/opp-setup` → `/opp-search next-year` to see what you'll be eligible for → `/opp-search local`
for things you can do *this* year → pick one project or activity that moves you toward the
programs you liked.

**"I'm a junior aiming for top research programs (RSI, Simons, SSP...)."**
Start in **September-October**. `/opp-search` → `/opp-deadlines ics` (RSI closes in December)
→ ask teachers for recommendations early → `/opp-apply` each one → add 4-6 targets and likely
options, plus `/opp-outreach` as a backup.

**"I need to earn money this summer."**
Say *"needs income: yes"* in `/opp-setup`, then `/opp-search paid internships`. Look at
stipend programs (federal labs, Bank of America Student Leaders, Hutton) and your city's
summer youth employment program, which often opens in January-February.

**"Nothing fits, or I got rejected everywhere."**
`/opp-outreach` for labs near you, `/opp-search local` for museums, hospitals and community
colleges, and consider an independent project (science fair, open-source code, a research
question you investigate yourself). Many strong applicants built their own summer this way.

**"I can't travel."**
Say so in `/opp-setup`. Search results will favor local and online options: commutable labs,
online programs (PRIMES-USA, online writing workshops), and remote computational research
through `/opp-outreach`.

**"I'm not in the US."**
Tell `/opp-setup` your country, your school year as your school names it, and when your long
break is. Searches use your local terms (Year 12, sixth form, JC, lycée, work experience) and
your local language, and only show programs you're allowed to apply to. The curated list includes
the UK (UNIQ, Sutton Trust, In2scienceUK, PROMYS Europe), Canada (Shad), Australia (NYSF),
Singapore (A*STAR awards), Europe-wide and worldwide programs (PROMYS Europe, CERN Beamline for
Schools, Weizmann ISSI), and the US programs that accept international students (RSI, SSP, Ross,
PROMYS, Mathcamp, SUMaC, YYGS, TASS). For other countries the live search does most of the work.

**"I want to go abroad."**
Say so in `/opp-setup` (which countries, which languages), then `/opp-search abroad` or
`/opp-search <country>`. For US students, fully funded options include NSLI-Y (languages),
CBYX (a year in Germany) and YES Abroad. These close around November-December for the
following year, so start early. For anyone, give yourself extra time for passports and visas
(2-4 months), budget for flights and insurance, and involve a parent or guardian from the
start.

---

## Where your files are

Everything lives in the project folder (`~/high-school-opportunity-searcher` if you followed the README):

| File / folder | What's in it |
|---|---|
| `.claude/skills/opportunity-assistant/profile.md` | Your profile. You can edit it by hand. (The `.claude` folder is hidden; press ⌘⇧. in Finder to see it.) |
| `data/tracker.csv` | Your application tracker. Opens in Excel, Numbers, or Google Sheets. |
| `applications/<program>/` | `plan.md`, `resume.md` / `resume.html`, `essays/`, `rec-requests.md`, `interview.md` |
| `applications/outreach/<professor>/` | Lab notes and email drafts |
| `documents/` | Files you gave `/opp-setup` |
| `deadlines.ics` | Your calendar export |

All of these are **private**: git ignores them, so they never get uploaded.

## Using the tracker directly (optional)

The commands manage the tracker for you, but you can also use it from the terminal (run these
from the project folder):

```bash
python3 tools/opps.py track list                       # open applications, by deadline
python3 tools/opps.py track list --all                 # including finished ones
python3 tools/opps.py track add --program "SSP" --url https://summerscience.org --deadline 2027-02-15
python3 tools/opps.py track update --program "SSP" --status submitted --notes "sent Feb 10"
python3 tools/opps.py deadlines --days 45 --ics deadlines.ics
python3 tools/opps.py seed --grade 10 --field biology --cost no-paid   # browse the curated list
python3 tools/opps.py seed --grade 11 --home UK                        # what a UK student can apply to
python3 tools/opps.py seed --home US --abroad                          # programs abroad for US students
python3 tools/opps.py seed --international --field math                # open to any country
```

Statuses: `interested, preparing, submitted, interview, accepted, waitlisted, rejected,
declined, withdrawn, missed`.

---

## Troubleshooting

**"Unknown command /opp-search."**
The installer hasn't run, or Claude Code was already open when you ran it. Run
`python3 ~/high-school-opportunity-searcher/install.py`, then restart Claude Code. Or open Claude
Code inside the project folder and use `/search`.

**"It says to run /setup first."**
Your profile is missing or still has blanks in the Basics section (grade, age, location,
citizenship). Eligibility can't be checked without them. Run `/opp-setup`.

**It keeps asking for permission.**
Run `python3 ~/high-school-opportunity-searcher/install.py` again (without `--no-permissions`).
It pre-approves the project's own scripts, files inside the project folder, and web search/fetch,
and nothing else. Anything outside that, such as a file in another folder, will still ask,
on purpose. If you moved the project folder, re-run the installer so the approvals point to the
new location.

**"Couldn't verify" or "blocked" on a program.**
Some sites block automated reading. Open the official link yourself and check the deadline and
eligibility. Never rely on an unverified date.

**The search seems wrong about me (grade, age...).**
Check the "Searched as" line at the top of the results. Correct it in chat, and run
`/opp-setup` to fix it permanently.

**I moved the project folder.**
Run `python3 <new location>/install.py` again so the global commands point to the new place.

**Getting updates.**
`git -C ~/high-school-opportunity-searcher pull`. Your profile and applications aren't
touched.

**Uninstall.**
`python3 ~/high-school-opportunity-searcher/install.py --uninstall` removes the global
commands. Then delete the folder (after saving anything you want to keep from `applications/`).

**Something else?**
[Open an issue](https://github.com/0909yejun0909-commits/high-school-opportunity-searcher/issues).
Please don't include personal details.
