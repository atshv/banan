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
4. Reihenfolge so wählen, dass früh etwas Lauffähiges entsteht.
5. Alle Tasks in `memory/status.md` als „offen“ eintragen.

## Output → `handoffs/05-tasks.md`
```
## T-<Nr>: <Titel>
Modul · Braucht: T-<Nr> · Fertig wenn: <prüfbar> · Abnahmekriterium aus Brief: <Nr>
```

## Gate
- Jedes Abnahmekriterium aus dem Brief ist mindestens einem Task zugeordnet.
- Kein Task ohne „fertig wenn“.
