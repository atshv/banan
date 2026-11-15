# Software Factory von A bis Z

Ein Baukasten für eine KI-Software-Factory. 15 Stationen bauen ein Projekt von der Idee bis zum Betrieb. Übergreifende Regeln halten das Ganze zusammen.

Whiteboard mit der Übersicht: https://claude.ai/artifact/4hGCWWWr2gkzLB6iUQdmXu

**Leitsatz** Klare Übergaben zwischen Stationen zählen mehr als mehr Creator.

## Ablauf

| Phase | Station | Ordner |
|---|---|---|
| Planen | 1 Brief-Creator | `stations/01-brief-creator` |
| | 2 Research | `stations/02-research` |
| | 3 Architect-Creator | `stations/03-architect-creator` |
| | 4 Design / UX | `stations/04-design-ux` |
| | 5 Planner | `stations/05-planner` |
| Ausrüsten | 6 Projekt-Setup | `stations/06-projekt-setup` |
| | 7 Skill-Creator | `stations/07-skill-creator` |
| | 8 Agent-Creator | `stations/08-agent-creator` |
| Bauen & prüfen | 9 Builder | `stations/09-builder` |
| | 10 Tester | `stations/10-tester` |
| | 11 Reviewer | `stations/11-reviewer` |
| | 12 Security-Check | `stations/12-security-check` |
| Ausliefern | 13 Release | `stations/13-release` |
| | 14 Doku-Writer | `stations/14-doku-writer` |
| Betreiben | 15 Betrieb | `stations/15-betrieb` |

**Rückwege**
- Tester oder Reviewer lehnen ab → zurück zum Builder. Höchstens 3 Versuche, dann geht der Task an dich.
- Reviewer findet wiederkehrende Fehler → Lessons learned → Skill-Creator verbessert die Skills.
- Betrieb meldet Bugs und Feedback → neuer Brief.

## Ordner

```
software-factory/
├── README.md            Diese Übersicht
├── stations/            15 Stationen, je eine SKILL.md
├── shared/              Regeln, die für alle Stationen gelten
├── memory/              Vorlagen fürs Projekt-Gedächtnis
├── design/              Design-Regeln nach Magic UI
└── vendor-skills/       Übernommene Skills von Anthropic und Magic UI (mit Lizenz)
```

## So startest du ein Projekt

1. Ordner `memory/` ins neue Projekt-Repo kopieren.
2. Orchestrator mit `shared/orchestrator.md` starten.
3. Station 1 interviewt dich. Danach laufen die Stationen der Reihe nach.
4. Du entscheidest nur an den Checkpoints (Brief, Architektur, Release) und wenn ein Task 3× scheitert.

## Muster, die jeder Skill hier befolgt

- **Description = Auslöser.** Sie sagt klar, wann der Skill greift.
- **Schlanke SKILL.md.** Unter 500 Zeilen, Details in `references/`.
- **Scripts als Blackbox.** In `scripts/`, aufrufen statt lesen.
- **Warum statt MUSS.** Gründe erklären statt Befehle in Grossbuchstaben.
- **Evals.** Mit und ohne Skill vergleichen, bevor ein Skill als fertig gilt.
- **Wiederholtes bündeln.** Was Agents mehrfach bauen, wird ein Script.

## Herkunft

Die Muster stammen aus [anthropics/skills](https://github.com/anthropics/skills), die Design-Regeln aus [magicuidesign/magicui](https://github.com/magicuidesign/magicui). Lizenzen liegen bei den Skills in `vendor-skills/`.
