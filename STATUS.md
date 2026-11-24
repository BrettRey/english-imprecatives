---
slug: english-imprecatives
kind: paper
title: 'The Grammar of English Subjectless Imprecatives and Benedictives: Lexical Asymmetries, Evaluative Modification, and Euphemistic Inheritance'
stage: reframed_draft_pre_submission_checks
external: https://github.com/BrettRey/english-imprecatives
blocked_on: [brett-review]
updated: 2026-11-24
next_action: 'Submission candidate is english-imprecatives-reframed.tex (english-imprecatives.tex retained; passes.py pinned to the reframed file). Submission checks 2026-11-24: quotation, terminology (after acronym fixes), build, blinding pass; cold read FAIL on the first run, PASS after the abstract and opening revision (question first, results led by where generalizing from damn/fuck fails, abstract ends on what the results rule out; rerun 2/3 advance, no MISSING, convergent problem statements); 20 registered passes outstanding. Next: work through the passes, then package and portal-fields record.'
---

# STATUS.md: English Subjectless Imprecatives and Benedictives

**2026-11-23 (Gelman overhaul + B1 TV controls `D1`–`D4` + B2 Spoken BNC2014 calibration complete & pushed):** Public repo live at `https://github.com/BrettRey/english-imprecatives`. Both `english-imprecatives.pdf` (9,915 inclusive words, 21 pp.) and `english-imprecatives-blind.pdf` (9,916 inclusive words, 21 pp., gitignored) compile cleanly with 0 errors, 0 overfulls, 0 font warnings, 0 non-quote house-style flags, 0 AI-voice flags, 0 Fisher *p*-values, and 0 anonymity leaks.

## Completed phases
- **Phase 1 (Tier-1 local corpora, 19.95M deduplicated words):** CABNC (2.05M) + deduplicated BNC Baby XML (3.44M, excl. 12 overlapping BNC1994 `dem` files) + OANC (14.45M); 220 verified subjectless tokens across 143 distinct files.
- **Phase 2–5 (Tier-2 Davies corpora 2.225B words + COCA check + Rounds 1–3 follow-ups `F1a`–`F5c`, `C1a`–`C4`):** Clean parsers & aggregated summaries tracked in `analysis/` and `data/davies/`; raw corpus extracts and internal review logs gitignored.
- **Phase 6 (Gelman quantitative overhaul + B1 TV controls `D1`–`D4`, 2026-11-23):** Removed all Fisher *p*-values; added deterministic undisplayed-concordance bounds on `T7a` vs. `T7b` (**97.0–98.1%** vs. **16.2–27.5%**, min gap **69.5 pp**; all-audited **73.2 pp**); added `D1` (3/3 retaliatory `fuck PRON up for V-ing`), `D2a`/`D2b` (1 nominal *Rules be darned* vs. 167 non-OCR `be damned/buggered` / 134 types, 88/100 bare), `D3` (0/13 `yay/boo` lexical-NP complements), `D4` (75/100 `confound`, 8 full NPs, 57.3% *A Nero Wolfe Mystery*); added non-reflexive 1sg `me` (`Fuck me!`, `Bugger me!`) diagnostic.
- **Phase 7 (B2 Spoken BNC2014 contemporary unscripted British benchmark, 11.83M tokens via Sketch Engine `preloaded/bnc2014_spoken_tt3`, 2012–2016):**
  - Core 13 heads (`B2-1a`, $N = 1{,}311$ + 12 `dammit`): living heads dominate (`bless` 502, `fuck` 457 incl. 65 `fuck me`, `damn` 167 + 12 `dammit`, `screw` 50, `bugger` 27 incl. 4 `bugger me`, `sod` 26; 48/100 audited `DET/POSS` tokens + 1 quoted *fuck the world*); archaic/minced near-absent (`drat` 0, `dang` 0, `blast` 0/13, `dash` 1/2, `curse` 1/4, `darn` 2/3, `confound` 1/1).
  - `B2-2` (`fuck`-euphemisms): **0/11** verified subjectless imprecatives in unscripted speech, proving TV `F3`'s strong censorship/franchise component.
  - `B2-3` (overt `God`): **15/15 (100%)** verified optatives theological (`god damn it` 10, `god bless` 5), **0** secular (both `god fuck` hits are standalone *oh [my] god!* exclamations).
  - `B2-4a/b` & `B2-5b`: `1/1` *damn it to hell*, `3/3` *for V-ing* (`bless` 2, `damn` 1), and **0/17** `yay/boo` NP complements.
