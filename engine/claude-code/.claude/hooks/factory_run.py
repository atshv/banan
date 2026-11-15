#!/usr/bin/env python3
"""Fuehrt Pruefungen aus und zeichnet das Ergebnis auf.

Aufruf im Projektordner:
  python3 .claude/hooks/factory_run.py rot <T-Nr>          vor dem Bau: die neuen Tests muessen scheitern
  python3 .claude/hooks/factory_run.py alle <T-Nr>         nach dem Bau: alle Pflicht-Pruefungen und die Groesse
  python3 .claude/hooks/factory_run.py <pruefung> <T-Nr>   eine einzelne Pruefung, z. B. test T-001

Die Befehle stehen in memory/gates.json, z. B.
  {"pflicht": ["typecheck", "lint", "test", "build"], "test": "npm test", "max_zeilen": 800, ...}
Jedes Ergebnis landet in memory/runs/T-<Nr>-<pruefung>.json. Nur dieses Script schreibt dort.
Der Stop-Check glaubt fuer 'fertig' nur aufgezeichneten Laeufen.
"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

GATES = "memory/gates.json"
TASKS = "memory/handoffs/05-tasks.md"
RUNS = "memory/runs"
TIMEOUT = 30 * 60
TAIL = 40
MAX_LINES = 800
LOCKFILES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb",
    "Package.resolved", "Podfile.lock", "Gemfile.lock", "poetry.lock", "uv.lock", "Cargo.lock",
}


def git(root, *args):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def now():
    return datetime.datetime.now().astimezone()


def load_json(root, path):
    try:
        with open(os.path.join(root, path), encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def required(gates):
    listed = gates.get("pflicht")
    names = [g for g in listed if isinstance(g, str) and g] if isinstance(listed, list) else []
    return names if "test" in names else names + ["test"]


def task_field(root, task, key):
    """Wert eines Feldes des Tasks aus 05-tasks.md, sonst ''."""
    try:
        with open(os.path.join(root, TASKS), encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return ""
    no, current = int(task[2:]), None
    for line in lines:
        h = re.match(r"#{1,6}\s*T-(\d+)\b", line)
        if h:
            current = int(h.group(1))
            continue
        if current == no:
            m = re.match(r"\s*[-*]?\s*\**([^:*]{1,40}?)\**\s*:\s*\**\s*(.+)$", line)
            if m and m.group(1).strip().lower() == key:
                return m.group(2).strip()
    return ""


def skipped(path):
    return path.startswith(("memory/", ".claude/")) or os.path.basename(path) in LOCKFILES


def base_commit(root):
    for name in ("main", "master"):
        found = git(root, "merge-base", "HEAD", name)
        if found:
            return found
    return None


def changed_files(root):
    """Dateien, die der Task gegenueber main geaendert oder neu angelegt hat."""
    base = base_commit(root)
    if not base:
        return []
    names = (git(root, "diff", "--name-only", base) or "").splitlines()
    names += (git(root, "ls-files", "--others", "--exclude-standard") or "").splitlines()
    return sorted({n for n in names if n and not skipped(n)})


def file_hash(root, path):
    try:
        with open(os.path.join(root, path), "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None


def changed_lines(root):
    """Geaenderte Zeilen des Tasks gegenueber main, None wenn nicht bestimmbar."""
    base = base_commit(root)
    if not base:
        return None
    total = 0
    for line in (git(root, "diff", "--numstat", base) or "").splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit() and not skipped(parts[2]):
            total += int(parts[0]) + int(parts[1])
    for path in (git(root, "ls-files", "--others", "--exclude-standard") or "").splitlines():
        if path and not skipped(path):
            try:
                with open(os.path.join(root, path), "rb") as f:
                    total += sum(1 for _ in f)
            except OSError:
                pass
    return total


def write_record(root, task, gate, record):
    record = {"task": task, "gate": gate, **record,
              "branch": git(root, "symbolic-ref", "--short", "-q", "HEAD"),
              "commit": git(root, "rev-parse", "--short", "HEAD")}
    os.makedirs(os.path.join(root, RUNS), exist_ok=True)
    target = f"{RUNS}/{task}-{gate}.json"
    with open(os.path.join(root, target), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return target


def execute(root, command):
    start = now()
    try:
        r = subprocess.run(command, shell=True, cwd=root, capture_output=True, text=True,
                           errors="replace", timeout=TIMEOUT)
        code, output = r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        code, output = 124, out + f"\nAbgebrochen nach {TIMEOUT // 60} Minuten."
    tail = "\n".join(output.splitlines()[-TAIL:])
    return code, tail, {"befehl": command, "exit": code, "zeit": start.isoformat(timespec="seconds"),
                        "dauer_s": round((now() - start).total_seconds(), 1), "ausgabe_ende": tail}


def run_red(root, task, command):
    """Vor dem Bau: die neuen Tests muessen scheitern. Haelt fest, welche Dateien es da gab."""
    old = load_json(root, f"{RUNS}/{task}-rot.json")
    if old.get("exit") not in (None, 0):
        print(f"Factory: Der rote Lauf für {task} ist schon aufgezeichnet und bleibt bestehen.")
        return 0
    code, tail, record = execute(root, command)
    record["bestanden"] = code != 0
    record["dateien"] = {p: file_hash(root, p) for p in changed_files(root)}
    target = write_record(root, task, "rot", record)
    print(tail)
    if code == 0:
        print(f"\nFactory: Die Tests für {task} sind grün, obwohl noch nichts gebaut ist. Sie prüfen das Neue "
              f"also nicht. Schreib Tests, die jetzt scheitern. Aufgezeichnet in {target}")
        return 1
    print(f"\nFactory: Roter Lauf für {task} aufgezeichnet in {target}. Jetzt kann gebaut werden.")
    return 0


def run_size(root, task, gates):
    own = task_field(root, task, "max zeilen")
    limit = int(own) if own.isdigit() else gates.get("max_zeilen", MAX_LINES)
    limit = limit if isinstance(limit, int) and limit >= 0 else MAX_LINES
    lines = changed_lines(root)
    too_big = bool(limit) and lines is not None and lines > limit
    target = write_record(root, task, "groesse", {
        "exit": 1 if too_big else 0, "bestanden": not too_big, "zeilen": lines, "grenze": limit,
        "zeit": now().isoformat(timespec="seconds")})
    if too_big:
        print(f"Factory: {task} ändert {lines} Zeilen, erlaubt sind {limit}. Der Task ist zu gross, um ihn genau "
              f"zu prüfen. Melde das dem Orchestrator, er teilt ihn. Aufgezeichnet in {target}")
        return 1
    print(f"Factory: groesse für {task} bestanden ({lines if lines is not None else '?'} Zeilen), "
          f"aufgezeichnet in {target}")
    return 0


def run_gate(root, name, task, command, quiet):
    code, tail, record = execute(root, command)
    record["bestanden"] = code == 0
    record["ungespeicherte_aenderungen"] = bool(git(root, "status", "--porcelain", "--", ".", ":!memory"))
    if name == "test":
        before = load_json(root, f"{RUNS}/{task}-rot.json").get("dateien")
        if isinstance(before, dict):
            record["tests_seit_rot_geaendert"] = sorted(p for p, h in before.items() if file_hash(root, p) != h)
    target = write_record(root, task, name, record)
    if code == 0 and quiet:
        print(f"Factory: {name} für {task} bestanden, aufgezeichnet in {target}")
    else:
        print(tail)
        print(f"\nFactory: {name} für {task} {'bestanden' if code == 0 else 'NICHT bestanden'} "
              f"(Exit {code}), aufgezeichnet in {target}")
    if record.get("tests_seit_rot_geaendert"):
        print("Factory: Seit dem roten Lauf geändert: " + ", ".join(record["tests_seit_rot_geaendert"])
              + ". Der Reviewer prüft, ob dabei Tests abgeschwächt wurden.")
    return code


def main():
    if len(sys.argv) != 3 or not re.match(r"[a-z][a-z0-9-]*$", sys.argv[1]) or not re.match(r"T-\d+$", sys.argv[2]):
        print("Aufruf: python3 .claude/hooks/factory_run.py <rot|alle|pruefung> <T-Nr>, z. B. alle T-001",
              file=sys.stderr)
        return 64
    gate, task = sys.argv[1], sys.argv[2]
    root = os.environ.get("CLAUDE_PROJECT_DIR") or git(os.getcwd(), "rev-parse", "--show-toplevel") or os.getcwd()
    gates = load_json(root, GATES)
    if gate == "groesse":
        return run_size(root, task, gates)
    names = required(gates) if gate == "alle" else ["test" if gate == "rot" else gate]
    commands = {n: gates[n].strip() if isinstance(gates.get(n), str) else "" for n in names}
    empty = [n for n in names if not commands[n]]
    if empty:
        print(f"Kein Befehl für {', '.join(empty)} in {GATES}. Der Orchestrator trägt ihn auf main ein (Station 6).",
              file=sys.stderr)
        return 65
    if gate == "rot":
        return run_red(root, task, commands["test"])
    worst = 0
    for name in names:
        worst = run_gate(root, name, task, commands[name], quiet=gate == "alle") or worst
    if gate == "alle":
        worst = run_size(root, task, gates) or worst
    return worst


if __name__ == "__main__":
    sys.exit(main())
