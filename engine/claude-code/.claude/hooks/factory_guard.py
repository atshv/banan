#!/usr/bin/env python3
"""Schalter der Software Factory fuer Claude Code.

Aufruf durch Hooks in .claude/settings.json, Eingabe als JSON auf stdin:
  factory_guard.py write   vor Write/Edit      -> Schreibsperre main, Task-Bereich
  factory_guard.py bash    vor Bash            -> kein Commit von Produktcode auf main
  factory_guard.py stop    vor dem Aufhoeren   -> offene Tasks, fehlende Nachweise

Exit 0 = erlaubt. Exit 2 = blockiert, der Text auf stderr geht an die KI.
Bei einem eigenen Fehler laesst das Script alles durch, damit es nie die Arbeit lahmlegt.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys

MAIN = {"main", "master"}
ADMIN_DIRS = ("memory/", "factory/", ".claude/")
ADMIN_FILES = {"CLAUDE.md", "VERSION", "CHANGELOG.md", "README.md", ".gitignore", ".env.example", "LICENSE"}
PROTECTED_DIRS = (".claude/hooks/",)
PROTECTED_FILES = {".claude/settings.json"}
LOCKFILES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb",
    "Package.resolved", "Podfile.lock", "Gemfile.lock", "poetry.lock", "uv.lock", "Cargo.lock",
}
TASKS = "memory/handoffs/05-tasks.md"
STATUS = "memory/status.md"
REPORTS = "memory/handoffs/tasks"
ACTIVE = {"in arbeit", "test", "review", "security"}
PASS = {"ok", "grün", "gruen"}


def git(root, *args):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def branch(root):
    """Aktueller Branch. None ohne Git, ohne ersten Commit oder bei losem HEAD."""
    if git(root, "rev-parse", "--verify", "-q", "HEAD") is None:
        return None
    return git(root, "symbolic-ref", "--short", "-q", "HEAD") or None


def rel(root, cwd, path):
    """Pfad relativ zum Projekt, None wenn er ausserhalb liegt."""
    if not path:
        return None
    full = os.path.realpath(os.path.join(cwd or root, path))
    base = os.path.realpath(root)
    if full != base and not full.startswith(base + os.sep):
        return None
    return os.path.relpath(full, base).replace(os.sep, "/")


def is_admin(r):
    return r in ADMIN_FILES or r.startswith(ADMIN_DIRS)


def is_protected(r):
    return r in PROTECTED_FILES or r.startswith(PROTECTED_DIRS)


def task_no(name):
    m = re.match(r"task/T-(\d+)", name or "", re.I)
    return int(m.group(1)) if m else None


def scope(root, no):
    """Bereich eines Tasks aus 05-tasks.md, None wenn keiner eingetragen ist."""
    try:
        lines = open(os.path.join(root, TASKS), encoding="utf-8").read().splitlines()
    except OSError:
        return None
    current = None
    for line in lines:
        h = re.match(r"#{1,6}\s*T-(\d+)\b", line)
        if h:
            current = int(h.group(1))
            continue
        if current == no:
            m = re.match(r"\s*[-*]?\s*\**Bereich\**\s*:\s*\**\s*(.+)$", line, re.I)
            if m:
                items = [p.strip().strip("`").strip() for p in m.group(1).split(",")]
                return [p[2:] if p.startswith("./") else p for p in items if p]
    return None


def in_scope(r, entries):
    for e in entries:
        if e.endswith("/"):
            if r.startswith(e):
                return True
        elif "*" in e:
            if fnmatch.fnmatch(r, e):
                return True
        elif r == e or r.startswith(e + "/"):
            return True
    return False


def check_write(root, cwd, path):
    r = rel(root, cwd, path)
    if r is None:
        return None
    if is_protected(r):
        return f"Factory-Schalter: {r} gehört zu den Schaltern der Factory. Nur der Auftraggeber ändert sie."
    b = branch(root)
    if b is None:
        return None
    if b in MAIN:
        if is_admin(r):
            return None
        return (f"Factory-Schalter: {r} ist Produktcode und darf nicht direkt auf {b} geändert werden. "
                "Wechsle auf einen Branch (task/T-<Nr>-<kurzname> oder setup/<name>) und arbeite dort.")
    no = task_no(b)
    if no is None:
        return None
    if r == TASKS:
        return f"Factory-Schalter: {TASKS} wird nur auf main geändert, nicht auf einem Task-Branch."
    if r.startswith("memory/") or os.path.basename(r) in LOCKFILES:
        return None
    entries = scope(root, no)
    if entries is None:
        return (f"Factory-Schalter: Task T-{no} hat in {TASKS} keine Zeile 'Bereich:'. "
                "Stopp und melde das dem Orchestrator. Er trägt den Bereich auf main ein.")
    if in_scope(r, entries):
        return None
    return (f"Factory-Schalter: {r} liegt ausserhalb des Bereichs von T-{no} ({', '.join(entries)}). "
            "Bleib im Bereich. Braucht der Task wirklich mehr, stopp und melde es dem Orchestrator.")


def check_bash(root, command):
    if not re.search(r"\bgit\b[^|;&\n]*\bcommit\b", command or ""):
        return None
    b = branch(root)
    if b not in MAIN:
        return None
    git_dir = git(root, "rev-parse", "--absolute-git-dir")
    if git_dir and os.path.exists(os.path.join(git_dir, "MERGE_HEAD")):
        return None
    changed = (git(root, "diff", "--name-only", "HEAD") or "").splitlines()
    changed += (git(root, "ls-files", "--others", "--exclude-standard") or "").splitlines()
    bad = sorted({f for f in changed if f and not is_admin(f)})
    if not bad:
        return None
    shown = ", ".join(bad[:5]) + (" …" if len(bad) > 5 else "")
    return (f"Factory-Schalter: Auf {b} wird kein Produktcode direkt committet ({shown}). "
            "Lege zuerst in einem eigenen Befehl einen Branch an und committe dort. "
            "Nach main kommt Code nur per git merge.")


def reports(root):
    found = {}
    try:
        names = os.listdir(os.path.join(root, REPORTS))
    except OSError:
        return found
    for name in names:
        m = re.match(r"T-(\d+)-(build|test|review|security)\.md$", name, re.I)
        if m:
            found[(int(m.group(1)), m.group(2).lower())] = os.path.join(root, REPORTS, name)
    return found


def passed(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return False
    m = re.search(r"ergebnis\**\s*:\s*\**\s*([A-Za-zäöüÄÖÜ]+)", text, re.I)
    return bool(m) and m.group(1).lower() in PASS


def check_stop(root):
    try:
        lines = open(os.path.join(root, STATUS), encoding="utf-8").read().splitlines()
    except OSError:
        return None
    found = reports(root)
    problems = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        m = re.match(r"T-(\d+)$", cells[0])
        if not m:
            continue
        no, label, state = int(m.group(1)), cells[0], cells[2].lower()
        if state in ACTIVE:
            problems.append(f"{label} ist noch unterwegs (Status '{cells[2]}').")
        elif state == "fertig":
            if (no, "build") not in found:
                problems.append(f"{label} steht auf 'fertig', aber der Build-Bericht fehlt.")
            for kind, word in (("test", "Test"), ("review", "Review"), ("security", "Security")):
                path = found.get((no, kind))
                if path is None:
                    problems.append(f"{label} steht auf 'fertig', aber der {word}-Bericht fehlt.")
                elif not passed(path):
                    problems.append(f"{label} steht auf 'fertig', aber der {word}-Bericht ist nicht bestanden.")
    if not problems:
        return None
    shown = " ".join(problems[:6]) + (" …" if len(problems) > 6 else "")
    return ("Factory-Schalter: " + shown + " Führe die Tasks zu Ende oder setz sie in memory/status.md auf "
            "'blockiert' mit Grund. Fehlende Nachweise holst du nach, statt den Status zu behaupten. "
            "Wartest du nur auf eine Antwort des Auftraggebers, sag ihm das und hör dann auf.")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        data = {}
    cwd = data.get("cwd") or os.getcwd()
    root = os.environ.get("CLAUDE_PROJECT_DIR") or cwd
    tool = data.get("tool_input") or {}
    reason = None
    if mode == "write":
        reason = check_write(root, cwd, tool.get("file_path") or tool.get("notebook_path"))
    elif mode == "bash":
        reason = check_bash(root, tool.get("command"))
    elif mode == "stop" and not data.get("stop_hook_active"):
        reason = check_stop(root)
    if reason:
        print(reason, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
