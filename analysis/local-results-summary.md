# Tier-1 Local Corpus Results Summary (Adjudicated & Deduplicated)

## 1. Corpus Footprint and Zero-Overlap Deduplication

| Corpus | Variety / Register | Files | Tokens | Notes |
|---|---|---:|---:|---|
| CABNC (TalkBank CHAT) | UK spoken (BNC1994 demographic) | 1,860 | 2,054,817 | Unit-initial capitalization preserves BNC `<s>` boundaries |
| BNC Baby XML (full) | UK dem + fic + news + aca | 182 | 4,001,787 | CLAWS5 POS-tagged (100% recall incl. `NP0`, bare nouns) |
| BNC Baby XML (deduplicated) | UK non-CABNC dem (18) + fic/news/aca (152) | 170 | 3,442,717 | Excludes 12 `dem` files overlapping CABNC (559,070 tokens) |
| OANC | US spoken + written | 8,824 | 14,449,791 | Disjoint US sample (Switchboard, Charlotte, Slate, Verbatim, etc.) |
| **Deduplicated Tier-1 Total** | **UK + US** | **10,854** | **19,947,325** | **Zero duplicate BNC1994 spoken tokens** |

## 2. Pooled Deduplicated Bare-NP & `God`-Optative Counts (All 13 Target Heads)

| Head | Raw Cand. | Bare-NP Verified | `it` | `bless you` | 2sg (`you`) | Non-2sg pron | Dem (`this/that`) | Poss-body | Full lexical NP | Overt `God + HEAD + NP` | Excluded |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| *damn* | 80 | **33** | 17 | 0 | 7 | 2 | 0 | 0 | 7 | 3 | 44 |
| *bless* | 124 | **82** | 1 | 31 | 0 | 18 | 0 | 31 | 1 | 20 | 22 |
| *fuck* | 101 | **46** | 17 | 0 | 10 | 9 | 5 | 0 | 5 | 0 | 55 |
| *sod* | 29 | **21** | 8 | 0 | 2 | 4 | 3 | 0 | 4 | 0 | 8 |
| *bugger* | 43 | **21** | 7 | 0 | 0 | 10 | 2 | 0 | 2 | 0 | 22 |
| *screw* | 42 | **13** | 3 | 0 | 3 | 1 | 1 | 0 | 5 | 0 | 29 |
| *blast* | 49 | **1** | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 48 |
| *curse* | 14 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 14 |
| *hang* | 103 | **1** | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 102 |
| *drat* | 1 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| *darn* | 6 | **2** | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| *dash* | 4 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| *dang* | 0 | **0** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total** | **596** | **220** | **56** | **31** | **22** | **45** | **11** | **31** | **24** | **23** | **353** |

## 3. UK vs. US Regional Split (Deduplicated Tier-1 Bare-NP Verified)

| Head | UK (CABNC + dedup BNC Baby, 5.50M) | US (OANC, 14.45M) | Key Attested Full-NP / `for`-PP Examples |
|---|---:|---:|---|
| *bless* | 52 (+10 *God*) | 30 (+10 *God*) | *Bless you for helping me out with the Watsons*; *bless mummy and dad*; *bless his little cotton socks*; US *bless your/his/her/their heart(s)* (×22) |
| *fuck* | 33 | 13 | *oh fuck this for an idea*; *Fuck the doctors*; *Fuck the title*; *Fuck this court!*; *Fuck the gravy*; *Fuck the Draft* |
| *damn* | 22 | 11 (+3 *God*) | *Damn McIllvanney*; *damn his blackmail*; *Damn the bell!*; *damn the copy desk*; *Damn the myopic... eyes of that news-ferret Cramer for having...*; *Damn that infernal Sun Yat-Sen*; *Damn those miserable bastards at Shining Path* |
| *sod* | 20 | 1 | *sod this for a lark*; *Sod the choir!* (×2); *Sod my time*; *sod the filmmakers!* |
| *bugger* | 20 | 1 | *Bugger the rest!*; *Bugger your sovereignty* |
| *screw* | 7 | 6 | *Oh, screw Jesus Christ*; *And screw his mother Mary too!*; *Screw the Times, young readers, and everything else*; *Screw the Cabinet and the rest*; *screw everything they're going to think...* |
| *blast* | 1 | 0 | *blast it* (BNC Baby `FPB.xml:3077`) |
| *hang* | 0 | 1 | *But hang me* (archaic literary quote in Slate) |
| *darn* | 1 | 1 | *Darn it* (CABNC); *oh gosh darn it* (OANC Switchboard) |
| *curse / drat / dash / dang* | 0 | 0 | *Verbatim* literary quotes (*Curse it!*, *Drat you and your dog!*) excluded as metalinguistic; *Dash that* in CABNC excluded as UK fashion brand *Dash* |

