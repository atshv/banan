---
name: factory-neu
description: Richtet die Software Factory in einem neuen oder bestehenden Projektordner ein. Nur auf Befehl, mit dem Zielordner als Argument, z. B. /factory-neu ~/Projekte/meine-app
disable-model-invocation: true
---

# Factory in ein Projekt installieren

1. Zielordner ist `$ARGUMENTS`. Fehlt er, frag danach.
2. Führe im Factory-Ordner `./install.sh "<Zielordner>" <KI>` aus. Nennt der Auftraggeber keine KI, lass sie weg, dann gilt Claude Code.
3. Sag dem Auftraggeber in zwei Sätzen, was installiert wurde, und dass er im Zielordner Claude Code startet und `/factory-start` eingibt.
