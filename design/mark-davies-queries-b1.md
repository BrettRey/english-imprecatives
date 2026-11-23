# B1 Targeted TV Corpus Mini-Controls (Round 4 Follow-Up)

**Corpus:** The TV Corpus (325M words, `https://www.english-corpora.org/tv/`), LIST view (plus KWIC lines where noted).
**Goal:** Close four concrete empirical questions raised in Round-4 review (Claude #2/#3/#5, Codex #3/#7).

---

### `D1` — Particle-verb counterexample check (`fuck/screw PRON up for V-ing`)
- **Query:** `fuck|fucked|screw|screwed you|him|her|them|me up for _v?g*`
- **Paste back:** Frequency list + all KWIC lines (if any).
- **Why:** Tests whether particle-verb punishment/harm uses (*I'll fuck you up for touching her*) supply ordinary-verb `for V-ing` outside the subjectless frame (directly testing Claude #5).

---

### `D2a` & `D2b` — Productive bare-subjunctive passive dismissals (`X be darned/danged` vs. `damned/buggered`)
- **`D2a` Query:** `_n* be darned|danged`
- **`D2b` Query (matched baseline):** `_n* be damned|buggered`
- **Paste back:** Frequency lists + all KWIC lines for `D2a` (and top 100 freq / sample KWICs for `D2b` if large).
- **Why:** Directly tests productive nominal-subject `X be darned/danged!` dismissals across all 325M words instead of extrapolating from 12/103 displayed `F5a` lines (Claude #2, Codex #7).

---

### `D3` — Non-verbal `yay` / `boo` open lexical-NP check
- **Query:** `yay|boo the|this|that|my|your|his|her|their _n*`
- **Paste back:** Frequency list + KWIC lines (up to 100).
- **Why:** `C2b` showed non-verbal `yay me/you` and `boo me/him/her` take default accusative pronouns; `D3` tests whether they also take integrated determined/possessive lexical NPs or remain pronoun/cheering-restricted (Codex #3, Claude #3).

---

### `D4` — Non-taboo verbal head check (`confound`)
- **Query:** `confound it|you|him|her|them|me|the|this|that`
- **Paste back:** Frequency list + KWIC lines (up to 100).
- **Why:** Checks archaic non-taboo verbal recruitment (*Confound it!*, *Confound the rules!*) flagged by Claude #3 and Muse #8 without literal-verb swamping from *blow/bother*.
