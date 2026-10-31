# Notes brief: video 01, How the Residency Match System Actually Works

Source: `gale_shapley.pdf`, 13 pages of handwritten lecture notes on stable matching, from an undergraduate algorithms course.
The PDF is kept out of git (see `notes/README.md`). The script specialist should work from this brief.

## What the notes cover

| Pages | Lecture | Topic | Used for video 1? |
| --- | --- | --- | --- |
| 1-4 | 1 | Course intro, problem setup, definitions, Gale-Shapley pseudocode, worked example run in two orders | Yes |
| 9-13 | 2 | Pseudocode again (rejections labelled), O(n²) running time, proof of stability, valid partners, "no hospital is rejected by a valid partner" | Yes |
| 5-6 (top) | 3 | Recap: hospital-optimal, then proof that the output is resident-pessimal | Yes |
| 6 (bottom)-8 | 3 | **Greedy algorithms: interval scheduling, Earliest Finish Time, "greedy stays ahead"** | No. This is a good candidate for a future video. |

The PDF pages are not in lecture order: pages 9-13 come before pages 5-8.

## Key definitions (the notes' wording, lightly cleaned)

- **Setup.** There is a set H of hospitals and a set R of residents. Each side ranks everyone on the other side.
- **Assumptions in the notes.** |H| = |R| = n. Preference lists are complete and have no ties. Each hospital wants one resident, and each resident wants one hospital.
- **Matching.** A set of pairs (h, r) in which each hospital and each resident appears at most once.
- **Perfect matching.** A matching with |M| = n.
- **Instability.** For a perfect matching M, a pair (h, r) where h prefers r to its match in M, *and* r prefers h to its match in M. The video outline calls this a **blocking pair**. The notes never use that term, so the script should say once that the two names mean the same thing.
- **Stable matching.** A perfect matching with no instabilities.
- **Valid partner / valid match.** h and r are valid partners if *some* stable matching pairs them.
- **Hospital-optimal.** Every hospital gets its best valid partner.
- **Resident-pessimal.** Every resident gets their worst valid partner.

## The algorithm as the notes give it (hospitals propose)

```
M ← ∅
while some hospital h is unmatched:
    r ← first resident on h's list that h hasn't proposed to
    h proposes to r
    if r is unmatched:            add (h, r)
    elif r prefers h to current h': remove (h', r), add (h, r)   # r "rejects" h'
    else:                         do nothing                      # r "rejects" h
return M
```

**Important for the script:** in the notes, **hospitals propose**. The video's main run (section 4) has **applicants propose**, because that is what the NRMP has used since 1998. The script has to flip the roles on purpose. The notes' hospital-proposing version fits section 6, "Who proposes matters."

## Examples in the notes (all checked by running the algorithm)

### Example A: 3x3, pages 2 and 4

| Hospital | Ranks residents | | Resident | Ranks hospitals |
| --- | --- | --- | --- | --- |
| a | 1, 2, 3 | | 1 | a, b, c |
| b | 3, 2, 1 | | 2 | c, b, a |
| c | 1, 3, 2 | | 3 | a, b, c |

- **Page 2, unstable matching.** M = {(a,1), (b,2), (c,3)}. Its instability is **(b, 3)**: b ranks 3 first, and 3 prefers b to c. This is drawn as a green line. **It is a ready-made shot for section 3 (the blocking pair in red).**
- **Page 4, run in order a, b, c.** a→1 held, b→3 held, c→1 rejected, c→3 rejected, c→2 held. That is 5 proposals, ending at {(a,1), (b,3), (c,2)}.
- **Page 4, run in order b, c, a.** b→3 held, c→1 held, a→1 (1 drops c for a), c→3 rejected, c→2 held. The result is the same matching. This shows that **the order of proposals doesn't change the result.**
- Caveat: this instance has **only one** stable matching, so it **cannot** show "who proposes matters." Resident-proposing gives the same {(a,1), (b,3), (c,2)}.

### Example B: 3x3 with two stable matchings, page 12

| Hospital | Ranks residents | | Resident | Ranks hospitals |
| --- | --- | --- | --- | --- |
| a | 1, 2, 3 | | 1 | b, a, c |
| b | 2, 1, 3 | | 2 | a, b, c |
| c | 1, 2, 3 | | 3 | a, b, c |

