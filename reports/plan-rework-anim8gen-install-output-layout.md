# Plan Report: Rework anim8gen Install and Output Layout

## Phase

Phase 7: Tests and clean-room verification

Status: implemented and verified; landing pending.

## Scope Assessment

Phase 7 was limited to automated regression coverage and a synthetic clean-room package pipeline. The only runtime change fixes the local synthetic-frame helper so the documented `--root .anim8gen/runs/<id>` smoke-test command writes into the hidden run workspace instead of the old visible workbench shape. It does not change live image generation or package quality rules.

## Changes

- Added regression coverage that generated new specs and manifests avoid `anim8gen/assets`, `anim8gen/config`, `anim8gen/preview`, and `anim8gen/reports` paths.
- Added coverage that an explicit visible `anim8gen/<id>` export root contains result files only, without tools, config, manifests, or reports.
- Added a complete synthetic run test that initializes a hidden package, creates synthetic raw frames, aligns, validates, builds a contact sheet, builds a hidden preview, exports a GIF, exports the visible bundle, and confirms no visible repo-root `anim8gen/` workbench is created.
- Fixed `create_synthetic_frames.py` to infer or accept a hidden run root and write `raw/`, `manifests/`, and `review/` directly under that root.
- Marked Phase 7 as `✅ Done` in the plan tracker.

## Tests Run

- `python3 -m py_compile .codex/skills/anim8gen/scripts/*.py .codex/skills/anim8gen/runtime/tools/*.py anim8gen/tools/*.py tests/*.py`
- `python3 tests/test_anim8gen_tools.py`

## Verification Result

Passed. Inline verification covered Python syntax for skill scripts, installed runtime tools, source tools, and tests, plus the anim8gen regression suite. The new synthetic clean-room test exercises the full local package pipeline without starting a preview server and verifies the hidden workspace and visible bundle contract. Separate verifier assurance was not used because this runner-managed chunk did not explicitly authorize sub-agent delegation.

## Landing Result

Pending. The Phase 7 worktree changes have not yet been committed or cherry-picked to `main`.

## Remaining Phases

- None.
