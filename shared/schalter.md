# Schalter

Die meisten Regeln der Factory sind Anweisungen. Diese acht werden von einem Programm erzwungen, egal was die KI gerade denkt. Die Programme liegen in `.banan/`. Sie laufen über die Hooks deiner KI und zusätzlich bei jedem Commit über Git. Sie schicken keinen Kontext mit und kosten darum keine Tokens, solange sie nichts blockieren.

| Schalter | Wann er prüft | Was er erzwingt |
|---|---|---|
| Schreibsperre `main` | vor jedem Schreiben und vor `git commit` | Kein Produktcode direkt auf `main`. Erlaubt bleiben `memory/`, `factory/`, `.claude/`, `CLAUDE.md`, `README.md`, `VERSION`, `CHANGELOG.md`. |
| Task-Bereich | vor jedem Schreiben auf `task/T-<Nr>-…` | Nur Dateien aus der Zeile `Bereich:` des Tasks in `memory/handoffs/05-tasks.md`. Erlaubt bleiben `memory/` und Lockfiles. |
| Aufgezeichnete Prüfungen | wenn der Tester prüft | Typprüfung, Lint, Tests und Build laufen über `python3 .banan/factory_run.py alle T-<Nr>`. Das Script führt die Befehle aus `memory/gates.json` aus und speichert Befehl, Ergebnis und Ausgabe in `memory/runs/`. Welche Prüfungen Pflicht sind, legt das Profil fest (Liste `pflicht`), Tests gehören immer dazu. |
| Tests zuerst | vor dem Bau | `factory_run.py rot T-<Nr>` zeichnet auf, dass die neuen Tests scheitern. Ohne diesen roten Lauf gilt ein Task nie als fertig. Ändert jemand danach die Tests, steht das im grünen Lauf, und der Reviewer prüft es. Ausnahme nur mit `Tests zuerst: nein` im Task. |
| Vertrag | vor jedem Schreiben auf einem Task-Branch | Dateien unter `vertrag` in `memory/gates.json` sind gesperrt, ausser der Task hat `Vertrag ändern: ja`. |
| Grösse | bei `factory_run.py alle` | Ändert ein Task mehr als 800 Zeilen (`max_zeilen`, pro Task `Max Zeilen:`), ist er nicht fertig und wird geteilt. Lockfiles und `memory/` zählen nicht. |
| Freigaben | vor der nächsten Station und vor `git tag` | Research braucht die Freigabe Brief, Design die Freigabe Architektur, der Plan die Freigabe Design, ein Versions-Tag die Freigabe Release. |
| Stop-Check | bevor die KI aufhört | Kein Aufhören, solange ein Task unterwegs ist. „Fertig“ gilt nur mit Build-Bericht, rotem Lauf vor dem Bau, allen Pflicht-Prüfungen und der Grösse aufgezeichnet und grün, und bestandenem Review und Security-Check. Heikle Tasks brauchen zusätzlich die zweite Review. |

## Freigaben
Du gibst frei, indem du eine Nachricht schreibst, die nur daraus besteht.

`Freigabe Brief` · `Freigabe Architektur` · `Freigabe Design` · `Freigabe Release` · in einem bestehenden Projekt auch `Freigabe Bestand`

Ein Programm zeichnet das in `memory/freigaben/` auf, zusammen mit dem genauen Stand des Dokuments. Ändert sich das Dokument danach, gilt die Freigabe nicht mehr. Ein „ja“ im Chat oder eine Freigabe mit Zusatz („…, aber ändere noch X“) zählt nicht. Die Freigabe Release gilt für genau die Version in `VERSION`.

## Bestehendes Projekt
Zwei Angaben in `memory/gates.json` stellen die Schalter auf ein Projekt ein, das es schon gibt. `./install.sh <Ordner> <KI> bestand` setzt die erste, `factory-uebernehmen` trägt den Rest ein.

