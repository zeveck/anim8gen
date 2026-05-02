# Build Anim8gen Skill

## Goal

Turn the cat sprite animation prototype into a repo-local Codex skill named
`anim8gen`.

The intended user experience is natural language:

```text
anim8gen make a four-frame pixel art cat that sits, lifts a paw, licks it, and sits again
```

or, in clients that expose skill aliases as slash commands:

```text
/anim8gen make a two-frame side-view walk cycle for a tiny pixel adventurer
```

The skill should use `imagegen2` for raster frame candidates, then apply
agentic review and local tooling to turn imperfect still images into a short,
reviewable HTML animation package.

## Context

- The current prototype lives under `sprite-lab/`.
- The prototype proved these reusable pieces:
  - JSON animation specs.
  - Frame candidate manifests.
  - Pillow-based chroma-key segmentation and fixed-canvas alignment.
  - Validation reports for structural failures and advisory continuity drift.
  - Contact sheets for human and agent review.
  - Static HTML previews using JavaScript playback.
  - A second synthetic cat sequence that reuses the alignment and validation
    tools without cat-specific tool changes.
- The previous plan did not explicitly require a Codex skill wrapper. It built
  the backend prototype shape.
- `imagegen2` cannot directly produce animation and cannot be trusted to
  reliably produce every requested pose on the first attempt. The skill must
  control generation, inspect returned images, retry or revise prompts when
  needed, and use preview/layout adjustments to make accepted frames animate
  coherently.

## Product Intent

`anim8gen` creates simple, short animations from text prompts. It is for small
game-like sprite actions, not production-grade animation authoring.

Good initial targets:

- Two-frame or four-frame walk cycles.
- A cat sitting, lifting a paw, licking it, and returning to sitting.
- A curled-up cat standing, stretching, lying down, and returning to curled.
- Small idle loops, blinks, hops, emotes, or simple object motions.

The generated output should include:

- Raw generated frame candidates.
- Accepted aligned frames.
- A validation report.
- A review contact sheet.
- A static HTML preview.
- A package report explaining what was generated, warnings, and how to rerun.

The implementation should finish with at least two test runs:

- one deterministic local test that exercises the spec, alignment, validation,
  contact-sheet, and preview pipeline without calling paid image generation;
- one live `imagegen2` test when credentials are available, with a clear
  blocked report if credentials are absent.

## Non-goals

- Do not build a full animation editor.
- Do not promise fluent motion for broad or complex actions.
- Do not attempt four-direction movement as the first skill milestone.
- Do not rely on `imagegen2` to solve pose continuity without agentic review.
- Do not bake preview effects such as labels, Zs, motion guides, or UI overlays
  into sprite frames unless the user explicitly asks for those pixels.
- Do not keep the user-facing project name `sprite-lab`.

## Target Naming

Rename user-facing and code-facing prototype paths from `sprite-lab` to
`anim8gen`.

Target repo layout:

```text
anim8gen/
  README.md
  requirements.txt
  config/
  assets/
  tools/
  preview/
  reports/
.codex/
  skills/
    anim8gen/
      SKILL.md
      scripts/
      references/
      assets/
```

The `anim8gen/` directory is the working output area and reference prototype.
The `.codex/skills/anim8gen/` directory is the reusable skill interface loaded
by Codex.

The existing `scripts/install-codex-skills.sh` installs vendored skills from
`.codex/skills/` into `${CODEX_HOME:-$HOME/.codex}/skills`. The new skill must
work with that installer rather than requiring a separate installation path.

## Skill Behavior

When the skill is invoked, Codex should:

1. Parse the natural-language request into a small animation brief:
   - subject;
   - style;
   - view direction;
   - frame count;
   - frame labels;
   - per-frame pose descriptions;
   - canvas size;
   - FPS;
   - runtime effects or preview-only overlays.
