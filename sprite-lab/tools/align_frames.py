#!/usr/bin/env python3
"""Align raw sprite frames onto a fixed transparent canvas."""

from __future__ import annotations

import argparse
import json
import math
from collections import deque
from pathlib import Path
from statistics import median

from PIL import Image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def is_visible(pixel: tuple[int, int, int, int], spec: dict) -> bool:
    r, g, b, a = pixel
    if a <= spec["segmentation"].get("alphaThreshold", 8):
        return False
    chroma = spec["segmentation"].get("chromaKey", "#ff00ff").lstrip("#")
    key = tuple(int(chroma[i : i + 2], 16) for i in (0, 2, 4))
    tolerance = spec["segmentation"].get("chromaTolerance", 32)
    distance = math.sqrt((r - key[0]) ** 2 + (g - key[1]) ** 2 + (b - key[2]) ** 2)
    # Generated images contain anti-aliased magenta gradients. Treat saturated
    # magenta-family pixels as background in addition to strict key tolerance.
    magenta_family = r >= 180 and b >= 180 and g <= 95
    return not (distance <= tolerance or magenta_family)


def largest_component(mask: list[bool], width: int, height: int) -> list[bool]:
    visited = [False] * len(mask)
    best: list[int] = []
    neighbors = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for start, visible in enumerate(mask):
        if not visible or visited[start]:
            continue
        component: list[int] = []
        queue = deque([start])
        visited[start] = True
        while queue:
            idx = queue.popleft()
            component.append(idx)
            x, y = idx % width, idx // width
            for dx, dy in neighbors:
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= width or ny >= height:
                    continue
                nidx = ny * width + nx
                if mask[nidx] and not visited[nidx]:
                    visited[nidx] = True
                    queue.append(nidx)
        if len(component) > len(best):
            best = component
    kept = [False] * len(mask)
    for idx in best:
        kept[idx] = True
    return kept


