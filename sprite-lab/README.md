# Sprite Lab

Sprite Lab is a small prototype workspace for generating, aligning, validating,
and reviewing fixed-canvas sprite animation frames.

The first target sequence is `cat-yawn-lay-sleep`: a 16-bit pixel-art cat that
yawns, lies down, and sleeps. The sleeping Zs are intentionally rendered by the
preview/runtime layer instead of being baked into sprite frames.

The second readiness sequence is `cat-sit-lick-paw-sit`. It uses local
synthetic placeholder frames to prove that the same spec-driven alignment and
validation tools run against another animation without changing tool code.

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

Generated image outputs are ignored by default. Keep reviewed manifests,
package manifests, and summary reports when they are needed for provenance.
For the accepted cat prototype package, start with
`reports/cat-yawn-lay-sleep.package.md`.
For the second-animation readiness check, see
`reports/cat-sit-lick-paw-sit.readiness.md`.

## Dependency Approach

Use Node.js for generation wrappers and static preview generation. Use Python 3
for image alignment, validation, and contact sheets.

Expected Python packages:

- Pillow for image loading, segmentation, overlays, and contact sheets.

No package lockfile is required for this prototype. The current scoped Python
dependency list is `requirements.txt`.
