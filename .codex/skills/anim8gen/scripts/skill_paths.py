#!/usr/bin/env python3
"""Print install-independent anim8gen skill helper paths."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import layout_paths


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "name",
        choices=[
            "skill-dir",
            "script-dir",
            "init-package",
            "validate-review-records",
            "create-synthetic-frames",
            "runtime-tools",
            "imagegen2-cli",
        ],
    )
    parser.add_argument("--start", default=".", help="Project search start directory")
    parser.add_argument("--animation-id", default="example", help="Animation id for layout-derived paths")
    return parser.parse_args()


def candidate_roots(start: Path) -> list[Path]:
    roots: list[Path] = []
    current = start.resolve()
    roots.extend([current, *current.parents])
    home = Path.home()
    for raw in (
        os.environ.get("CLAUDE_CONFIG_DIR"),
        os.environ.get("CODEX_HOME"),
    ):
        if raw:
            roots.append(Path(raw).expanduser())
    roots.extend([home / ".claude", home / ".codex"])
    return roots


def find_imagegen2_cli(start: Path) -> Path:
    candidates: list[Path] = []
    for root in candidate_roots(start):
        candidates.extend(
            [
                root / ".claude" / "skills" / "imagegen2" / "generate.cjs",
                root / ".codex" / "skills" / "imagegen2" / "generate.cjs",
                root / ".agents" / "skills" / "imagegen2" / "generate.cjs",
                root / "skills" / "imagegen2" / "generate.cjs",
                root / "imagegen2" / "generate.cjs",
            ]
        )
    sibling = SKILL_DIR.parent / "imagegen2" / "generate.cjs"
    candidates.insert(0, sibling)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise SystemExit("ERROR: could not find imagegen2 generate.cjs")


def main() -> None:
    args = parse_args()
    paths = {
        "skill-dir": SKILL_DIR,
        "script-dir": SCRIPT_DIR,
        "init-package": SCRIPT_DIR / "init_package.py",
        "validate-review-records": SCRIPT_DIR / "validate_review_records.py",
        "create-synthetic-frames": SCRIPT_DIR / "create_synthetic_frames.py",
        "runtime-tools": layout_paths.resolve_layout(args.animation_id, args.start).runtime_tool_root,
    }
    if args.name == "imagegen2-cli":
        print(find_imagegen2_cli(Path(args.start)))
    else:
        print(paths[args.name])


if __name__ == "__main__":
    main()
