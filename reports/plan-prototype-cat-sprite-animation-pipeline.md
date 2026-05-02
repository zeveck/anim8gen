# Plan Report: Prototype Cat Sprite Animation Pipeline

## Phase 1: Scaffold The Prototype Workspace

Status: complete

Branch/worktree:

- Branch: `run-plan/prototype-cat-sprite-animation-pipeline-phase-1`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-1`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/README.md`
- `sprite-lab/config/cat-yawn-lay-sleep.json`
- `sprite-lab/assets/cat-yawn-lay-sleep/.gitignore`
- `sprite-lab/assets/cat-yawn-lay-sleep/*/.gitkeep`
- `sprite-lab/tools/.gitkeep`
- `sprite-lab/preview/.gitkeep`
- `sprite-lab/reports/.gitkeep`

Verification:

```bash
python3 -m json.tool sprite-lab/config/cat-yawn-lay-sleep.json >/dev/null
find sprite-lab -maxdepth 3 -type d | sort
```

Result: passed with inline verification.

Landing result: landed on `main` as commit `3ccbc2a` by local cherry-pick.

Notes:

- The spec is parseable and follows the reusable sections from the plan:
  `asset`, `render`, `generation`, `segmentation`, `alignment`, `validation`,
  `preview`, and `frames`.
- The prototype dependency approach is documented in `sprite-lab/README.md`.
- Generated image directories are ignored while placeholder files keep the
  scaffold visible in git.
- No separate verifier agent was used in this chunk; verification was run
  inline from the actual diff.

## Remaining Phases

- Phase 4: Segment, crop, and align frames.
- Phase 5: Validate sprite consistency.
- Phase 6: Produce review artifacts.
- Phase 7: Build HTML preview.
- Phase 8: Manual review and iteration loop.
- Phase 9: Package prototype result.
- Phase 10: Second animation readiness check.

## Phase 3: Generate Candidate Still Frames

Status: complete

Branch/worktree:

