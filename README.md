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
| espeak-ng | offline placeholder voice when gTTS can't reach Google (optional on macOS, which has `say`) | `brew install espeak-ng` | `apt install espeak-ng` |
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
voice = "placeholder"   # robot voice for drafts
# voice = "recorder"    # record each narration line through your mic
```

`VOICE=recorder make preview VIDEO=01` overrides it for a single run.

The placeholder voice is gTTS. If Google can't be reached, it falls back to an
offline voice (espeak-ng, or `say` on macOS) and logs a warning, so previews still
render with realistic timing. `placeholder_engine` in `config.toml` pins one engine
(`"gtts"` or `"offline"`) if you'd rather not fall back.

`make voice-check` renders a 15-second clip with two narration lines. Run it with
`VOICE=recorder` to test your mic before recording a real video.

To record a video's narration, see [docs/recording.md](docs/recording.md). In short:
`make record VIDEO=01` to record, `make takes VIDEO=01` to see what's done, and
`make redo VIDEO=01 SCENE=hook LINE=1` to redo one line.

## Rendering

```bash
make preview VIDEO=01   # 480p15, fast
make final VIDEO=01     # 1080p60, stitched with ffmpeg
```

Output goes to `build/<video>/<quality>/`: the mp4 plus a matching `.srt` caption
file, built from the narration lines (TODO-VERIFY notes are left out). The stitched soundtrack is mixed to
-14 LUFS, YouTube's playback level, and each recorded line is leveled to -16 LUFS
when you accept it, so quiet and loud takes match. Both are set in `config.toml`.
