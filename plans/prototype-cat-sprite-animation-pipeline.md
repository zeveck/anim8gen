# Prototype Cat Sprite Animation Pipeline

## Goal

Build a small, implementation-ready prototype pipeline for creating and reviewing a simple 16-bit pixel-art sprite animation from generated still frames.

Target animation:

```text
16-bit cat: yawn -> lay down -> sleep
```

The first successful output is not a general animation product. It is a repeatable workflow that can generate candidate cat frames, align them on a fixed canvas, validate measurable drift, and preview the short loop in HTML with the sleeping Zs rendered separately.

## Context

- Workspace: `/workspaces/anim8gen`
- Current workspace has no git repository and no app source yet.
- Installed image skills:
  - `nanogen`: best first choice when continuity, seeded generation, iterative edits, or pose refinement matter. It can use style presets such as `pixel-16bit`, reference images, history continuation, and dry-run key preflight. It does not provide native alpha; use chromakey or cleanup.
  - `imagegen2`: best OpenAI comparison/fallback for game-oriented raster assets. It supports dry-run, high-fidelity references, flexible output sizes, and good request metadata. Native transparency requires fallback mode.
  - `imagegen`: useful fallback for simpler transparent bitmap generation or masked edits. It has less batch ergonomics and no dry-run.
- Sleeping Zs should be rendered by the preview/runtime layer, not baked into sprite frames.
- Automation should align, validate, and flag suspicious frames. Human review remains the final quality gate.

## Non-goals

- Do not build a production animation editor.
- Do not attempt walk cycles or four-directional movement in the first prototype.
- Do not generate video as the primary source asset.
- Do not bake Zs, backgrounds, UI labels, or decorative effects into the cat sprite frames.
- Do not require perfect automated approval. The prototype should make manual review fast and informed.

## Proposed Output Structure

Use this structure unless implementation discovers a better local convention:

```text
plans/
  prototype-cat-sprite-animation-pipeline.md
sprite-lab/
  config/
    cat-yawn-lay-sleep.json
  assets/
    cat-yawn-lay-sleep/
      reference/
      raw/
      aligned/
      review/
      manifests/
  tools/
    generate_frames.mjs
    align_frames.py
    validate_sprites.py
    make_contact_sheet.py
    make_preview.py
  preview/
    cat-yawn-lay-sleep.html
  reports/
    cat-yawn-lay-sleep.validation.json
    cat-yawn-lay-sleep.summary.md
```

Keep generated image assets out of source control unless the user later asks to preserve example outputs. If a git repository is initialized later, add runtime/generated directories to `.gitignore`.

## Animation Spec

Create a machine-readable animation spec before generating images.

Recommended fields:

