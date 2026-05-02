# Anim8gen

Anim8gen is a prototype workspace for building fixed-canvas sprite animation
packages from generated still frames. It keeps animation behavior
spec-driven: each sequence has a JSON spec, raw candidate images, aligned
128x128 RGBA sprite frames, validation reports, review artifacts, and optional
HTML previews.

A natural-language request such as "make a four-frame pixel art cat that sits,
lifts a paw, licks it, and sits again" is first expanded into a small brief,
then into a reusable animation spec and package folder. The cat packages in
this repo are examples and regression fixtures for that pipeline; the product
is the package convention and review workflow, not cat-specific tooling.

The current completed package is `cat-yawn-lay-sleep`, a 16-bit pixel-art cat
that sits, yawns, lies down, and sleeps. The sleeping Zs are a runtime preview
effect, not pixels baked into the sprite frames.

There is also a second readiness sequence, `cat-sit-lick-paw-sit`, that uses
local synthetic placeholder frames to prove the tools work against another
animation spec without changing tool code.

## Quick Start

Run commands from the repository root.

Install the Python image dependency:

```bash
python3 -m pip install -r anim8gen/requirements.txt
```

Regenerate the accepted `cat-yawn-lay-sleep` package:

```bash
python3 anim8gen/tools/align_frames.py \
  --spec anim8gen/config/cat-yawn-lay-sleep.json \
  --input anim8gen/assets/cat-yawn-lay-sleep/raw \
  --output anim8gen/assets/cat-yawn-lay-sleep/aligned

python3 anim8gen/tools/validate_sprites.py \
  --spec anim8gen/config/cat-yawn-lay-sleep.json \
  --frames anim8gen/assets/cat-yawn-lay-sleep/aligned \
  --out anim8gen/reports/cat-yawn-lay-sleep.validation.json

python3 anim8gen/tools/make_contact_sheet.py \
  --spec anim8gen/config/cat-yawn-lay-sleep.json \
  --raw anim8gen/assets/cat-yawn-lay-sleep/raw \
  --aligned anim8gen/assets/cat-yawn-lay-sleep/aligned \
  --validation anim8gen/reports/cat-yawn-lay-sleep.validation.json \
  --out anim8gen/assets/cat-yawn-lay-sleep/review/contact-sheet.png

python3 anim8gen/tools/make_preview.py \
  --spec anim8gen/config/cat-yawn-lay-sleep.json \
  --frames anim8gen/assets/cat-yawn-lay-sleep/aligned \
  --validation anim8gen/reports/cat-yawn-lay-sleep.validation.json \
  --out anim8gen/preview/cat-yawn-lay-sleep.html
```

