# Live Cat Paw Loop Package

## Status

`blocked`

The package scaffold was created for a four-frame cat paw loop, and the
required `imagegen2 --dry-run` preflight succeeded. Live generation was blocked
because `OPENAI_API_KEY` was absent.

## Outputs

- Spec: `anim8gen/config/live-cat-paw-loop.json`
- Package manifest: `anim8gen/assets/live-cat-paw-loop/manifests/package-manifest.json`
- Candidate manifest: `anim8gen/assets/live-cat-paw-loop/manifests/candidates.jsonl`
- Frame reviews: `anim8gen/assets/live-cat-paw-loop/review/frame-reviews.json`
- Blocked report: `anim8gen/reports/live-cat-paw-loop.blocked.md`

## Review Decisions

No live candidate pixels were generated. The tracked review records are mocked
blocked-trial evidence only:

- Frame 0 uses `accepted-with-warning` to record that a dry-run placeholder can
  flow through the review schema while remaining visually unverified.
- Frame 1 uses `rejected-pose` to record the retry/rejection branch that would
  be used when a required paw-lift pose is missing.

## Limitations

This trial verifies live preflight plumbing, blocked credential reporting, and
candidate review semantics. It does not verify live image quality, pose
matching, identity continuity, camera continuity, segmentation, alignment, or
preview output for the cat sequence.
