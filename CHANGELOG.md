# Changelog

Alle Änderungen an der Software Factory. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach den Regeln in `shared/versionierung.md`.

Vor v1.0.0 ist alles Entwicklungsstand. v1.0.0 ist das erste echte Release.

## [Unreleased]

## [0.0.4] – 2026-11-15

### Hinzugefügt
- Aufgezeichnete Testläufe. `factory_run.py` führt den Testbefehl aus `memory/gates.json` aus und speichert Befehl, Ergebnis und Ausgabe in `memory/runs/`. „Fertig“ gilt nur noch mit einem solchen grünen Lauf, nicht mehr mit einem „grün“ im Bericht.
- Freigaben, die sich die KI nicht selbst geben kann. Eine Nachricht wie `Freigabe Brief` wird von einem Programm aufgezeichnet, zusammen mit dem Stand des Dokuments. Ohne gültige Freigabe blockiert ein Schalter Research, Design, Plan und den Versions-Tag.
- Schutz für `memory/runs/` und `memory/freigaben/`, auch gegen Shell-Befehle
- 9 weitere Tests, zusammen 23

### Geändert
- README neu, kurz und unter dem Namen banan
- Link auf das private Whiteboard aus dem README entfernt

## [0.0.3] – 2026-11-15

### Hinzugefügt
- Drei Schalter, die Regeln per Programm erzwingen (`engine/claude-code/.claude/hooks/factory_guard.py`, erklärt in `shared/schalter.md`)
  - Schreibsperre auf `main` für Produktcode, auch bei `git commit`
  - Task-Bereich, auf einem Task-Branch darf nur im „Bereich“ des Tasks geschrieben werden
  - Stop-Check, kein Aufhören mit laufenden Tasks oder „fertig“ ohne bestandene Berichte
- Schutz der Schalter selbst, die KI kann `.claude/hooks/` und `.claude/settings.json` nicht ändern
- 14 automatische Tests für die Schalter in `engine/claude-code/tests/`

### Geändert
- Planner schreibt Tasks mit einem Feld pro Zeile und einer Pflichtzeile `Bereich:`
- Projekt-Setup baut das Gerüst auf dem Branch `setup/grundgeruest`, wenn `main` schon einen Commit hat
- `install.sh` kopiert die Schalter und fügt sie in eine bestehende `settings.json` ein, statt diese auszulassen

## [0.0.2] – 2026-11-15

### Hinzugefügt
- Motor für den Orchestrator mit Claude Code in `engine/claude-code/`
  - `CLAUDE.md` mit Ablauf, Task-Schleife, 3-Versuche-Regel und Checkpoints
  - Sub-Agents `factory-researcher`, `factory-builder`, `factory-tester`, `factory-reviewer` und `factory-security`. Reviewer und Security dürfen nur lesen.
  - Befehle `/factory-start`, `/factory-weiter`, `/factory-status` und `/factory-release`
  - Sperren in `settings.json` gegen Force-Push, `git reset --hard`, `rm -rf` und das Lesen von `.env`
- `install.sh` installiert oder aktualisiert die Factory in einem Projektordner, ohne Projekt-Gedächtnis oder eigene Einstellungen zu überschreiben
- Befehl `/factory-neu <Ordner>` im Factory-Repo als Abkürzung für `install.sh`

### Geändert
- README erklärt den Start eines Projekts mit dem neuen Motor

## [0.0.1] – 2026-11-15

### Hinzugefügt
- 15 Stationen von Brief-Creator bis Betrieb, je als SKILL.md mit Input, Ablauf, Übergabeformat und Gate
- Übergreifende Regeln in `shared/` für Orchestrator, Übergabeformat, Quality Gates, Checkpoints, Limits, Git-Strategie, Statusbericht und Kennzahlen
- Vorlagen fürs Projekt-Gedächtnis in `memory/`
- Design-Regeln und Komponentenwahl nach Magic UI in `design/`
- Übernommene Skills von Anthropic und Magic UI mit Lizenzen in `vendor-skills/`
- Versionierung ab 0.0.1 mit `VERSION`, `CHANGELOG.md` und `shared/versionierung.md`

### Behoben
- Ordner- und Dateinamen in `vendor-skills/anthropic/` hatten nach dem Upload Zeitstempel im Namen (z. B. `skill-creator 19.24.30`). Sie heissen wieder wie im Original, sonst finden Agents die Skills nicht.

[Unreleased]: https://github.com/atshv/banan/compare/v0.0.4...HEAD
[0.0.4]: https://github.com/atshv/banan/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/atshv/banan/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/atshv/banan/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/atshv/banan/releases/tag/v0.0.1
