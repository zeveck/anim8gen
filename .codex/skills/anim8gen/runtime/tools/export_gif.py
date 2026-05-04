#!/usr/bin/env python3
"""Export an anim8gen package preview as an animated GIF."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image

import make_preview


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--frames", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--fps", type=float, help="Override spec render.fps")
    parser.add_argument("--scale", type=int, default=1, help="Nearest-neighbor export scale")
    return parser.parse_args()


def playback_indexes(spec: dict[str, Any]) -> list[int]:
    return make_preview.build_payload_for_indexes(spec)


def render_frame(
    source: Path,
    canvas_size: tuple[int, int],
    offset: dict[str, Any],
    scale: int,
) -> Image.Image:
    source_image = Image.open(source).convert("RGBA")
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    canvas.alpha_composite(source_image, (round(offset["x"]), round(offset["y"])))
    if scale != 1:
        scaled_size = (canvas.width * scale, canvas.height * scale)
        canvas = canvas.resize(scaled_size, Image.Resampling.NEAREST)
    return canvas


def export_gif(spec: dict[str, Any], frames_dir: Path, out_path: Path, fps: float, scale: int) -> None:
    if fps <= 0:
        raise ValueError("--fps must be greater than zero")
    if scale < 1:
        raise ValueError("--scale must be at least 1")

    canvas_size = tuple(spec["render"]["canvas"])
    if len(canvas_size) != 2:
        raise ValueError("spec render.canvas must contain width and height")

    preview = spec.get("preview", {})
    rendered: list[Image.Image] = []
    for index in playback_indexes(spec):
        frame = spec["frames"][index]
        source = frames_dir / make_preview.aligned_name(frame)
        if not source.exists():
            raise FileNotFoundError(f"missing aligned frame: {source}")
        rendered.append(render_frame(source, canvas_size, make_preview.preview_offset(preview, frame), scale))

    if not rendered:
        raise ValueError("no frames to export")

    duration_ms = max(20, round(1000 / fps))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rendered[0].save(
        out_path,
        save_all=True,
        append_images=rendered[1:],
        duration=duration_ms,
        loop=0,
        disposal=2,
        optimize=False,
    )


def main() -> None:
    args = parse_args()
    spec = json.loads(Path(args.spec).read_text())
    fps = args.fps if args.fps is not None else float(spec["render"].get("fps", 8))
    export_gif(spec, Path(args.frames), Path(args.out), fps, args.scale)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
