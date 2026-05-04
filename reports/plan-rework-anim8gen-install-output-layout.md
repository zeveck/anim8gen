# Plan Report: Rework anim8gen Install and Output Layout

## Phase

Phase 1: Path model and runtime boundaries

Status: implemented, verified, and landed.

## Scope Assessment

Phase 1 was kept to the path model boundary. The change adds a reusable helper for resolving project root, hidden workspace root, run root, temp scratch root, visible export root, runtime tool root, and explicit legacy spec paths. It does not move package initialization defaults or rewrite the skill workflow, which remain Phase 2 and Phase 6 work.

## Changes

- Added `.codex/skills/anim8gen/scripts/layout_paths.py` with default hidden workspace, visible export, temp scratch, runtime tool, and legacy spec resolution.
- Updated `.codex/skills/anim8gen/scripts/skill_paths.py` to expose the layout-derived runtime tool root.
- Added regression tests for default layout, environment overrides, temp scratch placement outside the project, and explicit legacy spec lookup.
- Marked Phase 1 as `✅ Done` in the plan tracker.

## Tests Run

- `python3 -m py_compile .codex/skills/anim8gen/scripts/*.py anim8gen/tools/*.py tests/*.py`
- `python3 tests/test_anim8gen_tools.py`
- `python3 .codex/skills/anim8gen/scripts/layout_paths.py trex-roar-v1 --project-root /tmp/example-client --json`
- `python3 .codex/skills/anim8gen/scripts/skill_paths.py runtime-tools --start /tmp/example-client --animation-id trex-roar-v1`

## Verification Result

Passed. Inline verification covered the new helper behavior and existing anim8gen tool regressions. Separate verifier assurance was not used because this runner-managed chunk did not explicitly authorize sub-agent delegation.

## Landing Result

Landed. Worktree commit `d6ead9e` was cherry-picked to `main` as `fea1dd8`.

## Remaining Phases

- Phase 2: Package initialization root fixes
- Phase 3: Tooling install boundary
- Phase 4: Visible export step
- Phase 5: Demo/repo surface cleanup
- Phase 6: Skill and README updates
- Phase 7: Tests and clean-room verification
