# Deterministic Square Hop Package

## Status

`complete`

This Trial A package converts the request "make a four-frame pixel art blue
square that squashes, hops, and lands" into a deterministic Anim8gen package
without calling paid image generation.

## Outputs

- Spec: `anim8gen/config/deterministic-square-hop.json`
- Candidate manifest: `anim8gen/assets/deterministic-square-hop/manifests/candidates.jsonl`
- Accepted frames: `anim8gen/assets/deterministic-square-hop/manifests/accepted-frames.json`
- Frame reviews: `anim8gen/assets/deterministic-square-hop/review/frame-reviews.json`
- Alignment metrics: `anim8gen/assets/deterministic-square-hop/manifests/alignment-metrics.json`
- Validation: `anim8gen/reports/deterministic-square-hop.validation.json`
- Contact sheet: `anim8gen/assets/deterministic-square-hop/review/contact-sheet.png`
- Preview: `anim8gen/preview/deterministic-square-hop.html`

The raw, aligned, and contact-sheet PNGs are generated assets and remain
ignored by git. The tracked manifests and reports preserve the package
provenance.

## Review Decisions

All four synthetic candidates were accepted. They use the
`anim8gen-test-helper` generator and are suitable only for deterministic local
pipeline coverage, not visual quality evaluation of `imagegen2`.

The `hop-up` frame has a preview-only display offset:

```json
{"x": 0, "y": -6}
```

That offset exaggerates the hop apex in HTML playback only. It is not baked
into the raw or aligned sprite frames and does not change the accepted-frame
review verdict.

## Validation

Validation passed with zero warnings across all adjacent frame comparisons.

## Limitations

This trial verifies package initialization, synthetic candidate records,
alignment, validation, contact-sheet generation, preview generation, preview
offset metadata, and package reporting. It does not verify live model pose
quality or identity continuity.
