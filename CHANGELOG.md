# Changelog

anim8gen uses date-based versions: `vYYYY.M.D` (for example `v2026.10.11`),
which are also valid semver. For a second release on the same day, use the next
day's date rather than a `-1` suffix, because semver sorts `2026.10.11-1`
before `2026.10.11`.

The running version is printed by
`python3 <skill-dir>/scripts/skill_paths.py version` and recorded as
`generation.anim8genVersion` in every new package spec.

## v2026.10.11

### Claude Code plugin

- anim8gen is now a Claude Code plugin with its own marketplace. It declares
  imagegen2 as a dependency, so installing anim8gen also installs imagegen2
  once the imagegen2 marketplace is added:
  `/plugin marketplace add zeveck/imagegen2`, then
  `/plugin install anim8gen --marketplace zeveck/anim8gen`. The plugin is
  rooted at `.codex/skills/`, so an install copies only the skill, not the
  repository.
- anim8gen now finds imagegen2 when it is installed as a Claude Code plugin.
  `python3 <skill-dir>/scripts/skill_paths.py imagegen2-info` prints which imagegen2 it
  found, where, its version, and the model this project will use. A managed
  plugin install wins over an old copied `~/.claude/skills/imagegen2`;
  `IMAGEGEN2_CLI` names an exact copy to use.
- This repository no longer vendors imagegen2, imagegen, or nanogen. The
  vendored imagegen2 was an old build, and as a sibling of the anim8gen skill
  it shadowed whatever imagegen2 the user installed. The Codex install script
  fetches the current imagegen2 Codex skill instead.

### Native transparency

- New sprite packages use imagegen2's native alpha (GPT Image 2.5) when the
  project's imagegen2 and model support it: frames are requested "isolated
  on a transparent background" with `--transparent-mode native-alpha` and
  aligned by alpha only. Soft edges such as fire, smoke, glow, and fur no
  longer pick up key-color fringes, subject colors close to the key (magenta
  magic, green slime) are no longer cut out, and detached sparks, embers, and
  smoke puffs of at least 16 source pixels (`segmentation.minDetachedPixels`)
  are kept instead of dropped.
- `init-package` decides with an imagegen2 dry run in the project, so it
  picks chroma-key when the project's imagegen2 or model can't produce native
  alpha: imagegen2 releases before v2026.10.11, or a pinned model without
  native alpha (`IMAGEGEN2_MODEL=gpt-image-2`).
  Set the brief's `segmentation` to `chroma-key` or `native-alpha` to choose
  explicitly. Existing packages keep the segmentation recorded in their spec.
- Reference preparation no longer strips key-colored pixels from references
  in native-alpha packages.
- SKILL.md now runs every command from the project root and calls helpers by
  the skill's absolute path. The old "cd into the skill folder" instructions
  could write packages into the skill's own folder, which a plugin update
  replaces.

### Also

- Dev container refreshed from github.com/zeveck/devcontainers (`gh`, `glab`,
  `auth`, `dc`, Node 24, and agent sign-ins and history that survive
  rebuilds).

## Before v2026.10.11

Unversioned releases, installed by copying the skill folder, using
imagegen2's chroma-key transparency.
