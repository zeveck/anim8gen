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

Landing result: Committed on `main` as `2b6d00c`.

Remaining phases:

- Phase 4: Tests
- Phase 5: Public demo sanity

## Phase

Phase 4: Tests

Status: ✅ Done

Scope assessment: Scoped to deterministic local tool behavior. Added a
standard-library test runner covering GIF dimensions/frame count, terminal
reuse-frame skipping, non-terminal frame preservation, display-offset rendering,
preview/public-demo playback ordering, and magenta/green/cyan chroma-key family
cleanup. Kept tests offline and temporary-file based.

Tests run:

- `python3 tests/test_anim8gen_tools.py`
- `python3 -m py_compile anim8gen/tools/*.py .codex/skills/anim8gen/scripts/*.py`

Verification result: Passed. The tests run without network or imagegen2 API
access and do not write into committed demo folders.

Landing result: Committed on `main` as `786e720`.

Remaining phases:

- Phase 5: Public demo sanity

## Phase

Phase 5: Public demo sanity

Status: ✅ Done

Scope assessment: Scoped to the committed public demo surface. Re-exported the
six curated demos, added their specs, added the static GitHub Pages workflow,
and kept public GIF media under `public/media/`. Removed older non-curated
tracked cat/live specs from the release index while preserving local copies for
stash. Did not commit exploratory smoke/quality configs beyond the selected
curated set.

Tests run:

- `python3 anim8gen/tools/export_public_demo.py quality-knight-sword-spark-v4 quality-cat-tail-swish-v4 quality-cat-pounce-v2 quality-dragon-tail-flick-v4 sci-fi-space-station-explosion pirate-ship-kraken-cannon --clean`
- `python3 -m http.server 8767 --bind 127.0.0.1 --directory public`
- `curl -I http://127.0.0.1:8767/`
- `curl -I http://127.0.0.1:8767/demos/pirate-ship-kraken-cannon/`
- `curl -I http://127.0.0.1:8767/media/pirate-ship-kraken-cannon.gif`
- Python URL probe for every curated demo page, each demo's first frame, and all `public/media/*.gif`.

Verification result: Passed on port `8767`. The originally requested port
`8766` was already in use and failed with `OSError: [Errno 98] Address already
in use`; retrying on `8767` passed with HTTP `200` for the gallery, curated
demo pages, representative frames, and GIF media.

Landing result: Pending before commit.

Remaining phases: none.
