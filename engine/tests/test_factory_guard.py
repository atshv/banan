"""Tests für die Schalter. Aufruf im Factory-Ordner: python3 -m unittest discover engine/tests"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HOOKS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "banan")
GUARD = os.path.join(HOOKS, "factory_guard.py")
RUNNER = os.path.join(HOOKS, "factory_run.py")

TASKS = """# Tasks
## T-001: Login
- Modul: auth
- Bereich: src/login/, tests/login/, app/page.tsx, `src/lib/*.ts`
- Fertig wenn: Login geht
- Tests zuerst: nein, reines Layout

## T-002: Ohne Bereich
- Modul: x

## T-003: Rechner
- Bereich: src/
- Fertig wenn: rechnet

## T-004: Zahlung
- Bereich: src/
- Tests zuerst: nein
- Heikel: ja

## T-005: Vertrag anpassen
- Bereich: src/
- Vertrag ändern: ja
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
        self.assertFalse(self.can_write(".banan/factory_guard.py"))

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
        self.assertEqual(self.run_runner("alle", "T-001").returncode, 0)
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

    # Präziser Code
    def done(self, task):
        self.status(f"| {task} | X | fertig |\n")
        for kind in ("build", "review", "security"):
            self.write(f"memory/handoffs/tasks/{task}-{kind}.md", "Ergebnis: ok")

    def gates(self, **data):
        self.write("memory/gates.json", json.dumps(data))

    def record(self, name):
        with open(os.path.join(self.root, "memory/runs", name), encoding="utf-8") as f:
            return json.load(f)

    def test_tests_must_fail_before_the_build(self):
        self.done("T-003")
        self.gates(test="true")
        self.assertEqual(self.run_runner("alle", "T-003").returncode, 0)
        self.assertIn("roten Testlauf", self.run_guard("stop")[1])
        self.assertEqual(self.run_runner("rot", "T-003").returncode, 1, "grüne Tests vor dem Bau zählen nicht")
        self.assertIn("roten Testlauf", self.run_guard("stop")[1])
        self.gates(test="false")
        self.assertEqual(self.run_runner("rot", "T-003").returncode, 0)
        self.gates(test="true")
        self.assertIn("bleibt bestehen", self.run_runner("rot", "T-003").stdout)
        self.assertEqual(self.record("T-003-rot.json")["exit"], 1)
        self.assertEqual(self.run_runner("alle", "T-003").returncode, 0)
        self.assertEqual(self.run_guard("stop")[0], 0)

    def test_tests_changed_after_red_run_are_flagged(self):
        self.gates(test="false")
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "task/T-003-rechner")
        self.write("src/a.test.ts", "erwartet 4")
        self.write("src/b.test.ts", "erwartet 5")
        self.run_runner("rot", "T-003")
        self.write("src/a.test.ts", "erwartet irgendwas")
        self.gates(test="true")
        r = self.run_runner("test", "T-003")
        self.assertEqual(self.record("T-003-test.json")["tests_seit_rot_geaendert"], ["src/a.test.ts"])
        self.assertIn("abgeschwächt", r.stdout)

    def test_task_size_limit(self):
        self.gates(test="true", max_zeilen=10)
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "task/T-003-rechner")
        self.write("src/big.ts", "x\n" * 30)
        r = self.run_runner("alle", "T-003")
        self.assertEqual(r.returncode, 1)
        self.assertIn("zu gross", r.stdout)
        self.assertEqual(self.record("T-003-groesse.json")["zeilen"], 30)
        self.gates(test="true", max_zeilen=100)
        self.assertEqual(self.run_runner("alle", "T-003").returncode, 0)

    def test_contract_is_locked(self):
        self.gates(test="true", vertrag=["src/contracts/"])
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "task/T-003-rechner")
        self.assertFalse(self.can_write("src/contracts/api.ts"))
        self.assertTrue(self.can_write("src/rechner.ts"))
        sh(self.root, "checkout", "-q", "-b", "task/T-005-vertrag")
        self.assertTrue(self.can_write("src/contracts/api.ts"))

    def test_risky_task_needs_second_review(self):
        self.done("T-004")
        self.gates(test="true")
        self.run_runner("alle", "T-004")
        code, err = self.run_guard("stop")
        self.assertEqual(code, 2)
        self.assertIn("zweite Review", err)
        self.write("memory/handoffs/tasks/T-004-review2.md", "Ergebnis: ok")
        self.assertEqual(self.run_guard("stop")[0], 0)

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
        self.assertEqual(bash("sed -i s/a/b/ .banan/factory_guard.py"), 2)
        self.assertEqual(bash("python3 .banan/factory_run.py test T-001"), 0)
        self.assertEqual(bash("python3 .banan/factory_run.py test T-001; rm memory/runs/x"), 2)

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

    # Andere KIs und Git
    def guard(self, mode, ki=None, **data):
        data.setdefault("cwd", self.root)
        env = {k: v for k, v in os.environ.items() if not k.endswith("_PROJECT_DIR")}
        args = [sys.executable, GUARD, mode] + (["--ki", ki] if ki else [])
        return subprocess.run(args, input=json.dumps(data), capture_output=True, text=True, env=env, cwd=self.root)

    def test_codex_patch_is_checked_file_by_file(self):
        self.commit()
        patch = "*** Begin Patch\n*** Update File: memory/status.md\n@@\n*** Add File: src/app.ts\n+x\n*** End Patch"
        r = self.guard("write", "codex", tool_name="apply_patch", tool_input={"command": patch})
        self.assertEqual(r.returncode, 2)
        self.assertIn("src/app.ts", r.stderr)
        ok = "*** Begin Patch\n*** Update File: memory/status.md\n@@\n*** End Patch"
        self.assertEqual(self.guard("write", "codex", tool_input={"command": ok}).returncode, 0)
        r = self.guard("bash", "codex", tool_input={"command": ["bash", "-lc", "apply_patch <<EOF\n" + patch + "\nEOF"]})
        self.assertEqual(r.returncode, 2)

    def test_gemini_and_cursor_inputs(self):
        self.commit()
        self.assertEqual(self.guard("write", "gemini", tool_name="write_file",
                                    tool_input={"file_path": "src/a.ts", "content": "x"}).returncode, 2)
        self.assertEqual(self.guard("bash", "gemini", tool_name="run_shell_command",
                                    tool_input={"command": "git tag v1"}).returncode, 2)
        self.assertEqual(self.guard("write", "cursor", tool_name="Write", tool_input={"path": "src/a.ts"}).returncode, 2)
        self.assertEqual(self.guard("bash", "cursor", command="rm -r memory/runs").returncode, 2)
        self.assertEqual(self.guard("bash", "cursor", command="npm test").returncode, 0)

    def test_stop_answers_in_each_dialect(self):
        self.status("| T-001 | Login | in Arbeit |\n")
        self.assertEqual(self.guard("stop", "gemini").returncode, 2)
        self.assertEqual(self.guard("stop", "gemini", stop_hook_active=True).returncode, 0)
        r = self.guard("stop", "codex")
        self.assertEqual((r.returncode, json.loads(r.stdout)["decision"]), (0, "block"))
        r = self.guard("stop", "cursor")
        self.assertIn("T-001", json.loads(r.stdout)["followup_message"])
        self.assertEqual(self.guard("stop", "cursor", loop_count=1).stdout, "")

    def test_prompt_note_is_json_for_the_right_event(self):
        self.write("memory/handoffs/01-brief.md", "B")
        r = self.guard("prompt", "gemini", prompt="Freigabe Brief")
        self.assertEqual(json.loads(r.stdout)["hookSpecificOutput"]["hookEventName"], "BeforeAgent")
        r = self.guard("prompt", "codex", prompt="Freigabe Brief")
        self.assertEqual(json.loads(r.stdout)["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")

    def test_git_hook_checks_every_commit(self):
        self.commit()
        hook = os.path.join(HOOKS, "githooks", "pre-commit")
        os.makedirs(os.path.join(self.root, ".banan"))
        for name in ("factory_guard.py", "factory_run.py"):
            with open(os.path.join(HOOKS, name), encoding="utf-8") as src:
                self.write(f".banan/{name}", src.read())
        sh(self.root, "add", "-A")
        sh(self.root, "commit", "-q", "-m", "banan")
        sh(self.root, "config", "core.hooksPath", os.path.dirname(hook))
        commit = lambda: subprocess.run(["git", "-C", self.root, "commit", "-q", "-m", "x"], capture_output=True, text=True)
        self.write("src/app.ts", "x")
        sh(self.root, "add", "-A")
        r = commit()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Produktcode", r.stderr)
        sh(self.root, "checkout", "-q", "-b", "task/T-003-rechner")
        self.assertEqual(commit().returncode, 0)
        self.write("docs/x.md", "ausserhalb")
        self.write("memory/runs/T-003-test.json", "{}")
        sh(self.root, "add", "-A")
        r = commit()
        self.assertIn("ausserhalb des Bereichs", r.stderr)
        sh(self.root, "reset", "-q", "docs/x.md")
        self.assertEqual(commit().returncode, 0, "Nachweise in memory/runs dürfen committet werden")

    def test_check_command_and_terminal_only_approval(self):
        self.status("| T-001 | Login | in Arbeit |\n")
        r = self.guard("pruefe")
        self.assertEqual(r.returncode, 1)
        self.assertIn("T-001", r.stdout)
        self.status("| T-001 | Login | offen |\n")
        self.assertEqual(self.guard("pruefe").returncode, 0)
        self.write("memory/handoffs/01-brief.md", "B")
        r = subprocess.run([sys.executable, os.path.join(HOOKS, "freigabe.py"), "brief"], input="ja\n",
                           capture_output=True, text=True, cwd=self.root)
        self.assertEqual(r.returncode, 2, "ohne echtes Terminal keine Freigabe")
        self.assertFalse(os.path.exists(os.path.join(self.root, "memory/freigaben/brief.json")))
        self.assertEqual(self.guard("bash", tool_input={"command": "python3 .banan/freigabe.py brief"}).returncode, 2)
        self.assertEqual(self.guard("bash", tool_input={"command": "python3 .banan/factory_guard.py pruefe"}).returncode, 0)
        self.assertEqual(self.guard("bash", tool_input={"command": "git commit --no-verify -m x"}).returncode, 2)

    # Bestehendes Projekt
    def bash(self, command):
        return self.run_guard("bash", tool_input={"command": command})[0] == 0

    def test_existing_project_needs_survey_then_brief(self):
        self.gates(modus="bestand")
        self.assertFalse(self.can_write("memory/handoffs/01-brief.md"), "erst die Freigabe Bestand")
        self.write("memory/handoffs/00-bestand.md", "Karte")
        self.run_guard("prompt", prompt="Freigabe Bestand")
        self.assertTrue(self.can_write("memory/handoffs/01-brief.md"))
        self.assertFalse(self.can_write("memory/handoffs/05-tasks.md"), "erst die Freigabe Brief")
        self.write("memory/handoffs/01-brief.md", "Auftrag")
        self.run_guard("prompt", prompt="Freigabe Brief")
        self.assertTrue(self.can_write("memory/handoffs/05-tasks.md"), "ohne Architektur und Design")
        self.write("memory/handoffs/00-bestand.md", "Karte, geändert")
        self.assertFalse(self.can_write("memory/handoffs/01-brief.md"))

    def test_any_branch_with_a_task_number_is_a_task_branch(self):
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "feature/T-001-login")
        self.assertTrue(self.can_write("src/login/form.tsx"))
        self.assertFalse(self.can_write("src/profile/x.tsx"))
        sh(self.root, "checkout", "-q", "-b", "feature/NOT-1-x")
        self.assertTrue(self.can_write("src/profile/x.tsx"))

    def test_pull_request_mode_plans_on_the_branch_once(self):
        self.gates(abschluss="pr", modus="bestand")
        self.write("memory/handoffs/01-brief.md", "Auftrag")
        self.run_guard("prompt", prompt="Freigabe Brief")
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "feature/T-006-lasso")
        self.assertTrue(self.can_write("memory/handoffs/05-tasks.md"), "T-006 ist noch nicht geplant")
        self.assertFalse(self.can_write("memory/gates.json"))
        self.write("memory/handoffs/05-tasks.md", TASKS + "\n## T-006: Lasso\n- Bereich: src/lasso/\n")
        self.assertTrue(self.can_write("memory/handoffs/05-tasks.md"), "bis zum Commit des Plans")
        self.commit()
        self.assertFalse(self.can_write("memory/handoffs/05-tasks.md"), "danach gesperrt")
        self.assertTrue(self.can_write("src/lasso/a.ts"))
        self.assertFalse(self.can_write("src/login/a.ts"))

    def test_pull_request_mode_leaves_merging_and_tags_to_people(self):
        self.commit()
        for cmd in ("git merge feature/T-001-x", "git push origin main", "git push", "git tag v1.0.0",
                    "gh pr merge 12 --squash", "gh release create v1"):
            self.gates(abschluss="pr")
            self.assertFalse(self.bash(cmd), cmd)
        for cmd in ("git merge --ff-only origin/main", "git tag --list", "git fetch origin", "gh pr create --fill",
                    "gh pr view 3 --json state"):
            self.assertTrue(self.bash(cmd), cmd)
        sh(self.root, "checkout", "-q", "-b", "feature/T-001-login")
        for cmd in ("git push -u origin feature/T-001-login", "git push", "git merge origin/main"):
            self.assertTrue(self.bash(cmd), cmd)
        self.assertFalse(self.bash("git push origin HEAD:main"))
        self.write("memory/freigaben/release-1.json", "{}")
        self.assertFalse(self.bash("git tag v1.0.0"), "auch mit Freigabe setzt die KI keinen Tag")

    def test_conditional_gates_run_only_for_matching_files(self):
        self.gates(pflicht=["native"], test="true", native="false", wenn={"native": ["core/", "*.cpp"]})
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "task/T-003-rechner")
        self.write("src/a.ts", "x")
        self.assertEqual(self.run_runner("alle", "T-003").returncode, 0)
        self.assertTrue(self.record("T-003-native.json")["uebersprungen"])
        self.write("src/deep/b.cpp", "x")
        self.assertEqual(self.run_runner("alle", "T-003").returncode, 1)
        self.assertNotIn("uebersprungen", self.record("T-003-native.json"))

    def test_size_ignores_listed_files(self):
        self.gates(test="true", max_zeilen=5, zaehlt_nicht=["fixtures/", "*.snap"])
        self.commit()
        sh(self.root, "checkout", "-q", "-b", "task/T-003-rechner")
        self.write("fixtures/big.json", "x\n" * 50)
        self.write("src/a.snap", "x\n" * 50)
        self.write("src/a.ts", "x\n" * 4)
        self.assertEqual(self.run_runner("alle", "T-003").returncode, 0)
        self.assertEqual(self.record("T-003-groesse.json")["zeilen"], 4)
        self.write("src/b.ts", "x\n" * 4)
        self.assertEqual(self.run_runner("alle", "T-003").returncode, 1)

    def test_broken_input_never_blocks(self):
        r = subprocess.run([sys.executable, GUARD, "write"], input="kein json", capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
