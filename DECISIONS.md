# DECISIONS.md -- English Maledictive and Benedictive NP Paradigm

## 2026-11-22 -- Project creation & empirical design
- **Origin:** Created as a standalone *ELL* empirical paper (`<= 10,000` words) after five rounds of simulated reviews on `../english-interjections/interjection-disputes.tex` established that the English bare-NP maledictive/benedictive paradigm is the focused empirical paper *ELL* referees want.
- **Folder location:** Sibling directory `papers/queue/english-imprecatives/` (matching portfolio convention and keeping `english-interjections/` cleanly separated).
- **Corpora selected:**
  - Local Tier 1 (full recall, auditable full-text + prosodic markers): BNC Baby (4M UK XML), CABNC TalkBank CHAT `0a28a11` (2.05M UK spoken, raw Jeffersonian prosody preserved), and OANC (15M US spoken + written).
  - External Tier 2 (manual Mark Davies queries by Brett): TV Corpus (325M, US/CA vs. UK dialogue), GloWbE (1.9B, GB vs. US vs. CA), and COCA (1B, US).
- **Key methodological commitments (from R4–R5 lessons):**
  1. Test **four** explicit competing hypotheses (H1 head-by-head optative ellipsis, H2 lexical verbal inheritance, H3 lexical-variant/euphemistic inheritance, H4 schematic construction `[X NP (PP)]`), avoiding binary false dichotomies.
  2. Separate fused/resignative `it`-formulae (*dammit, fuck it, sod it*) and routine post-sneeze *Bless you* from variable-target NP objects in every rate and comparison.
  3. Match corpus variety explicitly (UK arm vs. North American arm) rather than pooling 1990s British tokens with Canadian introspection.
  4. Test head-independent prosodic cues in CABNC raw `.cha` transcripts for primary interjections + adjacent NP (*Ouch, my foot*; *Oh, the...*; *Ah, you pillock*) vs. integrated maledictive/benedictive complements.


## 2026-11-23 -- External review clearance & Option #2 Freeze-and-Ship pass
- **External quantitative review:** Cleared the Gelman statistical overhaul (deterministic undisplayed-hit bounds on `to hell` vs. `for V-ing`, primary-interjection query-yield framing, illustrative *bless* framing, surviving theoretical underdetermination) and recommended freezing corpus collection and applying five bounded claim-scope/audit-label corrections plus trimming the abstract before *ELL* submission.
- **Decision (Brett: "proceed" on Option #2):** Applied all five external-reviewer fixes, tightened the abstract (288 $\to$ 205 words), fixed four minor R5 bookkeeping items (updated title to *Partial Euphemistic Correspondence*; listed the 60 unaudited raw `hang` hits in `B2-1a`; noted KWIC-context provenance for `(6b) Eff Christmas`; separated the two colliding `37` counts in §5.3), and upgraded §6.2 with a compact **head-by-property verbal-retention matrix** (`Table 8`) built solely from already-audited diagnostics showing graded, lineage-specific retention while keeping lexicalist vs. constructionist storage honestly underdetermined.
- **Verification (clean):** Both named (`english-imprecatives.pdf`, 21 pp., 9,891 words) and anonymized (`english-imprecatives-blind.pdf`, 21 pp., 9,892 words) PDFs built with 0 LaTeX errors/overfulls/font warnings/undefined refs, 0 non-quote style flags, 0 AI-voice flags, 0 stale phrases, 0 anonymity leaks, and all Python audit assertions passing. No Round-6 simulated review loop; ready for *ELL* submission.
