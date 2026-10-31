"""Load a video's narration.md so wording can change without touching code.

Format: one `## scene_id` heading per scene. Each paragraph under it is one
voiceover line (one take when recording). HTML comments are ignored, and
`TODO-VERIFY` notes in square brackets are stripped from the spoken text:

    ## hook
    Every March, thousands of med students open an envelope at the same moment.

    How does one computer decide all of this fairly? [TODO-VERIFY: date]
"""

from __future__ import annotations

import re
from pathlib import Path

_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_TODO = re.compile(r"\[TODO-VERIFY[^\]]*\]")
_HEADING = re.compile(r"^##\s+(\S+)\s*$", re.MULTILINE)


def load_narration(path: str | Path) -> dict[str, list[str]]:
    """Return {scene_id: [line, line, ...]} in file order."""
    text = _COMMENT.sub("", Path(path).read_text(encoding="utf-8"))
    parts = _HEADING.split(text)
    scenes: dict[str, list[str]] = {}
    # parts = [preamble, id1, body1, id2, body2, ...]
    for scene_id, body in zip(parts[1::2], parts[2::2]):
        if scene_id in scenes:
            raise ValueError(f"duplicate scene id {scene_id!r} in {path}")
        lines = []
        for para in re.split(r"\n\s*\n", body):
            spoken = " ".join(_TODO.sub("", para).split())
            if spoken:
                lines.append(spoken)
        scenes[scene_id] = lines
    return scenes


def todo_verify_notes(path: str | Path) -> list[str]:
    """List every TODO-VERIFY note, so nothing unchecked slips into a final render."""
    return _TODO.findall(Path(path).read_text(encoding="utf-8"))
