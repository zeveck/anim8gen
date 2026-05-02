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
