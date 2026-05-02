# Sprite Lab

Sprite Lab is a small prototype workspace for generating, aligning, validating,
and reviewing fixed-canvas sprite animation frames.

The first target sequence is `cat-yawn-lay-sleep`: a 16-bit pixel-art cat that
yawns, lies down, and sleeps. The sleeping Zs are intentionally rendered by the
preview/runtime layer instead of being baked into sprite frames.

## Layout

- `config/` contains machine-readable animation specs.
- `assets/<animation-id>/reference/` stores canonical reference images.
- `assets/<animation-id>/raw/` stores raw generated still-frame candidates.
- `assets/<animation-id>/aligned/` stores fixed-canvas aligned PNG frames.
- `assets/<animation-id>/review/` stores contact sheets and review images.
- `assets/<animation-id>/manifests/` stores candidate and accepted-frame
  metadata.
- `tools/` will contain generation, alignment, validation, contact-sheet, and
  preview scripts.
- `preview/` will contain generated local HTML previews.
- `reports/` will contain validation and summary reports.

Generated image outputs are ignored by default. Keep reviewed manifests and
summary reports when they are needed for provenance.

## Dependency Approach

Use Node.js for generation wrappers and static preview generation. Use Python 3
for image alignment, validation, and contact sheets.

Expected Python packages for later phases:

- Pillow for image loading, segmentation, overlays, and contact sheets.
- NumPy if later metrics need faster pixel operations.

No package lockfile is required yet because Phase 1 does not add executable
tools.
