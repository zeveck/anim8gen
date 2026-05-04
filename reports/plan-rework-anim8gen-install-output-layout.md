# Plan Report: Rework anim8gen Install and Output Layout

## Phase

Phase 4: Visible export step

Status: implemented, verified, and landed.

## Scope Assessment

Phase 4 was kept to the visible deliverable export boundary. The change adds an explicit export helper that packages aligned frames, a static preview, optional GIF output, and conditional raw candidates under `assets/anim8gen/<id>/`. It also fixes preview frame URLs so exported previews use paths relative to their own folder. It does not clean demo specs/reports, rewrite README install behavior, or run the final clean-room verification reserved for later phases.

## Changes

- Added `export_bundle.py` to the source tools and installed skill runtime tools.
- Registered `export-bundle` in `skill_paths.py`.
- Updated preview payload generation to compute frame URLs relative to the preview output file rather than assuming a shared two-level workspace layout.
- Updated the anim8gen skill workflow to run the visible export step and serve `assets/anim8gen/<id>/preview.html` when preview display is requested.
- Added regression coverage for export-local preview paths, clean visible bundles without manifests/reports, optional GIF export, and conditional raw export when accepted raw candidates differ from aligned frames.
- Marked Phase 4 as `✅ Done` in the plan tracker.

## Tests Run

- `python3 -m py_compile .codex/skills/anim8gen/scripts/*.py .codex/skills/anim8gen/runtime/tools/*.py anim8gen/tools/*.py tests/*.py`
- `python3 tests/test_anim8gen_tools.py`

## Verification Result

Passed. Inline verification covered Python syntax for scripts, installed runtime tools, source tools, and tests, plus the anim8gen regression suite. The new tests verify the visible bundle contains frames, `preview.html`, and GIF output without internal manifests or reports; exported previews reference `frames/...`; raw candidates stay hidden when visually equivalent and are exported when they differ. Separate verifier assurance was not used because this runner-managed chunk did not explicitly authorize sub-agent delegation.

## Landing Result

Landed. Worktree commit `940043d` was cherry-picked to `main` as `e985142`.

## Remaining Phases

- Phase 5: Demo/repo surface cleanup
- Phase 6: Skill and README updates
- Phase 7: Tests and clean-room verification
