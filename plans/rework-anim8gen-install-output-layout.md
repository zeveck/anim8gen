# Rework anim8gen Install and Output Layout

## Goal

Make anim8gen install and run cleanly in a user's repository without placing a visible `anim8gen/` workbench full of runtime machinery, intermediate files, and this repo's demo configs in the project root.

The visible repo-root `anim8gen/` workbench is itself the UX bug. Even without
demo cruft, it exposes too much implementation detail: frequently changing
tools, schemas, manifests, reports, retries, alignment state, and development
docs. Normal users should see finished animation assets, not the pipeline.

New runs should separate:

- installed skill/runtime code
- hidden per-run working state and provenance
- user-visible deliverables
- this repository's public demo surface

The end state should feel simple after a clean README install:

- no visible repo-root `anim8gen/` directory is required for normal use
- no copied demo specs, demo reports, or development docs appear in the user's project
- finished frames, preview HTML, requested GIFs, and package summaries are easy to find
- raw candidates remain available when they add value, but are not forced into the user's face; for many transparent-background runs they are visually redundant with final frames and mostly add noise

## Research Notes

- GitHub's ignore-file guidance frames generated local files as a normal `.gitignore` use case, especially files that should not be shared with collaborators. Source: <https://docs.github.com/en/get-started/git-basics/ignoring-files>
- Python's `tempfile` module is the standard library path for creating temporary files and directories safely when files do not need to be durable project artifacts. Source: <https://docs.python.org/3/library/tempfile.html>
- The XDG Base Directory Specification separates persistent user data, cache, runtime, and state. Even though anim8gen is project-local, the same principle applies: do not mix durable deliverables with cache/intermediate state. Source: <https://specifications.freedesktop.org/basedir-spec/latest/>
- The Filesystem Hierarchy Standard distinguishes temporary files from files that must persist across reboots. Use `/tmp` only for genuinely disposable or recoverable intermediates. Source: <https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch03s18.html>

## Current Findings

- The skill still instructs agents to create packages under `anim8gen/config/<id>.json`, `anim8gen/assets/<id>/`, `anim8gen/preview/<id>.html`, `anim8gen/reports/<id>.*`, and `anim8gen/gifs/<id>.gif`.
- The README demo links and images already use `public/**`, so this repo's public demo pages do not need the runtime demo specs and old reports under `anim8gen/`.
- `git ls-files anim8gen/config anim8gen/reports` currently includes demo specs such as `quality-cat-pounce-v2.json`, `pirate-ship-kraken-cannon.json`, and `sci-fi-space-station-explosion.json`, plus old report markdown. Those are being copied during a basic install when the installer copies the repo's `anim8gen/` subtree.
- `init_package.py` accepts `--root`, but generated spec and manifest fields still hard-code `anim8gen/assets`, `anim8gen/config`, `anim8gen/preview`, and `anim8gen/reports`. The root override is therefore incomplete.
- `make_preview.py` currently computes frame URLs with an assumption that the preview output is two levels below a shared root. Hidden run state plus exported preview bundles will need either copied colocated assets or a more robust relative path calculation.
- `.gitignore` currently hides `anim8gen/assets`, `anim8gen/preview/*.html`, generated report JSON/package markdown, and GIF outputs, but it does not solve the install UX because the root directory, tooling, config templates, demo specs, and old reports are still visible.
- `anim8gen/tools` are reusable project tooling, but exposing them as a copied root workbench is not necessary if the skill can find bundled tools or install a minimal hidden runtime.
- The current layout makes pipeline churn visible. Changes to alignment, validation, preview generation, retries, and manifests appear as repo-root files even though most users only want frames, a GIF, and a preview page.

## Directory Contract

Adopt this contract for new installs and new runs:

