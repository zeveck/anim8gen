# Build Anim8gen Skill Plan Report

## Phase

Phase 8: Documentation and handoff.

Status: Done.

## Scope Assessment

The phase stayed within documentation and handoff scope. It updates
`anim8gen/README.md` to distinguish the public `/anim8gen` natural-language
skill intent from the `anim8gen/` working output area, documents the
`.codex/skills/anim8gen/` Codex skill, explains preview, validation, contact
sheet, and review-report interpretation, and records why `imagegen2` requires
agentic candidate review instead of blind acceptance.

The older prototype plan report now points to `plans/build-anim8gen-skill.md`
as the continuation path. Phase 7 Trial A and Trial B reports already existed;
the README now references the deterministic package result and the blocked
live `imagegen2` trial result.

Phase 8 is marked `✅ Done` in the plan tracker.

## Tests Run

```bash
test -s anim8gen/README.md
test -s .codex/skills/anim8gen/SKILL.md
rg -n "natural language|imagegen2|review|preview|contact sheet|validation|Codex skill" anim8gen/README.md .codex/skills/anim8gen/SKILL.md >/tmp/phase8-doc-keywords.txt
rg -n "deterministic-square-hop|live-cat-paw-loop|Trial A|Trial B|blocked|temporary CODEX_HOME" anim8gen/README.md anim8gen/reports >/tmp/phase8-trial-keywords.txt
! rg -n "sprite-lab|Sprite Lab" anim8gen .codex/skills/anim8gen
```

Final cross-phase verification after landing:

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

## Verification Result

Passed with inline verification. The documentation contains the required skill
handoff language, trial references, validation/review/preview terms, and no
stale `sprite-lab` or `Sprite Lab` references under active Anim8gen paths.
Final cross-phase verification also passed on `main`; the cat package
validators preserved the known advisory warnings for intentional motion, and
the temporary `CODEX_HOME` installer check installed the vendored Anim8gen
skill successfully.

Remote freshness could not be checked because the repository has no usable
`origin` remote configured.

## Landing Result

Landed. Worktree commit `c919fca` was cherry-picked to local `main` as
`d4def3b`, then this final landing and cross-phase verification result was
amended into the current local `main` commit.

## Remaining Phases

None. Phase 8 was the final planned phase.
