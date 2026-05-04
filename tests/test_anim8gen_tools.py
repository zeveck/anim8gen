#!/usr/bin/env python3
"""Lightweight regression tests for local anim8gen tools."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageSequence


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "anim8gen" / "tools"
sys.path.insert(0, str(TOOLS_DIR))

import align_frames  # noqa: E402
import export_bundle  # noqa: E402
import export_gif  # noqa: E402
import export_public_demo  # noqa: E402
import make_preview  # noqa: E402

SKILL_SCRIPT_DIR = REPO_ROOT / ".codex" / "skills" / "anim8gen" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPT_DIR))

import layout_paths  # noqa: E402


INIT_PACKAGE_SCRIPT = SKILL_SCRIPT_DIR / "init_package.py"


def write_frame(path: Path, color: tuple[int, int, int, int], pixel: tuple[int, int] = (1, 1)) -> None:
    image = Image.new("RGBA", (4, 4), (0, 0, 0, 0))
    image.putpixel(pixel, color)
    image.save(path)


def base_spec(animation_id: str = "fixture") -> dict:
    return {
        "id": animation_id,
        "render": {"canvas": [4, 4], "fps": 4},
        "segmentation": {"alphaThreshold": 8, "chromaKey": "#ff00ff", "chromaTolerance": 24},
        "alignment": {"defaultAnchor": "body_center", "floorY": 3},
        "generation": {
            "candidateManifest": f"anim8gen/assets/{animation_id}/manifests/candidates.jsonl",
            "acceptedManifest": f"anim8gen/assets/{animation_id}/manifests/accepted-frames.json",
        },
        "preview": {},
        "frames": [
            {"index": 0, "label": "idle", "pose": "idle"},
            {"index": 1, "label": "hop", "pose": "hop"},
            {"index": 2, "label": "return", "pose": "return", "reuseFrame": 0},
        ],
    }


def gif_frames(path: Path) -> list[Image.Image]:
    with Image.open(path) as image:
        return [frame.convert("RGBA") for frame in ImageSequence.Iterator(image)]


def brief(animation_id: str = "trex-roar-v1") -> dict:
    return {
        "id": animation_id,
        "subject": "tyrannosaurus roaring",
        "style": "pixel art",
        "frames": [
            {"index": 0, "label": "idle", "pose": "standing"},
            {"index": 1, "label": "roar", "pose": "mouth open"},
            {"index": 2, "label": "settle", "pose": "mouth closing"},
        ],
    }


def test_export_gif_dimensions_frame_count_and_terminal_reuse() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        frames_dir = root / "frames"
        frames_dir.mkdir()
        spec = base_spec()
        write_frame(frames_dir / "frame-000.idle.png", (255, 0, 0, 255))
        write_frame(frames_dir / "frame-001.hop.png", (0, 255, 0, 255))
        write_frame(frames_dir / "frame-002.return.png", (0, 0, 255, 255))

        assert export_gif.playback_indexes(spec) == [0, 1]

        out = root / "out.gif"
        export_gif.export_gif(spec, frames_dir, out, fps=4, scale=2)
        frames = gif_frames(out)
        assert out.exists()
        assert frames[0].size == (8, 8)
        assert len(frames) == 2


def test_non_terminal_reuse_is_preserved() -> None:
    spec = base_spec()
    spec["frames"] = [
        {"index": 0, "label": "idle", "pose": "idle"},
        {"index": 1, "label": "hold", "pose": "hold", "reuseFrame": 0},
        {"index": 2, "label": "hop", "pose": "hop"},
    ]
    assert export_gif.playback_indexes(spec) == [0, 1, 2]
    assert make_preview.build_payload_for_indexes(spec) == [0, 1, 2]


def test_terminal_reuse_can_be_played_when_requested() -> None:
    spec = base_spec()
    spec["preview"] = {"playTerminalReuseFrame": True}
    assert export_gif.playback_indexes(spec) == [0, 1, 2]
    assert make_preview.build_payload_for_indexes(spec) == [0, 1, 2]


def test_display_offsets_affect_gif_pixels() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        frames_dir = root / "frames"
        frames_dir.mkdir()
        spec = base_spec()
        spec["preview"] = {"displayOffsets": {"0": {"x": 1, "y": 1}}}
        spec["frames"] = [{"index": 0, "label": "idle", "pose": "idle"}, {"index": 1, "label": "hop", "pose": "hop"}]
        write_frame(frames_dir / "frame-000.idle.png", (255, 0, 0, 255), pixel=(0, 0))
        write_frame(frames_dir / "frame-001.hop.png", (0, 255, 0, 255), pixel=(0, 0))

        out = root / "offset.gif"
        export_gif.export_gif(spec, frames_dir, out, fps=4, scale=1)
        first = gif_frames(out)[0]
        assert first.getpixel((1, 1))[3] > 0
        assert first.getpixel((0, 0))[3] == 0


def test_preview_and_public_demo_use_same_frame_order() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        workspace = root / "anim8gen"
        frames_dir = workspace / "assets" / "fixture" / "aligned"
        reports_dir = workspace / "reports"
        config_dir = workspace / "config"
        preview_dir = workspace / "preview"
        for path in (frames_dir, reports_dir, config_dir, preview_dir):
            path.mkdir(parents=True)

        spec = base_spec("fixture")
        (config_dir / "fixture.json").write_text(json.dumps(spec))
        (reports_dir / "fixture.validation.json").write_text(json.dumps({"frames": []}))
        write_frame(frames_dir / "frame-000.idle.png", (255, 0, 0, 255))
        write_frame(frames_dir / "frame-001.hop.png", (0, 255, 0, 255))
        write_frame(frames_dir / "frame-002.return.png", (0, 0, 255, 255))

        preview_payload = make_preview.build_payload(
            spec,
            {"frames": []},
            frames_dir,
            preview_dir / "fixture.html",
        )
        export_public_demo.export_demo("fixture", workspace, root / "public", clean=True)
        html = (root / "public" / "demos" / "fixture" / "index.html").read_text()

        assert preview_payload["playbackIndexes"] == [0, 1]
        assert '"playbackIndexes":[0,1]' in html
        assert (root / "public" / "demos" / "fixture" / "frames" / "frame-001.hop.png").exists()


def test_preview_uses_paths_relative_to_output_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        frames_dir = root / "assets" / "anim8gen" / "fixture" / "frames"
        preview_out = root / "assets" / "anim8gen" / "fixture" / "preview.html"
        frames_dir.mkdir(parents=True)
        spec = base_spec("fixture")
        write_frame(frames_dir / "frame-000.idle.png", (255, 0, 0, 255))
        write_frame(frames_dir / "frame-001.hop.png", (0, 255, 0, 255))
        write_frame(frames_dir / "frame-002.return.png", (0, 0, 255, 255))

        payload = make_preview.build_payload(spec, {"frames": []}, frames_dir, preview_out)

        assert [frame["src"] for frame in payload["frames"]] == [
            "frames/frame-000.idle.png",
            "frames/frame-001.hop.png",
            "frames/frame-002.return.png",
        ]


def test_export_bundle_writes_visible_deliverables_without_manifests() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        run_root = project / ".anim8gen" / "runs" / "fixture"
        for path in [
            run_root / "config",
            run_root / "aligned",
            run_root / "raw",
            run_root / "manifests",
            run_root / "reports",
            run_root / "gifs",
        ]:
            path.mkdir(parents=True)

        spec = base_spec("fixture")
        spec["generation"]["acceptedManifest"] = str(run_root / "manifests" / "accepted-frames.json")
        spec_path = run_root / "config" / "fixture.json"
        spec_path.write_text(json.dumps(spec))
        (run_root / "reports" / "fixture.validation.json").write_text(json.dumps({"frames": []}))
        for frame in spec["frames"]:
            write_frame(run_root / "aligned" / make_preview.aligned_name(frame), (frame["index"] * 40, 120, 200, 255))
            shutil.copy2(run_root / "aligned" / make_preview.aligned_name(frame), run_root / "raw" / f"raw-{frame['index']}.png")
        (run_root / "manifests" / "accepted-frames.json").write_text(
            json.dumps(
                {
                    "frames": [
                        {"index": frame["index"], "raw": str(run_root / "raw" / f"raw-{frame['index']}.png")}
                        for frame in spec["frames"]
                    ]
                }
            )
        )

        gif_path = run_root / "gifs" / "fixture.gif"
        export_gif.export_gif(spec, run_root / "aligned", gif_path, fps=4, scale=1)
        out_dir = project / "assets" / "anim8gen" / "fixture"
        result = export_bundle.export_bundle(spec_path, out_dir)
        html = (out_dir / "preview.html").read_text()

        assert result["rawFrames"] == 0
        assert (out_dir / "frames" / "frame-001.hop.png").exists()
        assert (out_dir / "preview.html").exists()
        assert (out_dir / "fixture.gif").exists()
        assert not (out_dir / "manifests").exists()
        assert not (out_dir / "reports").exists()
        assert not (out_dir / "raw").exists()
        assert '"src":"frames/frame-000.idle.png"' in html


def test_export_bundle_exports_raw_when_candidates_differ() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp)
        run_root = project / ".anim8gen" / "runs" / "fixture"
        for path in [run_root / "config", run_root / "aligned", run_root / "raw", run_root / "manifests"]:
            path.mkdir(parents=True)

        spec = base_spec("fixture")
        spec["generation"]["acceptedManifest"] = str(run_root / "manifests" / "accepted-frames.json")
        spec_path = run_root / "config" / "fixture.json"
        spec_path.write_text(json.dumps(spec))
        for frame in spec["frames"]:
            write_frame(run_root / "aligned" / make_preview.aligned_name(frame), (0, 0, 255, 255))
            write_frame(run_root / "raw" / f"raw-{frame['index']}.png", (255, 0, 0, 255))
        (run_root / "manifests" / "accepted-frames.json").write_text(
            json.dumps(
                {
                    "frames": [
                        {"index": frame["index"], "raw": str(run_root / "raw" / f"raw-{frame['index']}.png")}
                        for frame in spec["frames"]
                    ]
                }
            )
        )

        out_dir = project / "assets" / "anim8gen" / "fixture"
        result = export_bundle.export_bundle(spec_path, out_dir)

        assert result["rawFrames"] == 3
        assert (out_dir / "raw" / "frame-000.idle.png").exists()


def test_chroma_key_color_families_are_background() -> None:
    for key, family_pixel in [
        ("#ff00ff", (230, 35, 225, 255)),
        ("#00ff00", (30, 230, 35, 255)),
        ("#00ffff", (25, 225, 230, 255)),
    ]:
        spec = {"segmentation": {"alphaThreshold": 8, "chromaKey": key, "chromaTolerance": 12}}
        assert not align_frames.is_visible(family_pixel, spec)
        assert align_frames.is_visible((120, 80, 40, 255), spec)


def test_anim8gen_layout_defaults_keep_state_hidden_and_exports_visible() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "client"
        project.mkdir()
        layout = layout_paths.resolve_layout("trex-roar-v1", project, env={})

        assert layout.project_root == project.resolve()
        assert layout.workspace_root == project / ".anim8gen"
        assert layout.run_root == project / ".anim8gen" / "runs" / "trex-roar-v1"
        assert layout.spec_path == project / ".anim8gen" / "runs" / "trex-roar-v1" / "config" / "trex-roar-v1.json"
        assert layout.export_root == project / "assets" / "anim8gen" / "trex-roar-v1"
        assert layout.export_frames_dir == project / "assets" / "anim8gen" / "trex-roar-v1" / "frames"
        assert layout.runtime_tool_root == REPO_ROOT / ".codex" / "skills" / "anim8gen" / "runtime" / "tools"
        assert not layout.scratch_root.is_relative_to(project)


def test_anim8gen_layout_environment_overrides() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "client"
        project.mkdir()
        env = {
            "ANIM8GEN_WORKSPACE_ROOT": ".state/anim8gen",
            "ANIM8GEN_EXPORT_ROOT": "dist/sprites",
            "ANIM8GEN_TMPDIR": str(Path(tmp) / "scratch-base"),
        }
        layout = layout_paths.resolve_layout("orb-cast", project, env=env)

        assert layout.workspace_root == project / ".state" / "anim8gen"
        assert layout.run_root == project / ".state" / "anim8gen" / "runs" / "orb-cast"
        assert layout.export_root == project / "dist" / "sprites" / "orb-cast"
        assert layout.scratch_root == Path(tmp) / "scratch-base" / "orb-cast" / "scratch"


def test_anim8gen_layout_keeps_explicit_legacy_spec_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "client"
        legacy_config = project / "anim8gen" / "config"
        legacy_config.mkdir(parents=True)
        legacy_spec = legacy_config / "old-run.json"
        legacy_spec.write_text("{}\n")

        layout = layout_paths.resolve_layout("old-run", project, env={})

        assert layout.legacy_spec_path == legacy_spec
        assert layout.legacy_spec_path.exists()
        assert layout.spec_path != legacy_spec


def test_anim8gen_skill_runtime_bundle_is_minimal_and_self_contained() -> None:
    skill_dir = SKILL_SCRIPT_DIR.parent
    runtime_tools = skill_dir / "runtime" / "tools"
    runtime_config = skill_dir / "runtime" / "config"

    expected_tools = {
        "align_frames.py",
        "export_bundle.py",
        "export_gif.py",
        "make_contact_sheet.py",
        "make_preview.py",
        "validate_sprites.py",
    }
    expected_config = {"brief.schema.json", "template.animation-spec.json"}

    assert {path.name for path in runtime_tools.iterdir() if path.is_file()} == expected_tools
    assert {path.name for path in runtime_config.iterdir() if path.is_file()} == expected_config
    assert not (runtime_tools / "export_public_demo.py").exists()
    assert not (skill_dir / "runtime" / "DEV_README.md").exists()
    assert "anim8gen/assets" not in (runtime_config / "template.animation-spec.json").read_text()


def test_repo_demo_sources_are_outside_installable_workbench() -> None:
    repo_config = REPO_ROOT / "anim8gen" / "config"
    repo_reports = REPO_ROOT / "anim8gen" / "reports"
    source_runtime_config = REPO_ROOT / "anim8gen" / "runtime" / "config"
    example_specs = REPO_ROOT / "examples" / "specs"

    expected_specs = {
        "deterministic-square-hop.json",
        "pirate-ship-kraken-cannon.json",
        "quality-cat-pounce-v2.json",
        "quality-cat-tail-swish-v4.json",
        "quality-dragon-tail-flick-v4.json",
        "quality-knight-sword-spark-v4.json",
        "sci-fi-space-station-explosion.json",
    }

    assert not repo_config.exists()
    assert not repo_reports.exists()
    assert {path.name for path in source_runtime_config.iterdir() if path.is_file()} == {
        "brief.schema.json",
        "template.animation-spec.json",
    }
    assert {path.name for path in example_specs.iterdir() if path.is_file()} == expected_specs
    assert "anim8gen/assets" not in (source_runtime_config / "template.animation-spec.json").read_text()


def test_skill_paths_resolves_bundled_runtime_tools_without_source_workbench() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "client"
        project.mkdir()
        copied_skill = Path(tmp) / "skills" / "anim8gen"
        shutil.copytree(SKILL_SCRIPT_DIR.parent, copied_skill)

        result = subprocess.run(
            [
                sys.executable,
                str(copied_skill / "scripts" / "skill_paths.py"),
                "align-frames",
                "--start",
                str(project),
            ],
            check=True,
            text=True,
            capture_output=True,
        )

        resolved = Path(result.stdout.strip())
        assert resolved == copied_skill / "runtime" / "tools" / "align_frames.py"
        assert resolved.exists()
        assert not (project / "anim8gen").exists()


def test_init_package_defaults_to_hidden_workspace_without_visible_anim8gen_root() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "client"
        project.mkdir()
        brief_path = Path(tmp) / "trex.brief.json"
        brief_path.write_text(json.dumps(brief()))

        subprocess.run(
            [
                sys.executable,
                str(INIT_PACKAGE_SCRIPT),
                "--brief",
                str(brief_path),
                "--project-root",
                str(project),
            ],
            check=True,
            text=True,
            capture_output=True,
        )

        run_root = project / ".anim8gen" / "runs" / "trex-roar-v1"
        spec_path = run_root / "config" / "trex-roar-v1.json"
        package_manifest_path = run_root / "manifests" / "package-manifest.json"
        accepted_manifest_path = run_root / "manifests" / "accepted-frames.json"

        assert run_root.exists()
        assert not (project / "anim8gen").exists()
        assert spec_path.exists()
        assert package_manifest_path.exists()
        assert accepted_manifest_path.exists()
        for path in [run_root / "reference", run_root / "raw", run_root / "aligned", run_root / "review"]:
            assert (path / ".gitkeep").exists()

        spec_text = spec_path.read_text()
        assert "anim8gen/assets" not in spec_text
        assert "anim8gen/config" not in spec_text
        assert "anim8gen/preview" not in spec_text
        assert "anim8gen/reports" not in spec_text

        spec = json.loads(spec_text)
        assert spec["asset"]["canonicalReference"] == ".anim8gen/runs/trex-roar-v1/reference/reference.png"
        assert spec["generation"]["candidateManifest"] == ".anim8gen/runs/trex-roar-v1/manifests/candidates.jsonl"
        assert spec["generation"]["acceptedManifest"] == ".anim8gen/runs/trex-roar-v1/manifests/accepted-frames.json"

        accepted_manifest = json.loads(accepted_manifest_path.read_text())
        assert (
            accepted_manifest["generator"]["candidateManifest"]
            == ".anim8gen/runs/trex-roar-v1/manifests/candidates.jsonl"
        )

        package_manifest = json.loads(package_manifest_path.read_text())
        assert package_manifest["runRoot"] == ".anim8gen/runs/trex-roar-v1"
        assert package_manifest["spec"] == ".anim8gen/runs/trex-roar-v1/config/trex-roar-v1.json"
        assert package_manifest["preview"] == ".anim8gen/runs/trex-roar-v1/preview/trex-roar-v1.html"
        assert package_manifest["export"] == "assets/anim8gen/trex-roar-v1"


def test_init_package_root_alias_writes_self_consistent_run_paths() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "client"
        project.mkdir()
        brief_path = Path(tmp) / "orb.brief.json"
        brief_path.write_text(json.dumps(brief("orb-cast")))

        subprocess.run(
            [
                sys.executable,
                str(INIT_PACKAGE_SCRIPT),
                "--brief",
                str(brief_path),
                "--project-root",
                str(project),
                "--root",
                ".anim8gen/runs/orb-cast",
            ],
            check=True,
            text=True,
            capture_output=True,
        )

        run_root = project / ".anim8gen" / "runs" / "orb-cast"
        spec = json.loads((run_root / "config" / "orb-cast.json").read_text())
        package_manifest = json.loads((run_root / "manifests" / "package-manifest.json").read_text())

        assert spec["generation"]["candidateManifest"] == ".anim8gen/runs/orb-cast/manifests/candidates.jsonl"
        assert package_manifest["runRoot"] == ".anim8gen/runs/orb-cast"
        assert "export" not in package_manifest
        assert not (project / "anim8gen").exists()


def run() -> None:
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")


if __name__ == "__main__":
    run()
