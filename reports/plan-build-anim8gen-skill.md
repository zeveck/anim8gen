# Build Anim8gen Skill Plan Report

## Phase

Phase 5: Define imagegen2 prompt and candidate review loop.

Status: Done.

## Scope Assessment

The phase stayed within the candidate review and prompt-loop scope. It refined
the skill runbook and README so `imagegen2` transport metadata is separate from
Anim8gen review decisions, documented bounded retry states, and required
`review/frame-reviews.json` before claiming frame acceptance.

The package initializer now creates a review ledger, package ignore rules allow
review JSON and Markdown to be tracked, the synthetic helper emits candidate
review status plus `frame-reviews.json`, and a validator checks candidate JSONL
and frame review JSON records. Existing cat example packages now include
tracked frame review ledgers.

Phase 5 is marked `✅ Done` in the plan tracker.

## Tests Run

```bash
python3 -m py_compile .codex/skills/anim8gen/scripts/init_package.py .codex/skills/anim8gen/scripts/create_synthetic_frames.py .codex/skills/anim8gen/scripts/validate_review_records.py
rg -n "candidate|accepted|rejected|retry|imagegen2|reference|pose|packageStatus|frame-reviews|retry budget" .codex/skills/anim8gen anim8gen/README.md
python3 -m json.tool anim8gen/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json >/dev/null
python3 -m json.tool anim8gen/assets/cat-yawn-lay-sleep/review/frame-reviews.json >/dev/null
python3 -m json.tool anim8gen/assets/cat-sit-lick-paw-sit/review/frame-reviews.json >/dev/null
python3 - <<'PY'
from pathlib import Path
text = Path('.codex/skills/anim8gen/SKILL.md').read_text()
for token in ['rejected-pose', 'rejected-identity', 'accepted-with-warning', 'retry budget', 'packageStatus', 'frame-reviews.json']:
    assert token in text
print('candidate review guidance ok')
PY
cat >/tmp/anim8gen-phase5-brief.json <<'JSON'
{
  "id": "phase-five-test",
  "subject": "test square",
  "style": "pixel art",
  "view": "side",
  "canvas": [128, 128],
  "workingSize": [1024, 1024],
  "fps": 8,
  "frames": [
    {"index": 0, "label": "idle", "pose": "idle pose"},
    {"index": 1, "label": "hop", "pose": "hop pose"}
  ]
}
JSON
rm -rf /tmp/anim8gen-phase5-test
python3 .codex/skills/anim8gen/scripts/init_package.py --brief /tmp/anim8gen-phase5-brief.json --root /tmp/anim8gen-phase5-test
python3 .codex/skills/anim8gen/scripts/create_synthetic_frames.py --spec /tmp/anim8gen-phase5-test/config/phase-five-test.json --root /tmp/anim8gen-phase5-test
python3 .codex/skills/anim8gen/scripts/validate_review_records.py --candidates /tmp/anim8gen-phase5-test/assets/phase-five-test/manifests/candidates.jsonl --reviews /tmp/anim8gen-phase5-test/assets/phase-five-test/review/frame-reviews.json
test -s /tmp/anim8gen-phase5-test/assets/phase-five-test/review/frame-reviews.json
```

## Verification Result

Passed with inline verification. The required Phase 5 grep and metadata checks
pass, both existing review ledgers parse as JSON, the new scripts compile, and
the validator accepts a deterministic initialized package after synthetic frame
generation.

## Landing Result

Landed. Worktree commit `e32383b` was cherry-picked to local `main` as
`9a5c506`, then this final landing result was amended into the current `main`
commit.

## Remaining Phases

Phase 6 through Phase 8 remain:

- Phase 6: Improve preview packaging for agentic alignment.
- Phase 7: End-to-end skill trials on short animations.
- Phase 8: Documentation and handoff.
