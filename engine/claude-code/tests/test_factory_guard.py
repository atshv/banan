"""Tests für die Schalter. Aufruf im Factory-Ordner: python3 -m unittest discover engine/claude-code/tests"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

GUARD = os.path.join(os.path.dirname(__file__), "..", ".claude", "hooks", "factory_guard.py")

TASKS = """# Tasks
## T-001: Login
- Modul: auth
- Bereich: src/login/, tests/login/, app/page.tsx, `src/lib/*.ts`
- Fertig wenn: Login geht

## T-002: Ohne Bereich
- Modul: x
"""


def sh(root, *args):
    subprocess.run(["git", "-C", root, *args], check=True, capture_output=True)


class GuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = os.path.realpath(self.tmp.name)
        sh(self.root, "init", "-q", "-b", "main")
        sh(self.root, "config", "user.email", "t@t")
        sh(self.root, "config", "user.name", "t")
        self.write("memory/handoffs/05-tasks.md", TASKS)
        self.write("memory/status.md", "| Task | Titel | Status |\n|---|---|---|\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, text):
        full = os.path.join(self.root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(text)

    def commit(self):
        sh(self.root, "add", "-A")
        sh(self.root, "commit", "-q", "-m", "x")

    def run_guard(self, mode, **data):
        data.setdefault("cwd", self.root)
        env = dict(os.environ, CLAUDE_PROJECT_DIR=self.root)
        r = subprocess.run([sys.executable, GUARD, mode], input=json.dumps(data),
                           capture_output=True, text=True, env=env)
        return r.returncode, r.stderr

    def can_write(self, path):
        return self.run_guard("write", tool_input={"file_path": path})[0] == 0

    def status(self, rows):
        self.write("memory/status.md", "| Task | Titel | Status |\n|---|---|---|\n" + rows)

    # Schreibsperre main
    def test_before_first_commit_everything_is_allowed(self):
        self.assertTrue(self.can_write("src/app.ts"))

    def test_main_blocks_product_code(self):
        self.commit()
        self.assertFalse(self.can_write("src/app.ts"))
        self.assertFalse(self.can_write(os.path.join(self.root, "package.json")))

    def test_main_allows_admin_files(self):
        self.commit()
        for p in ("memory/status.md", "CHANGELOG.md", "VERSION", ".claude/skills/x/SKILL.md", "factory/shared/a.md"):
            self.assertTrue(self.can_write(p), p)

    def test_outside_project_is_allowed(self):
        self.commit()
        self.assertTrue(self.can_write("/tmp/irgendwas.txt"))

    def test_switches_are_protected_everywhere(self):
        self.assertFalse(self.can_write(".claude/settings.json"))
        self.assertFalse(self.can_write(".claude/hooks/factory_guard.py"))

    def test_other_branches_are_free(self):
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "setup/grundgeruest")
        self.assertTrue(self.can_write("src/app.ts"))

    # Task-Bereich
    def test_task_branch_scope(self):
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "task/T-001-login")
        for p in ("src/login/form.tsx", "tests/login/a.test.ts", "app/page.tsx", "src/lib/auth.ts",
                  "memory/handoffs/tasks/T-001-build.md", "package-lock.json"):
            self.assertTrue(self.can_write(p), p)
        for p in ("src/profile/x.tsx", "app/layout.tsx", "memory/handoffs/05-tasks.md", ".claude/agents/x.md"):
            self.assertFalse(self.can_write(p), p)

    def test_task_number_matches_without_leading_zeros(self):
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "task/T-1-login")
        self.assertTrue(self.can_write("src/login/form.tsx"))

    def test_task_without_scope_is_blocked(self):
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "task/T-002-x")
        code, err = self.run_guard("write", tool_input={"file_path": "src/a.ts"})
        self.assertEqual(code, 2)
        self.assertIn("Bereich", err)

    # Commit auf main
    def test_commit_on_main(self):
        self.commit()
        cmd = {"tool_input": {"command": "git add -A && git commit -m x"}}
        self.write("memory/status.md", "neu")
        self.assertEqual(self.run_guard("bash", **cmd)[0], 0)
        self.write("src/app.ts", "x")
        self.assertEqual(self.run_guard("bash", **cmd)[0], 2)
        self.assertEqual(self.run_guard("bash", tool_input={"command": "npm test"})[0], 0)
        sh(self.root, "checkout", "-q", "-b", "task/T-001-login")
        self.assertEqual(self.run_guard("bash", **cmd)[0], 0)

    # Stop-Check
    def test_stop_passes_when_nothing_is_open(self):
        self.status("| T-001 | Login | offen |\n| T-002 | X | blockiert |\n")
        self.assertEqual(self.run_guard("stop")[0], 0)

    def test_stop_blocks_active_task_once(self):
        self.status("| T-001 | Login | in Arbeit |\n")
        self.assertEqual(self.run_guard("stop")[0], 2)
        self.assertEqual(self.run_guard("stop", stop_hook_active=True)[0], 0)

    def test_stop_needs_evidence_for_done(self):
        self.status("| T-001 | Login | fertig |\n")
        self.assertEqual(self.run_guard("stop")[0], 2)
        self.write("memory/handoffs/tasks/T-001-build.md", "Task T-001")
        self.write("memory/handoffs/tasks/T-001-test.md", "Ergebnis: grün · Tests 4")
        self.write("memory/handoffs/tasks/T-001-review.md", "---\nergebnis: ok\n---")
        self.write("memory/handoffs/tasks/T-001-security.md", "**Ergebnis:** abgelehnt")
        code, err = self.run_guard("stop")
        self.assertEqual(code, 2)
        self.assertIn("Security", err)
        self.write("memory/handoffs/tasks/T-001-security.md", "**Ergebnis:** OK")
        self.assertEqual(self.run_guard("stop")[0], 0)

    def test_broken_input_never_blocks(self):
        r = subprocess.run([sys.executable, GUARD, "write"], input="kein json", capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
