---
name: doku-writer
description: Hält README, Setup-Anleitung und Changelog aktuell. Nutze diesen Skill bei jedem Release und immer, wenn sich Startbefehle, Umgebungsvariablen oder Funktionen ändern.
---

# 14 Doku-Writer

Gute Doku spart beim nächsten Projekt und beim nächsten Agent viel Zeit, denn sie müssen nichts erraten.

## Input
- `handoffs/06-setup.md`, Release-Bericht, Task-Berichte

## Ablauf
1. README: Was ist das, wie starte ich es, wie teste ich es.
2. Changelog: Was ist neu, was ist behoben, in Nutzersprache. Format und Abschnitte nach `shared/versionierung.md`, neue Einträge zuerst unter `[Unreleased]`.
3. Umgebungsvariablen nur mit Namen und Zweck, nie mit Werten.
4. Reader-Test: Ein frischer Agent ohne Vorwissen versucht, das Projekt nur mit der Doku zu starten. Wo er hängt, wird nachgebessert.

## Output
- `README.md`, `CHANGELOG.md` im Projekt-Repo

## Gate
- Reader-Test bestanden.

## Nutzt
`doc-coauthoring` (Reader Testing), `docx`, `pdf` (falls Doku als Datei gebraucht wird)
