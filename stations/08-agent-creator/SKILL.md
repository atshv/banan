---
name: agent-creator
description: Definiert Rollen, Prompts, erlaubte Tools und Grenzen für jeden Agent der Factory. Nutze diesen Skill, wenn ein Projekt startet oder eine Station einen neuen oder angepassten Agent braucht, etwa ein Builder mit Spezial-Skills.
---

# 8 Agent-Creator

Ein Agent mit zu vielen Tools oder unklarer Rolle macht Dinge, die keiner bestellt hat. Klare Grenzen machen ihn verlässlich.

## Input
- Stationsliste aus dem README, Skills aus `handoffs/07-skills.md`
- `shared/limits.md`

## Ablauf
1. Pro Rolle festlegen: Aufgabe, Input, Output, welche Skills sie lädt.
2. Nur die Tools freigeben, die die Rolle wirklich braucht (Reviewer liest nur, Builder schreibt nur im eigenen Task).
3. Modell pro Rolle wählen (stark für Architect und Reviewer, günstig für Routine).
4. Limits eintragen: Token-Budget, maximale Schritte, maximale Versuche.
5. Prompt mit Begründungen statt Befehlen schreiben.

## Output → `handoffs/08-agents.md`
```
## Agent: <Rolle>
Modell · Skills · Tools (erlaubt) · Tools (verboten) · Budget · Max. Schritte · Prompt-Datei
```

## Gate
- Reviewer hat keinen Schreibzugriff auf Code.
- Jeder Agent hat ein Budget.

## Nutzt
`claude-api` (nur wenn die Agents über die Claude-API laufen)
