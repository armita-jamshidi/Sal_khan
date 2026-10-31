"""Deferred acceptance (Gale-Shapley) with program capacities.

Either side can propose. `match()` returns the final matching plus an event
log of every step, and `scenes.py` replays that log, so changing the example
data changes the animation.

The algorithm runs in rounds. At the start of a round, every proposer with an
open slot and someone left on its list proposes to its next choice (a program
with k open seats makes k proposals). Each proposal is decided on the spot:
the receiver holds its best proposers so far, up to its capacity, and bumps or
rejects the rest. Anyone bumped proposes again in the next round. It ends when
a round has no proposals.

Rankings are acceptability lists: an applicant who doesn't rank a program (or
a program that doesn't rank an applicant) will never be matched to it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Side = Literal["applicants", "programs"]
EventKind = Literal["propose", "hold", "reject", "bump", "final", "unmatched"]


@dataclass(frozen=True)
class Market:
    """Both sides' rankings, best first, plus each program's number of seats."""

    applicant_prefs: dict[str, list[str]]
    program_prefs: dict[str, list[str]]
    capacities: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for a, prefs in self.applicant_prefs.items():
            _check_ranking(a, prefs, self.program_prefs)
        for p, prefs in self.program_prefs.items():
            _check_ranking(p, prefs, self.applicant_prefs)
        for p, seats in self.capacities.items():
            if p not in self.program_prefs:
                raise ValueError(f"capacity given for unknown program {p!r}")
            if seats < 1:
                raise ValueError(f"program {p!r} needs at least 1 seat, got {seats}")

    def capacity(self, program: str) -> int:
        return self.capacities.get(program, 1)

    def acceptable(self, applicant: str, program: str) -> bool:
        """True if each ranks the other."""
        return (program in self.applicant_prefs[applicant]
                and applicant in self.program_prefs[program])


def _check_ranking(owner: str, prefs: list[str], other_side: dict) -> None:
    if len(set(prefs)) != len(prefs):
        raise ValueError(f"{owner!r} ranks someone twice: {prefs}")
    unknown = [x for x in prefs if x not in other_side]
    if unknown:
        raise ValueError(f"{owner!r} ranks unknown names: {unknown}")


@dataclass(frozen=True)
class Event:
    """One step of the algorithm, always named by its applicant and program.

    kind:
      propose    the proposing side asks
      hold       the receiver says "maybe" and holds the pair
      reject     the receiver turns the new proposal down
      bump       the receiver drops a pair it was holding, to make room
      final      the pair is matched when the algorithm ends
      unmatched  the applicant ends with no program (program is None)
    """

    step: int
    round: int
    kind: EventKind
    applicant: str
    program: str | None


@dataclass
class MatchResult:
    proposing: Side
    assignment: dict[str, str | None]  # applicant -> program, or None
    events: list[Event]

    @property
    def program_matches(self) -> dict[str, list[str]]:
        """program -> its applicants, sorted alphabetically."""
        out: dict[str, list[str]] = {}
        for a, p in sorted(self.assignment.items()):
            if p is not None:
                out.setdefault(p, []).append(a)
        return out

    @property
    def unmatched(self) -> list[str]:
        return sorted(a for a, p in self.assignment.items() if p is None)

    @property
    def rounds(self) -> int:
        return max((e.round for e in self.events if e.kind == "propose"), default=0)


def match(market: Market, proposing: Side = "applicants") -> MatchResult:
    """Run deferred acceptance with `proposing` making the offers."""
    if proposing == "applicants":
        proposer_prefs, receiver_prefs = market.applicant_prefs, market.program_prefs
        proposer_cap = {a: 1 for a in proposer_prefs}
        receiver_cap = {p: market.capacity(p) for p in receiver_prefs}
    elif proposing == "programs":
        proposer_prefs, receiver_prefs = market.program_prefs, market.applicant_prefs
        proposer_cap = {p: market.capacity(p) for p in proposer_prefs}
        receiver_cap = {a: 1 for a in receiver_prefs}
    else:
        raise ValueError(f"proposing must be 'applicants' or 'programs', got {proposing!r}")

    # rank[r][x] = position of x on r's list (lower is better)
    rank = {r: {x: i for i, x in enumerate(prefs)} for r, prefs in receiver_prefs.items()}
    next_choice = {x: 0 for x in proposer_prefs}
    held: dict[str, list[str]] = {r: [] for r in receiver_prefs}  # receiver -> proposers
    held_count = {x: 0 for x in proposer_prefs}

    events: list[Event] = []

    def log(round_no: int, kind: EventKind, proposer: str, receiver: str) -> None:
        a, p = (proposer, receiver) if proposing == "applicants" else (receiver, proposer)
        events.append(Event(len(events), round_no, kind, a, p))

    round_no = 0
    while True:
        # Snapshot who proposes this round, in name order, so the log is deterministic.
        offers: list[tuple[str, str]] = []
        for x in sorted(proposer_prefs):
            free = proposer_cap[x] - held_count[x]
            while free > 0 and next_choice[x] < len(proposer_prefs[x]):
                offers.append((x, proposer_prefs[x][next_choice[x]]))
                next_choice[x] += 1
                free -= 1
        if not offers:
            break
        round_no += 1

        for x, r in offers:
            log(round_no, "propose", x, r)
            if x not in rank[r]:
                log(round_no, "reject", x, r)
                continue
            current = held[r]
            if len(current) < receiver_cap[r]:
                current.append(x)
                held_count[x] += 1
                log(round_no, "hold", x, r)
                continue
            worst = max(current, key=rank[r].__getitem__)
            if rank[r][x] < rank[r][worst]:
                current.remove(worst)
                held_count[worst] -= 1
                log(round_no, "bump", worst, r)
                current.append(x)
                held_count[x] += 1
                log(round_no, "hold", x, r)
            else:
                log(round_no, "reject", x, r)

    assignment: dict[str, str | None] = {a: None for a in market.applicant_prefs}
    for r, xs in held.items():
        for x in xs:
            a, p = (x, r) if proposing == "applicants" else (r, x)
            assignment[a] = p

    for a in sorted(assignment):
        p = assignment[a]
        events.append(Event(len(events), round_no, "final" if p else "unmatched", a, p))

    return MatchResult(proposing, assignment, events)


def blocking_pairs(market: Market, assignment: dict[str, str | None]) -> list[tuple[str, str]]:
    """Every (applicant, program) pair that would both rather be together.

    That is: they rank each other, the applicant prefers the program to what
    they got (or got nothing), and the program has a free seat or prefers the
    applicant to one of the applicants it got. Sorted for stable output.
    """
    seats: dict[str, list[str]] = {p: [] for p in market.program_prefs}
    for a, p in assignment.items():
        if p is not None:
            seats[p].append(a)

    pairs = []
    for a, a_prefs in market.applicant_prefs.items():
        current = assignment.get(a)
        cutoff = a_prefs.index(current) if current in a_prefs else len(a_prefs)
        for p in a_prefs[:cutoff]:
            p_prefs = market.program_prefs[p]
            if a not in p_prefs:
                continue
            got = seats[p]
            if len(got) < market.capacity(p):
                pairs.append((a, p))
            elif any(p_prefs.index(a) < p_prefs.index(b) for b in got if b in p_prefs):
                pairs.append((a, p))
            elif any(b not in p_prefs for b in got):
                pairs.append((a, p))  # program holds someone it never ranked
    return sorted(pairs)


def is_stable(market: Market, assignment: dict[str, str | None]) -> bool:
    """True if the matching is valid and has no blocking pair."""
    seats: dict[str, int] = {}
    for a, p in assignment.items():
        if p is None:
            continue
        if not market.acceptable(a, p):
            return False
        seats[p] = seats.get(p, 0) + 1
    if any(n > market.capacity(p) for p, n in seats.items()):
        return False
    return not blocking_pairs(market, assignment)
