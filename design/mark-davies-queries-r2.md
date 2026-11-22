# Mark Davies TV Corpus Follow-Up Queries (Round 2 — Path B)

**Corpus:** TV Corpus (`https://www.english-corpora.org/tv/`, 325M words — KWIC contexts work on all queries!).
**Mode:** `LIST` (copy the frequency table + up to 100 KWIC lines where noted; for `F5a` just the frequency table is enough).
**Save output to:** `/Users/brettreynolds/projects/LLM-CLI-projects/papers/queue/english-imprecatives/data/davies/tv-r2-followup.txt` (avoids the chat paste size limit!) or paste in 1–2 short chat messages.

---

### F1a — Direct-NP non-verbal evaluative heads + `for V-ing` (tests Reversal Condition a)
```text
silly|lucky|poor|yay|boo you|me|him|her|them for _v?g*
```
*(LIST + KWIC up to 100)*

### F1b — PP-target evaluative formulae + `for V-ing` (general evaluative reason-adjunct control)
```text
shame|good|kudos on|for|to you|me|him|her|them for _v?g*
```
*(LIST + KWIC up to 100)*

### F2 — Lexical NPs (animate vs. inanimate dismissal test) + `for V-ing` (tests Reversal Condition b)
```text
damn|fuck|screw|sod|bugger|bless|curse|darn|dang the|this|that|my|your|his|her _n* for _v?g*
```
*(LIST + KWIC up to 100)*

### F3 — *Fuck*-euphemisms inside `[X NP]` (tests H3 beyond *damn*)
```text
frig|frick|feck|fudge|frak|eff it|you|him|her|them|me|the|this|that
```
*(LIST + KWIC up to 100)*

### F4a — Local *God*-ellipsis test on *bless* + lexical NP (compare with `T4/T5` bare *bless*)
```text
god bless the|this|that|my|your|his|her|their _n*
```
*(LIST + KWIC 100)*

### F4b — Minced *God*-optatives (`gosh darn`, `gol dang`, `God rot`)
```text
gosh|gol|gold|dog|god darn|dang|rot|drat it|you|him|her|them|me
```
*(LIST + KWIC 100)*

### F5a — Defective-verb participial cells (`be darned/danged/dratted/buggered/damned`)
```text
be darned|danged|dratted|buggered|damned
```
*(LIST frequency table only)*

### F5b — Positive-controlled finite/infinitival baseline (*damn/curse* vs. *darn/dang/drat*, incl. `I`)
```text
he|she|they|i|will|would|could|to damn|damns|damned|curse|curses|cursed|darn|darns|darned|dang|dangs|danged|drat|drats|dratted him|her|them
```
*(LIST + KWIC up to 100)*

### F5c — Audit TV Corpus `dash it` in context (resolves *dash* status)
```text
dash it
```
*(KWIC all 65 rows)*
