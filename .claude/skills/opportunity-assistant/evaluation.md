# Opportunity Evaluation Framework

Used by `/search` (quick version) and `/apply` (full version). Gates run first; a FAIL stops
the evaluation and is reported with the quoted rule from the official page.

## Gates (run before scoring)

Read each rule **verbatim from the official page for the current cycle**. If the page still shows
last year's cycle, say so and treat the result as provisional.

| Gate | FAIL when | Notes |
|---|---|---|
| **Grade / age** | Student's grade at application time or age at program start is outside the stated range | Watch the wording: "rising senior" = currently a junior. "Must be 16 by June 15" is checked against the profile's age next summer. |
| **Citizenship / residency** | Program requires a status the student does not have (US citizen, PR, state resident, specific metro area) | Federal labs usually require citizenship. Local programs (SIMR, NIH, Fred Hutch, Broad) often require living within commuting distance. |
| **Deadline** | Deadline for this cycle has passed | If passed, record the usual month so `/deadlines` warns next year. If it closes within 14 days, flag **URGENT** and check whether recommendations can still be gathered in time. |
| **Logistics** | Dates clash with the student's stated commitments, or residential when the student can't travel | Partial clashes are a FLAG, not a FAIL. |
| **Budget** | Cost exceeds the budget *after* realistic aid | "Need-based aid available" is not "free" - say what the aid policy actually says. |

When a gate is **unclear** (page silent, ambiguous wording), mark it UNVERIFIED and tell the
student exactly what to check or whom to email. Silence is not permission.

## Legitimacy check

Rate every opportunity **Established / Unclear / Caution**:

- **Established:** run by a university, national lab, government agency, museum, hospital, or a
  long-running nonprofit; clear selection process; published dates and contacts.
- **Caution** - say which signals fired:
  - Invites students by mail/email as "nominated" or "selected" without the student applying
  - High fees with very high acceptance rates, or "pay to get published / pay for a recommendation"
  - Uses a university's name but is run by a third-party company renting the campus (say so -
    it can still be a fine experience, but it is not "a Harvard/Stanford program")
  - Asks for SSN, bank info, or payment before an offer
  - "Internship" that is sales, unpaid work for a for-profit with no learning plan, or
    commission-based
- Paid research-mentorship companies (online programs pairing students with grad-student
  mentors for a fee) are legitimate businesses but not selective honors - describe them
  neutrally and point out free alternatives (cold-emailing labs via `/outreach`, local
  university outreach programs).

## Scoring (0-100 each)

1. **Interest match** - how closely the field/topic matches the profile's interests and goals.
2. **Readiness** - does the student have the coursework, skills, or prior experience the program
   expects? (e.g. RSI expects prior research and top scores; SSP expects calculus/physics
   readiness; a museum teen program expects curiosity.)
3. **Value** - real research, mentorship, or skills vs. a lecture-only camp; credentials; pay;
   peer cohort. Free and paid opportunities score higher for students who flagged "needs income".
4. **Odds** - realistic chance of admission given selectivity and the student's profile.
   Never inflate this to be encouraging.
5. **Logistics fit** - dates, location, commute, cost after aid.

**Overall** = 0.30 interest + 0.20 readiness + 0.20 value + 0.15 odds + 0.15 logistics.

**Bucket** (independent of overall):
- **Reach** - selectivity "very/extremely high", or readiness < 60
- **Target** - competitive but the profile is solid
- **Likely** - open, rolling, local, or the profile clearly exceeds the bar

A healthy list has a mix: roughly 3-5 reaches, 4-6 targets, 2-4 likely - plus at least one
self-made option (cold-emailing labs, an independent project) so the summer never depends on
admissions luck.

## Output format (full evaluation)

```
## [Program] - [Org]
Official page: <url>  (cycle checked: 20XX)
Deadline: YYYY-MM-DD (verified / unverified)   Cost: ...   Dates: ...   Format: ...

Gates: Grade/age PASS · Citizenship PASS · Deadline PASS (in 47 days) · Logistics FLAG (...) · Budget PASS
Legitimacy: Established

| Interest | Readiness | Value | Odds | Logistics | Overall | Bucket |
|---|---|---|---|---|---|---|
| 85 | 70 | 90 | 35 | 80 | 74 | Reach |

Why it fits: ...
Honest gaps: ...
What the application needs: essays (N, word limits), recs (N, from whom), transcript, scores, problem set, fee/waiver
Recommendation: Apply / Apply as a reach / Skip (reason)
```
