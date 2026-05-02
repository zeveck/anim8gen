# Cat Yawn Lay Sleep Prototype Package

## What Is Final

- Final aligned sprite frames:
  `anim8gen/assets/cat-yawn-lay-sleep/aligned/frame-000.sit-idle.png`
  through
  `anim8gen/assets/cat-yawn-lay-sleep/aligned/frame-007.sleep-loop.png`
- Validation report:
  `anim8gen/reports/cat-yawn-lay-sleep.validation.json`
- Review contact sheet:
  `anim8gen/assets/cat-yawn-lay-sleep/review/contact-sheet.png`
- HTML preview:
  `anim8gen/preview/cat-yawn-lay-sleep.html`
- Manual review summary:
  `anim8gen/reports/cat-yawn-lay-sleep.summary.md`
- Package manifest:
  `anim8gen/assets/cat-yawn-lay-sleep/manifests/package-manifest.json`

The raw candidates and canonical reference image are intermediate assets. Keep
them with the package for provenance and future regeneration, but do not treat
them as final sprite frames.

## Provenance

- Animation spec:
  `anim8gen/config/cat-yawn-lay-sleep.json`
- Reference image:
  `anim8gen/assets/cat-yawn-lay-sleep/reference/cat-reference.jpg`
- Candidate metadata:
  `anim8gen/assets/cat-yawn-lay-sleep/manifests/candidates.jsonl`
- Accepted frame manifest:
  `anim8gen/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json`
- Alignment metrics:
  `anim8gen/assets/cat-yawn-lay-sleep/manifests/alignment-metrics.json`

Generated bitmap assets are ignored by git on purpose. The tracked manifests
and reports describe the package, while the local `reference/`, `raw/`,
`aligned/`, and `review/` folders hold the generated image files.

## Rebuild Commands

Install Python dependencies:

```bash
python3 -m pip install -r anim8gen/requirements.txt
```

Regenerate aligned frames from the accepted raw candidates:

```bash
python3 anim8gen/tools/align_frames.py \
  --spec anim8gen/config/cat-yawn-lay-sleep.json \
  --input anim8gen/assets/cat-yawn-lay-sleep/raw \
  --output anim8gen/assets/cat-yawn-lay-sleep/aligned
```

Run validation:

```bash
python3 anim8gen/tools/validate_sprites.py \
  --spec anim8gen/config/cat-yawn-lay-sleep.json \
  --frames anim8gen/assets/cat-yawn-lay-sleep/aligned \
  --out anim8gen/reports/cat-yawn-lay-sleep.validation.json
```

Regenerate review artifacts:

```bash
python3 anim8gen/tools/make_contact_sheet.py \
  --spec anim8gen/config/cat-yawn-lay-sleep.json \
  --raw anim8gen/assets/cat-yawn-lay-sleep/raw \
  --aligned anim8gen/assets/cat-yawn-lay-sleep/aligned \
  --validation anim8gen/reports/cat-yawn-lay-sleep.validation.json \
  --out anim8gen/assets/cat-yawn-lay-sleep/review/contact-sheet.png

python3 anim8gen/tools/make_preview.py \
  --spec anim8gen/config/cat-yawn-lay-sleep.json \
  --frames anim8gen/assets/cat-yawn-lay-sleep/aligned \
  --validation anim8gen/reports/cat-yawn-lay-sleep.validation.json \
  --out anim8gen/preview/cat-yawn-lay-sleep.html
```

Open the preview:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory anim8gen
```

Then visit `http://127.0.0.1:8765/preview/cat-yawn-lay-sleep.html`.
