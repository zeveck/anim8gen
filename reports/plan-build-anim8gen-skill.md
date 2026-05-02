# Build Anim8gen Skill Plan Report

## Phase

Phase 7: End-to-end skill trials on short animations.

Status: Done.

## Scope Assessment

The phase stayed within the two required skill-trial workflows. Trial A adds
`deterministic-square-hop` as a deterministic local package that exercises
brief-to-spec initialization, synthetic candidate records, alignment,
validation, contact-sheet generation, preview generation, preview-only display
offset metadata, frame review JSON, accepted-frame metadata, and package
reporting.

Trial B adds `live-cat-paw-loop` as a live `imagegen2` trial scaffold. The
required dry-run preflight succeeded, but `OPENAI_API_KEY` was absent, so the
live run is honestly marked blocked. Its package includes blocked-trial
candidate and frame-review records that exercise `accepted-with-warning` and
`rejected-pose` semantics without claiming live candidate pixels exist.

Phase 7 is marked `✅ Done` in the plan tracker.

## Tests Run

```bash
python3 .codex/skills/anim8gen/scripts/init_package.py --brief <deterministic-square-hop brief>
python3 .codex/skills/anim8gen/scripts/create_synthetic_frames.py --spec anim8gen/config/deterministic-square-hop.json --root anim8gen
python3 anim8gen/tools/align_frames.py --spec anim8gen/config/deterministic-square-hop.json --input anim8gen/assets/deterministic-square-hop/raw --output anim8gen/assets/deterministic-square-hop/aligned
python3 anim8gen/tools/validate_sprites.py --spec anim8gen/config/deterministic-square-hop.json --frames anim8gen/assets/deterministic-square-hop/aligned --out anim8gen/reports/deterministic-square-hop.validation.json
python3 anim8gen/tools/make_contact_sheet.py --spec anim8gen/config/deterministic-square-hop.json --raw anim8gen/assets/deterministic-square-hop/raw --aligned anim8gen/assets/deterministic-square-hop/aligned --validation anim8gen/reports/deterministic-square-hop.validation.json --out anim8gen/assets/deterministic-square-hop/review/contact-sheet.png
python3 anim8gen/tools/make_preview.py --spec anim8gen/config/deterministic-square-hop.json --frames anim8gen/assets/deterministic-square-hop/aligned --validation anim8gen/reports/deterministic-square-hop.validation.json --out anim8gen/preview/deterministic-square-hop.html
node .codex/skills/imagegen2/generate.cjs --prompt "dry-run preflight for live-cat-paw-loop frame 0" --output /tmp/live-cat-paw-loop-dry-run.png --quality low --dry-run
python3 .codex/skills/anim8gen/scripts/init_package.py --brief <live-cat-paw-loop brief>
python3 -m json.tool anim8gen/config/deterministic-square-hop.json >/dev/null
python3 -m json.tool anim8gen/config/live-cat-paw-loop.json >/dev/null
python3 -m json.tool anim8gen/reports/deterministic-square-hop.validation.json >/dev/null
python3 .codex/skills/anim8gen/scripts/validate_review_records.py --candidates anim8gen/assets/deterministic-square-hop/manifests/candidates.jsonl --reviews anim8gen/assets/deterministic-square-hop/review/frame-reviews.json
python3 .codex/skills/anim8gen/scripts/validate_review_records.py --candidates anim8gen/assets/live-cat-paw-loop/manifests/candidates.jsonl --reviews anim8gen/assets/live-cat-paw-loop/review/frame-reviews.json
test -s anim8gen/assets/deterministic-square-hop/review/frame-reviews.json
test -s anim8gen/reports/deterministic-square-hop.package.md
if [ -z "${OPENAI_API_KEY:-}" ]; then test -s anim8gen/reports/live-cat-paw-loop.blocked.md; fi
test -s anim8gen/reports/live-cat-paw-loop.package.md || test -s anim8gen/reports/live-cat-paw-loop.blocked.md
```

## Verification Result

Passed with inline verification. The deterministic trial generated four raw
synthetic PNGs, four aligned PNGs, a validation report with zero warnings, a
contact sheet, and a static preview. Both deterministic and blocked live-trial
candidate/review records passed the local review-record validator.

Live image generation was blocked by missing `OPENAI_API_KEY`; the dry-run
preflight itself passed and is recorded in
`anim8gen/reports/live-cat-paw-loop.blocked.md`.

## Landing Result

Landed. Worktree commit `1fb4c39` was cherry-picked to local `main` as
`fe2ee41`, then this final landing result was amended into the current `main`
commit.

## Remaining Phases

Phase 8 remains:

- Phase 8: Documentation and handoff.
