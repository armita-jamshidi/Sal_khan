"""Render every scene of one video and stitch them into a single mp4.

    python -m pipeline.render 01 --quality low     # preview
    python -m pipeline.render 01 --quality final   # 1080p60

Scene order comes from the SCENES list in videos/NN-slug/scenes.py.
"""

from __future__ import annotations

import argparse
import ast
import os
import subprocess
import sys
from pathlib import Path

from common.config import REPO_ROOT

QUALITY_FLAGS = {
    "low": ["-ql"],                    # 480p15, fast
    "final": ["-qh", "--fps", "60"],   # 1080p60
}


def find_video_dir(number: str) -> Path:
    matches = sorted((REPO_ROOT / "videos").glob(f"{int(number):02d}-*"))
    if not matches:
        sys.exit(f"No folder videos/{int(number):02d}-*")
    return matches[0]


def scene_order(scenes_file: Path) -> list[str]:
    """Read SCENES = [...] without importing manim."""
    tree = ast.parse(scenes_file.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "SCENES" for t in node.targets):
            return [elt.id if isinstance(elt, ast.Name) else elt.value for elt in node.value.elts]
    sys.exit(f"{scenes_file} has no SCENES list")


def render(video_dir: Path, quality: str) -> Path:
    scenes_file = video_dir / "scenes.py"
    if not scenes_file.exists():
        sys.exit(f"{scenes_file} does not exist yet")
    out_dir = REPO_ROOT / "build" / video_dir.name / quality
    media_dir = out_dir / "media"
    env = {**os.environ, "PYTHONPATH": str(REPO_ROOT)}

    clips = []
    for name in scene_order(scenes_file):
        subprocess.run(
            [sys.executable, "-m", "manim", *QUALITY_FLAGS[quality],
             "--media_dir", str(media_dir), str(scenes_file), name],
            check=True, env=env, cwd=REPO_ROOT,
        )
        found = sorted((media_dir / "videos").rglob(f"{name}.mp4"), key=lambda p: p.stat().st_mtime)
        clips.append(found[-1])

    concat_list = out_dir / "clips.txt"
    concat_list.write_text("".join(f"file '{c}'\n" for c in clips))
    output = out_dir / f"{video_dir.name}-{quality}.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-c", "copy", str(output)],
        check=True,
    )
    print(f"Wrote {output}")
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("video", help="video number, e.g. 01")
    parser.add_argument("--quality", choices=QUALITY_FLAGS, default="low")
    args = parser.parse_args()
    render(find_video_dir(args.video), args.quality)


if __name__ == "__main__":
    main()
