"""See which narration lines you've recorded, and redo any of them.

    python -m pipeline.takes 01                  # every line, recorded or not
    python -m pipeline.takes 01 --redo hook 2    # forget line 2 of `## hook`
    python -m pipeline.takes 01 --redo hook      # forget every line of `## hook`
    python -m pipeline.takes --devices           # list microphones

A forgotten line is recorded again the next time you render with
VOICE=recorder. Editing a line's words in narration.md does the same thing
automatically, because takes are matched by their exact text.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common.narration import load_narration
from pipeline.render import find_video_dir

CACHE_FILE = "cache.json"


def recorder_dir(video_dir: Path) -> Path:
    return video_dir / "voiceovers" / "recorder"


def load_takes(video_dir: Path) -> list[dict]:
    cache = recorder_dir(video_dir) / CACHE_FILE
    return json.loads(cache.read_text()) if cache.exists() else []


def recorded_texts(takes: list[dict]) -> set[str]:
    return {t["input_data"]["input_text"] for t in takes if t.get("input_data", {}).get("service") == "recorder"}


def list_takes(video_dir: Path) -> None:
    narration = load_narration(video_dir / "narration.md")
    done = recorded_texts(load_takes(video_dir))
    total = sum(len(lines) for lines in narration.values())
    count = 0
    for scene_id, lines in narration.items():
        print(f"## {scene_id}")
        for i, line in enumerate(lines):
            mark = "x" if line in done else " "
            count += line in done
            print(f"  [{mark}] {i}  {line[:70]}{'...' if len(line) > 70 else ''}")
    print(f"\n{count} of {total} lines recorded.")


def forget(video_dir: Path, scene_id: str, index: int | None) -> list[str]:
    """Drop the takes for one line (or a whole scene) so they get recorded again."""
    narration = load_narration(video_dir / "narration.md")
    if scene_id not in narration:
        sys.exit(f"No `## {scene_id}` in narration.md. Scenes: {', '.join(narration)}")
    lines = narration[scene_id]
    if index is not None and not 0 <= index < len(lines):
        sys.exit(f"`## {scene_id}` has lines 0 to {len(lines) - 1}")
    targets = set(lines if index is None else [lines[index]])

    keep, dropped = [], []
    for take in load_takes(video_dir):
        if take.get("input_data", {}).get("input_text") in targets:
            dropped.append(take)
        else:
            keep.append(take)
    for take in dropped:
        for key in ("original_audio", "final_audio"):
            audio = recorder_dir(video_dir) / take.get(key, "")
            for f in (audio, audio.with_suffix(".wav")):
                if f.is_file():
                    f.unlink()
    if dropped:
        (recorder_dir(video_dir) / CACHE_FILE).write_text(json.dumps(keep, indent=2))
    return [t["input_data"]["input_text"] for t in dropped]


def list_devices() -> None:
    import pyaudio

    audio = pyaudio.PyAudio()
    try:
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            if info.get("maxInputChannels", 0) > 0:
                print(f"  {i}: {info['name']}")
    finally:
        audio.terminate()
    print('\nPut the number in config.toml as recorder_device = <number>.')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("video", nargs="?", help="video number, e.g. 01")
    parser.add_argument("--redo", nargs="+", metavar=("SCENE", "LINE"), help="forget a scene's takes, or one line")
    parser.add_argument("--devices", action="store_true", help="list microphones and exit")
    args = parser.parse_args()

    if args.devices:
        return list_devices()
    if not args.video:
        parser.error("give a video number, or --devices")
    video_dir = find_video_dir(args.video)
    if args.redo:
        if len(args.redo) > 2:
            parser.error("--redo takes a scene id and an optional line number")
        index = int(args.redo[1]) if len(args.redo) == 2 else None
        dropped = forget(video_dir, args.redo[0], index)
        if not dropped:
            print("Nothing recorded for that yet, so there's nothing to redo.")
        for text in dropped:
            print(f"Will re-record: {text}")
        return
    list_takes(video_dir)


if __name__ == "__main__":
    main()
