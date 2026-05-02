---
name: anim8gen
description: Generate short, simple sprite animations from natural-language prompts by using imagegen2 for raster frame candidates, agentic frame review for pose and continuity, and local Anim8gen tools for alignment, validation, contact sheets, previews, and package reports.
---

# Anim8gen

Use this skill when the user asks to make a short, simple animation from text:
walk cycles, idle loops, blinks, hops, emotes, small object motion, or compact
character actions of roughly two to eight frames. The output is a reviewable
Anim8gen package, not a production animation editor.

Do not use this skill for long cinematic animation, complex multi-character
scenes, four-direction sprite packs, production-grade motion authoring, or
requests where the user only wants a single static image.

## Workflow

1. Locate the repo root. Prefer the nearest ancestor containing `anim8gen/`,
   `.codex/skills/anim8gen/`, and `.codex/skills/imagegen2/generate.cjs`.
   Installed copies may instead have this skill under
   `${CODEX_HOME:-$HOME/.codex}/skills/anim8gen`; in that case find the project
   root from the user's current working directory.
2. Parse the natural-language request into a brief: `id`, subject, style, view,
   frame count, frame labels, per-frame pose descriptions, canvas size, FPS,
   and preview-only effects. Use the defaults and limits in
   `anim8gen/config/brief.schema.json`.
3. Ask for clarification when the subject, camera view, frame count, or core
   action is ambiguous. Narrow or decline requests that exceed the first
   Anim8gen scope.
4. Initialize the package paths under `anim8gen/config/<id>.json` and
   `anim8gen/assets/<id>/` with
   `.codex/skills/anim8gen/scripts/init_package.py --brief <brief.json>`.
   Use the conventions in `anim8gen/README.md` and the reusable shape in
   `anim8gen/config/template.animation-spec.json`.
5. Locate `imagegen2`. In this repository use
   `.codex/skills/imagegen2/generate.cjs`; in an installed environment search
   `${CODEX_HOME:-$HOME/.codex}/skills/imagegen2/generate.cjs` and then any
   project-vendored `.codex/skills/imagegen2/generate.cjs`.
6. Run an `imagegen2 --dry-run` before live generation. Generate one raw frame
   candidate per spec frame into
   `anim8gen/assets/<id>/raw/frame-<index>.retry-<retry>.png`.
7. Inspect candidates before accepting them. Verify pose presence, identity
   continuity, camera continuity, sprite hygiene, segmentable background, and
   absence of text, watermarks, UI labels, extra subjects, unwanted props, or
   baked preview effects.
8. Record every attempt in
   `anim8gen/assets/<id>/manifests/candidates.jsonl`. Keep generation
   transport metadata separate from review fields: use `reviewStatus` and
   `reviewNotes` for review decisions. Preserve rejected candidates and notes;
   do not silently replace weak outputs.
9. When a frame is missing or weak, revise the prompt and retry within the
   package retry budget. If acceptable poses cannot be produced, continue with
   a partial or blocked package report instead of claiming success.
10. Write `anim8gen/assets/<id>/review/frame-reviews.json` before alignment
    succeeds or fails. Every accepted frame must have an explicit pose,
    identity, camera, hygiene, background, and decision record.
11. Align accepted frames with `anim8gen/tools/align_frames.py`, validate with
    `anim8gen/tools/validate_sprites.py`, create a contact sheet with
    `anim8gen/tools/make_contact_sheet.py`, and create an HTML preview with
    `anim8gen/tools/make_preview.py`.
12. Review the contact sheet and preview. Use spec manual anchors or
    preview-only offsets only for alignment and playback polish; regenerate
    images for wrong identity, wrong pose, wrong camera angle, or unclean
    sprite pixels.
13. Return final package paths, validation status, review warnings, rejected
    candidate summary, preview path, and remaining limitations.

## Required Package Paths

Use these paths for each animation id:

```text
anim8gen/config/<animation-id>.json
anim8gen/assets/<animation-id>/reference/
anim8gen/assets/<animation-id>/raw/frame-000.retry-001.png
anim8gen/assets/<animation-id>/aligned/frame-000.<label>.png
anim8gen/assets/<animation-id>/review/contact-sheet.png
anim8gen/assets/<animation-id>/review/frame-reviews.json
anim8gen/assets/<animation-id>/manifests/candidates.jsonl
anim8gen/assets/<animation-id>/manifests/accepted-frames.json
anim8gen/reports/<animation-id>.validation.json
anim8gen/reports/<animation-id>.package.md
anim8gen/preview/<animation-id>.html
```

The aligned frames are the sprite outputs. Raw candidates, references, aligned
PNGs, and review images may be ignored local artifacts, but JSON, JSONL,
Markdown reports, specs, and preview HTML are provenance and should be kept
with the package when the task asks for durable output.

## Imagegen2 Prompt Rules

Keep prompts frame-specific and continuity-aware:

- State the subject, style, camera view, and exact pose for that frame.
- Request a single centered subject on a solid chroma-key background, usually
  magenta `#ff00ff`, unless the spec says otherwise.
