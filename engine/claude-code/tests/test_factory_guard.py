"""Tests für die Schalter. Aufruf im Factory-Ordner: python3 -m unittest discover engine/claude-code/tests"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HOOKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "hooks")
GUARD = os.path.join(HOOKS, "factory_guard.py")
RUNNER = os.path.join(HOOKS, "factory_run.py")

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
        self.write("memory/handoffs/tasks/T-001-security.md", "**Ergebnis:** OK")
        code, err = self.run_guard("stop")
        self.assertEqual(code, 2, "ein Bericht 'grün' ohne aufgezeichneten Lauf reicht nicht")
        self.assertIn("nicht aufgezeichnet: test", err)
        self.write("memory/gates.json", json.dumps({"test": "exit 1"}))
        self.assertEqual(self.run_runner("test", "T-001").returncode, 1)
        self.assertIn("rot: test", self.run_guard("stop")[1])
        self.write("memory/gates.json", json.dumps({"test": "echo alles gut"}))
        self.assertEqual(self.run_runner("test", "T-001").returncode, 0)
        self.assertEqual(self.run_guard("stop")[0], 0)
        self.write("memory/handoffs/tasks/T-001-security.md", "**Ergebnis:** abgelehnt")
        self.assertIn("Security", self.run_guard("stop")[1])

    # Aufgezeichnete Läufe
    def run_runner(self, *args):
        env = dict(os.environ, CLAUDE_PROJECT_DIR=self.root)
        return subprocess.run([sys.executable, RUNNER, *args], capture_output=True, text=True, env=env, cwd=self.root)

    def test_runner_records_result(self):
        self.write("memory/gates.json", json.dumps({"test": "echo hallo && exit 3"}))
        r = self.run_runner("test", "T-007")
        self.assertEqual(r.returncode, 3)
        with open(os.path.join(self.root, "memory/runs/T-007-test.json"), encoding="utf-8") as f:
            record = json.load(f)
        self.assertEqual((record["exit"], record["bestanden"], record["befehl"]), (3, False, "echo hallo && exit 3"))
        self.assertIn("hallo", record["ausgabe_ende"])

    def test_done_needs_every_required_gate(self):
        self.status("| T-001 | Login | fertig |\n")
        self.write("memory/handoffs/tasks/T-001-build.md", "x")
        self.write("memory/handoffs/tasks/T-001-review.md", "Ergebnis: ok")
        self.write("memory/handoffs/tasks/T-001-security.md", "Ergebnis: ok")
        self.write("memory/gates.json", json.dumps({"pflicht": ["typecheck", "build"], "typecheck": "true",
                                                    "build": "false", "test": "true"}))
        self.assertEqual(self.run_runner("test", "T-001").returncode, 0)
        code, err = self.run_guard("stop")
        self.assertEqual(code, 2)
        self.assertIn("typecheck, build", err)
        r = self.run_runner("alle", "T-001")
        self.assertEqual(r.returncode, 1)
        self.assertIn("typecheck für T-001 bestanden", r.stdout)
        self.assertIn("rot: build", self.run_guard("stop")[1])
        self.write("memory/gates.json", json.dumps({"pflicht": ["typecheck", "build"], "typecheck": "true",
                                                    "build": "true", "test": "true"}))
        self.assertEqual(self.run_runner("alle", "T-001").returncode, 0)
        self.assertEqual(self.run_guard("stop")[0], 0)

    def test_all_stops_on_missing_command(self):
        self.write("memory/gates.json", json.dumps({"pflicht": ["lint"], "test": "true", "lint": ""}))
        r = self.run_runner("alle", "T-001")
        self.assertEqual(r.returncode, 65)
        self.assertIn("lint", r.stderr)

    def test_runner_needs_a_command(self):
        self.assertEqual(self.run_runner("test", "T-001").returncode, 65)
        self.assertEqual(self.run_runner("test", "kaputt").returncode, 64)
        self.assertFalse(os.path.exists(os.path.join(self.root, "memory/runs")))

    def test_evidence_cannot_be_written_by_hand(self):
        self.assertFalse(self.can_write("memory/runs/T-001-test.json"))
        self.assertFalse(self.can_write("memory/freigaben/brief.json"))
        bash = lambda c: self.run_guard("bash", tool_input={"command": c})[0]
        self.assertEqual(bash("echo '{\"exit\":0}' > memory/runs/T-001-test.json"), 2)
        self.assertEqual(bash("cp x memory/freigaben/brief.json"), 2)
        self.assertEqual(bash("sed -i s/a/b/ .claude/hooks/factory_guard.py"), 2)
        self.assertEqual(bash("python3 .claude/hooks/factory_run.py test T-001"), 0)
        self.assertEqual(bash("python3 .claude/hooks/factory_run.py test T-001; rm memory/runs/x"), 2)

    def test_gates_only_change_on_main(self):
        self.commit()
        self.assertTrue(self.can_write("memory/gates.json"))
        sh(self.root, "checkout", "-q", "-b", "task/T-001-login")
        self.assertFalse(self.can_write("memory/gates.json"))

    # Freigaben
    def say(self, text):
        return self.run_guard("prompt", prompt=text)

    def test_approval_gates_the_next_station(self):
        self.write("memory/handoffs/01-brief.md", "Brief v1")
        self.assertFalse(self.can_write("memory/handoffs/02-research.md"))
        code, _ = self.say("Freigabe Brief, aber ändere noch den Titel")
        self.assertEqual(code, 0)
        self.assertFalse(self.can_write("memory/handoffs/02-research.md"), "nur die reine Freigabe zählt")
        code, _ = self.say("Freigabe Brief")
        self.assertEqual(code, 0)
        self.assertTrue(self.can_write("memory/handoffs/02-research.md"))
        self.write("memory/handoffs/01-brief.md", "Brief v2")
        self.assertFalse(self.can_write("memory/handoffs/02-research.md"), "geänderter Brief braucht neue Freigabe")
        self.say("freigabe: brief.")
        self.assertTrue(self.can_write("memory/handoffs/02-research.md"))

    def test_approval_needs_the_document(self):
        r = subprocess.run([sys.executable, GUARD, "prompt"], input=json.dumps({"prompt": "Freigabe Design", "cwd": self.root}),
                           capture_output=True, text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=self.root))
        self.assertIn("nicht aufgezeichnet", r.stdout)
        self.assertFalse(os.path.exists(os.path.join(self.root, "memory/freigaben/design.json")))

    def test_ordinary_messages_stay_silent(self):
        r = subprocess.run([sys.executable, GUARD, "prompt"], input=json.dumps({"prompt": "mach weiter", "cwd": self.root}),
                           capture_output=True, text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=self.root))
        self.assertEqual((r.returncode, r.stdout, r.stderr), (0, "", ""))

    def test_design_and_tasks_need_their_approvals(self):
        self.write("memory/handoffs/03-architektur.md", "A")
        self.write("memory/handoffs/04-design.md", "D")
        self.assertFalse(self.can_write("memory/handoffs/04-design.md"))
        self.assertFalse(self.can_write("memory/handoffs/05-tasks.md"))
        self.say("Freigabe Architektur")
        self.say("Freigabe Design")
        self.assertTrue(self.can_write("memory/handoffs/04-design.md"))
        self.assertTrue(self.can_write("memory/handoffs/05-tasks.md"))

    def test_tag_needs_release_approval(self):
        self.write("VERSION", "0.0.1\n")
        bash = lambda c: self.run_guard("bash", tool_input={"command": c})[0]
        self.assertEqual(bash("git tag v0.0.1"), 2)
        self.assertEqual(bash("git tag -a v0.0.1 -m x && git push origin v0.0.1"), 2)
        self.assertEqual(bash("git tag -l"), 0)
        self.assertEqual(bash("git tag"), 0)
        self.say("Freigabe Release")
        self.assertEqual(bash("git tag v0.0.1"), 0)
        self.write("VERSION", "0.0.2\n")
        self.assertEqual(bash("git tag v0.0.2"), 2, "jede Version braucht ihre eigene Freigabe")

    def test_broken_input_never_blocks(self):
        r = subprocess.run([sys.executable, GUARD, "write"], input="kein json", capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
