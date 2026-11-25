# CLAUDE.md -- English Maledictive and Benedictive NP Paradigm (ELL)

## Role: Editor/Researcher

Deep empirical, analytical, and editorial work welcome here. This is not a PM session.

## Project overview

Focused empirical English-grammar paper targeting *English Language and Linguistics* (*ELL*, <= 10,000 words inclusive of references and footnotes).

**Submitted 24 November 2026 to English Language and Linguistics.** Title: *Damn him to hell, fuck me for giving a shit, thank you for coming: How Far Generalizations Reach in English*. Current working source: `english-imprecatives-reframed.tex`; the exact submitted package is archived locally in `submission/ell-2026-11-24/`. Await editorial assessment. The earlier `english-imprecatives.tex` is retained as a prior version; the design below records the original research plan.

**Origin (2026-11-22):** Spun off from `../english-interjections/` (`interjection-disputes.tex`, reverted to `8235a47` / `8c8af90` and parked separately) after Round-4 and Round-5 blinded *ELL* reviews converged on the same diagnosis: the English bare-NP imprecative/optative paradigm (*Damn/Bless/Sod/Bugger/Fuck/Blast/Curse/Screw/Hang* + minced *Drat/Darn/Dash/Dang* + *God*-optatives) is the genuinely publishable *ELL* empirical paper, whereas keeping it inside a four-basis interjection survey diluted its evidence base.

**Preprint posted 24 November 2026:** [LingBuzz 010557](https://ling.auf.net/lingbuzz/010557), with the full supplement and a link to the replication archive. Journal status remains submitted, awaiting editorial assessment.

## Core empirical design

See `design/study-design-and-predictions.md` and `design/mark-davies-queries.md`.

- **Research question:** How is grammatical labour divided between lexical head and phrasal construction in English subjectless bare-NP maledictives and benedictives?
- **Four competing hypotheses tested head-by-head:**
  1. **H1 (Local optative/imperative ellipsis):** Head-by-head `God + HEAD + NP` alternation (*bless*, *damn* vs. *fuck*, *sod*, *bugger*).
  2. **H2 (Lexical verbal inheritance):** Restricted/defective verbal heads inheriting head-specific NP and PP valency.
  3. **H3 (Lexical-variant / euphemistic inheritance):** Minced heads (*darn, dang, drat, dash*) mirroring the multi-constructional profile of their taboo source lexeme (*damn*) both inside and outside `[X NP]` (attributive `that darn N`, adverbial `darn good`, participial `darned/dratted`).
  4. **H4 (Schematic constructional licensing, `[X NP (PP)]`):** Uniform variable-NP and PP constraints across transparent and minced heads (Goldberg 2006; Napoli & Hoeksema 2009), excluding primary interjections.
- **Two-tier variety-matched corpora:**
  - **Tier 1 (Local full-text, auditable):** BNC Baby (4M, UK conversation + fiction + news + academic, POS-tagged XML), CABNC (2.05M, UK spoken, TalkBank CHAT `0a28a11` with BNC `<s>` unit-initial capitalization cues; 0/200 `.cha` files contain millisecond Jeffersonian pauses), and OANC (14.45M, US spoken + written). Deduplicated Tier-1 total: 19,947,325 unique words after removing 12 overlapping BNC Baby `dem` files.
  - **Tier 2 (Contemporary high-power UK vs. US/CA):** Targeted manual queries on Mark Davies's TV Corpus (325M, US/CA vs. UK dialogue), GloWbE (1.9B, GB vs. US vs. CA), and COCA (1B, US), saved in `data/davies/`.

## Guardrails

- Never run automated scrapers against `english-corpora.org` (Turnstile / ToS block); Brett runs the small query sheet in `design/mark-davies-queries.md` by hand.
- Never route restricted data (`~/RestrictedCorpora`) to external APIs.
- Keep `it`-formulae (*dammit, fuck it, sod it*) and routine post-sneeze *Bless you* explicitly separated from variable-target NP objects in all counts and rates.
- Preserve strict house style (`.house-style/style-rules.yaml`: `\term{}`, `\mention{}`, `\enquote{}`, spaced en-dashes `~-- `, no em-dashes, contractions preferred, Canadian/Oxford spelling, <= 5 keywords for *ELL*).
- Never create `main.*` files; name the manuscript after the project slug (`english-imprecatives.tex` / `english-imprecatives.pdf`).
