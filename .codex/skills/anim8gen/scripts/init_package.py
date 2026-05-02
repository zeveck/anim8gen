#!/usr/bin/env python3
"""Initialize an Anim8gen package from a prepared JSON brief."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ANCHORS = {"body_bottom_center", "feet_center", "body_center", "head_center", "manual"}
VIEWS = {"side", "front", "three-quarter", "top-down", "isometric"}
PACKAGE_DIRS = ("reference", "raw", "aligned", "review", "manifests")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", required=True, help="Path to a prepared Anim8gen brief JSON file.")
    parser.add_argument(
        "--root",
        default="anim8gen",
        help="Anim8gen workspace root containing config/ and assets/. Defaults to ./anim8gen.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing spec and manifests.")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: brief must be a JSON object")
    return data


def require_text(data: dict[str, Any], key: str, default: str | None = None) -> str:
    value = data.get(key, default)
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"brief.{key} must be a non-empty string")
    return value.strip()


def require_pair(data: dict[str, Any], key: str, default: list[int], minimum: int, maximum: int) -> list[int]:
    value = data.get(key, default)
    if (
        not isinstance(value, list)
        or len(value) != 2
        or not all(isinstance(item, int) for item in value)
        or not all(minimum <= item <= maximum for item in value)
    ):
        raise SystemExit(f"brief.{key} must be two integers between {minimum} and {maximum}")
    return [int(value[0]), int(value[1])]


def validate_frames(data: dict[str, Any]) -> list[dict[str, Any]]:
    raw_frames = data.get("frames")
    if not isinstance(raw_frames, list) or not (2 <= len(raw_frames) <= 8):
        raise SystemExit("brief.frames must contain 2 to 8 frame objects")

    frames: list[dict[str, Any]] = []
    seen_labels: set[str] = set()
    for expected_index, raw_frame in enumerate(raw_frames):
        if not isinstance(raw_frame, dict):
            raise SystemExit(f"brief.frames[{expected_index}] must be an object")
        index = raw_frame.get("index")
        if index != expected_index:
            raise SystemExit(
                f"brief.frames[{expected_index}].index must be contiguous from 0; got {index!r}"
            )
        label = require_text(raw_frame, "label")
        if not ID_RE.fullmatch(label):
            raise SystemExit(f"brief.frames[{expected_index}].label must be lowercase kebab-case")
        if label in seen_labels:
            raise SystemExit(f"duplicate frame label: {label}")
        seen_labels.add(label)
        pose = require_text(raw_frame, "pose")
        anchor = raw_frame.get("anchor", "body_bottom_center")
        if anchor not in ANCHORS:
            raise SystemExit(f"brief.frames[{expected_index}].anchor must be one of {sorted(ANCHORS)}")
        frames.append({"index": index, "label": label, "pose": pose, "anchor": anchor})
    return frames


def build_spec(brief: dict[str, Any]) -> dict[str, Any]:
    animation_id = require_text(brief, "id")
    if not ID_RE.fullmatch(animation_id):
        raise SystemExit("brief.id must be lowercase kebab-case")

    subject = require_text(brief, "subject")
    style = require_text(brief, "style", "pixel art")
    view = require_text(brief, "view", "side")
    if view not in VIEWS:
        raise SystemExit(f"brief.view must be one of {sorted(VIEWS)}")
    canvas = require_pair(brief, "canvas", [128, 128], 32, 512)
    working_size = require_pair(brief, "workingSize", [1024, 1024], 256, 2048)
    fps = brief.get("fps", 8)
    if not isinstance(fps, int) or not (1 <= fps <= 24):
        raise SystemExit("brief.fps must be an integer between 1 and 24")
    retry_budget = brief.get("retryBudget", 2)
    if not isinstance(retry_budget, int) or not (0 <= retry_budget <= 5):
        raise SystemExit("brief.retryBudget must be an integer between 0 and 5")
    runtime_effects = brief.get("runtimeEffects", [])
    if not isinstance(runtime_effects, list) or not all(isinstance(item, str) for item in runtime_effects):
        raise SystemExit("brief.runtimeEffects must be an array of strings")

    floor_y = brief.get("floorY", max(0, canvas[1] - 16))
    if not isinstance(floor_y, int) or not (0 <= floor_y < canvas[1]):
        raise SystemExit("brief.floorY must be an integer inside the canvas height")

    prompt_traits = [
        "single subject",
        f"{view}-view",
        "compact readable silhouette",
        "solid chroma-key background",
        "no text",
    ]

    return {
        "id": animation_id,
        "asset": {
            "subject": subject,
            "style": style,
            "canonicalReference": f"anim8gen/assets/{animation_id}/reference/reference.png",
            "promptTraits": prompt_traits,
        },
        "render": {
            "canvas": canvas,
            "workingSize": working_size,
            "exportScale": brief.get("exportScale", 8),
            "fps": fps,
            "paletteLimit": brief.get("paletteLimit", 48),
        },
        "generation": {
            "preferredSkill": "imagegen2",
            "fallbackSkills": ["imagegen"],
            "candidateManifest": f"anim8gen/assets/{animation_id}/manifests/candidates.jsonl",
            "acceptedManifest": f"anim8gen/assets/{animation_id}/manifests/accepted-frames.json",
            "retryBudget": retry_budget,
        },
        "segmentation": {
            "strategy": "chroma-key",
            "chromaKey": brief.get("chromaKey", "#ff00ff"),
            "alphaThreshold": brief.get("alphaThreshold", 8),
            "chromaTolerance": brief.get("chromaTolerance", 32),
        },
        "alignment": {
            "defaultAnchor": brief.get("defaultAnchor", "body_bottom_center"),
            "floorY": floor_y,
            "supportedAnchors": sorted(ANCHORS),
            "manualOverrides": {},
        },
        "validation": {
            "defaultThresholds": {
                "anchorXJumpPx": 3,
                "anchorYJumpPx": 2,
                "bboxHeightVariancePct": 12,
                "bboxWidthVariancePct": 18,
                "visibleAreaVariancePct": 20,
                "centroidJumpPx": 5,
                "adjacentSilhouetteIouMin": 0.55,
                "meanLuminanceShiftPct": 15,
                "dominantHueShiftDegrees": 12,
            },
            "motionPhases": [],
        },
        "preview": {
            "strategy": "canvas-playback",
            "runtimeEffects": runtime_effects,
            "minimalControls": ["playPause", "fps", "step", "frameLabel", "checkerboard"],
        },
        "frames": validate_frames(brief),
    }


def package_gitignore() -> str:
    return """# Generated or externally produced image assets stay out of source control.