2. Create an animation package folder under `anim8gen/assets/<animation-id>/`.
3. Write a machine-readable spec under `anim8gen/config/<animation-id>.json`.
4. Generate or request raw frame candidates with `imagegen2`.
5. Inspect generated candidates before accepting them:
   - verify the requested subject appears;
   - verify each pose roughly matches its frame description;
   - reject frames with text, watermarks, extra subjects, wrong camera angle,
     baked effects, or unusable backgrounds;
   - retry with revised prompts when a necessary pose is missing or too weak;
   - preserve rejected candidate metadata for traceability.
6. Align accepted frames on a fixed canvas.
7. Validate structural and continuity properties.
8. Generate a contact sheet.
9. Generate a static HTML preview.
10. Review the preview and contact sheet. Use alignment offsets or spec manual
    anchors when that produces a better animation without regenerating images.
11. Report final paths, validation status, warnings, and remaining limitations.

## HTML Animation Strategy

The skill should not assume one fixed rendering technique.

Acceptable preview implementations:

- Canvas playback of aligned frame PNGs.
- An `overflow: hidden` viewport with absolutely positioned frame images and
  per-frame offsets.
- CSS or JavaScript runtime effects layered separately from sprite pixels.

The agent should choose the simplest technique that makes the specific
animation reviewable. The first implementation can keep the current canvas
preview, but the skill guidance should allow per-frame offsets or overflow
containers when they better solve alignment.

## Agentic Review Requirements

The skill must explicitly include review loops because this is the core value
over raw image generation.

Minimum review checks:

- Pose presence: each accepted frame must visibly represent the requested pose.
- Identity continuity: the same character or object should appear across
  frames.
- Camera continuity: side view/top-down/front view should not drift unless
  requested.
- Sprite hygiene: no text, watermarks, UI labels, unwanted props, baked effects,
  or complex backgrounds.
- Animation continuity: frame size, anchor point, baseline, and centroid drift
  should be either acceptable or documented.
- Runtime separation: preview effects stay out of the sprite frames unless the
  user explicitly asks for baked pixels.

The skill should allow bounded retries. If generation cannot produce acceptable
poses after the retry budget, it should return the best package plus a clear
quality report instead of pretending the result is good.

## Phase 1: Rename Prototype Workspace To Anim8gen

### Scope

- Move `sprite-lab/` to `anim8gen/`.
- Update all tracked references in:
  - specs;
  - manifests;
  - reports;
  - preview HTML;
  - README;
  - package report;
  - plan/report files where current commands need to remain executable.
- Update generated-asset ignore rules.
- Preserve ignored generated bitmap files during the move. The current package
  relies on local ignored raw, aligned, reference, and review PNG/JPG files for
  rebuild verification.
- Before moving, write an inventory of ignored generated image files with:
  `find sprite-lab/assets -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' \) | sort`.
  After moving, compare the same paths transformed from `sprite-lab/` to
  `anim8gen/`, and fail the phase if any generated image was lost.
- Preserve any pre-existing README edits by transforming the current file
  content rather than replacing it from an old committed copy.
- Keep historical plan reports readable, but prefer current paths in active
  docs and package metadata.

### Acceptance Criteria

- `rg -n "sprite-lab|Sprite Lab" anim8gen .codex plans reports` returns only
  intentionally historical references, if any.
- Existing rebuild commands work using `anim8gen/...` paths.
- Ignored generated bitmap assets remain ignored after the move.
- Ignored generated bitmap assets that existed before the move still exist
  under `anim8gen/assets/...` after the move.
- The README describes `anim8gen`, not `sprite-lab`.
- Active specs, manifests, reports, preview HTML, and README do not contain
  stale `sprite-lab` or `Sprite Lab` references.

### Verification

