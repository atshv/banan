#!/usr/bin/env python3
"""Fuehrt Pruefungen aus und zeichnet das Ergebnis auf.

Aufruf im Projektordner:
  python3 .claude/hooks/factory_run.py <pruefung> <T-Nr>   z. B. test T-001
  python3 .claude/hooks/factory_run.py alle <T-Nr>         alle Pflicht-Pruefungen der Reihe nach

Die Befehle stehen in memory/gates.json, z. B.
  {"pflicht": ["typecheck", "lint", "test", "build"], "test": "npm test", ...}
Jedes Ergebnis landet in memory/runs/T-<Nr>-<pruefung>.json. Nur dieses Script schreibt dort.
Der Stop-Check glaubt fuer 'fertig' nur aufgezeichneten Laeufen mit Exit 0.
"""
import datetime
import json
import os
import re
import subprocess
import sys

GATES = "memory/gates.json"
RUNS = "memory/runs"
TIMEOUT = 30 * 60
TAIL = 40


def git(root, *args):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def load_gates(root):
    try:
        with open(os.path.join(root, GATES), encoding="utf-8") as f:
            gates = json.load(f)
    except (OSError, ValueError):
        return {}
    return gates if isinstance(gates, dict) else {}


def required(gates):
    listed = gates.get("pflicht")
    names = [g for g in listed if isinstance(g, str) and g] if isinstance(listed, list) else []
    return names if "test" in names else names + ["test"]


def run_gate(root, gate, task, command):
    """Fuehrt eine Pruefung aus, zeichnet sie auf, gibt (Exit-Code, Ende der Ausgabe, Datei) zurueck."""
    start = datetime.datetime.now().astimezone()
    try:
        r = subprocess.run(command, shell=True, cwd=root, capture_output=True, text=True,
                           errors="replace", timeout=TIMEOUT)
        code, output = r.returncode, (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        code, output = 124, out + f"\nAbgebrochen nach {TIMEOUT // 60} Minuten."
    tail = "\n".join(output.splitlines()[-TAIL:])
    record = {
        "task": task,
        "gate": gate,
        "befehl": command,
        "exit": code,
        "bestanden": code == 0,
        "zeit": start.isoformat(timespec="seconds"),
        "dauer_s": round((datetime.datetime.now().astimezone() - start).total_seconds(), 1),
        "branch": git(root, "symbolic-ref", "--short", "-q", "HEAD"),
        "commit": git(root, "rev-parse", "--short", "HEAD"),
        "ungespeicherte_aenderungen": bool(git(root, "status", "--porcelain", "--", ".", ":!memory")),
        "ausgabe_ende": tail,
    }
    os.makedirs(os.path.join(root, RUNS), exist_ok=True)
    target = f"{RUNS}/{task}-{gate}.json"
    with open(os.path.join(root, target), "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return code, tail, target


def main():
    if len(sys.argv) != 3 or not re.match(r"[a-z][a-z0-9-]*$", sys.argv[1]) or not re.match(r"T-\d+$", sys.argv[2]):
        print("Aufruf: python3 .claude/hooks/factory_run.py <pruefung|alle> <T-Nr>, z. B. alle T-001", file=sys.stderr)
        return 64
    gate, task = sys.argv[1], sys.argv[2]
    root = os.environ.get("CLAUDE_PROJECT_DIR") or git(os.getcwd(), "rev-parse", "--show-toplevel") or os.getcwd()
    gates = load_gates(root)
    names = required(gates) if gate == "alle" else [gate]
    commands = {n: (gates.get(n) or "").strip() if isinstance(gates.get(n), str) else "" for n in names}
    empty = [n for n in names if not commands[n]]
    if empty:
        print(f"Kein Befehl für {', '.join(empty)} in {GATES}. Der Orchestrator trägt ihn auf main ein (Station 6).",
              file=sys.stderr)
        return 65

    worst = 0
    for name in names:
        code, tail, target = run_gate(root, name, task, commands[name])
        if code == 0 and gate == "alle":
            print(f"Factory: {name} für {task} bestanden, aufgezeichnet in {target}")
            continue
        print(tail)
        print(f"\nFactory: {name} für {task} {'bestanden' if code == 0 else 'NICHT bestanden'} "
              f"(Exit {code}), aufgezeichnet in {target}")
        worst = worst or code
    return worst


if __name__ == "__main__":
    sys.exit(main())