| Angabe | Was sich ändert |
|---|---|
| `"modus": "bestand"` | Der erste Auftrag braucht die `Freigabe Bestand` für die Karte des Projekts (`memory/handoffs/00-bestand.md`). Der Plan braucht nur die `Freigabe Brief`, weil es Architektur und Design schon gibt. |
| `"abschluss": "pr"` | Die KI öffnet Pull Requests. Mergen nach `main`, Tags und Veröffentlichen sind für sie gesperrt, auch mit Freigabe. Brief und Tasks schreibt der Orchestrator als ersten Commit auf den Task-Branch, danach ist die Taskliste dort gesperrt. |
| `"wenn": {"native": ["src/core/", "*.cpp"]}` | Die Prüfung `native` läuft nur, wenn der Task solche Dateien ändert. Sonst wird sie als „nicht nötig“ aufgezeichnet. |
| `"zaehlt_nicht": ["fixtures/", "*.snap"]` | Diese Dateien zählen nicht zur Grösse eines Tasks, z. B. erzeugte Dateien und Referenzbilder. |

Ein Task-Branch ist jeder Branch, dessen Name nach einem `/` mit `T-<Nr>` weitergeht, also auch `feature/T-012-lasso`.

## Geschützt
`.banan/`, die Hook-Dateien der KIs (`.claude/settings.json`, `.cursor/hooks.json`, `.gemini/settings.json`, `.codex/hooks.json`), `memory/runs/` und `memory/freigaben/` kann die KI weder mit den Schreib-Werkzeugen noch per Shell-Befehl ändern. `memory/gates.json` und `05-tasks.md` lassen sich nur auf `main` ändern, also nicht vom Builder.

## Gut zu wissen
- Vor dem ersten Commit und auf anderen Branches (z. B. `setup/…`) greift keine Schreibsperre.
- Der Stop-Check meldet sich pro Antwort höchstens einmal, damit keine Endlosschleife entsteht.
- Die Schalter brauchen `python3`. Fehlt es, läuft die Factory ohne Schalter weiter.

## Welche KI kann was
Die Schalter haben zwei Ebenen.

**Git, für jede KI.** Bei jedem Commit prüft ein Git-Hook dieselben Schreibregeln: kein Produktcode auf `main`, nur der Bereich des Tasks, Vertrag gesperrt. Das gilt auch für KIs ohne eigene Hooks und für Menschen.

**Hooks der KI.** Claude Code, Cursor, Gemini CLI und Codex melden jeden Schreibversuch, jeden Shell-Befehl, jede Nachricht und das Ende einer Antwort. Dort greifen die Schalter schon vor dem Schreiben.

| | Claude Code | Cursor | Gemini CLI | Codex | DeepSeek Harness, andere |
|---|---|---|---|---|---|
| Datei für die Hooks | `.claude/settings.json` | `.cursor/hooks.json` | `.gemini/settings.json` | `.codex/hooks.json` | keine |
| Schreibregeln | vor dem Schreiben | vor dem Schreiben | vor dem Schreiben | vor dem Schreiben | beim Commit |
| Freigabe | Nachricht `Freigabe Brief` | Nachricht | Nachricht | Nachricht | `python3 .banan/freigabe.py brief` im eigenen Terminal |
| Stop-Check | blockiert | schickt die KI zurück an die Arbeit | blockiert | schickt die KI zurück an die Arbeit | KI ruft `python3 .banan/factory_guard.py pruefe` auf |
| Sub-Agents | benannt, mit eigenen Rechten | über Rollendatei | über Rollendatei | über Rollendatei | über Rollendatei |

Die Freigabe im Terminal geht bei jeder KI. Das Script läuft nur in einem echten Terminal und fragt nach, eine KI kann es nicht selbst auslösen.

Bei Codex musst du die Schalter einmal mit `/hooks` bestätigen, sonst laufen sie nicht.

**Stand der Erprobung.** Die Schalter selbst sind mit 42 automatischen Tests geprüft, auch mit den Eingaben im Format von Cursor, Gemini und Codex. In den KIs selbst ist noch keine Anbindung gelaufen. Die Formate folgen der Doku von Codex und Gemini. Bei Cursor sind die Feldnamen der Eingabe nicht bestätigt.

## Grenzen
Die Schalter sind kein Tresor. Sie prüfen die Schreib-Werkzeuge, `git commit`, `git tag` und Shell-Befehle, die geschützte Ordner nennen, aber nicht jeden denkbaren Umweg. Ein Befehl wie `npx shadcn add` kann Dateien ausserhalb des Bereichs anlegen. Das fängt der Reviewer. Welche Befehle und Pflicht-Prüfungen in `gates.json` stehen, legt der Orchestrator fest. Der Befehl steht in jedem aufgezeichneten Lauf, damit man ihn prüfen kann.

## Tests
Im Ordner von banan: `python3 -m unittest discover engine/tests`
