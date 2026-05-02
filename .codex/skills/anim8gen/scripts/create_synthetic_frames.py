#!/usr/bin/env python3
"""Create deterministic chroma-keyed raw PNG candidates for Anim8gen tests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, help="Path to an Anim8gen animation spec JSON file.")
    parser.add_argument(
        "--root",
        default="anim8gen",
        help="Anim8gen workspace root containing assets/. Defaults to ./anim8gen.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing synthetic raw frames.")
    return parser.parse_args()


def load_spec(path: Path) -> dict[str, Any]:
    try:
        spec = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(spec, dict) or not isinstance(spec.get("frames"), list):
        raise SystemExit(f"{path}: not an Anim8gen spec")
    return spec


def parse_hex_color(value: str) -> tuple[int, int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise SystemExit("segmentation.chromaKey must be a #rrggbb color")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4)) + (255,)


def draw_pixel_square(draw: ImageDraw.ImageDraw, x: int, y: int, size: int, color: tuple[int, int, int, int]) -> None:
    draw.rectangle((x, y, x + size - 1, y + size - 1), fill=color)


def draw_sprite(draw: ImageDraw.ImageDraw, frame: dict[str, Any], image_size: tuple[int, int]) -> None:
    width, height = image_size
    index = int(frame["index"])
    x_offset = (index % 4) * 42
    hop = 54 if "hop" in frame.get("label", "") or "up" in frame.get("label", "") else 0
    base_x = width // 2 - 120 + x_offset
    base_y = height // 2 + 170 - hop

    body = (66, 135, 245, 255)
    outline = (12, 34, 72, 255)
    highlight = (133, 196, 255, 255)
    shadow = (21, 79, 160, 255)

    draw.rectangle((base_x - 8, base_y - 8, base_x + 136, base_y + 136), fill=outline)
    draw.rectangle((base_x, base_y, base_x + 128, base_y + 128), fill=body)
    draw.rectangle((base_x + 16, base_y + 16, base_x + 62, base_y + 62), fill=highlight)
    draw.rectangle((base_x + 82, base_y + 86, base_x + 112, base_y + 116), fill=shadow)

    # Add a simple pose marker that changes per frame without relying on text.
    marker_x = base_x + 18 + index * 10
    marker_y = base_y - 34 if hop else base_y + 144
    draw_pixel_square(draw, marker_x, marker_y, 24, (245, 196, 66, 255))


def synthetic_record(spec: dict[str, Any], frame: dict[str, Any], output_path: Path) -> dict[str, Any]:
    animation_id = spec["id"]
    return {
        "generatorSkill": "anim8gen-test-helper",
        "model": "deterministic-synthetic",
        "prompt": f"synthetic test frame for {animation_id} frame {frame['index']} {frame['label']}",
        "negativePrompt": "not applicable; deterministic local test helper",
        "style": [spec.get("asset", {}).get("style", "pixel art")],
        "sourceReferencePath": None,
        "seed": 0,
        "historyId": f"{animation_id}-synthetic-frame-{frame['index']:03d}-retry-001",
        "requestId": f"synthetic-{animation_id}-{frame['index']:03d}",
        "frameIndex": frame["index"],
        "frameLabel": frame["label"],
        "pose": frame["pose"],
        "outputPath": str(output_path),
        "retry": 1,
        "parentCandidate": None,
        "neighboringReference": None,
        "status": "candidate",
        "acceptedStatus": "pending-review",
        "bytes": output_path.stat().st_size,
        "outputFormat": "png",
        "refusalReason": None,
        "testHelper": True,
    }


def main() -> None:
    args = parse_args()
    spec_path = Path(args.spec)
    root = Path(args.root)
    spec = load_spec(spec_path)
    animation_id = spec["id"]
    working_size = tuple(spec.get("render", {}).get("workingSize", [1024, 1024]))
    if len(working_size) != 2:
        raise SystemExit("render.workingSize must contain width and height")
    background = parse_hex_color(spec.get("segmentation", {}).get("chromaKey", "#ff00ff"))

    raw_dir = root / "assets" / animation_id / "raw"
    manifest_dir = root / "assets" / animation_id / "manifests"
    raw_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    for frame in spec["frames"]:
        if not isinstance(frame, dict) or "index" not in frame or "label" not in frame:
            raise SystemExit("each spec frame must include index and label")
        out = raw_dir / f"frame-{frame['index']:03d}.retry-001.png"
        if out.exists() and not args.force:
            raise SystemExit(f"{out} already exists; pass --force to overwrite")
        image = Image.new("RGBA", working_size, background)
        draw_sprite(ImageDraw.Draw(image), frame, working_size)
        image.save(out)
        records.append(synthetic_record(spec, frame, out))

    manifest = manifest_dir / "candidates.jsonl"
    if manifest.exists() and manifest.read_text() and not args.force:
        raise SystemExit(f"{manifest} already has content; pass --force to overwrite")
    manifest.write_text("".join(json.dumps(record, sort_keys=True) + "\n" for record in records))
    print(f"wrote {len(records)} synthetic raw frames to {raw_dir}")
    print(f"wrote candidate manifest to {manifest}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(1)
