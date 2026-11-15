# Orchestrator

Der Orchestrator steuert die Factory. Er baut nichts selbst, sondern verteilt Arbeit und hält den Projektzustand.

Umgesetzt ist er mit Claude Code in `engine/claude-code/CLAUDE.md`. Sub-Agents liegen in `engine/claude-code/.claude/agents/`.

## Aufgaben
- Liest beim Start `memory/status.md` und entscheidet, welche Station als Nächstes läuft.
- Startet pro Station einen Agent nach `handoffs/08-agents.md`.
- Prüft nach jeder Station das Gate aus deren SKILL.md. Nicht bestanden → zurück, nicht weiter.
- Führt den Versuchszähler pro Task. Beim 3. Fehlschlag stoppt er und meldet an den Auftraggeber.
- Hält an jedem Checkpoint an (`checkpoints.md`).
- Schreibt nach jeder Station den Stand in `memory/status.md`.
- Erstellt den Statusbericht (`statusbericht.md`).

## Reihenfolge
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → pro Task (9 → 10 → 11 → 12) → 13 → 14 → 15 → zurück zu 1 oder 5

## Parallel erlaubt
- Tasks ohne gegenseitige Abhängigkeit dürfen parallel gebaut werden, je in eigenem Branch.
- Nie parallel: zwei Agents im gleichen Task oder in der gleichen Datei.
