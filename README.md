# Algorithm Explainers

A reusable Python pipeline that turns class notes on algorithms into 5–7 minute
explainer videos. Every animation is driven by real, tested algorithm code: each
video's `algorithm.py` returns an event log, and its Manim scenes replay that log,
so changing the example data changes the animation.

> Work in progress. A full README with a demo GIF comes once video 1 is finished.

## Layout

```
common/          shared Manim style, icons, intro/outro templates, narration loader
notes/inbox/     drop new class notes here
notes/used/      notes that already became a video
videos/NN-slug/  one folder per video: algorithm.py, tests/, outline.md, narration.md, scenes.py
pipeline/        render + stitch script, and later the 2-day cycle prompt
config.toml      pipeline settings, including the voice switch
```

## Setup

Python 3.11 or 3.12 (manimpango has no wheels for 3.13 yet).

System dependencies:

| Tool | Why | macOS | Ubuntu/Debian |
| --- | --- | --- | --- |
| ffmpeg | stitching and encoding | `brew install ffmpeg` | `apt install ffmpeg` |
| Cairo + Pango | Manim text rendering | `brew install cairo pango pkg-config` | `apt install libcairo2-dev libpango1.0-dev pkg-config` |
| PortAudio | recording narration through the mic | `brew install portaudio` | `apt install portaudio19-dev` |
| SoX | audio trimming in manim-voiceover | `brew install sox` | `apt install sox` |
| Inter font | channel font (falls back to system sans) | [rsms.me/inter](https://rsms.me/inter/) | `apt install fonts-inter` |

LaTeX is not needed: all on-screen text uses `Text`, not `Tex`.

```bash
make setup     # creates .venv and installs requirements.txt
make test      # runs pytest for common/ and every video
make style     # renders the shared style reel at low quality
```

## Voice

`config.toml` has one switch:

```toml
voice = "placeholder"   # gTTS robot voice for drafts
# voice = "recorder"    # record each narration line through your mic
```

`VOICE=recorder make preview VIDEO=01` overrides it for a single run.

## Rendering

```bash
make preview VIDEO=01   # 480p15, fast
make final VIDEO=01     # 1080p60, stitched with ffmpeg
```

Output goes to `build/<video>/<quality>/`.
