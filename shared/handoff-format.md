# Handoff-Format

Jede Station übergibt ihr Ergebnis als Datei in `memory/handoffs/`. Die nächste Station liest nur diese Datei und das Gedächtnis, nicht den Chatverlauf. So geht unterwegs nichts verloren.

## Kopf jeder Handoff-Datei
```
---
station: <Nr und Name>
projekt: <Name>
datum: <JJJJ-MM-TT>
task: <T-Nr oder leer>
ergebnis: ok | abgelehnt | blockiert
naechste_station: <Nr>
---
```

## Regeln
- Ein Handoff ist für sich verständlich. Wer nur diese Datei liest, weiss, was zu tun ist.
- Annahmen werden als Annahmen markiert und in `memory/questions.md` eingetragen.
- Keine Secrets, keine Passwörter, keine Keys.
- Die genaue Gliederung steht im Abschnitt „Output“ der jeweiligen Station.
