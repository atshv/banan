#!/usr/bin/env python3
"""Fuehrt ein Gate aus und zeichnet das Ergebnis auf.

Aufruf im Projektordner:  python3 .claude/hooks/factory_run.py <gate> <T-Nr>
Beispiel:                 python3 .claude/hooks/factory_run.py test T-001

Der Befehl kommt aus memory/gates.json, z. B. {"test": "npm test", "lint": "npm run lint"}.
Das Ergebnis landet in memory/runs/T-<Nr>-<gate>.json. Nur dieses Script schreibt dort.
Der Stop-Check glaubt fuer 'fertig' nur einem aufgezeichneten Testlauf mit Exit 0.
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


def main():
    if len(sys.argv) != 3 or not re.match(r"[a-z][a-z0-9-]*$", sys.argv[1]) or not re.match(r"T-\d+$", sys.argv[2]):
        print("Aufruf: python3 .claude/hooks/factory_run.py <gate> <T-Nr>, z. B. test T-001", file=sys.stderr)
        return 64
    gate, task = sys.argv[1], sys.argv[2]
    root = os.environ.get("CLAUDE_PROJECT_DIR") or git(os.getcwd(), "rev-parse", "--show-toplevel") or os.getcwd()
    try:
        with open(os.path.join(root, GATES), encoding="utf-8") as f:
            command = (json.load(f).get(gate) or "").strip()
    except (OSError, ValueError, AttributeError):
        command = ""
    if not command:
        print(f"Kein Befehl für '{gate}' in {GATES}. Der Orchestrator trägt ihn auf main ein (Station 6).",
              file=sys.stderr)
        return 65

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

    print(tail)
    print(f"\nFactory: {gate} für {task} {'bestanden' if code == 0 else 'NICHT bestanden'} "
          f"(Exit {code}), aufgezeichnet in {target}")
    return code


if __name__ == "__main__":
    sys.exit(main())