Open the preview through a local static server:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory anim8gen
```

Then visit:

```text
http://127.0.0.1:8765/preview/cat-yawn-lay-sleep.html
```

## Request To Package Flow

Anim8gen keeps the agentic part explicit:

1. Parse the user request into an animation brief with subject, style, view,
   frame count, frame labels, per-frame pose descriptions, canvas size, FPS,
   and preview-only effects.
2. Convert the brief into `anim8gen/config/<animation-id>.json` using the
   reusable spec shape in `anim8gen/config/template.animation-spec.json`.
3. Create `anim8gen/assets/<animation-id>/` with `reference/`, `raw/`,
   `aligned/`, `review/`, and `manifests/` folders.
4. Generate or place raw candidates as
   `raw/frame-<index>.retry-<retry>.png`.
5. Record candidate provenance in `manifests/candidates.jsonl`; accepted
   frames and review decisions are tracked separately.
6. Align frames, validate the aligned sprites, generate a contact sheet, and
   create `preview/<animation-id>.html`.
7. Review the contact sheet and preview before declaring the package complete.

The structured brief schema lives at `anim8gen/config/brief.schema.json`.
Defaults are intentionally narrow: side-view pixel art, a 128x128 final
canvas, 1024x1024 raw generation size, 8 FPS, and a maximum of eight frames for
the first milestone. Codex should ask for clarification when subject, view,
frame count, or the core action is ambiguous. Requests for long cinematic
animation, complex scenes, four-direction packs, or production-grade motion
should be narrowed or rejected with a clear limitation.

## Package Conventions

Use lowercase kebab-case animation ids:

```text
anim8gen/config/<animation-id>.json
anim8gen/assets/<animation-id>/reference/
anim8gen/assets/<animation-id>/raw/frame-000.retry-001.png
anim8gen/assets/<animation-id>/aligned/frame-000.<label>.png
anim8gen/assets/<animation-id>/review/contact-sheet.png
anim8gen/assets/<animation-id>/manifests/candidates.jsonl
anim8gen/assets/<animation-id>/manifests/accepted-frames.json
anim8gen/assets/<animation-id>/manifests/alignment-metrics.json
anim8gen/assets/<animation-id>/manifests/package-manifest.json
anim8gen/reports/<animation-id>.validation.json
anim8gen/reports/<animation-id>.summary.md
anim8gen/reports/<animation-id>.package.md
anim8gen/preview/<animation-id>.html
```

Raw candidate filenames preserve retries. Accepted aligned frame filenames use
the spec frame label:

```text
raw/frame-002.retry-001.png
raw/frame-002.retry-002.png
aligned/frame-002.yawn-wide.png
```

Tracked provenance is JSON, JSONL, Markdown, specs, and generated HTML preview
files. Live generated bitmap assets are ignored inside each package folder:
`reference/`, `raw/`, `aligned/`, and `review/` image outputs remain local
package artifacts while `.gitkeep` files preserve the directory shape.

## Example Packages

The completed `cat-yawn-lay-sleep` example package consists of:

- `assets/cat-yawn-lay-sleep/aligned/frame-000.sit-idle.png` through
  `assets/cat-yawn-lay-sleep/aligned/frame-007.sleep-loop.png`
- `preview/cat-yawn-lay-sleep.html`
- `assets/cat-yawn-lay-sleep/review/contact-sheet.png`
- `reports/cat-yawn-lay-sleep.validation.json`
- `reports/cat-yawn-lay-sleep.summary.md`
- `assets/cat-yawn-lay-sleep/manifests/accepted-frames.json`
- `assets/cat-yawn-lay-sleep/manifests/package-manifest.json`

The raw generated candidates and reference image are intermediate provenance
assets. Keep them with the package when moving or archiving it, but use the
aligned PNGs as the actual sprite frames.

Generated bitmap assets are ignored by git on purpose. Tracked JSON and
Markdown files record package decisions and validation evidence, while the
local `reference/`, `raw/`, `aligned/`, and `review/` folders hold generated
image files.

For a concise package inventory, see
`anim8gen/reports/cat-yawn-lay-sleep.package.md`.

The `cat-sit-lick-paw-sit` package is a synthetic readiness fixture. It proves
that the same spec, alignment, validation, and reporting conventions work for
another short animation without changing tool code.

## Directory Layout

- `config/` contains animation specs. The spec is the source of truth for frame
  order, labels, canvas size, FPS, segmentation settings, alignment behavior,
  validation thresholds, and preview effects.
- `assets/<animation-id>/reference/` stores canonical reference images.
- `assets/<animation-id>/raw/` stores generated still-frame candidates. Tools
  expect names like `frame-000.retry-001.png`.
- `assets/<animation-id>/aligned/` stores fixed-canvas transparent PNG frames.
- `assets/<animation-id>/review/` stores contact sheets and review images.
- `assets/<animation-id>/manifests/` stores candidate, accepted-frame,
  alignment, and package metadata.
- `tools/` contains the alignment, validation, contact-sheet, and preview
  scripts.
- `preview/` contains generated local HTML previews.
- `reports/` contains validation, readiness, package, and manual review
  reports.

## Animation Specs

Each animation is described by `anim8gen/config/<animation-id>.json`.

Important fields:

- `id`: folder and report identifier for the animation.
- `asset`: subject, style, canonical reference path, and prompt traits.
- `render.canvas`: final sprite canvas, currently `[128, 128]`.
- `render.workingSize`: expected raw generation size, currently `[1024, 1024]`.
- `render.fps`: default preview playback rate.
- `generation`: preferred generation skill and manifest paths.
- `segmentation`: background removal settings. Current frames use magenta
  chroma-key cleanup.
- `alignment.floorY`: target shared floor line in the final canvas.
- `alignment.defaultAnchor`: automatic anchor strategy for frames that do not
  specify another anchor.
- `alignment.manualOverrides`: explicit raw-image anchor points for reviewed
  frames that need hand alignment.
- `validation.defaultThresholds`: structural and advisory continuity checks.
- `validation.motionPhases`: threshold overrides for known large movements.
- `preview.runtimeEffects`: non-sprite effects rendered by the preview, such as
  `sleeping-zs`.
- `frames`: ordered frame definitions with `index`, `label`, `pose`, and
  optional `anchor`.

Start from `anim8gen/config/template.animation-spec.json` for a new package.
The template includes frame labels, pose descriptions, alignment settings,
validation thresholds, preview strategy, runtime effects, and image generation
manifest paths. The cat specs are examples of the same schema, not required
inputs for the tools.

Brief-to-spec expansion uses these defaults unless the user request says
otherwise:

- `style`: `pixel art`
- `view`: `side`
- `canvas`: `[128, 128]`
- `workingSize`: `[1024, 1024]`
- `fps`: `8`
- `maxFrameCount`: `8`
- `segmentation.strategy`: `chroma-key`
- `segmentation.chromaKey`: `#ff00ff`
- `alignment.defaultAnchor`: `body_bottom_center`

