#!/usr/bin/env python3
"""Fügt Sperren und Schalter von banan in eine bestehende Einstellungsdatei einer KI ein.

Aufruf: merge_settings.py <Datei von banan> <Datei im Projekt>
Passt für .claude/settings.json, .gemini/settings.json, .codex/hooks.json und .cursor/hooks.json.
Eigene Einträge im Projekt bleiben erhalten. Alte banan-Schalter werden ersetzt.
"""
import json
import sys

MARK = "factory_guard.py"


def main(source, target):
    with open(source, encoding="utf-8") as f:
        ours = json.load(f)
    with open(target, encoding="utf-8") as f:
        theirs = json.load(f)

    for rule in ours.get("permissions", {}).get("deny", []):
        deny = theirs.setdefault("permissions", {}).setdefault("deny", [])
        if rule not in deny:
            deny.append(rule)

    names = ours.get("context", {}).get("fileName", [])
    if names:
        current = theirs.setdefault("context", {}).setdefault("fileName", [])
        if isinstance(current, str):
            current = theirs["context"]["fileName"] = [current]
        current.extend(n for n in names if n not in current)

    if "version" in ours:
        theirs.setdefault("version", ours["version"])

    hooks = theirs.setdefault("hooks", {})
    for event, groups in ours.get("hooks", {}).items():
        kept = [g for g in hooks.get(event, []) if MARK not in json.dumps(g)]
        hooks[event] = kept + groups

    with open(target, "w", encoding="utf-8") as f:
        json.dump(theirs, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
