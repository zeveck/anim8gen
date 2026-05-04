# Clean Public Release Surface

## Goal

Prepare `anim8gen` for a public release branch by committing only the durable
source, docs, tests, and curated demo artifacts while keeping generated working
packages local by default.

## Context

The repo currently has a strong working anim8gen pipeline and public demo UI,
but the worktree includes a large exploration corpus:

- `anim8gen/assets/` is roughly 209 MB across dozens of generated packages.
- `anim8gen/contact/` is roughly 27 MB of generated review sheets.
- `public/` is roughly 33 MB and contains the curated demo site.
- `anim8gen/gifs/` exists as local GIF export output.
- `.codex/skills/imagegen`, `.codex/skills/imagegen2`, and
  `.codex/skills/nanogen` are local vendored/development copies, but anim8gen
  should require imagegen2 as an external skill.

The public repo should show enough visual output to be credible, but should
not commit every raw candidate, reference image, aligned frame, old smoke test,
or failed experiment.

## Non-Goals

- Do not delete user-local generated work irreversibly without a backup or a
  clear command.
- Do not vendor imagegen2 into this repo.
- Do not make browser-side GIF encoding part of this cleanup. GIF package
  export is handled by the Python exporter first.
- Do not rewrite the animation-generation workflow beyond docs and artifact
  policy.

## Policy

Track:

- `.codex/skills/anim8gen/**`
- `anim8gen/tools/*.py`
- `anim8gen/config/brief.schema.json`
- `anim8gen/config/template.animation-spec.json`
- Curated demo specs:
  - `anim8gen/config/quality-knight-sword-spark-v4.json`
  - `anim8gen/config/quality-cat-tail-swish-v4.json`
  - `anim8gen/config/quality-cat-pounce-v2.json`
  - `anim8gen/config/quality-dragon-tail-flick-v4.json`
  - `anim8gen/config/sci-fi-space-station-explosion.json`
  - `anim8gen/config/pirate-ship-kraken-cannon.json`
- `README.md`, `anim8gen/README.md`, `anim8gen/DEV_README.md`
- `anim8gen/requirements.txt`
- `.github/workflows/pages.yml`
- Curated public demo site under `public/`
- `public/media/*.gif`
- Plan/report docs that are useful release history.

Ignore:

- `.env`
- `.imagegen2-history.jsonl`
- `.zskills/`
- `.claude/`
- `external/`
- `__pycache__/`, `*.py[cod]`
- `.playwright/output/`
- `anim8gen/assets/**`
- `anim8gen/contact/**`
- `anim8gen/preview/*.html`
- `anim8gen/reports/*.json`
- `anim8gen/reports/*.package.md`
- `anim8gen/gifs/**`
- root duplicate GIFs such as `anim8gen-demo.gif` and `anim8gen-demo2.gif`

Keep only `.gitkeep` placeholders where useful for empty generated-output
directories.

## Phase 1: Artifact Policy And Ignore Rules

- Update root `.gitignore` with root-level ignores for generated package
  assets and local outputs.
- Keep `public/**` intentionally unignored.
- Keep source config/templates/docs/tools unignored.
- Add comments explaining that `public/demos` is the committed demo surface and
  `anim8gen/assets` is the local working surface.

Acceptance criteria:

- `git status --short` no longer lists old generated package asset folders,
  contact sheets, preview HTML, local GIF exports, or duplicate root media.
- Curated `public/` files remain visible to git.
- New generated packages will be ignored even if their per-package `.gitignore`
  is missing.

Verification:

```bash
git status --short
git check-ignore -v anim8gen/assets/pirate-ship-kraken-cannon/raw/frame-000.retry-001.png
git check-ignore -v anim8gen/contact/pirate-ship-kraken-cannon.png
git check-ignore -v anim8gen/gifs/quality-cat-pounce-v2.gif
git check-ignore -v anim8gen/preview/pirate-ship-kraken-cannon.html
git check-ignore -v public/demos/pirate-ship-kraken-cannon/index.html || true
```

## Phase 2: Prune Staging Surface

- Do not commit `.codex/skills/imagegen`, `.codex/skills/imagegen2`, or
  `.codex/skills/nanogen` changes in this repo. Keep them local or move
  imagegen2 work to the imagegen2 repo.
- Do not stage old exploratory config files unless they are part of the curated
  demo set or deterministic fixtures.