```json
{
  "id": "cat-yawn-lay-sleep",
  "asset": {
    "subject": "cat",
    "style": "16-bit pixel art",
    "canonicalReference": "sprite-lab/assets/cat-yawn-lay-sleep/reference/cat-reference.png",
    "promptTraits": [
      "small cat",
      "side-view",
      "compact readable silhouette",
      "simple markings",
      "no text"
    ]
  },
  "render": {
    "canvas": [128, 128],
    "workingSize": [1024, 1024],
    "exportScale": 8,
    "fps": 8,
    "paletteLimit": 48
  },
  "generation": {
    "preferredSkill": "nanogen",
    "fallbackSkills": ["imagegen2", "imagegen"],
    "candidateManifest": "sprite-lab/assets/cat-yawn-lay-sleep/manifests/candidates.jsonl",
    "acceptedManifest": "sprite-lab/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json"
  },
  "segmentation": {
    "strategy": "chroma-key",
    "chromaKey": "#ff00ff",
    "alphaThreshold": 8,
    "chromaTolerance": 32
  },
  "alignment": {
    "defaultAnchor": "body_bottom_center",
    "floorY": 112,
    "supportedAnchors": ["body_bottom_center", "feet_center", "body_center", "head_center", "manual"],
    "manualOverrides": {}
  },
  "validation": {
    "defaultThresholds": {
      "anchorXJumpPx": 3,
      "anchorYJumpPx": 2,
      "bboxHeightVariancePct": 12,
      "bboxWidthVariancePct": 18,
      "visibleAreaVariancePct": 20,
      "centroidJumpPx": 5,
      "adjacentSilhouetteIouMin": 0.55,
      "meanLuminanceShiftPct": 15,
      "dominantHueShiftDegrees": 12
    },
    "motionPhases": [
      {
        "name": "yawn",
        "frames": [0, 1, 2, 3],
        "thresholdOverrides": {
          "headTopDriftPx": 8,
          "adjacentSilhouetteIouMin": 0.45
        },
        "ignoredWarnings": ["mouthShapeChange"]
      },
      {
        "name": "lower-to-floor",
        "frames": [4, 5],
        "thresholdOverrides": {
          "bboxHeightVariancePct": 35,
          "visibleAreaVariancePct": 35,
          "centroidJumpPx": 12,
          "adjacentSilhouetteIouMin": 0.35
        }
      },
      {
        "name": "sleep-hold",
        "frames": [6, 7],
        "thresholdOverrides": {
          "anchorXJumpPx": 2,
          "anchorYJumpPx": 1,
          "bboxHeightVariancePct": 8,
          "bboxWidthVariancePct": 8,
          "visibleAreaVariancePct": 10
        }
      }
    ]
  },
  "preview": {
    "runtimeEffects": ["sleeping-zs"],
    "minimalControls": ["playPause", "fps", "step", "frameLabel", "checkerboard"]
  },
  "frames": [
    { "index": 0, "label": "sit-idle", "pose": "sitting, eyes open, relaxed", "anchor": "body_bottom_center" },
    { "index": 1, "label": "yawn-start", "pose": "sitting, mouth beginning to open, head starts to tilt up", "anchor": "body_bottom_center" },
    { "index": 2, "label": "yawn-wide", "pose": "sitting, full yawn, mouth wide open, body mostly unchanged", "anchor": "body_bottom_center" },
    { "index": 3, "label": "yawn-end", "pose": "sitting, mouth closing, sleepy eyes", "anchor": "body_bottom_center" },
    { "index": 4, "label": "lowering", "pose": "front legs bend, body lowering toward the floor", "anchor": "body_bottom_center" },
    { "index": 5, "label": "lying-head-up", "pose": "lying down, head still slightly raised", "anchor": "body_center" },
    { "index": 6, "label": "lying-head-down", "pose": "lying down, head resting on paws, eyes closed", "anchor": "body_center" },
    { "index": 7, "label": "sleep-loop", "pose": "lying still asleep, eyes closed, calm breathing pose", "anchor": "body_center" }
  ]
}
```

Notes:

- The exact frame count can be adjusted during implementation, but start with 8 frames because it gives enough shape change without becoming a broad animation problem.
- Work at a high generated resolution, then downsample or crop into a fixed 128x128 sprite canvas for review.
- Prefer chromakey for `nanogen` outputs. Use transparent output only when the selected generator reliably produces it for the current task.
- Keep reusable pipeline settings separate from cat-specific frame poses so the next stationary animation can reuse the same tools without code changes.
- Prefer explicit numeric `thresholdOverrides` in `validation.motionPhases`. Named warning categories are acceptable only when the validator defines their exact mapping in code and report output.

## Phase 1: Scaffold The Prototype Workspace

Tasks:

- Create the `sprite-lab/` folders.
- Create the animation spec JSON.
- Add a short README or report note describing how the prototype is intended to be run.
- Decide dependency approach:
  - Node for generation wrappers and static preview generation.
  - Python with Pillow and optionally NumPy for image analysis and contact sheets.
- Add minimal dependency documentation. If adding package files, keep them scoped to the prototype.

Acceptance criteria:

- The animation spec exists and can be parsed.
- The folder structure exists.
- No image generation is required yet.

Verification:

```bash
python3 -m json.tool sprite-lab/config/cat-yawn-lay-sleep.json >/dev/null
find sprite-lab -maxdepth 3 -type d | sort
```

## Phase 2: Create A Canonical Cat Reference

Tasks:

- Generate or place one canonical cat reference image.
- The reference should be a side-view or three-quarter side-view 16-bit cat that can plausibly sit and lie down.
- Keep details simple enough to survive 128x128 review:
  - readable silhouette
  - limited palette
  - no collar text or tiny markings that will shimmer
  - no background details
  - clear body shape, head, ears, tail, paws
- Prefer `nanogen --style pixel-16bit` for first attempt if key preflight passes.
- Use `imagegen2` as comparison/fallback if `nanogen` output is inconsistent or chromakey cleanup is poor.
- Use `imagegen` only if transparent bitmap output becomes more useful than continuity controls.

