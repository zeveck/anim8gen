# Plan Report: Rework anim8gen Install and Output Layout

## Phase

Phase 2: Package initialization root fixes

Status: implemented, verified, and landed.

## Scope Assessment

Phase 2 was kept to package initialization. The change updates the initializer to use the Phase 1 layout helper for new runs, keeps `--root` as a deprecated run-root alias, and makes generated spec and manifest paths self-consistent with the selected hidden run root. It does not move install artifacts, add the export helper, clean demo files, or rewrite README/SKILL behavior.

## Changes

- Updated `.codex/skills/anim8gen/scripts/init_package.py` with `--project-root`, `--workspace-root`, and `--export-root` options.
- Changed the default initializer output to `.anim8gen/runs/<id>/**` with visible export metadata pointing at `assets/anim8gen/<id>`.
- Kept `--root` as a compatibility alias for an explicit run root.
- Removed generated `anim8gen/assets`, `anim8gen/config`, `anim8gen/preview`, and `anim8gen/reports` references from new specs and package manifests.
- Added regression tests for hidden-workspace initialization and the `--root` alias.
- Marked Phase 2 as `✅ Done` in the plan tracker.

## Tests Run

- `python3 -m py_compile .codex/skills/anim8gen/scripts/*.py anim8gen/tools/*.py tests/*.py`
- `python3 tests/test_anim8gen_tools.py`
- Temp clean initializer check:
  - `python3 .codex/skills/anim8gen/scripts/init_package.py --brief "$tmpdir/trex.brief.json" --project-root "$tmpdir/client"`
  - `find "$tmpdir/client" -maxdepth 3 -type d | sort`
  - `test ! -e "$tmpdir/client/anim8gen"`
  - `! rg -n "anim8gen/(assets|config|preview|reports)" "$tmpdir/client/.anim8gen/runs/trex-roar-v1/config/trex-roar-v1.json"`

## Verification Result

Passed. Inline verification covered the updated initializer behavior, old `--root` alias behavior, no visible `anim8gen/` creation for a temp client project, no hard-coded legacy paths in generated specs, and existing anim8gen tool regressions. Separate verifier assurance was not used because this runner-managed chunk did not explicitly authorize sub-agent delegation.

## Landing Result

Landed. Worktree commit `fb55892` was cherry-picked to `main` as `dc337d3`.

## Remaining Phases

- Phase 3: Tooling install boundary
- Phase 4: Visible export step
- Phase 5: Demo/repo surface cleanup
- Phase 6: Skill and README updates
- Phase 7: Tests and clean-room verification
