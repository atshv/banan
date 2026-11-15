---
name: builder
description: Setzt genau einen Task aus der Taskliste um, im Gerüst aus dem Setup und nach Architektur und Design. Nutze diesen Skill für jeden Bau-Task und für jede Nachbesserung nach Ablehnung durch Tester oder Reviewer.
---

# 9 Builder

Ein Task aufs Mal. So bleibt jede Änderung klein genug, dass Tester und Reviewer sie wirklich prüfen können.

## Input
- Ein Task aus `handoffs/05-tasks.md`
- `handoffs/03-architektur.md`, `handoffs/04-design.md`, `memory/conventions.md`
- Bei Nachbesserung: Bericht von Tester oder Reviewer

## Ablauf
1. Eigenen Branch nach `shared/git-strategie.md` anlegen.
2. Nur Dateien im „Bereich“ des Tasks ändern. Ein Schalter blockiert alles andere. Reicht der Bereich nicht, stoppen und dem Orchestrator melden, er erweitert ihn auf `main`.
3. Web-UI: Komponenten über `npx shadcn@latest add @magicui/<name>` holen, per Props und className anpassen, nicht im Registry-Code.
4. Lokal starten, Lint laufen lassen, eigene Schnelltests machen.
5. Commit mit Task-Nummer, Übergabe an den Tester.
6. Bei Nachbesserung den Versuchszähler erhöhen. Beim 3. Fehlschlag stoppen und an den Auftraggeber melden.

## Output → `handoffs/tasks/T-<Nr>-build.md`
```
Task · Branch · Geänderte Dateien · Was gemacht · Bekannte Einschränkungen · Versuch <1-3>
```

## Gate
- Lint ohne Fehler, Projekt startet.
- Keine Änderungen ausserhalb des Tasks.

## Nutzt
`magic-ui`, `frontend-design`, `mcp-builder` (für API-Anbindungen)
