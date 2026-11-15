---
name: research
description: Prüft vor jeder Architektur-Entscheidung den aktuellen Stand von Libraries, APIs, Preisen und Limits. Nutze diesen Skill nach dem Brief und immer dann, wenn ein Agent eine Technologie, ein Paket oder einen Dienst wählen will. Wissen aus dem Training ist oft veraltet, darum hier nachschlagen statt annehmen.
---

# 2 Research

Falsche Annahmen über eine API kosten später ganze Tage. Hier werden sie früh und billig gefunden.

## Input
- `handoffs/01-brief.md`

## Ablauf
1. Aus dem Brief die technischen Fragen ableiten (Plattform, Daten, Dienste, Kosten).
2. Pro Frage aktuelle Quellen lesen. Offizielle Doku vor Blogposts.
3. Für jede Option notieren: Version, Preis, Limits, Lizenz, Wartungszustand.
4. Höchstens 3 Optionen pro Frage, mit Empfehlung und Grund.

## Output → `handoffs/02-research.md`
```
# Research: <Projekt>
## Frage 1: <...>
| Option | Version | Kosten | Limits | Lizenz | Empfehlung |
Quellen: <Links>
## Risiken
## Was noch unklar ist
```

## Gate
- Jede Empfehlung hat eine Quelle mit Datum.
- Kostenpflichtige Dienste sind als solche markiert.

## Nutzt
`mcp-builder` Phase 1 (erst Doku studieren, dann planen)
