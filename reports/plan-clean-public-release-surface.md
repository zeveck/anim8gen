# Clean Public Release Surface Report

## Phase

Phase 2: Prune staging surface

Status: ✅ Done

Scope assessment: Scoped to public release staging cleanup. Removed previously tracked generated package asset metadata/placeholders, generated local preview HTML, validation JSON, and package reports from the index while leaving source specs, tools, docs, and durable Markdown reports in the repo. Documented `deterministic-square-hop` as the retained tiny regression fixture spec; its generated outputs stay local and ignored. Did not include `.codex/skills/imagegen`, `.codex/skills/imagegen2`, `.codex/skills/nanogen`, duplicate root GIFs, or exploratory untracked configs.

Tests run:

- `git ls-files -ci --exclude-standard`
- `git diff --stat --cached`
- `git status --short`
- `git diff --cached --name-only | rg '^(\\.codex/skills/(imagegen|imagegen2|nanogen)|anim8gen-demo|anim8gen-demo2)' || true`

Verification result: Passed. The staged surface consists of generated-output removals plus documentation, plan tracker, and this report. No imagegen/imagegen2/nanogen skill changes or duplicate root GIFs are staged.

Landing result: Pending cherry-pick to `main`.

Remaining phases:

- Phase 3: GIF flag integration
- Phase 4: Tests
- Phase 5: Public demo sanity