def bbox_for(mask: list[bool], width: int) -> tuple[int, int, int, int]:
    xs: list[int] = []
    ys: list[int] = []
    for idx, visible in enumerate(mask):
        if visible:
            xs.append(idx % width)
            ys.append(idx // width)
    if not xs:
        raise ValueError("empty sprite mask")
    return min(xs), min(ys), max(xs), max(ys)


def centroid(mask: list[bool], width: int) -> tuple[float, float]:
    points = [(idx % width, idx // width) for idx, visible in enumerate(mask) if visible]
    if not points:
        return 0.0, 0.0
    return sum(x for x, _ in points) / len(points), sum(y for _, y in points) / len(points)


def anchor_for(mask: list[bool], width: int, bbox: tuple[int, int, int, int], strategy: str) -> tuple[float, float]:
    min_x, min_y, max_x, max_y = bbox
    cx, cy = centroid(mask, width)
    if strategy in ("body_bottom_center", "feet_center"):
        band_y = max(min_y, max_y - 4)
        xs = [idx % width for idx, visible in enumerate(mask) if visible and idx // width >= band_y]
        return (float(median(xs)) if xs else (min_x + max_x) / 2, float(max_y))
    if strategy == "body_center":
        return cx, cy
    if strategy == "head_center":
        upper_limit = min_y + max(1, (max_y - min_y + 1) // 3)
        points = [(idx % width, idx // width) for idx, visible in enumerate(mask) if visible and idx // width <= upper_limit]
        if not points:
            return cx, cy
        return float(median([x for x, _ in points])), float(median([y for _, y in points]))
    return cx, cy


def manual_override(spec: dict, frame: dict) -> tuple[float, float] | None:
    overrides = spec["alignment"].get("manualOverrides", {})
    if not isinstance(overrides, dict):
        return None
    candidates = (
        str(frame["index"]),
        f"{frame['index']:03d}",
        frame["label"],
        f"frame-{frame['index']:03d}",
    )
    for key in candidates:
        value = overrides.get(key)
        if isinstance(value, dict) and "anchor" in value:
            value = value["anchor"]
        if isinstance(value, dict) and {"x", "y"} <= value.keys():
            return float(value["x"]), float(value["y"])
        if isinstance(value, list) and len(value) == 2:
            return float(value[0]), float(value[1])
    return None


def output_name(frame: dict) -> str:
    return f"frame-{frame['index']:03d}.{frame['label']}.png"


def visible_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()
    if bbox is None:
        return (0, 0, -1, -1)
    left, top, right, bottom = bbox
    return left, top, right - 1, bottom - 1


def main() -> None:
    args = parse_args()
    spec = json.loads(Path(args.spec).read_text())
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    canvas_w, canvas_h = spec["render"]["canvas"]
    floor_y = spec["alignment"]["floorY"]

    loaded = []
    for frame in spec["frames"]:
        matches = sorted(input_dir.glob(f"frame-{frame['index']:03d}.retry-*.png"))
        if not matches:
            raise FileNotFoundError(f"missing raw frame for index {frame['index']}")
        source = matches[0]
        image = Image.open(source).convert("RGBA")
        width, height = image.size
        pixels = list(image.get_flattened_data())
        mask = largest_component([is_visible(pixel, spec) for pixel in pixels], width, height)
        bbox = bbox_for(mask, width)
        override_anchor = manual_override(spec, frame)
        anchor_strategy = frame.get("anchor", spec["alignment"]["defaultAnchor"])
        loaded.append(
            {
                "frame": frame,
                "source": source,
                "image": image,
                "mask": mask,
                "bbox": bbox,
                "anchor": override_anchor if override_anchor else anchor_for(mask, width, bbox, anchor_strategy),
                "anchorStrategy": "manual" if override_anchor else anchor_strategy,
                "centroid": centroid(mask, width),
                "visibleArea": sum(1 for visible in mask if visible),
            }
        )

    max_bbox_w = max(item["bbox"][2] - item["bbox"][0] + 1 for item in loaded)
    max_bbox_h = max(item["bbox"][3] - item["bbox"][1] + 1 for item in loaded)
    scale = min((canvas_w - 8) / max_bbox_w, (canvas_h - 8) / max_bbox_h)

    metrics = {"id": spec["id"], "canvas": [canvas_w, canvas_h], "floorY": floor_y, "scale": scale, "frames": []}
    for item in loaded:
        frame = item["frame"]
        min_x, min_y, max_x, max_y = item["bbox"]
        crop_w, crop_h = max_x - min_x + 1, max_y - min_y + 1
        mask_img = Image.new("L", item["image"].size, 0)
        mask_img.putdata([255 if visible else 0 for visible in item["mask"]])
        sprite = Image.new("RGBA", item["image"].size, (0, 0, 0, 0))
        sprite.paste(item["image"], (0, 0), mask_img)
        crop = sprite.crop((min_x, min_y, max_x + 1, max_y + 1))
        scaled_w, scaled_h = max(1, round(crop_w * scale)), max(1, round(crop_h * scale))
        crop = crop.resize((scaled_w, scaled_h), Image.Resampling.NEAREST)

        anchor_x, anchor_y = item["anchor"]
        target_x = canvas_w / 2
        target_y = canvas_h / 2 if frame.get("anchor") == "body_center" else floor_y
        offset = (round(target_x - (anchor_x - min_x) * scale), round(target_y - (anchor_y - min_y) * scale))
        canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        canvas.alpha_composite(crop, offset)

        out = output_dir / output_name(frame)
        canvas.save(out)
        metrics["frames"].append(
            {
                "index": frame["index"],
                "label": frame["label"],
                "source": str(item["source"]),
                "output": str(out),
                "anchorStrategy": item["anchorStrategy"],
                "sourceDimensions": list(item["image"].size),
                "sourceBBox": list(item["bbox"]),
                "sourceVisibleArea": item["visibleArea"],
                "sourceCentroid": [round(item["centroid"][0], 3), round(item["centroid"][1], 3)],
                "sourceAnchor": [round(anchor_x, 3), round(anchor_y, 3)],
                "scaledSize": [scaled_w, scaled_h],
                "alignedBBox": list(visible_bbox(canvas)),
                "alignedVisibleArea": visible_area_rgba(canvas),
                "appliedOffset": list(offset),
            }
        )

    metrics_path = Path(spec["generation"]["candidateManifest"]).parent / "alignment-metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n")
    print(f"wrote {len(loaded)} aligned frames to {output_dir}")
    print(f"wrote metrics to {metrics_path}")


def visible_area_rgba(image: Image.Image) -> int:
    histogram = image.getchannel("A").histogram()
    return sum(histogram[1:])


if __name__ == "__main__":
    main()
