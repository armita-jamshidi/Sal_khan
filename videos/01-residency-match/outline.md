# Outline: How the Residency Match System Actually Works

Target runtime **6:20**, following the pacing plan (`pacing.md`). Word budgets
assume 150 spoken words per minute.

Built from the notes brief (`notes_brief.md`), the fact check (`sources.md`),
and the example in `example.py`. Every name and result below comes from
`algorithm.py`'s event log for that example.

## The example

Four applicants and three programs. City has 2 seats, and Mercy and Lake have 1 each.

| Applicant | Ranks programs | | Program | Seats | Ranks applicants |
| --- | --- | --- | --- | --- | --- |
| Ana | Mercy, City, Lake | | City | 2 | Ana, Ben, Cy, Dee |
| Ben | Mercy, Lake, City | | Mercy | 1 | Dee, Ana, Ben, Cy |
| Cy | City, Mercy, Lake | | Lake | 1 | Ana, Cy, Ben, Dee |
| Dee | Lake, City, Mercy | | | | |

**Applicants propose (3 rounds).**

1. Round 1: Ana and Ben both ask Mercy. Mercy keeps Ana and says no to Ben. Cy asks City and Dee asks Lake, and both get a maybe.
2. Round 2: Ben asks Lake. Lake likes Ben more than Dee, so Dee is bumped.
3. Round 3: Dee asks City, which still has a free seat. Nobody is left to ask.

Final: **Ana–Mercy, Ben–Lake, Cy and Dee at City.** Ana and Cy get their first
choice, and Ben and Dee get their second.

**Programs propose (2 rounds).** Final: **Ana and Ben at City, Cy–Lake, Dee–Mercy.**
Every applicant ends up somewhere different. Ben, Cy and Dee all land at their
last choice, while every program does at least as well as before.

**Naive matching for scene 3.** "Everyone gets their first choice, and a coin
flip settles ties." Ben wins the coin flip for Mercy, so Ana falls back to City:
**Ben–Mercy, Ana–City, Cy–City, Dee–Lake.** The one blocking pair is
**(Ana, Mercy)**: Ana would rather be at Mercy, and Mercy would rather have Ana
than Ben.
<!-- TODO-VERIFY: the algorithm thread is adding the naive matching to example.py.
If it picks a different one, scene 3's lines change to match. -->

## Words used on screen

- **Applicants** and **programs**. "Hospital" is fine in passing, since the icons are hospitals.
- **Blocking pair.** It's said once that textbooks also call it an "instability".
- **Ask** (propose), **maybe** (tentatively held), **no** (rejected), **bumped** (a held applicant replaced by a better one), **final**.
- Colors follow `common/style.py`: proposing in blue, held in peach, rejected in gray, final in tangerine, blocking pair in red. The narration never names a color, so the palette can change without re-recording.

## Scenes

Each scene's `scene_id` is the `## heading` in `narration.md`.

### 1. Hook, `hook` (0:00–0:30, ~75 words)

- **Question:** how does one computer decide where thousands of doctors go, fairly?
- **On screen:** a grid of envelopes, one opens, then they all collapse into a box labeled "the algorithm". A short title card comes after the question.
- **Facts:** noon Eastern on a Friday in March. The 2025 Match had about 52,000 applicants and 43,000 positions (`sources.md` #12, #13).
- **Takeaway:** the viewer will be able to run the algorithm by hand by the end.

### 2. The problem, `problem` (0:30–1:15, ~110 words)

- **Question:** who should go where?
- **On screen:** applicants slide in on the left and programs on the right. City shows two seats. Then the rank lists unfold.
- **Takeaway:** both sides have opinions, and a program can take more than one person.

### 3. Why naive approaches fail, `blocking_pair` (1:15–2:00, ~110 words)

- **Question:** what goes wrong with the obvious answer?
- **On screen:** the naive matching is drawn, then Ana and Mercy flash red at about 1:35.
- **Definition:** a blocking pair is an applicant and a program who both prefer each other to what they got.
- **History, 15 seconds:** before 1952, hospitals made offers years early, then used exploding offers with deadlines down to hours (`sources.md` #1–3).
- **Takeaway:** we want a matching with no blocking pair. That's called stable.

### 4. The algorithm, `algorithm` (2:00–4:00, ~300 words)

`AlgorithmScene` reads this block **by paragraph position**, so it needs exactly
five paragraphs, in this order:

1. The rules in one breath.
2. Round 1, slow, with every proposal narrated.
3. Round 2, the first bump (the camera zooms in here): Ben bumps Dee from Lake.
4. Round 3, fast-forwarded: Dee lands at City.
5. Nobody is left to ask, so every maybe becomes final.

- **Takeaway:** a "maybe" isn't a yes until the very end. That's why it's called *deferred* acceptance.

### 5. Why it's stable, `stability` (4:00–4:45, ~110 words)

- **Question:** could a blocking pair be hiding in the result?
- **Argument** (notes p. 11, flipped so applicants propose): if Ben likes Mercy more than Lake, he must have asked Mercy first. Mercy said no because it had someone it liked more, and programs only ever trade up. So Mercy doesn't want Ben. The same goes for Dee and Lake.
- **On screen:** a flashback of Ben's round 1 rejection and Dee's round 2 bump, then a check mark.
- **Takeaway:** says the word "fair" on purpose, to close the hook's question.

### 6. Who proposes matters, `who_proposes` (4:45–5:30, ~110 words)

- **Question:** what if the programs did the asking?
- **On screen:** the arrows flip direction and the program-proposing run plays at 2x, then a split screen holds both results for 5 seconds.
- **Takeaway:** both results are stable, but the side that asks gets its best possible stable outcome, and the side that waits gets its worst (notes pp. 5–6, 12–13). Most textbooks, including the notes, run it with hospitals asking. The real Match switched to applicants asking: the NRMP board voted for it in 1997, and it was first used in the 1998 Match (`sources.md` #6).

### 7. Real world, `real_world` (5:30–6:00, ~75 words)

- **On screen:** two linked applicant icons for a couple, then a text card.
- **Facts:** the real Match runs the Roth–Peranson algorithm, which is deferred acceptance plus extras like couples applying together. With couples a stable answer isn't guaranteed, but in practice one is found. Roth and Shapley shared the 2012 Nobel Prize in Economics. Gale died before it was awarded (`sources.md` #7–11).

### 8. Recap and outro, `outro` (6:00–6:20, ~45 words)

- Three recap beats: ask your favorite, a maybe isn't a yes, whoever asks wins.
- Call to action, then the end screen by 6:10.

## Word budget

| Scene | Target | Draft |
| --- | --- | --- |
| hook | 75 | see `narration.md` |
| problem | 110 | |
| blocking_pair | 110 | |
| algorithm | 300 | |
| stability | 110 | |
| who_proposes | 110 | |
| real_world | 75 | |
| outro | 45 | |
| **Total** | **935 (~6:15)** | |
