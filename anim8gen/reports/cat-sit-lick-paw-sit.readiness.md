# Cat Sit Lick Paw Sit Readiness Check

## Purpose

This second animation is a small synthetic check that the anim8gen alignment
and validation tools are driven by animation specs and folder paths, not by the
first `cat-yawn-lay-sleep` sequence.

## Inputs

- Spec: `anim8gen/config/cat-sit-lick-paw-sit.json`
- Synthetic raw frames:
  `anim8gen/assets/cat-sit-lick-paw-sit/raw/frame-000.retry-001.png`
  through
  `anim8gen/assets/cat-sit-lick-paw-sit/raw/frame-002.retry-001.png`
- Candidate metadata:
  `anim8gen/assets/cat-sit-lick-paw-sit/manifests/candidates.jsonl`

The raw and aligned PNGs are local generated assets and remain ignored by git,
matching the first prototype package convention.

## Commands

```bash
python3 -m json.tool anim8gen/config/cat-sit-lick-paw-sit.json >/dev/null
python3 anim8gen/tools/align_frames.py \
  --spec anim8gen/config/cat-sit-lick-paw-sit.json \
  --input anim8gen/assets/cat-sit-lick-paw-sit/raw \
  --output anim8gen/assets/cat-sit-lick-paw-sit/aligned
python3 anim8gen/tools/validate_sprites.py \
  --spec anim8gen/config/cat-sit-lick-paw-sit.json \
  --frames anim8gen/assets/cat-sit-lick-paw-sit/aligned \
  --out anim8gen/reports/cat-sit-lick-paw-sit.validation.json
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