Ask for clarification instead of guessing when a request omits the subject,
uses an unclear camera direction, asks for an unspecified number of distinct
poses, or combines unrelated actions that cannot fit the max frame count.
Unsupported broad requests should be narrowed into a short loop or reported as
out of scope.

Output file names are derived from each frame definition:

```text
frame-<index>.<label>.png
```

For example, frame index `6` with label `lying-head-down` becomes:

```text
frame-006.lying-head-down.png
```

## Tool Workflow

### 1. Generate Or Place Raw Candidates

The current package was generated with AI image tooling, then reviewed and
accepted as raw candidates. The tooling expects raw files in:

```text
anim8gen/assets/<animation-id>/raw/
```

Use this naming convention:

```text
frame-000.retry-001.png
frame-001.retry-001.png
frame-002.retry-001.png
```

The aligner uses the first sorted `frame-<index>.retry-*.png` file for each
frame listed in the spec.

Raw frames should use the configured chroma-key background, currently magenta
`#ff00ff`, so the aligner can isolate the sprite silhouette.

### 2. Align Frames

Run:

```bash
python3 anim8gen/tools/align_frames.py \
  --spec anim8gen/config/<animation-id>.json \
  --input anim8gen/assets/<animation-id>/raw \
  --output anim8gen/assets/<animation-id>/aligned
```

The aligner:

- loads each raw candidate as RGBA;
- removes chroma-key background pixels;
- keeps the largest visible connected component;
- computes the sprite bounding box and anchor;
- scales all frames consistently to fit the configured canvas;
- places each frame on the shared `floorY`;
- writes aligned PNG frames to `aligned/`;
- writes `assets/<animation-id>/manifests/alignment-metrics.json`.

Use `manualOverrides` in the spec when automatic anchors produce clipping,
floor drift, or bad centering.

### 3. Validate Frames

Run:

```bash
python3 anim8gen/tools/validate_sprites.py \
  --spec anim8gen/config/<animation-id>.json \
  --frames anim8gen/assets/<animation-id>/aligned \
  --out anim8gen/reports/<animation-id>.validation.json
```

The validator checks:

- every expected frame exists;
- images are readable;
- dimensions match the configured canvas;
- frames are RGBA;
- visible sprite masks are non-empty;
- adjacent frames stay within configured continuity thresholds.