reference/*
raw/*
aligned/*
review/*

# Keep the package folder structure visible.
!reference/.gitkeep
!raw/.gitkeep
!aligned/.gitkeep
!review/.gitkeep
!review/*.json
!review/*.md
"""


def write_if_missing(path: Path, content: str, force: bool = False) -> None:
    if path.exists() and not force:
        raise SystemExit(f"{path} already exists; pass --force to overwrite")
    path.write_text(content)


def init_package(root: Path, spec: dict[str, Any], force: bool) -> None:
    animation_id = spec["id"]
    config_dir = root / "config"
    assets_dir = root / "assets" / animation_id
    reports_dir = root / "reports"
    preview_dir = root / "preview"

    for path in (config_dir, reports_dir, preview_dir):
        path.mkdir(parents=True, exist_ok=True)
    for folder in PACKAGE_DIRS:
        package_dir = assets_dir / folder
        package_dir.mkdir(parents=True, exist_ok=True)
        (package_dir / ".gitkeep").touch()

    write_if_missing(assets_dir / ".gitignore", package_gitignore(), force=force)
    write_if_missing(config_dir / f"{animation_id}.json", json.dumps(spec, indent=2) + "\n", force=force)
    write_if_missing(assets_dir / "manifests" / "candidates.jsonl", "", force=force)
    write_if_missing(
        assets_dir / "review" / "frame-reviews.json",
        json.dumps(
            {
                "id": animation_id,
                "reviewSchemaVersion": 1,
                "packageStatus": "initialized",
                "retryBudget": spec["generation"]["retryBudget"],
                "frames": [],
            },
            indent=2,
        )
        + "\n",
        force=force,
    )

    accepted_manifest = {
        "id": animation_id,
        "status": "initialized",
        "generator": {
            "skill": "imagegen2",
            "candidateManifest": f"anim8gen/assets/{animation_id}/manifests/candidates.jsonl",
        },
        "frames": [],
    }
    write_if_missing(
        assets_dir / "manifests" / "accepted-frames.json",
        json.dumps(accepted_manifest, indent=2) + "\n",
        force=force,
    )

    package_manifest = {
        "id": animation_id,
        "packageStatus": "initialized",
        "spec": f"anim8gen/config/{animation_id}.json",
        "assets": f"anim8gen/assets/{animation_id}",
        "preview": f"anim8gen/preview/{animation_id}.html",
        "reports": {
            "validation": f"anim8gen/reports/{animation_id}.validation.json",
            "package": f"anim8gen/reports/{animation_id}.package.md",
        },
    }
    write_if_missing(
        assets_dir / "manifests" / "package-manifest.json",
        json.dumps(package_manifest, indent=2) + "\n",
        force=force,
    )


def main() -> None:
    args = parse_args()
    root = Path(args.root)
    brief = load_json(Path(args.brief))
    spec = build_spec(brief)
    init_package(root, spec, args.force)
    print(f"initialized {spec['id']}")
    print(f"spec: {root / 'config' / (spec['id'] + '.json')}")
    print(f"assets: {root / 'assets' / spec['id']}")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(1)
