#!/usr/bin/env python3
"""Export selected anim8gen packages into self-contained public demos."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import make_preview


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("ids", nargs="+", help="Animation ids to export")
    parser.add_argument("--root", default="anim8gen", help="anim8gen workspace root")
    parser.add_argument("--public", default="public", help="GitHub Pages output root")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove each selected demo output directory before exporting",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def export_demo(animation_id: str, root: Path, public_root: Path, clean: bool) -> None:
    spec_path = root / "config" / f"{animation_id}.json"
    validation_path = root / "reports" / f"{animation_id}.validation.json"
    frames_dir = root / "assets" / animation_id / "aligned"
    review_dir = root / "assets" / animation_id / "review"
    report_path = root / "reports" / f"{animation_id}.package.md"

    if not spec_path.exists():
        raise FileNotFoundError(f"missing spec: {spec_path}")
    if not validation_path.exists():
        raise FileNotFoundError(f"missing validation report: {validation_path}")

    out_dir = public_root / "demos" / animation_id
    if clean and out_dir.exists():
        shutil.rmtree(out_dir)

    frames_out = out_dir / "frames"
    frames_out.mkdir(parents=True, exist_ok=True)

    spec = load_json(spec_path)
    validation = load_json(validation_path)
    payload = make_preview.build_payload(
        spec,
        validation,
        frames_dir,
        root / "preview" / f"{animation_id}.html",
    )

    for frame, original in zip(payload["frames"], spec["frames"]):
        src = frames_dir / make_preview.aligned_name(original)
        dest = frames_out / f"frame-{original['index']:03d}.{original['label']}.png"
        shutil.copy2(src, dest)
        frame["src"] = f"frames/{dest.name}"

    contact_sheet = review_dir / "contact-sheet.png"
    if not contact_sheet.exists():
        contact_sheet = root / "contact" / f"{animation_id}.png"
    if contact_sheet.exists():
        shutil.copy2(contact_sheet, out_dir / "contact-sheet.png")

    if report_path.exists():
        shutil.copy2(report_path, out_dir / "package.md")

    (out_dir / "index.html").write_text(make_preview.render_html(payload), encoding="utf-8")
    print(f"Exported {animation_id} to {out_dir}")


def main() -> None:
    args = parse_args()
    root = Path(args.root)
    public_root = Path(args.public)
    for animation_id in args.ids:
        export_demo(animation_id, root, public_root, args.clean)


if __name__ == "__main__":
    main()