Reference prompt guidance:

```text
16-bit pixel art game sprite of a small cat, side-view, compact readable silhouette,
same floor line, centered on a flat magenta background, no shadow, no text,
no extra objects, simple markings, limited 32-to-48 color palette.
```

Acceptance criteria:

- At least one reference image exists in `sprite-lab/assets/cat-yawn-lay-sleep/reference/`.
- It is readable at 128x128 and 2x/4x pixelated preview scale.
- It has a simple background or alpha that can be segmented.

Verification:

- Run a preflight/dry-run for the chosen generator before any paid generation when the skill supports it.
- Open or inspect the generated image dimensions with `file`.
- Manually approve one canonical reference before generating animation frames.

## Phase 3: Generate Candidate Still Frames

Tasks:

- Implement or manually execute a generation workflow that reads the spec and creates candidate still frames.
- Generate each frame as an individual still image.
- Always include the canonical cat reference as an image reference when the generator supports it.
- Keep pose prompts specific to one frame at a time.
- Preserve consistent constraints in every frame:
  - same cat
  - same camera angle
  - same floor line
  - same palette/style
  - same background strategy
  - no Zs
  - no extra props
- Store raw outputs under `sprite-lab/assets/cat-yawn-lay-sleep/raw/`.
- Record metadata as a first-class artifact for every candidate output:
  - generator skill
  - model
  - prompt
  - negative prompt or style preset where applicable
  - source reference path
  - seed, history ID, thought signature, or request ID where available
  - frame index
  - output path
  - retry number
  - parent candidate or neighboring reference used for regeneration
  - accepted/rejected status after review
- Use stable candidate names such as `frame-003.retry-001.png` plus `frame-003.retry-001.json`, or append equivalent records to `manifests/candidates.jsonl`.
- Maintain `manifests/accepted-frames.json` once frames are approved so later phases know which candidate belongs to each frame index.

Generation strategy:

- First pass: generate one candidate per frame using `nanogen`.
- If individual frames drift, regenerate only those frames with stricter prompts and the nearest accepted neighboring frame as an additional reference.
- If the whole sequence drifts, regenerate from a stronger reference or switch to `imagegen2` for comparison.
- Do not spend time optimizing the wrapper until at least one manually generated sequence proves the pipeline can work.

Acceptance criteria:

- Raw candidate images exist for all planned frames.
- Each frame visibly matches the intended pose label.
- No frame includes baked-in Zs, labels, or background scene elements.

Verification:

```bash
find sprite-lab/assets/cat-yawn-lay-sleep/raw -type f | sort
file sprite-lab/assets/cat-yawn-lay-sleep/raw/*
test -s sprite-lab/assets/cat-yawn-lay-sleep/manifests/candidates.jsonl
```

## Phase 4: Segment, Crop, And Align Frames

Tasks:

- Implement `align_frames.py`.
- Input: raw frame directory plus animation spec.
- Output: fixed-canvas aligned PNGs under `aligned/`.
- Convert all frames to RGBA.
- Segment the sprite:
  - If alpha exists, use `alpha > 8`.
  - If chromakey exists, remove pixels close to the configured key color.
  - Remove tiny disconnected components where practical.
- Compute per-frame:
  - bounding box
  - visible pixel area
  - centroid
  - bottom contact band
  - proposed anchor point
- Place each sprite on a fixed 128x128 canvas using the frame's configured anchor strategy:
  - `anchorY` maps to configured `floorY`.
  - `anchorX` maps to canvas center unless manual override exists.
- Support named anchors:
  - `body_bottom_center`: midpoint near the bottom of the main body silhouette.
  - `feet_center`: median bottom contact point for standing or walking frames.
  - `body_center`: centroid or bbox center for lying, floating, or ambiguous-contact frames.
  - `head_center`: useful for head-focused holds or expressions.
  - `manual`: explicit point from spec or override sidecar.
- Support per-frame anchor choices in the main spec and manual coordinate overrides in a sidecar JSON if automatic alignment is wrong.

Anchor algorithm:

