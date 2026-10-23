# /outreach - Cold-Email a Lab About Research

Many high school research positions are never posted - students get them by emailing professors.
Input (`$ARGUMENTS`): a professor's name + university, a lab URL, or a topic + region
("computational neuroscience labs near Houston").

## Step 1: Find labs (topic input)
WebSearch university department pages near the student (commute radius from the profile) or
remote-friendly computational labs. Return 5-10 labs: PI, university, one-line research focus,
lab page, whether the lab mentions taking high school students. Let the student pick.

## Step 2: Research the lab
From the lab's own page and the PI's recent papers (titles + abstracts via WebSearch / Google
Scholar / PubMed): what they study, 1-2 recent papers in plain language, whether they list
undergrad/high school members, any posted policy on volunteers. Save to
`applications/outreach/<pi-lastname>/notes.md`.

Explain the student-relevant parts of one paper simply, and ask the student what genuinely
interests them about it - that becomes the email's core.

## Step 3: Draft the email
Under 150 words, subject like "High school student interested in [specific topic] research":
1. Who they are (grade, school *only if the student wants to include it*), one line.
2. The specific thing in the lab's work that interests them, in their words from Step 2.
3. Relevant skills/experience - 1-2 concrete items from the profile.
4. A small, clear ask: "Would you or someone in your lab have time for a short conversation about
   whether a high school student could help with [X] this summer?"
5. Resume attached; thanks.

Save to `applications/outreach/<pi-lastname>/email.md`. Note: send from a school or personal
email the student checks; it's normal to email 10-20 labs and hear back from a few. Suggest one
polite follow-up after 7-10 days, and draft it.

## Safety
The student sends emails themselves. Meetings should be at the university/lab or on video, and a
parent/guardian should know about any in-person arrangement. A legitimate lab will route a minor
through the university's minors-in-labs/safety process - mention this so the student isn't
surprised by paperwork.

Optionally track it: `python3 tools/opps.py track add --program "Outreach: <PI> lab" --org "<univ>"
--category research --url <lab url> --status submitted --notes "emailed <date>"`.
