---
name: brief-creator
description: Startet jedes neue Software-Projekt der Factory. Interviewt den Auftraggeber, bis Ziel, Nutzer, Must-haves, No-gos und Abnahmekriterien feststehen, und schreibt daraus den Projektbrief. Nutze diesen Skill immer, wenn eine neue App-Idee, ein neues Feature oder ein neuer Brief aus dem Betrieb kommt, auch wenn die Idee schon klar wirkt.
---

# 1 Brief-Creator

Der Brief ist die Grundlage für alle späteren Stationen. Was hier fehlt, baut später niemand richtig.

## Input
- Idee des Auftraggebers, frei formuliert
- Bei Wiederaufnahme `memory/questions.md` und Meldungen aus Station 15

## Ablauf
1. Erst Kontext sammeln. Den Auftraggeber alles erzählen lassen, was er im Kopf hat.
2. Rückfragen stellen, höchstens 5 auf einmal, in einfacher Sprache.
3. Lücken-Check gegen die Vorlage unten. Fehlt etwas, nachfragen statt raten.
4. Brief schreiben und dem Auftraggeber zur Freigabe zeigen (Checkpoint).

## Output → `handoffs/01-brief.md`
```
# Projektbrief: <Name>
## Ziel (ein Satz)
## Nutzer und Situation
## Must-haves
## Nice-to-haves
## No-gos
## Abnahmekriterien (prüfbar, je eine Zeile)
## Profil (eine Zeile `Profil: web-app`, mehrere mit Komma. Auswahl in `factory/profiles/README.md`)
## Offene Fragen
```

## Gate
- Jedes Must-have hat mindestens ein prüfbares Abnahmekriterium.
- Mindestens ein Profil ist gewählt.
- Auftraggeber hat den Brief freigegeben.

## Nutzt
`doc-coauthoring` (Kontext sammeln, Rückfragen, Lücken-Check), `discernment-nudge` (gezielte Rückfragen)