- **Blue: {(a,1), (b,2), (c,3)}.** This is what hospital-proposing produces. Each hospital gets its first choice.
- **Red: {(a,2), (b,1), (c,3)}.** This is what resident-proposing produces. Residents 1 and 2 each get their first choice.
- Valid partners: resident 1 can end up with a or b, but never c. If 1 were paired with c, then a and 1 would form an instability.
- **This is the right example for section 6.** One set of preferences gives two different stable answers, depending on which side proposes.

### Not in the notes

The outline's main example has 4 applicants, 3 programs, and one program with 2 slots. **The notes never cover capacities.** The script and algorithm specialists will need to design that example themselves. Its results should come from `algorithm.py`'s event log, not from working it out by hand.

## Proofs and arguments to adapt

1. **Running time, O(n²)** (page 10). A resident, once matched, stays matched and only trades up. So each hospital is rejected at most n−1 times, and there are at most n² proposals. This is a nice one-line aside, not a full section.
2. **Stability** (page 11). Suppose (h, r) is an instability. h prefers r to its partner, so h proposed to r earlier and r turned h down for someone better. Residents only trade up, so r's final partner is still better than h. Contradiction. **This is the core of section 5.** It is the same argument as the outline's, with the roles flipped for applicant-proposing.
3. **Proposer-optimal** (pages 12-13). No hospital is ever rejected by a valid partner. The proof is by contradiction about the *first* such rejection, with two cases. It is too long for the video. Use only its conclusion in section 6: "the proposing side gets its best possible stable outcome."
4. **Receiver-pessimal** (pages 5-6). The side that receives proposals gets its *worst* valid partner. This is a strong one-liner for section 6: the side that proposes gets its best stable outcome, and the side that waits gets its worst.

## Mapping to the video outline

| Outline section | What the notes give | Gaps |
| --- | --- | --- |
| 1. Hook | Nothing | Match Day material has to come from outside the notes |
| 2. The problem | Definitions, assumptions, the H/R two-column diagram | Notes are 3x3 with capacity 1. Video uses 4x3 with capacities. |
| 3. Naive approaches fail | Example A's unstable matching with instability (b,3) | The pre-1952 chaos and exploding offers are not in the notes |
| 4. The algorithm | Pseudocode, step-by-step run of Example A, order independence | Must flip to applicant-proposing and add capacities |
| 5. Why it's stable | Page 11 proof | Rephrase for applicants proposing |
| 6. Who proposes matters | Example B, hospital-optimal and resident-pessimal results | 1998 NRMP switch is not in the notes |
| 7. Real world | Only "Gale-Shapley (1962)" and the "Stable Marriage" label | Roth-Peranson, couples, and the Nobel are not in the notes |
| 8. Outro | Nothing | |

## Claims to fact-check (mark TODO-VERIFY in narration until checked)

- Gale and Shapley published in **1962**. The notes say this. Believed to be "College Admissions and the Stability of Marriage," *American Mathematical Monthly*.
- The NRMP started in **1952**, and before that the market had **exploding offers**. This comes from the outline, not the notes.
- The NRMP switched to **applicant-proposing** in **1998**, using the Roth-Peranson algorithm. Check whether the decision was made in 1997 and first used in the 1998 Match.
- **Roth and Shapley** won the 2012 economics Nobel for this work. This is optional for section 7.
- Running time is O(n²) proposals. This comes from the notes and is verified by the proof.
- "The proposing side gets its best stable outcome, and the other side gets its worst." This comes from the notes and is proven there for capacity 1. For the capacity version, the applicant-optimal half is standard. **Confirm the program-side statement with capacities before saying it on screen.**
- The real Match also handles couples, and with couples a stable matching might not exist. This is outside the notes and should be checked before saying it.

## Notes for the other specialists

- **Script:** The notes call it an "instability" and the outline calls it a "blocking pair." Pick one on-screen term and introduce the other once. The notes' "propose / reject" wording works well as everyday language. "Hold" (tentatively accept) is the video's word and does not appear in the notes.
- **Notation trap:** page 12 writes pairs as (resident, hospital), for example "(1, b)," while every other page uses (hospital, resident). Don't copy that onto the screen.
- **Visual:** the notes' two-column drawing works well as a layout. Hospitals go on the left with their rank lists, residents go on the right with theirs, lines show matches, dashed lines show rejections, and small circled numbers mark the order of proposals.
- **Do not name** the course, the university, or the instructor in the video.
