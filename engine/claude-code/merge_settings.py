#!/usr/bin/env python3
"""Fügt Sperren und Schalter der Factory in eine bestehende .claude/settings.json ein.

Aufruf: merge_settings.py <settings der Factory> <settings im Projekt>
Eigene Einträge im Projekt bleiben erhalten. Alte Factory-Schalter werden ersetzt.
"""
import json
import sys

MARK = "factory_guard.py"


def is_ours(group):
    return any(MARK in str(h.get("command", "")) for h in group.get("hooks", []))


def main(source, target):
    with open(source, encoding="utf-8") as f:
        ours = json.load(f)
    with open(target, encoding="utf-8") as f:
        theirs = json.load(f)

    deny = theirs.setdefault("permissions", {}).setdefault("deny", [])
    for rule in ours.get("permissions", {}).get("deny", []):
        if rule not in deny:
            deny.append(rule)

    hooks = theirs.setdefault("hooks", {})
    for event, groups in ours.get("hooks", {}).items():
        kept = [g for g in hooks.get(event, []) if not is_ours(g)]
        hooks[event] = kept + groups

    with open(target, "w", encoding="utf-8") as f:
        json.dump(theirs, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
