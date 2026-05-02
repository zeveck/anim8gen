# Build Anim8gen Skill Plan Report

## Phase

Phase 1: Rename Prototype Workspace To Anim8gen.

Status: Done.

## Scope Assessment

The phase stayed within the requested rename scope. It moved the tracked
prototype workspace from `sprite-lab/` to `anim8gen/`, updated active
workspace references, refreshed generated path metadata produced by the
existing tools, updated generated-asset ignore comments, and marked Phase 1 as
`✅ Done` in the plan tracker.

Historical prototype plan/report references were left readable. Active
`anim8gen/` specs, manifests, reports, preview HTML, and README no longer use
the stale `sprite-lab` or `Sprite Lab` names.

## Tests Run

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

Additional inventory check:

```bash
find sprite-lab/assets -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' \) | sort >/tmp/anim8gen-image-inventory.before
sed 's#^sprite-lab/#anim8gen/#' /tmp/anim8gen-image-inventory.before > /tmp/anim8gen-image-inventory.before.transformed
diff -u /tmp/anim8gen-image-inventory.before.transformed /tmp/anim8gen-image-inventory.after.worktree
```

## Verification Result

Passed. The ignored generated image inventory matched after transforming
`sprite-lab/` paths to `anim8gen/`, `sprite-lab/` was absent in the worktree,
and the rebuilt validation/contact-sheet/preview pipeline completed with the
renamed paths.

## Landing Result

Landed. Worktree commit `5842a7aa86ffda924f30eff1dc9911d99d49e736` was
cherry-picked to local `main`, then amended with this final report text. The
ignored generated image files were then moved in the main checkout from
`sprite-lab/` to `anim8gen/` and the transformed before/after inventory
matched.

## Remaining Phases

Phase 2 through Phase 8 remain:

- Phase 2: Extract reusable Anim8gen package conventions.
- Phase 3: Create the `.codex/skills/anim8gen` skill skeleton.
- Phase 4: Add spec and package initialization helper.
- Phase 5: Define imagegen2 prompt and candidate review loop.
- Phase 6: Improve preview packaging for agentic alignment.
- Phase 7: End-to-end skill trials on short animations.
- Phase 8: Documentation and handoff.
