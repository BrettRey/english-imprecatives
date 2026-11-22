# Tier-2 Mark Davies Results Summary (TV Corpus 325M + GloWbE 1.9B)

## 1. TV Corpus (325M Words): Pronoun-Complement & `God`-Optative Profile (`T1a`, `T2`, `T3`, `T6`)

| Head | `HEAD it` (`T1a`) | `HEAD you` (`T2`) | `HEAD him/her/them/me/us` (`T3`) | `God + HEAD + NP` (`T6`) | `to hell` (`T7a`) | `for V-ing` (`T7b`, tok/typ) |
|---|---:|---:|---:|---:|---:|---:|
| *damn* | 20,107 | 1,400 | 295 | 2,229 | 101 | 15 / 11 |
| *bless* | 51 | 2,431 | 1,223 | 1,802 | 0 | 28 / 20 |
| *fuck* | 1,842 | 6,869 | 3,237 | 2 | 0 | 30 / 25 |
| *sod* | 129 | 26 | 27 | 0 | 0 | 0 / 0 |
| *bugger* | 41 | 16 | 67 | 0 | 0 | 0 / 0 |
| *screw* | 1,625 | 1,936 | 1,212 | 0 | 0 | 22 / 17 |
| *blast* | 234 | 127 | 318 | 3 | 2 | 0 / 0 |
| *curse* | 15 | 247 | 120 | 9 | 0 | 3 / 3 |
| *hang* | 634 | 344 | 1,005 | 0 | 0 | 0 / 0 |
| *drat* | 7 | 6 | 2 | 0 | 0 | 0 / 0 |
| *darn* | 613 | 25 | 12 | 11 | 0 | 1 / 1 |
| *dash* | 65 | 4 | 12 | 0 | 0 | 0 / 0 |
| *dang* | 553 | 4 | 4 | 28 | 1 | 0 / 0 |
| **Total** | **25,916** | **13,435** | **7,534** | **4,084** | **104** | **99 / 77** |

- **Univerbated (`T1b`):** *dammit* = 1,694, *goddammit* = 310 (total 2,004).
- **Open lexical NP slots (`T4`, `T5`):** `HEAD + DET + N` = **3,605** tokens across **2,178** unique types; `HEAD + POSS + N` = **2,228** tokens across **1,082** unique types.

## 2. Decisive Hypothesis Tests (TV Corpus + GloWbE)

### 2.1 H1b (`God`-Optative Ellipsis) Fails Across the Paradigm (`T6`)
- Overt `God + HEAD + NP` is overwhelmingly concentrated on theological *damn* (2,229) and *bless* (1,802), plus euphemistic *God dang it* (28) and *God darn it* (11), archaic *God curse* (9), and *God blast it* (3).
- Across the four productive secular maledictives (*fuck, screw, sod, bugger*), `God + HEAD + NP` occurs only **2** times (*God fuck you* 1, *God fuck it* 1; **0** for *screw, sod, bugger*) against **17,027** raw pronoun-complement hits (Fisher's exact $p < 10^-300$ against both *bless* and *damn*).

### 2.2 The `to hell` (`T7a`) vs. `for V-ing` (`T7b`) Double Dissociation
- **Goal PP `to hell` (`T7a`, 104 raw / 85 KWICs audited):** lexically restricted to *damn* (101) + euphemism *dang* (*Dang it to hell*, 1) + 1 coordinated *Damn, and blast you to hell* (1 literal explosive *blast them to hell* excluded). **0** tokens for *fuck, screw, sod, bugger, curse, hang, bless*.
- **Reason PP `for V-ing` (`T7b`, 99 raw across 77 unique types / 72 KWICs audited):** construction-general across *fuck* (30 tokens / 25 types), *bless* (28 / 20), *screw* (22 / 17), *damn* (15 / 11), *curse* (3 / 3), and minced *darn* (*Darn you for raising us so well*, 1 / 1).
- **Exact two-sided Fisher's exact test (`damn/dang` vs. non-`damn` across `T7a` vs. `T7b`):**
  - Full frequency tables (excl. 1 literal *blast*): **102:1** vs. **15:84**, **$p = 7.76e-40$**.
  - Strictly audited bare-NP KWICs (excl. finite/modal/nominalized/overt-*God*): **74:1** vs. **11:42**, **$p = 2.53e-22$**.

### 2.3 Coordination (`T8a`) & Primary-Interjection Control (`T8b`)
- **Coordination (`T8a`, $N=11$):** 100% lexicalized British binomial (*damn and blast it* 8, *blast and damn it* 2, *damn and blast you* 1; all 7 KWICs UK/IE). Zero free coordination of other heads.
- **Primary-interjection accusative control (`T8b`, $N=76$):** **0/76 (0.0%)** bare-NP complements (75 literal transitive verb *wow* 'impress', 1 modal-coerced verb *can't ouch him*, 0 for *oops/ugh/whoops/yuck* across 325M words).

### 2.4 H2 vs. H4 & H3 in 1.9B-Word GloWbE (`G1`, `G2`, `G3a`, `G3b`, `G4`)
- **Finite/infinitival curse-verb check for minced heads (`G4`):** **0** hits in 1.9B words (`he/she/they/will/would/could/to drat/darn/dang + him/her/them`).
- **Yet in the exact same 1.9B corpus, non-*dash* minced heads (*darn, dang, drat*) take open lexical NPs (`G1`) and unambiguous accusative pronouns (`G2`):**
  - `G1` verified non-literal full lexical NPs (top 100): **58 tokens** across **53 distinct types** (*darn*: 47 tokens / 42 types, e.g., *darn the TTC*, *darn my iPad*, *darn those Nats*, *darn those commies*, *darn my proof-reading*, *darn the consequences*; *dang*: 11 tokens / 11 types, e.g., *dang those plans*, *dang this swarm*, *dang the manager*, *dang these temptations*; excluding 4 literal sock/hole-mending *darn* tokens and 88 literal/West-African *dash* tokens).
  - `G2` unambiguous accusative pronouns (*darn/dang/drat*): **26 tokens** (*darn* 13, *dang* 11, *drat* 2).
  - **World-Englishes homonymy control on *dash* (`G2`):** Of 87 raw `dash + PRON` tokens, **31 (35.6%)** come from Nigeria and Ghana (and 16/22 = 72.7% of `dash me`), reflecting the West African English ditransitive verb *dash* ('give/tip'), alongside literal *dash [hopes/foot against a stone]*.
- **H3 Outside-Construction Mirroring (`G3a`, `G3b`):**
  - Attributive `that X N` (`G3a`, top 100 = 280): *damn* 234, *darn* 32, *darned* 8, *dang* 4, *dratted* 2.
  - Adverbial `X ADJ` (`G3b`, top 100 = 10,794): *damn* 8,742, *darn* 1,880 (e.g., *darn good* 894, *darn sure* 130, *darn close* 126, *darn cute* 81 > *damn cute* 73), *darned* 117, *dang* 55 (0 *drat/dratted/dash* in top 100).
