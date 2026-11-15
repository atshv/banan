# Profil web-app

Websites und Web-Apps im Browser.

## Stack-Vorschlag (Station 3)
- Next.js mit TypeScript im strict-Modus, Tailwind, shadcn/ui, Magic UI
- Tests mit Vitest (Logik) und Playwright (Abläufe im Browser)
- Lint und Format mit Ultracite/Biome
- Bibliotheken für Toasts, Drawer, Menüs usw. wählt der Skill `pick-ui-library`, nichts davon selbst bauen

## Pflicht-Prüfungen (Station 6 → `memory/gates.json`)
```json
{
  "pflicht": ["typecheck", "lint", "test", "build"],
  "typecheck": "npx tsc --noEmit",
  "lint": "npx ultracite check",
  "test": "npx vitest run && npx playwright test",
  "build": "npm run build"
}
```
Befehle an den gewählten Stack anpassen. Jede Pflicht-Prüfung muss einen echten Befehl haben.

## Design (Station 4)
- Regeln in `factory/design/design-regeln.md`, Komponenten in `factory/design/komponenten.md`
- Haltung und Feinschliff: `emil-design-eng`, `apple-design`, `frontend-design`
- Mehrere Varianten zum Auswählen: `prototype`
- Jeder Screen wird mit den Zuständen leer, lädt, Fehler und gefüllt beschrieben

## Bau (Station 9)
- Komponenten: `magic-ui`
- Animation bauen: `animate`, mehrere Elemente zusammen: `choreograph`, Ziehen und Wischen: `gestures`
- Damit es sich auf dem Handy wie eine App anfühlt: `mobile-native`
- Toasts: `ask-sonner`
- Welcher Emil-Skill passt: `ask-emil`, Begriffe für Bewegungen: `animation-vocabulary`

## Test (Station 10)
- Abläufe im Browser: `webapp-testing`
- Oberfläche mit Extremdaten angreifen (lange Namen, leere Listen, riesige Zahlen): `break-ui`
- Screenshots mit 390 px und 1440 px Breite, hell und dunkel

## Review (Station 11)
- Animationen: `review-animations`, ruckelnde Bewegung: `animation-performance`
- Überflüssige Bewegung entfernen: `remove-animations`

## Betrieb und Feinschliff (Stationen 7 und 15)
- Bestandsaufnahme aller Animationen: `improve-animations`, fehlende sinnvolle Bewegung: `find-animation-opportunities`
- Deine Design-Korrekturen zu festen Regeln machen: `learn-taste`

## Vor dem Release (Station 13)
- Impressum und Datenschutzerklärung vorhanden und verlinkt
- Cookie-Hinweis nur, wenn wirklich Tracking läuft
- Seitentitel, Beschreibung, Vorschaubild und Favicon gesetzt
- Fehlerseiten 404 und 500 gestaltet
- Umgebungsvariablen auf dem Hosting gesetzt, keine Keys im Code
- Fehler-Überwachung eingerichtet
- Auf einem echten Handy geprüft
