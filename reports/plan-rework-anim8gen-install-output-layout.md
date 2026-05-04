# Plan Report: Rework anim8gen Install and Output Layout

## Phase

Phase 3: Tooling install boundary

Status: implemented, verified, and landed.

## Scope Assessment

Phase 3 was kept to the install/runtime boundary. The change bundles the normal runtime tools and minimal config templates inside the anim8gen skill, teaches `skill_paths.py` to resolve those bundled files from an installed copy, and removes skill instructions that depended on a visible repo-root `anim8gen/` workbench. It does not add the final visible export step, clean this repo's demo surface, or complete the clean-room end-to-end verification reserved for later phases.

## Changes

- Added `.codex/skills/anim8gen/runtime/tools/` with the runtime commands needed by installed anim8gen runs.
- Added `.codex/skills/anim8gen/runtime/config/` with only `brief.schema.json` and `template.animation-spec.json`.
- Updated `.codex/skills/anim8gen/scripts/skill_paths.py` so installed copies can resolve bundled tools and config without hard-coded `.codex`, `.claude`, or repo-root workbench paths.
- Updated the anim8gen skill and prompting reference to point at hidden `.anim8gen/runs/<id>` state and bundled runtime tools instead of `anim8gen/tools` and `anim8gen/assets`.
- Added regression coverage that copies the installed skill to a temp location, resolves a bundled tool, and verifies no visible `anim8gen/` directory is created.
- Marked Phase 3 as `✅ Done` in the plan tracker.

## Tests Run

- `python3 -m py_compile .codex/skills/anim8gen/scripts/*.py .codex/skills/anim8gen/runtime/tools/*.py anim8gen/tools/*.py tests/*.py`
- `python3 tests/test_anim8gen_tools.py`

## Verification Result

Passed. Inline verification covered Python syntax for scripts, bundled runtime tools, source tools, and tests, plus the anim8gen regression suite. The new tests verify the runtime bundle contents, exclude development/demo-only files from the installed runtime package, and prove `skill_paths.py` resolves bundled tools from a copied skill without creating a visible project-root `anim8gen/` directory. Separate verifier assurance was not used because this runner-managed chunk did not explicitly authorize sub-agent delegation.

## Landing Result

Landed. Worktree commit `ea47204` was cherry-picked to `main` as `c6f3ecd`.

## Remaining Phases

- Phase 4: Visible export step
- Phase 5: Demo/repo surface cleanup
- Phase 6: Skill and README updates
- Phase 7: Tests and clean-room verification
