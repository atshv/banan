---
name: security-check
description: Sucht nach Secrets, API-Keys, unsicheren Abhängigkeiten und offenen Angriffsflächen. Nutze diesen Skill nach dem Review jedes Tasks und vor jedem Release, besonders wenn Login, Zahlungen, Nutzerdaten oder externe APIs im Spiel sind.
---

# 12 Security-Check

Ein einziger Key im Code kann teuer werden. Dieser Check ist billig, ein Leck nicht.

## Input
- Diff des Task-Branches, `package.json` oder entsprechende Abhängigkeitsdatei

## Ablauf
1. Secrets suchen: Keys, Tokens, Passwörter, private URLs im Code und in der Git-Historie.
2. Abhängigkeiten prüfen (z. B. `npm audit`), bekannte Lücken melden.
3. Eingaben prüfen: Werden Nutzereingaben validiert? Keine gefährlichen HTML-Einfügungen.
4. Rechte prüfen: Sind Daten nur für Berechtigte sichtbar?
5. Externe Links mit `rel="noopener"`, keine unnötigen Berechtigungen in Apps.

## Output → `handoffs/tasks/T-<Nr>-security.md`
```
Ergebnis: OK | blockiert · Funde (Schwere, Datei, Was, Empfehlung)
```

## Gate
- Keine Secrets im Code.
- Keine kritischen oder hohen Lücken in Abhängigkeiten.
