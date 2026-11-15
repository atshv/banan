---
name: planner
description: Zerlegt Architektur und Design in kleine Tasks mit Abhängigkeiten und je einem klaren „fertig wenn“. Nutze diesen Skill, bevor gebaut wird, und immer, wenn ein Task zu gross ist oder neue Anforderungen dazukommen.
---

# 5 Planner

Kleine Tasks scheitern selten und lassen sich gut prüfen. Grosse Tasks verstecken Fehler.

## Input
- `handoffs/03-architektur.md`, `handoffs/04-design.md`

## Ablauf
1. Pro Modul die Tasks ableiten. Ein Task = ein Builder-Durchgang, ideal unter 200 Zeilen Code.
2. Abhängigkeiten festlegen (welcher Task braucht welchen).
3. Jedem Task ein „fertig wenn“ geben, das der Tester prüfen kann.
4. Jedem Task einen Bereich geben, also die Ordner und Dateien, in denen der Builder schreiben darf, inklusive Testordner. Ein Schalter erzwingt ihn (`shared/schalter.md`), darum lieber eng und genau.
5. Reihenfolge so wählen, dass früh etwas Lauffähiges entsteht.
6. Alle Tasks in `memory/status.md` als „offen“ eintragen.

## Output → `handoffs/05-tasks.md`
Genau dieses Format, ein Feld pro Zeile. Der Schalter liest die Überschrift und die Zeile `Bereich:`.
```
## T-<Nr>: <Titel>
- Modul: <Name>
- Braucht: T-<Nr>
- Bereich: src/login/, tests/login/, app/page.tsx
- Fertig wenn: <prüfbar>
- Abnahmekriterium aus Brief: <Nr>
```
Im Bereich meint ein Eintrag mit `/` am Ende einen ganzen Ordner, sonst eine Datei. `*` ist erlaubt.

## Gate
- Jedes Abnahmekriterium aus dem Brief ist mindestens einem Task zugeordnet.
- Kein Task ohne „fertig wenn“.
- Kein Task ohne „Bereich“.
