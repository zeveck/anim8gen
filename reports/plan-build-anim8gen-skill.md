# Build Anim8gen Skill Plan Report

## Phase

Phase 6: Improve preview packaging for agentic alignment.

Status: Done.

## Scope Assessment

The phase stayed within preview packaging and agentic alignment scope. It
keeps canvas playback as the default preview strategy, adds spec-level
`preview.displayOffsets` for playback-only x/y shifts, and makes
`preview.runtimeEffects` drive whether runtime overlays such as sleeping Zs
are shown.

The implementation keeps preview metadata separate from accepted-frame review
metadata: display offsets affect only HTML playback and do not change source
sprite pixels, accepted candidate quality, or validation results. The README,
skill runbook, template spec, brief schema, package initializer, cat specs, and
cat package report now document that separation.

Phase 6 is marked `✅ Done` in the plan tracker.

## Tests Run

```bash
python3 -m py_compile anim8gen/tools/make_preview.py .codex/skills/anim8gen/scripts/init_package.py
python3 -m json.tool anim8gen/config/cat-yawn-lay-sleep.json >/dev/null
python3 -m json.tool anim8gen/config/cat-sit-lick-paw-sit.json >/dev/null
python3 -m json.tool anim8gen/config/brief.schema.json >/dev/null
python3 anim8gen/tools/make_preview.py --spec anim8gen/config/cat-yawn-lay-sleep.json --frames anim8gen/assets/cat-yawn-lay-sleep/aligned --validation anim8gen/reports/cat-yawn-lay-sleep.validation.json --out anim8gen/preview/cat-yawn-lay-sleep.html
python3 -m http.server 8765 --bind 127.0.0.1 --directory anim8gen
playwright-cli open http://127.0.0.1:8765/preview/cat-yawn-lay-sleep.html
playwright-cli eval '() => ({canvasBytes: document.querySelector("canvas")?.toDataURL().length, thumbs: document.querySelectorAll(".thumb").length, zHidden: document.querySelector("#zToggle")?.closest(".toggle")?.hidden, frameLabel: document.querySelector("#frameLabel")?.textContent})'
playwright-cli snapshot
playwright-cli click e13
playwright-cli eval '() => document.querySelector("#frameLabel")?.textContent'
rg -n "displayOffsets|runtimeEffects|canvas-playback|preview-only offsets|preview-only display offsets|wrong identity|wrong pose|wrong camera" anim8gen/README.md .codex/skills/anim8gen/SKILL.md anim8gen/config anim8gen/reports/cat-yawn-lay-sleep.package.md
```

The Playwright console contained one expected static-server 404 for
`/favicon.ico`; sprite frame assets loaded successfully.

## Verification Result

Passed with inline verification. The preview generator compiled, all changed
JSON parsed, the cat preview regenerated, Playwright confirmed a non-empty
canvas data URL, eight thumbnails, visible sleeping-Z controls for the package
that requests them, and working Next-frame interaction.

## Landing Result

Landed. Worktree commit `5cad89f` was cherry-picked to local `main` as
`9fc3eb1`, then this final landing result was amended into the current `main`
commit.

## Remaining Phases

Phase 7 through Phase 8 remain:

- Phase 7: End-to-end skill trials on short animations.
- Phase 8: Documentation and handoff.
