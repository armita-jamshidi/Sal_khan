"""Channel look: colors, fonts, sizes and layout constants.

Every scene imports from here so all videos look like the same channel.
"""

from manim import ManimColor

# Background and text
BACKGROUND = ManimColor("#0F1420")
TEXT = ManimColor("#E8ECF4")
TEXT_MUTED = ManimColor("#8A93A6")
PANEL = ManimColor("#1B2232")

# One accent color per algorithm state
PROPOSING = ManimColor("#4C9AFF")  # blue: a proposal in flight
HELD = ManimColor("#FFC940")       # yellow: tentatively held
REJECTED = ManimColor("#5C6373")   # gray: rejected / bumped
FINAL = ManimColor("#3DDC84")      # green: final match
BLOCKING = ManimColor("#FF5C5C")   # red: blocking pair / instability

STATE_COLORS = {
    "proposing": PROPOSING,
    "held": HELD,
    "rejected": REJECTED,
    "final": FINAL,
    "blocking": BLOCKING,
}

# Typography (Inter is free: https://rsms.me/inter/, falls back to the system sans)
FONT = "Inter"
MONO_FONT = "JetBrains Mono"
TITLE_SIZE = 56
HEADING_SIZE = 40
BODY_SIZE = 30
LABEL_SIZE = 24
SMALL_SIZE = 18

# Layout: applicants on the left, programs on the right
LEFT_COLUMN_X = -4.5
RIGHT_COLUMN_X = 4.5
ROW_SPACING = 1.4
STROKE = 4
