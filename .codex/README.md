# Project Codex Skills

`.codex/skills/anim8gen/` is the anim8gen skill itself. The same folder is the
skill in the Claude Code plugin (see `.claude-plugin/plugin.json`).

Codex discovers active skills from `${CODEX_HOME:-$HOME/.codex}/skills`, so a
fresh clone still needs to install the skill into the local Codex home:

```bash
bash scripts/install-codex-skills.sh
```

The script also installs the current imagegen2 Codex skill from
github.com/zeveck/imagegen2 (override with `IMAGEGEN2_REPO`), because anim8gen
requires imagegen2 but does not vendor it. The devcontainer setup runs the
script automatically.

The install script overwrites matching project-owned skill directories in
`CODEX_HOME` and preserves unrelated skills.
