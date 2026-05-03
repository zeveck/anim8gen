# Plan Report: Add Solid Transparency Support To Imagegen2

## Phase

Phase 1: Define CLI Contract

Status: completed and landed via cherry-pick.

## Summary

- Added the documented `chroma-key` transparency contract for PNG output:
  user intent remains `background: "transparent"` while the normalized API
  request uses `background: "opaque"` and `output_format: "png"`.
- Added `--chroma-tolerance <0-442>` with conservative default `16`.
- Added chroma-key prompt suffix guidance and dry-run `postprocess` metadata.
- Updated README, migration notes, CLI reference, Codex skill guidance, bundled
  CLI/reference copies, and offline tests for the Phase 1 contract.

## Tests Run

- `node --check cli/generate.cjs` in `/tmp/imagegen2-cp-solid-transparency-phase1`
- `npm test` in `/tmp/imagegen2-cp-solid-transparency-phase1` (`48 passed, 0 failed`)
- `npm run test:all` in `/tmp/imagegen2-cp-solid-transparency-phase1` (`48 passed, 0 failed`; live smoke skipped because `IMAGEGEN2_LIVE_TEST` was not set)
- Target chroma-key dry-run command in `/tmp/imagegen2-cp-solid-transparency-phase1`
- `node --check cli/generate.cjs` in `/workspaces/anim8gen/external/imagegen2` after cherry-pick
- `npm test` in `/workspaces/anim8gen/external/imagegen2` after cherry-pick (`48 passed, 0 failed`)

## Verification Result

Passed. Verification was run inline in a fresh manual worktree and repeated
after cherry-pick on `external/imagegen2` main. Dry-run output now clearly
shows `transparentMode: "chroma-key"`, `background: "transparent"`,
`params.background: "opaque"`, `params.output_format: "png"`, the key color,
and `postprocess` details.

## Landing Result

Resolved landing mode: cherry-pick.

Implementation worktree: `/tmp/imagegen2-cp-solid-transparency-phase1`

Worktree commit: `24e5bd7 Define chroma-key transparency CLI contract`

Cherry-picked to `/workspaces/anim8gen/external/imagegen2` main as:
`8851fa9 Define chroma-key transparency CLI contract`

No `.zskills` tracking files were committed.

## Remaining Phases

- Phase 2: Implement PNG chroma-key post-processing.
- Phase 3: Wire full validation and request building for non-dry-run
  chroma-key behavior, including edits and history/stdout details.
- Phase 4: Offline post-processing tests.
- Phase 5: Docs and skill guidance.
- Phase 6: Live smoke gate.
- Phase 7: Native transparency probe.

## Scope Assessment

Scope stayed within Phase 1. The change defines and verifies the user-facing
contract and dry-run/request-normalization surface, but intentionally leaves
actual PNG alpha post-processing and non-dry-run chroma-key generation blocked
until the next implementation phase.
