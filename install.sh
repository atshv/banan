#!/usr/bin/env bash
# Installiert die Software Factory mit dem Claude-Code-Motor in einen Projektordner.
# Aufruf: ./install.sh <Projektordner>
# Mehrfach aufrufbar. Aktualisiert Factory-Dateien, lässt Projekt-Gedächtnis und eigene Dateien in Ruhe.
set -euo pipefail

FACTORY="$(cd "$(dirname "$0")" && pwd)"
ENGINE="$FACTORY/engine/claude-code"

if [ $# -ne 1 ]; then
  echo "Aufruf: ./install.sh <Projektordner>" >&2
  exit 1
fi

mkdir -p "$1"
ZIEL="$(cd "$1" && pwd)"

if [ "$ZIEL" = "$FACTORY" ]; then
  echo "Der Projektordner darf nicht die Factory selbst sein." >&2
  exit 1
fi

skill_name() {
  sed -n 's/^name:[[:space:]]*//p' "$1/SKILL.md" | head -n 1
}

copy_skill() {
  local quelle="$1" name
  [ -f "$quelle/SKILL.md" ] || return 0
  name="$(skill_name "$quelle")"
  [ -n "$name" ] || { echo "Kein Name in $quelle/SKILL.md" >&2; exit 1; }
  rm -rf "$ZIEL/.claude/skills/$name"
  cp -R "$quelle" "$ZIEL/.claude/skills/$name"
}

mkdir -p "$ZIEL/.claude/skills" "$ZIEL/.claude/agents"

# Stationen und übernommene Skills
for d in "$FACTORY"/stations/*/ "$FACTORY"/vendor-skills/anthropic/*/ "$FACTORY"/vendor-skills/magic-ui/; do
  copy_skill "${d%/}"
done

# Befehle und Sub-Agents
for d in "$ENGINE"/.claude/skills/*/; do
  copy_skill "${d%/}"
done
cp "$ENGINE"/.claude/agents/*.md "$ZIEL/.claude/agents/"

# Schalter (Hooks). Sie brauchen python3.
mkdir -p "$ZIEL/.claude/hooks"
cp "$ENGINE"/.claude/hooks/*.py "$ZIEL/.claude/hooks/"
if ! command -v python3 >/dev/null 2>&1; then
  echo "Achtung: python3 fehlt. Die Schalter der Factory laufen erst, wenn python3 installiert ist." >&2
fi

# Sperren und Schalter anlegen oder in bestehende Einstellungen einfügen
if [ ! -f "$ZIEL/.claude/settings.json" ]; then
  cp "$ENGINE/.claude/settings.json" "$ZIEL/.claude/settings.json"
elif command -v python3 >/dev/null 2>&1; then
  python3 "$ENGINE/merge_settings.py" "$ENGINE/.claude/settings.json" "$ZIEL/.claude/settings.json"
else
  echo "Achtung: .claude/settings.json nicht aktualisiert, weil python3 fehlt." >&2
fi

# Regeln und Design gehören der Factory und werden aktualisiert
rm -rf "$ZIEL/factory"
mkdir -p "$ZIEL/factory"
cp -R "$FACTORY/shared" "$FACTORY/design" "$ZIEL/factory/"
cp "$FACTORY/VERSION" "$ZIEL/factory/FACTORY_VERSION"

# Projekt-Gedächtnis nur anlegen, nie überschreiben
mkdir -p "$ZIEL/memory/handoffs/tasks"
for f in "$FACTORY"/memory/*.md "$FACTORY"/memory/handoffs/README.md; do
  rel="${f#"$FACTORY"/}"
  [ -f "$ZIEL/$rel" ] || cp "$f" "$ZIEL/$rel"
done

# CLAUDE.md anlegen oder den Factory-Abschnitt ersetzen
START="<!-- software-factory:start -->"
ENDE="<!-- software-factory:end -->"
if [ ! -f "$ZIEL/CLAUDE.md" ]; then
  cp "$ENGINE/CLAUDE.md" "$ZIEL/CLAUDE.md"
elif grep -qF "$START" "$ZIEL/CLAUDE.md"; then
  tmp="$(mktemp)"
  awk -v s="$START" -v e="$ENDE" -v neu="$ENGINE/CLAUDE.md" '
    $0 == s { while ((getline line < neu) > 0) print line; skip = 1; next }
    $0 == e { skip = 0; next }
    !skip { print }
  ' "$ZIEL/CLAUDE.md" > "$tmp"
  mv "$tmp" "$ZIEL/CLAUDE.md"
else
  { echo; cat "$ENGINE/CLAUDE.md"; } >> "$ZIEL/CLAUDE.md"
fi

echo "Software Factory $(cat "$FACTORY/VERSION") installiert in $ZIEL"
echo "Nächster Schritt: in diesem Ordner Claude Code starten und /factory-start eingeben."
