# Anim8gen Prompting

Use this template for each generated frame:

```text
<style> sprite frame of <subject>, <view> view, single centered full-body
subject, pose for frame <index> (<label>): <frame pose>. Compact readable
silhouette, consistent identity with the reference, full body inside the image,
solid #ff00ff chroma-key background, no text, no watermark, no labels, no UI
overlay, no extra subjects, no props unless requested, no motion marks, no
baked preview effects.
```

When a canonical reference exists, pass it to `imagegen2` with `--image`.
For adjacent-frame continuity, consider passing the previous accepted frame as
an additional reference when that does not over-constrain the requested pose.

Keep each retry targeted. Preserve the accepted identity, style, camera, and
background instructions, then name the one failure that caused the retry.

Retry prompts should name the specific failure:

```text
Retry frame 002. Keep the same cat identity and side view as the reference, but
make the paw visibly raised and touching the mouth. Keep the magenta background
flat and remove all labels or motion marks.
```
