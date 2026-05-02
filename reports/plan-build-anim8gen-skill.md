# Build Anim8gen Skill Plan Report

## Phase

Phase 4: Add spec and package initialization helper.

Status: Done.

## Scope Assessment

The phase stayed within the requested helper scope. It added deterministic
package initialization and synthetic-frame helper scripts under the
repo-local `anim8gen` skill. The helpers do not call image generation APIs.

The initializer validates prepared brief fields, contiguous frame indexes,
lowercase kebab-case ids and labels, frame anchors, view values, canvas size,
working size, FPS, and retry budget. It creates the spec JSON, package
directories, `.gitkeep` files, package `.gitignore`, empty candidate manifest,
accepted-frame manifest, and package manifest. It refuses to overwrite existing
package files unless `--force` is passed.

The synthetic helper creates deterministic chroma-keyed raw PNG candidates and
candidate manifest records for local smoke tests. The skill and README now
document both helpers and clearly label synthetic frames as test fixtures, not
live `imagegen2` output. Phase 4 is marked `✅ Done` in the plan tracker.

## Tests Run

```bash
cat >/tmp/anim8gen-test-brief.json <<'JSON'
{
  "id": "test-animation",
  "subject": "test square",
  "style": "pixel art",
  "view": "side",
  "canvas": [128, 128],
  "workingSize": [1024, 1024],
  "fps": 8,
  "frames": [
    {"index": 0, "label": "idle", "pose": "idle pose"},
    {"index": 1, "label": "move", "pose": "simple moved pose"}
  ]
}
JSON
rm -rf /tmp/anim8gen-test
python3 .codex/skills/anim8gen/scripts/init_package.py --help
python3 .codex/skills/anim8gen/scripts/create_synthetic_frames.py --help
python3 .codex/skills/anim8gen/scripts/init_package.py --brief /tmp/anim8gen-test-brief.json --root /tmp/anim8gen-test
python3 -m json.tool /tmp/anim8gen-test/config/test-animation.json >/dev/null
python3 .codex/skills/anim8gen/scripts/create_synthetic_frames.py --spec /tmp/anim8gen-test/config/test-animation.json --root /tmp/anim8gen-test
test -s /tmp/anim8gen-test/assets/test-animation/raw/frame-000.retry-001.png
test -s /tmp/anim8gen-test/assets/test-animation/manifests/candidates.jsonl
find /tmp/anim8gen-test -maxdepth 3 -type d | sort
python3 -m py_compile .codex/skills/anim8gen/scripts/init_package.py .codex/skills/anim8gen/scripts/create_synthetic_frames.py
python3 .codex/skills/anim8gen/scripts/init_package.py --brief /tmp/anim8gen-test-brief.json --root /tmp/anim8gen-test >/tmp/anim8gen-overwrite.out 2>&1 && exit 1 || rg -n "already exists" /tmp/anim8gen-overwrite.out
```

## Verification Result

Passed. The required help commands work, package initialization succeeds under
an arbitrary root, the generated spec parses as JSON, the synthetic helper
creates raw PNG frames and candidate manifest records, the expected package
directories exist, both helper scripts compile, and overwrite refusal is
covered.

## Landing Result

Landed. Worktree commit `4ed5607` was cherry-picked to local `main` as
`9162eb8`, then this final landing result was amended into the current `main`
commit.

## Remaining Phases

Phase 5 through Phase 8 remain:

- Phase 5: Define imagegen2 prompt and candidate review loop.
- Phase 6: Improve preview packaging for agentic alignment.
- Phase 7: End-to-end skill trials on short animations.
- Phase 8: Documentation and handoff.
