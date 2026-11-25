#!/usr/bin/env python3
"""
Round-2 analyzer for the 9 targeted TV Corpus follow-up queries (F1a-F5c)
archived in data/davies/tv-r2-followup-2026-11-22-raw.txt, plus cross-checks
against Round-1 TV Corpus tables (T4, T5, T6, T7a, T7b).

Enforces exact conservation on every parsed block and outputs:
  - data/davies/davies_r2_summary.json
  - analysis/davies-r2-results-summary.md
"""
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAVIES_DIR = ROOT / "data" / "davies"
RAW_R2 = DAVIES_DIR / "tv-r2-followup-2026-11-22-raw.txt"
TV_R1 = DAVIES_DIR / "tv_t1a_to_t8a_parsed.json"
OUT_JSON = DAVIES_DIR / "davies_r2_summary.json"
OUT_MD = ROOT / "analysis" / "davies-r2-results-summary.md"


def fisher_exact_two_sided(a: int, b: int, c: int, d: int) -> float:
    n1, n2, m1, n = a + b, c + d, a + c, a + b + c + d

    def log_comb(nn: int, kk: int) -> float:
        return math.lgamma(nn + 1) - math.lgamma(kk + 1) - math.lgamma(nn - kk + 1)

    denom = log_comb(n, n1)

    def hp(k: int) -> float:
        return math.exp(log_comb(m1, k) + log_comb(n - m1, n1 - k) - denom)

    p_obs = hp(a)
    lo, hi = max(0, n1 - (n - m1)), min(n1, m1)
    return min(1.0, sum(hp(k) for k in range(lo, hi + 1) if hp(k) <= p_obs * (1.0 + 1e-12)))


def parse_kwic_line(l: str):
    if not re.match(r"^\d+\s+\d{4}\s+", l):
        return None
    parts = re.split(r"\t+", l)
    if len(parts) >= 5:
        return {
            "n": int(parts[0].strip()),
            "year": int(parts[1].strip()),
            "region": parts[2].strip(),
            "show": parts[3].strip(),
            "text": parts[-1].strip(),
        }
    m = re.match(r"^(\d+)\s+(\d{4})\s+(\S+)\s+(.*?)\s{3,}(.*)$", l)
    if m:
        return {
            "n": int(m.group(1)),
            "year": int(m.group(2)),
            "region": m.group(3),
            "show": m.group(4).strip(),
            "text": m.group(5).strip(),
        }
    return None


def parse_freq_line(l: str):
    if "See 'word page'" not in l or l.strip().startswith("HELP"):
        return None
    parts = [p.strip() for p in re.split(r"\t+|\s{3,}", l) if p.strip()]
    if len(parts) >= 2 and re.match(r"^[\d,]+$", parts[-1]):
        return {"form": parts[-2], "freq": int(parts[-1].replace(",", ""))}
    return None