```bash
find anim8gen/assets -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' \) | sort >/tmp/anim8gen-image-inventory.after
test ! -d sprite-lab
python3 -m json.tool anim8gen/config/cat-yawn-lay-sleep.json >/dev/null
python3 -m json.tool anim8gen/config/cat-sit-lick-paw-sit.json >/dev/null
python3 -m py_compile anim8gen/tools/align_frames.py anim8gen/tools/validate_sprites.py anim8gen/tools/make_contact_sheet.py anim8gen/tools/make_preview.py
python3 anim8gen/tools/align_frames.py --spec anim8gen/config/cat-yawn-lay-sleep.json --input anim8gen/assets/cat-yawn-lay-sleep/raw --output anim8gen/assets/cat-yawn-lay-sleep/aligned
python3 anim8gen/tools/validate_sprites.py --spec anim8gen/config/cat-yawn-lay-sleep.json --frames anim8gen/assets/cat-yawn-lay-sleep/aligned --out anim8gen/reports/cat-yawn-lay-sleep.validation.json
python3 anim8gen/tools/make_contact_sheet.py --spec anim8gen/config/cat-yawn-lay-sleep.json --raw anim8gen/assets/cat-yawn-lay-sleep/raw --aligned anim8gen/assets/cat-yawn-lay-sleep/aligned --validation anim8gen/reports/cat-yawn-lay-sleep.validation.json --out anim8gen/assets/cat-yawn-lay-sleep/review/contact-sheet.png
python3 anim8gen/tools/make_preview.py --spec anim8gen/config/cat-yawn-lay-sleep.json --frames anim8gen/assets/cat-yawn-lay-sleep/aligned --validation anim8gen/reports/cat-yawn-lay-sleep.validation.json --out anim8gen/preview/cat-yawn-lay-sleep.html
test -s anim8gen/assets/cat-yawn-lay-sleep/raw/frame-000.retry-001.png
test -s anim8gen/assets/cat-yawn-lay-sleep/aligned/frame-000.sit-idle.png
test -s anim8gen/assets/cat-yawn-lay-sleep/review/contact-sheet.png
! rg -n "sprite-lab|Sprite Lab" anim8gen/config anim8gen/assets/*/manifests anim8gen/reports anim8gen/preview anim8gen/README.md
git status --short --ignored=matching
```

## Phase 2: Extract Reusable Anim8gen Package Conventions

### Scope

- Refactor docs and reports so `cat-yawn-lay-sleep` is an example package, not
  the product itself.
- Define package conventions for:
  - animation ids;
  - raw candidate filenames;
  - accepted frame manifests;
  - validation report paths;
  - contact sheet paths;
  - preview paths;
  - package reports.
- Add a reusable template spec or documented spec skeleton.
- Add a brief schema, either as `anim8gen/config/brief.schema.json` or as a
  precise documented schema in `anim8gen/README.md`, covering defaults,
  constraints, unsupported request handling, ambiguity policy, max frame count,
  id generation, and example brief expansions.
- Preserve the existing cat examples as initial targets and regression
  fixtures.
- Add a clear distinction between reusable package schema and example-specific
  cat content.

### Acceptance Criteria

- `anim8gen/README.md` explains how a new natural-language animation request
  maps to a spec and package folder.
- The cat examples are documented as examples, not hardcoded requirements.
- The spec template includes frame labels, pose descriptions, alignment
  settings, validation thresholds, and preview strategy.
- The brief schema defines defaults and limits, including initial max frame
  count, canvas defaults, FPS defaults, and when Codex should ask for
  clarification instead of guessing.
- Package conventions include where live generated assets are ignored and where
  tracked provenance lives.

### Verification

```bash
python3 -m json.tool anim8gen/config/cat-yawn-lay-sleep.json >/dev/null
python3 -m json.tool anim8gen/config/cat-sit-lick-paw-sit.json >/dev/null
test -s anim8gen/README.md
rg -n "cat-yawn-lay-sleep|cat-sit-lick-paw-sit|template|natural language|imagegen2|max frame|clarification|unsupported" anim8gen/README.md anim8gen/config
```

