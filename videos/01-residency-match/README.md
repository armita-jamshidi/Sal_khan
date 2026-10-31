# 01: How the Residency Match System Actually Works

Deferred acceptance (Gale-Shapley) with program capacities.

| File | What it is |
| --- | --- |
| `algorithm.py` | Deferred acceptance where either side proposes, with an event log, plus `is_stable()` |
| `example.py` | The 4-applicant, 3-program market used throughout the video, plus the naive matching for scene 3 |
| `tests/` | pytest suite for the algorithm |
| `outline.md` | Scene-by-scene outline |
| `narration.md` | Script, one `## scene_id` block per scene |
| `scenes.py` | Manim scenes that replay the event log |

Status: algorithm and example data done. Tests come next.
