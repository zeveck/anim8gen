# Changelog

anim8gen uses the release date as its version: `vYYYY.M.D` (for example
`v2026.10.11`). A second release on the same day adds `.2`, a third `.3`, and
so on (`v2026.10.11.2`).

The running version is printed by
`python3 <skill-dir>/scripts/skill_paths.py version` and recorded as
`generation.anim8genVersion` in every new package spec.

## v2026.11.1.3

Fix from a third bug review ([#3](https://github.com/zeveck/anim8gen/issues/3)):

- Sprites whose reach sets the scale (a long tail, a swung weapon) are no
  longer cut off at the canvas edge. A tiny rounding error used to skip the
  step that keeps them inside.

## v2026.11.1.2

Fixes from a second bug review ([#2](https://github.com/zeveck/anim8gen/issues/2)):

- A frame that reuses another now follows that frame's retries. Before, after
  a retry it kept the old, rejected pose, so a loop popped back to it.
- The bundle's raw frames come from the same accepted frames as the
  animation, including packages that record them only in `candidates.jsonl`.

## v2026.11.1

Fixes from a bug review ([#1](https://github.com/zeveck/anim8gen/issues/1)):

- The tools no longer crash on Pillow older than 12.1. Before, alignment and
  validation failed after every frame had already been paid for.
- Animations are built from the accepted retry of each frame, never an older
  rejected one, and frames that reuse another frame no longer stop alignment
  or the contact sheet. SKILL.md now shows what `accepted-frames.json` holds.
- Sprites anchored at `body_center` (flames, explosions, projectiles) stay
  inside the canvas instead of losing their top or bottom.

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

- Dev container refreshed from github.com/zeveck/devcontainer-plus (`gh`, `glab`,
  `auth`, `dc`, Node 24). Agent history, memory, settings, and plugins survive
  rebuilds; sign-ins don't, and `dc volumes` manages the saved data.

## Before v2026.10.11

Unversioned releases, installed by copying the skill folder, using
imagegen2's chroma-key transparency.
