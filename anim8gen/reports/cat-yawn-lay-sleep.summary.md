# Cat Yawn Lay Sleep Review Summary

## Accepted Frame Set

All eight generated `imagegen2` candidates are accepted for the first prototype after manual anchor adjustments in the animation spec.

| Frame | Label | Review status | Note |
| --- | --- | --- | --- |
| 000 | sit-idle | accept | Manual anchor fix removed right-edge clipping. |
| 001 | yawn-start | accept | Yawn starts clearly. |
| 002 | yawn-wide | accept | Full yawn reads clearly. |
| 003 | yawn-end | accept | Mouth closes into a sleepy expression. |
| 004 | lowering | accept | Intentional large silhouette change toward the floor. |
| 005 | lying-head-up | accept | Manual anchor fix keeps the body on the floor line. |
| 006 | lying-head-down | accept | Sleep pose works with preview-rendered Zs. |
| 007 | sleep-loop | accept | Subtle sleep-hold shape difference is acceptable for this prototype. |

## Generator And Provenance

- Generator: `imagegen2`
- Model: `gpt-image-2`
- Reference: `anim8gen/assets/cat-yawn-lay-sleep/reference/cat-reference.jpg`
- Candidate metadata: `anim8gen/assets/cat-yawn-lay-sleep/manifests/candidates.jsonl`
- Accepted manifest: `anim8gen/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json`

## Manual Approval Notes

- The cat remains a consistent orange tabby with the same side-view camera across the sequence.
- The sequence reads as sit, yawn, lower, lie down, and sleep at the preview FPS.
- Sleeping Zs are rendered separately in HTML and are not baked into the sprite frames.
- The first review found right-edge clipping on frame 000 and floor-line mismatch on frames 005 through 007. These were corrected with spec-level manual anchor overrides, then alignment, validation, contact sheet generation, and preview generation were rerun.

## Validation Warning Summary

The latest validation report has zero structural failures and 14 advisory warnings.

Warnings accepted as intentional or acceptable for the first prototype:

- `000->001`: horizontal and centroid movement caused by transitioning from relaxed sit to yawn-start after correcting frame 000 clipping.
- `003->004`: large bbox, centroid, and IoU changes caused by the sit-to-lower pose transition.
- `004->005`: anchor movement caused by switching from lowering to fully lying on the floor line.
- `005->006`: head-lowering and lying-pose shape change.
- `006->007`: sleep-hold size variation representing a subtle breathing/resting pose change.

## Known Limitations

- The frames are generated candidates and may still shimmer in markings during close inspection.
- Manual anchors are source-image specific; regenerated frames should rerun review before reusing these exact coordinates.
- The first prototype does not include palette remapping or automatic regeneration decisions.

## Verification

- Contact sheet reviewed: `anim8gen/assets/cat-yawn-lay-sleep/review/contact-sheet.png`
- Preview reviewed in Chromium through a local static server: `http://127.0.0.1:8766/preview/cat-yawn-lay-sleep.html`
- Browser checks covered frame rendering, thumbnail frame selection, play/pause, next-frame stepping, and sleep-frame Z activation.
