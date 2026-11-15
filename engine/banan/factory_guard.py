#!/usr/bin/env python3
"""Schalter von banan. Laeuft mit jeder KI, die Hooks kennt, und als Git-Hook mit allen anderen.

Aufruf durch die Hooks der jeweiligen KI, Eingabe als JSON auf stdin:
  factory_guard.py write  [--ki NAME]  vor dem Schreiben    -> Schreibsperre main, Task-Bereich, Vertrag, Freigaben
  factory_guard.py bash   [--ki NAME]  vor Shell-Befehlen   -> Commit auf main, Tag ohne Freigabe, geschuetzte Ordner
  factory_guard.py stop   [--ki NAME]  vor dem Aufhoeren    -> offene Tasks, fehlende Nachweise
  factory_guard.py prompt [--ki NAME]  bei jeder Nachricht  -> zeichnet "Freigabe <Checkpoint>" auf
Ohne Hooks, fuer jede KI:
  factory_guard.py commit              als Git pre-commit   -> dieselben Schreibregeln fuer alles, was committet wird
  factory_guard.py pruefe              von Hand oder durch die KI -> dieselbe Pruefung wie stop

NAME ist claude (Standard), cursor, gemini oder codex.
Exit 0 = erlaubt. Exit 2 = blockiert, der Text auf stderr geht an die KI.
Bei einem eigenen Fehler laesst das Script alles durch, damit es nie die Arbeit lahmlegt.
"""
import datetime
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys

MAIN = {"main", "master"}
ADMIN_DIRS = ("memory/", "factory/", ".banan/", ".agents/", ".claude/", ".cursor/", ".gemini/", ".codex/")
ADMIN_FILES = {"AGENTS.md", "CLAUDE.md", "GEMINI.md", "VERSION", "CHANGELOG.md", "README.md", ".gitignore", ".env.example", "LICENSE"}
RUNS = "memory/runs"
APPROVALS = "memory/freigaben"
PROTECTED_DIRS = (".banan/", RUNS + "/", APPROVALS + "/")
PROTECTED_FILES = {".claude/settings.json", ".cursor/hooks.json", ".gemini/settings.json",
                   ".codex/hooks.json", ".codex/config.toml"}
RUNNER = ".banan/factory_run.py"
CHECKER = ".banan/factory_guard.py pruefe"
LOCKFILES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb",
    "Package.resolved", "Podfile.lock", "Gemfile.lock", "poetry.lock", "uv.lock", "Cargo.lock",
}
TASKS = "memory/handoffs/05-tasks.md"
GATES = "memory/gates.json"
STATUS = "memory/status.md"
REPORTS = "memory/handoffs/tasks"
ACTIVE = {"in arbeit", "test", "review", "security"}
PASS = {"ok", "grün", "gruen"}

# Checkpoint -> Datei, die der Auftraggeber freigibt
CHECKPOINTS = {
    "brief": "memory/handoffs/01-brief.md",
    "architektur": "memory/handoffs/03-architektur.md",
    "design": "memory/handoffs/04-design.md",
}
# Datei -> Checkpoint, der vorher freigegeben sein muss
NEEDS = {
    "memory/handoffs/02-research.md": "brief",
    "memory/handoffs/04-design.md": "architektur",
    TASKS: "design",
}


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