```text
mask = visible pixels
bbox = bounding box(mask)
if anchor strategy is body_bottom_center or feet_center:
  bottomBand = visible pixels within 2-4 px of bbox.maxY
  anchorX = median x of bottomBand, fallback bbox.centerX
  anchorY = bbox.maxY
if anchor strategy is body_center:
  anchorX, anchorY = centroid, fallback bbox center
if anchor strategy is head_center:
  anchorX = median x of upper visible pixels
  anchorY = median y of upper visible pixels
if anchor strategy is manual:
  anchorX, anchorY = configured override
target = (canvas.width / 2, floorY)
offset = target - anchor
paste segmented sprite onto transparent canvas at offset
```

Acceptance criteria:

- Every raw frame has an aligned PNG.
- Aligned frames share identical dimensions.
- Cat body does not jump obviously when frames are played in sequence.
- Background is transparent after alignment, or consistently chromakeyed if transparency is deferred.
- Alignment output includes a metrics sidecar or validation-ready manifest with bbox, anchor, centroid, visible area, and applied offset per frame.

Verification:

```bash
python3 sprite-lab/tools/align_frames.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --input sprite-lab/assets/cat-yawn-lay-sleep/raw \
  --output sprite-lab/assets/cat-yawn-lay-sleep/aligned

file sprite-lab/assets/cat-yawn-lay-sleep/aligned/*
```

## Phase 5: Validate Sprite Consistency

Tasks:

- Implement `validate_sprites.py`.
- Input: aligned frame directory plus animation spec.
- Output:
  - `sprite-lab/reports/cat-yawn-lay-sleep.validation.json`
  - concise console table
- Treat findings as warnings unless there is a structural failure.
- Structural failures:
  - missing frame
  - unreadable image
  - inconsistent dimensions
  - empty sprite mask
- Warning metrics:
  - anchor drift
  - bbox width/height variance
  - visible area variance
  - centroid drift
  - top-of-head drift
  - adjacent silhouette overlap
  - palette or luminance outliers
- Read `validation.motionPhases` from the spec and apply relaxed or tightened thresholds for expected motion segments.
- Report warnings with phase context so intentional sit-to-lay shape changes are separated from accidental style or alignment drift.
- Implement motion-aware thresholds with this contract:
  - Start from `validation.defaultThresholds`.
  - For each adjacent frame comparison, find any `motionPhases` containing both frame indexes.
  - Apply that phase's numeric `thresholdOverrides`.
  - Emit any `ignoredWarnings` as informational notes instead of warnings.
  - Include the applied phase name and effective thresholds in `validation.json`.

Initial thresholds:

```text
anchor x jump: warn > 3 px
anchor y jump: warn > 2 px
bbox height variance: warn > 12 percent
bbox width variance: warn > 18 percent
visible area variance: warn > 20 percent
centroid jump: warn > 5 px
adjacent silhouette IoU: warn < 0.55
mean luminance shift: warn > 15 percent
dominant hue shift: warn > 12 degrees
```

Do not let thresholds override animation intent. For example, the frame where the cat lowers to the ground should legitimately change bbox height and silhouette area. The spec should encode these expected changes so warnings are useful rather than noisy.

Acceptance criteria:

- Validation report is generated.
- Structural failures are absent.
- Warnings identify likely review targets without blocking all expressive movement.
- The report distinguishes structural errors, likely drift, and expected motion changes.
- Phase-specific numeric threshold overrides are visible in the report for at least one yawn, lower-to-floor, or sleep-hold comparison.

Verification:

```bash
python3 sprite-lab/tools/validate_sprites.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --out sprite-lab/reports/cat-yawn-lay-sleep.validation.json
```

## Phase 6: Produce Review Artifacts

Tasks:

- Implement `make_contact_sheet.py`.
- Produce a PNG contact sheet in `review/` showing:
  - raw frame row
  - aligned frame row
  - bbox overlay
  - anchor marker
  - floor line
  - warning markers from validation JSON
- Add onion-skin composites:
  - previous frame in red at low opacity
  - current frame normal
  - next frame in blue at low opacity
- Keep overlays outside final sprite assets.

Acceptance criteria:

- Contact sheet exists and is readable.
- A reviewer can identify frame-to-frame jitter and obvious style drift without opening each image separately.

Verification:

```bash
python3 sprite-lab/tools/make_contact_sheet.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --raw sprite-lab/assets/cat-yawn-lay-sleep/raw \
  --aligned sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json \
  --out sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png
```

