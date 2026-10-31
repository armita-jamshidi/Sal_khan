# Fact check: video 1

Every historical or numeric claim the narration says out loud, with a source.
Anything not confirmed here is marked `TODO-VERIFY` in `narration.md`.

| # | Claim used in the script | Status | Source |
| --- | --- | --- | --- |
| 1 | The national Match started in 1952, run by what was then the National Intern Matching Program. | Confirmed | [Roth, "The Origins, History, and Design of the Resident Match", JAMA 2003](https://stanford.edu/~alroth/papers/JAMA.OriginsAndHistoryNRMP.Roth.pdf); [Wikipedia: NRMP](https://en.wikipedia.org/wiki/National_Resident_Matching_Program) |
| 2 | Before the Match, hospitals made offers earlier and earlier, at one point up to two years before graduation. | Confirmed | Wikipedia: NRMP ("up to two years in advance"), citing Roth 2003 |
| 3 | After 1945, hospitals used time-limited "exploding" offers, and the deadline shrank from about 10 days in 1945 to under 12 hours by 1950. | Confirmed | Wikipedia: NRMP, citing Roth 2003 |
| 4 | The 1952 procedure was, in effect, the hospital-proposing version of the algorithm, about ten years before Gale and Shapley published it. | Confirmed | Roth 1984, "The Evolution of the Labor Market for Medical Interns and Residents" (summarized on Wikipedia: NRMP: the pre-1995 algorithm was "essentially the hospital-optimal algorithm") |
| 5 | Gale and Shapley published the algorithm in 1962 ("College Admissions and the Stability of Marriage", American Mathematical Monthly). | Confirmed | Wikipedia: NRMP; Nobel press release |
| 6 | The NRMP board voted in May 1997 to switch to an applicant-proposing algorithm, first used in the 1998 Match. | Confirmed | [Roth's NRMP page](https://stanford.edu/~alroth/nrmp.html) ("NRMP Will Employ New Residency Match Algorithm In 1998"); Wikipedia: NRMP |
| 7 | The new algorithm was designed by Alvin Roth and Elliott Peranson (the Roth–Peranson algorithm, published 1999) and handles couples. | Confirmed | Roth & Peranson, "The Redesign of the Matching Market for American Physicians", American Economic Review 1999 ([PDF](https://gwern.net/doc/economics/1999-roth.pdf)) |
| 8 | Couples could match together starting in 1984. | Confirmed (one secondary source) | [Becker's Hospital Review, "Match Day: Then & now"](https://www.beckershospitalreview.com/?p=56695) |
| 9 | With couples, a stable matching isn't guaranteed to exist, but in practice the algorithm finds one. | Confirmed | Wikipedia: NRMP (couples make it NP-complete; "always terminated quickly on a stable solution" in testing) |
| 10 | Roth and Shapley won the 2012 Nobel Memorial Prize in Economic Sciences "for the theory of stable allocations and the practice of market design." | Confirmed | [Nobel Prize press release, 2012](https://www.nobelprize.org/prizes/economic-sciences/2012/press-release/) |
| 11 | David Gale died in 2008, so he could not share the prize. | Not checked. The narration doesn't use it. | `TODO-VERIFY` before adding it |
| 12 | The 2026 Match: 53,373 registered applicants and 44,344 positions, the largest Match ever. Results released at noon Eastern on March 20, 2026. (2025: 52,498 and 43,237.) | Confirmed | [NRMP press release, March 2026](https://www.nrmp.org/about/news/2026/03/nrmp-releases-results-of-the-2026-main-residency-match-for-more-than-38000-future-residents/); [NRMP press release, March 2025](https://www.nrmp.org/about/news/2025/03/national-resident-matching-program-releases-the-2025-main-residency-match-results-celebrates-the-next-generation-of-physicians/) |
| 13 | Students learn their match at the same moment, noon Eastern on Match Day. Many schools hand out envelopes at a ceremony. | Confirmed (noon ET); envelopes are a school tradition, not universal | NRMP press release; Becker's |
| 14 | In the applicant-proposing version, no applicant can do better by lying about their ranking. | Confirmed | Wikipedia: NRMP ("applicants cannot benefit by misreporting preferences") |

## Things the script avoids on purpose

- It doesn't say the real Match is plain Gale-Shapley. The real one is Roth–Peranson, an extension.
- It says the 1998 switch had a small effect in practice. Roth's own studies found very few applicants would have matched differently.
  `TODO-VERIFY`: the exact share (often quoted as about 0.1%).
- It never names the NRMP's logo or branding on screen. The name "NRMP" is said only as a fact.
- The "side that waits gets its worst stable outcome" line is proven in the notes for one seat per program. With capacities it's a standard result for responsive preferences (Roth and Sotomayor, *Two-Sided Matching*, 1990), still marked `TODO-VERIFY` in the narration.
