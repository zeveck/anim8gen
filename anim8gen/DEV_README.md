# anim8gen development notes

This directory contains the package workspace for the public `anim8gen` skill:
animation specs, package manifests, local preview HTML, validation reports, and
image-processing tools.

Run commands from the repository root.

## Install Local Tooling

```bash
python3 -m pip install -r anim8gen/requirements.txt
```

## Test

```bash
python3 tests/test_anim8gen_tools.py
python3 -m py_compile anim8gen/tools/*.py .codex/skills/anim8gen/scripts/*.py
```

The checked-in skill path above is for repository development only. Installed
skills must resolve helper scripts relative to their own `SKILL.md` directory,
whether that directory is under `.claude/skills`, `.codex/skills`,
`.agents/skills`, or a user-level skills folder.

## Package Tool Commands

Replace `<animation-id>` with a package id:

```bash
python3 anim8gen/tools/align_frames.py \
  --spec anim8gen/config/<animation-id>.json \
  --input anim8gen/assets/<animation-id>/raw \
  --output anim8gen/assets/<animation-id>/aligned

python3 anim8gen/tools/validate_sprites.py \
  --spec anim8gen/config/<animation-id>.json \
  --frames anim8gen/assets/<animation-id>/aligned \
  --out anim8gen/reports/<animation-id>.validation.json

python3 anim8gen/tools/make_contact_sheet.py \
  --spec anim8gen/config/<animation-id>.json \
  --raw anim8gen/assets/<animation-id>/raw \
  --aligned anim8gen/assets/<animation-id>/aligned \
  --validation anim8gen/reports/<animation-id>.validation.json \
  --out anim8gen/assets/<animation-id>/review/contact-sheet.png

python3 anim8gen/tools/make_preview.py \
  --spec anim8gen/config/<animation-id>.json \
  --frames anim8gen/assets/<animation-id>/aligned \
  --validation anim8gen/reports/<animation-id>.validation.json \
  --out anim8gen/preview/<animation-id>.html

python3 anim8gen/tools/export_gif.py \
  --spec anim8gen/config/<animation-id>.json \
  --frames anim8gen/assets/<animation-id>/aligned \
  --out anim8gen/gifs/<animation-id>.gif
```

## Public Demo Export

Selected demos are copied into self-contained folders under `public/demos/`:

```bash
python3 anim8gen/tools/export_public_demo.py <animation-id> [<animation-id> ...] --clean
```

The exporter reuses the local preview page format, copies aligned frames into a
local `frames/` folder, and includes the contact sheet and package report when
available.

## Generated Assets

Generated bitmap outputs under package folders are local working artifacts.
The root `.gitignore` keeps `anim8gen/assets/`, `anim8gen/contact/`,
`anim8gen/preview/`, `anim8gen/reports/*.json`, package reports, and local GIF
exports out of source control. Curated public demos live under `public/`.
