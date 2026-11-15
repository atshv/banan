---
name: release
description: Baut, deployed und veröffentlicht das Projekt, bei Web über die Hosting-Plattform, bei iPhone über TestFlight und App Store. Nutze diesen Skill, wenn alle Tasks eines Meilensteins grün, reviewt und sicherheitsgeprüft sind. Release ist ein Checkpoint, der Auftraggeber gibt frei.
---

# 13 Release

Erst hier sieht ein echter Nutzer das Ergebnis. Darum wird nichts veröffentlicht, was nicht durch alle Gates ging.

## Input
- Alle Task-Berichte des Meilensteins mit Ergebnis OK
- `handoffs/06-setup.md`

## Ablauf
1. Alle Task-Branches nach `shared/git-strategie.md` zusammenführen.
2. Vollständige Testsuite und Security-Check auf dem Hauptbranch laufen lassen.
3. Versionsnummer nach `shared/versionierung.md` setzen (Start bei 0.0.1), Changelog vom Doku-Writer übernehmen.
4. Vor v1.0.0 nur Staging oder TestFlight. Ab v1.0.0 Web zuerst auf Staging, dann Produktion, iPhone über TestFlight in den App Store.
5. Statusbericht mit Link an den Auftraggeber, Freigabe abwarten (Checkpoint).
6. Nach Freigabe veröffentlichen und Git-Tag setzen.

## Output → `handoffs/13-release-<Version>.md`
```
Version · Datum · Enthaltene Tasks · Link (Staging, Produktion, TestFlight) · Rollback-Befehl
```

## Gate
- Alle Tests auf dem Hauptbranch grün.
- Rollback ist dokumentiert.
- Auftraggeber hat freigegeben.
