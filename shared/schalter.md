# Schalter

Die meisten Regeln der Factory sind Anweisungen. Diese drei werden von einem Programm erzwungen, egal was die KI gerade denkt. Das Programm ist `.claude/hooks/factory_guard.py` und läuft über Hooks von Claude Code. Es schickt keinen Kontext mit und kostet darum keine Tokens, solange es nichts blockiert.

| Schalter | Wann er prüft | Was er blockiert |
|---|---|---|
| Schreibsperre `main` | vor jedem Schreiben und vor `git commit` | Produktcode direkt auf `main`. Erlaubt bleiben `memory/`, `factory/`, `.claude/`, `CLAUDE.md`, `README.md`, `VERSION`, `CHANGELOG.md`. |
| Task-Bereich | vor jedem Schreiben auf einem Branch `task/T-<Nr>-…` | Dateien ausserhalb der Zeile `Bereich:` des Tasks in `memory/handoffs/05-tasks.md`. Erlaubt bleiben `memory/` und Lockfiles. |
| Stop-Check | bevor die KI aufhört | Aufhören, solange ein Task auf „in Arbeit“, „Test“, „Review“ oder „Security“ steht, oder auf „fertig“ ohne bestandene Berichte von Build, Test, Review und Security. |

Dazu sind die Schalter selbst geschützt. `.claude/hooks/` und `.claude/settings.json` kann die KI nicht ändern.

## Gut zu wissen
- Vor dem ersten Commit und auf anderen Branches (z. B. `setup/…`) greift keine Schreibsperre.
- `memory/handoffs/05-tasks.md` wird nur auf `main` geändert. So kann ein Builder seinen Bereich nicht selbst erweitern.
- Der Stop-Check meldet sich pro Antwort höchstens einmal. Danach darf die KI aufhören, damit keine Endlosschleife entsteht.
- Die Schalter brauchen `python3`. Fehlt es, läuft die Factory ohne Schalter weiter.

## Grenzen
Die Schalter sind kein Tresor. Sie prüfen die Schreib-Werkzeuge und `git commit`, aber nicht jeden Shell-Befehl. Ein Befehl wie `npx shadcn add` kann Dateien ausserhalb des Bereichs anlegen. Das fängt der Reviewer mit dem Gate „Keine Änderungen ausserhalb des Tasks“.

## Tests
Im Factory-Ordner: `python3 -m unittest discover engine/claude-code/tests`
