"""Manim scenes for video 1: How the Residency Match System Actually Works.

Everything on screen comes from algorithm.py's event log for the example in
example.py, so changing the example data changes the animation.

    make preview VIDEO=01                                # all scenes, stitched
    manim -ql videos/01-residency-match/scenes.py AlgorithmScene   # one scene

Narration comes from narration.md (one `## scene_id` block per scene). Until a
line exists there, the scene speaks a placeholder built from the event log, so
the timing is still realistic.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UL, UP,
    AnimationGroup, Arrow, Cross, FadeIn, FadeOut, GrowArrow, Line, MovingCameraScene,
    Polygon, RoundedRectangle, Text, Transform, VGroup, Write,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))

from algorithm import Event, Market, MatchResult, match  # noqa: E402
from example import EXAMPLE  # noqa: E402

from common import style  # noqa: E402
from common.icons import HospitalIcon, StudentIcon  # noqa: E402
from common.scene import ChannelScene  # noqa: E402

SCENES = ["AlgorithmScene"]

RANK_SIZE = 20
APPLICANT_X = -3.3
PROGRAM_X = 3.3


def label(text: str, size: int = style.LABEL_SIZE, color=style.TEXT, **kwargs) -> Text:
    return Text(text, font=style.FONT, font_size=size, color=color, **kwargs)


def rank_list(names: list[str]) -> VGroup:
    """A numbered wish list, best first. Entry i is `group[i]`; its name is `group[i][1]`."""
    rows = VGroup(*[
        VGroup(label(f"{i + 1}.", RANK_SIZE, style.TEXT_MUTED), label(n, RANK_SIZE)).arrange(RIGHT, buff=0.12)
        for i, n in enumerate(names)
    ])
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)


def fast_forward_badge() -> VGroup:
    tri = Polygon([0, 0.15, 0], [0.22, 0, 0], [0, -0.15, 0], color=style.TEXT, fill_opacity=1, stroke_width=0)
    icon = VGroup(tri, tri.copy().shift(RIGHT * 0.2))
    return VGroup(icon, label("2x", style.SMALL_SIZE)).arrange(RIGHT, buff=0.15)


def legend() -> VGroup:
    items = VGroup()
    for name, color in [("asking", style.PROPOSING), ("maybe", style.HELD),
                        ("no", style.REJECTED), ("final", style.FINAL)]:
        chip = RoundedRectangle(width=0.32, height=0.2, corner_radius=0.06,
                                color=color, fill_opacity=1, stroke_width=0)
        items.add(VGroup(chip, label(name, style.SMALL_SIZE, style.TEXT_MUTED)).arrange(RIGHT, buff=0.12))
    return items.arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.3)


class Board(VGroup):
    """Applicants on the left, programs on the right, wish lists on the outside.

    Each `*_steps` method turns one event into a list of steps to play in
    order. A step is a function that returns animations, so it is built only
    when it plays, from the board as it looks at that moment. Bookkeeping
    (who holds which seat) updates right away.
    """

    def __init__(self, market: Market, **kwargs):
        super().__init__(**kwargs)
        self.market = market
        self.applicants = {a: StudentIcon(a, size=0.8) for a in market.applicant_prefs}
        self.programs = {p: HospitalIcon(p, market.capacity(p), size=0.8) for p in market.program_prefs}

        self._column(self.applicants.values(), APPLICANT_X)
        self._column(self.programs.values(), PROGRAM_X)

        self.applicant_ranks = {a: rank_list(prefs) for a, prefs in market.applicant_prefs.items()}
        self.program_ranks = {p: rank_list(prefs) for p, prefs in market.program_prefs.items()}
        for a, ranks in self.applicant_ranks.items():
            ranks.next_to(self.applicants[a], LEFT, buff=0.55)
        for p, ranks in self.program_ranks.items():
            ranks.next_to(self.programs[p], RIGHT, buff=0.55)

        self.add(*self.applicants.values(), *self.programs.values(),
                 *self.applicant_ranks.values(), *self.program_ranks.values())

        self.arrows: dict[tuple[str, str], Arrow] = {}
        self.seats: dict[str, list[str | None]] = {p: [None] * market.capacity(p) for p in market.program_prefs}

    @staticmethod
    def _column(icons, x: float):
        group = VGroup(*icons).arrange(DOWN, buff=0.35)
        group.move_to([x, -0.2, 0])

    # Lookups

    def applicant_entry(self, a: str, p: str) -> Text:
        return self.applicant_ranks[a][self.market.applicant_prefs[a].index(p)][1]

    def program_entry(self, p: str, a: str) -> Text | None:
        prefs = self.market.program_prefs[p]
        return self.program_ranks[p][prefs.index(a)][1] if a in prefs else None

    def arrow(self, a: str, p: str, seat: int, color) -> Arrow:
        cap = len(self.seats[p])
        offset = (seat - (cap - 1) / 2) * 0.28
        start = self.applicants[a].figure.get_right()
        end = self.programs[p].figure.get_left() + UP * offset
        return Arrow(start, end, buff=0.15, color=color, stroke_width=style.STROKE,
                     max_tip_length_to_length_ratio=0.05, max_stroke_width_to_length_ratio=10)

    def filled(self, p: str) -> int:
        return sum(s is not None for s in self.seats[p])

    # Event steps

    def _strike(self, entry: Text) -> Line:
        return Line(entry.get_left(), entry.get_right(), color=style.REJECTED, stroke_width=3)

    def propose_steps(self, a: str, p: str):
        seat = self.seats[p].index(None) if None in self.seats[p] else 0

        def grow():
            self.arrows[(a, p)] = self.arrow(a, p, seat, style.PROPOSING)
            return [self.applicants[a].figure.animate.set_color(style.PROPOSING),
                    self.applicant_entry(a, p).animate.set_color(style.PROPOSING),
                    GrowArrow(self.arrows[(a, p)])]
        return [grow]

    def hold_steps(self, a: str, p: str):
        seat = self.seats[p].index(None)
        self.seats[p][seat] = a
        filled = self.filled(p)

        def hold():
            anims = [Transform(self.arrows[(a, p)], self.arrow(a, p, seat, style.HELD)),
                     self.applicants[a].figure.animate.set_color(style.HELD),
                     self.applicant_entry(a, p).animate.set_color(style.HELD),
                     self.programs[p].slots.animate.set_filled(filled)]
            entry = self.program_entry(p, a)
            if entry is not None:
                anims.append(entry.animate.set_color(style.HELD))
            return anims
        return [hold]

    def reject_steps(self, a: str, p: str):
        cross = Cross(scale_factor=0.18, stroke_color=style.TEXT_MUTED, stroke_width=6)

        def refuse():
            arrow = self.arrows[(a, p)]
            cross.move_to(arrow.get_center())
            return [arrow.animate.set_color(style.REJECTED), FadeIn(cross, scale=1.5),
                    self.applicants[a].figure.animate.set_color(style.REJECTED)]

        def cross_off():
            entry = self.applicant_entry(a, p)
            return [FadeOut(self.arrows.pop((a, p))), FadeOut(cross),
                    entry.animate.set_color(style.REJECTED), Write(self._strike(entry)),
                    self.applicants[a].figure.animate.set_color(style.TEXT)]
        return [refuse, cross_off]

    def bump_steps(self, a: str, p: str):
        """`a` loses the seat it held at `p`: gray, step back, then wait to ask again."""
        self.seats[p][self.seats[p].index(a)] = None
        filled = self.filled(p)
        figure = self.applicants[a].figure

        def drop():
            anims = [self.arrows[(a, p)].animate.set_color(style.REJECTED),
                     figure.animate.set_color(style.REJECTED).shift(LEFT * 0.35),
                     self.programs[p].slots.animate.set_filled(filled)]
            entry = self.program_entry(p, a)
            if entry is not None:
                anims.append(entry.animate.set_color(style.TEXT))
            return anims

        def step_back():
            entry = self.applicant_entry(a, p)
            return [FadeOut(self.arrows.pop((a, p))), entry.animate.set_color(style.REJECTED),
                    Write(self._strike(entry)), figure.animate.set_color(style.TEXT).shift(RIGHT * 0.35)]
        return [drop, step_back]

    def final_steps(self, finals: list[Event]):
        def finish():
            anims = []
            for e in finals:
                if e.kind == "final":
                    anims += [self.arrows[(e.applicant, e.program)].animate.set_color(style.FINAL),
                              self.applicants[e.applicant].figure.animate.set_color(style.FINAL),
                              self.applicant_entry(e.applicant, e.program).animate.set_color(style.FINAL)]
                    entry = self.program_entry(e.program, e.applicant)
                    if entry is not None:
                        anims.append(entry.animate.set_color(style.FINAL))
                else:
                    anims.append(self.applicants[e.applicant].figure.animate.set_color(style.REJECTED))
            for p, icon in self.programs.items():
                anims += [icon.slots.animate.set_filled(self.filled(p), style.FINAL),
                          icon.figure.animate.set_color(style.FINAL if self.filled(p) else style.REJECTED)]
            return anims
        return [finish]

    def steps(self, event: Event):
        kind, a, p = event.kind, event.applicant, event.program
        return {"propose": self.propose_steps, "hold": self.hold_steps,
                "reject": self.reject_steps, "bump": self.bump_steps}[kind](a, p)


def describe_round(events: list[Event]) -> str:
    """Placeholder narration for one round of applicant proposals, from the log."""
    sentences = []
    bumped = None
    for e in events:
        if e.kind == "propose":
            sentences.append(f"{e.applicant} asks {e.program}.")
        elif e.kind == "bump":
            bumped = e.applicant
        elif e.kind == "hold":
            if bumped:
                sentences.append(f"{e.program} likes {e.applicant} better, so {bumped} gets bumped.")
                bumped = None
            else:
                sentences.append(f"{e.program} says maybe.")
        elif e.kind == "reject":
            sentences.append(f"{e.program} prefers who it has, so {e.applicant} gets a no.")
    return " ".join(sentences)


class Video1Scene(ChannelScene):
    """Adds placeholder narration: `self.narrate(i, fallback)` speaks line i of
    narration.md if it exists, otherwise the fallback text."""

    def narrate(self, index: int, fallback: str):
        text = self.lines[index] if index < len(self.lines) else fallback
        return self.voiceover(text=text)

    def play_steps(self, steps, total: float, min_step: float = 0.35, max_step: float = 1.2):
        """Play board steps back to back, sharing `total` seconds between them."""
        if not steps:
            return
        run_time = float(np.clip(total / len(steps), min_step, max_step))
        for step in steps:
            self.play(AnimationGroup(*step()), run_time=run_time)


class AlgorithmScene(Video1Scene, MovingCameraScene):
    """Section 4: deferred acceptance, replayed from the event log.

    Pacing: rounds up to and including the first bump play at full speed (the
    first bump gets a zoom), later rounds are fast-forwarded, then everything
    turns final at once.
    """

    scene_id = "algorithm"

    def construct(self):
        result: MatchResult = match(EXAMPLE, proposing="applicants")
        by_round: dict[int, list[Event]] = defaultdict(list)
        for e in result.events:
            if e.kind not in ("final", "unmatched"):
                by_round[e.round].append(e)
        finals = [e for e in result.events if e.kind in ("final", "unmatched")]
        first_bump = next((e.round for e in result.events if e.kind == "bump"), None)
        slow_rounds = {r for r in by_round if r == 1 or (first_bump and r <= first_bump)}

        board = Board(EXAMPLE)
        line = 0

        # Rules in one sentence, then shrink them into a corner reminder.
        rules = VGroup(
            label("Applicants ask their favorite program.", style.BODY_SIZE),
            label("Programs say maybe to the best so far, and no to the rest.", style.BODY_SIZE),
            label("Repeat until nobody is left to ask.", style.BODY_SIZE, style.TEXT_MUTED),
        ).arrange(DOWN, buff=0.3)
        with self.narrate(line, "Here's the whole algorithm in one sentence. Every applicant asks their "
                                "favorite program. Each program says maybe to the best applicants so far, "
                                "up to its number of seats, and says no to the rest.") as tracker:
            self.play(FadeIn(rules, shift=UP * 0.2), run_time=1)
            self.wait(max(tracker.duration - 2.5, 0.5))
            reminder = VGroup(*[label(t, style.SMALL_SIZE, style.TEXT_MUTED) for t in
                                ("Ask your favorite", "Maybe to the best so far", "Repeat")])
            reminder.arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.3)
            self.play(Transform(rules, reminder), FadeIn(board), FadeIn(legend()), run_time=1.2)
        line += 1

        round_label = label("Round 1", style.HEADING_SIZE, weight="BOLD").to_edge(UP, buff=0.3)
        badge = fast_forward_badge().next_to(round_label, RIGHT, buff=0.4)
        shown_label = False

        for r in sorted(by_round):
            events = by_round[r]
            new_label = label(f"Round {r}", style.HEADING_SIZE, weight="BOLD").to_edge(UP, buff=0.3)
            fast = r not in slow_rounds

            if r == first_bump and r != 1:
                # Pattern break: zoom on the program about to bump someone.
                bump = next(e for e in events if e.kind == "bump")
                proposer = next(e.applicant for e in events
                                if e.kind == "propose" and e.program == bump.program)
                focus = VGroup(board.applicants[proposer], board.applicants[bump.applicant],
                               board.programs[bump.program])
                with self.narrate(line, f"Round {r}. Now watch what happens when someone better shows up. "
                                        + describe_round(events)) as tracker:
                    self.play(Transform(round_label, new_label), run_time=0.5)
                    center = [1.0, focus.get_center()[1], 0]
                    self.play(self.camera.frame.animate.set(width=10.5).move_to(center), run_time=1.2)
                    steps = [s for e in events for s in board.steps(e)]
                    self.play_steps(steps, tracker.duration - 3.2, max_step=1.5)
                    self.play(self.camera.frame.animate.set(width=14.222).move_to([0, 0, 0]), run_time=1)
                line += 1
                continue

            fallback = (f"Round {r}. " if r > 1 else "Round one. Everyone asks their top choice. ") \
                + describe_round(events)
            if fast:
                fallback = f"Round {r}, fast forward. " + describe_round(events)
            with self.narrate(line, fallback) as tracker:
                if not shown_label:
                    round_label = new_label
                    self.play(FadeIn(round_label), run_time=0.5)
                    shown_label = True
                else:
                    self.play(Transform(round_label, new_label), run_time=0.5)
                if fast:
                    self.play(FadeIn(badge), run_time=0.3)
                steps = [s for e in events for s in board.steps(e)]
                if fast:
                    self.play_steps(steps, tracker.duration - 1, min_step=0.25, max_step=0.5)
                    self.play(FadeOut(badge), run_time=0.3)
                else:
                    self.play_steps(steps, tracker.duration - 0.5)
            line += 1

        with self.narrate(line, "Nobody is left to ask, so every maybe becomes final.") as tracker:
            self.play(FadeOut(round_label), run_time=0.4)
            self.play_steps(board.final_steps(finals), 1.5, max_step=1.5)
        self.wait(1.5)
