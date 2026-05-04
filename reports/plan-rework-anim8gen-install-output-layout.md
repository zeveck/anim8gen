# Plan Report: Rework anim8gen Install and Output Layout

## Phase

Phase 6: Skill and README updates

Status: implemented and verified; landing pending.

## Scope Assessment

Phase 6 was kept to README and skill behavior documentation, plus a focused regression test for the documented output contract. It does not run the final clean-room install verification reserved for Phase 7, and it does not change runtime generation or export code.

## Changes

- Updated README install guidance so a normal install adds skill directories and does not copy the repo-root `anim8gen/` development workbench into user projects.
- Documented the hidden `.anim8gen/runs/<id>/` provenance workspace and visible `assets/anim8gen/<id>/` deliverable bundle.
- Clarified `showit`, `noshow`, and no-flag preview-server behavior in README.
- Fixed the skill preview server URL example to point at exported `preview.html`.
- Added regression coverage for the README/SKILL output contract.
- Marked Phase 6 as `✅ Done` in the plan tracker.

## Tests Run

- `python3 -m py_compile .codex/skills/anim8gen/scripts/*.py .codex/skills/anim8gen/runtime/tools/*.py anim8gen/tools/*.py tests/*.py`
- `python3 tests/test_anim8gen_tools.py`

## Verification Result

Passed. Inline verification covered Python syntax for scripts, installed runtime tools, source tools, and tests, plus the anim8gen regression suite. The new regression confirms README and SKILL.md document the hidden workspace, visible export bundle, precise preview-server flags, and exported `preview.html` URL. Separate verifier assurance was not used because this runner-managed chunk did not explicitly authorize sub-agent delegation.

## Landing Result

Pending. The Phase 6 worktree change has not been committed or cherry-picked yet.

## Remaining Phases

- Phase 7: Tests and clean-room verification
