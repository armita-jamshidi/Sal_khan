"""Join Manim's per-scene .srt files into one caption track for the stitched video.

Manim writes `SceneName.srt` next to `SceneName.mp4`, one cue per voiceover
line, timed from the start of that scene. Stitching shifts each scene's cues by
the total length of the clips before it.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

_TIME = re.compile(r"(\d+):(\d+):(\d+)[,.](\d+)")
_TODO = re.compile(r"\s*\[TODO-VERIFY[^\]]*\]")


@dataclass
class Cue:
    start: float
    end: float
    text: str


def _seconds(stamp: str) -> float:
    h, m, s, ms = _TIME.match(stamp.strip()).groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, "0")[:3]) / 1000


def _stamp(seconds: float) -> str:
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def read_srt(path: str | Path) -> list[Cue]:
    cues = []
    for block in re.split(r"\n\s*\n", Path(path).read_text(encoding="utf-8").strip()):
        lines = block.strip().splitlines()
        timing = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if timing is None:
            continue
        start, end = lines[timing].split("-->")
        text = _TODO.sub("", "\n".join(lines[timing + 1:])).strip()
        if text:
            cues.append(Cue(_seconds(start), _seconds(end), text))
    return cues


def write_srt(cues: list[Cue], path: str | Path) -> None:
    blocks = [f"{i}\n{_stamp(c.start)} --> {_stamp(c.end)}\n{c.text}\n" for i, c in enumerate(cues, 1)]
    Path(path).write_text("\n".join(blocks), encoding="utf-8")


def clip_duration(path: str | Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def stitch_captions(clips: list[Path], output: str | Path) -> int:
    """Write one .srt for the clips played back to back. Returns the number of cues."""
    cues, offset = [], 0.0
    for clip in clips:
        srt = clip.with_suffix(".srt")
        if srt.exists():
            cues += [Cue(c.start + offset, c.end + offset, c.text) for c in read_srt(srt)]
        offset += clip_duration(clip)
    write_srt(cues, output)
    return len(cues)
