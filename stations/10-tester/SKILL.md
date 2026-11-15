---
name: tester
description: Schreibt Tests aus den Abnahmekriterien und führt sie wirklich aus. Nutze diesen Skill nach jedem Builder-Durchgang und idealerweise schon bevor gebaut wird. Da der Auftraggeber den Code nicht selbst liest, sind die Tests seine Augen.
---

# 10 Tester

Ein Task ist erst fertig, wenn ein Test es beweist. „Sieht gut aus“ zählt nicht.

## Input
- Task mit „fertig wenn“ aus `handoffs/05-tasks.md`
- Abnahmekriterien aus `handoffs/01-brief.md`
- Build-Bericht `handoffs/tasks/T-<Nr>-build.md`

## Ablauf
1. Aus „fertig wenn“ und Abnahmekriterien Testfälle ableiten, auch Randfälle und Fehlerfälle.
2. Tests schreiben (Unit, und für UI End-to-End mit Playwright).
3. Web-UI erst ansehen, dann klicken: Seite laden, auf `networkidle` warten, Screenshot, dann Selektoren wählen.
4. Screenshots mobil (390 px) und Desktop (1440 px) ablegen.
5. Alle Tests ausführen, nicht nur die neuen, und zwar mit `python3 .claude/hooks/factory_run.py test T-<Nr>`. Das Script zeichnet Befehl und Ergebnis in `memory/runs/` auf. Nur dieser aufgezeichnete Lauf zählt als Nachweis, ein „grün“ im Bericht allein nicht.
6. Grün → weiter an Reviewer. Rot → zurück an Builder mit genauer Fehlerbeschreibung.

## Output → `handoffs/tasks/T-<Nr>-test.md`
```
Ergebnis: grün | rot · Tests (neu, gesamt, fehlgeschlagen) · Fehlerbeschreibung · Screenshots
```

## Gate
- Aufgezeichneter Testlauf in `memory/runs/T-<Nr>-test.json` ist bestanden.
- Jedes „fertig wenn“ hat mindestens einen Test.

## Nutzt
`webapp-testing` (Playwright, `with_server.py`)
