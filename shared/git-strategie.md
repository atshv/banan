# Git-Strategie

Git ist das Sicherheitsnetz, wenn man den Code nicht selbst lesen kann. Jeder Schritt ist umkehrbar.

## Regeln
- `main` ist immer lauffähig. Niemand arbeitet direkt auf `main`.
- Ein Branch pro Task: `task/T-<Nr>-<kurzname>`.
- Commit-Nachricht beginnt mit der Task-Nummer: `T-12: Login-Formular`.
- Zusammenführen nur nach bestandenem Tester-, Reviewer- und Security-Gate.
- Jedes Release bekommt einen Tag: `v<Major>.<Minor>.<Patch>`.

## Rollback
- Einzelner Task: `git revert <Merge-Commit>`
- Ganzes Release: auf den letzten Tag zurück deployen.
- Der Rollback-Befehl steht in jedem Release-Bericht.
