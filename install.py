#!/usr/bin/env python3
"""Make the opportunity-search commands available in every folder.

Writes thin user-level skills to ~/.claude/skills/opp-*/ that point back at THIS
folder, which stays the one home for your profile, tracker and applications.
Edits to the workspace take effect immediately; re-run this only if you move
the folder.

  python3 install.py              install / refresh
  python3 install.py --uninstall  remove the global skills and agents
  python3 install.py --dry-run    show what would be written
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HOME = Path(__file__).resolve().parent
CLAUDE = Path.home() / ".claude"
MARKER = "<!-- installed by hs-opportunity-search/install.py -->"

COMMANDS = {
    "setup": ("Build or update the high school student's profile for the opportunity search "
              "(interview, pasted resume, or documents folder).", ""),
    "search": ("Find internships, research opportunities, summer programs and exchanges for a high "
               "school student in any country, at home or abroad; verify official pages, check "
               "eligibility, rank by fit. Use when the user asks to find summer programs, research, "
               "internships or programs abroad for high schoolers.", "[focus | abroad | international | country]"),
    "apply": ("Evaluate a high school program/internship and prepare the application: checklist, "
              "activities resume, essay coaching, recommendation requests, review.", "<url, name, or # from search>"),
    "deadlines": ("Show upcoming high school program deadlines and programs that usually open soon; "
                  "optional .ics calendar export.", "[days] [ics]"),
    "outreach": ("Find research labs and help a high school student write a cold email to a professor "
                 "asking about research.", "<topic, professor, or lab>"),
    "outcome": ("Record a result (submitted, accepted, rejected...) for a high school program "
                "application and update the tracker.", "<program> <result> | status"),
    "interview": ("Prepare a high school student for a program or internship interview, with a mock "
                  "interview.", "<program>"),
}
AGENTS = ["opportunity-fetcher", "opportunity-reviewer"]


def wrapper(cmd: str, description: str, hint: str) -> str:
    others = ", ".join(f"/{c} = /opp-{c}" for c in COMMANDS)
    hint_line = f"argument-hint: \"{hint}\"\n" if hint else ""
    return f"""---
name: opp-{cmd}
description: {description}
{hint_line}---
{MARKER}

This is the global entry point to the High School Opportunity Searcher workspace at
`{HOME}`. The current working directory is unrelated to it.

1. Read `{HOME}/CLAUDE.md` (ground rules - always apply them), then read
   `{HOME}/.claude/commands/{cmd}.md` and follow it with these arguments: $ARGUMENTS
2. **Paths:** every relative path in the workspace files (`tools/`, `data/`, `applications/`,
   `documents/`, `.claude/...`, `CLAUDE.md`) means `{HOME}/<path>`. Run tools as
   `python3 {HOME}/tools/<tool>.py ...`. Write every file under `{HOME}`, never in the
   current working directory.
3. **Names:** the workspace files refer to commands by their short names: {others}.
   Agents `opportunity-fetcher` and `opportunity-reviewer` are installed globally.
"""


def rewrite_agent(text: str) -> str:
    """Agents run in whatever folder the user is in, so pin their paths to HOME."""
    text = re.sub(r"(?<![\w/])(tools/|\.claude/skills/)", lambda m: f"{HOME}/{m.group(1)}", text)
    head, sep, body = text.partition("\n---\n")
    return head + sep + MARKER + "\n" + body


def targets():
    out = {CLAUDE / "skills" / f"opp-{c}" / "SKILL.md": wrapper(c, d, h) for c, (d, h) in COMMANDS.items()}
    for a in AGENTS:
        src = HOME / ".claude" / "agents" / f"{a}.md"
        out[CLAUDE / "agents" / f"{a}.md"] = rewrite_agent(src.read_text(encoding="utf-8"))
    return out


def owned(path: Path) -> bool:
    return path.exists() and MARKER in path.read_text(encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--uninstall", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    for path, content in targets().items():
        if path.exists() and not owned(path):
            print(f"skip (not ours, left alone): {path}")
            continue
        if args.uninstall:
            if path.exists():
                print(f"remove {path}")
                if not args.dry_run:
                    path.unlink()
                    if path.name == "SKILL.md" and not any(path.parent.iterdir()):
                        path.parent.rmdir()
            continue
        print(f"{'would write' if args.dry_run else 'write'} {path}")
        if not args.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    if not args.uninstall and not args.dry_run:
        print(f"\nInstalled. From any folder, start `claude` and run /opp-setup.\nWorkspace: {HOME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
