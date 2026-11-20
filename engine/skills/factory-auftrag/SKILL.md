---
name: factory-auftrag
description: Nimmt in einem bestehenden Projekt einen neuen Wunsch auf und schreibt daraus den Auftrag. Nur auf Befehl des Auftraggebers.
disable-model-invocation: true
---

# Neuer Auftrag

1. Lies `memory/status.md`. Ist noch ein Task unterwegs oder ein Pull Request nicht gemergt, sag das dem Auftraggeber und frag, ob der neue Auftrag warten soll.
2. Lass den Auftraggeber frei erzählen. Stell höchstens 5 Rückfragen, in einfacher Sprache.
3. Such in der Karte (`memory/handoffs/00-bestand.md`), welche Teile, welches Rezept und welche Prüfungen der Wunsch berührt.
4. Hol den neuesten Hauptzweig, vergib die nächste freie Task-Nummer und leg den Branch nach dem Muster der Karte an.
5. Schreib den Auftrag nach der Vorlage und zeig ihn dem Auftraggeber in einfacher Sprache.
6. Bitte um `Freigabe Brief` und hör auf.

## Output → `memory/handoffs/01-brief.md`
```
# Auftrag: <Titel>
## Ziel (ein Satz)
## Was sich für den Nutzer ändert
## Was gleich bleibt
## Berührte Teile (aus der Karte)
## Rezept (Skill des Projekts, falls eines passt)
## Vertrag ändern (nein, oder was und welcher Versionssprung)
## Sichtbare Änderung (nein, oder was neu aufgenommen werden muss)
## Abnahmekriterien (prüfbar, je eine Zeile)
## Offene Fragen
```

## Gate
- Jedes Abnahmekriterium lässt sich mit einer Prüfung der Karte belegen.
- Der Auftraggeber hat den Auftrag freigegeben.
