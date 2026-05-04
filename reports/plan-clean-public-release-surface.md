# Clean Public Release Surface Report

## Phase

Phase 2: Prune staging surface

Status: ✅ Done

Scope assessment: Scoped to public release staging cleanup. Removed previously tracked generated package asset metadata/placeholders, generated local preview HTML, validation JSON, and package reports from the index while leaving source specs, tools, docs, and durable Markdown reports in the repo. Documented `deterministic-square-hop` as the retained tiny regression fixture spec; its generated outputs stay local and ignored. Did not include `.codex/skills/imagegen`, `.codex/skills/imagegen2`, `.codex/skills/nanogen`, duplicate root GIFs, or exploratory untracked configs.

Tests run:

- `git ls-files -ci --exclude-standard`
- `git diff --stat --cached`
- `git status --short`
- `git diff --cached --name-only | rg '^(\\.codex/skills/(imagegen|imagegen2|nanogen)|anim8gen-demo|anim8gen-demo2)' || true`

Verification result: Passed. The staged surface consists of generated-output removals plus documentation, plan tracker, and this report. No imagegen/imagegen2/nanogen skill changes or duplicate root GIFs are staged.

Landing result: Worktree commit `afedf7c` was cherry-picked to `main` as `f9d972f`.

Remaining phases:

- Phase 3: GIF flag integration
- Phase 4: Tests
- Phase 5: Public demo sanity

## Phase

Phase 3: GIF flag integration

Status: ✅ Done

Scope assessment: Scoped to GIF package export behavior and user-facing skill
instructions. Added the local GIF exporter, documented order-insensitive `gif`
usage alongside `showit` and `noshow`, and kept generated GIFs under ignored
`anim8gen/gifs/` by default. Shared playback-index logic with preview payload
generation so terminal reused frames are skipped consistently unless explicitly
requested.

Tests run:

- `python3 -m py_compile anim8gen/tools/*.py .codex/skills/anim8gen/scripts/*.py`
- `python3 anim8gen/tools/export_gif.py --spec anim8gen/config/quality-cat-pounce-v2.json --frames anim8gen/assets/quality-cat-pounce-v2/aligned --out /tmp/quality-cat-pounce-v2.gif`
- Pillow inspection of `/tmp/quality-cat-pounce-v2.gif`, confirming `(128, 128)` and `3` frames.

Verification result: Passed. GIF export creates a multi-frame animated GIF from
the curated cat pounce package without committing generated GIF output.

Landing result: Pending before commit.

Remaining phases:

- Phase 4: Tests
- Phase 5: Public demo sanity
