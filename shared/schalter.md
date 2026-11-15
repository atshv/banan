# Schalter

Die meisten Regeln der Factory sind Anweisungen. Diese acht werden von einem Programm erzwungen, egal was die KI gerade denkt. Die Programme liegen in `.claude/hooks/` und laufen über Hooks von Claude Code. Sie schicken keinen Kontext mit und kosten darum keine Tokens, solange sie nichts blockieren.

| Schalter | Wann er prüft | Was er erzwingt |
|---|---|---|
| Schreibsperre `main` | vor jedem Schreiben und vor `git commit` | Kein Produktcode direkt auf `main`. Erlaubt bleiben `memory/`, `factory/`, `.claude/`, `CLAUDE.md`, `README.md`, `VERSION`, `CHANGELOG.md`. |
| Task-Bereich | vor jedem Schreiben auf `task/T-<Nr>-…` | Nur Dateien aus der Zeile `Bereich:` des Tasks in `memory/handoffs/05-tasks.md`. Erlaubt bleiben `memory/` und Lockfiles. |
| Aufgezeichnete Prüfungen | wenn der Tester prüft | Typprüfung, Lint, Tests und Build laufen über `python3 .claude/hooks/factory_run.py alle T-<Nr>`. Das Script führt die Befehle aus `memory/gates.json` aus und speichert Befehl, Ergebnis und Ausgabe in `memory/runs/`. Welche Prüfungen Pflicht sind, legt das Profil fest (Liste `pflicht`), Tests gehören immer dazu. |
| Tests zuerst | vor dem Bau | `factory_run.py rot T-<Nr>` zeichnet auf, dass die neuen Tests scheitern. Ohne diesen roten Lauf gilt ein Task nie als fertig. Ändert jemand danach die Tests, steht das im grünen Lauf, und der Reviewer prüft es. Ausnahme nur mit `Tests zuerst: nein` im Task. |
| Vertrag | vor jedem Schreiben auf einem Task-Branch | Dateien unter `vertrag` in `memory/gates.json` sind gesperrt, ausser der Task hat `Vertrag ändern: ja`. |
| Grösse | bei `factory_run.py alle` | Ändert ein Task mehr als 800 Zeilen (`max_zeilen`, pro Task `Max Zeilen:`), ist er nicht fertig und wird geteilt. Lockfiles und `memory/` zählen nicht. |
| Freigaben | vor der nächsten Station und vor `git tag` | Research braucht die Freigabe Brief, Design die Freigabe Architektur, der Plan die Freigabe Design, ein Versions-Tag die Freigabe Release. |
| Stop-Check | bevor die KI aufhört | Kein Aufhören, solange ein Task unterwegs ist. „Fertig“ gilt nur mit Build-Bericht, rotem Lauf vor dem Bau, allen Pflicht-Prüfungen und der Grösse aufgezeichnet und grün, und bestandenem Review und Security-Check. Heikle Tasks brauchen zusätzlich die zweite Review. |

## Freigaben
Du gibst frei, indem du eine Nachricht schreibst, die nur daraus besteht.

`Freigabe Brief` · `Freigabe Architektur` · `Freigabe Design` · `Freigabe Release`

Ein Programm zeichnet das in `memory/freigaben/` auf, zusammen mit dem genauen Stand des Dokuments. Ändert sich das Dokument danach, gilt die Freigabe nicht mehr. Ein „ja“ im Chat oder eine Freigabe mit Zusatz („…, aber ändere noch X“) zählt nicht. Die Freigabe Release gilt für genau die Version in `VERSION`.

## Geschützt
`.claude/hooks/`, `.claude/settings.json`, `memory/runs/` und `memory/freigaben/` kann die KI weder mit den Schreib-Werkzeugen noch per Shell-Befehl ändern. `memory/gates.json` und `05-tasks.md` lassen sich nur auf `main` ändern, also nicht vom Builder.

## Gut zu wissen
- Vor dem ersten Commit und auf anderen Branches (z. B. `setup/…`) greift keine Schreibsperre.
- Der Stop-Check meldet sich pro Antwort höchstens einmal, damit keine Endlosschleife entsteht.
- Die Schalter brauchen `python3`. Fehlt es, läuft die Factory ohne Schalter weiter.

## Grenzen
Die Schalter sind kein Tresor. Sie prüfen die Schreib-Werkzeuge, `git commit`, `git tag` und Shell-Befehle, die geschützte Ordner nennen, aber nicht jeden denkbaren Umweg. Ein Befehl wie `npx shadcn add` kann Dateien ausserhalb des Bereichs anlegen. Das fängt der Reviewer. Welche Befehle und Pflicht-Prüfungen in `gates.json` stehen, legt der Orchestrator fest. Der Befehl steht in jedem aufgezeichneten Lauf, damit man ihn prüfen kann.

## Tests
Im Factory-Ordner: `python3 -m unittest discover engine/claude-code/tests`