## Phase 7: Build HTML Preview

Tasks:

- Implement `make_preview.py` or a static HTML file generator.
- Preview should load aligned frames and play them as a pixelated loop.
- Provide in the first pass:
  - play/pause
  - FPS control
  - frame step controls
  - current frame label
  - transparent checkerboard background
  - separate sleeping Zs effect toggle
- Defer diagnostic overlay toggles until alignment and validation work:
  - floor line toggle
  - onion-skin toggle
  - bbox/anchor toggle
- Render Zs in HTML/CSS/canvas only during sleep frames.
- Use pixelated rendering:

```css
canvas, img {
  image-rendering: pixelated;
  image-rendering: crisp-edges;
}
```

Acceptance criteria:

- Preview opens locally without a server unless browser file restrictions require one.
- Animation loops at target FPS.
- Zs drift upward separately from the sprite during sleep frames.
- Minimal controls work before optional diagnostic overlays are added.

Verification:

```bash
python3 sprite-lab/tools/make_preview.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json \
  --out sprite-lab/preview/cat-yawn-lay-sleep.html
```

Manual verification:

- Open `sprite-lab/preview/cat-yawn-lay-sleep.html`.
- Check 1x, 2x, and intended display scale.
- Step through every frame.
- Watch the loop for jitter, style drift, and bad pose progression.

## Phase 8: Manual Review And Iteration Loop

Tasks:

- Create a manual review checklist in the summary report.
- Review frame sequence in this order:
  1. Does each frame match the intended pose?
  2. Does the cat still look like the same cat?
  3. Does the body baseline stay stable?
  4. Does the yawn read clearly?
  5. Does the transition from sitting to lying read clearly?
  6. Does the sleep pose loop or hold comfortably?
  7. Are Zs timed and positioned well when rendered separately?
- Mark frames as:
  - `accept`
  - `regenerate`
  - `manual-anchor-fix`
  - `manual-cleanup-needed`
- Regenerate only the failing frames where possible.
- Re-run alignment, validation, contact sheet, and preview after each accepted change.

Acceptance criteria:

- The first accepted animation has all frames approved manually.
- Remaining validation warnings are either fixed or documented as intentional.
- Preview demonstrates the intended yawn -> lay down -> sleep progression.

Verification:

- Save a summary report listing:
  - accepted frame set
  - generator used
  - known limitations
  - validation warning summary
  - manual approval notes

## Phase 9: Package The Prototype Result

Tasks:

- Export final aligned frames.
- Keep raw candidates and rejected frames separate.
- Preserve generation metadata, accepted frame manifests, tool versions, and reference paths.
- Write a short usage note:
  - how to regenerate
  - how to align
  - how to validate
  - how to open preview
  - which files are final vs intermediate
- If a git repo is initialized later, add generated asset folders to `.gitignore` unless the user wants sample assets tracked.

Acceptance criteria:

- A later `run-plan` pass can repeat the workflow and inspect the provenance of accepted frames. Byte-identical regeneration is not required because image models are not deterministic enough to promise that.
- Final output is easy to inspect:
  - aligned PNG frames
  - validation JSON
  - contact sheet
  - HTML preview
  - summary report
  - candidate and accepted-frame manifests

## Phase 10: Second Animation Readiness Check

Tasks:

- Define a second stationary animation spec without changing tool code. Recommended target: `cat-sit-lick-paw-sit`.
- Reuse the same pipeline sections:
  - `asset`
  - `render`
  - `generation`
  - `segmentation`
  - `alignment`
  - `validation`
  - `preview`
  - `frames`
- Create at least two frames for the second animation so alignment and validation genuinely execute:
  - Prefer two cheap/generated trial frames if budget and keys are available.
  - Otherwise create tiny synthetic placeholder frames with simple colored pixel silhouettes on the configured background.
- Run alignment and validation against the second spec and frames.
- Use this phase to verify that the tools are not hardcoded to yawn, lay, sleep, `cat-yawn-lay-sleep`, or the first spec's frame labels beyond the asset description.

Acceptance criteria:

- A second spec can be parsed by the same tooling.
- The same alignment and validation tools run successfully against the second spec's folder layout and at least two real or synthetic frames.
- The second validation report has no structural failures.
- Any cat-prototype assumptions discovered during the second spec pass are documented as follow-up work.

Verification:

