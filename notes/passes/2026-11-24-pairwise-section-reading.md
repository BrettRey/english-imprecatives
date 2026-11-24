# Pairwise section reading: english-imprecatives-reframed.tex
<!-- SUMMARY: Every pair of the abstract and seven sections read against each other for contradictions, term drift, number mismatches and unmet references; 9 findings, all fixed · status: complete · updated: 2026-11-24 -->

Run by Claude Opus 5.5 at Brett's request ("read pairwise all section pairs that haven't had a pairwise reading"). Units: abstract, §§1–7 (28 pairs). Already read as a triple: abstract–§1, abstract–§7, §1–§7. The remaining 25 were read here, from the full text of §§2–6 plus the abstract, §1 and §7.

| Pair | Finding | Fix |
|---|---|---|
| §2–§3 | §3.1 said the Tier-1 NP could begin with "a pronoun"; the extraction script (`analysis/extract_local_corpora.py`, `NEXT_NP_STARTERS`) admits only *it*, *you* and accusative pronouns, as §2.1's nominative statement assumes | §3.1 now lists *you* or an accusative pronoun, and quantifiers such as *all*, *everyone* |
| §2–§4 | the act-scoped *for the moment* was "dismissal-scope" in (1g), "frame-level" in §2.1, "scopes over the act of dismissing" in §4 | §2.1 now says "dismissal-scope" |
| §2–§5, §2–§6 | "living heads" used in §2.3, §5.1, §5.6, never defined | defined in §2.1 (*damn*, *bless*, *fuck*, *screw*, *sod*, *bugger*) |
| §2–§6, abstract–§2 | §2.1 said the pattern "displays seven grammatical properties"; abstract and §6.2 say open NPs hold for most heads | §2.1: "though not every head shows every one" |
| §1–§2 | §1 names imprecative and benedictive as pragmatic categories; §2.2 "subtypes" had no link | §2.2 opens: "The pragmatic categories of Section 1 also divide within the pattern." |
| §3–§5 | §3.3 required "an external rate" for an informative zero; §5.2 uses *damn*'s rate | §3.3: "a rate from another head or another corpus" |
| §5–§6 | §5.2's "domain of judging and retaliating" vs §6.2's evaluation-only relation | §6.2: "the grounds for evaluating it, or for retaliating against it" |
| §5–§7 | conclusion's "not even with a non-referential *it*" covered *bless*, whose *it* needs a referent (§2.2) | conclusion: "nor with *fuck it* or *screw it* where *damn it* takes it" |
| §1–§6 | §6 heading "Convergence, divergence, and productivity" left over from the old framing | "Discussion: Understood subjects, scope, and categories" |

Checked and consistent: candidate arithmetic (596 = 220 + 23 + 353), corpus sizes, 32 of 33, the bounds (97–98%, 16–27%), *G*² 145 and 127, the eight Chart-view searches, the *God* counts across Tier 1 and the TV Corpus, cross-references to §§2.1, 4.3, 5.2, 5.6, 6.1 and 6.2.
