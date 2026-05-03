# Add Solid Transparency Support To Imagegen2

## Goal

Add reliable "solid transparency" support to `github.com/zeveck/imagegen2` so
callers can keep using the `gpt-image-2` quality path while still receiving a
transparent PNG when the model produces a flat chroma-key background.

Primary target command:

```bash
node cli/generate.cjs \
  --prompt "A cute 16-bit RPG kitten sprite, centered, no text" \
  --output ./assets/kitten.png \
  --background transparent \
  --transparent-mode chroma-key \
  --chroma-key '#ff00ff' \
  --quality low
```

Expected behavior: the CLI sends an opaque `gpt-image-2` request with a solid
chroma-key background instruction, removes the chroma-key pixels locally, and
writes a transparent PNG. It records the mode, key color, request background,
and post-processing details in stdout and `.imagegen2-history.jsonl`.

## Context

- Clone researched at `external/imagegen2`, commit `bfa2bed`.
- Baseline verification: `npm test` passes, `46 passed, 0 failed`.
- Current implementation is zero-dependency Node in `cli/generate.cjs`.
- Agent skill folders bundle exact copies of `cli/generate.cjs` and
  `cli/reference.md`; tests enforce this for `.codex`, `.claude`, and
  `.gemini`.
- `--transparent-mode chroma-key` is already reserved but intentionally fails
  in `validate()`.
- Official OpenAI docs now describe transparent and opaque backgrounds for GPT
  image models generally, but this repository still treats `gpt-image-2`
  transparent output as unsupported. Keep the local chroma-key path as the
  deterministic fallback, and separately probe native support before changing
  default behavior.

## Non-goals

- Do not replace `gpt-image-2` with `gpt-image-1.5` for chroma-key mode.
- Do not add production sprite alignment, animation validation, or manual
  anchors to imagegen2; those remain Anim8gen concerns.
- Do not support JPEG transparent output.
- Do not silently overwrite existing output or history behavior.
- Do not remove `fallback-model`; it remains the native-alpha option.

## Phase 1: Define CLI Contract

- Decide and document exact semantics:
  - `--background transparent --transparent-mode chroma-key` means "generate
    opaque with `gpt-image-2`, then remove `--chroma-key` locally."
  - Output format must be PNG for the first implementation. WebP alpha can be
    a later phase unless a no-dependency encoder is already available.
  - `--chroma-key` remains a required/validated hex option with default
    `#00ff00`.
  - Add `--chroma-tolerance <0-442>` or equivalent if exact key removal is too
    brittle for model outputs. Default should be conservative and documented.
  - Add an internal prompt suffix for chroma-key mode, for example:
    `Solid flat #ff00ff chroma-key background filling the canvas, no shadows,
    no gradients, no background objects.`
- Make dry-run output show both user-facing transparent intent and actual API
  request background:
  - `transparentMode: "chroma-key"`
  - `chromaKey`
  - `background: "transparent"` in top-level user intent
  - `params.background: "opaque"` for the actual request
  - `postprocess: { type: "chroma-key", ... }`

Acceptance criteria:

- Contract is reflected in `--help`, README, `cli/reference.md`, and the Codex
  skill docs.
- Dry-run JSON is explicit enough for agents to disclose that the output is
  local chroma-key transparency, not native model alpha.

## Phase 2: Implement PNG Chroma-Key Post-processing

- Preserve zero-dependency packaging unless there is a deliberate maintainer
  decision to add a dependency.
- Add a small internal PNG helper in `cli/generate.cjs` or a local
  `cli/png.cjs` module:
  - Parse PNG signature and chunks.
  - Support 8-bit RGB and RGBA PNGs at minimum.
  - Decode PNG filters 0-4 using Node `zlib`.
  - Convert to RGBA pixels.
  - Set alpha to `0` for pixels matching the chroma key within tolerance.
  - Optionally suppress key-color spill on near-edge pixels if tests show
    visible halos.
  - Re-encode as 8-bit RGBA PNG with standard chunks and CRCs.
- Keep unsupported PNG variants fail-fast with clear JSON errors:
  - unsupported bit depth
  - unsupported color type
  - corrupt PNG
  - no key pixels found, unless `--chroma-key-allow-empty` or equivalent is
    intentionally added later
- Apply post-processing after the API response is decoded and before writing
  `outputPath`.

Acceptance criteria:

- Chroma-key mode writes a PNG with alpha channel.
- Existing opaque, auto, fallback-model, edit, mask, compression, history, and
  dry-run behavior remains unchanged.
- Failure modes are machine-readable JSON with `success: false`.

## Phase 3: Wire Validation And Request Building

- Change `validate()`:
  - Stop failing for `transparent + chroma-key`.
  - Continue failing for JPEG output.
  - Initially fail for WebP output unless WebP alpha post-processing is
    explicitly implemented.
  - Continue failing when `--transparent-mode` is used without
    `--background transparent`.
  - Keep fallback-model behavior exactly as-is.
- Add a request-normalization layer so the API request uses:
  - `model: "gpt-image-2"`
  - `background: "opaque"`
  - `output_format: "png"`
  - prompt plus chroma-key suffix
- Ensure edits endpoint uses the same normalized request behavior when
  `--image` is provided.
- Record both original args and normalized request details in dry-run, stdout,
  and history.

Acceptance criteria:

- `--background transparent --transparent-mode chroma-key --dry-run` succeeds
  and reports `gpt-image-2`.
- `fallback-model` dry-run still reports `gpt-image-1.5`.
- `reject` still rejects transparent mode with the existing guidance.

## Phase 4: Offline Tests

Update `tests/generate.test.js`:

