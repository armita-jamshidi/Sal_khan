"""Intro and outro templates shared by every video."""

from __future__ import annotations

from manim import (
    DOWN, UP, FadeIn, FadeOut, LaggedStart, Line, Scene, Text, VGroup, Write,
)

from . import style


def title_card(title: str, subtitle: str = "") -> VGroup:
    heading = Text(title, font=style.FONT, font_size=style.TITLE_SIZE, color=style.TEXT, weight="BOLD")
    if heading.width > 12:
        heading.scale_to_fit_width(12)
    rule = Line(heading.get_left(), heading.get_right(), color=style.PROPOSING, stroke_width=style.STROKE)
    rule.next_to(heading, DOWN, buff=0.25)
    group = VGroup(heading, rule)
    if subtitle:
        sub = Text(subtitle, font=style.FONT, font_size=style.BODY_SIZE, color=style.TEXT_MUTED)
        sub.next_to(rule, DOWN, buff=0.3)
        group.add(sub)
    return group.move_to([0, 0, 0])


def play_intro(scene: Scene, title: str, subtitle: str = "", hold: float = 1.5):
    card = title_card(title, subtitle)
    scene.play(Write(card[0]), run_time=1.2)
    scene.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in card[1:]], lag_ratio=0.3))
    scene.wait(hold)
    scene.play(FadeOut(card))


def recap_card(points: list[str]) -> VGroup:
    heading = Text("Recap", font=style.FONT, font_size=style.HEADING_SIZE, color=style.FINAL, weight="BOLD")
    bullets = VGroup(*[
        Text(f"•  {p}", font=style.FONT, font_size=style.BODY_SIZE, color=style.TEXT) for p in points
    ]).arrange(DOWN, aligned_edge=[-1, 0, 0], buff=0.3)
    return VGroup(heading, bullets).arrange(DOWN, buff=0.5)


def play_outro(scene: Scene, points: list[str], call_to_action: str = "Subscribe for the next algorithm"):
    recap = recap_card(points)
    scene.play(FadeIn(recap[0], shift=DOWN * 0.2))
    scene.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in recap[1]], lag_ratio=0.4))
    scene.wait(1)
    cta = Text(call_to_action, font=style.FONT, font_size=style.BODY_SIZE, color=style.PROPOSING)
    scene.play(FadeOut(recap), FadeIn(cta))
    scene.wait(1.5)
    scene.play(FadeOut(cta))
