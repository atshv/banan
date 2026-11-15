---
name: projekt-setup
description: Richtet Repo, Ordnerstruktur, Abhängigkeiten, CI und Entwicklungsumgebung ein, bevor der erste Builder startet. Nutze diesen Skill einmal pro Projekt nach dem Planner und immer, wenn ein neues Teilprojekt (z. B. Backend) dazukommt. So arbeiten alle Builder im gleichen Gerüst.
---

# 6 Projekt-Setup

Ohne festes Gerüst richtet jeder Builder-Agent das Projekt anders ein. Das führt zu Chaos und doppeltem Code.

## Input
- `handoffs/03-architektur.md` (Stack, Ordnerstruktur)

## Ablauf
1. Repo anlegen, Branch-Regeln aus `shared/git-strategie.md` einrichten. Gibt es auf `main` schon einen Commit, das Gerüst auf dem Branch `setup/grundgeruest` bauen und danach nach `main` mergen, denn die Schreibsperre lässt auf `main` keinen Produktcode zu.
2. Grundgerüst mit dem offiziellen Init-Befehl des Stacks erzeugen (z. B. `npx create-next-app`, Xcode-Vorlage).
3. Web-Apps: `npx shadcn@latest init`, danach Tailwind und Design-Tokens aus `design/design-regeln.md`.
4. Linter und Formatter einrichten (Web: `npx ultracite init`).
5. CI anlegen, das bei jedem Push baut, lintet und testet.
6. `memory/` ins Repo kopieren, `conventions.md` mit Namen und Ordnern füllen.
7. Pflicht-Prüfungen aus dem Profil in `memory/gates.json` eintragen (Liste `pflicht` und je ein Befehl), an den gewählten Stack angepasst. Bei mehreren Profilen gilt die Summe. Der Tester startet sie später über `factory_run.py`.
8. Die Vertrags-Dateien aus der Architektur anlegen und ihre Pfade in `memory/gates.json` unter `vertrag` eintragen, z. B. `"vertrag": ["src/contracts/"]`.
9. Prüfen, dass das leere Projekt startet und die CI grün ist.

## Output → `handoffs/06-setup.md`
```
# Setup: <Projekt>
Repo · Startbefehl · Testbefehl · Lint-Befehl · CI-Link · Umgebungsvariablen (nur Namen, keine Werte)
```

## Gate
- Leeres Projekt startet lokal.
- CI läuft grün.
- Jede Pflicht-Prüfung des Profils steht in `memory/gates.json` mit einem echten Befehl und läuft im leeren Projekt grün.
- Keine Secrets im Repo, nur `.env.example`.

## Nutzt
`web-artifacts-builder` (Init-Script als Vorbild)
