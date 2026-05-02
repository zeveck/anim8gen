#!/usr/bin/env python3
"""Generate a local HTML preview for aligned sprite frames."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--frames", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def aligned_name(frame: dict[str, Any]) -> str:
    return f"frame-{frame['index']:03d}.{frame['label']}.png"


def relative_src(path: Path, out_path: Path) -> str:
    return Path("../" + str(path.relative_to(out_path.parent.parent))).as_posix()


def warning_counts(validation: dict[str, Any]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for comparison in validation.get("comparisons", []):
        count = len(comparison.get("warnings", []))
        if not count:
            continue
        counts[comparison["from"]] = counts.get(comparison["from"], 0) + count
        counts[comparison["to"]] = counts.get(comparison["to"], 0) + count
    for failure in validation.get("structuralFailures", []):
        counts[failure["index"]] = counts.get(failure["index"], 0) + 1
    return counts


def build_payload(spec: dict[str, Any], validation: dict[str, Any], frames_dir: Path, out_path: Path) -> dict[str, Any]:
    counts = warning_counts(validation)
    frames = []
    for frame in spec["frames"]:
        path = frames_dir / aligned_name(frame)
        if not path.exists():
            raise FileNotFoundError(f"missing aligned frame: {path}")
        frames.append(
            {
                "index": frame["index"],
                "label": frame["label"],
                "pose": frame.get("pose", ""),
                "sleep": "sleep" in frame["label"] or "eyes closed" in frame.get("pose", ""),
                "warnings": counts.get(frame["index"], 0),
                "src": relative_src(path, out_path),
            }
        )
    return {
        "id": spec["id"],
        "canvas": spec["render"]["canvas"],
        "fps": spec["render"].get("fps", 8),
        "validationSummary": validation.get("summary", {}),
        "frames": frames,
    }


def render_html(payload: dict[str, Any]) -> str:
    payload_json = json.dumps(payload, separators=(",", ":"))
    title = html.escape(f"{payload['id']} preview")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #1d1d22;
      --muted: #66666f;
      --panel: #f6f4ee;
      --line: #cbc8bd;
      --accent: #2776b8;
      --warn: #c94a36;
      --checker-a: #d9d9d9;
      --checker-b: #f5f5f5;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background: #ece8dc;
      color: var(--ink);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    main {{
      width: min(980px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 24px 0 32px;
    }}
    header {{
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 16px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 12px;
    }}
    h1 {{
      margin: 0;
      font-size: 22px;
      line-height: 1.15;
      font-weight: 700;
      letter-spacing: 0;
    }}
    .meta {{
      color: var(--muted);
      font-size: 13px;
      text-align: right;
    }}
    .stage-row {{
      display: grid;
      grid-template-columns: minmax(280px, 1fr) 280px;
      gap: 20px;
      align-items: start;
    }}
    .stage {{
      position: relative;
      min-height: 540px;
      display: grid;
      place-items: center;
      border: 1px solid var(--line);
      background-color: var(--checker-b);
      background-image:
        linear-gradient(45deg, var(--checker-a) 25%, transparent 25%),
        linear-gradient(-45deg, var(--checker-a) 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, var(--checker-a) 75%),
        linear-gradient(-45deg, transparent 75%, var(--checker-a) 75%);
      background-size: 24px 24px;
      background-position: 0 0, 0 12px, 12px -12px, -12px 0;
      overflow: hidden;
    }}
    .stage.plain {{
      background: #f4f0e6;
    }}
    canvas {{
      width: min(512px, calc(100vw - 64px));
      height: auto;
      aspect-ratio: 1 / 1;
      image-rendering: pixelated;
      image-rendering: crisp-edges;
    }}
    .zs {{
      position: absolute;
      left: 50%;
      top: 39%;
      width: 160px;
      height: 140px;
      pointer-events: none;
      transform: translate(-4%, -50%);
      opacity: 0;
    }}
    .zs.active {{
      opacity: 1;
    }}
    .z {{
      position: absolute;
      color: #5b6db7;
      font-family: Georgia, "Times New Roman", serif;
      font-weight: 700;
      text-shadow: 0 2px 0 rgba(255, 255, 255, 0.75);
      animation: drift 1600ms linear infinite;
    }}
    .z:nth-child(1) {{ left: 18px; bottom: 12px; font-size: 22px; animation-delay: 0ms; }}
    .z:nth-child(2) {{ left: 60px; bottom: 44px; font-size: 28px; animation-delay: 260ms; }}
    .z:nth-child(3) {{ left: 106px; bottom: 82px; font-size: 36px; animation-delay: 520ms; }}
    @keyframes drift {{
      from {{ transform: translateY(16px); opacity: 0; }}
      20% {{ opacity: 1; }}
      78% {{ opacity: 1; }}
      to {{ transform: translateY(-26px); opacity: 0; }}
    }}
    .controls {{
      display: grid;
      gap: 12px;
      border: 1px solid var(--line);
      background: var(--panel);
      padding: 14px;
    }}
    .buttons {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
    }}
    button {{
      min-height: 38px;
      border: 1px solid #a8a496;
      background: #fffdf8;
      color: var(--ink);
      font: inherit;
      font-weight: 650;
      cursor: pointer;
    }}
    button:hover {{ border-color: var(--accent); }}
    label {{
      display: grid;
      gap: 6px;
      font-size: 13px;
      color: var(--muted);
    }}
    input[type="range"] {{ width: 100%; }}
    .toggles {{
      display: grid;
      gap: 8px;
    }}
    .toggle {{
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--ink);
    }}
    .frame-card {{
      border-top: 1px solid var(--line);
      padding-top: 12px;
      display: grid;
      gap: 4px;
    }}
    .frame-label {{
      font-size: 18px;
      font-weight: 700;
    }}
    .pose, .warnings {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
    }}
    .warnings.warn {{ color: var(--warn); font-weight: 650; }}
    .strip {{
      display: grid;
      grid-template-columns: repeat(8, minmax(0, 1fr));
      gap: 6px;
    }}
    .thumb {{
      border: 2px solid transparent;
      background: #fffdf8;
      padding: 2px;
      cursor: pointer;
    }}
    .thumb.active {{ border-color: var(--accent); }}
    .thumb img {{
      display: block;
      width: 100%;
      aspect-ratio: 1 / 1;
      object-fit: contain;
      image-rendering: pixelated;
      image-rendering: crisp-edges;
    }}
    @media (max-width: 760px) {{
      .stage-row {{ grid-template-columns: 1fr; }}
      .stage {{ min-height: min(520px, calc(100vw - 32px)); }}
      header {{ align-items: start; flex-direction: column; }}
      .meta {{ text-align: left; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{html.escape(payload["id"])}</h1>
      <div class="meta" id="meta"></div>
    </header>
    <div class="stage-row">
      <section class="stage" id="stage" aria-label="Sprite preview stage">
        <canvas id="sprite" width="{payload["canvas"][0]}" height="{payload["canvas"][1]}"></canvas>
        <div class="zs" id="zs" aria-hidden="true"><span class="z">Z</span><span class="z">Z</span><span class="z">Z</span></div>
      </section>
      <section class="controls" aria-label="Playback controls">
        <div class="buttons">
          <button type="button" id="prev" title="Previous frame">Prev</button>
          <button type="button" id="play" title="Play or pause">Pause</button>
          <button type="button" id="next" title="Next frame">Next</button>
        </div>
        <label>FPS <input type="range" id="fps" min="1" max="16" step="1"></label>
        <div class="toggles">
          <label class="toggle"><input type="checkbox" id="checker" checked> Checkerboard</label>
          <label class="toggle"><input type="checkbox" id="zToggle" checked> Sleeping Zs</label>
        </div>
        <div class="frame-card">
          <div class="frame-label" id="frameLabel"></div>
          <div class="pose" id="pose"></div>
          <div class="warnings" id="warnings"></div>
        </div>
        <div class="strip" id="strip"></div>
      </section>
    </div>
  </main>
  <script>
    const payload = {payload_json};
    const canvas = document.getElementById("sprite");
    const ctx = canvas.getContext("2d");
    const stage = document.getElementById("stage");
    const zs = document.getElementById("zs");
    const frameLabel = document.getElementById("frameLabel");
    const pose = document.getElementById("pose");
    const warningLabel = document.getElementById("warnings");
    const playButton = document.getElementById("play");
    const fpsInput = document.getElementById("fps");
    const checkerInput = document.getElementById("checker");
    const zToggle = document.getElementById("zToggle");
    const meta = document.getElementById("meta");
    const strip = document.getElementById("strip");
    const images = [];
    let frameIndex = 0;
    let playing = true;
    let lastTime = 0;

    ctx.imageSmoothingEnabled = false;
    fpsInput.value = payload.fps;
    meta.textContent = `${{payload.frames.length}} frames, ${{payload.validationSummary.warningCount || 0}} validation warnings`;

    function loadImages() {{
      return Promise.all(payload.frames.map((frame, index) => new Promise((resolve, reject) => {{
        const img = new Image();
        img.onload = () => {{
          images[index] = img;
          resolve();
        }};
        img.onerror = reject;
        img.src = frame.src;
      }})));
    }}

    function renderStrip() {{
      strip.innerHTML = "";
      payload.frames.forEach((frame, index) => {{
        const button = document.createElement("button");
        button.type = "button";
        button.className = "thumb";
        button.title = `${{frame.index}} ${{frame.label}}`;
        const img = document.createElement("img");
        img.alt = frame.label;
        img.src = frame.src;
        button.appendChild(img);
        button.addEventListener("click", () => {{
          frameIndex = index;
          render();
        }});
        strip.appendChild(button);
      }});
    }}

    function render() {{
      const frame = payload.frames[frameIndex];
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(images[frameIndex], 0, 0);
      frameLabel.textContent = `${{String(frame.index).padStart(3, "0")}} ${{frame.label}}`;
      pose.textContent = frame.pose;
      warningLabel.textContent = frame.warnings ? `${{frame.warnings}} linked validation warnings` : "No linked validation warnings";
      warningLabel.classList.toggle("warn", frame.warnings > 0);
      zs.classList.toggle("active", zToggle.checked && frame.sleep);
      [...strip.children].forEach((child, index) => child.classList.toggle("active", index === frameIndex));
    }}

    function step(delta) {{
      frameIndex = (frameIndex + delta + payload.frames.length) % payload.frames.length;
      render();
    }}

    function tick(time) {{
      const interval = 1000 / Number(fpsInput.value || payload.fps);
      if (playing && time - lastTime >= interval) {{
        step(1);
        lastTime = time;
      }}
      requestAnimationFrame(tick);
    }}

    document.getElementById("prev").addEventListener("click", () => step(-1));
    document.getElementById("next").addEventListener("click", () => step(1));
    playButton.addEventListener("click", () => {{
      playing = !playing;
      playButton.textContent = playing ? "Pause" : "Play";
    }});
    checkerInput.addEventListener("change", () => stage.classList.toggle("plain", !checkerInput.checked));
    zToggle.addEventListener("change", render);

    loadImages().then(() => {{
      renderStrip();
      render();
      requestAnimationFrame(tick);
    }}).catch((error) => {{
      frameLabel.textContent = "Preview failed to load";
      pose.textContent = String(error);
    }});
  </script>
</body>
</html>
"""


def main() -> None:
    args = parse_args()
    spec_path = Path(args.spec)
    validation_path = Path(args.validation)
    out_path = Path(args.out)
    spec = json.loads(spec_path.read_text())
    validation = json.loads(validation_path.read_text())
    payload = build_payload(spec, validation, Path(args.frames), out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_html(payload), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