- Remove or ignore duplicate root media:
  - `anim8gen-demo.gif`
  - `anim8gen-demo2.gif`
- Decide whether to keep `deterministic-square-hop` as a tiny regression
  fixture. If kept, document it as a fixture. If not, ignore/prune it with the
  rest of the old package outputs.

Acceptance criteria:

- `git diff --stat` for staged source changes is readable.
- Staged files are explainable as source, docs, tests, selected specs, or
  public demo output.

Verification:

```bash
git diff --stat --cached
git status --short
```

## Phase 3: GIF Flag Integration

- Keep `anim8gen/tools/export_gif.py`.
- Update `.codex/skills/anim8gen/SKILL.md` so the `gif` flag is
  order-insensitive alongside `showit` and `noshow`.
- Update README usage examples for `anim8gen gif <prompt>`.
- Update package-report expectations so GIF path is included when requested.
- Do not commit generated `anim8gen/gifs/*.gif`; they are local run artifacts.

Acceptance criteria:

- A user can request `anim8gen gif <prompt>` and the agent knows to run
  `export_gif.py` after preview generation.
- GIF export output defaults to `anim8gen/gifs/<animation-id>.gif`.
- `gif showit` and `gif noshow` behavior is documented.

Verification:

```bash
python3 -m py_compile anim8gen/tools/export_gif.py
python3 anim8gen/tools/export_gif.py \
  --spec anim8gen/config/quality-cat-pounce-v2.json \
  --frames anim8gen/assets/quality-cat-pounce-v2/aligned \
  --out /tmp/quality-cat-pounce-v2.gif
python3 - <<'PY'
from PIL import Image
im = Image.open('/tmp/quality-cat-pounce-v2.gif')
print(im.size, getattr(im, 'n_frames', 1))
assert getattr(im, 'n_frames', 1) >= 2
PY
```

## Phase 4: Tests

Add lightweight tests around deterministic local behavior:

- `export_gif.py` exports a GIF with expected dimensions and frame count.
- Terminal `reuseFrame` that points to frame 0 is skipped unless
  `preview.playTerminalReuseFrame` is true.
- Non-terminal repeated/held frames are preserved.
- `preview.displayOffsets` affect GIF pixels.
- `make_preview.build_payload` and `export_public_demo.py` agree on frame
  ordering for a fixture spec.
- `align_frames.py` rejects generic chroma-key color families for magenta,
  green, and cyan.

Prefer `pytest` if acceptable; otherwise use a small `tests/*.py` script with
plain asserts and a documented command.

Acceptance criteria:

- Test command is documented in `anim8gen/DEV_README.md`.
- Tests do not require network or imagegen2 API access.
- Tests create temporary fixtures under `/tmp` or pytest `tmp_path`, not under
  committed demo folders.

Verification:

```bash
python3 -m py_compile anim8gen/tools/*.py .codex/skills/anim8gen/scripts/*.py
python3 -m pytest
```

## Phase 5: Public Demo Sanity

- Re-export curated demos after the ignore policy is in place.
- Ensure `public/index.html` links only to curated demos.
- Ensure public demo pages load their local frames.
- Ensure public media GIFs are under `public/media/`, not repo root.

Acceptance criteria:

- `public/` contains only the curated demo gallery and supporting media.
- Local server returns `200` for each curated demo page and media GIF.
- README demo links match `public/index.html`.

Verification:

```bash
python3 -m http.server 8766 --bind 127.0.0.1 --directory public
curl -I http://127.0.0.1:8766/
curl -I http://127.0.0.1:8766/demos/pirate-ship-kraken-cannon/
curl -I http://127.0.0.1:8766/media/pirate-ship-kraken-cannon.gif
```

## Risks

- Root-level ignores for `anim8gen/assets/**` will hide generated manifests and
  review JSON too. That is intentional for public release unless a fixture is
  explicitly unignored.
- Public demos are still generated artifacts and may grow. Keep the curated set
  small and prefer optimized media when possible.
- Existing tracked generated files may require `git rm --cached` rather than
  only `.gitignore`.
- Claude install instructions need a real install smoke test from a clean
  checkout before release.

## Progress Tracker

- [✅ Done] Phase 1: Artifact policy and ignore rules
- [✅ Done] Phase 2: Prune staging surface
- [ ] Phase 3: GIF flag integration
- [ ] Phase 4: Tests
- [ ] Phase 5: Public demo sanity
