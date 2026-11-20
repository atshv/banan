# Changelog

Alle Änderungen an der Software Factory. Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionen nach den Regeln in `shared/versionierung.md`.

Vor v1.0.0 ist alles Entwicklungsstand. v1.0.0 ist das erste echte Release.

## [Unreleased]

## [0.0.9] – 2026-11-20

### Hinzugefügt
- Bestehende Projekte. `./install.sh <Ordner> <KI> bestand` richtet banan für ein Projekt ein, das es schon gibt, mit eigener Anleitung (`engine/AGENTS-bestand.md`) und ohne Profile und Design-Regeln von banan.
- `factory-uebernehmen` liest das Repo und schreibt die Karte des Projekts (`memory/handoffs/00-bestand.md`), die Prüfungen und den Vertrag. Neue `Freigabe Bestand`.
- `factory-auftrag` nimmt einen Wunsch auf. Der Plan braucht danach nur die `Freigabe Brief`.
- Abschluss per Pull Request (`"abschluss": "pr"`). Mergen nach `main`, Tags und Veröffentlichen sind für die KI gesperrt. Brief und Tasks reisen als erster Commit auf dem Task-Branch mit.
- Prüfungen mit Bedingung (`wenn`) laufen nur, wenn der Task passende Dateien ändert.
- `zaehlt_nicht` nimmt erzeugte Dateien und Testdaten aus der Grössengrenze.
- `memory/skills.txt` wählt, welche Skills von banan ein bestehendes Projekt bekommt.
- 6 weitere Tests, zusammen 42

### Geändert
- Jeder Branch mit `T-<Nr>` nach einem `/` gilt als Task-Branch, also auch `feature/T-012-lasso`.
- Die Grösse eines Tasks misst sich am nächsten Abzweigpunkt, auch gegenüber `origin/main`.

## [0.0.8] – 2026-11-15

### Hinzugefügt
- banan läuft mit jeder KI, nicht mehr nur mit Claude Code. `./install.sh <Ordner> cursor,codex` wählt die KIs: `claude`, `cursor`, `gemini`, `codex`, `deepseek`, `andere`.
- Anleitung für den Orchestrator als `AGENTS.md`, das alle lesen. `CLAUDE.md` und `GEMINI.md` verweisen darauf.
- Skills für alle anderen KIs in `.agents/skills/`
- Hooks für Cursor (`.cursor/hooks.json`), Gemini CLI (`.gemini/settings.json`) und Codex (`.codex/hooks.json`). Der Schalter versteht deren Eingaben, bei Codex auch Patches mit mehreren Dateien.
- Git-Schalter. Jeder Commit läuft durch dieselben Schreibregeln, egal welche KI ihn macht. `--no-verify` ist gesperrt.
- Freigabe im eigenen Terminal mit `python3 .banan/freigabe.py brief`, für KIs ohne Hooks. Läuft nur in einem echten Terminal.
- `python3 .banan/factory_guard.py pruefe` als Stop-Check auf Anweisung
- Rollen der Sub-Agents als Dateien in `.banan/rollen/` für KIs ohne benannte Sub-Agents
- 6 weitere Tests, zusammen 36

### Geändert
- Schalter und Werkzeuge liegen im Projekt neu in `.banan/` statt `.claude/hooks/`. `install.sh` räumt den alten Ort auf.
- Ordner `engine/claude-code/` heisst `engine/`, mit `engine/adapter/` je KI
- README und Banner nennen alle KIs

## [0.0.7] – 2026-11-15

### Hinzugefügt
- Tests zuerst. Der Tester schreibt die Tests vor dem Bau, `factory_run.py rot T-<Nr>` zeichnet auf, dass sie scheitern. Ohne diesen roten Lauf gilt ein Task nicht als fertig. Werden Tests danach geändert, steht das im grünen Lauf, und der Reviewer prüft es.
- Vertrag. Dateien mit Schnittstellen und Datentypen (`vertrag` in `memory/gates.json`) sind für Builder gesperrt, ausser der Task hat `Vertrag ändern: ja`.
- Grössengrenze. Ändert ein Task mehr als 800 Zeilen, ist er nicht fertig und wird geteilt.
- Zweite Review für Tasks mit `Heikel: ja`, mit dem Auftrag, den Code zu brechen
- 5 weitere Tests, zusammen 30

### Geändert
- Task-Schleife: Tester (rot) → Builder → Tester (alle Prüfungen) → Reviewer → Security
- Architektur legt den Vertrag fest, Setup legt die Dateien an

## [0.0.6] – 2026-11-15

### Hinzugefügt
- Profile pro Projekttyp in `profiles/`: `web-app`, `iphone-app`, `engine`, `backend`. Jedes legt Stack-Vorschlag, Pflicht-Prüfungen, Testmethode, passende Skills und eine Release-Liste fest. Der Brief wählt das Profil.
- Mehr aufgezeichnete Prüfungen. `memory/gates.json` hat eine Liste `pflicht`, z. B. Typprüfung, Lint, Tests und Build. „Fertig“ braucht alle davon grün.
- `factory_run.py alle T-<Nr>` startet alle Pflicht-Prüfungen in einem Aufruf
- 20 Skills von Emil Kowalski für Oberflächen, Animation und Swift in `vendor-skills/emilkowalski/` (MIT), in den Profilen den Stationen zugeordnet
- Design-Station verlangt für jeden Screen die Zustände leer, lädt, Fehler und gefüllt

### Geändert
- Brief hat neu die Zeile `Profil:` statt „Plattform“

## [0.0.5] – 2026-11-15

### Geändert
- README neu gestaltet, mit Banner, Abzeichen und einer Grafik der Linie (`docs/images/`)

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

[Unreleased]: https://github.com/atshv/banan/compare/v0.0.9...HEAD
[0.0.9]: https://github.com/atshv/banan/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/atshv/banan/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/atshv/banan/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/atshv/banan/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/atshv/banan/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/atshv/banan/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/atshv/banan/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/atshv/banan/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/atshv/banan/releases/tag/v0.0.1
