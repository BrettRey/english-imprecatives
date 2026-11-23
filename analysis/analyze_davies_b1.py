#!/usr/bin/env python3
"""Parse and audit B1 targeted TV Corpus controls (D1, D2a, D2b, D3, D4)."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "davies" / "davies-b1-2026-11-23-raw.txt"
OUT_JSON = ROOT / "data" / "davies" / "davies_b1_summary.json"
OUT_MD = ROOT / "analysis" / "davies-b1-results-summary.md"

text = RAW.read_text(encoding="utf-8")

def parse_sections(txt):
    blocks = re.split(r"^=== (D\d[ab]?): (.+?) ===$", txt, flags=re.M)
    out = {}
    for i in range(1, len(blocks), 3):
        qid, query, body = blocks[i], blocks[i+1], blocks[i+2]
        freq_rows = []
        kwic_rows = []
        mode = None
        for line in body.splitlines():
            s = line.strip()
            if not s:
                continue
            if s.startswith("FREQ"):
                mode = "freq"
                continue
            if s.startswith("KWIC"):
                mode = "kwic"
                continue
            if s.startswith("TOTAL"):
                continue
            parts = s.split("\t")
            if mode == "freq" and len(parts) >= 3:
                freq_rows.append((int(parts[0]), parts[1].strip(), int(parts[2])))
            elif mode == "kwic" and len(parts) >= 5:
                kwic_rows.append({
                    "id": int(parts[0]),
                    "year": int(parts[1]),
                    "variety": parts[2].strip(),
                    "show": parts[3].strip(),
                    "ctx": parts[4].strip(),
                })
        out[qid] = {"query": query, "freq": freq_rows, "kwic": kwic_rows}
    return out

data = parse_sections(text)

# --- D1: fuck|fucked|screw|screwed PRON up for _v?g* ---
d1_freq_sum = sum(c for _, _, c in data["D1"]["freq"])
assert d1_freq_sum == 3 and len(data["D1"]["kwic"]) == 3
d1_shows = sorted({r["show"] for r in data["D1"]["kwic"]})
d1_res = {
    "raw_tokens": d1_freq_sum,
    "kwic_audited": len(data["D1"]["kwic"]),
    "verified_particle_verb_retaliatory": 3,
    "distinct_shows": len(d1_shows),
    "shows": d1_shows,
    "items": [(r["show"], r["year"], r["ctx"]) for r in data["D1"]["kwic"]],
}

# --- D2a: _n* be darned|danged ---
d2a_freq_sum = sum(c for _, _, c in data["D2a"]["freq"])
assert d2a_freq_sum == 4 and len(data["D2a"]["kwic"]) == 4
# Manual line-level adjudication of all 4 D2a lines:
# Line 1: "Rules be darned, Richard." (Call Me Fitz, 2012) -> VERIFIED nominal passive dismissal (1)
# Line 2: "Well, I? ll be darned." (Everwood, 2002) -> EXCLUDED OCR-corrupted I'll be darned
# Line 3: "lll be darned." (Highway to Heaven, 1985) -> EXCLUDED OCR-corrupted I'll be darned
# Line 4: "lll be darned he showed up" (Highway to Heaven, 1984) -> EXCLUDED OCR-corrupted I'll be darned
d2a_codes = {1: "verified_nominal_dismissal", 2: "excl_ocr_ill", 3: "excl_ocr_ill", 4: "excl_ocr_ill"}
assert len(d2a_codes) == len(data["D2a"]["kwic"])
d2a_res = {
    "raw_tokens": d2a_freq_sum,
    "kwic_audited": len(data["D2a"]["kwic"]),
    "verified_nominal_dismissals": sum(1 for v in d2a_codes.values() if v == "verified_nominal_dismissal"),
    "verified_be_darned": 1,
    "verified_be_danged": 0,
    "excl_ocr_ill_be_darned": sum(1 for v in d2a_codes.values() if v == "excl_ocr_ill"),
}

# --- D2b: _n* be damned|buggered ---
d2b_freq_sum = sum(c for _, _, c in data["D2b"]["freq"])
assert d2b_freq_sum == 175 and len(data["D2b"]["freq"]) == 136 and len(data["D2b"]["kwic"]) == 100
d2b_ocr_types = {"I'IL BE DAMNED", "LL BE DAMNED"}
d2b_ocr_tokens = sum(c for _, s, c in data["D2b"]["freq"] if s in d2b_ocr_types)
assert d2b_ocr_tokens == 8
d2b_buggered_tokens = sum(c for _, s, c in data["D2b"]["freq"] if "BUGGERED" in s)
d2b_buggered_types = sum(1 for _, s, _ in data["D2b"]["freq"] if "BUGGERED" in s)
d2b_damned_non_ocr_tokens = d2b_freq_sum - d2b_ocr_tokens - d2b_buggered_tokens
d2b_damned_non_ocr_types = len(data["D2b"]["freq"]) - len(d2b_ocr_types) - d2b_buggered_types
assert d2b_buggered_tokens == 4 and d2b_buggered_types == 3  # ALMONDS(2), CLIMATE(1), SONY(1)

# Manual line-level audit of all 100 displayed D2b KWICs:
# Exclusions in D2b 100 KWICs:
#   OCR I'll / She'll / 'll be damned: lines 36, 74, 78, 81, 97 (5 lines)
#   Let X be damned / finite modal / literal theological / pun:
#     line 44: "Well, alva be damned." (pun on I'll be damned / name Alva -> borderline pun, code as pun_or_formula)
#     line 56: "Let Christoforo Castanea be damned for an eternity." (let-optative)
#     line 58: "Let Christoforo Castanea be damned." (let-optative)
#     line 76: "We'll not let any brother be damned by this dirty mob." (literal finite let-passive)
#     line 86: "let the r est of the world be damned" (let-optative dismissal)
#     line 90: "and that brains be damned" (subordinate subjunctive dismissal)
#     line 92: "Let the regulations be damned." (let-optative dismissal)
# All remaining 88 lines are direct bare-subjunctive passive dismissals (X be damned/buggered)!
d2b_non_bare = {
    36: "excl_ocr_ill", 74: "excl_ocr_ill", 78: "excl_ocr_shell", 81: "excl_ocr_ill", 97: "excl_ocr_ll",
    56: "let_optative_theological", 58: "let_optative_theological",
    76: "excl_literal_let_passive",
    86: "let_dismissal", 90: "subordinate_that_dismissal", 92: "let_dismissal",
    44: "wordplay_pun",
}
d2b_bare_kwic = [r for r in data["D2b"]["kwic"] if r["id"] not in d2b_non_bare]
assert len(d2b_bare_kwic) + len(d2b_non_bare) == 100
d2b_bare_shows = sorted({r["show"] for r in d2b_bare_kwic})
d2b_bare_buggered = [r for r in d2b_bare_kwic if "buggered" in r["ctx"].lower()]
d2b_res = {
    "raw_tokens": d2b_freq_sum,
    "raw_types": len(data["D2b"]["freq"]),
    "ocr_tokens_in_freq": d2b_ocr_tokens,
    "non_ocr_tokens_in_freq": d2b_freq_sum - d2b_ocr_tokens,
    "non_ocr_types_in_freq": len(data["D2b"]["freq"]) - len(d2b_ocr_types),
    "damned_non_ocr_tokens": d2b_damned_non_ocr_tokens,
    "damned_non_ocr_types": d2b_damned_non_ocr_types,
    "buggered_tokens": d2b_buggered_tokens,
    "buggered_types": d2b_buggered_types,
    "kwic_audited": 100,
    "kwic_direct_bare_dismissals": len(d2b_bare_kwic),
    "kwic_direct_bare_buggered": len(d2b_bare_buggered),
    "kwic_distinct_shows_bare": len(d2b_bare_shows),
    "kwic_non_bare_breakdown": dict(Counter(d2b_non_bare.values())),
}

# --- D3: yay|boo + DET/POSS _n* ---
d3_freq_sum = sum(c for _, _, c in data["D3"]["freq"])
assert d3_freq_sum == 13 and len(data["D3"]["kwic"]) == 13
d3_codes = {
    1: "excl_slang_boo_boo_the_fool",
    2: "excl_slang_boo_boo_the_fool",
    3: "excl_transitive_verb_boo",
    4: "excl_imperative_verb_boo",
    5: "excl_slang_boo_boo_the_fool",
    6: "excl_chant_refrain_boo",
    7: "excl_transitive_verb_boo",
    8: "excl_transitive_verb_boo",
    9: "excl_proper_or_petname_boo",
    10: "excl_imperative_verb_boo",
    11: "excl_proper_name_boo_dbz",
    12: "excl_misspelled_yea_vocative",
    13: "excl_imperative_verb_boo",
}
assert len(d3_codes) == 13
d3_res = {
    "raw_tokens": d3_freq_sum,
    "kwic_audited": 13,
    "verified_subjectless_expressive_np": 0,
    "exclusion_breakdown": dict(Counter(d3_codes.values())),
}

# --- D4: confound + PRON/DET ---
d4_freq_sum = sum(c for _, _, c in data["D4"]["freq"])
assert d4_freq_sum == 122 and len(data["D4"]["kwic"]) == 100
# Manual line-level audit of all 100 D4 KWIC lines:
# Ordinary literal/finite/infinitival/imperative verb 'confound' (= confuse/defeat/mix up):
d4_literal_ids = {
    1,  # Your lust will confound you
    3,  # could also confound the mind uploaders
    4,  # George, you confound me sometimes
    6,  # I'll confound you
    7,  # Mortal laws confound me
    8,  # I would confound this pope
    10, # I would confound this pope
    11, # to confound the other kings
    12, # When life's perils thick confound you (hymn)
    14, # Confound her with legal jargon. Go on. (imperative 'confuse')
    15, # seems to confound the media
    16, # You speak to confound me
    17, # purpose to confound you
    18, # to confound her by treating her with kindness
    19, # very few mysteries will confound you
    20, # Come to condemn the wretches or confound the jury today?
    21, # Shakespeare Hamlet quote: 'Confound the ignorant'
    23, # How to confound the blue with the yellow
    52, # Well, you confound me some, is all
    65, # just to confound the white man
    73, # I SHALL CONFOUND YOU WITH QUADRATIC IMPONDERABLES
    76, # to confound me with the official detective force
    81, # The prospect does not confound me
    89, # I'm going to confound them with conundrums
    94, # sometimes that man does confound me
}
d4_imprec_kwic = [r for r in data["D4"]["kwic"] if r["id"] not in d4_literal_ids]
assert len(d4_imprec_kwic) + len(d4_literal_ids) == 100

def classify_d4_target(ctx):
    m = re.search(r"\bconfound\s+(it|you|him|her|them|me|the|this|that)\b", ctx, re.I)
    if not m:
        return "other"
    w = m.group(1).lower()
    if w == "it":
        return "it"
    if w == "you":
        return "you"
    if w in {"him", "her", "them", "me"}:
        return "acc_pron"
    return "full_np"

d4_targets = Counter(classify_d4_target(r["ctx"]) for r in d4_imprec_kwic)
d4_shows = Counter(r["show"] for r in d4_imprec_kwic)
d4_full_np_lines = [r for r in d4_imprec_kwic if classify_d4_target(r["ctx"]) == "full_np"]
d4_res = {
    "raw_tokens": d4_freq_sum,
    "kwic_audited": 100,
    "verified_imprecative": len(d4_imprec_kwic),
    "excl_literal_verb": len(d4_literal_ids),
    "verified_target_breakdown": dict(d4_targets),
    "distinct_shows_verified": len(d4_shows),
    "nero_wolfe_tokens": d4_shows["A Nero Wolfe Mystery"],
    "top_shows": d4_shows.most_common(8),
    "full_np_examples": [(r["show"], r["year"], r["variety"], r["ctx"]) for r in d4_full_np_lines],
}

summary = {"D1": d1_res, "D2a": d2a_res, "D2b": d2b_res, "D3": d3_res, "D4": d4_res}
OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

md_lines = [
    "# B1 Targeted TV Corpus Controls Summary (2026-11-23)",
    "",
    f"- **D1 (`fuck|fucked|screw|screwed PRON up for _v?g*`)**: {d1_res['raw_tokens']} raw / {d1_res['verified_particle_verb_retaliatory']} verified retaliatory particle-verb tokens across {d1_res['distinct_shows']} shows (*Survivor's Remorse*, *United States of Tara*, *Crash*). Contrasts with 0 bare-transitive hits (`C1a`) and joins 1 `screw over` (`C1b`).",
    f"- **D2a (`_n* be darned|danged`)**: {d2a_res['raw_tokens']} raw / **{d2a_res['verified_nominal_dismissals']} verified nominal bare-subjunctive dismissal** (*Rules be darned, Richard.*, *Call Me Fitz*, 2012; 0 `be danged`) + {d2a_res['excl_ocr_ill_be_darned']} OCR-corrupted `I'll be darned`.",
    f"- **D2b (`_n* be damned|buggered`)**: {d2b_res['raw_tokens']} raw tokens across {d2b_res['raw_types']} types ({d2b_res['non_ocr_tokens_in_freq']} non-OCR tokens across {d2b_res['non_ocr_types_in_freq']} noun types: {d2b_res['damned_non_ocr_tokens']} `damned` / {d2b_res['damned_non_ocr_types']} types + {d2b_res['buggered_tokens']} `buggered` / {d2b_res['buggered_types']} types). In 100 audited KWICs: **{d2b_res['kwic_direct_bare_dismissals']}/100 direct bare-subjunctive dismissals** across {d2b_res['kwic_distinct_shows_bare']} shows ({d2b_res['kwic_direct_bare_buggered']} `buggered`).",
    f"- **D3 (`yay|boo + DET/POSS _n*`)**: {d3_res['raw_tokens']} raw / **0/13 verified subjectless non-verbal lexical-NP complements** (3 transitive verb `boo`, 3 imperative verb `boo`, 3 slang `Boo Boo the Fool`, 2 proper-name `Boo`, 1 chant refrain, 1 misspelled vocative *Yay my children* = *Yea*).",
    f"- **D4 (`confound + PRON/DET`)**: {d4_res['raw_tokens']} raw / **{d4_res['verified_imprecative']}/100 verified subjectless imprecatives** across {d4_res['distinct_shows_verified']} shows ({d4_res['excl_literal_verb']}/100 literal verb). Targets: `it` {d4_targets['it']}, `full_np` {d4_targets['full_np']}, `you` {d4_targets['you']}, `acc_pron` {d4_targets['acc_pron']}. Heavy period-drama/franchise skew: *A Nero Wolfe Mystery* alone supplies **{d4_res['nero_wolfe_tokens']}/{d4_res['verified_imprecative']} ({100*d4_res['nero_wolfe_tokens']/d4_res['verified_imprecative']:.1f}%)** of verified KWICs.",
    "",
    "### D4 Verified Full-NP Examples (n=" + str(len(d4_full_np_lines)) + ")",
]
for show, yr, var, ctx in d4_res["full_np_examples"]:
    md_lines.append(f"- ({yr}, {var}, *{show}*): `{ctx}`")

OUT_MD.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
print("ALL B1 ASSERTIONS PASSED")
print("\n".join(md_lines))
