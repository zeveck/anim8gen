# Cat Sit Lick Paw Sit Readiness Check

## Purpose

This second animation is a small synthetic check that the sprite-lab alignment
and validation tools are driven by animation specs and folder paths, not by the
first `cat-yawn-lay-sleep` sequence.

## Inputs

- Spec: `sprite-lab/config/cat-sit-lick-paw-sit.json`
- Synthetic raw frames:
  `sprite-lab/assets/cat-sit-lick-paw-sit/raw/frame-000.retry-001.png`
  through
  `sprite-lab/assets/cat-sit-lick-paw-sit/raw/frame-002.retry-001.png`
- Candidate metadata:
  `sprite-lab/assets/cat-sit-lick-paw-sit/manifests/candidates.jsonl`

The raw and aligned PNGs are local generated assets and remain ignored by git,
matching the first prototype package convention.

## Commands

```bash
python3 -m json.tool sprite-lab/config/cat-sit-lick-paw-sit.json >/dev/null
python3 sprite-lab/tools/align_frames.py \
  --spec sprite-lab/config/cat-sit-lick-paw-sit.json \
  --input sprite-lab/assets/cat-sit-lick-paw-sit/raw \
  --output sprite-lab/assets/cat-sit-lick-paw-sit/aligned
python3 sprite-lab/tools/validate_sprites.py \
  --spec sprite-lab/config/cat-sit-lick-paw-sit.json \
  --frames sprite-lab/assets/cat-sit-lick-paw-sit/aligned \
  --out sprite-lab/reports/cat-sit-lick-paw-sit.validation.json
```

## Result

The same alignment and validation tools run successfully against the second
spec and three synthetic frames. The validation report has zero structural
failures and zero warnings, including the motion-phase comparison for the
deliberately simple paw-lift motion.

## Follow-Up

- Add a tiny checked-in synthetic fixture generator if future clean-checkout
  regression tests need to recreate ignored PNG fixtures automatically.
- Consider a repository-level generated-assets convention if more animation
  packages are added.