Structural failures mean the package is not usable. Warnings are review
signals for motion, silhouette, luminance, or color drift. Some warnings can be
acceptable for deliberate motion; document accepted warnings in a summary
report.

### 4. Generate A Contact Sheet

Run:

```bash
python3 anim8gen/tools/make_contact_sheet.py \
  --spec anim8gen/config/<animation-id>.json \
  --raw anim8gen/assets/<animation-id>/raw \
  --aligned anim8gen/assets/<animation-id>/aligned \
  --validation anim8gen/reports/<animation-id>.validation.json \
  --out anim8gen/assets/<animation-id>/review/contact-sheet.png
```

The contact sheet is the fastest manual review surface. It shows raw
candidates, aligned frames, anchor and floor overlays, validation warning
markers, and onion-skin comparisons.

Use it to review:

- clipping at canvas edges;
- foot or body floor-line drift;
- sudden size changes;
- accidental background remnants;
- pose readability;
- whether warnings are expected motion or real problems.

### 5. Generate The HTML Preview

Run:

```bash
python3 anim8gen/tools/make_preview.py \
  --spec anim8gen/config/<animation-id>.json \
  --frames anim8gen/assets/<animation-id>/aligned \
  --validation anim8gen/reports/<animation-id>.validation.json \
  --out anim8gen/preview/<animation-id>.html
```

The preview is a static HTML file. It references the local aligned PNG files by
relative path instead of embedding image bytes.

Start a static server from `anim8gen/`:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory anim8gen
```

Then open:

```text
http://127.0.0.1:8765/preview/<animation-id>.html
```

The current preview includes playback, pause, frame stepping, FPS control,
frame thumbnails, checkerboard background toggle, frame labels, validation
warning indicators, and runtime sleeping Zs for sleep frames.

## Manual Review Loop

Use this loop after generating or changing frames:

1. Align the raw candidates.
2. Validate the aligned frames.
3. Generate the contact sheet.
4. Generate the HTML preview.
5. Review the contact sheet for clipping, drift, and inconsistent silhouette.
6. Review the preview for readable motion at the intended FPS.
7. If needed, add `alignment.manualOverrides` to the spec and rerun the tools.
8. Record accepted frames in `assets/<animation-id>/manifests/accepted-frames.json`.
9. Record review decisions in `reports/<animation-id>.summary.md`.
10. Update or create `assets/<animation-id>/manifests/package-manifest.json`
    when the package is ready to hand off.

For the completed cat package, manual review added explicit anchors for frames
0, 5, 6, and 7 to avoid clipping and keep lying poses on the shared floor line.

## Adding A New Animation

To add another sequence:

1. Translate the request into a prepared brief JSON. The brief must follow
   `anim8gen/config/brief.schema.json`, with contiguous frame indexes and
   lowercase kebab-case frame labels.
2. Initialize the package skeleton:

```bash
python3 .codex/skills/anim8gen/scripts/init_package.py \
  --brief /tmp/<animation-id>.brief.json \
  --root anim8gen
```

The initializer writes `anim8gen/config/<animation-id>.json`, creates package
folders, adds `.gitkeep` files, adds a package `.gitignore`, initializes
`manifests/candidates.jsonl`, and creates initial accepted-frame and package
manifests. It refuses to overwrite an existing package unless `--force` is
passed.

For deterministic smoke tests without paid image generation, create synthetic
chroma-keyed raw frames:

```bash
python3 .codex/skills/anim8gen/scripts/create_synthetic_frames.py \
  --spec anim8gen/config/<animation-id>.json \
  --root anim8gen
