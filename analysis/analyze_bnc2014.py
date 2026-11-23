#!/usr/bin/env python3
"""Parse and audit Sketch Engine Spoken BNC2014 (B2) exports."""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "bnc2014" / "raw"
OUT_JSON = ROOT / "data" / "bnc2014" / "bnc2014_summary.json"
OUT_MD = ROOT / "analysis" / "bnc2014-results-summary.md"

def load_csv(fname):
    with (RAW / fname).open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.reader(fh))
    meta = {r[0].strip(): r[1].strip() for r in rows[:4] if len(r) >= 2}
    return meta, rows[5:]

# 1. Core 13 heads full frequency breakdown (B2-1a) + dammit (B2-1b)
m_core, r_core = load_csv("frequency_preloaded_bnc2014_spoken_tt3_20261123143251.csv")
core_total = int(m_core["concordance size"])
core_by_head = Counter()
core_pairs = Counter()
for w, freq, ipm, pct in r_core:
    f = int(freq)
    pair = w.strip().lower()
    head = pair.split()[0]
    core_by_head[head] += f
    core_pairs[pair] += f
assert sum(core_by_head.values()) == core_total == 1311

# Infer corpus size from singleton ipm (1 / 0.08451 * 1e6)
singleton_ipms = [float(ipm) for _, freq, ipm, _ in r_core if int(freq) == 1]
est_corpus_words = round(1_000_000 / singleton_ipms[0])  # ~11,832,919 tokens in Sketch Engine tt3

m_dammit, r_dammit = load_csv("frequency_preloaded_bnc2014_spoken_tt3_20261123143640.csv")
dammit_total = sum(int(r[1]) for r in r_dammit)
assert dammit_total == int(m_dammit["concordance size"]) == 12

# 2. All 22 low-frequency/archaic/minced hits (blast|curse|drat|darn|dash|dang)
m_low, r_low = load_csv("concordance_preloaded_bnc2014_spoken_tt3_20261123143454.csv")
assert len(r_low) == int(m_low["concordance size"]) == 22
# Manual line-level adjudication (1-indexed):
low_codes = {
    1: ("darn", "excl_literal_mending"),        # darn these socks
    2: ("blast", "excl_literal_verb"),          # try and blast them
    3: ("blast", "excl_literal_verb"),          # blast it up a little bit
    4: ("dash", "excl_literal_verb"),           # dash them down
    5: ("blast", "excl_literal_verb"),          # blast them off again
    6: ("curse", "excl_finite_verb"),           # I still curse them
    7: ("blast", "excl_literal_verb"),          # have to blast it
    8: ("blast", "excl_literal_verb"),          # gotta blast it at high speed
    9: ("blast", "excl_literal_verb"),          # gotta blast them anyway
    10: ("blast", "excl_literal_verb"),         # gotta blast the pipe
    11: ("blast", "excl_literal_verb"),         # gotta blast it to check
    12: ("curse", "excl_finite_verb"),          # have to curse you
    13: ("blast", "excl_literal_verb"),         # just like blast it (paint)
    14: ("dash", "verified_it"),                # dash it all (SF3V)
    15: ("curse", "verified_full_np"),          # curse the world (SLDD)
    16: ("darn", "verified_it"),                # darn it (SLT4)
    17: ("darn", "verified_it"),                # darn it (SLT4)
    18: ("blast", "excl_literal_verb"),         # blast it with like pulses
    19: ("curse", "excl_finite_verb"),          # gonna curse him
    20: ("blast", "excl_literal_verb"),         # have to blast it to clean
    21: ("blast", "excl_literal_verb"),         # blast them in the pan
    22: ("blast", "excl_literal_verb"),         # want me to blast him
}
assert len(low_codes) == 22
low_summary = defaultdict(lambda: Counter())
for idx, (h, code) in low_codes.items():
    assert r_low[idx - 1][2].lower().startswith(h)
    low_summary[h][code] += 1