```text
<skill-dir>/
  SKILL.md
  references/
  scripts/
  runtime/
    tools/
    config/
      brief.schema.json
      template.animation-spec.json

<user-project>/
  .anim8gen/
    runs/<id>/
      config/<id>.json
      reference/
      raw/
      aligned/
      review/
      manifests/
      reports/
      preview/<id>.html
      gifs/<id>.gif

  /tmp/anim8gen-<project-hash>/<id>/
    scratch/             # disposable conversions, probes, and other transient inner workings

  assets/anim8gen/<id>/
    frames/
    preview.html
    <id>.gif
    raw/                 # only when final frames materially differ from raw candidates
```

Rules:

- The hidden workspace `.anim8gen/` is the default process/provenance area.
- The hidden workspace should contain durable run state that is useful after the run: spec, accepted frame mapping, compact manifests, reports, review notes, and final aligned source frames.
- Disposable inner workings should use a temp work area, not the user's project tree. Good candidates include format conversions, experimental masks, probe images, and other artifacts that can be recreated and are not needed for retry provenance.
- The visible export directory `assets/anim8gen/<id>/` is the default handoff area. Allow `ANIM8GEN_EXPORT_ROOT=anim8gen` or an explicit user option for teams that prefer visible results under `anim8gen/<id>/`, but never use repo-root `anim8gen/` for tools/config/workbench state.
- Raw candidates stay hidden when they are byte-for-byte or visually equivalent to final frames. Copy them to `assets/anim8gen/<id>/raw` automatically when final frames materially differ from raw candidates because of chroma-key removal, alpha conversion, trimming, resizing, alignment, edge cleanup, or other pixel edits.
- Preview pages should be generated in the hidden run folder and exported to the visible deliverable folder after packaging.
- The preview server, when requested, should serve the visible export folder or `.anim8gen/runs/<id>/preview`, not a visible root workbench.
- Preview server consent is part of the output contract, not a convenience detail:
  - `showit` means start the local server and provide the URL after packaging.
  - `noshow` means do not offer and do not start a server.
  - with neither flag, finish the package, report local paths, ask whether to start a preview server, and wait for confirmation before starting one.
- Existing packages under `anim8gen/` should keep working during transition, but new packages must not default there.

## Non-goals

- Do not remove or downgrade the committed `public/` demo gallery.
- Do not require users to commit generated outputs.
- Do not make `/tmp` the only place where durable run state exists; losing accepted-frame provenance after reboot would make debugging expensive. Do use `/tmp` for genuinely disposable inner workings.
- Do not redesign animation generation quality rules in this plan.
- Do not remove support for existing local `anim8gen/<id>` packages until a migration/fallback path exists.
- Do not silently start a local preview server when the request omitted `showit`.

## Phase 1: Path Model and Runtime Boundaries

- Add a small path helper used by scripts and skill examples. It should resolve:
  - project root
  - hidden workspace root, default `.anim8gen`
  - run root, default `.anim8gen/runs/<id>`
  - temp scratch root, default OS temp under `anim8gen-<project-hash>/<id>`
  - visible export root, default `assets/anim8gen/<id>`
  - bundled runtime tool root
- Keep environment overrides for advanced users:
  - `ANIM8GEN_WORKSPACE_ROOT`
  - `ANIM8GEN_EXPORT_ROOT`
  - `ANIM8GEN_TMPDIR`
  - `ANIM8GEN_ALWAYS_EXPORT_RAW` for development/debug runs only
- Preserve legacy fallback when a run spec already lives under `anim8gen/config/<id>.json`.

Acceptance criteria:

- New path helper tests cover defaults and environment overrides.
- No new code path builds `anim8gen/...` strings by hand for new runs.
- Temp scratch paths are outside the project tree by default.
- Legacy specs can still be read explicitly.

## Phase 2: Fix Package Initialization

- Update `init_package.py` so `--root .anim8gen/runs/<id>` or equivalent writes self-consistent paths into:
  - `asset.canonicalReference`
  - `generation.candidateManifest`
  - `generation.acceptedManifest`
  - `package-manifest.json`
