"""Channel look: colors, fonts, sizes and layout constants.

Every scene imports from here so all videos look like the same channel.
"""

from manim import ManimColor

# Palette: Atomic Tangerine FF6B35, Peach Glow F7C59F, Beige EFEFD0,
# Steel Azure 004E89, Baltic Blue 1A659E. Background and gray are darkened
# tints of the same family, and blocking red is the one off-palette color.
BACKGROUND = ManimColor("#061A2E")  # deep Steel Azure
TEXT = ManimColor("#EFEFD0")        # Beige
TEXT_MUTED = ManimColor("#9AA3A0")
PANEL = ManimColor("#004E89")       # Steel Azure

# One accent color per algorithm state
PROPOSING = ManimColor("#3A8DDE")  # Baltic Blue, lifted so it reads on the dark background
HELD = ManimColor("#F7C59F")       # Peach Glow: tentatively held
REJECTED = ManimColor("#4A5560")   # gray: rejected / bumped
FINAL = ManimColor("#FF6B35")      # Atomic Tangerine: final match
BLOCKING = ManimColor("#E63946")   # red: blocking pair / instability

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
