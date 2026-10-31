# Recording the narration

You record one line at a time. Each paragraph in a video's `narration.md` is one
line, and the animation stretches or shrinks to fit how long you take to say it.
You never have to match a timer.

## Before you start (once per computer)

1. Install PortAudio: `brew install portaudio` (macOS) or `sudo apt install portaudio19-dev` (Linux),
   then `make setup`.
2. Give your terminal app two permissions. The recorder listens for the `r` key
   and uses the mic:
   - **macOS:** System Settings → Privacy & Security → **Microphone** and
     **Input Monitoring**. Turn both on for Terminal (or iTerm, or VS Code), then
     quit and reopen it.
   - **Linux:** the key listener needs a desktop session (X11 or Wayland), not a
     plain SSH login.
3. Pick your mic: `make mics` prints a numbered list. Put the number in
   `config.toml` as `recorder_device = <number>`. If you skip this, you're asked
   to choose at the start of every scene.
4. Test it: `VOICE=recorder make voice-check`. That's two short lines that don't
   belong to any video, so nothing gets overwritten.

## Recording a video

1. Read the script out loud once: `videos/NN-slug/narration.md`. Fix anything
   that's awkward to say before recording it, because changing a line's words later
   means recording that line again.
2. Find a quiet room, put the mic a hand's width from your mouth, and start:

   ```bash
   make record VIDEO=01
   ```

3. For each line, the terminal shows a box with the words. Then:
   - **Hold `r`**, wait one second, say the line, wait one second, **let go of `r`**.
     The pauses get trimmed, and they keep the key click out of the audio.
   - Press **`l`** to listen, **`r`** to try again, or **`a`** to accept and move on.
4. When every line in a scene is accepted, that scene renders and the next one
   starts. You can stop any time with Ctrl+C. Accepted lines are saved, so the
   next `make record` picks up where you left off.

`make takes VIDEO=01` shows which lines are done:

```
## hook
  [x] 0  Every March, thousands of med students open an envelope at the...
  [ ] 1  How does one computer decide all of this fairly?
```

## Redoing a line

You accepted a take and later don't like it:

```bash
make redo VIDEO=01 SCENE=hook LINE=1   # one line (numbers come from `make takes`)
make redo VIDEO=01 SCENE=hook          # the whole scene
make record VIDEO=01                   # records only what's missing
```

If you edit a line's words in `narration.md`, that line is recorded again
automatically on the next `make record`, and the old take is ignored.

## Where the takes live

`videos/NN-slug/voiceovers/recorder/`, one mp3 per line. They are not committed
to git (they're large, and it's your voice), and `make clean` doesn't touch them.
Back that folder up if you want to keep it.

Once every line shows `[x]`, `make final VIDEO=01` renders the 1080p60 cut with
your voice.