```

Synthetic frames are test fixtures only. They are not a substitute for live
`imagegen2` coverage.

The initializer creates these folders:

```text
anim8gen/assets/<animation-id>/reference/
anim8gen/assets/<animation-id>/raw/
anim8gen/assets/<animation-id>/aligned/
anim8gen/assets/<animation-id>/review/
anim8gen/assets/<animation-id>/manifests/
```

Then:

3. Add or generate a canonical reference image in `reference/`.
4. Generate raw candidates into `raw/` using `frame-<index>.retry-<n>.png`
   names.
5. Write `manifests/candidates.jsonl` with enough provenance to understand how
   each candidate was produced.
6. Run alignment, validation, contact-sheet, and preview commands with the new
   spec path and animation id.
7. Use validation reports and contact sheets to tune thresholds or manual
   anchors.
8. Write accepted-frame and package manifests once the sequence is ready.

The `cat-sit-lick-paw-sit` readiness sequence is a minimal example of a second
spec using the same tools. Its report is
`anim8gen/reports/cat-sit-lick-paw-sit.readiness.md`.

## Generated Asset Policy

Generated bitmap outputs are intentionally ignored by git. This keeps the
repository small while allowing local package folders to contain working
assets.

Ignored generated files include:

- reference images;
- raw generated candidates;
- aligned PNG frames;
- review contact sheets.

Tracked files include:

- specs in `config/`;
- tool scripts in `tools/`;
- HTML previews in `preview/`;
- metadata manifests in `assets/<animation-id>/manifests/`;
- reports in `reports/`;
- `.gitkeep` files for empty directories.

If someone checks out the repo without the ignored bitmap assets, they will
have the specs, scripts, previews, manifests, and reports, but not the local
raw or aligned PNG files. To rebuild the same package, restore the ignored
asset files from the package archive or regenerate candidates from the recorded
provenance.

## Dependencies

Anim8gen uses Python 3 and Pillow:

```text
Pillow==12.2.0
```

Pillow is used for loading images, RGBA conversion, chroma-key segmentation,
resizing, alpha-mask checks, contact-sheet rendering, and overlay drawing.

The prototype does not require a package lockfile. Install dependencies with:

```bash
python3 -m pip install -r anim8gen/requirements.txt
```

## Troubleshooting

### `ModuleNotFoundError: No module named 'PIL'`

Install dependencies:

```bash
python3 -m pip install -r anim8gen/requirements.txt
```

### Missing Raw Frame

The aligner requires one raw file for every frame listed in the spec. Check
that the raw directory contains names like:

```text
frame-000.retry-001.png
```

The frame index must match the spec's `frames[].index`.

### Empty Sprite Mask

The aligner or validator could not find non-background pixels. Check that:

- the raw image has an alpha channel or visible RGB sprite pixels;
- the background matches the configured chroma key;
- the sprite is not accidentally the same color as the chroma-key background;
- `segmentation.chromaTolerance` is not too broad.

### Clipping Or Bad Floor Alignment

Use the contact sheet overlays first. If automatic anchoring is wrong, add a
manual anchor to `alignment.manualOverrides` in the spec:

```json
"manualOverrides": {
  "5": {
    "anchor": [494, 771],
    "reason": "Keep the lying pose on the same floor line as adjacent frames."
  }
}
```

Then rerun alignment, validation, contact-sheet generation, and preview
generation.

### Validation Warnings

Warnings do not always mean failure. Large intended motions, such as lowering
from sitting to lying down, can need looser `motionPhases` thresholds. Keep
threshold overrides narrow and phase-specific, then document accepted warnings
in the sequence summary report.

### Preview Does Not Show Images

Serve `anim8gen/` with a local HTTP server and open the preview through that
server. The HTML uses relative paths to local aligned PNGs, so opening the file
from another directory can break image loading.

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory anim8gen
```

## Current Reports

- `reports/cat-yawn-lay-sleep.package.md`: package inventory and rebuild
  commands for the completed cat prototype.
- `reports/cat-yawn-lay-sleep.summary.md`: manual review notes and accepted
  warning context.
- `reports/cat-yawn-lay-sleep.validation.json`: validation evidence for the
  accepted eight-frame package.
- `reports/cat-sit-lick-paw-sit.readiness.md`: second-animation readiness
  check.
- `reports/cat-sit-lick-paw-sit.validation.json`: validation evidence for the
  three-frame synthetic readiness sequence.
