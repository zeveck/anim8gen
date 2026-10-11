#!/usr/bin/env python3
"""Print install-independent anim8gen skill helper paths."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

import layout_paths


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

ANIM8GEN_VERSION = "2026.10.11"

# imagegen2 releases from this version on support --transparent-mode
# native-alpha (GPT Image 2.5). Older copies only offer chroma-key.
IMAGEGEN2_NATIVE_ALPHA_VERSION = (2026, 10, 10)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "name",
        choices=[
            "skill-dir",
            "script-dir",
            "init-package",
            "prepare-references",
            "validate-review-records",
            "create-synthetic-frames",
            "runtime-tools",
            "runtime-config",
            "align-frames",
            "validate-sprites",
            "make-contact-sheet",
            "make-preview",
            "export-gif",
            "export-webp",
            "export-bundle",
            "clean-reference",
            "brief-schema",
            "template-animation-spec",
            "imagegen2-cli",
            "imagegen2-info",
            "version",
        ],
    )
    parser.add_argument("--start", default=".", help="Project search start directory")
    parser.add_argument("--animation-id", default="example", help="Animation id for layout-derived paths")
    return parser.parse_args()


def project_roots(start: Path) -> list[Path]:
    """The start directory and its parents, stopping above the home directory.

    Home-level skill folders are user installs; they are checked after Claude
    Code plugin installs so a stale copied skill can't shadow a managed plugin.
    """
    home = Path.home().resolve()
    roots: list[Path] = []
    for root in [start.resolve(), *start.resolve().parents]:
        if root == home or root in home.parents:
            break
        roots.append(root)
    return roots


def claude_config_dirs() -> list[Path]:
    dirs: list[Path] = []
    raw = os.environ.get("CLAUDE_CONFIG_DIR")
    if raw:
        dirs.append(Path(raw).expanduser())
    dirs.append(Path.home() / ".claude")
    return dirs


def user_skill_roots() -> list[Path]:
    roots = claude_config_dirs()
    raw = os.environ.get("CODEX_HOME")
    if raw:
        roots.append(Path(raw).expanduser())
    home = Path.home()
    roots.extend([home / ".codex", home / ".agents"])
    return roots


def version_key(version: str) -> tuple[int, ...]:
    parts = re.findall(r"\d+", version or "")
    return tuple(int(part) for part in parts[:3]) or (0,)


def plugin_candidates() -> list[Path]:
    """imagegen2 CLIs from Claude Code plugin installs, newest version first."""
    found: list[tuple[tuple[int, ...], Path]] = []
    for config_dir in claude_config_dirs():
        plugins_dir = config_dir / "plugins"
        registry = plugins_dir / "installed_plugins.json"
        try:
            data = json.loads(registry.read_text())
            entries = data.get("plugins", {})
        except (OSError, ValueError, AttributeError):
            entries = {}
        for key, installs in entries.items() if isinstance(entries, dict) else []:
            if key.split("@", 1)[0] != "imagegen2" or not isinstance(installs, list):
                continue
            for install in installs:
                if not isinstance(install, dict) or not install.get("installPath"):
                    continue
                cli = Path(install["installPath"]) / "skills" / "imagegen2" / "generate.cjs"
                found.append((version_key(str(install.get("version", ""))), cli))
        # Fall back to the cache layout if the registry is missing or unreadable.
        for cli in plugins_dir.glob("cache/*/imagegen2/*/skills/imagegen2/generate.cjs"):
            found.append((version_key(cli.parents[2].name), cli))
    found.sort(key=lambda item: item[0], reverse=True)
    return [cli for _, cli in found]


def imagegen2_candidates(start: Path) -> list[tuple[str, Path]]:
    candidates: list[tuple[str, Path]] = []
    override = os.environ.get("IMAGEGEN2_CLI")
    if override:
        candidates.append(("IMAGEGEN2_CLI", Path(override).expanduser()))
    candidates.append(("sibling skill", SKILL_DIR.parent / "imagegen2" / "generate.cjs"))
    for root in project_roots(start):
        for rel in (
            Path(".claude") / "skills" / "imagegen2",
            Path(".codex") / "skills" / "imagegen2",
            Path(".agents") / "skills" / "imagegen2",
            Path("skills") / "imagegen2",
            Path("imagegen2"),
        ):
            candidates.append(("project skill", root / rel / "generate.cjs"))
    for cli in plugin_candidates():
        candidates.append(("Claude Code plugin", cli))
    for root in user_skill_roots():
        candidates.append(("user skill", root / "skills" / "imagegen2" / "generate.cjs"))
    return candidates


def find_imagegen2(start: Path) -> tuple[str, Path]:
    for source, candidate in imagegen2_candidates(start):
        if candidate.is_file():
            return source, candidate
    raise SystemExit("ERROR: could not find imagegen2 generate.cjs")


def find_imagegen2_cli(start: Path) -> Path:
    return find_imagegen2(start)[1]


def imagegen2_version(cli: Path) -> str | None:
    try:
        match = re.search(r'IMAGEGEN2_VERSION\s*=\s*"([^"]+)"', cli.read_text(encoding="utf-8"))
    except OSError:
        return None
    return match.group(1) if match else None


def imagegen2_info(start: Path) -> dict:
    source, cli = find_imagegen2(start)
    version = imagegen2_version(cli)
    native_alpha = bool(version) and version_key(version) >= IMAGEGEN2_NATIVE_ALPHA_VERSION
    return {
        "path": str(cli),
        "source": source,
        "version": version,
        "nativeAlpha": native_alpha,
        "defaultSegmentation": "native-alpha" if native_alpha else "chroma-key",
    }


def main() -> None:
    args = parse_args()
    layout = layout_paths.resolve_layout(args.animation_id, args.start)
    runtime_tools = layout.runtime_tool_root
    runtime_config = SKILL_DIR / "runtime" / "config"
    paths = {
        "skill-dir": SKILL_DIR,
        "script-dir": SCRIPT_DIR,
        "init-package": SCRIPT_DIR / "init_package.py",
        "prepare-references": SCRIPT_DIR / "prepare_references.py",
        "validate-review-records": SCRIPT_DIR / "validate_review_records.py",
        "create-synthetic-frames": SCRIPT_DIR / "create_synthetic_frames.py",
        "runtime-tools": runtime_tools,
        "runtime-config": runtime_config,
        "align-frames": runtime_tools / "align_frames.py",
        "validate-sprites": runtime_tools / "validate_sprites.py",
        "make-contact-sheet": runtime_tools / "make_contact_sheet.py",
        "make-preview": runtime_tools / "make_preview.py",
        "export-gif": runtime_tools / "export_gif.py",
        "export-webp": runtime_tools / "export_webp.py",
        "export-bundle": runtime_tools / "export_bundle.py",
        "clean-reference": runtime_tools / "clean_reference.py",
        "brief-schema": runtime_config / "brief.schema.json",
        "template-animation-spec": runtime_config / "template.animation-spec.json",
    }
    if args.name == "imagegen2-cli":
        print(find_imagegen2_cli(Path(args.start)))
    elif args.name == "imagegen2-info":
        print(json.dumps(imagegen2_info(Path(args.start)), indent=2))
    elif args.name == "version":
        print(ANIM8GEN_VERSION)
    else:
        print(paths[args.name])


if __name__ == "__main__":
    main()
