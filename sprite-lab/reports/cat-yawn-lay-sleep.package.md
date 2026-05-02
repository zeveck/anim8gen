# Cat Yawn Lay Sleep Prototype Package

## What Is Final

- Final aligned sprite frames:
  `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-000.sit-idle.png`
  through
  `sprite-lab/assets/cat-yawn-lay-sleep/aligned/frame-007.sleep-loop.png`
- Validation report:
  `sprite-lab/reports/cat-yawn-lay-sleep.validation.json`
- Review contact sheet:
  `sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png`
- HTML preview:
  `sprite-lab/preview/cat-yawn-lay-sleep.html`
- Manual review summary:
  `sprite-lab/reports/cat-yawn-lay-sleep.summary.md`
- Package manifest:
  `sprite-lab/assets/cat-yawn-lay-sleep/manifests/package-manifest.json`

The raw candidates and canonical reference image are intermediate assets. Keep
them with the package for provenance and future regeneration, but do not treat
them as final sprite frames.

## Provenance

- Animation spec:
  `sprite-lab/config/cat-yawn-lay-sleep.json`
- Reference image:
  `sprite-lab/assets/cat-yawn-lay-sleep/reference/cat-reference.jpg`
- Candidate metadata:
  `sprite-lab/assets/cat-yawn-lay-sleep/manifests/candidates.jsonl`
- Accepted frame manifest:
  `sprite-lab/assets/cat-yawn-lay-sleep/manifests/accepted-frames.json`
- Alignment metrics:
  `sprite-lab/assets/cat-yawn-lay-sleep/manifests/alignment-metrics.json`

Generated bitmap assets are ignored by git on purpose. The tracked manifests
and reports describe the package, while the local `reference/`, `raw/`,
`aligned/`, and `review/` folders hold the generated image files.

## Rebuild Commands

Install Python dependencies:

```bash
python3 -m pip install -r sprite-lab/requirements.txt
```

Regenerate aligned frames from the accepted raw candidates:

```bash
python3 sprite-lab/tools/align_frames.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --input sprite-lab/assets/cat-yawn-lay-sleep/raw \
  --output sprite-lab/assets/cat-yawn-lay-sleep/aligned
```

Run validation:

```bash
python3 sprite-lab/tools/validate_sprites.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --out sprite-lab/reports/cat-yawn-lay-sleep.validation.json
```

Regenerate review artifacts:

```bash
python3 sprite-lab/tools/make_contact_sheet.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --raw sprite-lab/assets/cat-yawn-lay-sleep/raw \
  --aligned sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json \
  --out sprite-lab/assets/cat-yawn-lay-sleep/review/contact-sheet.png

python3 sprite-lab/tools/make_preview.py \
  --spec sprite-lab/config/cat-yawn-lay-sleep.json \
  --frames sprite-lab/assets/cat-yawn-lay-sleep/aligned \
  --validation sprite-lab/reports/cat-yawn-lay-sleep.validation.json \
  --out sprite-lab/preview/cat-yawn-lay-sleep.html
```

Open the preview:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory sprite-lab
```

Then visit `http://127.0.0.1:8765/preview/cat-yawn-lay-sleep.html`.
