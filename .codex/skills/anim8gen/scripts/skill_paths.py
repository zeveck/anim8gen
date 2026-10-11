#!/usr/bin/env python3
"""Print install-independent anim8gen skill helper paths."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import layout_paths


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

ANIM8GEN_VERSION = "2026.10.11"

# imagegen2 releases from this version on support --transparent-mode
# native-alpha (GPT Image 2.5). Older copies only offer chroma-key. Used only
# when the dry-run probe below can't run.
IMAGEGEN2_NATIVE_ALPHA_VERSION = (2026, 10, 11)


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
    """The start directory and its parents, except the home directory.

    Home-level skill folders are user installs; they are checked after Claude
    Code plugin installs so a stale copied skill can't shadow a managed plugin.
    """
    home = Path.home().resolve()
    return [root for root in [start.resolve(), *start.resolve().parents] if root != home]


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


def plugin_install_applies(install: dict, start: Path) -> bool:
    """User installs apply everywhere; project/local installs only inside their project."""
    if install.get("scope", "user") == "user":
        return True
    project_path = install.get("projectPath")
    if not project_path:
        return False
    project = Path(project_path).expanduser().resolve()
    here = start.resolve()
    return here == project or project in here.parents


# Where generate.cjs sits inside an imagegen2 plugin install: the plugin is
# rooted at the repo's skills/ folder (v2026.10.11 as published); the second
# path covers an install rooted at the repo itself.
PLUGIN_CLI_PATHS = (Path("imagegen2") / "generate.cjs", Path("skills") / "imagegen2" / "generate.cjs")


def plugin_candidates(start: Path) -> list[Path]:
    """imagegen2 CLIs from Claude Code plugin installs, newest version first."""
    found: list[tuple[tuple[int, ...], Path]] = []
    for config_dir in claude_config_dirs():
        plugins_dir = config_dir / "plugins"
        registry = plugins_dir / "installed_plugins.json"
        try:
            entries = json.loads(registry.read_text()).get("plugins", {})
            readable = isinstance(entries, dict)
        except (OSError, ValueError, AttributeError):
            entries, readable = {}, False
        for key, installs in entries.items() if readable else []:
            if key.split("@", 1)[0] != "imagegen2" or not isinstance(installs, list):
                continue
            for install in installs:
                if not isinstance(install, dict) or not install.get("installPath"):
                    continue
                if not plugin_install_applies(install, start):
                    continue
                key = version_key(str(install.get("version", "")))
                for rel in PLUGIN_CLI_PATHS:
                    found.append((key, Path(install["installPath"]) / rel))
        if not readable:
            # No usable registry: fall back to the cache layout.
            for rel in PLUGIN_CLI_PATHS:
                for cli in plugins_dir.glob(f"cache/*/imagegen2/*/{rel.as_posix()}"):
                    version_dir = cli.parents[len(rel.parts) - 1]
                    found.append((version_key(version_dir.name), cli))
    found.sort(key=lambda item: item[0], reverse=True)
    return [cli for _, cli in found]


def imagegen2_candidates(start: Path) -> list[tuple[str, Path]]:
    candidates: list[tuple[str, Path]] = []
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
    for cli in plugin_candidates(start):
        candidates.append(("Claude Code plugin", cli))
    for root in user_skill_roots():
        candidates.append(("user skill", root / "skills" / "imagegen2" / "generate.cjs"))
    return candidates


def find_imagegen2(start: Path) -> tuple[str, Path]:
    override = os.environ.get("IMAGEGEN2_CLI")
    if override:
        cli = Path(override).expanduser()
        if not cli.is_file():
            raise SystemExit(f"ERROR: IMAGEGEN2_CLI points to a missing file: {cli}")
        return "IMAGEGEN2_CLI", cli
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


def probe_transparency(cli: Path, start: Path) -> dict | None:
    """Ask imagegen2 how it would handle a transparent request in this project.

    A dry run needs no API key and makes no API call, but it applies the
    project's .env and IMAGEGEN2_MODEL, so it reports the model that frames
    will actually use. Returns None if the probe can't run (no node, old CLI
    output, timeout).
    """
    with tempfile.TemporaryDirectory() as tmp:
        try:
            result = subprocess.run(
                [
                    "node",
                    str(cli),
                    "--dry-run",
                    "--prompt",
                    "anim8gen transparency probe",
                    "--output",
                    str(Path(tmp) / "probe.png"),
                    "--background",
                    "transparent",
                ],
                cwd=start,
                text=True,
                capture_output=True,
                timeout=30,
            )
        except (OSError, subprocess.SubprocessError):
            return None
    try:
        payload = json.loads(result.stdout)
    except ValueError:
        return None
    return payload if isinstance(payload, dict) else None


def imagegen2_info(start: Path) -> dict:
    source, cli = find_imagegen2(start)
    version = imagegen2_version(cli)
    probe = probe_transparency(cli, start)
    if probe is not None:
        native_alpha = bool(probe.get("success")) and probe.get("transparentMode") == "native-alpha"
        detail = None if native_alpha else probe.get("error")
        model = probe.get("model")
        if not model and isinstance(detail, str):
            # imagegen2 errors don't carry a model field; its transparency
            # error starts with the model name.
            match = re.match(r"(\S+) does not support", detail)
            model = match.group(1) if match else None
    else:
        native_alpha = bool(version) and version_key(version) >= IMAGEGEN2_NATIVE_ALPHA_VERSION
        model = None
        detail = "dry-run probe unavailable; decided from the imagegen2 version"
    return {
        "path": str(cli),
        "source": source,
        "version": version,
        "model": model,
        "nativeAlpha": native_alpha,
        "defaultSegmentation": "native-alpha" if native_alpha else "chroma-key",
        "detail": detail,
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