## Phase 3: Create The `.codex/skills/anim8gen` Skill Skeleton

### Scope

- Add `.codex/skills/anim8gen/SKILL.md`.
- Add concise skill instructions that trigger for requests to generate short,
  simple animations from text prompts.
- Reference `imagegen2` as the generation skill and the local Anim8gen tools as
  the packaging backend.
- Include a concrete end-to-end runbook:
  - locate the repo root;
  - locate `imagegen2` at `.codex/skills/imagegen2/generate.cjs` or an
    installed skill path;
  - initialize the package;
  - generate or dry-run candidates;
  - review candidates;
  - align, validate, create contact sheet, create preview, and write report;
  - return final package paths and quality status.
- Include clear limits: short actions, bounded frame counts, agentic review,
  retries, and quality reporting.
- Add skill resources only where they are directly useful:
  - scripts for deterministic helper steps;
  - references for prompt/review guidance;
  - no extra README inside the skill.
- Ensure the existing project skill installer picks up `anim8gen`.

### Acceptance Criteria

- The skill frontmatter name is exactly `anim8gen`.
- The skill description clearly covers natural-language short animation
  generation and agentic frame review.
- The body tells Codex when to use `imagegen2`, how to inspect candidates, and
  how to package outputs.
- The skill avoids obsolete `sprite-lab` naming.
- Running `scripts/install-codex-skills.sh` installs an `anim8gen` skill into
  a temporary `CODEX_HOME`.

### Verification

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('.codex/skills/anim8gen/SKILL.md').read_text()
assert 'name: anim8gen' in text
assert 'imagegen2' in text
assert 'agentic' in text.lower() or 'review' in text.lower()
for token in ['repo root', 'generate.cjs', 'align', 'validate', 'contact sheet', 'preview', 'package paths']:
    assert token.lower() in text.lower(), token
