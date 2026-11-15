# Profil backend

Server, APIs und Kommandozeilen-Programme.

## Stack-Vorschlag (Station 3)
- TypeScript im strict-Modus auf Node, oder die Sprache aus dem Research
- API als Vertrag festgelegt (Routen, Eingaben, Antworten, Fehlercodes), bevor gebaut wird
- Datenbank mit Migrationen, nie von Hand am Schema ändern
- Eingaben an jeder Grenze prüfen
- Einstellungen und Keys nur über Umgebungsvariablen

## Pflicht-Prüfungen (Station 6 → `memory/gates.json`)
```json
{
  "pflicht": ["typecheck", "lint", "test", "build"],
  "typecheck": "npx tsc --noEmit",
  "lint": "npx ultracite check",
  "test": "npx vitest run",
  "build": "npm run build"
}
```

## Design (Station 4)
Keine Screens. `04-design.md` enthält den API-Vertrag oder bei einem Kommandozeilen-Programm die Befehle mit Beispielen und Fehlermeldungen.

## Bau (Station 9)
- Anbindung fremder Dienste und Tools: `mcp-builder`
- Fehlermeldungen sagen, was zu tun ist
- Keine Secrets in Logs

## Test (Station 10)
- Jede Route mit gutem Fall, falscher Eingabe und fehlender Berechtigung
- Tests gegen eine echte Test-Datenbank, nicht nur gegen Attrappen

## Vor dem Release (Station 13)
- Migrationen laufen auf einer Kopie der Daten durch
- Backup und Wiederherstellung einmal geprobt
- Zugriffsbegrenzung gegen Missbrauch
- Fehler-Überwachung und ein Gesundheits-Check eingerichtet
- Rollback-Befehl dokumentiert
