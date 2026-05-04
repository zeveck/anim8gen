# anim8gen workspace

This directory contains the package workspace for the public `anim8gen` skill:
animation specs, generated-package manifests, local preview HTML, validation
reports, and reusable image-processing tools.

The public project README lives at [../README.md](../README.md).

Common local commands are run from the repository root:

```bash
python3 -m pip install -r anim8gen/requirements.txt

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
```

To publish a selected package as a GitHub Pages demo:

```bash
python3 anim8gen/tools/export_public_demo.py <animation-id> --clean
```

## Release Surface

The public repository tracks durable specs, templates, tools, docs, and the
curated public demo surface. Generated package assets, review JSON, validation
JSON, package reports, local preview HTML, and local GIF exports stay ignored
unless a later release explicitly promotes a small fixture.

The `deterministic-square-hop` spec is retained as a tiny deterministic
regression fixture. Its generated assets, preview, validation JSON, and package
report are local outputs and are not part of the committed release surface.
