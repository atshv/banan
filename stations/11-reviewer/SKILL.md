---
name: reviewer
description: Prüft jeden fertigen Task unabhängig gegen Brief, Architektur, Design und Konventionen. Nutze diesen Skill nach grünem Test. Der Reviewer läuft als frischer Agent ohne Wissen über den Bauweg, damit die Arbeit sich nicht selbst bewertet.
---

# 11 Reviewer

Wer etwas gebaut hat, sieht die eigenen Fehler schlecht. Darum prüft hier jemand, der den Bau nicht gesehen hat.

## Input
- Diff des Task-Branches
- `handoffs/01-brief.md`, `handoffs/03-architektur.md`, `handoffs/04-design.md`
- `memory/conventions.md`, `memory/decisions.md`, `design/design-regeln.md`
- Bewusst nicht: Build-Bericht und Chatverlauf des Builders

## Ablauf
1. Ziel des Tasks nur aus dem Task-Text verstehen.
2. Prüfen: Erfüllt der Code das „fertig wenn“? Hält er Architektur, Design-Regeln und Konventionen ein?
3. `memory/runs/T-<Nr>-test.json` lesen. Steht dort `tests_seit_rot_geaendert`, diese Dateien genau ansehen. Wurde ein Test abgeschwächt, damit er besteht, ist das blockierend.
4. Lesbarkeit und unnötige Komplexität prüfen.
5. Jedem Befund eine Schwere geben: blockierend, sollte, kann.
6. Wiederkehrende Fehler als Lesson in `memory/lessons.md` eintragen.

## Output → `handoffs/tasks/T-<Nr>-review.md`
```
Ergebnis: OK | abgelehnt · Befunde (Schwere, Datei, Was, Warum) · Lessons
```

## Zweite Review
Bei Tasks mit `Heikel: ja` prüft ein zweiter, frischer Reviewer mit anderem Auftrag: Er sucht aktiv nach Wegen, den Code zu brechen (falsche Eingaben, fehlende Rechte, doppelte Aufrufe, Abbruch mittendrin). Ergebnis in `handoffs/tasks/T-<Nr>-review2.md`, gleiches Format.

## Gate
- Keine blockierenden Befunde.

## Nutzt
`doc-coauthoring` (Reader Testing: frischer Sub-Agent ohne Vorwissen), Grader aus `skill-creator`
