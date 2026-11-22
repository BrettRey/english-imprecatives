# Mark Davies (english-corpora.org) Manual Query Sheet (v2 — Clean Syntax)

**Purpose:** Variety-matched contemporary data (US/CA vs. UK) for *Between Defective Verb and Schematic Construction: The English Maledictive and Benedictive NP Paradigm* (*ELL*).
**Total:** 12 query blocks (**TV Corpus** T1–T8 + **GloWbE** G1–G4). Every query is in a **plain fenced code block with unescaped `|`** (zero backslashes).
**Interface setting:** Select **LIST** view and check **Sections** (TV Corpus: `US/CA` vs. `UK/IE`; GloWbE: `GB`, `US`, `CA`) so each query returns a single frequency table across all heads and varieties in one click. Copy-paste the **LIST frequency table** (plus KWIC only on the 4 queries marked `[+KWIC]`) into `papers/queue/english-imprecatives/data/davies/` (or paste directly into chat).

---

## Block 1: TV Corpus (325M words — LIST view, Sections: US/CA vs. UK/IE)

### T1a — Fused `HEAD it` (`IT_FORMULA` baseline across all 13 heads)
```text
damn|fuck|sod|bugger|blast|curse|screw|hang|bless|drat|darn|dash|dang it
```

### T1b — Univerbated `dammit` / `goddammit`
```text
dammit|goddammit
```

### T2 — Caseless 2sg `HEAD you`
```text
damn|fuck|sod|bugger|blast|curse|screw|hang|bless|drat|darn|dash|dang you
```

### T3 — Unambiguous non-2sg accusative pronouns (`him/her/them/me/us`)
```text
damn|fuck|sod|bugger|blast|curse|screw|hang|bless|drat|darn|dash|dang him|her|them|me|us
```

### T4 — Definite & demonstrative full lexical NPs (`FULL_NP_LEX`)
```text
damn|fuck|sod|bugger|blast|curse|screw|hang|bless|drat|darn|dash|dang the|this|that|these|those _n*
```

### T5 — Possessive full lexical NPs (`Bless his heart`, `Damn your eyes`, `Darn my luck`)
```text
damn|fuck|sod|bugger|blast|curse|screw|hang|bless|drat|darn|dash|dang my|your|his|her|their _n*
```

### T6 — Overt `God + HEAD + NP` optative alternation (tests H1b head by head)
```text
god damn|bless|fuck|sod|bugger|blast|curse|screw|hang|drat|darn|dash|dang it|you|him|her|them|me|us|the|this|that|my|your|his|her
```

### T7a — Goal PP `to hell`
```text
damn|fuck|sod|bugger|blast|curse|screw|bless|drat|darn|dash|dang you|him|her|them|it to hell
```

### T7b — Reason PP `for V-ing`
```text
damn|fuck|sod|bugger|blast|curse|screw|bless|drat|darn|dash|dang you|him|her|them|me for _v?g*
```

### T8a — Coordinated heads over shared pronoun
```text
damn|blast|curse|fuck|screw|sod|bugger and damn|blast|curse|fuck|screw|sod|bugger it|you|him|her|them
```

### T8b — Primary-interjection accusative control `[+KWIC up to 50]`
```text
ouch|oops|ugh|wow|whoops|yuck him|her|them
```

---

## Block 2: GloWbE (1.9B words — LIST view, Sections: GB, US, CA)

### G1 — Minced heads + full lexical NPs `[+KWIC 100]` (decisive H4 test)
```text
drat|darn|dang|dash the|this|that|these|those|my|your|his|her _n*
```

### G2 — Minced heads + unambiguous accusative pronouns `[+KWIC 50]`
```text
drat|darn|dang|dash him|her|them|me|us
```

### G3a — Outside-construction mirroring: attributive (`that damn/darn/dang/dratted N`, tests H3)
```text
that damn|darn|dang|dratted|darned|dashed|danged _n*
```

### G3b — Outside-construction mirroring: adverbial (`damn/darn/dang/darned ADJ`, tests H3)
```text
damn|darn|dang|darned|dratted|danged _j*
```

### G4 — Finite transitive curse-verb check for minced heads `[+KWIC 100]` (decisive H2 test)
```text
i|you|he|she|they|we dratted|danged|darned it|him|her|them|the|this|that
```
