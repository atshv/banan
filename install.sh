#!/usr/bin/env bash
# Installiert banan in einen Projektordner.
#
#   ./install.sh <Projektordner> [KI]
#
# KI ist eine oder mehrere von: claude, cursor, gemini, codex, deepseek, andere
# Mehrere mit Komma, z. B. cursor,codex. Ohne Angabe: claude.
# "deepseek" und "andere" bekommen AGENTS.md, Skills und die Git-Schalter, aber keine eigenen Hooks.
#
# Mehrfach aufrufbar. Aktualisiert banan, lässt Projekt-Gedächtnis und eigene Einstellungen in Ruhe.
set -euo pipefail

FACTORY="$(cd "$(dirname "$0")" && pwd)"
ENGINE="$FACTORY/engine"

if [ $# -lt 1 ] || [ $# -gt 2 ]; then
  echo "Aufruf: ./install.sh <Projektordner> [claude,cursor,gemini,codex,deepseek,andere]" >&2
  exit 1
fi

KIS="${2:-claude}"
for ki in ${KIS//,/ }; do
  case "$ki" in
    claude|cursor|gemini|codex|deepseek|andere) ;;
    *) echo "Unbekannte KI: $ki. Erlaubt: claude, cursor, gemini, codex, deepseek, andere" >&2; exit 1 ;;
  esac
done
has() { case ",$KIS," in *",$1,"*) return 0 ;; *) return 1 ;; esac; }

mkdir -p "$1"
ZIEL="$(cd "$1" && pwd)"
if [ "$ZIEL" = "$FACTORY" ]; then
  echo "Der Projektordner darf nicht banan selbst sein." >&2
  exit 1
fi

HAT_PYTHON=1
command -v python3 >/dev/null 2>&1 || HAT_PYTHON=0

skill_name() { sed -n 's/^name:[[:space:]]*//p' "$1/SKILL.md" | head -n 1; }

copy_skills() { # $1 = Zielordner für Skills
  local ziel="$1" d name
  mkdir -p "$ziel"
  for d in "$FACTORY"/stations/*/ "$FACTORY"/vendor-skills/anthropic/*/ "$FACTORY"/vendor-skills/emilkowalski/*/ \
           "$FACTORY"/vendor-skills/magic-ui/ "$ENGINE"/skills/*/; do
    d="${d%/}"
    [ -f "$d/SKILL.md" ] || continue
    name="$(skill_name "$d")"
    [ -n "$name" ] || { echo "Kein Name in $d/SKILL.md" >&2; exit 1; }
    rm -rf "${ziel:?}/$name"
    cp -R "$d" "$ziel/$name"
  done
}

settings() { # $1 = Vorlage von banan, $2 = Datei im Projekt
  mkdir -p "$(dirname "$2")"
  if [ ! -f "$2" ]; then
    cp "$1" "$2"
  elif [ "$HAT_PYTHON" = 1 ]; then
    python3 "$ENGINE/merge_settings.py" "$1" "$2"
  else
    echo "Achtung: ${2#"$ZIEL"/} nicht aktualisiert, weil python3 fehlt." >&2
  fi
}

ensure_import() { # sorgt dafür, dass die Datei $1 auf AGENTS.md verweist
  if [ ! -f "$1" ]; then
    printf '@AGENTS.md\n' > "$1"
  elif ! grep -qxF '@AGENTS.md' "$1"; then
    printf '\n@AGENTS.md\n' >> "$1"
  fi
}

START="<!-- software-factory:start -->"
ENDE="<!-- software-factory:end -->"
strip_section() { # entfernt den banan-Abschnitt aus $1
  local tmp; tmp="$(mktemp)"
  awk -v s="$START" -v e="$ENDE" '$0 == s { skip = 1; next } $0 == e { skip = 0; next } !skip { print }' "$1" > "$tmp"
  mv "$tmp" "$1"
}

# ---------- Für jede KI gleich ----------

