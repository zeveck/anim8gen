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
