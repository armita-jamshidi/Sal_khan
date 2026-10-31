"""Base scene every video builds on: channel background, voice and narration."""

from __future__ import annotations

import inspect
from pathlib import Path

from manim import config as manim_config
from manim_voiceover import VoiceoverScene

from . import style
from .config import load_config
from .narration import load_narration


def make_speech_service(voice: str, cache_dir: Path):
    """The single switch between the robot placeholder voice and your mic."""
    settings = load_config()
    if voice == "placeholder":
        from manim_voiceover.services.gtts import GTTSService

        return GTTSService(lang=settings["gtts_lang"], tld=settings["gtts_tld"], cache_dir=str(cache_dir))
    if voice == "recorder":
        from manim_voiceover.services.recorder import RecorderService

        return RecorderService(cache_dir=str(cache_dir))
    raise ValueError(f"unknown voice mode {voice!r}")


class ChannelScene(VoiceoverScene):
    """Subclass this in videos/NN-slug/scenes.py.

    Set `scene_id` to the matching `## heading` in that video's narration.md,
    then use `self.say(i)` to get line i as a voiceover context.
    """

    scene_id: str = ""

    def setup(self):
        super().setup()
        manim_config.background_color = style.BACKGROUND
        self.camera.background_color = style.BACKGROUND
        video_dir = Path(inspect.getfile(type(self))).resolve().parent
        voice = load_config()["voice"]
        self.set_speech_service(make_speech_service(voice, video_dir / "voiceovers" / voice))
        narration_file = video_dir / "narration.md"
        self.lines = load_narration(narration_file).get(self.scene_id, []) if narration_file.exists() else []

    def say(self, index: int):
        """`with self.say(0) as tracker:` speaks line 0 of this scene's narration."""
        return self.voiceover(text=self.lines[index])
