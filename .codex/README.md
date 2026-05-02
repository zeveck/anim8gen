# Project Codex Skills

This directory vendors the Codex skills this project depends on.

Codex discovers active skills from `${CODEX_HOME:-$HOME/.codex}/skills`, so a
fresh clone still needs to install these vendored copies into the local Codex
home:

```bash
bash scripts/install-codex-skills.sh
```

The devcontainer setup runs that script automatically.

The vendored `.codex/skills/` tree intentionally excludes the built-in
`.system` skills. The install script overwrites matching project-owned skill
directories in `CODEX_HOME` and preserves unrelated skills.
