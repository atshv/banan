# Versionierung

Gilt für die Factory selbst und für jedes Projekt, das sie baut.

## Regeln
- Jedes Projekt startet bei **0.0.1**.
- Format `MAJOR.MINOR.PATCH`, der Git-Tag bekommt ein `v` davor (`v0.0.1`).
- **Vor v1.0.0** ist alles Entwicklungsstand.
  - `0.0.x` → Patch für Fixes und kleine Änderungen
  - `0.x.0` → Minor für eine neue Funktion oder einen fertigen Meilenstein, Patch zurück auf 0
- **v1.0.0** ist das erste echte Release. Es braucht den Release-Checkpoint, also deine Freigabe.
- **Ab v1.0.0** gilt normales SemVer.
  - Patch → Fehler behoben, nichts ändert sich für Nutzer
  - Minor → neue Funktion, alles Bestehende läuft weiter
  - Major → etwas Bestehendes ändert sich oder fällt weg

## Bei jeder neuen Version
1. Nummer in `VERSION` erhöhen.
2. Einträge aus `[Unreleased]` in `CHANGELOG.md` unter die neue Version mit Datum verschieben.
3. Vergleichslinks unten im Changelog nachführen.
4. Nach dem Merge auf `main` den Tag setzen: `git tag v<Version> && git push origin v<Version>`.

## Changelog-Abschnitte
Hinzugefügt · Geändert · Behoben · Entfernt · Sicherheit
