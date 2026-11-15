# Design-Regeln nach Magic UI

Gilt für Web-Apps mit React oder Next.js. Für native iPhone-Apps gelten nur Motion, Lesbarkeit und Gate.

Quelle: [magicuidesign/magicui](https://github.com/magicuidesign/magicui), Skill in `vendor-skills/magic-ui`.

## 1 Stack & Setup
- React oder Next.js mit Tailwind und shadcn.
- shadcn einmal pro Projekt einrichten: `npx shadcn@latest init`
- Komponenten nur über die Registry holen: `npx shadcn@latest add @magicui/<name>`
- shadcn-Tokens für Farben, Radius `0.625rem`, Schrift Geist (Sans und Mono).
- Hell und Dunkel von Anfang an mitdenken.
- Registry-Code nicht umschreiben, nur Props und className anpassen.
- Grössere Anpassung in eine eigene Wrapper-Komponente auslagern.
- Fehlende Pakete (z. B. `motion`, `cobe`) und CSS-Keyframes aus der Komponenten-Doku nachinstallieren.

## 2 Motion
- Erst Abschnitt, Ton und Motion-Stärke festlegen, dann Komponenten wählen.
- Start mit 1 Kernkomponente + 1 Effekt, erst bei Bedarf mehr.
- Höchstens 2 starke Effekte pro Bildschirm.
- Ein visueller Anker pro Hero.
- Im Grid nur 1–2 Karten animiert.
- Hintergrund-Effekte sind Nebenebene, nie Hauptinhalt.
- Immer `prefers-reduced-motion` beachten. Nur 6 von 80 Magic-UI-Komponenten tun das selbst, darum im Wrapper ergänzen.

## 3 Lesbarkeit & Bedienung
- Kontrast über animierten Hintergründen prüfen.
- Laufbänder (Marquee) pausieren bei Hover und Fokus.
- Alles per Tastatur erreichbar, Buttons immer mit `type`.
- Semantisches HTML, sinnvolle Alt-Texte.
- Ein Haupt-CTA und ein Neben-CTA pro Abschnitt.
- CTA-Stil pro Abschnitt einheitlich.
- Kurze, scannbare Texte in Karten.

## 4 Quality Gate vor Übergabe
- Mobile ohne horizontales Scrollen.
- Keine schweren Hintergründe gestapelt.
- `npx ultracite check` ohne Fehler.
- Kein `any`, keine API-Keys im Code.
- Fehlende Keyframes und Pakete nachinstalliert.
- Tester macht Screenshots mobil (390 px) und Desktop (1440 px).
