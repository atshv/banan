#!/usr/bin/env python3
"""Freigabe des Auftraggebers im eigenen Terminal, für jede KI.

Aufruf im Projektordner:  python3 .banan/freigabe.py <brief|architektur|design|release>

Das Script läuft nur in einem echten Terminal und fragt nach. Eine KI, die es über ihre
Shell startet, hat kein Terminal und wird abgewiesen.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factory_guard as guard  # noqa: E402

NAMES = ("brief", "architektur", "design", "release")


def main():
    name = sys.argv[1].lower() if len(sys.argv) == 2 else ""
    if name not in NAMES:
        print("Aufruf: python3 .banan/freigabe.py <brief|architektur|design|release>", file=sys.stderr)
        return 64
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        print("Factory-Schalter: Freigaben gibt nur der Auftraggeber, in seinem eigenen Terminal. "
              "Bitte ihn darum und hör auf.", file=sys.stderr)
        return 2
    root = guard.project_root(os.getcwd())
    if name == "release":
        what = f"Version {guard.version(root) or '?'}"
    else:
        what = guard.CHECKPOINTS[name]
    answer = input(f"Freigabe '{name.capitalize()}' für {what} geben? Tippe ja: ").strip().lower()
    if answer != "ja":
        print("Nichts freigegeben.")
        return 1
    print(guard.record_approval(root, f"Freigabe {name}"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
