# Quality Gates

Eine Station gilt erst als fertig, wenn ihr Gate bestanden ist. Das Gate steht in jeder SKILL.md unter „Gate“.

## Immer gültig
- Nur weiter bei Grün. Kein „fast fertig“.
- Der Prüfer ist nie der Ersteller.
- Ein Gate wird mit Beweis bestanden (Testausgabe, Screenshot, Link), nicht mit einer Behauptung.

## Pro Task
| Gate | Wer prüft | Beweis |
|---|---|---|
| Lint und Start | Builder | Lint-Ausgabe |
| Tests grün | Tester | Testausgabe, Screenshots |
| Review OK | Reviewer | Review-Bericht ohne blockierende Befunde |
| Security OK | Security-Check | Bericht ohne kritische Funde |

## Pro Release
- Ganze Testsuite auf dem Hauptbranch grün
- Rollback dokumentiert
- Freigabe durch den Auftraggeber
