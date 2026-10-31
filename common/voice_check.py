"""A 15-second scene to check the voice setup. Render with `make voice-check`.

With voice = "recorder" it is a safe place to test your mic before recording
a real video: two short lines, and nothing else gets overwritten.
"""

from manim import DOWN, UP, FadeIn, FadeOut, Text, Write

from common import style
from common.scene import ChannelScene


class VoiceCheck(ChannelScene):
    def construct(self):
        self.lines = [
            "This is a voice check. If you can hear me, the narration is wired up.",
            "Each line of the script becomes one take, and the animation waits for it.",
        ]
        title = Text("Voice check", font=style.FONT, font_size=style.TITLE_SIZE, color=style.TEXT)
        with self.say(0) as tracker:
            self.play(Write(title), run_time=tracker.duration * 0.5)
        sub = Text("one line = one take", font=style.FONT, font_size=style.LABEL_SIZE, color=style.PROPOSING)
        sub.next_to(title, DOWN, buff=0.5)
        with self.say(1) as tracker:
            self.play(FadeIn(sub, shift=UP * 0.2), run_time=tracker.duration * 0.4)
        self.play(FadeOut(title), FadeOut(sub))
