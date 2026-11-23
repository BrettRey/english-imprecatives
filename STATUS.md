---
slug: english-imprecatives
kind: paper
title: 'The Grammar of English Subjectless Imprecatives and Benedictives: Lexical Asymmetries, Evaluative Modification, and Euphemistic Inheritance'
stage: submission_ready_gelman_overhaul_plus_b1
external: https://github.com/BrettRey/english-imprecatives
blocked_on: []
updated: 2026-11-23
next_action: 'Brett conducts final submission inspection of english-imprecatives.pdf (9,818 inclusive words) and english-imprecatives-blind.pdf (9,819 words) for English Language and Linguistics (or adds Spoken BNC2014 once Lancaster CQPweb/Sketch Engine access is used).'
---

# STATUS.md: English Subjectless Imprecatives and Benedictives

**2026-11-23 (Gelman quantitative overhaul + Round-4 fixes + B1 controls `D1`–`D4` complete & pushed):** Public repo live at `https://github.com/BrettRey/english-imprecatives`. Both `english-imprecatives.pdf` (9,818 inclusive words, 21 pp.) and `english-imprecatives-blind.pdf` (9,819 inclusive words, 21 pp., gitignored) compile cleanly with 0 errors, 0 overfulls, 0 font warnings, 0 non-quote house-style flags, 0 AI-voice flags, 0 Fisher *p*-values, and 0 anonymity leaks.

## Completed phases
- **Phase 1 (Tier-1 local corpora, 19.95M deduplicated words):** CABNC (2.05M) + deduplicated BNC Baby XML (3.44M, excl. 12 overlapping BNC1994 `dem` files) + OANC (14.45M); 220 verified subjectless tokens across 143 distinct files.
- **Phase 2 (Tier-2 Davies corpora Round 1, 2.225B words + COCA check):** TV Corpus (`T1a`–`T8b`, 325M) + GloWbE (`G1`–`G4`, 1.9B).
- **Phase 3–5 (Rounds 1–3 follow-ups `F1a`–`F5c`, `C1a`–`C4`, primary-source citation audit):** Archived in `reviews/` and `data/davies/*-raw.txt` (gitignored); clean parsers & summaries tracked in `analysis/` and `data/davies/`.
- **Phase 6 (Gelman quantitative overhaul + Round-4 fixes + B1 controls `D1`–`D4`, 2026-11-23):**
  - **Gelman quantitative overhaul:** Removed all Fisher *p*-values; replaced with exact counts, proportions, explicit denominators, document/series dispersion, and deterministic undisplayed-concordance bounds on `T7a` vs. `T7b` (**97.0–98.1%** vs. **16.2–27.5%**, min gap **69.5 pp**; all-audited sensitivity **98.7–98.9%** vs. **15.4–25.5%**, min gap **73.2 pp**); retired low-power `0 vs. 297` GloWbE framing; distinguished search space from audited sample size.
  - **B1 controls (`D1`–`D4`, TV Corpus):** `D1` (`fuck/screw PRON up for V-ing`, **3/3** verified retaliatory particle-verb tokens across 3 shows); `D2a` vs. `D2b` (`_n* be darned|danged` **1** verified nominal dismissal *Rules be darned* / 0 `danged` vs. **167** non-OCR `be damned/buggered` across **134** noun types, **88/100** direct bare dismissals); `D3` (`yay|boo + DET/POSS _n*`, **0/13** verified subjectless non-verbal lexical-NP complements); `D4` (`confound + PRON/DET`, **75/100** verified subjectless imprecatives across 26 shows, incl. **8** full NPs, 57.3% from *A Nero Wolfe Mystery*).
  - **Grammatical & editorial fixes:** Added non-reflexive 1sg `me` (`Fuck me!`, `Bugger me!`) diagnostic ruling out speaker-subject reduced performatives; repaired §5.3 adjunct-control and presupposed-vs.-asserted-grounds discussion; fixed abstract count (`Four`), Table 1 (`5 maledictive heads`), full `(3a)` OANC quote, non-duplicate `(1g)`, COCA `dang me` (7/7) query spec + `Davies (2020)` URL.
  - **External note on Spoken BNC2014 (`B2`):** Lancaster's `corpora.lancs.ac.uk/bnc2014/do-signup.php` MySQL socket was down on 2026-11-23; Spoken BNC2014 remains cleanly noted in §7 Limitations (query sheet prepared at `design/spoken-bnc2014-queries-b2.md`).
