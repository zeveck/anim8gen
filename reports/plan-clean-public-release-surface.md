# Clean Public Release Surface Report

## Phase

Phase 1: Artifact policy and ignore rules

Status: ✅ Done

Scope assessment: Scoped to root ignore policy plus the plan tracker and this report. No generated package assets, contact sheets, previews, GIF exports, public demo files, or tool/source changes were modified.

Tests run:

- `git status --short`
- `git check-ignore -v anim8gen/assets/pirate-ship-kraken-cannon/raw/frame-000.retry-001.png`
- `git check-ignore -v anim8gen/contact/pirate-ship-kraken-cannon.png`
- `git check-ignore -v anim8gen/gifs/quality-cat-pounce-v2.gif`
- `git check-ignore -v anim8gen/preview/pirate-ship-kraken-cannon.html`
- `git check-ignore -v public/demos/pirate-ship-kraken-cannon/index.html || true`

Verification result: Passed. Generated package assets, contact sheets, local GIF exports, and preview HTML are ignored by root `.gitignore`; the public demo path is not ignored.

Landing result: Cherry-picked worktree commit `d0eda6f` to `main` as `dbe5d5d`; cherry-picked report evidence commit `4c13518` to `main` as `6b67df3`.

Remaining phases:

- Phase 2: Prune staging surface
- Phase 3: GIF flag integration
- Phase 4: Tests
- Phase 5: Public demo sanity
