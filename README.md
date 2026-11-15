# 🍌 banan

**Eine schlanke KI-Software-Factory für Claude Code.** Du beschreibst deine Idee, banan führt sie durch 15 Stationen bis zur fertigen App. Du entscheidest nur an vier Stellen.

Version siehe [`VERSION`](VERSION) · Änderungen im [`CHANGELOG.md`](CHANGELOG.md) · vor v1.0.0 Entwicklungsstand

## Start

```bash
git clone https://github.com/atshv/banan
cd banan
./install.sh ~/Projekte/meine-app
```

Danach im Projektordner Claude Code starten und `/factory-start` eingeben. Gebraucht werden Git und Python 3.

| Du gibst ein | Was passiert |
|---|---|
| `/factory-start` | Interview zu deiner Idee, daraus entsteht der Brief |
| `/factory-weiter` | Arbeitet weiter bis zur nächsten Entscheidung |
| `/factory-status` | Stand in einfacher Sprache |
| `/factory-release` | Liefert die nächste Version aus |
| `Freigabe Brief` | Deine Freigabe. Auch `Architektur`, `Design`, `Release` |

## Die Linie

| Phase | Stationen |
|---|---|
| Planen | 1 Brief · 2 Research · 3 Architektur · 4 Design · 5 Plan |
| Ausrüsten | 6 Setup · 7 Skills · 8 Agents |
| Bauen & prüfen | 9 Builder · 10 Tester · 11 Reviewer · 12 Security |
| Ausliefern | 13 Release · 14 Doku |
| Betreiben | 15 Betrieb, Bugs und Feedback werden zum nächsten Brief |

Scheitert ein Task dreimal, kommt er zu dir. Fehler aus Review und Test werden zu Lessons und daraus zu besseren Skills.

## Schalter statt Vertrauen

Die wichtigsten Regeln erzwingt ein kleines Programm, nicht nur eine Anweisung. Es kostet keine Tokens, solange es nichts blockiert.

- Kein Produktcode direkt auf `main`
- Ein Builder schreibt nur im Bereich seines Tasks
- „Fertig“ gilt nur mit aufgezeichnetem, grünem Testlauf und bestandenem Review
- Weiter geht es nur mit deiner Freigabe, die KI kann sie sich nicht selbst geben

Details und Grenzen in [`shared/schalter.md`](shared/schalter.md).

## Aufbau

| Ordner | Inhalt |
|---|---|
| [`stations/`](stations) | 15 Stationen, je eine `SKILL.md` |
| [`shared/`](shared) | Regeln für alle Stationen |
| [`memory/`](memory) | Vorlagen fürs Projekt-Gedächtnis |
| [`design/`](design) | Design-Regeln nach Magic UI |
| [`engine/claude-code/`](engine/claude-code) | Orchestrator, Sub-Agents, Befehle, Schalter |
| [`vendor-skills/`](vendor-skills) | Übernommene Skills mit ihren Lizenzen |

`install.sh` kann jederzeit wieder laufen und aktualisiert banan im Projekt. Dein Projekt-Gedächtnis und eigene Einstellungen bleiben erhalten.

## Herkunft

Skill-Muster aus [anthropics/skills](https://github.com/anthropics/skills), Design-Regeln aus [magicuidesign/magicui](https://github.com/magicuidesign/magicui).
