---
name: factory-release
description: Liefert die nächste Version des Projekts aus, mit Versionsnummer, Changelog, Doku und Tag. Nur auf Befehl des Auftraggebers.
disable-model-invocation: true
---

# Version ausliefern

1. Prüfe in `memory/status.md`, dass alle Tasks des Meilensteins „fertig“ sind. Wenn nicht, nenn die offenen und hör auf.
2. Bestimme die neue Version nach `factory/shared/versionierung.md`. Vor v1.0.0 nur 0.x.y. Schlag die Nummer vor und lass sie bestätigen.
3. v1.0.0 ist das erste echte Release. Frag dafür ausdrücklich nach und erklär, was es bedeutet.
4. Lade den Skill `doku-writer`, dann den Skill `release`, und arbeite beide ab.
5. Halte vor dem Veröffentlichen am Release-Checkpoint an und bitte den Auftraggeber, als eigene Nachricht `Freigabe Release` zu schreiben. Ohne sie blockiert ein Schalter den Tag.
6. Nach der Freigabe Tag `v<Version>` auf `main` setzen und den Release-Bericht schreiben.
