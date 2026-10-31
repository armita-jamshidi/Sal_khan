"""The example market the video tells its story with.

4 applicants, 3 programs, and City has 2 seats. The rankings are chosen so the
two proposing sides end differently: with applicants proposing, everyone gets
a different program than with programs proposing. Change the data here and
the animation follows, since scenes.py replays match() on this market.

Applicant-proposing (3 rounds):
  round 1  Mercy holds Ana and rejects Ben
  round 2  Ben goes to Lake and bumps Dee
  round 3  Dee lands at City
  final    Ana-Mercy, Ben-Lake, Cy and Dee at City

Program-proposing (2 rounds):
  final    Ana and Ben at City, Cy-Lake, Dee-Mercy
"""

from __future__ import annotations

from algorithm import Market

APPLICANTS = ["Ana", "Ben", "Cy", "Dee"]
PROGRAMS = ["City", "Mercy", "Lake"]

EXAMPLE = Market(
    applicant_prefs={
        "Ana": ["Mercy", "City", "Lake"],
        "Ben": ["Mercy", "Lake", "City"],
        "Cy": ["City", "Mercy", "Lake"],
        "Dee": ["Lake", "City", "Mercy"],
    },
    program_prefs={
        "City": ["Ana", "Ben", "Cy", "Dee"],
        "Mercy": ["Dee", "Ana", "Ben", "Cy"],
        "Lake": ["Ana", "Cy", "Ben", "Dee"],
    },
    capacities={"City": 2},
)

# Scene 3: "everyone takes their first choice, and a coin flip settles ties."
# Ana and Ben both want Mercy, Ben wins the flip, and Ana falls to City.
# Ana and Mercy would both rather be together, so this is the one blocking pair.
NAIVE_MATCHING = {"Ana": "City", "Ben": "Mercy", "Cy": "City", "Dee": "Lake"}
NAIVE_BLOCKING_PAIR = ("Ana", "Mercy")