- Prefer a clearer CLI contract:

```bash
python3 scripts/init_package.py \
  --brief /tmp/<id>.brief.json \
  --workspace-root .anim8gen \
  --export-root assets/anim8gen
```

- Keep `--root` as a deprecated compatibility alias for one cycle.
- Ensure generated package `.gitignore` is still useful inside hidden workspaces but does not imply users should commit intermediates.

Acceptance criteria:

- Running the initializer for `trex-roar-v1` in a temp repo creates `.anim8gen/runs/trex-roar-v1/**` and does not create `anim8gen/`.
- The generated spec contains no hard-coded `anim8gen/assets`, `anim8gen/config`, `anim8gen/preview`, or `anim8gen/reports` paths.
- Existing tests using old `--root` continue to pass or are intentionally updated with a documented compatibility check.

## Phase 3: Move Tooling Out of the User-Facing Workbench

- Bundle runtime tools and minimal config templates with the skill, probably under `.claude/skills/anim8gen/runtime/` or `.codex/skills/anim8gen/runtime/` depending on installer target.
- Stop telling users or agents to copy this repo's root `anim8gen/` directory into client projects.
- Keep this repo's source `anim8gen/tools` during development if useful, but define the install artifact as a minimal skill package rather than the full repo workbench.
- Remove development docs such as `DEV_README.md` from the client install path unless the user explicitly installs from source for development.

Acceptance criteria:

- A clean install from README creates only the skill directory plus any intentionally hidden project workspace needed at first run.
- Before the first run, the user's project root has no visible `anim8gen/` directory.
- After a run, the only visible default project output is the deliverable bundle, not tools, schemas, manifests, retry ledgers, or development docs.
- The installed skill can locate its bundled tools without `.codex` hard-coded paths.

## Phase 4: Add Explicit Export Step

- Add or update an export helper that copies final deliverables from the hidden run workspace to `assets/anim8gen/<id>/`.
- Default visible deliverables:
  - `frames/frame-NNN.<label>.png`
  - `preview.html`
  - `<id>.gif` when requested with `gif`
- Conditional visible deliverables:
  - `raw/` when final frames materially differ from raw candidates
- Debug artifacts such as contact sheets, validation JSON, manifests, retry ledgers, review notes, and internal reports stay hidden unless the user explicitly requests a debug/provenance export target. They must not be part of the normal final deliverable bundle.
- Make exported `preview.html` use relative paths within `assets/anim8gen/<id>/` so it works as a static artifact.
- Fix preview URL generation so it does not assume the preview file is two levels below a shared workspace root. Prefer export-local paths such as `frames/frame-000.idle.png`.

Acceptance criteria:

- A generated package has a clean visible output folder with no manifests unless explicitly requested.
- The visible output folder can be placed under either `assets/anim8gen/<id>` by default or another explicit export root such as `anim8gen/<id>`, but it contains results only.
- `preview.html` opens from the exported folder and via local static server.
- Exported preview frame URLs are relative to the exported bundle, not to `.anim8gen`.
- GIF export uses the same playback indexes, display offsets, and runtime effects as the preview.

## Phase 5: Clean Demo and Repo Surfaces

- Keep committed public demos under `public/demos/**` and `public/media/**`.
- Move demo source specs out of the installable runtime path. Options:
  - `examples/specs/<id>.json` for source specs we want to keep
  - `public/demos/<id>/package.md` only if a public-readable summary is enough
- Remove old report markdown from `anim8gen/reports` unless it is intentionally part of examples.
- Decide whether repo-local `anim8gen/config/template.animation-spec.json` and `brief.schema.json` stay as source copies or move under `anim8gen/runtime/config`.

Acceptance criteria:

- A basic install cannot copy `quality-*`, `pirate-*`, or `sci-fi-*` specs into the user's project root.
- README demo links continue to work through `public/`.
- `git ls-files anim8gen/config anim8gen/reports` is either empty or limited to intentionally source-owned runtime templates.