```bash
python3 -m json.tool sprite-lab/config/cat-sit-lick-paw-sit.json >/dev/null
python3 sprite-lab/tools/align_frames.py --spec sprite-lab/config/cat-sit-lick-paw-sit.json --input sprite-lab/assets/cat-sit-lick-paw-sit/raw --output sprite-lab/assets/cat-sit-lick-paw-sit/aligned
python3 sprite-lab/tools/validate_sprites.py --spec sprite-lab/config/cat-sit-lick-paw-sit.json --frames sprite-lab/assets/cat-sit-lick-paw-sit/aligned --out sprite-lab/reports/cat-sit-lick-paw-sit.validation.json
```

## First Success Criteria

The prototype is successful when:

- There is a canonical 16-bit cat reference.
- There are 6-8 aligned sprite frames for yawn -> lay down -> sleep.
- All final frames share a fixed canvas and consistent background/alpha treatment.
- The cat appears to be the same character across the sequence.
- The loop reads clearly at intended game scale.
- Sleeping Zs are rendered separately in preview.
- Validation has no structural failures.
- Candidate and accepted-frame manifests preserve generation provenance.
- Validation can distinguish expected motion-phase changes from likely drift.
- Contact sheet and HTML preview make review practical.
- Manual review approves the final frame set or documents remaining issues.
- A second stationary animation spec can reuse the same pipeline shape without code restructuring.

## Risks And Mitigations

| Risk | Mitigation |
| --- | --- |
| Model changes cat proportions across frames | Use canonical reference in every generation, regenerate only failing frames, prefer `nanogen` continuity tools first. |
| Pixel art is too soft or painterly | Use stricter 16-bit prompt language, downsample carefully, audit palette, reject noisy frames. |
| No native alpha from best continuity model | Use chromakey background and local cleanup. Keep transparent output as fallback path, not first assumption. |
| Frame alignment jitters | Register by body-bottom anchor and floor line; support manual anchor overrides. |
| First implementation bakes in cat-specific assumptions | Keep spec sections reusable and add a second-animation readiness check before calling the prototype generalizable. |
| Anchor strategy fails for lying or ambiguous-contact frames | Support named anchor strategies and per-frame anchors instead of relying only on bottom contact. |
| Validation is too noisy during intentional motion | Encode motion phases and relaxed/tightened expectations in the spec. |
| Generation provenance is lost | Store candidate metadata and accepted-frame manifests as first-class artifacts. |
| Yawn or lay-down motion does not read | Use explicit pose labels and review in HTML at actual FPS; regenerate unclear pose frames. |
| Validation overflags intentional motion | Treat metrics as warnings, not final approval. Document intentional silhouette changes. |
| Prototype grows into a general animation system | Keep first target to one cat animation and defer walk cycles, directional movement, batching, and editor UX. |
| Generator costs accumulate | Dry-run when available, generate low-quality candidates first, regenerate only specific failed frames. |

## Verification Summary

Minimum verification commands after implementation:

```bash
python3 -m json.tool sprite-lab/config/cat-yawn-lay-sleep.json >/dev/null
python3 sprite-lab/tools/align_frames.py --spec sprite-lab/config/cat-yawn-lay-sleep.json --input sprite-lab/assets/cat-yawn-lay-sleep/raw --output sprite-lab/assets/cat-yawn-lay-sleep/aligned
python3 sprite-lab/tools/validate_sprites.py --spec sprite-lab/config/cat-yawn-lay-sleep.json --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned --out sprite-lab/reports/cat-yawn-lay-sleep.validation.json
python3 sprite-lab/tools/make_contact_sheet.py --spec sprite-lab/config/cat-yawn-lay-sleep.json --raw sprite-lab/assets/cat-yawn-lay-sleep/raw --aligned sprite-lab/assets/cat-yawn-lay-sleep/aligned --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json --out sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png
python3 sprite-lab/tools/make_preview.py --spec sprite-lab/config/cat-yawn-lay-sleep.json --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json --out sprite-lab/preview/cat-yawn-lay-sleep.html
test -s sprite-lab/assets/cat-yawn-lay-sleep/manifests/candidates.jsonl
test -s sprite-lab/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json
```

Manual verification:

- Open the contact sheet.
- Open the HTML preview.
- Step through each frame.
- Confirm Zs are rendered separately.
- Confirm validation warnings are resolved or documented.
- Confirm the accepted-frame manifest points to the reviewed frame set.