def read(root, path):
    try:
        with open(os.path.join(root, path), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def read_json(root, path):
    try:
        return json.loads(read(root, path) or "")
    except ValueError:
        return None


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def is_admin(r):
    return r in ADMIN_FILES or r.startswith(ADMIN_DIRS)


def is_protected(r):
    return r in PROTECTED_FILES or r.startswith(PROTECTED_DIRS)


def task_no(name):
    m = re.match(r"task/T-(\d+)", name or "", re.I)
    return int(m.group(1)) if m else None


# ---------- Freigaben ----------

def version(root):
    return (read(root, "VERSION") or "").strip()


def approved(root, checkpoint):
    """True, wenn der Auftraggeber genau den heutigen Stand der Datei freigegeben hat."""
    record = read_json(root, f"{APPROVALS}/{checkpoint}.json")
    current = read(root, CHECKPOINTS[checkpoint])
    return bool(record) and current is not None and record.get("sha256") == sha(current)


def release_approved(root):
    v = version(root)
    record = read_json(root, f"{APPROVALS}/release-{v}.json") if v else None
    return bool(record) and record.get("version") == v


def record_approval(root, prompt):
    """Zeichnet 'Freigabe <Checkpoint>' auf. Gibt den Text fuer die KI zurueck oder None."""
    m = re.match(r"\s*freigabe\s*:?\s+(brief|architektur|design|release)\s*[.!]?\s*$", prompt or "", re.I)
    if not m:
        return None
    name = m.group(1).lower()
    record = {"checkpoint": name, "zeit": datetime.datetime.now().astimezone().isoformat(timespec="seconds")}
    if name == "release":
        v = version(root)
        if not v:
            return "Freigabe nicht aufgezeichnet. Die Datei VERSION fehlt oder ist leer."
        record["version"] = v
        target = f"{APPROVALS}/release-{v}.json"
        label = f"Release {v}"
    else:
        source = CHECKPOINTS[name]
        text = read(root, source)
        if text is None:
            return f"Freigabe nicht aufgezeichnet. {source} gibt es noch nicht."
        record.update(datei=source, sha256=sha(text))
        target = f"{APPROVALS}/{name}.json"
        label = name.capitalize()
    os.makedirs(os.path.join(root, APPROVALS), exist_ok=True)
    with open(os.path.join(root, target), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return f"Factory: Freigabe '{label}' des Auftraggebers ist aufgezeichnet in {target}."


# ---------- Schreiben ----------

def task_fields(root, no):
    """Felder eines Tasks aus 05-tasks.md als {name in Kleinbuchstaben: wert}."""
    fields = {}
    text = read(root, TASKS)
    if text is None:
        return fields
    current = None
    for line in text.splitlines():
        h = re.match(r"#{1,6}\s*T-(\d+)\b", line)
        if h:
            current = int(h.group(1))
            continue
        if current == no:
            m = re.match(r"\s*[-*]?\s*\**([^:*]{1,40}?)\**\s*:\s*\**\s*(.+)$", line)
            if m:
                fields.setdefault(m.group(1).strip().lower(), m.group(2).strip())
    return fields


def path_list(value):
    items = [p.strip().strip("`").strip() for p in (value or "").split(",")]
    return [p[2:] if p.startswith("./") else p for p in items if p]


def scope(root, no):
    """Bereich eines Tasks, None wenn keiner eingetragen ist."""
    return path_list(task_fields(root, no).get("bereich")) or None


def says(fields, key, word):
    return fields.get(key, "").lower().startswith(word)


def contract_paths(root):
    """Vertrags-Dateien aus gates.json (Liste 'vertrag')."""
    gates = read_json(root, GATES)
    listed = gates.get("vertrag") if isinstance(gates, dict) else None
    return path_list(",".join(p for p in listed if isinstance(p, str))) if isinstance(listed, list) else []


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


def check_write(root, cwd, path, tool=True):
    """Grund, warum die Datei nicht geschrieben werden darf, sonst None. tool=False beim Commit."""
    r = rel(root, cwd, path)
    if r is None:
        return None
    if tool and is_protected(r):
        return (f"Factory-Schalter: {r} gehört zu den Schaltern und Nachweisen der Factory. "
                "Die KI ändert sie nicht von Hand.")
    need = NEEDS.get(r)
    if need and not approved(root, need):
        return (f"Factory-Schalter: {r} braucht zuerst die Freigabe '{need.capitalize()}' des Auftraggebers "
                f"für den heutigen Stand von {CHECKPOINTS[need]}. Zeig ihm das Ergebnis in einfacher Sprache "
                f"und bitte ihn, als eigene Nachricht 'Freigabe {need.capitalize()}' zu schreiben. Dann hör auf.")
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
    if r in (TASKS, GATES):
        return f"Factory-Schalter: {r} wird nur auf main geändert, nicht auf einem Task-Branch."
    if r.startswith("memory/") or os.path.basename(r) in LOCKFILES:
        return None
    fields = task_fields(root, no)
    if in_scope(r, contract_paths(root)) and not says(fields, "vertrag ändern", "ja"):
        return (f"Factory-Schalter: {r} gehört zum Vertrag (Schnittstellen und Datentypen). T-{no} darf ihn nicht "
                "ändern. Bau gegen den Vertrag. Muss er sich ändern, stopp und melde es dem Orchestrator.")
    entries = path_list(fields.get("bereich")) or None
    if entries is None:
        return (f"Factory-Schalter: Task T-{no} hat in {TASKS} keine Zeile 'Bereich:'. "
                "Stopp und melde das dem Orchestrator. Er trägt den Bereich auf main ein.")
    if in_scope(r, entries):
        return None
    return (f"Factory-Schalter: {r} liegt ausserhalb des Bereichs von T-{no} ({', '.join(entries)}). "
            "Bleib im Bereich. Braucht der Task wirklich mehr, stopp und melde es dem Orchestrator.")


# ---------- Shell ----------

def check_bash(root, command):
    command = command or ""
    rest = command.replace(RUNNER, "").replace(CHECKER, "")
    for p in (".banan", *sorted(PROTECTED_FILES), RUNS, APPROVALS):
        if p in rest:
            return (f"Factory-Schalter: Shell-Befehle fassen {p} nicht an. Lies solche Dateien mit dem "
                    f"Lese-Werkzeug. Testläufe zeichnet nur 'python3 {RUNNER} <gate> <T-Nr>' auf.")
    tag = re.search(r"\bgit\b[^|;&\n]*?\btag\b([^|;&\n]*)", command)
    if tag:
        args = tag.group(1).split()
        listing = {"-l", "--list", "-d", "--delete", "-n", "-v", "--verify", "--contains", "--points-at"}
        if args and not listing.intersection(args) and not release_approved(root):
            v = version(root) or "?"
            return (f"Factory-Schalter: Für Version {v} fehlt die Freigabe 'Release' des Auftraggebers. "
                    "Zeig ihm den Statusbericht und bitte ihn, als eigene Nachricht 'Freigabe Release' "
                    "zu schreiben. Dann hör auf.")
    if not re.search(r"\bgit\b[^|;&\n]*\bcommit\b", command):
        return None
    if "--no-verify" in command:
        return "Factory-Schalter: Commits laufen immer mit den Prüfungen, ohne --no-verify."
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


# ---------- Aufhoeren ----------

def reports(root):
    found = {}
    try:
        names = os.listdir(os.path.join(root, REPORTS))
    except OSError:
        return found
    for name in names:
        m = re.match(r"T-(\d+)-(build|review2?|security)\.md$", name, re.I)
        if m:
            found[(int(m.group(1)), m.group(2).lower())] = f"{REPORTS}/{name}"
    return found


def recorded_runs(root):
    """Aufgezeichnete Laeufe: (Task-Nummer, Pruefung) -> Exit-Code."""
    found = {}
    try:
        names = os.listdir(os.path.join(root, RUNS))
    except OSError:
        return found
    for name in names:
        m = re.match(r"T-(\d+)-([a-z][a-z0-9-]*)\.json$", name, re.I)
        record = read_json(root, f"{RUNS}/{name}") if m else None
        if isinstance(record, dict):
            found[(int(m.group(1)), m.group(2).lower())] = record.get("exit")
    return found


def required_gates(root):
    """Pflicht-Pruefungen aus gates.json. 'test' gehoert immer dazu."""
    gates = read_json(root, GATES)
    listed = gates.get("pflicht") if isinstance(gates, dict) else None
    names = [g for g in listed if isinstance(g, str) and g] if isinstance(listed, list) else []
    return names if "test" in names else names + ["test"]


def passed(root, path):
    m = re.search(r"ergebnis\**\s*:\s*\**\s*([A-Za-zäöüÄÖÜ]+)", read(root, path) or "", re.I)
    return bool(m) and m.group(1).lower() in PASS


def check_stop(root):
    text = read(root, STATUS)
    if text is None:
        return None
    found, runs, required = reports(root), recorded_runs(root), required_gates(root)
    problems = []
    for line in text.splitlines():
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
            fields = task_fields(root, no)
            if not says(fields, "tests zuerst", "nein") and runs.get((no, "rot"), 0) == 0:
                problems.append(f"{label} steht auf 'fertig', aber es gibt keinen roten Testlauf vor dem Bau "
                                f"(python3 {RUNNER} rot {label}).")
            needed = required + ["groesse"]
            missing = [g for g in needed if (no, g) not in runs]
            red = [g for g in needed if runs.get((no, g), 0) != 0]
            if missing:
                problems.append(f"{label} steht auf 'fertig', aber diese Prüfungen sind nicht aufgezeichnet: "
                                f"{', '.join(missing)} (python3 {RUNNER} alle {label}).")
            if red:
                problems.append(f"{label} steht auf 'fertig', aber diese Prüfungen sind rot: {', '.join(red)}.")
            checks = [("review", "Review"), ("security", "Security")]
            if says(fields, "heikel", "ja"):
                checks.insert(1, ("review2", "zweite Review"))
            for kind, word in checks:
                path = found.get((no, kind))
                if path is None:
                    problems.append(f"{label} steht auf 'fertig', aber der {word}-Bericht fehlt.")
                elif not passed(root, path):
                    problems.append(f"{label} steht auf 'fertig', aber der {word}-Bericht ist nicht bestanden.")
    if not problems:
        return None
    shown = " ".join(problems[:6]) + (" …" if len(problems) > 6 else "")
    return ("Factory-Schalter: " + shown + " Führe die Tasks zu Ende oder setz sie in memory/status.md auf "
            "'blockiert' mit Grund. Fehlende Nachweise holst du nach, statt den Status zu behaupten. "
            "Wartest du nur auf eine Antwort des Auftraggebers, sag ihm das und hör dann auf.")


# ---------- Eingabe und Ausgabe je KI ----------

def project_root(cwd):
    for name in ("CLAUDE_PROJECT_DIR", "GEMINI_PROJECT_DIR", "CURSOR_PROJECT_DIR"):
        if os.environ.get(name):
            return os.environ[name]
    return git(cwd, "rev-parse", "--show-toplevel") or cwd


def patch_paths(text):
    """Dateien aus einem apply_patch-Text (Codex)."""
    found = re.findall(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$", text or "", re.M)
    return [p.strip() for pair in found for p in pair if p.strip()]


def shell_command(data, tool):
    command = tool.get("command") or data.get("command") or ""
    return " ".join(str(c) for c in command) if isinstance(command, list) else str(command)


def tool_paths(data, tool):
    """Dateien, die ein Schreib-Werkzeug anfassen will. Die KIs nennen das Feld verschieden."""
    patched = patch_paths(shell_command(data, tool))
    if patched:
        return patched
    for source in (tool, data):
        for key in ("file_path", "notebook_path", "path", "filePath", "target_file", "absolute_path"):
            if isinstance(source.get(key), str) and source[key]:
                return [source[key]]
    return []


def check_commit(root):
    """Git pre-commit: dieselben Schreibregeln fuer alle vorgemerkten Dateien."""
    if branch(root) is None:
        return None
    staged = (git(root, "diff", "--cached", "--name-only") or "").splitlines()
    reasons = [r for r in (check_write(root, root, f, tool=False) for f in staged if f) if r]
    return "\n".join(reasons[:3]) if reasons else None


def block(ki, mode, reason):
    if mode == "stop" and ki == "codex":
        print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
        sys.exit(0)
    if mode == "stop" and ki == "cursor":
        print(json.dumps({"followup_message": reason}, ensure_ascii=False))
        sys.exit(0)
    print(reason, file=sys.stderr)
    sys.exit(2)


def main():
    args = sys.argv[1:]
    mode = args[0] if args else ""
    ki = args[args.index("--ki") + 1] if "--ki" in args[:-1] else "claude"
    data = {}
    if mode not in ("commit", "pruefe"):
        try:
            data = json.loads(sys.stdin.read() or "{}")
        except ValueError:
            data = {}
        if not isinstance(data, dict):
            data = {}
    cwd = data.get("cwd") or os.getcwd()
    root = project_root(cwd)
    tool = data.get("tool_input") if isinstance(data.get("tool_input"), dict) else {}
    reason = None
    if mode == "prompt":
        note = record_approval(root, data.get("prompt"))
        if note and ki != "cursor":
            event = "BeforeAgent" if ki == "gemini" else "UserPromptSubmit"
            print(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": note}},
                             ensure_ascii=False))
        return
    if mode == "commit":
        reason = check_commit(root)
        if reason:
            print(reason, file=sys.stderr)
            sys.exit(1)
        return
    if mode == "pruefe":
        reason = check_stop(root)
        print(reason or "Factory: Alles in Ordnung, kein Task ist offen oder ohne Nachweis.")
        sys.exit(1 if reason else 0)
    if mode == "write":
        reason = next((r for r in (check_write(root, cwd, p) for p in tool_paths(data, tool)) if r), None)
    elif mode == "bash":
        command = shell_command(data, tool)
        reason = check_bash(root, command) or next(
            (r for r in (check_write(root, cwd, p) for p in patch_paths(command)) if r), None)
    elif mode == "stop":
        again = data.get("stop_hook_active") or (isinstance(data.get("loop_count"), int) and data["loop_count"] > 0)
        reason = None if again else check_stop(root)
    if reason:
        block(ki, mode, reason)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