assert 'sprite-lab' not in text
print('skill ok')
PY
tmp_codex_home="$(mktemp -d)"
CODEX_HOME="$tmp_codex_home" bash scripts/install-codex-skills.sh
test -s "$tmp_codex_home/skills/anim8gen/SKILL.md"
```

## Phase 4: Add Spec And Package Initialization Helper

### Scope

- Add a deterministic helper script that creates a package scaffold from
  structured arguments or a prepared JSON brief.
- The helper should not call image generation APIs.
- It should create:
  - spec JSON;
  - package directories;
  - `.gitkeep` files where needed;
  - empty or initialized manifests.
- Codex remains responsible for translating natural language into the initial
  brief, but the script should make the file operations reliable.
- The helper should support deterministic smoke-test briefs so the skill can be
  tested without calling `imagegen2`.
- Add a deterministic synthetic frame helper for tests. It should create simple
  chroma-keyed raw PNGs and candidate manifest records from a spec or brief,
  but it must be clearly labeled as a test helper rather than a substitute for
  live `imagegen2` coverage.

### Acceptance Criteria

- A new package can be initialized without hand-writing directory structure.
- The helper validates frame indexes and labels.
- The helper refuses to overwrite an existing package unless explicitly told to
  do so.
- The generated spec can be parsed by existing tools.
- The helper emits paths that match the `anim8gen/` package conventions.
- The synthetic helper can create raw frames for `deterministic-square-hop`
  under an arbitrary root.

### Verification

```bash
cat >/tmp/anim8gen-test-brief.json <<'JSON'
{
  "id": "test-animation",
  "subject": "test square",
  "style": "pixel art",
  "view": "side",
  "canvas": [128, 128],
  "workingSize": [1024, 1024],
  "fps": 8,
  "frames": [
    {"index": 0, "label": "idle", "pose": "idle pose"},
    {"index": 1, "label": "move", "pose": "simple moved pose"}
  ]
}
JSON
python3 .codex/skills/anim8gen/scripts/init_package.py --help
python3 .codex/skills/anim8gen/scripts/create_synthetic_frames.py --help
python3 .codex/skills/anim8gen/scripts/init_package.py --brief /tmp/anim8gen-test-brief.json --root /tmp/anim8gen-test
python3 -m json.tool /tmp/anim8gen-test/config/test-animation.json >/dev/null
python3 .codex/skills/anim8gen/scripts/create_synthetic_frames.py --spec /tmp/anim8gen-test/config/test-animation.json --root /tmp/anim8gen-test
test -s /tmp/anim8gen-test/assets/test-animation/raw/frame-000.retry-001.png
test -s /tmp/anim8gen-test/assets/test-animation/manifests/candidates.jsonl
find /tmp/anim8gen-test -maxdepth 3 -type d | sort
```

## Phase 5: Define Imagegen2 Prompt And Candidate Review Loop

### Scope

- Add skill guidance and optional helper templates for generating per-frame
  `imagegen2` prompts.
- Specify how to use references:
  - generate or choose a canonical reference;
  - use it for identity/style continuity;
  - optionally use prior accepted frames as neighboring references.
- Define bounded retries and candidate status values:
  - `candidate`;
  - `accepted`;
  - `rejected-pose`;
  - `rejected-identity`;
  - `rejected-background`;
  - `rejected-artifact`;
  - `accepted-with-warning`.
- Define state transitions and terminal package states:
  - every spec frame needs one `accepted` or `accepted-with-warning` candidate
    before normal alignment;
  - `packageStatus` must be `complete`, `partial`, or `blocked`;
  - retry budget defaults to a small numeric value and must be recorded.
- Record all attempts in `manifests/candidates.jsonl`.
- Define the review record schema separately from the raw `imagegen2` response
  so review status is not confused with generation transport metadata.
- Add `review/frame-reviews.json` to record visual review verdicts for pose,
  identity, camera, hygiene, background, decision, retry reason, and notes.

### Acceptance Criteria

- The skill tells Codex not to accept generated frames blindly.
- The prompt template keeps backgrounds segmentable and avoids baked preview
  effects.
- Candidate manifests record prompt, frame index, output path, retry number,
  review status, and notes.
- Retry guidance is bounded and reports quality honestly when candidates remain
  weak.
- Rejected candidate records preserve enough information to understand why a
  retry was requested.
- The plan requires Codex to inspect raw candidates or the contact sheet and
  write per-frame review notes before claiming acceptance.
- Candidate JSONL and frame review JSON have schema or validator coverage.

### Verification

```bash
rg -n "candidate|accepted|rejected|retry|imagegen2|reference|pose|packageStatus|frame-reviews|retry budget" .codex/skills/anim8gen anim8gen/README.md
python3 -m json.tool anim8gen/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json >/dev/null
python3 - <<'PY'
from pathlib import Path
text = Path('.codex/skills/anim8gen/SKILL.md').read_text()
for token in ['rejected-pose', 'rejected-identity', 'accepted-with-warning', 'retry budget', 'packageStatus', 'frame-reviews.json']:
    assert token in text
