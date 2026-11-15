---
name: design-ux
description: Legt Screens, Abläufe und den visuellen Stil fest, bevor Code entsteht. Nutze diesen Skill nach der Architektur für jedes Projekt mit Oberfläche und immer, wenn neue Screens oder Abschnitte dazukommen. Für Web-Apps gelten die Regeln in design/design-regeln.md (Magic UI).
---

# 4 Design / UX

Wer erst baut und dann gestaltet, baut doppelt. Hier wird festgelegt, wie es aussieht und wie man es bedient.

## Input
- `handoffs/01-brief.md`, `handoffs/03-architektur.md`
- `design/design-regeln.md`, `design/komponenten.md`

## Ablauf
1. Alle Screens auflisten, mit Zweck und wichtigsten Elementen.
2. Hauptabläufe als Schritte beschreiben (z. B. Start → Scan → Ergebnis).
3. Pro Abschnitt Ton und Motion-Stärke festlegen (ruhig, mittel, stark).
4. Komponenten aus `design/komponenten.md` wählen. Start mit 1 Kernkomponente + 1 Effekt.
5. Wireframe als Bild oder Mockup erstellen und vom Auftraggeber bestätigen lassen.

## Output → `handoffs/04-design.md`
```
# Design: <Projekt>
## Screens (Name, Zweck, Elemente)
## Abläufe
## Stil (Farben, Schrift, Radius, Hell/Dunkel)
## Komponenten pro Abschnitt (mit Motion-Stärke)
## Wireframes (Links oder Dateien)
```

## Gate
- Jeder Screen ist einem Must-have zugeordnet.
- Kein Abschnitt hat mehr als 2 starke Effekte.
- Native iPhone-Apps: nur Motion-, Lesbarkeits- und Gate-Regeln gelten.

## Nutzt
`magic-ui`, `frontend-design`, `theme-factory`
