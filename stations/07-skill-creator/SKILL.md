---
name: skill-creator-factory
description: Baut und verbessert projektspezifische Skills für Konventionen, Stack-Eigenheiten und wiederkehrende Abläufe. Nutze diesen Skill nach dem Setup, wenn Builder für dieses Projekt Spezialwissen brauchen, und jedes Mal, wenn lessons.md neue Einträge hat, die in Regeln übergehen sollen.
---

# 7 Skill-Creator

Skills sind das Gedächtnis der Factory für das Wie. Jede Lektion, die nicht in einem Skill landet, wird wiederholt.

## Input
- `handoffs/03-architektur.md`, `memory/conventions.md`, `memory/lessons.md`
- Vorbild und Werkzeug: `vendor-skills/anthropic/skill-creator`

## Ablauf
1. Absicht klären: Was soll der Skill können, wann soll er greifen, was kommt heraus?
2. Entwurf schreiben nach den Mustern im README (Description als Auslöser, unter 500 Zeilen, Details in `references/`, Scripts in `scripts/`).
3. 3 Test-Prompts anlegen und je einmal mit und ohne Skill laufen lassen.
4. Ergebnisse vergleichen. Nur behalten, was messbar besser ist.
5. Wiederholt geschriebene Hilfscode-Stücke als Script bündeln.
6. Bei Lessons: Regel mit Begründung einbauen, Eintrag in `lessons.md` als „übernommen“ markieren.

## Output
- `skills/<name>/SKILL.md` im Projekt-Repo
- Eintrag in `handoffs/07-skills.md` mit Name, Zweck und Eval-Ergebnis

## Gate
- Skill schlägt den Lauf ohne Skill in mindestens 2 von 3 Tests.
- Description nennt konkrete Auslöser.

## Nutzt
`skill-creator`
