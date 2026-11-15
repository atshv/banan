# Limits

Limits verhindern, dass sich ein Agent endlos im Kreis dreht und Geld verbrennt.

| Limit | Wert (Startwert, anpassen) |
|---|---|
| Versuche pro Task | 3, danach an den Auftraggeber |
| Schritte pro Agent-Lauf | 50 |
| Budget pro Task | festlegen in `handoffs/08-agents.md` |
| Budget pro Projekt | festlegen im Brief |
| Dateien pro Task | höchstens 10, sonst Task teilen |

## Wenn ein Limit erreicht ist
1. Agent stoppt sofort.
2. Stand in `memory/status.md` als „blockiert“ eintragen, mit Grund.
3. Orchestrator meldet im Statusbericht.
