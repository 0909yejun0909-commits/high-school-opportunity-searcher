"""install.py and the template/.gitignore split are what make this safe to share.

install.py writes into the user's global ~/.claude, so it must only ever touch
files it created. The templates are committed and public, so they must stay
blank, and the filled-in copies must be git-ignored.
"""
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
import install  # noqa: E402

PERSONAL = [
    ".claude/skills/opportunity-assistant/profile.md",
    ".claude/skills/opportunity-search/search-queries.md",
    "data/tracker.csv",
    "data/seen.json",
    "documents/transcript.pdf",
    "applications/ssp/resume.md",
    "deadlines.ics",
]


class Install(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self._saved = install.CLAUDE
        install.CLAUDE = Path(self.tmp.name) / ".claude"

    def tearDown(self):
        install.CLAUDE = self._saved
        self.tmp.cleanup()

    def run_install(self, *argv):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = install.main(list(argv))
        return code, out.getvalue()

    def test_install_writes_wrappers_and_agents(self):
        self.assertEqual(self.run_install()[0], 0)
        for cmd in install.COMMANDS:
            skill = install.CLAUDE / "skills" / f"opp-{cmd}" / "SKILL.md"
            text = skill.read_text()
            self.assertIn(f"name: opp-{cmd}", text)
            self.assertIn(f"{install.HOME}/.claude/commands/{cmd}.md", text)
            self.assertTrue((install.HOME / ".claude" / "commands" / f"{cmd}.md").exists(), cmd)
        for agent in install.AGENTS:
            text = (install.CLAUDE / "agents" / f"{agent}.md").read_text()
            self.assertTrue(text.startswith("---\nname: "), agent)  # frontmatter intact
            self.assertIn(install.MARKER, text)

    def test_agent_tool_paths_are_absolute(self):
        self.run_install()
        text = (install.CLAUDE / "agents" / "opportunity-fetcher.md").read_text()
        self.assertIn(f"python3 {install.HOME}/tools/fetch_page.py", text)
        self.assertNotIn("python3 tools/", text)

    def test_foreign_files_left_alone(self):
        theirs = install.CLAUDE / "skills" / "opp-search" / "SKILL.md"
        theirs.parent.mkdir(parents=True)
        theirs.write_text("someone else's skill")
        _, out = self.run_install()
        self.assertIn("skip (not ours", out)
        self.assertEqual(theirs.read_text(), "someone else's skill")
        self.run_install("--uninstall")
        self.assertEqual(theirs.read_text(), "someone else's skill")

    def test_uninstall_removes_only_ours(self):
        self.run_install()
        self.run_install("--uninstall")
        self.assertFalse(list((install.CLAUDE / "skills").glob("opp-*")))
        for agent in install.AGENTS:
            self.assertFalse((install.CLAUDE / "agents" / f"{agent}.md").exists())

    def test_dry_run_writes_nothing(self):
        self.run_install("--dry-run")
        self.assertFalse(install.CLAUDE.exists())


class Privacy(unittest.TestCase):
    def test_templates_are_blank(self):
        profile = (REPO_ROOT / ".claude/skills/opportunity-assistant/profile.template.md").read_text()
        for token in ("[STUDENT_NAME]", "[GRADE]", "[CITIZENSHIP]", "[CITY]"):
            self.assertIn(token, profile)
        queries = (REPO_ROOT / ".claude/skills/opportunity-search/search-queries.template.md").read_text()
        self.assertIn("[GRADE]", queries)

    def test_personal_files_are_gitignored(self):
        try:
            res = subprocess.run(
                ["git", "-C", str(REPO_ROOT), "check-ignore", "--no-index", *PERSONAL],
                capture_output=True, text=True,
            )
        except FileNotFoundError:
            self.skipTest("git not installed")
        if res.returncode == 128:
            self.skipTest("not a git checkout")
        ignored = set(res.stdout.split())
        self.assertEqual(sorted(set(PERSONAL) - ignored), [], "personal files not ignored")

    def test_kept_placeholders_are_not_ignored(self):
        for path in ("documents/README.md", "applications/.gitkeep",
                     ".claude/skills/opportunity-assistant/profile.template.md"):
            res = subprocess.run(["git", "-C", str(REPO_ROOT), "check-ignore", "--no-index", "-q", path])
            if res.returncode == 128:
                self.skipTest("not a git checkout")
            self.assertEqual(res.returncode, 1, f"{path} should be committed")


if __name__ == "__main__":
    unittest.main()
