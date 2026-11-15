<p align="center">
  <img src="docs/images/banner.svg" alt="banan – die schlanke Software-Factory für Claude Code, Cursor, Gemini, Codex und Co." width="100%">
</p>

<p align="center">
  <a href="https://github.com/atshv/banan/tags"><img alt="Version" src="https://img.shields.io/github/v/tag/atshv/banan?style=flat-square&label=version&color=FFD23F&labelColor=0E1014"></a>
  <img alt="KIs" src="https://img.shields.io/badge/KIs-Claude%20Code%20%C2%B7%20Cursor%20%C2%B7%20Gemini%20%C2%B7%20Codex%20%C2%B7%20DeepSeek-d97757?style=flat-square&labelColor=0E1014">
  <img alt="Stationen" src="https://img.shields.io/badge/Stationen-15-FFD23F?style=flat-square&labelColor=0E1014">
  <img alt="Abhängigkeiten" src="https://img.shields.io/badge/Abh%C3%A4ngigkeiten-keine-34d399?style=flat-square&labelColor=0E1014">
</p>

<p align="center">
  <b>Du beschreibst deine Idee. banan baut sie Station für Station bis zur fertigen App.</b><br>
  Du entscheidest nur an vier Stellen. Den Rest prüft die Factory selbst.
</p>

<br>

## 🚀 Start

```bash
git clone https://github.com/atshv/banan
cd banan
./install.sh ~/Projekte/meine-app            # Claude Code
./install.sh ~/Projekte/meine-app cursor     # oder gemini, codex, deepseek, andere
./install.sh ~/Projekte/meine-app cursor,codex   # mehrere auf einmal
```

Dann im Projektordner deine KI öffnen und `factory-start` schreiben, in Claude Code `/factory-start`. Du brauchst nur Git und Python 3.

## 💬 Bedienung

| Du gibst ein | Was passiert |
|:--|:--|
| `factory-start` | Interview zu deiner Idee, daraus entsteht der Brief |
| `factory-weiter` | Arbeitet weiter bis zur nächsten Entscheidung |
| `factory-status` | Stand in einfacher Sprache |
| `factory-release` | Liefert die nächste Version aus |
| `Freigabe Brief` | Deine Freigabe, auch für `Architektur`, `Design` und `Release` |

## 🏭 Die Linie

<p align="center">
  <img src="docs/images/line.svg" alt="15 Stationen in 5 Phasen: Planen, Ausrüsten, Bauen und prüfen, Ausliefern, Betreiben" width="100%">
</p>

Scheitert ein Task dreimal, kommt er zu dir.

## 🎯 Profile

Der Brief legt fest, was gebaut wird. Jedes Profil bringt eigenen Stack, eigene Pflicht-Prüfungen und eine eigene Release-Liste mit. Ein Projekt kann mehrere haben.

| 🌐 [`web-app`](profiles/web-app.md) | 📱 [`iphone-app`](profiles/iphone-app.md) | ⚙️ [`engine`](profiles/engine.md) | 🖥️ [`backend`](profiles/backend.md) |
|:--|:--|:--|:--|
| Websites und Web-Apps | Native iPhone-Apps | Kernlogik ohne Oberfläche | Server, APIs, CLI |

## 🔒 Schalter statt Vertrauen

Die wichtigsten Regeln erzwingt ein kleines Programm, nicht nur eine Anweisung. Solange es nichts blockiert, kostet es keine Tokens.

| | |
|:--|:--|
| 🌿 **Geschützter Hauptzweig**<br>Kein Produktcode direkt auf `main` | 📦 **Task-Bereich**<br>Ein Builder schreibt nur in den Ordnern seines Tasks |
| ✅ **Echte Nachweise**<br>Tests scheitern zuerst und bestehen danach, dazu Typprüfung, Lint und Build, alles aufgezeichnet | 🙋 **Deine Freigabe**<br>Die KI kann sich nicht selbst freigeben |

Dazu kommen ein gesperrter Vertrag für Schnittstellen, eine Grössengrenze pro Task und eine zweite Review bei heiklen Tasks. Details und Grenzen stehen in [`shared/schalter.md`](shared/schalter.md).

## 🤝 Welche KI kann was

| | Claude Code | Cursor | Gemini CLI | Codex | DeepSeek, andere |
|:--|:-:|:-:|:-:|:-:|:-:|
| Anleitung und Skills | ✅ | ✅ | ✅ | ✅ | ✅ |
| Schalter bei jedem Commit | ✅ | ✅ | ✅ | ✅ | ✅ |
| Schalter schon vor dem Schreiben | ✅ | ✅ | ✅ | ✅ | – |
| Freigabe per Nachricht | ✅ | ✅ | ✅ | ✅ | im Terminal |
| Prüfung vor dem Aufhören | ✅ | ✅ | ✅ | ✅ | auf Anweisung |

Jede KI, die `AGENTS.md` liest, kann banan nutzen. Stand der Erprobung in [`shared/schalter.md`](shared/schalter.md).

<details>
<summary><b>📁 Was im Repo liegt</b></summary>
<br>

| Ordner | Inhalt |
|:--|:--|
| [`stations/`](stations) | 15 Stationen, je eine `SKILL.md` |
| [`shared/`](shared) | Regeln für alle Stationen |
| [`memory/`](memory) | Vorlagen fürs Projekt-Gedächtnis |
| [`profiles/`](profiles) | Ein Profil pro Projekttyp |
| [`design/`](design) | Design-Regeln nach Magic UI |
| [`engine/`](engine) | Orchestrator, Rollen, Befehle, Schalter und die Anbindung je KI |
| [`vendor-skills/`](vendor-skills) | Übernommene Skills mit ihren Lizenzen |

`install.sh` kann jederzeit wieder laufen und aktualisiert banan im Projekt. Dein Projekt-Gedächtnis und eigene Einstellungen bleiben erhalten.

</details>

<br>

<p align="center">
  <a href="CHANGELOG.md">Changelog</a> ·
  <a href="shared/versionierung.md">Versionen</a> ·
  vor v1.0.0 Entwicklungsstand
</p>

<p align="center">
  <sub>Skill-Muster aus <a href="https://github.com/anthropics/skills">anthropics/skills</a> · Design-Regeln aus <a href="https://github.com/magicuidesign/magicui">magicuidesign/magicui</a> · Feinschliff aus <a href="https://github.com/emilkowalski/skills">emilkowalski/skills</a></sub>
</p>
