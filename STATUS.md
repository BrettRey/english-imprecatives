---
slug: english-imprecatives
kind: paper
title: 'The Grammar of English Bare-NP Imprecatives and Benedictives: Lexical Asymmetries, Evaluative Modification, and Euphemistic Inheritance'
stage: round2_rebuilt_ready_for_r2_review
external: none
blocked_on: []
updated: 2026-11-22
next_action: 'Run Round-2 blinded ELL referee review on english-imprecatives-blind.pdf (or Brett direct review of english-imprecatives.pdf).'
---

# STATUS.md: English Bare-NP Imprecatives and Benedictives

**2026-11-22 (Round 2 rebuild complete):** Completely rebuilt `english-imprecatives.tex` for *English Language and Linguistics* (*ELL*, $\le 10{,}000$ inclusive words) following the four-referee Round-1 review (`reviews/journal-review-r1-2026-11-22/`) and Path B's nine targeted TV Corpus follow-up queries (`F1a`–`F5c`).

## Completed phases
- **Phase 1 (Tier-1 local corpora, 19.95M deduplicated words):** CABNC (2.05M UK spoken) + deduplicated BNC Baby XML (3.44M, excluding 12 overlapping BNC1994 `dem` files) + OANC (14.45M US). Conservation-verified line-level adjudication in `analysis/adjudicate_local_corpora.py` -> `data/local/adjudicated_summary.json` & `analysis/local-results-summary.md`.
- **Phase 2 (Tier-2 Davies corpora Round 1, 2.225B words + COCA pilot):** All 11 TV Corpus queries (`T1a`–`T8b`, 325M) and 5 GloWbE queries (`G1`–`G4`, 1.9B) archived verbatim in `data/davies/` and analyzed in `analysis/analyze_davies.py` -> `data/davies/davies_summary.json` & `analysis/davies-results-summary.md`.
- **Phase 3 (Round-1 draft + four-referee review):** Archived in `reviews/journal-review-r1-2026-11-22/` (Codex, Muse, Claude + Review 4).
- **Phase 4 (Path B follow-up queries `F1a`–`F5c`):** Archived verbatim in `data/davies/tv-r2-followup-2026-11-22-raw.txt` and analyzed in `analysis/analyze_davies_r2.py` -> `data/davies/davies_r2_summary.json` & `analysis/davies-r2-results-summary.md`.
- **Phase 5 (Round-2 rebuilt manuscript + named & blind PDFs):** Rebuilt `english-imprecatives.tex` -> `english-imprecatives.pdf` and `english-imprecatives-blind.pdf` (~9,650 inclusive words, 22 pages, 0 errors, 0 overfull hboxes, 0 font warnings, 0 AI-voice flags, 0 anonymity leaks, 0 `main.*` files).
