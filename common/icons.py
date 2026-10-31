"""Generic student and hospital icons drawn with Manim shapes (no logos)."""

from __future__ import annotations

from manim import (
    DOWN, LEFT, RIGHT, UP,
    Circle, Polygon, Rectangle, RoundedRectangle, Square, Text, VGroup,
)

from . import style


class StudentIcon(VGroup):
    """A person with a graduation cap, plus a name label underneath."""

    def __init__(self, name: str, color=style.TEXT, size: float = 0.9, **kwargs):
        super().__init__(**kwargs)
        head = Circle(radius=0.18 * size, color=color, fill_opacity=1, stroke_width=0)
        body = RoundedRectangle(
            width=0.55 * size, height=0.4 * size, corner_radius=0.18 * size,
            color=color, fill_opacity=1, stroke_width=0,
        ).next_to(head, DOWN, buff=0.04 * size)
        cap_top = Polygon(
            [-0.3, 0, 0], [0, 0.1, 0], [0.3, 0, 0], [0, -0.1, 0],
            color=color, fill_opacity=1, stroke_width=0,
        ).scale(size).next_to(head, UP, buff=-0.06 * size)
        self.figure = VGroup(head, body, cap_top)
        self.label = Text(name, font=style.FONT, font_size=style.LABEL_SIZE, color=style.TEXT)
        self.label.next_to(self.figure, DOWN, buff=0.12)
        self.add(self.figure, self.label)

    def set_state(self, state: str):
        """Recolor the figure for an algorithm state (see style.STATE_COLORS)."""
        self.figure.set_color(style.STATE_COLORS[state])
        return self


class SlotCounter(VGroup):
    """A row of boxes, one per program slot, filled as slots are held."""

    def __init__(self, capacity: int, box: float = 0.3, **kwargs):
        super().__init__(**kwargs)
        self.boxes = VGroup(*[
            Square(side_length=box, color=style.TEXT_MUTED, stroke_width=2)
            for _ in range(capacity)
        ]).arrange(RIGHT, buff=0.08)
        self.add(self.boxes)

    def set_filled(self, n: int, color=style.HELD):
        for i, b in enumerate(self.boxes):
            b.set_fill(color, opacity=1 if i < n else 0)
        return self


class HospitalIcon(VGroup):
    """A small building with a cross, a name label and a slot counter."""

    def __init__(self, name: str, capacity: int = 1, color=style.TEXT, size: float = 0.9, **kwargs):
        super().__init__(**kwargs)
        building = Rectangle(width=0.9 * size, height=0.7 * size, color=color, stroke_width=style.STROKE)
        roof = Polygon(
            [-0.5, 0, 0], [0, 0.25, 0], [0.5, 0, 0],
            color=color, stroke_width=style.STROKE,
        ).scale(size).next_to(building, UP, buff=0)
        bar_v = Rectangle(width=0.1 * size, height=0.34 * size, color=color, fill_opacity=1, stroke_width=0)
        bar_h = Rectangle(width=0.34 * size, height=0.1 * size, color=color, fill_opacity=1, stroke_width=0)
        cross = VGroup(bar_v, bar_h).move_to(building)
        self.figure = VGroup(building, roof, cross)
        self.label = Text(name, font=style.FONT, font_size=style.LABEL_SIZE, color=style.TEXT)
        self.label.next_to(self.figure, DOWN, buff=0.12)
        self.slots = SlotCounter(capacity).next_to(self.label, DOWN, buff=0.1)
        self.add(self.figure, self.label, self.slots)

    def set_state(self, state: str):
        self.figure.set_color(style.STATE_COLORS[state])
        return self