# 3. 100-line DET/POSS sample (out of 237 raw hits)
m_det, r_det = load_csv("concordance_preloaded_bnc2014_spoken_tt3_20261123143616.csv")
assert int(m_det["concordance size"]) == 237 and len(r_det) == 100
det_codes = {
    1: "excl_literal_verb",         # darn these socks
    2: "verified_poss_body",        # bless his heart
    3: "excl_standalone_clause",    # fuck! that would last me
    4: "verified_dem",              # right bugger this
    5: "verified_dem",              # bugger that
    6: "verified_dem",              # bugger that I'll just nip
    7: "excl_standalone_clause",    # bugger! that's what I am seeing
    8: "verified_dem",              # fuck that I'm gonna get them
    9: "verified_dem",              # screw that
    10: "excl_finite_literal",      # you fuck your uncle (South Park song)
    11: "excl_literal_verb",        # help me hang the studio
    12: "excl_literal_verb",        # used to fuck the wifi up
    13: "verified_dem",             # fuck that, that's what he said
    14: "verified_dem",             # yeah but fuck that
    15: "verified_full_np",         # Fuck this boat club, so disorganised
    16: "excl_literal_verb",        # hang the bell on
    17: "verified_dem",             # fucking fuck that
    18: "excl_standalone_clause",   # fuck! that's the whole premise
    19: "excl_literal_verb",        # hang my jewellery on
    20: "excl_literal_verb",        # you fuck your back up
    21: "excl_standalone_clause",   # fuck! my legs are burning
    22: "verified_dem",             # I was like fuck that
    23: "excl_literal_verb",        # better screw that in first
    24: "verified_dem",             # I'm not going in there, fuck that
    25: "excl_literal_verb",        # hang your coat up
    26: "excl_literal_verb",        # screw the butterfly on
    27: "excl_wh_the_fuck",         # dunno what the fuck that means
    28: "verified_poss_body",       # bless his cotton socks
    29: "excl_wh_the_fuck",         # the fuck the fuck that's weird
    30: "excl_standalone_clause",   # the fuck! that's weird
    31: "verified_poss_fml",        # fuck my life
    32: "verified_full_np",         # fuck those people
    33: "excl_literal_verb",        # hang that up somewhere
    34: "excl_as_fuck",             # creepy as fuck, this sounds like
    35: "excl_literal_verb",        # like fuck my whore wife
    36: "excl_literal_verb",        # going to fuck my whore wife
    37: "excl_wh_the_fuck",         # what the fuck that?
    38: "verified_full_np_quoted",  # it just says fuck the world (T-shirt quote)
    39: "verified_dem",             # no no fuck that
    40: "verified_poss_fml",        # fuck my life
    41: "excl_literal_verb",        # fuck their body up
    42: "excl_standalone_clause",   # oh fuck! that's not what happens
    43: "excl_literal_verb",        # did you fuck that shit up?
    44: "excl_wh_the_fuck",         # what the fuck that means
    45: "excl_literal_verb",        # hang your laundry up
    46: "verified_poss_fml",        # ah fuck my life
    47: "verified_poss_fml",        # oh fuck my life
    48: "verified_poss_fml",        # fuck my life
    49: "verified_poss_fml",        # oh fuck my life
    50: "verified_poss_fml",        # fuck my life
    51: "verified_dem",             # yeah yeah fuck that
    52: "excl_wh_the_fuck",         # what the fuck these fuckers are doing
    53: "excl_literal_verb",        # go home and fuck your mother
    54: "verified_poss_fml",        # oh fuck my life
    55: "excl_literal_verb",        # screw this fast (hardware)
    56: "excl_standalone_fragment", # damn! that well-known horse oil (sarcastic)
    57: "verified_dem",             # I was like fuck that
    58: "verified_dem",             # could it be Japan? fuck that
    59: "verified_dem",             # yeah fuck that
    60: "excl_literal_verb",        # hang your boots up
    61: "excl_standalone_clause",   # fuck! my question is
    62: "excl_literal_verb",        # hang the washing out
    63: "excl_literal_verb",        # hang that from a hook
    64: "verified_dem",             # fuck that (or ambiguous standalone; keep dem)
    65: "verified_dem",             # do you know what? Fuck this
    66: "verified_dem",             # no fuck that I'm not doing that
    67: "excl_as_fuck",             # guilty as fuck, that's what I said
    68: "verified_dem",             # it's a bit like oh fuck that
    69: "verified_full_np",         # damn those vampires
    70: "verified_dem",             # fuck that what a bitch
    71: "verified_dem",             # fuck that
    72: "verified_full_np",         # damn those apples
    73: "verified_dem",             # oh bugger that I'm going to go
    74: "verified_dem",             # oh fuck that why does it do that
    75: "verified_dem",             # I just thought fuck that
    76: "verified_dem",             # no fuck that
    77: "verified_dem",             # thought sod this for a lark
    78: "excl_noun_screw",          # just get a screw, that'll finish
    79: "excl_literal_verb",        # screw that to the wall
    80: "excl_wh_the_fuck",         # what the fuck that is
    81: "excl_wh_the_fuck",         # what the fuck the things are like
    82: "verified_dem",             # I'm just like fuck this
    83: "verified_dem",             # I go oh fuck that
    84: "verified_dem",             # I'm not weeding, fuck that
    85: "verified_dem",             # I said ooh sod that
    86: "excl_literal_verb",        # hang this on
    87: "excl_literal_verb",        # blast the pipe
    88: "excl_as_fuck",             # disrespectful as fuck that she was wasted
    89: "excl_literal_verb",        # cold'd screw your skin up
    90: "excl_standalone_clause",   # fuck! that's really low
    91: "excl_standalone_clause",   # damn! the starter's over
    92: "excl_literal_verb",        # gonna screw the copyright
    93: "excl_literal_verb",        # gonna screw the recording
    94: "verified_dem",             # yeah fuck that
    95: "verified_full_np",         # bless that poor girl who was acting
    96: "excl_standalone_clause",   # oh bless! that's really sweet
    97: "excl_standalone_clause",   # fuck! that's a good car
    98: "verified_dem",             # fuck that no way
    99: "excl_standalone_clause",   # damn! that's good television
    100: "verified_poss_fml",       # fuck my life
}
assert len(det_codes) == 100
det_counts = Counter(det_codes.values())
det_verified_total = sum(v for k, v in det_counts.items() if k.startswith("verified_") and k != "verified_full_np_quoted")

