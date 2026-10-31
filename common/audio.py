"""Loudness helpers built on ffmpeg's loudnorm filter (EBU R128).

Two levels, set in config.toml:
    take_lufs  -> each recorded line is leveled to this once, right after you accept it,
                  so a line you said quietly doesn't dip under the rest.
    final_lufs -> the stitched video's soundtrack. YouTube plays everything back at
                  about -14 LUFS, so mixing to that means it isn't turned down or up.
"""

from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
from pathlib import Path

TRUE_PEAK = -1.5   # dBTP, headroom so lossy encoding doesn't clip
LOUDNESS_RANGE = 11


def measure(path: str | Path, target: float) -> dict:
    """First loudnorm pass: measure the file without writing anything."""
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vn",
         "-af", f"loudnorm=I={target}:TP={TRUE_PEAK}:LRA={LOUDNESS_RANGE}:print_format=json",
         "-f", "null", "-"],
        check=True, capture_output=True, text=True,
    )
    return json.loads(re.findall(r"\{[^{}]*\}", result.stderr)[-1])


def has_audio(path: str | Path) -> bool:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
         "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return bool(result.stdout.strip())


def loudnorm_filter(path: str | Path, target: float) -> str | None:
    """Second-pass filter string, or None for silence. Linear mode keeps the speech dynamics."""
    m = measure(path, target)
    if not math.isfinite(float(m["input_i"])):
        return None
    return (
        f"loudnorm=I={target}:TP={TRUE_PEAK}:LRA={LOUDNESS_RANGE}"
        f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
        f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
        f":offset={m['target_offset']}:linear=true"
    )


def level_audio_file(path: str | Path, target: float) -> None:
    """Level an audio file in place."""
    path = Path(path)
    audio_filter = loudnorm_filter(path, target)
    if audio_filter is None:
        return
    tmp = path.with_name(path.stem + ".leveling" + path.suffix)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(path),
         "-af", audio_filter, "-ar", "48000", str(tmp)],
        check=True,
    )
    tmp.replace(path)


def level_video(src: str | Path, dst: str | Path, target: float) -> None:
    """Copy the video stream and re-encode the audio at the target loudness."""
    audio_filter = loudnorm_filter(src, target) if has_audio(src) else None
    if audio_filter is None:
        shutil.copyfile(src, dst)
        return
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-c:v", "copy", "-af", audio_filter,
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(dst)],
        check=True,
    )


def integrated_loudness(path: str | Path) -> float:
    return float(measure(path, -14)["input_i"])
