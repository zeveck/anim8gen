# anim8gen

Generate short game sprite animations with an agent skill.

`anim8gen` turns prompts like “a cat pounces,” “a knight swings a sword,” or
“a pirate ship fights a kraken” into reviewable animation packages: generated
frames, aligned sprites or scenes, contact sheets, and an interactive HTML
preview.

It is designed for compact game loops and actions, not long-form video.

## See It

Click a preview to open the interactive playback page.

<p>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/">
    <img src="public/media/pirate-ship-kraken-cannon.gif" alt="anim8gen pirate ship kraken animation preview" width="100%">
  </a>
</p>

<p>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-cat-pounce-v2/">
    <img src="public/media/anim8gen-demo2.gif" alt="anim8gen cat pounce interactive preview" width="100%">
  </a>
</p>

anim8gen can produce tiny transparent sprites, character actions, and wider
scene loops:

- Scene animation: [Pirate Ship Kraken](https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/), [Space Station Explosion](https://zeveck.github.io/anim8gen/demos/sci-fi-space-station-explosion/)
- Character action: [Knight Sword Spark](https://zeveck.github.io/anim8gen/demos/quality-knight-sword-spark-v4/), [Cat Pounce](https://zeveck.github.io/anim8gen/demos/quality-cat-pounce-v2/)
- Small loops: [Cat Tail Swish](https://zeveck.github.io/anim8gen/demos/quality-cat-tail-swish-v4/), [Dragon Tail Flick](https://zeveck.github.io/anim8gen/demos/quality-dragon-tail-flick-v4/)

Full gallery: https://zeveck.github.io/anim8gen/

## Install

Ask your agent to install both skills:

```text
Install the anim8gen skill from github.com/zeveck/anim8gen.
anim8gen requires imagegen2, so also install the imagegen2 skill from
github.com/zeveck/imagegen2. After installing both, reload or restart the
agent so the skills are available.
```

`anim8gen` requires [`imagegen2`](https://github.com/zeveck/imagegen2) for
image generation.

## Configure

Configure `imagegen2` with an OpenAI API key. A typical setup is a project
`.env` file:

```text
OPENAI_API_KEY=sk-proj-your-key-here
```

`imagegen2` loads `.env` itself and reports missing or invalid credentials.

## Use

Ask your agent for a compact sprite animation. In Claude Code and similar
agents, you can ask in natural language with `Use anim8gen ...` or invoke the
skill directly with `/anim8gen ...`.

These are user-level briefs. anim8gen expands them into stricter per-frame
imagegen2 prompts with reference frames, transparent or scene background
handling, alignment, and review.

Optional request words:

- `gif` exports an animated GIF.
- `showit` opens the finished local preview when the run completes.
- `noshow` skips the preview-server offer.

For example, this asks for both a GIF and an opened preview:

```text
Use anim8gen gif showit to make a 3-frame transparent-background 16-bit RPG
pixel art sprite of a cute orange tabby cat facing the viewer while its tail
swishes left and right.
```

```text
Use anim8gen to make a wide 10-frame 16-bit RPG pixel art scene of a pirate
ship attacked by a kraken at sea, with the ship firing a cannon and the kraken
retreating.
```

Equivalent direct invocation:

```text
/anim8gen make a wide 10-frame 16-bit RPG pixel art scene of a pirate ship
attacked by a kraken at sea, with the ship firing a cannon and the kraken
retreating.
```

<p>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-000.calm.png" alt="Pirate ship kraken frame 1" width="180"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-001.water-bulge.png" alt="Pirate ship kraken frame 2" width="180"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-002.tentacles-rise.png" alt="Pirate ship kraken frame 3" width="180"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-003.kraken-looms.png" alt="Pirate ship kraken frame 4" width="180"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-004.cannon-aim.png" alt="Pirate ship kraken frame 5" width="180"></a>
</p>
<p>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-005.cannon-fire.png" alt="Pirate ship kraken frame 6" width="180"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-006.impact.png" alt="Pirate ship kraken frame 7" width="180"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-007.kraken-retreats.png" alt="Pirate ship kraken frame 8" width="180"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-008.submerging.png" alt="Pirate ship kraken frame 9" width="180"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/pirate-ship-kraken-cannon/"><img src="public/demos/pirate-ship-kraken-cannon/frames/frame-009.sea-settles.png" alt="Pirate ship kraken frame 10" width="180"></a>
</p>

```text
Use anim8gen to make a 4-frame 16-bit RPG pixel art scene of a large sci-fi
space station in deep space: intact station, flash, explosion, and debris.
```

Then ask for a tweak:

```text
Use anim8gen retry sci-fi-space-station-explosion to add a quiet floating-debris
aftermath after the explosion.
```

<p>
  <a href="https://zeveck.github.io/anim8gen/demos/sci-fi-space-station-explosion/"><img src="public/demos/sci-fi-space-station-explosion/frames/frame-000.idle.png" alt="Space station explosion frame 1" width="128"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/sci-fi-space-station-explosion/"><img src="public/demos/sci-fi-space-station-explosion/frames/frame-001.flash.png" alt="Space station explosion frame 2" width="128"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/sci-fi-space-station-explosion/"><img src="public/demos/sci-fi-space-station-explosion/frames/frame-002.explosion.png" alt="Space station explosion frame 3" width="128"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/sci-fi-space-station-explosion/"><img src="public/demos/sci-fi-space-station-explosion/frames/frame-003.debris.png" alt="Space station explosion frame 4" width="128"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/sci-fi-space-station-explosion/"><img src="public/demos/sci-fi-space-station-explosion/frames/frame-004.floating-debris.png" alt="Space station explosion frame 5" width="128"></a>
</p>

```text
Use anim8gen to make a 3-frame transparent-background 16-bit RPG pixel art
sprite of a small brown-haired knight with a blue cape and short sword, side
view facing right: ready, sword slash, then a small yellow spark at the sword
tip.
```

<p>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-knight-sword-spark-v4/"><img src="public/demos/quality-knight-sword-spark-v4/frames/frame-000.ready.png" alt="Knight sword spark frame 1" width="160"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-knight-sword-spark-v4/"><img src="public/demos/quality-knight-sword-spark-v4/frames/frame-001.slash.png" alt="Knight sword spark frame 2" width="160"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-knight-sword-spark-v4/"><img src="public/demos/quality-knight-sword-spark-v4/frames/frame-002.spark.png" alt="Knight sword spark frame 3" width="160"></a>
</p>

```text
Use anim8gen to make a 3-frame transparent-background 16-bit RPG pixel art
sprite of a cute orange tabby cat facing the viewer, sitting upright while its
tail swishes left and right.
```

<p>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-cat-tail-swish-v4/"><img src="public/demos/quality-cat-tail-swish-v4/frames/frame-000.sit.png" alt="Cat tail swish frame 1" width="160"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-cat-tail-swish-v4/"><img src="public/demos/quality-cat-tail-swish-v4/frames/frame-001.tail-left.png" alt="Cat tail swish frame 2" width="160"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-cat-tail-swish-v4/"><img src="public/demos/quality-cat-tail-swish-v4/frames/frame-002.tail-right.png" alt="Cat tail swish frame 3" width="160"></a>
</p>

```text
Use anim8gen to make a 4-frame transparent-background 16-bit RPG pixel art
sprite of a cute orange tabby cat adventurer facing the viewer: crouch, pounce,
soft landing, then return to crouch.
```

<p>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-cat-pounce-v2/"><img src="public/demos/quality-cat-pounce-v2/frames/frame-000.crouch.png" alt="Cat pounce frame 1" width="160"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-cat-pounce-v2/"><img src="public/demos/quality-cat-pounce-v2/frames/frame-001.pounce.png" alt="Cat pounce frame 2" width="160"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-cat-pounce-v2/"><img src="public/demos/quality-cat-pounce-v2/frames/frame-002.land.png" alt="Cat pounce frame 3" width="160"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-cat-pounce-v2/"><img src="public/demos/quality-cat-pounce-v2/frames/frame-003.crouch-return.png" alt="Cat pounce frame 4" width="160"></a>
</p>

```text
Use anim8gen to make a 3-frame transparent-background 16-bit RPG pixel art
sprite of a small cute green baby dragon, side view facing left, sitting with
its tail flicking upward and then curling back down.
```

<p>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-dragon-tail-flick-v4/"><img src="public/demos/quality-dragon-tail-flick-v4/frames/frame-000.idle.png" alt="Dragon tail flick frame 1" width="160"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-dragon-tail-flick-v4/"><img src="public/demos/quality-dragon-tail-flick-v4/frames/frame-001.tail-up.png" alt="Dragon tail flick frame 2" width="160"></a>
  <a href="https://zeveck.github.io/anim8gen/demos/quality-dragon-tail-flick-v4/"><img src="public/demos/quality-dragon-tail-flick-v4/frames/frame-002.happy.png" alt="Dragon tail flick frame 3" width="160"></a>
</p>

Details that help:

- subject and action
- style, such as `16-bit RPG pixel art`
- camera view, such as front, side, or isometric
- frame count, if important
- any reference image or sprite sheet to preserve identity

## Good Fits

- idle loops
- blinks, hops, pounces, emotes
- small object animations
- quick attacks and casts
- quick game asset exploration

Not a good fit for long cinematic animation, full directional sprite packs,
complex multi-character scenes, or production animation authoring.

## What Gets Produced

Each run creates a reviewable package with:

- raw generated candidates
- accepted aligned sprite frames
- a contact sheet
- visual review notes
- validation output
- an HTML preview page
- an animated GIF when the request includes `gif`

## Development

Maintainer notes live in [anim8gen/DEV_README.md](anim8gen/DEV_README.md).

Public demos are exported into `public/`:

```bash
python3 anim8gen/tools/export_public_demo.py <animation-id> [<animation-id> ...] --clean
```

## License

MIT. See [LICENSE](LICENSE).
