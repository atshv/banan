---
name: factory-weiter
description: Arbeitet die Software Factory ab dem aktuellen Stand weiter, bis ein Checkpoint, ein blockierter Task oder ein Limit erreicht ist. Nur auf Befehl des Auftraggebers.
disable-model-invocation: true
---

# Weiterarbeiten

1. Lies `memory/status.md` und `memory/questions.md`.
2. Hat der Auftraggeber seit dem letzten Checkpoint etwas entschieden, trag es ein (Freigabe, Antworten, Änderungswünsche).
3. Führe die nächste Station nach dem Ablauf in `AGENTS.md` aus. Danach die nächste, und so weiter.
4. Hör auf, sobald einer dieser Fälle eintritt
   - ein Checkpoint aus `factory/shared/checkpoints.md`
   - ein Task scheitert zum 3. Mal
   - ein Limit aus `factory/shared/limits.md` ist erreicht
   - eine Frage lässt sich nur durch den Auftraggeber klären
5. Schreib zum Schluss einen kurzen Statusbericht nach `factory/shared/statusbericht.md`.