# 4. fuck-euphemisms (B2-2, ALL 11 audited)
m_euph, r_euph = load_csv("concordance_preloaded_bnc2014_spoken_tt3_20261123143710.csv")
assert len(r_euph) == int(m_euph["concordance size"]) == 11
euph_codes = {
    1: "excl_literal_noun_fudge",     # two thirds of the fudge, it's one of us
    2: "excl_literal_verb_fudge",     # meant to fudge the numbers
    3: "excl_standalone_frig_clause", # Monday frig! it's only Monday
    4: "excl_literal_noun_fudge",     # it's not fudge, it's crumbly
    5: "excl_literal_noun_fudge",     # fudge, that's for
    6: "excl_literal_noun_fudge",     # fudgish fudge, it's a fudgy fudge
    7: "excl_literal_noun_fudge",     # not a fudgy fudge, it's a tablet
    8: "excl_literal_noun_fudge",     # the fudge fudge, the fudgy fudge
    9: "excl_literal_noun_fudge",     # same as fudge, it's just the temp
    10: "excl_literal_verb_fudge",    # fudge the date on it
    11: "excl_wh_the_frig",           # what the frig the Gestapo was
}
assert len(euph_codes) == 11

# 5. Overt God + HEAD + NP (B2-3: 17 raw total, 7 non-it audited)
m_god_f, r_god_f = load_csv("frequency_preloaded_bnc2014_spoken_tt3_20261123143743.csv")
god_freq_sum = sum(int(r[1]) for r in r_god_f)
assert god_freq_sum == int(m_god_f["concordance size"]) == 17
m_god_c, r_god_c = load_csv("concordance_preloaded_bnc2014_spoken_tt3_20261123143854.csv")
assert len(r_god_c) == int(m_god_c["concordance size"]) == 7
god_non_it_codes = {
    1: "verified_god_bless",            # god bless him (S6ZU)
    2: "excl_oh_my_god_plus_fuck_you",  # oh my god! fuck you (S985)
    3: "verified_god_bless",            # god bless them (SA9T)
    4: "verified_god_bless",            # my god bless him -> wait: "now my god bless him" (SMKK)
    5: "verified_god_bless",            # god bless us one and all (SR5H)
    6: "excl_oh_god_plus_fuck_that",    # oh god! fuck that (STH5)
    7: "verified_god_bless",            # oh god bless him (STMM)
}
assert len(god_non_it_codes) == 7

