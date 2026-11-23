# Spoken BNC2014 Queries — Sketch Engine CQL (`B2`)

**Corpus:** Spoken BNC2014 (~11.4M words of spontaneous UK conversation, 2012–2016) on **Sketch Engine** (`https://app.sketchengine.eu/`).
**Where to paste:** **Concordance → Advanced → Query type: `CQL`**

> **Quick tip in Sketch Engine:**
> - For large queries (`B2-1a`, `B2-3`), click the **Frequency** icon (top toolbar) $\to$ **Node forms** (or **KWIC**) to copy the full pair-by-pair frequency table in one click.
> - For small queries (`B2-2`, `B2-4a`, `B2-4b`, `B2-5a`, `B2-5b`, and low-frequency heads), copy-paste the concordance lines (or export `.txt`/`.csv`).
> - All queries below use Sketch Engine's lowercase attribute `lc` (case-insensitive). *(If Spoken BNC2014 uses `word` instead of `lc`, replace `lc="` with `word="(?i)` and add `)"` before the closing quote.)*

---

## `B2-1a` — Core 13 heads + NP starters (living vs. period-bound contemporary UK baseline)
```cql
[lc="damn|bless|fuck|sod|bugger|screw|blast|curse|hang|drat|darn|dash|dang"] [lc="it|you|him|her|them|me|us|this|that|these|those|the|my|your|his|their"]
```
- **Paste back:**
  1. Total hit count + **Frequency → KWIC** table (so we get every `HEAD + TARGET` pair count).
  2. Concordance lines for all low-frequency heads (`blast`, `curse`, `drat`, `darn`, `dash`, `dang`) and for `the|this|that|these|those|my|your|his|their` full-NP hits if small enough (or top 100).

## `B2-1b` — Univerbated `dammit` / `goddammit` *(1-second check)*
```cql
[lc="dammit|goddammit"]
```
- **Paste back:** Total hit count + Frequency → KWIC counts.

---

## `B2-2` — `fuck`-euphemisms in unscripted speech (tests TV censorship vs. spoken usage)
```cql
[lc="frak|feck|fudge|eff|frig|frick"] [lc="it|you|him|her|them|me|us|this|that|these|those|the|my|your|his|their"]
```
- **Paste back:** Frequency → KWIC table + **all concordance lines** (should be small!).

---

## `B2-3` — Overt `God` + core heads & `rot`
```cql
[lc="god"] [lc="damn|bless|curse|fuck|screw|sod|bugger|blast|darn|dang|drat|dash|rot"] [lc="it|you|him|her|them|me|us|this|that|the|my|your|his|her|their"]
```
- **Paste back:** Frequency → KWIC table (plus concordance lines for any non-`it`, non-`bless you` hits if small).

---

## `B2-4a` & `B2-4b` — `to hell` vs. `for V-ing` in unscripted speech

### `B2-4a` (`to hell`)
```cql
[lc="damn|bless|fuck|sod|bugger|screw|blast|curse|darn|dang|drat|dash|eff|frak"] [lc="it|you|him|her|them|me|us"] [lc="to"] [lc="hell"]
```

### `B2-4b` (`for V-ing`)
```cql
[lc="damn|bless|fuck|sod|bugger|screw|blast|curse|darn|dang|drat|dash|eff|frak"] [lc="you|him|her|them|me|us"] [lc="for"] [lc=".*ing"]
```
- **Paste back:** All concordance lines for both (should be very small — 100% auditable!).

---

## `B2-5a` & `B2-5b` — Non-taboo heads (`confound`, `stuff`) + `yay`/`boo` in unscripted speech

### `B2-5a` (`confound` & `stuff`)
```cql
[lc="confound|stuff"] [lc="it|this|that|you|him|her|them|the"]
```

### `B2-5b` (`yay`/`boo`)
```cql
[lc="yay|boo"] [lc="me|you|him|her|them|us|this|that|the|my|your"]
```
- **Paste back:** Frequency → KWIC table + concordance lines (or all lines if < 50).
