---
name: factory-uebernehmen
description: Übernimmt ein bestehendes Projekt in die Software Factory. Liest das ganze Repo und schreibt daraus die Karte des Projekts, die Prüfungen und den Vertrag. Nur auf Befehl des Auftraggebers.
disable-model-invocation: true
---

# Bestehendes Projekt übernehmen

Ziel: Jede KI weiss danach genau, wie dieses eine Projekt gebaut ist und was darin wie getan wird. Du erfindest nichts. Jede Angabe stammt aus dem Repo und nennt ihre Quelle.

Arbeite auf einem eigenen Branch ohne Task-Nummer, z. B. `harness/bestand`.

## Ablauf
1. **Lesen.** README, Architektur- und Entscheidungsdokumente, Doku-Ordner, Manifeste (`package.json`, `CMakeLists.txt`, `Package.swift` …), CI, Lint-Regeln, Tests, die letzten 50 Commits. Bei grossen Repos ein Sub-Agent pro Bereich, jeder liefert Fundstellen mit Pfad.
2. **Prüfungen finden.** Jeden Befehl, den die CI oder die Doku als Prüfung nennt, einmal wirklich ausführen. Was hier nicht läuft (anderes Gerät, fehlendes Werkzeug), als „nur lokal“ festhalten, nicht weglassen.
3. **`memory/gates.json` füllen.**
   - `"modus": "bestand"`, dazu `"abschluss": "pr"`, wenn im Projekt ein Mensch mergt
   - `pflicht` und je ein Befehl, genau wie CI und Doku sie nennen
   - `wenn` für Prüfungen, die nur bei bestimmten Dateien nötig sind
   - `vertrag` mit den Dateien, die Schnittstellen und Datentypen festlegen
   - `zaehlt_nicht` für erzeugte Dateien, Testdaten und Referenzbilder
4. **Karte schreiben** nach der Vorlage unten. Kurz. Wo das Projekt ein Dokument hat, verweis darauf, statt es abzuschreiben.
5. **`memory/conventions.md` füllen**: Begriffe, Namen, Branch-Muster, Commit-Regeln, Sprache.
6. **Skills wählen.** In `memory/skills.txt` steht pro Zeile ein Skill von banan, den das Projekt braucht. Was fehlt, installiert `install.sh` nicht.
7. **Rezepte.** Für jede Arbeit, die im Projekt immer gleich abläuft, ein eigener Skill mit dem Skill `skill-creator`. Jeder verweist auf die Anleitung im Projekt.
8. Zeig dem Auftraggeber die Karte in einfacher Sprache, bitte um `Freigabe Bestand` und hör auf.

## Output → `memory/handoffs/00-bestand.md`
```
# Bestand: <Projekt>
## Was es ist (drei Sätze)
## Aufbau (Teile, wer wen benutzen darf)
## Unverrückbar (Entscheidungen und Verbote, je mit Quelle)
## Vertrag (Dateien, Regeln für Änderungen)
## Prüfungen (Name, Befehl, wann nötig, wo sie läuft)
## Ablauf einer Änderung (Branch, Commit, Pull Request, wer mergt)
## Fertig heisst
## Rezepte (Arbeit → Anleitung im Projekt → Skill)
## Doku, die mitziehen muss
## Für den Builder
## Für den Tester
## Für den Reviewer
## Für Security
## Stolperfallen (aus Doku und Git-Geschichte)
## Offene Fragen
```

## Gate
- Jede Regel der Karte nennt ihre Quelle im Repo.
- Jede Pflicht-Prüfung in `memory/gates.json` ist einmal gelaufen oder als „nur lokal“ markiert.
- Der Auftraggeber hat die Karte freigegeben.

## Später
Ändert sich das Projekt, führst du die Karte nach. Jede Änderung der Karte braucht eine neue `Freigabe Bestand`.
