# /deadlines - What's Due and What's Coming

1. Run `python3 tools/opps.py deadlines --days <N>`, where N is a number in `$ARGUMENTS` or 60 by
   default. If `$ARGUMENTS` contains `ics`, add `--ics deadlines.ics`.
2. Present two sections:
   - **Tracked deadlines** - overdue first, then this week, then the rest. For each one that's
     `interested` or `preparing`, read `applications/<slug>/plan.md` if it exists and name the
     next unchecked step.
   - **Usually due soon, not tracked** - from the seed list. Filter out ones the profile makes
     ineligible (grade, citizenship, location). Offer to verify the current-cycle dates for the
     ones the student cares about (dispatch `opportunity-fetcher`) and add them to the tracker.
3. If an `.ics` file was written, tell the student to double-click it (or import it into Google
   Calendar) - each deadline has a 1-week-before reminder.
4. Flag rec-letter timing: any deadline within 4 weeks whose recs haven't been requested.
