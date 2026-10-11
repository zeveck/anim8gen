#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

SRC_SKILLS="$ROOT/.codex/skills"
DST_SKILLS="$CODEX_HOME/skills"

if [ ! -d "$SRC_SKILLS" ]; then
  echo "ERROR: missing vendored skills at $SRC_SKILLS" >&2
  exit 1
fi

mkdir -p "$DST_SKILLS"

for skill_path in "$SRC_SKILLS"/*; do
  [ -d "$skill_path" ] || continue
  name=$(basename "$skill_path")
  rm -rf "$DST_SKILLS/$name"
  cp -R "$skill_path" "$DST_SKILLS/$name"
done

python3 - "$CODEX_HOME" <<'PY'
from pathlib import Path
import sys

codex_home = sys.argv[1].rstrip("/")
roots = [Path(codex_home) / "skills"]
for root in roots:
    if not root.exists():
        continue
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            data = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = data.replace("/home/vscode/.codex", codex_home)
        if updated != data:
            path.write_text(updated, encoding="utf-8")
PY

# anim8gen requires imagegen2 but no longer vendors it. Install the current
# release's Codex skill so this checkout works out of the box. Non-fatal: a
# network failure should not block the rest of the container setup.
IMAGEGEN2_REPO="${IMAGEGEN2_REPO:-https://github.com/zeveck/imagegen2.git}"
tmp=$(mktemp -d)
if git clone -q --depth 1 "$IMAGEGEN2_REPO" "$tmp/imagegen2" 2>/dev/null \
  && [ -f "$tmp/imagegen2/.codex/skills/imagegen2/generate.cjs" ]; then
  rm -rf "$DST_SKILLS/imagegen2"
  cp -R "$tmp/imagegen2/.codex/skills/imagegen2" "$DST_SKILLS/imagegen2"
  echo "Installed imagegen2 Codex skill from $IMAGEGEN2_REPO"
else
  echo "WARNING: could not install imagegen2 from $IMAGEGEN2_REPO; install it before running anim8gen." >&2
fi
rm -rf "$tmp"

count=$(find "$SRC_SKILLS" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')
echo "Installed $count vendored Codex skills into $CODEX_HOME"
echo "Restart Codex to pick up skill metadata changes."
