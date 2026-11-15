---
name: factory-start
description: Startet ein neues Projekt in der Software Factory mit Station 1 (Brief). Nur auf Befehl des Auftraggebers.
disable-model-invocation: true
---

# Neues Projekt starten

1. Prüfe, ob `memory/status.md` schon Tasks enthält. Wenn ja, frag den Auftraggeber, ob er wirklich neu beginnen will, und hör auf, falls nicht.
2. Setze in `memory/status.md` Phase „Planen“ und nächste Station 1.
3. Setze `VERSION` im Projekt auf `0.0.1` und lege `CHANGELOG.md` mit einem leeren Abschnitt `[Unreleased]` an, falls es beides noch nicht gibt.
4. Lade den Skill `brief-creator` und beginne das Interview. Frag zuerst, was der Auftraggeber bauen will, und lass ihn frei erzählen.
5. Halte nach dem Brief am Checkpoint an und warte auf die Freigabe.
