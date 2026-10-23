# /outcome - Record a Result

Input (`$ARGUMENTS`): a program and what happened, e.g. `SSP accepted`, `RSI rejected`,
`Navy SEAP submitted`, `BWSI interview next Tuesday`, or `status` to list everything open.

1. `status` → run `python3 tools/opps.py track list` and show it, with days since submission for
   `submitted` rows. Suggest a polite status-check email only if the program's stated decision
   date has passed.
2. Otherwise map the result to a tracker status (`interested, preparing, submitted, interview,
   accepted, waitlisted, rejected, declined, withdrawn, missed`) and run
   `python3 tools/opps.py track update --program "<name>" --status <status> --notes "<short note, date>"`.
   If the program isn't tracked, ask, then `track add`.
3. Follow-ups by status:
   - **interview** → offer `/interview <program>`.
   - **accepted** → list the acceptance to-dos from the official page (reply-by date, deposit,
     forms, medical/parent forms); if there are other pending applications, help compare offers;
     draft thank-you notes to recommenders.
   - **waitlisted** → draft a short, sincere letter of continued interest if the program accepts them.
   - **rejected** → one line of perspective (these programs admit a few percent; it's not a
     verdict on the student), then point to the next-best open option or `/outreach`.
   - **declined** → draft a gracious decline so the spot goes to someone else promptly.
4. Append a dated line to `applications/<slug>/plan.md` if it exists.
