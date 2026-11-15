# Profil engine

Kernlogik ohne Oberfläche: Spiel-, Rechen-, Regel- oder Such-Engine, Parser, Bibliothek. Oft zusammen mit einem zweiten Profil, das die Engine benutzt.

## Stack-Vorschlag (Station 3)
- Sprache nach Einsatzort: TypeScript für Web, Swift für iPhone, sonst nach Research
- Die Engine kennt keine Oberfläche, kein Netzwerk und keine Uhr. Zeit, Zufall und Daten bekommt sie von aussen. So bleibt sie berechenbar und testbar.
- Öffentliche Schnittstelle klein und als Vertrag festgelegt (Typen, Funktionen, Fehlerfälle), bevor gebaut wird
- Keine oder sehr wenige fremde Pakete

## Pflicht-Prüfungen (Station 6 → `memory/gates.json`)
```json
{
  "pflicht": ["typecheck", "lint", "test", "build"],
  "typecheck": "npx tsc --noEmit",
  "lint": "npx ultracite check",
  "test": "npx vitest run --coverage",
  "build": "npm run build"
}
```
Befehle an die gewählte Sprache anpassen, z. B. `swift build` und `swift test`.

## Design (Station 4)
Keine Screens. Stattdessen wird die Schnittstelle entworfen: Namen, Eingaben, Ausgaben, Fehler, je mit einem Beispiel. Das Dokument `04-design.md` enthält diesen Vertrag.

## Bau (Station 9)
- Gleiche Eingabe ergibt immer gleiche Ausgabe
- Fehler sind Teil des Vertrags, keine stillen Sonderfälle
- Änderungen am Vertrag macht nur der Orchestrator, nach Rückfrage

## Test (Station 10)
- Tests zuerst, aus den Beispielen des Vertrags
- Randfälle: leer, null, sehr gross, negativ, ungültig
- Eigenschafts-Tests mit vielen Zufallsfällen, wo es eine Regel gibt, die immer gelten muss
- Abdeckung der Kernlogik hoch halten, Ziel im Brief festlegen

## Vor dem Release (Station 13)
- Jede öffentliche Funktion dokumentiert, mit lauffähigem Beispiel
- Changelog nennt jede Änderung an der Schnittstelle
- Version nach `factory/shared/versionierung.md`, Bruch der Schnittstelle nur mit deiner Freigabe