- Ask for a compact readable silhouette and full body within the canvas.
- For continuity, use a canonical reference image when available, and optionally
  use the previous accepted frame as a neighboring reference.
- Explicitly say no text, no watermark, no labels, no UI overlay, no extra
  subjects, no shadows that prevent segmentation, and no baked runtime effects.

Use `references/prompting.md` when a task needs a prompt template.

## Candidate State Model

Treat `imagegen2` output metadata and review decisions as different records.
`candidates.jsonl` is append-only provenance for every attempt. Each record
must include at least `prompt`, `frameIndex`, `frameLabel`, `outputPath`,
`retry`, `reviewStatus`, and `reviewNotes`.

Allowed `reviewStatus` values:

- `candidate`: generated or staged but not reviewed yet.
- `accepted`: accepted as the source for that spec frame.
- `accepted-with-warning`: usable source frame with documented limits.
- `rejected-pose`: wrong or unreadable requested pose.
- `rejected-identity`: different subject, style, or character identity.
- `rejected-background`: background is not segmentable or contains scene
  elements.
- `rejected-artifact`: text, watermark, labels, extra subjects, baked effects,
  crop failure, or other unusable artifact.

Normal alignment requires one `accepted` or `accepted-with-warning` candidate
for every spec frame. If that cannot be achieved within `generation.retryBudget`
then set the package state to `partial` or `blocked` and explain the gap.

`review/frame-reviews.json` is the visual review ledger. It records
`packageStatus` as `complete`, `partial`, or `blocked`, plus per-frame pose,
identity, camera, hygiene, background, decision, retry reason, and notes.
Validate these records with:

```bash
python3 .codex/skills/anim8gen/scripts/validate_review_records.py \
  --candidates anim8gen/assets/<id>/manifests/candidates.jsonl \
  --reviews anim8gen/assets/<id>/review/frame-reviews.json
```

## Agentic Review

Do not accept generated frames blindly. A frame can be accepted only after
visual inspection of the raw candidate, the contact sheet, or both.

Minimum review checks:

- Pose presence: the requested pose is visibly represented.
- Identity continuity: the same character or object appears across frames.
- Camera continuity: the requested side, front, top-down, isometric, or
  three-quarter view does not drift.
- Sprite hygiene: no text, watermarks, UI labels, unwanted props, extra
  subjects, complex background, or baked preview-only effects.
- Animation continuity: size, anchor, baseline, centroid drift, and silhouette
  changes are acceptable or documented.
- Runtime separation: preview effects stay out of source sprite pixels unless
  the user explicitly requested baked pixels.

Use `references/review-checklist.md` for candidate acceptance notes.

## Package Initialization

After parsing the user's request, write a prepared brief JSON and initialize
the package deterministically:

```bash
python3 .codex/skills/anim8gen/scripts/init_package.py \
  --brief /tmp/<id>.brief.json \
  --root anim8gen
```

The initializer creates the spec, package directories, `.gitkeep` files,
package `.gitignore`, empty candidate manifest, accepted-frame manifest, and
package manifest. It refuses to overwrite an existing package unless `--force`
is passed.

For local smoke tests only, create synthetic chroma-keyed raw frames without
calling image generation:

```bash
python3 .codex/skills/anim8gen/scripts/create_synthetic_frames.py \
  --spec anim8gen/config/<id>.json \
  --root anim8gen
```

Do not present synthetic helper frames as `imagegen2` output.

## Local Tool Commands

Replace `<id>` with the package id:

```bash
python3 anim8gen/tools/align_frames.py \
  --spec anim8gen/config/<id>.json \
  --input anim8gen/assets/<id>/raw \
  --output anim8gen/assets/<id>/aligned

python3 anim8gen/tools/validate_sprites.py \
  --spec anim8gen/config/<id>.json \
  --frames anim8gen/assets/<id>/aligned \
  --out anim8gen/reports/<id>.validation.json

python3 anim8gen/tools/make_contact_sheet.py \
  --spec anim8gen/config/<id>.json \
  --raw anim8gen/assets/<id>/raw \
  --aligned anim8gen/assets/<id>/aligned \
  --validation anim8gen/reports/<id>.validation.json \
  --out anim8gen/assets/<id>/review/contact-sheet.png

python3 anim8gen/tools/make_preview.py \
  --spec anim8gen/config/<id>.json \
  --frames anim8gen/assets/<id>/aligned \
  --validation anim8gen/reports/<id>.validation.json \
  --out anim8gen/preview/<id>.html
```

## Quality Reporting

End every run with package paths and an honest status:

- `complete`: every spec frame has an accepted or accepted-with-warning
  candidate, alignment and validation ran, contact sheet and preview exist, and
  warnings are documented.
- `partial`: at least one frame is weak or missing, but the package is useful
  for review.
- `blocked`: generation, credentials, missing tools, or invalid inputs prevent
  a meaningful package.

Include validation failures and advisory continuity drift in the package
report. Never describe a preview as final without reviewing both the generated
frames and the playback package.
