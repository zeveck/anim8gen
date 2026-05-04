# Plan Report: Rework anim8gen Install and Output Layout

## Phase

Phase 5: Demo/repo surface cleanup

Status: implemented and verified; landing pending.

## Scope Assessment

Phase 5 was kept to the repository and demo surface. The change moves source demo specs out of the installable `anim8gen/config` path, moves source-owned runtime templates under `anim8gen/runtime/config`, removes tracked old report files from `anim8gen/reports`, and leaves the committed `public/demos/**` and `public/media/**` gallery intact. It does not rewrite README or skill behavior, and it does not run the final clean-room install verification reserved for later phases.

## Changes

- Moved retained demo/source specs to `examples/specs/`.
- Moved repo-local config templates to `anim8gen/runtime/config/`.
- Updated the moved source template to use `.anim8gen/runs/<id>/...` defaults instead of old visible workbench paths.
- Removed tracked old report files from `anim8gen/reports/`.
- Added regression coverage that the repo demo specs are outside the installable workbench, the old source config/report directories are absent, and source runtime templates do not point at `anim8gen/assets`.
- Marked Phase 5 as `✅ Done` in the plan tracker.

## Tests Run

- `python3 -m py_compile .codex/skills/anim8gen/scripts/*.py .codex/skills/anim8gen/runtime/tools/*.py anim8gen/tools/*.py tests/*.py`
- `python3 tests/test_anim8gen_tools.py`

## Verification Result

Passed. Inline verification covered Python syntax for scripts, installed runtime tools, source tools, and tests, plus the anim8gen regression suite. The new regression confirms `anim8gen/config` and `anim8gen/reports` are absent from the source tree, retained source specs live under `examples/specs`, and repo-local runtime templates use the hidden workspace layout. Separate verifier assurance was not used because this runner-managed chunk did not explicitly authorize sub-agent delegation.

## Landing Result

Pending. The phase is ready to commit in the cherry-pick worktree and cherry-pick to `main`.

## Remaining Phases

- Phase 6: Skill and README updates
- Phase 7: Tests and clean-room verification
