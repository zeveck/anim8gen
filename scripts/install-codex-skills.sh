#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

SRC_SKILLS="$ROOT/.codex/skills"
SRC_SUPPORT="$ROOT/.codex/zskills-support"
DST_SKILLS="$CODEX_HOME/skills"
DST_SUPPORT="$CODEX_HOME/zskills-support"

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

if [ -d "$SRC_SUPPORT" ]; then
  rm -rf "$DST_SUPPORT"
  mkdir -p "$CODEX_HOME"
  cp -R "$SRC_SUPPORT" "$DST_SUPPORT"
fi

python3 - "$CODEX_HOME" <<'PY'
from pathlib import Path
import sys

codex_home = sys.argv[1].rstrip("/")
roots = [Path(codex_home) / "skills", Path(codex_home) / "zskills-support"]
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

count=$(find "$SRC_SKILLS" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')
echo "Installed $count vendored Codex skills into $CODEX_HOME"
echo "Restart Codex to pick up skill metadata changes."