- Branch: `zskills/prototype-cat-sprite-animation-pipeline-phase-3`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-3`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `reports/plan-prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/assets/cat-yawn-lay-sleep/manifests/candidates.jsonl`

Generated local artifacts:

- `sprite-lab/assets/cat-yawn-lay-sleep/raw/frame-000.retry-001.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/raw/frame-001.retry-001.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/raw/frame-002.retry-001.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/raw/frame-003.retry-001.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/raw/frame-004.retry-001.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/raw/frame-005.retry-001.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/raw/frame-006.retry-001.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/raw/frame-007.retry-001.png`

Generation metadata:

- Generator: `imagegen2`
- Model: `gpt-image-2`
- Quality: `low`
- Size: `1024x1024`
- Reference image: `sprite-lab/assets/cat-yawn-lay-sleep/reference/cat-reference.jpg`
- Manifest: `sprite-lab/assets/cat-yawn-lay-sleep/manifests/candidates.jsonl`

Verification:

```bash
find sprite-lab/assets/cat-yawn-lay-sleep/raw -type f | sort
file sprite-lab/assets/cat-yawn-lay-sleep/raw/*
test -s sprite-lab/assets/cat-yawn-lay-sleep/manifests/candidates.jsonl
```

Result: passed with inline verification. All eight raw frame candidates exist
as 1024x1024 PNGs, and the candidate manifest contains one metadata record per
frame.

Visual review:

- Spot-checked all motion groups: sitting, yawn, lowering, lying, and sleep.
- Frames preserve a side-view orange tabby cat on magenta background.
- No frames include baked-in Zs, text labels, props, or scene backgrounds.
- These are still candidates, not manually accepted final frames.

Landing result: landed on `main` as commit `5de1857` by local cherry-pick.

Notes:

- `nanogen` was attempted first for Phase 3, but referenced frame generation
  stalled on frame 1 after producing only frame 0. The partial nanogen output
  was discarded and replaced with an `imagegen2` candidate set.
- Raw generated PNGs remain ignored by git per the plan's generated-asset
  rule; they must be copied from the phase worktree into the main workspace
  after landing so later phases can align and validate them locally.
- `accepted-frames.json` is intentionally not written yet because manual
  approval belongs to later review phases.

## Remaining Phases

- Phase 4: Segment, crop, and align frames.
- Phase 5: Validate sprite consistency.
- Phase 6: Produce review artifacts.
- Phase 7: Build HTML preview.
- Phase 8: Manual review and iteration loop.
- Phase 9: Package prototype result.
- Phase 10: Second animation readiness check.

## Phase 2: Create A Canonical Cat Reference

Status: complete

Branch/worktree:

- Branch: `zskills/prototype-cat-sprite-animation-pipeline-phase-2`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-2`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/config/cat-yawn-lay-sleep.json`
- `reports/plan-prototype-cat-sprite-animation-pipeline.md`

Generated local artifact:

- `sprite-lab/assets/cat-yawn-lay-sleep/reference/cat-reference.jpg`

Generation metadata:

- Generator: `nanogen`
- Model: `gemini-3.1-flash-image-preview`
- Style: `pixel-16bit`
- Aspect/size: `1:1`, `1K`
- History ID: `cat-yawn-lay-sleep-reference-v1`
- Output format returned by API: `jpeg`
- Prompt summary: 16-bit side-view small cat sprite, centered on a flat
  magenta chromakey background, no text, no props, limited 32-to-48 color
  palette.

Verification:

```bash
node .codex/skills/nanogen/generate.cjs --prompt preflight --output /tmp/nanogen-preflight.png --dry-run
file sprite-lab/assets/cat-yawn-lay-sleep/reference/cat-reference.jpg
```

Result: passed with inline verification. The generated image is a 1024x1024
JPEG, readable as a 16-bit side-view cat reference against a magenta
background.

Landing result: landed on `main` as commit `c951ca5` by local cherry-pick.

Notes:

- Gemini returned JPEG bytes, so the spec now points at
  `cat-reference.jpg` instead of the originally recommended PNG path.
- The reference has a small darker floor/contact shadow. This is documented as
  a cleanup risk for chromakey segmentation, but the silhouette, palette, and
  pose are suitable for Phase 3 continuity references.
- The generated bitmap remains ignored by git per the plan's generated-asset
  rule; it must be copied from the phase worktree into the main workspace after
  landing so later phases can use it locally.

## Remaining Phases

- Phase 3: Generate candidate still frames.
- Phase 4: Segment, crop, and align frames.
- Phase 5: Validate sprite consistency.
- Phase 6: Produce review artifacts.
- Phase 7: Build HTML preview.
- Phase 8: Manual review and iteration loop.
- Phase 9: Package prototype result.
- Phase 10: Second animation readiness check.

## Phase 4: Segment, Crop, And Align Frames

Status: complete

Branch/worktree:

- Branch: `zskills/prototype-cat-sprite-animation-pipeline-phase-4`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-4`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `reports/plan-prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/requirements.txt`
- `sprite-lab/tools/align_frames.py`
- `sprite-lab/assets/cat-yawn-lay-sleep/manifests/alignment-metrics.json`

Generated local artifacts:

- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-000.sit-idle.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-001.yawn-start.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-002.yawn-wide.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-003.yawn-end.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-004.lowering.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-005.lying-head-up.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-006.lying-head-down.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-007.sleep-loop.png`

Implementation notes:

- The aligner uses Pillow 12.2.0, scoped to `sprite-lab/requirements.txt`.
- Raw frames are converted to RGBA, chromakeyed against the configured magenta
  background, reduced to the largest connected component, cropped, scaled, and
  composited onto a 128x128 transparent canvas.
- The metrics manifest records source and aligned bounding boxes, visible area,
  centroid, anchor strategy, source anchor, scaled size, and applied offset.
- Manual anchor overrides are supported through `alignment.manualOverrides` in
  the animation spec.

Verification:

```bash
python3 -m py_compile sprite-lab/tools/align_frames.py
python3 -W error::DeprecationWarning sprite-lab/tools/align_frames.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --input sprite-lab/assets/cat-yawn-lay-sleep/raw \
  --output sprite-lab/assets/cat-yawn-lay-sleep/aligned
python3 -m json.tool sprite-lab/assets/cat-yawn-lay-sleep/manifests/alignment-metrics.json >/dev/null
file sprite-lab/assets/cat-yawn-lay-sleep/aligned/*.png
```

Result: passed with inline verification. All eight aligned frames are
128x128 RGBA PNGs with transparent backgrounds, and the metrics manifest is
valid JSON.

Visual review:

- Spot-checked `frame-002.yawn-wide.png` and `frame-006.lying-head-down.png`.
- The yawn and lying silhouettes are readable, centered on the canvas, and
  free of obvious magenta background residue at 128x128.

Landing result: landed on `main` by local cherry-pick.

Notes:

- Raw and aligned generated PNGs remain ignored by git per the plan's
  generated-asset rule; aligned outputs must be copied from the phase worktree
  into the main workspace after landing so later phases can validate and
  preview them locally.
- No separate verifier agent was used in this chunk; verification was run
  inline from the actual diff.

## Remaining Phases

- Phase 5: Validate sprite consistency.
- Phase 6: Produce review artifacts.
- Phase 7: Build HTML preview.
- Phase 8: Manual review and iteration loop.
- Phase 9: Package prototype result.
- Phase 10: Second animation readiness check.

## Phase 5: Validate Sprite Consistency

Status: complete

Branch/worktree:

- Branch: `zskills/prototype-cat-sprite-animation-pipeline-phase-5`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-5`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `reports/plan-prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/tools/validate_sprites.py`
- `sprite-lab/reports/cat-yawn-lay-sleep.validation.json`

Implementation notes:

- Added a spec-driven validator for aligned RGBA sprite frames.
- Structural failures are limited to missing frames, unreadable images,
  inconsistent dimensions, and empty sprite masks.
- Drift and style checks are emitted as warnings with phase context and the
  effective numeric thresholds used for each adjacent-frame comparison.
- Phase-specific overrides are visible in the validation JSON for `yawn`,
  `lower-to-floor`, and `sleep-hold` comparisons.

Tests run:

```bash
python3 -m py_compile sprite-lab/tools/validate_sprites.py
python3 -W error::DeprecationWarning sprite-lab/tools/validate_sprites.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --out sprite-lab/reports/cat-yawn-lay-sleep.validation.json
python3 -m json.tool sprite-lab/reports/cat-yawn-lay-sleep.validation.json >/dev/null
```

Verification result: passed with inline verification. The validation report
contains all eight expected frames, zero structural failures, and 13 warnings
for review. The warnings highlight likely motion or alignment review targets on
`000->001`, `003->004`, `004->005`, `005->006`, and `006->007`; they do not
block this phase because warnings are advisory by design.

Landing result: landed on `main` by local cherry-pick.

Scope assessment: Phase 5 stayed within the validator, its generated validation
report, and plan/report tracking. It did not modify generation, alignment, raw
assets, aligned assets, or animation spec semantics.

Notes:

- No separate verifier agent was used in this chunk; verification was run
  inline from the actual diff.
- Raw and aligned generated PNGs remain ignored by git per the generated-asset
  rule. The validation JSON is tracked because it is project report evidence
  required by later review and preview phases.

## Remaining Phases

- Phase 6: Produce review artifacts.
- Phase 7: Build HTML preview.
- Phase 8: Manual review and iteration loop.
- Phase 9: Package prototype result.
- Phase 10: Second animation readiness check.

## Phase 6: Produce Review Artifacts

Status: complete

Branch/worktree:

- Branch: `zskills/prototype-cat-sprite-animation-pipeline-phase-6`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-6`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `reports/plan-prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/tools/make_contact_sheet.py`

Generated local artifact:

- `sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png`

Implementation notes:

- Added a spec-driven contact sheet generator that renders raw candidates,
  aligned frames with bbox/anchor/floor overlays, per-frame warning markers,
  and onion-skin composites with previous frame in red and next frame in blue.
- The tool reads existing validation JSON and alignment-ready frame paths
  without changing raw, aligned, or validation outputs.

Tests run:

```bash
python3 -m py_compile sprite-lab/tools/make_contact_sheet.py
python3 -W error::DeprecationWarning sprite-lab/tools/make_contact_sheet.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --raw sprite-lab/assets/cat-yawn-lay-sleep/raw \
  --aligned sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json \
  --out sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png
file sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png
```

Verification result: passed with inline verification. The contact sheet was
generated as a 2338x944 RGB PNG and includes all eight frames across raw,
aligned overlay, and onion-skin rows.

Landing result: landed on `main` by local cherry-pick.

Scope assessment: Phase 6 stayed within the review artifact generator, its
ignored generated contact sheet, and plan/report tracking. It did not modify
generation, alignment, validation, raw assets, aligned assets, or animation spec
semantics.

Notes:

- No separate verifier agent was used in this chunk; verification was run
  inline from the actual diff.
- The generated contact sheet remains ignored by git per the generated-asset
  rule and must be copied from the phase worktree into the main workspace after
  landing so later manual review can use it locally.

## Remaining Phases

- Phase 7: Build HTML preview.
- Phase 8: Manual review and iteration loop.
- Phase 9: Package prototype result.
- Phase 10: Second animation readiness check.

## Phase 7: Build HTML Preview

Status: complete

Branch/worktree:

- Branch: `zskills/prototype-cat-sprite-animation-pipeline-phase-7`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-7`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `reports/plan-prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/tools/make_preview.py`
- `sprite-lab/preview/cat-yawn-lay-sleep.html`

Implementation notes:

- Added a spec-driven static HTML preview generator for aligned frames.
- The generated preview uses a canvas with pixelated rendering, play/pause,
  previous/next stepping, FPS control, current frame label and pose text,
  checkerboard toggle, thumbnail frame selection, and a separate CSS sleeping
  Zs overlay for sleep frames.
- The preview references local aligned PNGs by relative path instead of
  embedding generated image bytes in git.

Tests run:

```bash
python3 -m py_compile sprite-lab/tools/make_preview.py
python3 -W error::DeprecationWarning sprite-lab/tools/make_preview.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json \
  --out sprite-lab/preview/cat-yawn-lay-sleep.html
file sprite-lab/preview/cat-yawn-lay-sleep.html
rg -n "image-rendering|Sleeping Zs|\\.png|data:image" \
  sprite-lab/preview/cat-yawn-lay-sleep.html
python3 -m http.server 8765 --bind 127.0.0.1
playwright-cli open http://127.0.0.1:8765/preview/cat-yawn-lay-sleep.html
playwright-cli snapshot
playwright-cli eval '() => ({label: document.querySelector("#frameLabel")?.textContent, canvas: document.querySelector("#sprite")?.toDataURL().length, thumbs: document.querySelectorAll(".thumb").length})'
playwright-cli click lying-head-down
playwright-cli eval '() => ({label: document.querySelector("#frameLabel")?.textContent, zsActive: document.querySelector("#zs")?.classList.contains("active")})'
playwright-cli click Pause
playwright-cli eval '() => document.querySelector("#play")?.textContent'
```

Verification result: passed with inline verification. The generator produced
`sprite-lab/preview/cat-yawn-lay-sleep.html`, the HTML contains pixelated image
rendering and relative aligned-frame paths, Chromium loaded all eight frame
PNGs through a local static server, the canvas rendered non-empty frame data,
thumbnail selection moved to `006 lying-head-down`, sleeping Zs activated on
that sleep frame, and the play/pause button toggled back to `Play`.

Landing result: landed on `main` by local cherry-pick.

Scope assessment: Phase 7 stayed within the preview generator, its generated
HTML preview, and plan/report tracking. It did not modify generation,
alignment, validation, contact sheet generation, raw assets, aligned assets, or
animation spec semantics.

Notes:

- No separate verifier agent was used in this chunk; verification was run
  inline from the actual diff.
- The Playwright CLI blocks direct `file://` navigation, so browser
  verification used a temporary `python3 -m http.server` from `sprite-lab/`.
  The generated HTML still uses relative paths and is intended to open locally
  without a project dev server in normal browsers.

## Remaining Phases

- Phase 8: Manual review and iteration loop.
- Phase 9: Package prototype result.
- Phase 10: Second animation readiness check.

## Phase 8: Manual Review And Iteration Loop

Status: complete

Branch/worktree:

- Branch: `zskills/prototype-cat-sprite-animation-pipeline-phase-8`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-8`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `reports/plan-prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/config/cat-yawn-lay-sleep.json`
- `sprite-lab/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json`
- `sprite-lab/assets/cat-yawn-lay-sleep/manifests/alignment-metrics.json`
- `sprite-lab/reports/cat-yawn-lay-sleep.validation.json`
- `sprite-lab/reports/cat-yawn-lay-sleep.summary.md`
- `sprite-lab/preview/cat-yawn-lay-sleep.html`

Generated local artifacts:

- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-000.sit-idle.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-001.yawn-start.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-002.yawn-wide.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-003.yawn-end.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-004.lowering.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-005.lying-head-up.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-006.lying-head-down.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-007.sleep-loop.png`
- `sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png`

Implementation notes:

- Manual review found frame 000 clipped on the right edge and frames 005
  through 007 vertically centered above the intended shared floor line.
- Added spec-level manual anchor overrides for frames 000, 005, 006, and 007,
  then reran alignment, validation, contact sheet generation, and preview
  generation.
- Wrote `accepted-frames.json` and `cat-yawn-lay-sleep.summary.md` as the
  durable manual review record.

Tests run:

```bash
python3 -m json.tool sprite-lab/config/cat-yawn-lay-sleep.json >/dev/null
python3 -W error::DeprecationWarning sprite-lab/tools/align_frames.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --input sprite-lab/assets/cat-yawn-lay-sleep/raw \
  --output sprite-lab/assets/cat-yawn-lay-sleep/aligned
python3 -W error::DeprecationWarning sprite-lab/tools/validate_sprites.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --out sprite-lab/reports/cat-yawn-lay-sleep.validation.json
python3 -W error::DeprecationWarning sprite-lab/tools/make_contact_sheet.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --raw sprite-lab/assets/cat-yawn-lay-sleep/raw \
  --aligned sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json \
  --out sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png
python3 -W error::DeprecationWarning sprite-lab/tools/make_preview.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json \
  --out sprite-lab/preview/cat-yawn-lay-sleep.html
file sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png \
  sprite-lab/preview/cat-yawn-lay-sleep.html
python3 -m json.tool \
  sprite-lab/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json >/dev/null
```

Manual browser verification:

```bash
python3 -m http.server 8766 --bind 127.0.0.1
playwright-cli open http://127.0.0.1:8766/preview/cat-yawn-lay-sleep.html
playwright-cli snapshot
playwright-cli eval '() => ({label: document.querySelector("#frameLabel")?.textContent, pose: document.querySelector("#pose")?.textContent, canvasBytes: document.querySelector("#sprite")?.toDataURL().length, thumbs: document.querySelectorAll(".thumb").length, zsActive: document.querySelector("#zs")?.classList.contains("active")})'
playwright-cli click e38
playwright-cli eval '() => ({label: document.querySelector("#frameLabel")?.textContent, zsActive: document.querySelector("#zs")?.classList.contains("active"), canvasBytes: document.querySelector("#sprite")?.toDataURL().length})'
playwright-cli click e12
playwright-cli eval '() => document.querySelector("#play")?.textContent'
playwright-cli click e13
playwright-cli eval '() => ({label: document.querySelector("#frameLabel")?.textContent, zsActive: document.querySelector("#zs")?.classList.contains("active")})'
```

Verification result: passed with inline verification. The updated contact sheet
shows no right-edge clipping and the lying frames now sit on the shared floor
line. The validation report has zero structural failures and 14 advisory
warnings, all documented in the summary report. Browser verification confirmed
non-empty canvas rendering, eight thumbnail frames, frame selection,
play/pause, next-frame stepping, and sleep-frame Z activation. The only browser
console error was the expected missing `favicon.ico` request from the temporary
static server.

Landing result: landed on `main` by local cherry-pick.

Scope assessment: Phase 8 stayed within manual review and iteration outputs:
spec-level manual anchors, regenerated derived alignment/validation/preview
artifacts, accepted-frame provenance, summary report, and plan/report tracking.
It did not regenerate source candidate images or change tool code.

Notes:

- No separate verifier agent was used in this chunk; verification was run
  inline from the actual diff.
- Raw, aligned, reference, and review PNG/JPG assets remain ignored by git per
  the generated-asset rule and must be copied into the main workspace after
  landing for local Phase 9 packaging.

## Remaining Phases

- Phase 9: Package prototype result.
- Phase 10: Second animation readiness check.

## Phase 9: Package Prototype Result

Status: complete

Branch/worktree:

- Branch: `zskills/prototype-cat-sprite-animation-pipeline-phase-9`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-9`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `reports/plan-prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/README.md`
- `sprite-lab/assets/cat-yawn-lay-sleep/manifests/package-manifest.json`
- `sprite-lab/reports/cat-yawn-lay-sleep.package.md`

Implementation notes:

- Added a tracked package manifest that identifies final aligned frames,
  validation output, contact sheet, HTML preview, summary report, intermediate
  raw/reference assets, provenance manifests, and the tool scripts required to
  rebuild the accepted package.
- Added a concise package report that separates final outputs from
  intermediate assets and records the exact rebuild, validation, review, and
  preview commands.
- Updated the Sprite Lab README to point reviewers at the package report and
  current dependency file.

Tests run:

```bash
python3 -m json.tool sprite-lab/assets/cat-yawn-lay-sleep/manifests/package-manifest.json >/dev/null
python3 -m json.tool sprite-lab/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json >/dev/null
python3 -m json.tool sprite-lab/config/cat-yawn-lay-sleep.json >/dev/null
python3 -W error::DeprecationWarning sprite-lab/tools/align_frames.py --spec sprite-lab/config/cat-yawn-lay-sleep.json --input sprite-lab/assets/cat-yawn-lay-sleep/raw --output sprite-lab/assets/cat-yawn-lay-sleep/aligned
python3 -W error::DeprecationWarning sprite-lab/tools/validate_sprites.py --spec sprite-lab/config/cat-yawn-lay-sleep.json --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned --out sprite-lab/reports/cat-yawn-lay-sleep.validation.json
python3 -W error::DeprecationWarning sprite-lab/tools/make_contact_sheet.py --spec sprite-lab/config/cat-yawn-lay-sleep.json --raw sprite-lab/assets/cat-yawn-lay-sleep/raw --aligned sprite-lab/assets/cat-yawn-lay-sleep/aligned --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json --out sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png
python3 -W error::DeprecationWarning sprite-lab/tools/make_preview.py --spec sprite-lab/config/cat-yawn-lay-sleep.json --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json --out sprite-lab/preview/cat-yawn-lay-sleep.html
file sprite-lab/assets/cat-yawn-lay-sleep/aligned/*.png sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png sprite-lab/preview/cat-yawn-lay-sleep.html
test -s sprite-lab/reports/cat-yawn-lay-sleep.package.md
```

Verification result: passed with inline verification. The package manifest and
existing accepted-frame/spec JSON parse successfully. The rebuild commands
regenerated eight 128x128 RGBA aligned frames, validation, contact sheet, and
HTML preview from the local accepted assets. The contact sheet is a 2338x944
PNG and the preview is an ASCII HTML document.

Landing result: landed on `main` as commit `6c53798` by local cherry-pick.

Scope assessment: Phase 9 stayed within packaging and provenance. It did not
change generated source images, accepted-frame decisions, validation thresholds,
alignment behavior, contact sheet generation, or preview behavior. Ignored
bitmap assets were copied into the worktree only to verify package references
and were not staged.

Notes:

- No separate verifier agent was used in this chunk; verification was run
  inline from the actual diff.

## Remaining Phases

- Phase 10: Second animation readiness check.

## Phase 10: Second Animation Readiness Check

Status: complete

Branch/worktree:

- Branch: `zskills/prototype-cat-sprite-animation-pipeline-phase-10`
- Worktree: `/tmp/anim8gen-cp-prototype-cat-sprite-animation-pipeline-phase-10`

Files changed:

- `plans/prototype-cat-sprite-animation-pipeline.md`
- `reports/plan-prototype-cat-sprite-animation-pipeline.md`
- `sprite-lab/README.md`
- `sprite-lab/config/cat-sit-lick-paw-sit.json`
- `sprite-lab/assets/cat-sit-lick-paw-sit/.gitignore`
- `sprite-lab/assets/cat-sit-lick-paw-sit/*/.gitkeep`
- `sprite-lab/assets/cat-sit-lick-paw-sit/manifests/candidates.jsonl`
- `sprite-lab/assets/cat-sit-lick-paw-sit/manifests/alignment-metrics.json`
- `sprite-lab/reports/cat-sit-lick-paw-sit.validation.json`
- `sprite-lab/reports/cat-sit-lick-paw-sit.readiness.md`

Generated local artifacts:

- `sprite-lab/assets/cat-sit-lick-paw-sit/reference/synthetic-reference.png`
- `sprite-lab/assets/cat-sit-lick-paw-sit/raw/frame-000.retry-001.png`
- `sprite-lab/assets/cat-sit-lick-paw-sit/raw/frame-001.retry-001.png`
- `sprite-lab/assets/cat-sit-lick-paw-sit/raw/frame-002.retry-001.png`
- `sprite-lab/assets/cat-sit-lick-paw-sit/aligned/frame-000.sit-idle.png`
- `sprite-lab/assets/cat-sit-lick-paw-sit/aligned/frame-001.lick-paw.png`
- `sprite-lab/assets/cat-sit-lick-paw-sit/aligned/frame-002.sit-return.png`

Implementation notes:

- Added a second stationary animation spec, `cat-sit-lick-paw-sit`, using the
  same reusable spec sections as the accepted cat prototype.
- Created three local synthetic 1024x1024 chromakey raw frames for sit, lick
  paw, and sit return so the readiness check does not depend on generation
  budget or external image services.
- Ran the existing alignment and validation tools unchanged against the second
  spec and folder layout.
- Documented the readiness check and the ignored synthetic image convention.

Tests run:

```bash
python3 -m json.tool sprite-lab/config/cat-sit-lick-paw-sit.json >/dev/null
python3 -m py_compile sprite-lab/tools/align_frames.py sprite-lab/tools/validate_sprites.py
python3 -W error::DeprecationWarning sprite-lab/tools/align_frames.py \
  --spec sprite-lab/config/cat-sit-lick-paw-sit.json \
  --input sprite-lab/assets/cat-sit-lick-paw-sit/raw \
  --output sprite-lab/assets/cat-sit-lick-paw-sit/aligned