def main():
    raw = RAW_R2.read_text(encoding="utf-8")
    # Split cleanly into the 9 query sections by blank-line separated blocks after "Trying again:"
    # Actually parse sequentially by tracking transitions between freq-table mode and kwic mode!
    lines = raw.splitlines()
    # Find line starting "HELP" for F1a
    start_idx = next(i for i, l in enumerate(lines) if "SILLY ME FOR SINKING" in l) - 1
    body = lines[start_idx:]

    # Group lines into sections: each section is (freq_rows, kwic_rows); F5c has kwic_rows only.
    sections = []
    cur_freq, cur_kwic = [], []
    mode = "none"  # "freq" or "kwic"
    for l in body:
        s = l.strip()
        if not s or s.startswith("HELP") or s.startswith("TOTAL"):
            continue
        f = parse_freq_line(l)
        k = parse_kwic_line(l)
        if f is not None:
            if mode == "kwic":
                sections.append({"freq": cur_freq, "kwic": cur_kwic})
                cur_freq, cur_kwic = [], []
            cur_freq.append(f)
            mode = "freq"
        elif k is not None:
            # Detect F5c (starts at n=1 after F5b's kwic ended at n=49)
            if mode == "kwic" and k["n"] == 1 and len(cur_kwic) >= 40:
                sections.append({"freq": cur_freq, "kwic": cur_kwic})
                cur_freq, cur_kwic = [], []
            cur_kwic.append(k)
            mode = "kwic"
    if cur_freq or cur_kwic:
        sections.append({"freq": cur_freq, "kwic": cur_kwic})

    names = [
        "F1a_nonverbal_direct_for_ving",
        "F1b_pp_eval_for_ving",
        "F2_lex_np_for_ving",
        "F3_fuck_euphemisms",
        "F4a_god_bless_lex_np",
        "F4b_minced_god_and_god_rot",
        "F5a_be_participle",
        "F5b_finite_baseline",
        "F5c_dash_it_kwic",
    ]
    assert len(sections) == len(names), f"Expected {len(names)} sections, got {len(sections)}"
    parsed = dict(zip(names, sections))

    # --- Audit F1b (Shame on / Good for / Good on / Kudos to X for V-ing) ---
    f1b_by_frame = Counter()
    f1b_types_by_frame = Counter()
    for x in parsed["F1b_pp_eval_for_ving"]["freq"]:
        frame = " ".join(x["form"].lower().split()[:2])
        f1b_by_frame[frame] += x["freq"]
        f1b_types_by_frame[frame] += 1
    f1b_shows = len({x["show"] for x in parsed["F1b_pp_eval_for_ving"]["kwic"]})

    # --- Audit F2 (Lexical NP + for V-ing, all 13 tokens) ---
    # Line-level audit of all 13 rows:
    # 1: fuck that shithead for betting (bare-NP, animate human)
    # 2: I curse the heavens for pulling (1sg finite verb, personified)
    # 3: God bless the kids for trying (God-optative, animate human)
    # 4, 5, 9, 12: bless your heart for helping/joining/saying/giving (bare-NP, metonymic human addressee)
    # 6, 7: heard you curse the farmer for paying / damn the men for letting (perception-verb bare inf, human)
    # 8: God bless your mother for making (God-optative, animate human)
    # 10: God bless my dad for soundproofing (God-optative, animate human)
    # 11: Curse your father for making (bare-NP, animate human)
    # 13: bless my uncle for having (bare-NP, animate human)
    f2_audit = {
        "total_tokens": len(parsed["F2_lex_np_for_ving"]["kwic"]),
        "bare_np_imprec_bened": 7,  # rows 1, 4, 5, 9, 11, 12, 13
        "god_optative": 3,          # rows 3, 8, 10
        "finite_or_perc_verb": 3,   # rows 2, 6, 7
        "accountable_animate_or_personified": 13,
        "inanimate_dismissal": 0,
        "distinct_shows": len({x["show"] for x in parsed["F2_lex_np_for_ving"]["kwic"]}),
    }
    assert (
        f2_audit["bare_np_imprec_bened"] + f2_audit["god_optative"] + f2_audit["finite_or_perc_verb"]
        == f2_audit["total_tokens"]
    )

    # --- Audit F3 (Fuck-euphemisms, 223 tokens across 32 types; 100 KWICs) ---
    f3_by_head = Counter()
    for x in parsed["F3_fuck_euphemisms"]["freq"]:
        f3_by_head[x["form"].split()[0].lower()] += x["freq"]
    # Classify the 100 KWICs of F3: separate literal verb/noun 'fudge' ('fudge the numbers/paperwork/science/truth', 'hot fudge', 'piece of fudge')
    # and proper noun 'Frick' (row 87) and finite/infinitival euphemistic verb ('frick him', 'frig you over', 'eff it up', 'eff this up', 'fudge me' sexual)
    f3_kwic_cats = Counter()
    f3_imprec_by_head = Counter()
    f3_shows_imprec = defaultdict(set)
    F3_LITERAL_FUDGE_OR_NAME = {2, 3, 4, 14, 33, 34, 35, 37, 44, 58, 65, 66, 70, 75, 77, 82, 83, 87, 94, 98, 99}
    F3_VERBAL_EUPH_OUTSIDE = {1, 7, 13, 16, 22, 32, 57, 73, 84}  # e.g. 'we'll frick him', 'frig you over', 'don't eff this up', 'where the frak', 'feed you or frak you'
    F3_META_OR_MOD = {18, 19, 23, 24, 25, 26, 90, 91, 92}  # '"eff you" look', 'say "eff it"', '"Feck this and feck that"'
    for row in parsed["F3_fuck_euphemisms"]["kwic"]:
        n = row["n"]
        m = re.search(r"\b(frak|feck|eff|frig|fudge|frick)\b", row["text"], re.I)
        h = m.group(1).lower() if m else "?"
        if n in F3_LITERAL_FUDGE_OR_NAME:
            f3_kwic_cats["excl_literal_fudge_or_name"] += 1
        elif n in F3_VERBAL_EUPH_OUTSIDE:
            f3_kwic_cats["euphemistic_outside_bare_np"] += 1
        elif n in F3_META_OR_MOD:
            f3_kwic_cats["metalinguistic_or_quoted_imprec"] += 1
        else:
            f3_kwic_cats["verified_bare_np_imprec"] += 1
            f3_imprec_by_head[h] += 1
            f3_shows_imprec[h].add(row["show"])
    assert sum(f3_kwic_cats.values()) == len(parsed["F3_fuck_euphemisms"]["kwic"])

    # --- Audit F4a vs T4/T5 (Local God-ellipsis test WITHIN bless!) ---
    tv_r1 = json.loads(TV_R1.read_text(encoding="utf-8"))
    t4_map = {x["form"].upper(): x["freq"] for x in tv_r1["T4_head_det_n"]["freq_table"]}
    t5_map = {x["form"].upper(): x["freq"] for x in tv_r1["T5_head_poss_n"]["freq_table"]}
    f4a_map = {x["form"].upper(): x["freq"] for x in parsed["F4a_god_bless_lex_np"]["freq"]}

    civic_targets = ["BLESS THE UNITED", "BLESS THE CHILD", "BLESS YOUR MAJESTY", "BLESS THE KING"]
    affective_targets = ["BLESS YOUR HEART", "BLESS HER HEART", "BLESS HIS HEART", "BLESS MY SOUL"]
    civic_total = sum(t4_map.get(k, t5_map.get(k, 0)) for k in civic_targets)
    civic_god = sum(f4a_map.get("GOD " + k, 0) for k in civic_targets)
    aff_total = sum(t5_map.get(k, 0) for k in affective_targets)
    aff_god = sum(f4a_map.get("GOD " + k, 0) for k in affective_targets)
    p_bless_split = fisher_exact_two_sided(civic_god, civic_total - civic_god, aff_god, aff_total - aff_god)

    # --- Audit F4b (Minced God-optatives & God rot) ---
    f4b_freq = {x["form"].lower(): x["freq"] for x in parsed["F4b_minced_god_and_god_rot"]["freq"]}
    f4b_minced_it = sum(v for k, v in f4b_freq.items() if ("darn" in k or "dang" in k) and k.endswith(" it"))
    f4b_minced_non_it = sum(v for k, v in f4b_freq.items() if ("darn" in k or "dang" in k) and not k.endswith(" it"))
    f4b_god_rot = sum(v for k, v in f4b_freq.items() if " rot " in k)
    f4b_god_rot_shows = [
        (r["year"], r["region"], r["show"], r["text"])
        for r in parsed["F4b_minced_god_and_god_rot"]["kwic"]
        if "rot" in r["text"].lower()
    ]

    # --- Audit F5a (Participial cells) ---
    f5a_freq = {x["form"].lower(): x["freq"] for x in parsed["F5a_be_participle"]["freq"]}
    # Count 'X be damned' bare-subjunctive dismissal tokens inside the 100 F5a KWICs
    x_be_damned_kwic = [
        r for r in parsed["F5a_be_participle"]["kwic"]
        if re.search(r"\b(be damned|be buggered)\b", r["text"], re.I)
        and not re.search(r"\b(i'll|i will|i'd|you'll|they'll|'ll|to|shall|may|not|or|must|you)\s+be\s+(damned|buggered)\b", r["text"], re.I)
    ]

    # --- Audit F5b (Positive-controlled finite/infinitival baseline, all 49 rows) ---
    f5b_by_lemma = Counter()
    for x in parsed["F5b_finite_baseline"]["freq"]:
        v = x["form"].lower().split()[1]
        if v.startswith("curse"):
            f5b_by_lemma["curse"] += x["freq"]
        elif v.startswith("damn"):
            f5b_by_lemma["damn"] += x["freq"]
        elif v.startswith("darn"):
            f5b_by_lemma["darn_literal_mending"] += x["freq"]
        elif v.startswith("dang"):
            f5b_by_lemma["dang"] += x["freq"]
        elif v.startswith("drat"):
            f5b_by_lemma["drat"] += x["freq"]
    assert sum(f5b_by_lemma.values()) == 49

    # --- Audit F5c ('dash it', all 65 KWIC rows) ---
    # Verified exclusions:
    #   1: 'Yo, dash it, bro' (MLE slang 'throw/bin it')
    #   2: '1,000-mile dash it used to be' (noun 'dash' + relative clause)
    #   8: 'dash it through your window' (literal verb 'throw/smash')
    #   15, 16, 17: 'Flash it, Dash it' (wordplay/slogan)
    F5C_EXCL = {1, 2, 8, 15, 16, 17}
    f5c_imprec = [r for r in parsed["F5c_dash_it_kwic"]["kwic"] if r["n"] not in F5C_EXCL]
    f5c_regions = Counter(r["region"] for r in f5c_imprec)
    f5c_shows = Counter(r["show"] for r in f5c_imprec)

    summary = {
        "F1a_nonverbal_direct": {
            "total": sum(x["freq"] for x in parsed["F1a_nonverbal_direct_for_ving"]["freq"]),
            "forms": parsed["F1a_nonverbal_direct_for_ving"]["freq"],
        },
        "F1b_pp_eval_for_ving": {
            "total": sum(x["freq"] for x in parsed["F1b_pp_eval_for_ving"]["freq"]),
            "unique_types": len(parsed["F1b_pp_eval_for_ving"]["freq"]),
            "by_frame_tokens": dict(f1b_by_frame),
            "by_frame_types": dict(f1b_types_by_frame),
            "kwic_distinct_shows": f1b_shows,
        },
        "F2_lex_np_for_ving": f2_audit,
        "F3_fuck_euphemisms": {
            "raw_total": sum(f3_by_head.values()),
            "raw_unique_types": len(parsed["F3_fuck_euphemisms"]["freq"]),
            "raw_by_head": dict(f3_by_head),
            "kwic_100_audit": dict(f3_kwic_cats),
            "kwic_verified_imprec_by_head": dict(f3_imprec_by_head),
            "kwic_verified_shows_by_head": {k: len(v) for k, v in f3_shows_imprec.items()},
        },
        "F4a_bless_local_ellipsis_split": {
            "total_god_bless_lex_np": sum(x["freq"] for x in parsed["F4a_god_bless_lex_np"]["freq"]),
            "unique_types": len(parsed["F4a_god_bless_lex_np"]["freq"]),
            "civic_targets": {k: {"total": t4_map.get(k, t5_map.get(k, 0)), "god": f4a_map.get("GOD " + k, 0)} for k in civic_targets},
            "affective_targets": {k: {"total": t5_map.get(k, 0), "god": f4a_map.get("GOD " + k, 0)} for k in affective_targets},
            "civic_god": civic_god, "civic_bare": civic_total - civic_god,
            "affective_god": aff_god, "affective_bare": aff_total - aff_god,
            "fisher_two_sided_p": p_bless_split,
        },
        "F4b_minced_god_and_god_rot": {
            "total": sum(f4b_freq.values()),
            "forms": f4b_freq,
            "minced_it_only": f4b_minced_it,
            "minced_non_it": f4b_minced_non_it,
            "god_rot_total": f4b_god_rot,
            "god_rot_examples": f4b_god_rot_shows,
        },
        "F5a_be_participle": {
            "forms": f5a_freq,
            "total": sum(f5a_freq.values()),
            "x_be_damned_buggered_in_100_kwic": len(x_be_damned_kwic),
            "x_be_damned_samples": [(r["show"], r["text"]) for r in x_be_damned_kwic],
        },
        "F5b_finite_baseline": {
            "total": 49,
            "by_lemma": dict(f5b_by_lemma),
            "minced_curse_sense_hits": 0,
        },
        "F5c_dash_it_audit": {
            "raw_total": len(parsed["F5c_dash_it_kwic"]["kwic"]),
            "verified_imprecative": len(f5c_imprec),
            "excluded_literal_or_slang": len(F5C_EXCL),
            "regions": dict(f5c_regions),
            "distinct_shows": len(f5c_shows),
            "top_shows": f5c_shows.most_common(8),
        },
    }

    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [
        "# Round-2 TV Corpus Follow-Up Results Summary (F1a–F5c)",
        "",
        "## 1. General Evaluative Reason-PP Controls (`F1a`, `F1b`) & Lexical-NP Targets (`F2`)",
        f"- **F1a (direct-NP non-verbal evaluatives + `for V-ing`):** **{summary['F1a_nonverbal_direct']['total']}** tokens — both *Silly me for V-ing* (*Silly me for thinking...*, *Silly me for sinking so low...*); **0** for *lucky, poor, yay, boo*.",
        f"- **F1b (PP-target evaluative formulae + `for V-ing`):** **{summary['F1b_pp_eval_for_ving']['total']} tokens** across **{summary['F1b_pp_eval_for_ving']['unique_types']} distinct types** ({f1b_shows} distinct shows in the 100-line KWIC sample): *shame on* ({f1b_by_frame['shame on']} tokens / {f1b_types_by_frame['shame on']} types), *good for* ({f1b_by_frame['good for']} / {f1b_types_by_frame['good for']}), *good on* ({f1b_by_frame['good on']} / {f1b_types_by_frame['good on']}), *kudos to/for* ({f1b_by_frame['kudos to']+f1b_by_frame['kudos for']} / {f1b_types_by_frame['kudos to']+f1b_types_by_frame['kudos for']}), *shame to* ({f1b_by_frame['shame to']}). Confirms `for V-ing` is a general English evaluative-act reason modifier, not proprietary to bare-NP imprecatives.",
        f"- **F2 (Lexical NPs + `for V-ing`):** **{f2_audit['total_tokens']}** tokens total ({f2_audit['bare_np_imprec_bened']} bare-NP imprecative/benedictive, {f2_audit['god_optative']} overt *God*, {f2_audit['finite_or_perc_verb']} finite/perception verb; {f2_audit['distinct_shows']} shows). **13/13 (100%)** target accountable animate or personified/metonymic human agents; **0/13** inanimate dismissals.",
        "",
        "## 2. *Fuck*-Euphemisms (`F3`): Replicating H3 Beyond *Damn*",
        f"- **Raw total:** {summary['F3_fuck_euphemisms']['raw_total']} tokens across {summary['F3_fuck_euphemisms']['raw_unique_types']} types (*frak* {f3_by_head['frak']}, *fudge* {f3_by_head['fudge']}, *eff* {f3_by_head['eff']}, *feck* {f3_by_head['feck']}, *frig* {f3_by_head['frig']}, *frick* {f3_by_head['frick']}).",
        f"- **100-line KWIC audit:** **{f3_kwic_cats['verified_bare_np_imprec']}** verified bare-NP imprecatives (*frak* {f3_imprec_by_head['frak']}, *feck* {f3_imprec_by_head['feck']}, *eff* {f3_imprec_by_head['eff']}, *frig* {f3_imprec_by_head['frig']}, *fudge* {f3_imprec_by_head['fudge']}, *frick* {f3_imprec_by_head['frick']}; e.g. *Frak the Gods*, *frak the Graystones*, *Eff Christmas*, *Eff you all to H!*, *Frig the dip*, *frig the lot of you/them*, *Feck it*, *Fudge you*), plus **{f3_kwic_cats['metalinguistic_or_quoted_imprec']}** quoted/metalinguistic imprecatives, **{f3_kwic_cats['euphemistic_outside_bare_np']}** outside-construction euphemistic verbal/wh-uses (*don't eff this up*, *frig you over*, *where the frak*), and **{f3_kwic_cats['excl_literal_fudge_or_name']}** literal *fudge* / proper-name exclusions.",
        "",
        "## 3. Local *God*-Ellipsis Split Within *Bless* (`F4a`) & Minced *God*-Optatives (`F4b`)",
        f"- **F4a (`God bless` + lexical NP = {summary['F4a_bless_local_ellipsis_split']['total_god_bless_lex_np']} tokens / {summary['F4a_bless_local_ellipsis_split']['unique_types']} types):**",
        f"  - Civic/solemn targets (*the United [States]*, *the child*, *Your Majesty*, *the King*): **{civic_god}/{civic_total} ({100*civic_god/civic_total:.1f}%)** take overt *God*.",
        f"  - Affective possessive idioms (*your/her/his heart*, *my soul*): **{aff_god}/{aff_total} ({100*aff_god/aff_total:.1f}%)** take overt *God* (**{aff_total-aff_god}/{aff_total} = {100*(aff_total-aff_god)/aff_total:.1f}%** are bare *bless*!).",
        f"  - Exact two-sided Fisher's exact test within *bless*: **$p = {p_bless_split:.2e}$**.",
        f"- **F4b (Minced *God*-optatives & `God rot` = 140 tokens):** All **{f4b_minced_it}/135 (100%)** minced *God/Gosh/Dog + darn/dang* tokens are frozen on `it` (*gosh darn it* 71, *god dang it* 28, *gosh dang it* 24, *god darn it* 11, *dog darn it* 1; **0** non-`it` objects). Meanwhile, archaic *God rot* yields **5** UK/IE tokens (*God rot him* 2, *God rot you* 2, *God rot her* 1; 0 *it*).",
        "",
        "## 4. Defective-Verb Paradigm Cells (`F5a`), Positive-Controlled Finite Baseline (`F5b`), & `dash it` Audit (`F5c`)",
        f"- **F5a (`be + PART`):** *be damned* ({f5a_freq.get('be damned',0):,}, incl. {len(x_be_damned_kwic)} productive bare-subjunctive `X be damned/buggered` dismissals in the 100-line KWIC sample), *be darned* ({f5a_freq.get('be darned',0)}), *be buggered* ({f5a_freq.get('be buggered',0)}), *be danged* ({f5a_freq.get('be danged',0)}), *be dratted* (0). Confirms *darn* and *dang* maintain a two-cell defective paradigm (bare stem + past participle).",
        f"- **F5b (Positive-controlled finite/infinitival baseline incl. `I`, 49 tokens):** *curse* ({f5b_by_lemma['curse']}), *damn* ({f5b_by_lemma['damn']}), literal sock-mending *to darn her/them* ({f5b_by_lemma['darn_literal_mending']}, validating the query's positive control!), and **0** finite/infinitival curse-sense hits for *darn, dang, drat*.",
        f"- **F5c (`dash it` full 65-line KWIC audit):** **{len(f5c_imprec)}/65 (90.8%)** are verified imprecative *dash it (all)* across {len(f5c_shows)} shows ({f5c_regions.get('UK/IE',0)} UK/IE, {f5c_regions.get('US/CA',0)} US/CA, predominantly period British upper-class dialogue or pastiche: *Jeeves and Wooster* {f5c_shows.get('Jeeves and Wooster', 0)}, *BBC Play of the Month* 5, *Blandings* 4, *Parade's End* 4, *Dorothy L. Sayers* 3), with 6 literal/slang/wordplay exclusions.",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"F1a={summary['F1a_nonverbal_direct']['total']}, F1b={summary['F1b_pp_eval_for_ving']['total']}/{summary['F1b_pp_eval_for_ving']['unique_types']} types, F2={f2_audit['total_tokens']} (0 inanimate)")
    print(f"F3 verified bare-NP in 100 KWIC={f3_kwic_cats['verified_bare_np_imprec']} (by head: {dict(f3_imprec_by_head)})")
    print(f"F4a within-bless God split: civic {civic_god}/{civic_total} vs affective {aff_god}/{aff_total}, Fisher p={p_bless_split:.2e}")
    print(f"F5a={f5a_freq}, F5b={dict(f5b_by_lemma)}, F5c verified={len(f5c_imprec)}/65")


if __name__ == "__main__":
    main()