# 6. to hell (B2-4a) & for V-ing (B2-4b)
m_th, r_th = load_csv("concordance_preloaded_bnc2014_spoken_tt3_20261123143928.csv")
assert len(r_th) == int(m_th["concordance size"]) == 1  # damn it to hell (SAZX)
m_fv, r_fv = load_csv("concordance_preloaded_bnc2014_spoken_tt3_20261123143947.csv")
assert len(r_fv) == int(m_fv["concordance size"]) == 3  # bless him for carrying, damn you for being, bless him for coming

# 7. confound (B2-5a) & yay/boo (B2-5b)
m_conf, r_conf = load_csv("concordance_preloaded_bnc2014_spoken_tt3_20261123144249.csv")
assert len(r_conf) == int(m_conf["concordance size"]) == 1  # oh confound it (SA9P)

m_yb, r_yb = load_csv("concordance_preloaded_bnc2014_spoken_tt3_20261123144058.csv")
assert len(r_yb) == int(m_yb["concordance size"]) == 17
yb_codes = {
    1: "excl_clause", 2: "excl_detached_np", 3: "excl_clause", 4: "excl_clause",
    5: "excl_clause", 6: "excl_detached_np", 7: "excl_clause", 8: "excl_clause",
    9: "excl_clause", 10: "excl_clause", 11: "excl_clause", 12: "excl_clause",
    13: "excl_clause", 14: "excl_clause", 15: "excl_clause", 16: "excl_clause",
    17: "excl_detached_np",
}
assert len(yb_codes) == 17

summary = {
    "corpus": "Spoken BNC2014 (Sketch Engine preloaded/bnc2014_spoken_tt3)",
    "est_tokens": est_corpus_words,
    "B2_1a_raw_total": core_total,
    "B2_1a_by_head": dict(core_by_head.most_common()),
    "B2_1a_key_pairs": {k: core_pairs[k] for k in ["bless her", "bless him", "damn it", "fuck it", "fuck you", "bless you", "fuck that", "fuck me", "bugger me", "sod it", "screw it"] if k in core_pairs},
    "B2_1b_dammit": dammit_total,
    "B2_1a_low_freq_22_audited": {h: dict(c) for h, c in low_summary.items()},
    "B2_1a_det_poss_100_audited": dict(det_counts),
    "B2_1a_det_poss_verified_excl_quote": det_verified_total,
    "B2_2_euphemisms_11_audited": {"raw": 11, "verified_subjectless": 0, "breakdown": dict(Counter(euph_codes.values()))},
    "B2_3_god_17": {"raw": 17, "god_damn_it": 10, "god_bless_non_it": 5, "excl_oh_god_plus_fuck": 2, "verified_theological": 15, "verified_secular": 0},
    "B2_4a_to_hell": {"raw": 1, "verified": 1, "head": "damn", "text_id": "SAZX"},
    "B2_4b_for_ving": {"raw": 3, "verified": 3, "heads": {"bless": 2, "damn": 1}, "text_ids": ["S96L", "SD92", "SXEV"]},
    "B2_5a_confound": {"raw": 1, "verified": 1, "item": "confound it", "text_id": "SA9P"},
    "B2_5b_yay_boo": {"raw": 17, "verified_subjectless_complement": 0, "breakdown": dict(Counter(yb_codes.values()))},
}
OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