print('candidate review guidance ok')
PY
```

## Phase 6: Improve Preview Packaging For Agentic Alignment

### Scope

- Update the preview generator or skill guidance so the agent may choose:
  - canvas playback of aligned frames;
  - per-frame offsets in an overflow-hidden container;
  - runtime overlays or effects outside sprite pixels.
- Preserve the current canvas preview as the default.
- Define `preview.displayOffsets` and `preview.runtimeEffects` in the spec or
  preview config and update `make_preview.py` to consume them.
- Document when to prefer image regeneration versus preview/layout alignment.
- Keep preview alignment metadata separate from source-frame acceptance
  metadata so a display offset does not imply the underlying frame is a better
  pose than it is.

### Acceptance Criteria

- Existing `cat-yawn-lay-sleep` preview still works.
- The skill can describe per-frame preview offsets without modifying source
  image pixels.
- Preview effects remain separate from sprite frames by default.
- The package report records any preview-only offsets or runtime effects.
- Trial A exercises at least one preview-only offset or runtime overlay and
  documents that it was not baked into source frames.

### Verification

```bash
python3 anim8gen/tools/make_preview.py --spec anim8gen/config/cat-yawn-lay-sleep.json --frames anim8gen/assets/cat-yawn-lay-sleep/aligned --validation anim8gen/reports/cat-yawn-lay-sleep.validation.json --out anim8gen/preview/cat-yawn-lay-sleep.html
python3 -m http.server 8765 --bind 127.0.0.1 --directory anim8gen &
server_pid=$!
trap 'kill "$server_pid"' EXIT
playwright-cli open http://127.0.0.1:8765/preview/cat-yawn-lay-sleep.html
playwright-cli eval '() => ({canvasBytes: document.querySelector("canvas")?.toDataURL().length, thumbs: document.querySelectorAll(".thumb").length})'
playwright-cli click "Next"
playwright-cli eval '() => document.querySelector("#frameLabel")?.textContent'
```

## Phase 7: End-To-End Skill Trials On Short Animations

### Scope

- Run two small target workflows that are not identical to the original cat
  yawn sequence.
- Trial A is `deterministic-square-hop`, deterministic and local. It may use synthetic generated frames to
  verify package initialization, alignment, validation, contact-sheet, preview,
  and report plumbing without calling paid image generation.
- Trial B is `live-cat-paw-loop`, a live `imagegen2` trial for a cat that sits,
  lifts a paw, licks it, and returns to sitting.
- Always run an `imagegen2 --dry-run` preflight for Trial B. If
  `OPENAI_API_KEY` or dry-run preflight is unavailable, write
  `anim8gen/reports/live-cat-paw-loop.blocked.md`, still create a mocked
  candidate manifest that exercises retry/rejection semantics, and do not claim
  live image generation passed.

### Acceptance Criteria

- `deterministic-square-hop` converts a natural-language request into a spec and completes with
  deterministic local frames.
- `deterministic-square-hop` produces aligned frames, validation, contact sheet,
  HTML preview, preview-only offset evidence, frame review JSON, and package
  report.
- `live-cat-paw-loop` either produces a live `imagegen2` package with reviewed candidates or
  produces a blocked report that names the missing credential or generation
  blocker.
- `live-cat-paw-loop` dry-run preflight is recorded even when live generation is
  blocked.
- At least one trial exercises the candidate review record format, including an
  accepted frame and either a rejected candidate or an accepted-with-warning
  note.
- Package reports document review decisions, warnings, rejected candidates, and
  final limitations.

### Verification

```bash
python3 -m json.tool anim8gen/config/deterministic-square-hop.json >/dev/null
python3 .codex/skills/anim8gen/scripts/create_synthetic_frames.py --spec anim8gen/config/deterministic-square-hop.json --root anim8gen
python3 anim8gen/tools/align_frames.py --spec anim8gen/config/deterministic-square-hop.json --input anim8gen/assets/deterministic-square-hop/raw --output anim8gen/assets/deterministic-square-hop/aligned
python3 anim8gen/tools/validate_sprites.py --spec anim8gen/config/deterministic-square-hop.json --frames anim8gen/assets/deterministic-square-hop/aligned --out anim8gen/reports/deterministic-square-hop.validation.json
python3 anim8gen/tools/make_contact_sheet.py --spec anim8gen/config/deterministic-square-hop.json --raw anim8gen/assets/deterministic-square-hop/raw --aligned anim8gen/assets/deterministic-square-hop/aligned --validation anim8gen/reports/deterministic-square-hop.validation.json --out anim8gen/assets/deterministic-square-hop/review/contact-sheet.png
python3 anim8gen/tools/make_preview.py --spec anim8gen/config/deterministic-square-hop.json --frames anim8gen/assets/deterministic-square-hop/aligned --validation anim8gen/reports/deterministic-square-hop.validation.json --out anim8gen/preview/deterministic-square-hop.html
test -s anim8gen/assets/deterministic-square-hop/review/frame-reviews.json
test -s anim8gen/reports/deterministic-square-hop.package.md
node .codex/skills/imagegen2/generate.cjs --prompt "dry-run preflight for live-cat-paw-loop frame 0" --output /tmp/live-cat-paw-loop-dry-run.png --quality low --dry-run
if [ -z "${OPENAI_API_KEY:-}" ]; then test -s anim8gen/reports/live-cat-paw-loop.blocked.md; fi
test -s anim8gen/reports/live-cat-paw-loop.package.md || test -s anim8gen/reports/live-cat-paw-loop.blocked.md
```

## Phase 8: Documentation And Handoff

### Scope

- Update `anim8gen/README.md` to describe:
  - the public `/anim8gen` intent;
  - how the repo-local skill works;
  - how examples are organized;
  - how to view previews;
  - how to interpret validation and review reports.
- Add or update package reports for any new skill trial.
- Ensure the previous prototype plan report points to the new skill plan for
  continuation.
- Include the two test runs from Phase 7 in the handoff docs, including whether
  the live `imagegen2` trial passed or was blocked.

### Acceptance Criteria

- A developer can understand the difference between:
  - the `anim8gen/` working output area;
  - the `.codex/skills/anim8gen/` Codex skill.
- The README describes natural-language animation requests, not just manual
  command sequences.
- The docs explain `imagegen2` limitations and why agentic review is required.
- The docs explain how to run the deterministic smoke trial and the live
  `imagegen2` trial.
- The docs state that installing to the real `${CODEX_HOME:-$HOME/.codex}` is
  optional handoff, while verification uses a temporary `CODEX_HOME`.

### Verification

```bash
test -s anim8gen/README.md
test -s .codex/skills/anim8gen/SKILL.md
rg -n "natural language|imagegen2|review|preview|contact sheet|validation|Codex skill" anim8gen/README.md .codex/skills/anim8gen/SKILL.md
rg -n "deterministic-square-hop|live-cat-paw-loop|Trial A|Trial B|blocked|temporary CODEX_HOME" anim8gen/README.md anim8gen/reports
rg -n "sprite-lab|Sprite Lab" anim8gen .codex/skills/anim8gen
```

## Cross-Phase Verification

Run after the final phase:

```bash
python3 -m py_compile anim8gen/tools/align_frames.py anim8gen/tools/validate_sprites.py anim8gen/tools/make_contact_sheet.py anim8gen/tools/make_preview.py
python3 -m json.tool anim8gen/config/cat-yawn-lay-sleep.json >/dev/null
python3 -m json.tool anim8gen/config/cat-sit-lick-paw-sit.json >/dev/null
python3 anim8gen/tools/align_frames.py --spec anim8gen/config/cat-yawn-lay-sleep.json --input anim8gen/assets/cat-yawn-lay-sleep/raw --output anim8gen/assets/cat-yawn-lay-sleep/aligned
python3 anim8gen/tools/validate_sprites.py --spec anim8gen/config/cat-yawn-lay-sleep.json --frames anim8gen/assets/cat-yawn-lay-sleep/aligned --out anim8gen/reports/cat-yawn-lay-sleep.validation.json
python3 anim8gen/tools/align_frames.py --spec anim8gen/config/cat-sit-lick-paw-sit.json --input anim8gen/assets/cat-sit-lick-paw-sit/raw --output anim8gen/assets/cat-sit-lick-paw-sit/aligned
python3 anim8gen/tools/validate_sprites.py --spec anim8gen/config/cat-sit-lick-paw-sit.json --frames anim8gen/assets/cat-sit-lick-paw-sit/aligned --out anim8gen/reports/cat-sit-lick-paw-sit.validation.json
python3 - <<'PY'
from pathlib import Path
skill = Path('.codex/skills/anim8gen/SKILL.md').read_text()
assert 'name: anim8gen' in skill
assert 'imagegen2' in skill
assert 'sprite-lab' not in skill
print('anim8gen skill metadata ok')
PY
tmp_codex_home="$(mktemp -d)"
CODEX_HOME="$tmp_codex_home" bash scripts/install-codex-skills.sh
test -s "$tmp_codex_home/skills/anim8gen/SKILL.md"
```

## Risks And Mitigations

| Risk | Mitigation |
| ---- | ---------- |
| Rename loses ignored generated assets | Move ignored files carefully and verify with `git status --ignored=matching` plus rebuild commands. |
| Historical reports become noisy after path rename | Keep old plan reports understandable, but update active package metadata and docs to current paths. |
| Skill becomes too script-heavy and hides agent judgment | Keep scripts deterministic for scaffolding/tooling only; keep candidate review and prompt revision explicit in `SKILL.md`. |
| `imagegen2` produces inconsistent poses | Require bounded retries, candidate review statuses, contact sheets, and honest quality reports. |
| Preview offsets mask fundamentally wrong poses | Document when offsetting is acceptable and require regeneration for wrong identity, wrong pose, or wrong camera angle. |
| Skill overpromises complex animation | Limit first version to short, simple actions and report limitations. |
| Tests depend on paid image generation | Require one deterministic local trial and one separately reported live `imagegen2` trial. |
| Skill installs but cannot actually run | Require a concrete skill runbook, helper path resolution, temp `CODEX_HOME` installer verification, and end-to-end trial reports. |
| Visual review is claimed without evidence | Require `review/frame-reviews.json`, package report notes, and contact-sheet or raw-frame inspection before acceptance. |
| Preview server verification blocks automation | Run the server in the background with cleanup and use Playwright checks instead of a foreground server command. |

## Plan Review

Refinement was rerun with two independent sub-agent reviewers plus a local
sanity pass.

- Reviewer 1 focused on product and skill behavior. Incorporated findings for
  a concrete skill runbook, brief schema/defaults, candidate state transitions,
  frame review artifacts, preview offset schema, and `imagegen2` dry-run
  integration when live credentials are missing.
- Reviewer 2 focused on execution risk. Incorporated findings for bounded
  preview-server verification, concrete trial IDs, deterministic synthetic
  frame helper, temp `CODEX_HOME` install checks, pre/post generated-asset
  inventories, active-path stale-name checks, and explicit live credential
  gating.
- Local sanity pass fixed duplicated plan text and kept the previous inline
  review insights that still apply.

## Drift Log

- The original prototype plan produced reusable backend tooling but not the
  intended `/anim8gen` skill interface.
- This plan now treats `anim8gen/` as the working output area and
  `.codex/skills/anim8gen/` as the Codex skill.
- The generated-asset rename is now called out as a first-class risk because
  required raw, aligned, reference, and review images are intentionally ignored
  by git.
- The end-to-end phase now requires `deterministic-square-hop` and
  `live-cat-paw-loop` so the skill can be checked both without paid generation
  and, when credentials are present, with real `imagegen2` candidate review.
- The skill plan now requires visual review evidence instead of relying on
  grep-only checks for agentic review behavior.

## Progress Tracker

- [ ] Phase 1: Rename prototype workspace to Anim8gen.
- [ ] Phase 2: Extract reusable Anim8gen package conventions.
- [ ] Phase 3: Create the `.codex/skills/anim8gen` skill skeleton.
- [ ] Phase 4: Add spec and package initialization helper.
- [ ] Phase 5: Define imagegen2 prompt and candidate review loop.
- [ ] Phase 6: Improve preview packaging for agentic alignment.
- [ ] Phase 7: End-to-end skill trials on short animations.
- [ ] Phase 8: Documentation and handoff.