- Replace the current "`chroma-key` is explicitly deferred" test with a
  successful dry-run test.
- Add validation tests:
  - chroma-key rejects JPEG
  - chroma-key rejects WebP if not implemented
  - chroma-key accepts PNG
  - invalid `--chroma-key` still fails
  - optional `--chroma-tolerance` accepts valid range and rejects invalid input
- Add pure post-processing tests with tiny fixture PNGs generated inside the
  test:
  - RGB PNG with exact key background becomes RGBA with transparent corners.
  - RGBA PNG preserves non-key alpha and removes key pixels.
  - near-key pixels are removed or preserved according to tolerance.
  - unsupported PNG format fails clearly.
- Keep existing bundle-copy tests passing by syncing generated CLI/reference
  files to all agent skill folders.

Acceptance criteria:

```bash
npm test
```

passes without network access.

## Phase 5: Docs And Skill Guidance

Update:

- `README.md`
- `docs/migration-from-imagegen.md`
- `cli/reference.md`
- `.codex/skills/imagegen2/SKILL.md`
- `.claude/skills/imagegen2/SKILL.md`
- `.gemini/skills/imagegen2/SKILL.md`

Document:

- Three transparency choices:
  - `reject`: fail fast when transparent is requested.
  - `fallback-model`: native alpha via `gpt-image-1.5`.
  - `chroma-key`: `gpt-image-2` opaque generation plus local solid-color
    removal.
- Recommended sprite command using `#ff00ff` or `#00ff00`.
- Prompt guidance for flat key backgrounds:
  - "solid flat chroma-key background"
  - "no shadows"
  - "no gradients"
  - "no background objects"
- Disclosure guidance for agents: tell users when transparency is local
  chroma-key cleanup rather than native alpha.

Acceptance criteria:

- `node cli/generate.cjs --help` matches the documented options.
- Skill docs point agents toward chroma-key for game sprites when maintaining
  `gpt-image-2` style quality is more important than native alpha.

## Phase 6: Live Smoke Gate

Add opt-in live smoke coverage to `scripts/smoke-live.sh`:

```bash
node cli/generate.cjs \
  --prompt "A simple red circle, centered, no text" \
  --output "$OUT_DIR/red-circle-transparent.png" \
  --background transparent \
  --transparent-mode chroma-key \
  --chroma-key '#ff00ff' \
  --quality low \
  --size 1024x1024
```

Then add a local assertion script or test helper that verifies:

- output exists
- output is PNG
- at least one pixel has alpha `0`
- at least one non-key subject pixel has alpha `255`

Acceptance criteria:

```bash
IMAGEGEN2_LIVE_TEST=1 npm run test:all
```

passes in an environment with a valid OpenAI API key.

## Phase 7: Native Transparency Probe

Because official OpenAI docs now describe transparent backgrounds for GPT image
models generally, add a tracked research task before release:

- Run a live request with `model: gpt-image-2`, `background: transparent`,
  `output_format: png`.
- If it succeeds:
  - update validation to allow native transparent mode for `gpt-image-2`
    behind an explicit mode or version gate;
  - keep chroma-key as a documented fallback for better sprite consistency.
- If it fails:
  - preserve the current fallback-model and chroma-key behavior;
  - update docs with the observed API error and date.

Acceptance criteria:

- The release notes state whether `gpt-image-2` native transparent output was
  tested and what happened.

## Verification

Run in `external/imagegen2`:

```bash
node --check cli/generate.cjs
npm test
npm run test:all
```

Optional live verification:

```bash
IMAGEGEN2_LIVE_TEST=1 npm run test:all
```

Manual verification:

- Generate a sprite with `--transparent-mode chroma-key`.
- Open the PNG over a checkerboard.
- Confirm the background is transparent and there is no obvious key-color halo.
- Confirm stdout/history show `model: gpt-image-2`, `transparentMode:
  chroma-key`, and post-processing metadata.

## Risks

- A generated "solid" background may include gradients or shadows. Mitigate
  with prompt suffixes, tolerance, live smoke checks, and clear user guidance.
- Implementing PNG parsing in a zero-dependency CLI is easy to get subtly
  wrong. Keep the supported PNG surface narrow and test filter types directly.
- Tolerance can erase subject pixels if the key color appears in the asset.
  Document key-color selection and keep defaults conservative.
- WebP alpha post-processing is not realistic without a dependency; avoid
  promising it in phase 1.
- OpenAI native transparency behavior may change. Keep chroma-key explicit and
  separately probe native support.

## Progress Tracker

- ✅ Done Clone `github.com/zeveck/imagegen2` for research.
- ✅ Done Map current CLI validation, request-building, dry-run, history, tests,
      docs, and bundled skill files.
- ✅ Done Run baseline offline tests.
- ✅ Done Define CLI contract, help/docs, chroma-key dry-run normalization, and
      conservative `--chroma-tolerance`.
- [ ] Implement CLI validation and request normalization.
- [ ] Implement PNG chroma-key post-processing.
- [ ] Add offline post-processing tests.
- [ ] Update docs and bundled skill files.
- [ ] Add opt-in live smoke coverage.
- [ ] Probe current `gpt-image-2` native transparency behavior.

## Planning Review Notes

Inline review was used rather than sub-agents because the user did not request
delegation. Devil's-advocate concerns addressed in the plan:

- Do not assume native `gpt-image-2` transparency is unavailable forever.
- Do not add a dependency casually because the current repo markets a
  zero-dependency CLI and bundles it into skills.
- Do not make agents think chroma-key output is native alpha.
- Do not leave `chroma-key` hidden behind docs only; it needs dry-run,
  history, and tests because agents inspect those JSON fields.
