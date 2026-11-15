---
name: betrieb
description: Sammelt nach dem Release Crash-Reports, Fehlerlogs und Nutzerfeedback und macht daraus neue Briefs oder Tasks. Nutze diesen Skill regelmässig nach jedem Release, damit die Factory dauerhaft arbeitet statt nur einmal durchzulaufen.
---

# 15 Betrieb

Erst mit dem Rückweg aus dem Betrieb ist die Factory wirklich A bis Z.

## Input
- Crash-Reports (z. B. Xcode Organizer, Sentry), Logs, App-Store-Bewertungen, direktes Feedback

## Ablauf
1. Meldungen sammeln und gleiche Probleme zusammenfassen.
2. Jede Gruppe einordnen: Bug, Verbesserung, neue Idee.
3. Dringlichkeit bestimmen: Wie viele Nutzer, wie schlimm?
4. Bugs → direkt als Task an den Planner. Neue Ideen → als Mini-Brief an Station 1.
5. Wiederkehrende Fehlerarten als Lesson in `memory/lessons.md`.

## Output → `handoffs/15-betrieb-<Datum>.md`
```
| Problem | Anzahl | Schwere | Art | Weiter an |
```

## Gate
- Jede Meldung ist einer Gruppe zugeordnet.
- Kritische Bugs sind innerhalb eines Tages als Task angelegt.