## Inline Review Round 1

Findings:

- The prototype needs a concrete output structure because the workspace has no app conventions.
- The plan should not require generation before scaffolding and validation tools exist.
- `nanogen` should be the continuity-first path, but the plan should not depend exclusively on it because it has no native alpha and can return JPEG.
- The first pass should allow manual generation before a robust generation wrapper. This reduces tool complexity before the visual approach is proven.

Adjustments made:

- Added a proposed folder structure.
- Split canonical reference, candidate frame generation, alignment, validation, and preview into separate phases.
- Made generated Zs a preview/runtime concern.
- Added chromakey as the default background strategy for continuity-first generation.

## Inline Critique Round 2

Potential weaknesses:

- The plan may still be too tool-heavy for a first pass if implementation builds every script before generating one image.
- Validation thresholds are borrowed heuristics and may need tuning after seeing real generated frames.
- A 128x128 fixed canvas may be too small or too large depending on the generated cat proportions.
- HTML preview might be overbuilt if contact sheets already reveal the main issues.

Resolution:

- Treat wrapper automation as incremental. Manual generation is acceptable in Phase 3.
- Keep thresholds configurable in the spec or validation script.
- Use 128x128 as the prototype target, but allow the spec to adjust it before final acceptance.
- Keep the preview simple but include essential controls because timing and jitter are hard to judge from a contact sheet alone.

## Plan Review Round 3

External review findings:

- The plan is solid for a cat prototype and has the right high-level reusable pipeline shape.
- The spec mixed reusable pipeline settings with cat-specific poses, which could make later animations harder to add.
- Alignment relied too heavily on `body_bottom_center`; future simple game animations need named anchor strategies and per-frame choices.
- Validation needed motion-phase context so intentional yawn and lay-down changes are not treated the same as unwanted drift.
- Generation metadata needed explicit paths and durable manifests.
- The first HTML preview should stay minimal until generation, alignment, and validation are proven.
- A second stationary animation check is the best proof that the pipeline is not hardcoded to the first cat sequence.
- Final review found two remaining ambiguities: symbolic `relax`/`tighten` validation semantics and a Phase 10 check that could pass without real second-animation frames.

Refinements applied:

- Reworked the animation spec into reusable sections: `asset`, `render`, `generation`, `segmentation`, `alignment`, `validation`, `preview`, and `frames`.
- Added candidate and accepted-frame manifests.
- Added named anchor strategies and per-frame anchor choices.
- Added numeric motion-phase validation overrides and an explicit validator contract for applying them.
- Slimmed the initial preview requirements and deferred optional diagnostic overlays.
- Added Phase 10 for a second-animation readiness check that must run alignment and validation on at least two generated or synthetic frames.

## Drift Log

- Refined the plan from a strong one-off cat prototype into a better first slice of a reusable simple game-animation pipeline.
- Preserved the original target animation and all unstarted phases.
- No completed phase history existed, so no completed sections required immutability protection.
- The main behavior change is that `run-plan` should build reusable spec-driven primitives from the start, while still proving them first on `cat-yawn-lay-sleep`.
- Final ambiguity fixes made validation phase behavior numeric and made the second-animation readiness check executable without relying on image-generation budget.

## Follow-up Milestones

After the first cat animation works:

- Add a second stationary animation: sit -> lick paw -> sit.
- Add breathing/sleep hold frames that loop cleanly.
- Add palette remapping to a shared sequence palette.
- Add compare mode for multiple generated variants of the same frame.
- Add optional GIF/WebP export as a derived artifact, not the source format.
- Research walk cycles separately with stricter foot-contact logic.
- Research up/down directional sprites only after side-view stationary actions are reliable.

## Progress Tracker

- [x] Phase 1: Scaffold prototype workspace and animation spec.
- [x] Phase 2: Create canonical cat reference.
- [ ] Phase 3: Generate candidate still frames.
- [ ] Phase 4: Segment, crop, and align frames.
- [ ] Phase 5: Validate sprite consistency.
- [ ] Phase 6: Produce review artifacts.
- [ ] Phase 7: Build HTML preview.
- [ ] Phase 8: Manual review and iteration loop.
- [ ] Phase 9: Package prototype result.
- [ ] Phase 10: Second animation readiness check.