# Schalter und Werkzeuge
rm -rf "$ZIEL/.banan"
mkdir -p "$ZIEL/.banan/rollen"
cp -R "$ENGINE"/banan/. "$ZIEL/.banan/"
find "$ZIEL/.banan" -name "__pycache__" -prune -exec rm -rf {} +
chmod +x "$ZIEL/.banan/githooks/pre-commit"
for f in "$ENGINE"/agents/*.md; do  # Rollen ohne den Kopf, der nur für Claude Code gilt
  awk 'NR == 1 && $0 == "---" { skip = 1; next } skip && $0 == "---" { skip = 0; next } !skip { print }' \
    "$f" > "$ZIEL/.banan/rollen/$(basename "$f")"
done
cp "$FACTORY/VERSION" "$ZIEL/.banan/VERSION"

# Regeln, Design und Profile
rm -rf "$ZIEL/factory"
mkdir -p "$ZIEL/factory"
cp -R "$FACTORY/shared" "$FACTORY/design" "$FACTORY/profiles" "$ZIEL/factory/"

# Projekt-Gedächtnis nur anlegen, nie überschreiben
mkdir -p "$ZIEL/memory/handoffs/tasks"
for f in "$FACTORY"/memory/*.md "$FACTORY"/memory/gates.json "$FACTORY"/memory/handoffs/README.md; do
  rel="${f#"$FACTORY"/}"
  [ -f "$ZIEL/$rel" ] || cp "$f" "$ZIEL/$rel"
done

# AGENTS.md anlegen oder den banan-Abschnitt ersetzen
if [ -f "$ZIEL/AGENTS.md" ] && grep -qF "$START" "$ZIEL/AGENTS.md"; then
  strip_section "$ZIEL/AGENTS.md"
fi
if [ -s "$ZIEL/AGENTS.md" ]; then
  { echo; cat "$ENGINE/AGENTS.md"; } >> "$ZIEL/AGENTS.md"
else
  cp "$ENGINE/AGENTS.md" "$ZIEL/AGENTS.md"
fi

# Git-Schalter: gelten für jeden Commit, egal welche KI ihn macht
if command -v git >/dev/null 2>&1; then
  [ -d "$ZIEL/.git" ] || git -C "$ZIEL" init -q -b main
  ALT="$(git -C "$ZIEL" config --get core.hooksPath || true)"
  if [ -z "$ALT" ] || [ "$ALT" = ".banan/githooks" ]; then
    git -C "$ZIEL" config core.hooksPath .banan/githooks
  else
    echo "Achtung: Das Projekt nutzt schon eigene Git-Hooks ($ALT). Der Git-Schalter von banan ist nicht aktiv." >&2
  fi
else
  echo "Achtung: git fehlt. Ohne Git laufen die Schalter von banan nicht." >&2
fi
[ "$HAT_PYTHON" = 1 ] || echo "Achtung: python3 fehlt. Die Schalter laufen erst, wenn python3 installiert ist." >&2

# ---------- Je KI ----------

if has claude; then
  copy_skills "$ZIEL/.claude/skills"
  mkdir -p "$ZIEL/.claude/agents"
  cp "$ENGINE"/agents/*.md "$ZIEL/.claude/agents/"
  rm -rf "$ZIEL/.claude/hooks"  # Ort der Schalter vor 0.0.8
  settings "$ENGINE/adapter/claude/settings.json" "$ZIEL/.claude/settings.json"
  if [ -f "$ZIEL/CLAUDE.md" ] && grep -qF "$START" "$ZIEL/CLAUDE.md"; then
    strip_section "$ZIEL/CLAUDE.md"  # stand vor 0.0.8 hier, jetzt in AGENTS.md
  fi
  ensure_import "$ZIEL/CLAUDE.md"
fi

if has cursor || has gemini || has codex || has deepseek || has andere; then
  copy_skills "$ZIEL/.agents/skills"
fi
if has cursor; then settings "$ENGINE/adapter/cursor/hooks.json" "$ZIEL/.cursor/hooks.json"; fi
if has codex; then settings "$ENGINE/adapter/codex/hooks.json" "$ZIEL/.codex/hooks.json"; fi
if has gemini; then
  settings "$ENGINE/adapter/gemini/settings.json" "$ZIEL/.gemini/settings.json"
  ensure_import "$ZIEL/GEMINI.md"
fi

echo "banan $(cat "$FACTORY/VERSION") installiert in $ZIEL für: $KIS"
if has claude; then
  echo "Nächster Schritt: in diesem Ordner deine KI starten und /factory-start eingeben."
else
  echo "Nächster Schritt: in diesem Ordner deine KI starten und 'factory start' schreiben."
fi
if has codex; then echo "Codex: die Schalter einmal mit /hooks ansehen und bestätigen, sonst laufen sie nicht."; fi