## Phase 6: Update Skill and README Behavior

- Rewrite `SKILL.md` package paths and commands around `.anim8gen/runs/<id>` and `assets/anim8gen/<id>`.
- Update README install instructions and the prompt we give users so an installing agent does not infer that repo-root `anim8gen/` should be copied.
- Keep `showit`, `noshow`, and no-flag behavior precise:
  - `showit`: start preview server and provide URL
  - `noshow`: do not offer or start preview server
  - no flag: offer and wait before starting a server
- Explain generated output locations succinctly in README.

Acceptance criteria:

- The README prompt no longer causes an agent to copy demo configs/reports into the user's repo.
- The README states where hidden work and visible deliverables go.
- The skill no longer teaches a server rooted at visible `anim8gen/`.
- A no-flag clean-room run ends with paths and an offer to start the preview server, but no server process is started before user confirmation.
- A `noshow` clean-room run produces no server offer and starts no server.
- A `showit` clean-room run starts exactly one local static server rooted at the exported preview bundle or hidden preview folder and gives the correct URL.

## Phase 7: Tests and Clean-Room Verification

Add automated tests for:

- package initialization under a hidden workspace
- no hard-coded `anim8gen/...` strings in generated specs/manifests for new runs
- export to `assets/anim8gen/<id>` with frames, preview, and optional GIF
- conditional raw export when raw candidates differ materially from final frames
- backward compatibility for explicit legacy package paths
- preview path relativity after export
- a complete synthetic run that initializes a package, creates synthetic frames, aligns, validates, builds contact sheet, builds preview, exports GIF, and exports the visible bundle without creating visible `anim8gen/`

Run:

```bash
python3 -m py_compile .codex/skills/anim8gen/scripts/*.py anim8gen/tools/*.py tests/*.py
python3 tests/test_anim8gen_tools.py
```

Add a clean-room manual check:

```bash
tmpdir="$(mktemp -d)"
git clone https://github.com/zeveck/anim8gen "$tmpdir/anim8gen-src"
mkdir "$tmpdir/client"
cd "$tmpdir/client"
# Follow README install prompt exactly with Claude/Codex.
# Then run: Use anim8gen to make a 4 frame animation of a tyrannosaurus roaring on a transparent background noshow
find . -maxdepth 2 -type d | sort
pgrep -af "http.server|python.*anim8gen" || true
```

Expected result:

- no `./anim8gen` directory
- hidden `.anim8gen/runs/<id>` exists after run
- visible `assets/anim8gen/<id>` exists after run
- no demo specs or old reports are present in the client repo
- no preview server starts for `noshow`
- the same prompt without `noshow` asks before starting a server
- the same prompt with `showit` starts the server only after packaging

## Risks and Decisions

- Hidden state can be less discoverable. Mitigate with a short final response listing visible outputs and saying advanced provenance is in `.anim8gen/runs/<id>`.
- Some users may want raw candidates, but a request word is unnecessary. Export raw automatically only when it explains meaningful changes between generator output and final frames; otherwise keep it hidden.
- Public demo maintenance may currently depend on specs under `anim8gen/config`. Move those specs to an examples path before deleting anything.
- Legacy packages under `anim8gen/` may exist in local checkouts. Support explicit legacy paths and avoid destructive migrations.
- Installing from a source checkout and installing as a skill are different workflows. README should be biased toward users; DEV docs can cover source development.

## Progress Tracker

- [✅ Done] Phase 1: Path model and runtime boundaries
- [✅ Done] Phase 2: Package initialization root fixes
- [✅ Done] Phase 3: Tooling install boundary
- [ ] Phase 4: Visible export step
- [ ] Phase 5: Demo/repo surface cleanup
- [ ] Phase 6: Skill and README updates
- [ ] Phase 7: Tests and clean-room verification
