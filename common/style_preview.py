"""A short reel of the shared style. Render with `make style`."""

from manim import (
    DOWN, LEFT, RIGHT, UP,
    Arrow, Create, FadeIn, FadeOut, GrowArrow, LaggedStart, RoundedRectangle, Scene, Text, VGroup,
)

from common import style
from common.icons import HospitalIcon, StudentIcon
from common.templates import play_intro, play_outro


class StylePreview(Scene):
    def construct(self):
        self.camera.background_color = style.BACKGROUND
        play_intro(self, "How the Residency Match Actually Works", "Channel style preview", hold=1)

        swatches = VGroup()
        for name, color in [("Proposing", style.PROPOSING), ("Held", style.HELD),
                            ("Rejected", style.REJECTED), ("Final", style.FINAL),
                            ("Blocking pair", style.BLOCKING)]:
            chip = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.15,
                                    color=color, fill_opacity=1, stroke_width=0)
            label = Text(name, font=style.FONT, font_size=style.LABEL_SIZE, color=style.TEXT)
            label.next_to(chip, DOWN, buff=0.2)
            swatches.add(VGroup(chip, label))
        swatches.arrange(RIGHT, buff=0.35)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.3) for s in swatches], lag_ratio=0.15))
        self.wait(1.5)
        self.play(FadeOut(swatches))

        students = VGroup(*[StudentIcon(n) for n in ["Ana", "Ben", "Cy", "Dee"]]).arrange(DOWN, buff=0.35)
        students.move_to([style.LEFT_COLUMN_X, 0, 0])
        hospitals = VGroup(HospitalIcon("City", 2), HospitalIcon("Mercy", 1), HospitalIcon("Lake", 1))
        hospitals.arrange(DOWN, buff=0.45).move_to([style.RIGHT_COLUMN_X, 0, 0])
        self.play(FadeIn(students, shift=RIGHT * 0.3), FadeIn(hospitals, shift=LEFT * 0.3))

        ana, city = students[0], hospitals[0]
        arrow = Arrow(ana.figure.get_right(), city.figure.get_left(), color=style.PROPOSING, stroke_width=style.STROKE)
        ana.set_state("proposing")
        self.play(GrowArrow(arrow))
        self.play(ana.animate.set_state("held"), arrow.animate.set_color(style.HELD), city.slots.animate.set_filled(1))
        self.wait(0.5)
        self.play(ana.animate.set_state("final"), arrow.animate.set_color(style.FINAL),
                  city.slots.animate.set_filled(1, style.FINAL))
        self.wait(1)
        self.play(FadeOut(VGroup(students, hospitals, arrow)))

        play_outro(self, ["Applicants on the left, programs on the right",
                          "One color per state", "Slot counters show capacity"])
