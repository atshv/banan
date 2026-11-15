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
├── VERSION              Aktuelle Version
├── CHANGELOG.md         Alle Änderungen pro Version
├── stations/            15 Stationen, je eine SKILL.md
├── shared/              Regeln, die für alle Stationen gelten
├── memory/              Vorlagen fürs Projekt-Gedächtnis
├── design/              Design-Regeln nach Magic UI
├── engine/claude-code/  Motor: Orchestrator, Sub-Agents, Befehle, Sperren
├── install.sh           Installiert die Factory in einen Projektordner
└── vendor-skills/       Übernommene Skills von Anthropic und Magic UI (mit Lizenz)
```

## So startest du ein Projekt

Der Motor ist Claude Code. Er liegt in `engine/claude-code/` und wird mit `install.sh` in dein Projekt kopiert.

1. Factory einmal auf deinen Computer holen: `git clone https://github.com/atshv/banan`
2. In den Ordner `banan` wechseln und das Projekt anlegen: `./install.sh ~/Projekte/meine-app`
   Oder in Claude Code im Ordner `banan` eingeben: `/factory-neu ~/Projekte/meine-app`
3. Im Projektordner Claude Code starten und `/factory-start` eingeben.
4. Station 1 interviewt dich. Danach geht es mit `/factory-weiter` Station für Station weiter.
5. Du entscheidest nur an den Checkpoints (Brief, Architektur, Design, Release) und wenn ein Task 3× scheitert.

| Befehl | Was passiert |
|---|---|
| `/factory-start` | Neues Projekt, Interview für den Brief |
| `/factory-weiter` | Weiter bis zum nächsten Checkpoint oder Problem |
| `/factory-status` | Stand in einfacher Sprache |
| `/factory-release` | Nächste Version ausliefern |

`install.sh` kann jederzeit wieder laufen, um die Factory im Projekt zu aktualisieren. Dein Projekt-Gedächtnis, deine `settings.json` und eigene Abschnitte in `CLAUDE.md` bleiben dabei erhalten.

### Was im Projekt landet
```
meine-app/
├── CLAUDE.md            Anleitung für den Orchestrator
├── .claude/skills/      15 Stationen, 4 Befehle, übernommene Skills
├── .claude/agents/      Researcher, Builder, Tester, Reviewer, Security
├── .claude/settings.json  Sperren (kein Force-Push, kein .env lesen, kein rm -rf)
├── factory/             Regeln und Design-Vorgaben der Factory
└── memory/              Projekt-Gedächtnis und Übergaben
```

## Muster, die jeder Skill hier befolgt

- **Description = Auslöser.** Sie sagt klar, wann der Skill greift.
- **Schlanke SKILL.md.** Unter 500 Zeilen, Details in `references/`.
- **Scripts als Blackbox.** In `scripts/`, aufrufen statt lesen.
- **Warum statt MUSS.** Gründe erklären statt Befehle in Grossbuchstaben.
- **Evals.** Mit und ohne Skill vergleichen, bevor ein Skill als fertig gilt.
- **Wiederholtes bündeln.** Was Agents mehrfach bauen, wird ein Script.

## Versionen

Aktuelle Version steht in `VERSION`, alle Änderungen in `CHANGELOG.md`. Jedes Projekt startet bei 0.0.1, v1.0.0 ist das erste echte Release. Regeln in `shared/versionierung.md`.

## Herkunft

Die Muster stammen aus [anthropics/skills](https://github.com/anthropics/skills), die Design-Regeln aus [magicuidesign/magicui](https://github.com/magicuidesign/magicui). Lizenzen liegen bei den Skills in `vendor-skills/`.
