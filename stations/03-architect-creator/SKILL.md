---
name: architect-creator
description: Legt Stack, Module, Datenmodell und Schnittstellen eines Projekts fest und begründet jede Entscheidung. Nutze diesen Skill nach dem Research und immer, wenn sich die Struktur eines Projekts ändert, etwa bei neuen Modulen, einem Wechsel der Datenbank oder neuen Diensten.
---

# 3 Architect-Creator

Die Architektur ist der Bauplan. Builder halten sich daran, Reviewer prüfen dagegen.

## Input
- `handoffs/01-brief.md`, `handoffs/02-research.md`
- `memory/decisions.md` (bestehende Entscheidungen)

## Ablauf
1. Stack wählen, basierend auf der Research-Empfehlung.
2. Module schneiden. Jedes Modul hat eine Aufgabe und eine klare Schnittstelle.
3. Datenmodell festlegen (Tabellen oder Typen mit Feldern).
4. Den Vertrag festlegen, also die Datentypen und Schnittstellen zwischen den Modulen, und in welchen Dateien er liegen wird (z. B. `src/contracts/`). Builder bauen später gegen ihn und dürfen ihn nicht still ändern.
5. Jede wichtige Entscheidung als ADR in `memory/decisions.md` eintragen.
6. Dem Auftraggeber in einfacher Sprache zeigen (Checkpoint).

## Output → `handoffs/03-architektur.md`
```
# Architektur: <Projekt>
## Stack
## Module (Name, Aufgabe, Schnittstelle)
## Datenmodell
## Vertrag (Typen und Schnittstellen, mit Dateipfaden)
## Externe Dienste
## Ordnerstruktur
## Bewusst weggelassen
```

ADR-Format in `memory/decisions.md`
```
## ADR-<Nr>: <Titel> (<Datum>)
Entscheid · Grund · Verworfene Alternativen · Folgen
```

## Gate
- Jedes Must-have aus dem Brief ist einem Modul zugeordnet.
- Auftraggeber hat freigegeben.

## Nutzt
`mcp-builder` (Phasen-Plan, Referenzen erst bei Bedarf laden)
