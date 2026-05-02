# Build Anim8gen Skill Plan Report

## Phase

Phase 2: Extract Reusable Anim8gen Package Conventions.

Status: Done.

## Scope Assessment

The phase stayed within the requested package-conventions scope. It updated
`anim8gen/README.md` to describe natural-language request expansion,
animation-id and package path conventions, ignored generated asset policy,
brief defaults, ambiguity handling, unsupported request handling, and the cat
packages as examples rather than product-specific requirements.

It also added `anim8gen/config/brief.schema.json` for structured request
briefs and `anim8gen/config/template.animation-spec.json` as the reusable spec
skeleton covering frame labels, pose descriptions, alignment settings,
validation thresholds, preview strategy, and manifest paths. Phase 2 is marked
`✅ Done` in the plan tracker.

## Tests Run

```bash
python3 -m json.tool anim8gen/config/cat-yawn-lay-sleep.json >/dev/null
python3 -m json.tool anim8gen/config/cat-sit-lick-paw-sit.json >/dev/null
python3 -m json.tool anim8gen/config/brief.schema.json >/dev/null
python3 -m json.tool anim8gen/config/template.animation-spec.json >/dev/null
test -s anim8gen/README.md
rg -n "cat-yawn-lay-sleep|cat-sit-lick-paw-sit|template|natural language|imagegen2|max frame|clarification|unsupported" anim8gen/README.md anim8gen/config
```

## Verification Result

Passed. The existing cat specs and the new brief/schema template files parse
as JSON, the README exists, and the required convention, template, natural
language, `imagegen2`, max frame, clarification, and unsupported-request terms
are present in `anim8gen/README.md` and `anim8gen/config`.

## Landing Result

Landed. Worktree commit `8fb1a9ca125e15c7c2beaf69a5b8ab6801e037dd` was
cherry-picked to local `main` as `83c6a4b`, then amended with this final
landing result in the current `main` commit.

## Remaining Phases

Phase 3 through Phase 8 remain:

- Phase 3: Create the `.codex/skills/anim8gen` skill skeleton.
- Phase 4: Add spec and package initialization helper.
- Phase 5: Define imagegen2 prompt and candidate review loop.
- Phase 6: Improve preview packaging for agentic alignment.
- Phase 7: End-to-end skill trials on short animations.
- Phase 8: Documentation and handoff.
