#!/usr/bin/env bash
set -euo pipefail

start_dir="${1:-$PWD}"
dir=$(cd "$start_dir" && pwd)

while [ "$dir" != "/" ]; do
  if [ -d "$dir/anim8gen" ] && [ -d "$dir/.codex/skills/anim8gen" ]; then
    repo_root="$dir"
    break
  fi
  dir=$(dirname "$dir")
done

if [ -z "${repo_root:-}" ]; then
  echo "ERROR: could not find repo root containing anim8gen/ and .codex/skills/anim8gen/" >&2
  exit 1
fi

imagegen2_cli=""
for candidate in \
  "$repo_root/.codex/skills/imagegen2/generate.cjs" \
  "${CODEX_HOME:-$HOME/.codex}/skills/imagegen2/generate.cjs"; do
  if [ -s "$candidate" ]; then
    imagegen2_cli="$candidate"
    break
  fi
done

if [ -z "$imagegen2_cli" ]; then
  echo "ERROR: could not find imagegen2 generate.cjs" >&2
  exit 1
fi

printf 'repo root: %s\n' "$repo_root"
printf 'imagegen2 cli: %s\n' "$imagegen2_cli"