python3 -W error::DeprecationWarning sprite-lab/tools/validate_sprites.py \
  --spec sprite-lab/config/cat-sit-lick-paw-sit.json \
  --frames sprite-lab/assets/cat-sit-lick-paw-sit/aligned \
  --out sprite-lab/reports/cat-sit-lick-paw-sit.validation.json
python3 -m json.tool sprite-lab/reports/cat-sit-lick-paw-sit.validation.json >/dev/null
file sprite-lab/assets/cat-sit-lick-paw-sit/aligned/*.png \
  sprite-lab/reports/cat-sit-lick-paw-sit.validation.json
python3 - <<'PY'
import json
from pathlib import Path
report = json.loads(Path('sprite-lab/reports/cat-sit-lick-paw-sit.validation.json').read_text())
assert report['summary']['frameCount'] == 3, report['summary']
assert report['summary']['structuralFailureCount'] == 0, report['summary']
assert report['status'] == 'passed', report['status']
print(report['summary'])
PY
```

Verification result: passed with inline verification. The second spec parses,
the existing aligner produced three 128x128 RGBA aligned PNGs, and the
validation report has three expected frames, zero structural failures, and zero
warnings.

Landing result: pending local cherry-pick to `main`.

Scope assessment: Phase 10 stayed within the second-animation readiness check,
its spec, generated local synthetic fixtures, validation evidence,
documentation, and plan/report tracking. It did not change first-sequence
outputs, existing tool behavior, accepted-frame decisions, or packaging
semantics.

Notes:

- No separate verifier agent was used in this chunk; verification was run
  inline from the actual diff.
- The runner contract named `origin` as the execution remote, but this local
  repository has no configured remote. Cherry-pick landing will be completed
  locally from the phase worktree to `main`.
- Synthetic reference, raw, and aligned PNGs remain ignored by git per the
  generated-asset convention and must be copied into the main workspace after
  landing for local re-runs.

## Remaining Phases

- None. The plan is complete.
