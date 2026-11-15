# Changelog

Alle Änderungen an der Software Factory. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach den Regeln in `shared/versionierung.md`.

Vor v1.0.0 ist alles Entwicklungsstand. v1.0.0 ist das erste echte Release.

## [Unreleased]

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

[Unreleased]: https://github.com/atshv/banan/compare/v0.0.2...HEAD
[0.0.2]: https://github.com/atshv/banan/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/atshv/banan/releases/tag/v0.0.1