md = [
    "# Spoken BNC2014 (B2) Audit Summary (2026-11-23)",
    "",
    f"- **Corpus:** Spoken BNC2014 (Sketch Engine `preloaded/bnc2014_spoken_tt3`, ~{est_corpus_words:,} tokens of spontaneous UK conversation, 2012--2016).",
    f"- **B2-1a Core 13 heads (`N = {core_total}` raw + `12` `dammit`):** `bless` {core_by_head['bless']}, `fuck` {core_by_head['fuck']} (incl. **`fuck me` {core_pairs['fuck me']}**), `damn` {core_by_head['damn']} (+ 12 `dammit`), `hang` {core_by_head['hang']} (literal), `screw` {core_by_head['screw']}, `sod` {core_by_head['sod']}, `bugger` {core_by_head['bugger']} (incl. **`bugger me` {core_pairs['bugger me']}**), `blast` {core_by_head['blast']}, `curse` {core_by_head['curse']}, `darn` {core_by_head['darn']}, `dash` {core_by_head['dash']}, `drat` 0, `dang` 0.",
    f"- **All 22/22 low-frequency/archaic/minced hits audited (`blast/curse/drat/darn/dash/dang`):** `blast` **0/13** (all literal), `curse` **1/4** (*curse the world*, `SLDD`), `darn` **2/3** (*darn it* x2 in `SLT4`; 1 literal *darn these socks*, `S23A`), `dash` **1/2** (*dash it all*, `SF3V`), `drat` **0**, `dang` **0**.",
    f"- **DET/POSS 100/237 audited sample:** **{det_verified_total}/100** direct verified subjectless tokens (+ {det_counts['verified_full_np_quoted']} quoted *fuck the world*): {det_counts['verified_dem']} demonstratives (`fuck that/this`, `bugger that/this`, `sod that/this`, `screw that`), {det_counts['verified_poss_fml']} `fuck my life`, {det_counts['verified_poss_body']} `bless his heart/cotton socks`, and **{det_counts['verified_full_np']} open full NPs** (*Fuck this boat club*, *fuck those people*, *damn those vampires*, *damn those apples*, *bless that poor girl who was acting*).",
    "- **B2-2 `fuck`-euphemisms (`frak/feck/fudge/eff/frig/frick`, ALL 11/11 audited):** **0/11 verified subjectless NP imprecatives** (`frak` 0, `feck` 0, `eff` 0, `frick` 0; 9 literal noun/verb `fudge`; 2 non-imprecative `frig`: *Monday frig it's only Monday*, *what the frig the Gestapo was*).",
    "- **B2-3 Overt `God + HEAD + NP` (ALL 17 raw / 7 non-`it` audited):** **15/15 verified `God`-optatives are theological** (`god damn it` 10, `god bless him/them/us` 5) and **0 secular** — both `god fuck` hits are standalone *oh (my) God!* exclamations (*oh my god, fuck you* `S985`; *oh god, fuck that* `STH5`).",
    "- **B2-4a (`to hell`) vs. B2-4b (`for V-ing`):** 1/1 *damn it to hell* (`SAZX`) vs. 3/3 *for V-ing* across 3 files (*bless him for carrying* `S96L`, *damn you for being busy* `SD92`, *bless him for coming on TV* `SXEV`).",
    "- **B2-5a (`confound`):** **1/1** verified token (*oh confound it*, `SA9P`), confirming `confound` is virtually absent in contemporary unscripted British conversation.",
    "- **B2-5b (`yay/boo`, ALL 17/17 audited):** **0/17 verified subjectless NP complements** (0 accusative pronouns; 14 standalone exclamations before finite clauses, 3 detached echoic NP fragments).",
]
OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
print("ALL BNC2014 ASSERTIONS PASSED")
print("\n".join(md))