## 4. Key Hypothesis Diagnostics Already Resolved in Tier 1

### 4.1 Syntactic Integration vs. Primary Interjections (CABNC TalkBank Unit-Boundary Test)
- **Primary-6 comparators (*ouch, oops, ugh, wow, whoops, yuck*):** 0 verified bare-NP complements across all 19.95M deduplicated words (23 CABNC + 16 dedup BNC Baby + 109 OANC = 148 raw sequences audited; all are finite-clause subjects, fixed *oops/whoops a daisy*, literal verbs *wow us / yuck it up*, or detached verbless exclamatives like *Ouch. My foot*).
- **CABNC unit-boundary segmentation cue (unit-initial capitalization inherited from BNC `<s>` breaks):**
  - Verified bare-NP maledictives/benedictives: **0/80 (0.0%)** carry an intervening boundary cue.
  - Primary-6 + NP-starter sequences: **9/23 (39.1%)** carry an intervening boundary cue.
  - Two-sided Fisher's exact test (all verified vs. primary-6): **$p = 3.26e-07$** (excluding routine *bless you*: **0/66** vs. **9/23**, **$p = 1.29e-06$**).
  - Within the *same* maledictive heads (*damn/fuck*), standalone interjections followed by a new clause (*Fuck. That would have been amusing*; *Oh fuck. You dickhead*) show boundary cues in **4/7 (57.1%)** vs. **0/80** for verified bare-NP complements (Fisher's exact **$p = 1.57e-05$**).

### 4.2 H1b (`God`-Optative Ellipsis) Fails Across the Paradigm
- Overt `God + HEAD + NP` occurs **20** times with *bless* (20/102 = 19.6% of *bless* tokens) and **3** times with *damn* (all 3 are *God damn it* in OANC; 3/36 = 8.3%), vs. **0/105 (0.0%)** across *fuck, sod, bugger, screw, blast, hang, darn*.
- *bless* vs. all maledictives pooled: Fisher's exact **$p = 5.84e-06$**.
- *damn* vs. non-*damn* maledictives (*fuck/sod/bugger/screw/blast/hang/darn*): Fisher's exact **$p = 0.0156$**.
- Notably, BNC Baby `KP2.xml:1053` (*oh god darn , it 's not eleven yet is it ?*) is a standalone *oh god darn* followed by a finite clause, NOT an NP complement.

### 4.3 BNC Baby POS-Tagged Full-Recall Audit (What `PRON/DET`-Only Queries Miss)
- Using CLAWS5 POS tags (`NP0`, `NN1/NN2`, `PNI`) caught **3 genuine bare-NP imprecatives** that a closed-class `PRON/DET` filter would miss: *Damn McIllvanney* (`NP0`), *Oh, screw Jesus Christ* (`NP0`), and *bless mummy and dad* (`NN1`), plus the prenominal-vs.-imprecative ambiguity token *Damn DTs* (`NP0`, excluded from strict counts). This calibrates recall for our Tier-2 Davies queries.

### 4.4 Archived COCA Pilot (`coca-2026-11-22-pilot-dang.txt`) Preview for H3
- Outside-construction lexical mirroring is strong: `that danged _nn*` = 5, `danged _j*` = 16 (alongside OANC `darned` = 35, `darn` = 58), while `dang` inside `[X NP]` is heavily skewed toward fixed `dang it` (100+ cap) and echoic `dang me` (7/7 Roger Miller song/allusion) with 1 genuine variable full NP (*Dang those bananas*) and 1 reason-PP example (*Dang you, Whole Foods for being so dang good*).
- Tier-2 TV Corpus (325M) and GloWbE (1.9B) queries in `design/mark-davies-queries.md` will now deliver the large-sample US vs. UK frequencies needed to adjudicate **H2**, **H3**, and **H4** cleanly.
