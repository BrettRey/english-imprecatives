#!/usr/bin/env python3
"""
Phase 2 analyzer for all manually collected Mark Davies corpus datasets:
  - TV Corpus (325M words): T1a, T1b, T2, T3, T4, T5, T6, T7a, T7b, T8a, T8b
  - GloWbE (1.9B words, 20 Englishes): G1, G2, G3a, G3b, G4 (=0)
  - COCA pilot (coca-2026-11-22-pilot-dang.txt)

Computes:
  - Head-by-head frequency profiles across all 13 target heads
  - Precision-audited KWIC breakdowns for T1a-T8b (separating bare-NP
    maledictives/benedictives from literal/finite verbs, overt God-optatives,
    and metalinguistic/nominalized uses)
  - Exact two-sided Fisher's exact tests for H1b, H2, H3, H4, and the
    T7a (Goal PP 'to hell') vs. T7b (Reason PP 'for V-ing') double dissociation
  - World-Englishes regional splits in GloWbE (US/CA vs GB/IE vs AU/NZ vs
    West African English NG/GH homonymy on 'dash')

Outputs:
  - data/davies/davies_summary.json
  - analysis/davies-results-summary.md
"""
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAVIES_DIR = ROOT / "data" / "davies"
OUT_JSON = DAVIES_DIR / "davies_summary.json"
OUT_MD = ROOT / "analysis" / "davies-results-summary.md"

GLOWBE_REGIONS = [
    "US", "CA", "GB", "IE", "AU", "NZ", "IN", "LK", "PK", "BD",
    "SG", "MY", "PH", "HK", "ZA", "NG", "GH", "KE", "TZ", "JM",
]

ALL_HEADS = [
    "damn", "bless", "fuck", "sod", "bugger", "screw", "blast", "curse", "hang",
    "drat", "darn", "dash", "dang",
]


def fisher_exact_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Exact two-sided Fisher's exact test using log-factorials for large N."""
    n1 = a + b
    n2 = c + d
    m1 = a + c
    n = n1 + n2

    def log_comb(nn: int, kk: int) -> float:
        return math.lgamma(nn + 1) - math.lgamma(kk + 1) - math.lgamma(nn - kk + 1)

    denom = log_comb(n, n1)

    def hypergeom_p(k: int) -> float:
        return math.exp(log_comb(m1, k) + log_comb(n - m1, n1 - k) - denom)

    p_obs = hypergeom_p(a)
    lo = max(0, n1 - (n - m1))
    hi = min(n1, m1)
    p_sum = 0.0
    for k in range(lo, hi + 1):
        pk = hypergeom_p(k)
        if pk <= p_obs * (1.0 + 1e-12):
            p_sum += pk
    return min(1.0, p_sum)


def parse_glowbe_block(block: str) -> dict:
    """Parse a 20-region GloWbE CHART/LIST block preserving per-country counts."""
    rows = []
    total_by_region = Counter()
    total_all = 0
    for line in block.splitlines():
        if re.match(r"^\d+\s*\t", line) and "See 'word page'" in line:
            parts = line.split("\t")
            # Find form cell (index 3) and ALL cell (index 4), then region cells starting at index 6
            # Handle variable empty tab separators safely
            # Format: idx \t [See...] \t [Save...] \t   FORM \t ALL \t   \t US \t CA ...
            if len(parts) < 6:
                continue
            form = parts[3].strip()
            all_n = int(parts[4].strip().replace(",", ""))
            reg_vals = parts[6:]
            reg_map = {}
            for r, val in zip(GLOWBE_REGIONS, reg_vals):
                s = val.strip().replace(",", "")
                if s.isdigit():
                    reg_map[r] = int(s)
            rows.append({"form": form, "all": all_n, "regions": reg_map})
        elif "\t TOTAL \t" in line or re.search(r"\bTOTAL\b", line):
            parts = line.split("\t")
            # Locate TOTAL cell
            for i, p in enumerate(parts):
                if p.strip() == "TOTAL" and i + 1 < len(parts):
                    total_all = int(parts[i + 1].strip().replace(",", ""))
                    reg_vals = parts[i + 3:]
                    for r, val in zip(GLOWBE_REGIONS, reg_vals):
                        s = val.strip().replace(",", "")
                        if s.isdigit():
                            total_by_region[r] = int(s)
                    break
    return {
        "rows_captured": len(rows),
        "total_reported": total_all,
        "total_by_region": dict(total_by_region),
        "rows": rows,
    }


def parse_t8b_block(block: str) -> dict:
    freq_table = []
    kwic = []
    for l in block.splitlines():
        if "See 'word page'" in l:
            parts = [p.strip() for p in re.split(r"\t+|\s{3,}", l) if p.strip()]
            if len(parts) >= 2 and re.match(r"^[\d,]+$", parts[-1]):
                freq_table.append({"form": parts[-2], "freq": int(parts[-1].replace(",", ""))})
        elif re.match(r"^\d+\s+\d{4}\s+", l):
            parts = re.split(r"\t+", l)
            if len(parts) >= 5:
                kwic.append({
                    "n": int(parts[0].strip()),
                    "year": int(parts[1].strip()),
                    "region": parts[2].strip(),
                    "show": parts[3].strip(),
                    "text": parts[-1].strip(),
                })
    return {
        "total_reported": sum(x["freq"] for x in freq_table),
        "freq_table": freq_table,
        "kwic_rows_captured": len(kwic),
        "kwic": kwic,
    }


def audit_tv_t7a_t7b(tv: dict) -> dict:
    """Line-level verified audit of T7a (to hell, 85 KWICs) and T7b (for V-ing, 72 KWICs)."""
    # T7a KWIC audit (verified by inspection):
    # Excluded finite/modal/literal: 3 (gonna damn), 49 (I damn), 53 (gonna blast literal), 67 (I damn), 68 (I damn)
    # Overt God-optative: 1, 6 (may God), 12, 13, 45
    t7a_excl_finite = {3, 49, 67, 68}
    t7a_excl_literal = {53}
    t7a_god_opt = {1, 6, 12, 13, 45}

    t7a_kwic_counts = Counter()
    t7a_head_bare = Counter()
    for row in tv["T7a_to_hell"]["kwic"]:
        n = row["n"]
        txt = row["text"]
        m = re.search(r"\b(damn|dang|blast)\s+(?:it|you|him|her|them|me|us)\s+to\s+hell", txt, re.I)
        head = m.group(1).lower() if m else "other"
        if n in t7a_excl_finite:
            t7a_kwic_counts["excl_finite_verb"] += 1
        elif n in t7a_excl_literal:
            t7a_kwic_counts["excl_literal_verb"] += 1
        elif n in t7a_god_opt:
            t7a_kwic_counts["god_optative"] += 1
        else:
            t7a_kwic_counts["bare_np_imprecative"] += 1
            t7a_head_bare[head] += 1

    # T7a full frequency table (N = 104):
    t7a_freq_by_head = Counter()
    for x in tv["T7a_to_hell"]["freq_table"]:
        t7a_freq_by_head[x["form"].split()[0].lower()] += x["freq"]

    # T7b KWIC audit (verified by inspection of all 72 rows):
    # Excluded finite/modal/nominalized: 5 (passive aggressive fuck you for), 6 (giant "Screw you for..."),
    # 10 (all I can do is curse him for), 53 (I bless you for), 71 (would bless you for)
    t7b_excl_finite_or_nom = {5, 6, 10, 53, 71}
    # Overt God-optative: 3, 4, 23, 24, 39, 46, 54, 55, 57, 58, 59, 66, 67, 69
    t7b_god_opt = {3, 4, 23, 24, 39, 46, 54, 55, 57, 58, 59, 66, 67, 69}

    t7b_kwic_counts = Counter()
    t7b_head_bare = Counter()
    t7b_head_god = Counter()
    for row in tv["T7b_for_ving"]["kwic"]:
        n = row["n"]
        txt = row["text"]
        m = re.search(r"\b(damn|dang|blast|fuck|screw|sod|bugger|curse|hang|bless|darn|drat|dash)\s+(?:it|you|him|her|them|me|us)\s+for\s+\w+ing", txt, re.I)
        head = m.group(1).lower() if m else "other"
        if n in t7b_excl_finite_or_nom:
            t7b_kwic_counts["excl_finite_or_nom"] += 1
        elif n in t7b_god_opt:
            t7b_kwic_counts["god_optative"] += 1
            t7b_head_god[head] += 1
        else:
            t7b_kwic_counts["bare_np_imprecative"] += 1
            t7b_head_bare[head] += 1

    t7b_freq_by_head = Counter()
    t7b_types_by_head = Counter()
    for x in tv["T7b_for_ving"]["freq_table"]:
        h = x["form"].split()[0].lower()
        t7b_freq_by_head[h] += x["freq"]
        t7b_types_by_head[h] += 1

    # Fisher's exact test on the T7a vs T7b double dissociation:
    # (a) Full frequency tables (excluding the 1 verified literal 'blast them to hell'):
    #     T7a: damn+dang = 102, other = 1 (coordinated 'damn and blast you to hell')
    #     T7b: damn+dang = 15,  other = 84 (fuck 30, bless 28, screw 22, curse 3, darn 1)
    p_freq_dissoc = fisher_exact_two_sided(
        t7a_freq_by_head["damn"] + t7a_freq_by_head["dang"],
        1,  # coordinated blast you to hell
        t7b_freq_by_head["damn"] + t7b_freq_by_head["dang"],
        sum(v for k, v in t7b_freq_by_head.items() if k not in ("damn", "dang")),
    )
    # (b) Strictly audited bare-NP KWICs (excluding finite, modal, nominalized, and overt God):
    p_kwic_bare_dissoc = fisher_exact_two_sided(
        t7a_head_bare["damn"] + t7a_head_bare["dang"],
        sum(v for k, v in t7a_head_bare.items() if k not in ("damn", "dang")),
        t7b_head_bare["damn"] + t7b_head_bare["dang"],
        sum(v for k, v in t7b_head_bare.items() if k not in ("damn", "dang")),
    )

    return {
        "T7a_freq_by_head": dict(t7a_freq_by_head),
        "T7a_kwic_audit": dict(t7a_kwic_counts),
        "T7a_kwic_bare_by_head": dict(t7a_head_bare),
        "T7b_freq_by_head": dict(t7b_freq_by_head),
        "T7b_types_by_head": dict(t7b_types_by_head),
        "T7b_kwic_audit": dict(t7b_kwic_counts),
        "T7b_kwic_bare_by_head": dict(t7b_head_bare),
        "T7b_kwic_god_by_head": dict(t7b_head_god),
        "fisher_p_freq_dissociation": p_freq_dissoc,
        "fisher_p_kwic_bare_dissociation": p_kwic_bare_dissoc,
    }


def classify_glowbe_g1(g1: dict) -> dict:
    """Classify all 100 top types in GloWbE G1 (minced heads + DET/POSS + N)."""
    # Literal mending for 'darn': socks / hole(s)
    DARN_LITERAL = {"DARN THE HOLES", "DARN THE HOLE", "DARN THAT HOLE", "DARN HIS SOCKS"}
    # 'dash' in GloWbE G1 is heavily confounded by literal verb 'dash' (hopes, foot, head, brains, dreams, crowd, etc.)
    # and West African English 'dash' ('give/tip', e.g. 'dash her tailor', 'dash her bro', 'dash that horn' in NG/GH/KE).
    # We keep 'dash' strictly separate from clean minced 'darn' / 'dang' / 'drat' imprecatives!
    cats = Counter()
    by_head_verified = Counter()
    by_head_types = Counter()
    by_head_regions = defaultdict(Counter)
    darn_imprec_examples = []
    dang_imprec_examples = []

    for r in g1["rows"]:
        form = r["form"]
        n = r["all"]
        head = form.split()[0].lower()
        if head == "dash":
            cats["dash_literal_or_wae_excluded"] += n
        elif head == "darn":
            if form in DARN_LITERAL:
                cats["darn_literal_mending_excluded"] += n
            else:
                cats["darn_imprecative_verified"] += n
                by_head_verified["darn"] += n
                by_head_types["darn"] += 1
                for reg, cnt in r["regions"].items():
                    by_head_regions["darn"][reg] += cnt
                darn_imprec_examples.append((form, n, r["regions"]))
        elif head == "dang":
            cats["dang_imprecative_verified"] += n
            by_head_verified["dang"] += n
            by_head_types["dang"] += 1
            for reg, cnt in r["regions"].items():
                by_head_regions["dang"][reg] += cnt
            dang_imprec_examples.append((form, n, r["regions"]))
        elif head == "drat":
            cats["drat_imprecative_verified"] += n
            by_head_verified["drat"] += n
            by_head_types["drat"] += 1

    assert sum(cats.values()) == g1["total_reported"], (
        f"G1 conservation failed: {sum(cats.values())} vs {g1['total_reported']}"
    )
    return {
        "total_reported": g1["total_reported"],
        "breakdown": dict(cats),
        "verified_non_dash_tokens": by_head_verified["darn"] + by_head_verified["dang"] + by_head_verified["drat"],
        "verified_non_dash_types": by_head_types["darn"] + by_head_types["dang"] + by_head_types["drat"],
        "by_head_verified_tokens": dict(by_head_verified),
        "by_head_verified_types": dict(by_head_types),
        "by_head_regions": {k: dict(v) for k, v in by_head_regions.items()},
        "darn_examples": [x[0] for x in darn_imprec_examples[:20]],
        "dang_examples": [x[0] for x in dang_imprec_examples],
    }


def classify_glowbe_g2(g2: dict) -> dict:
    """Classify all 14 rows in GloWbE G2 (minced heads + accusative pronouns)."""
    by_head = Counter()
    by_head_regions = defaultdict(Counter)
    dash_ng_gh = 0
    dash_total = 0
    for r in g2["rows"]:
        head = r["form"].split()[0].lower()
        n = r["all"]
        by_head[head] += n
        for reg, cnt in r["regions"].items():
            by_head_regions[head][reg] += cnt
        if head == "dash":
            dash_total += n
            dash_ng_gh += r["regions"].get("NG", 0) + r["regions"].get("GH", 0)
    assert sum(by_head.values()) == g2["total_reported"]
    return {
        "total_reported": g2["total_reported"],
        "by_head_raw": dict(by_head),
        "clean_non_dash_minced_acc_tokens": by_head["darn"] + by_head["dang"] + by_head["drat"],
        "dash_total": dash_total,
        "dash_ng_gh_tokens": dash_ng_gh,
        "dash_ng_gh_share": dash_ng_gh / dash_total if dash_total else 0.0,
        "by_head_regions": {k: dict(v) for k, v in by_head_regions.items()},
    }


def summarize_glowbe_g3(g3a: dict, g3b: dict) -> dict:
    """Summarize H3 outside-construction mirroring in GloWbE G3a (attributive) & G3b (adverbial)."""
    out = {}
    for label, blk, word_idx in [("G3a_attributive_top100", g3a, 1), ("G3b_adverbial_top100", g3b, 0)]:
        by_head = Counter()
        by_head_us_ca = Counter()
        by_head_gb_ie = Counter()
        for r in blk["rows"]:
            h = r["form"].split()[word_idx].lower()
            by_head[h] += r["all"]
            by_head_us_ca[h] += r["regions"].get("US", 0) + r["regions"].get("CA", 0)
            by_head_gb_ie[h] += r["regions"].get("GB", 0) + r["regions"].get("IE", 0)
        assert sum(by_head.values()) == blk["total_reported"]
        out[label] = {
            "total_top100": blk["total_reported"],
            "by_head": dict(by_head),
            "by_head_us_ca": dict(by_head_us_ca),
            "by_head_gb_ie": dict(by_head_gb_ie),
        }
    return out


def summarize_tv_paradigm(tv: dict) -> dict:
    """Aggregate T1a, T1b, T2, T3, T6, T8a across all 13 target heads."""
    t1a = {x["form"].split()[0].lower(): x["freq"] for x in tv["T1a_head_it"]["freq_table"]}
    t2 = {x["form"].split()[0].lower(): x["freq"] for x in tv["T2_head_you"]["freq_table"]}
    t3 = Counter()
    for x in tv["T3_head_acc_pron"]["freq_table"]:
        t3[x["form"].split()[0].lower()] += x["freq"]
    t6 = Counter()
    for x in tv["T6_god_head_np"]["freq_table"]:
        t6[x["form"].split()[1].lower()] += x["freq"]
    t4_top100 = Counter()
    for x in tv["T4_head_det_n"]["freq_table"]:
        t4_top100[x["form"].split()[0].lower()] += x["freq"]
    t5_top100 = Counter()
    for x in tv["T5_head_poss_n"]["freq_table"]:
        t5_top100[x["form"].split()[0].lower()] += x["freq"]

    # H1b Fisher test on TV Corpus (325M):
    # Compare God+HEAD+NP (T6) vs pronoun-complement baseline (T1a+T2+T3) for:
    # (1) bless vs fuck+screw+sod+bugger
    # (2) damn vs fuck+screw+sod+bugger
    # Note: raw T1a+T2+T3 for fuck/screw includes literal verb tokens; even if only 50% of fuck/screw are imprecative,
    # 2 God-fuck out of ~5,000+ imprecative fuck+pron is <0.04%, vs 1,802/3,656 (49.3%!) for bless and 2,229/21,798 (10.2%) for damn!
    # We compute exact Fisher on raw counts (conservative denominator for fuck/screw/sod/bugger) AND note the precision bound.
    bless_base = t1a.get("bless", 0) + t2.get("bless", 0) + t3.get("bless", 0)
    damn_base = t1a.get("damn", 0) + t2.get("damn", 0) + t3.get("damn", 0)
    taboo4_base = sum(t1a.get(h, 0) + t2.get(h, 0) + t3.get(h, 0) for h in ("fuck", "screw", "sod", "bugger"))
    taboo4_god = sum(t6.get(h, 0) for h in ("fuck", "screw", "sod", "bugger"))
    p_god_bless_vs_taboo4 = fisher_exact_two_sided(t6["bless"], max(0, bless_base - t6["bless"]), taboo4_god, taboo4_base - taboo4_god)
    p_god_damn_vs_taboo4 = fisher_exact_two_sided(t6["damn"], max(0, damn_base - t6["damn"]), taboo4_god, taboo4_base - taboo4_god)

    # Regional distribution in T8a KWICs
    t8a_regions = Counter(x["region"] for x in tv["T8a_coord"]["kwic"])

    return {
        "T1a_by_head": t1a,
        "T1b_univerb": {x["form"].lower(): x["freq"] for x in tv["T1b_dammit"]["freq_table"]},
        "T2_by_head": t2,
        "T3_by_head": dict(t3),
        "T4_total": tv["T4_head_det_n"]["total_reported"],
        "T4_unique_types": tv["T4_head_det_n"]["unique_reported"],
        "T4_top100_by_head": dict(t4_top100),
        "T5_total": tv["T5_head_poss_n"]["total_reported"],
        "T5_unique_types": tv["T5_head_poss_n"]["unique_reported"],
        "T5_top100_by_head": dict(t5_top100),
        "T6_god_by_head": dict(t6),
        "T6_total": tv["T6_god_head_np"]["total_reported"],
        "T8a_coord_forms": tv["T8a_coord"]["freq_table"],
        "T8a_kwic_regions": dict(t8a_regions),
        "h1b_tv_tests": {
            "bless_god": t6["bless"], "bless_pron_total": bless_base,
            "damn_god": t6["damn"], "damn_pron_total": damn_base,
            "taboo4_god": taboo4_god, "taboo4_pron_total": taboo4_base,
            "fisher_p_bless_vs_taboo4": p_god_bless_vs_taboo4,
            "fisher_p_damn_vs_taboo4": p_god_damn_vs_taboo4,
        },
    }


def main():
    tv = json.loads((DAVIES_DIR / "tv_t1a_to_t8a_parsed.json").read_text(encoding="utf-8"))
    raw2 = (DAVIES_DIR / "tv-t8b-and-glowbe-2026-11-22-raw.txt").read_text(encoding="utf-8")
    # Strip any trailing metadata after </USER_REQUEST>
    if "</USER_REQUEST>" in raw2:
        raw2 = raw2.split("</USER_REQUEST>", 1)[0]
    blocks2 = [b for b in re.split(r"(?m)^(?=(?:/plan\s+)?HELP\b)", raw2) if b.strip() and not b.strip().startswith("<USER_REQUEST>")]
    assert len(blocks2) == 5, f"Expected 5 HELP blocks in second paste, got {len(blocks2)}"

    t8b = parse_t8b_block(blocks2[0])
    g1 = parse_glowbe_block(blocks2[1])
    g2 = parse_glowbe_block(blocks2[2])
    g3a = parse_glowbe_block(blocks2[3])
    g3b = parse_glowbe_block(blocks2[4])

    tv_summary = summarize_tv_paradigm(tv)
    t7_audit = audit_tv_t7a_t7b(tv)
    g1_cls = classify_glowbe_g1(g1)
    g2_cls = classify_glowbe_g2(g2)
    g3_cls = summarize_glowbe_g3(g3a, g3b)

    # T8b manual audit: 75/76 are transitive verb 'wow' ('impress'); 1/76 ('ouch him') is coerced verb after modal 'can't'
    # Verified bare-NP primary-interjection complements = 0 / 76!
    t8b_audit = {
        "total_raw": t8b["total_reported"],
        "kwic_audited": t8b["kwic_rows_captured"],
        "wow_transitive_verb": 75,
        "ouch_modal_coerced_verb": 1,
        "oops_ugh_whoops_yuck_acc": 0,
        "verified_bare_np_complements": 0,
    }

    # H2 vs H4 GloWbE minced-head test (1.9B words):
    # Clean non-dash minced heads (darn + dang + drat):
    #   [X NP] (G1 verified full NPs + G2 accusative pronouns) vs finite transitive curse-verb frame (G4 = 0)
    minced_in_cxn = g1_cls["verified_non_dash_tokens"] + g2_cls["clean_non_dash_minced_acc_tokens"]
    g4_finite_curse = 0

    summary = {
        "tv_corpus_325m": tv_summary,
        "tv_t7a_vs_t7b_double_dissociation": t7_audit,
        "tv_t8b_primary_control": t8b_audit,
        "glowbe_1_9b": {
            "G1_minced_full_np": g1_cls,
            "G2_minced_acc_pron": g2_cls,
            "G3_outside_mirroring": g3_cls,
            "G4_finite_curse_verb_minced": g4_finite_curse,
            "h2_vs_h4_minced_clean_summary": {
                "darn_dang_drat_full_np_verified_top100": g1_cls["verified_non_dash_tokens"],
                "darn_dang_drat_full_np_types_top100": g1_cls["verified_non_dash_types"],
                "darn_dang_drat_acc_pron_tokens": g2_cls["clean_non_dash_minced_acc_tokens"],
                "total_in_construction_tokens": minced_in_cxn,
                "G4_finite_infinitival_curse_verb_tokens": g4_finite_curse,
            },
        },
    }

    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Build clean Markdown summary report
    lines = [
        "# Tier-2 Mark Davies Results Summary (TV Corpus 325M + GloWbE 1.9B)",
        "",
        "## 1. TV Corpus (325M Words): Pronoun-Complement & `God`-Optative Profile (`T1a`, `T2`, `T3`, `T6`)",
        "",
        "| Head | `HEAD it` (`T1a`) | `HEAD you` (`T2`) | `HEAD him/her/them/me/us` (`T3`) | `God + HEAD + NP` (`T6`) | `to hell` (`T7a`) | `for V-ing` (`T7b`, tok/typ) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for h in ALL_HEADS:
        n1 = tv_summary["T1a_by_head"].get(h, 0)
        n2 = tv_summary["T2_by_head"].get(h, 0)
        n3 = tv_summary["T3_by_head"].get(h, 0)
        n6 = tv_summary["T6_god_by_head"].get(h, 0)
        n7a = t7_audit["T7a_freq_by_head"].get(h, 0)
        n7b = t7_audit["T7b_freq_by_head"].get(h, 0)
        t7b_ty = t7_audit["T7b_types_by_head"].get(h, 0)
        lines.append(f"| *{h}* | {n1:,} | {n2:,} | {n3:,} | {n6:,} | {n7a:,} | {n7b} / {t7b_ty} |")
    lines.append(
        f"| **Total** | **{sum(tv_summary['T1a_by_head'].values()):,}** | **{sum(tv_summary['T2_by_head'].values()):,}** | "
        f"**{sum(tv_summary['T3_by_head'].values()):,}** | **{tv_summary['T6_total']:,}** | **{sum(t7_audit['T7a_freq_by_head'].values()):,}** | "
        f"**{sum(t7_audit['T7b_freq_by_head'].values())} / {sum(t7_audit['T7b_types_by_head'].values())}** |"
    )
    lines.append("")
    lines.append(f"- **Univerbated (`T1b`):** *dammit* = {tv_summary['T1b_univerb'].get('dammit',0):,}, *goddammit* = {tv_summary['T1b_univerb'].get('goddammit',0):,} (total {sum(tv_summary['T1b_univerb'].values()):,}).")
    lines.append(f"- **Open lexical NP slots (`T4`, `T5`):** `HEAD + DET + N` = **{tv_summary['T4_total']:,}** tokens across **{tv_summary['T4_unique_types']:,}** unique types; `HEAD + POSS + N` = **{tv_summary['T5_total']:,}** tokens across **{tv_summary['T5_unique_types']:,}** unique types.")
    lines.append("")
    lines.extend([
        "## 2. Decisive Hypothesis Tests (TV Corpus + GloWbE)",
        "",
        "### 2.1 H1b (`God`-Optative Ellipsis) Fails Across the Paradigm (`T6`)",
        f"- Overt `God + HEAD + NP` is overwhelmingly concentrated on theological *damn* ({tv_summary['T6_god_by_head'].get('damn',0):,}) and *bless* ({tv_summary['T6_god_by_head'].get('bless',0):,}), plus euphemistic *God dang it* ({tv_summary['T6_god_by_head'].get('dang',0)}) and *God darn it* ({tv_summary['T6_god_by_head'].get('darn',0)}), archaic *God curse* ({tv_summary['T6_god_by_head'].get('curse',0)}), and *God blast it* ({tv_summary['T6_god_by_head'].get('blast',0)}).",
        f"- Across the four productive secular maledictives (*fuck, screw, sod, bugger*), `God + HEAD + NP` occurs only **{tv_summary['h1b_tv_tests']['taboo4_god']}** times (*God fuck you* 1, *God fuck it* 1; **0** for *screw, sod, bugger*) against **{tv_summary['h1b_tv_tests']['taboo4_pron_total']:,}** raw pronoun-complement hits (Fisher's exact $p < 10^{-300}$ against both *bless* and *damn*).",
        "",
        "### 2.2 The `to hell` (`T7a`) vs. `for V-ing` (`T7b`) Double Dissociation",
        f"- **Goal PP `to hell` (`T7a`, 104 raw / 85 KWICs audited):** lexically restricted to *damn* (101) + euphemism *dang* (*Dang it to hell*, 1) + 1 coordinated *Damn, and blast you to hell* (1 literal explosive *blast them to hell* excluded). **0** tokens for *fuck, screw, sod, bugger, curse, hang, bless*.",
        f"- **Reason PP `for V-ing` (`T7b`, 99 raw across 77 unique types / 72 KWICs audited):** construction-general across *fuck* (30 tokens / 25 types), *bless* (28 / 20), *screw* (22 / 17), *damn* (15 / 11), *curse* (3 / 3), and minced *darn* (*Darn you for raising us so well*, 1 / 1).",
        f"- **Exact two-sided Fisher's exact test (`damn/dang` vs. non-`damn` across `T7a` vs. `T7b`):**",
        f"  - Full frequency tables (excl. 1 literal *blast*): **102:1** vs. **15:84**, **$p = {t7_audit['fisher_p_freq_dissociation']:.2e}$**.",
        f"  - Strictly audited bare-NP KWICs (excl. finite/modal/nominalized/overt-*God*): **{t7_audit['T7a_kwic_bare_by_head'].get('damn',0)+t7_audit['T7a_kwic_bare_by_head'].get('dang',0)}:{sum(v for k,v in t7_audit['T7a_kwic_bare_by_head'].items() if k not in ('damn','dang'))}** vs. **{t7_audit['T7b_kwic_bare_by_head'].get('damn',0)+t7_audit['T7b_kwic_bare_by_head'].get('dang',0)}:{sum(v for k,v in t7_audit['T7b_kwic_bare_by_head'].items() if k not in ('damn','dang'))}**, **$p = {t7_audit['fisher_p_kwic_bare_dissociation']:.2e}$**.",
        "",
        "### 2.3 Coordination (`T8a`) & Primary-Interjection Control (`T8b`)",
        f"- **Coordination (`T8a`, $N=11$):** 100% lexicalized British binomial (*damn and blast it* 8, *blast and damn it* 2, *damn and blast you* 1; all 7 KWICs UK/IE). Zero free coordination of other heads.",
        f"- **Primary-interjection accusative control (`T8b`, $N=76$):** **0/76 (0.0%)** bare-NP complements (75 literal transitive verb *wow* 'impress', 1 modal-coerced verb *can't ouch him*, 0 for *oops/ugh/whoops/yuck* across 325M words).",
        "",
        "### 2.4 H2 vs. H4 & H3 in 1.9B-Word GloWbE (`G1`, `G2`, `G3a`, `G3b`, `G4`)",
        f"- **Finite/infinitival curse-verb check for minced heads (`G4`):** **0** hits in 1.9B words (`he/she/they/will/would/could/to drat/darn/dang + him/her/them`).",
        f"- **Yet in the exact same 1.9B corpus, non-*dash* minced heads (*darn, dang, drat*) take open lexical NPs (`G1`) and unambiguous accusative pronouns (`G2`):**",
        f"  - `G1` verified non-literal full lexical NPs (top 100): **{g1_cls['verified_non_dash_tokens']} tokens** across **{g1_cls['verified_non_dash_types']} distinct types** (*darn*: {g1_cls['by_head_verified_tokens'].get('darn',0)} tokens / {g1_cls['by_head_verified_types'].get('darn',0)} types, e.g., *darn the TTC*, *darn my iPad*, *darn those Nats*, *darn those commies*, *darn my proof-reading*, *darn the consequences*; *dang*: {g1_cls['by_head_verified_tokens'].get('dang',0)} tokens / {g1_cls['by_head_verified_types'].get('dang',0)} types, e.g., *dang those plans*, *dang this swarm*, *dang the manager*, *dang these temptations*; excluding 4 literal sock/hole-mending *darn* tokens and 88 literal/West-African *dash* tokens).",
        f"  - `G2` unambiguous accusative pronouns (*darn/dang/drat*): **{g2_cls['clean_non_dash_minced_acc_tokens']} tokens** (*darn* {g2_cls['by_head_raw'].get('darn',0)}, *dang* {g2_cls['by_head_raw'].get('dang',0)}, *drat* {g2_cls['by_head_raw'].get('drat',0)}).",
        f"  - **World-Englishes homonymy control on *dash* (`G2`):** Of {g2_cls['dash_total']} raw `dash + PRON` tokens, **{g2_cls['dash_ng_gh_tokens']} ({100*g2_cls['dash_ng_gh_share']:.1f}%)** come from Nigeria and Ghana (and 16/22 = 72.7% of `dash me`), reflecting the West African English ditransitive verb *dash* ('give/tip'), alongside literal *dash [hopes/foot against a stone]*.",
        f"- **H3 Outside-Construction Mirroring (`G3a`, `G3b`):**",
        f"  - Attributive `that X N` (`G3a`, top 100 = {g3_cls['G3a_attributive_top100']['total_top100']}): *damn* {g3_cls['G3a_attributive_top100']['by_head'].get('damn',0)}, *darn* {g3_cls['G3a_attributive_top100']['by_head'].get('darn',0)}, *darned* {g3_cls['G3a_attributive_top100']['by_head'].get('darned',0)}, *dang* {g3_cls['G3a_attributive_top100']['by_head'].get('dang',0)}, *dratted* {g3_cls['G3a_attributive_top100']['by_head'].get('dratted',0)}.",
        f"  - Adverbial `X ADJ` (`G3b`, top 100 = {g3_cls['G3b_adverbial_top100']['total_top100']:,}): *damn* {g3_cls['G3b_adverbial_top100']['by_head'].get('damn',0):,}, *darn* {g3_cls['G3b_adverbial_top100']['by_head'].get('darn',0):,} (e.g., *darn good* 894, *darn sure* 130, *darn close* 126, *darn cute* 81 > *damn cute* 73), *darned* {g3_cls['G3b_adverbial_top100']['by_head'].get('darned',0)}, *dang* {g3_cls['G3b_adverbial_top100']['by_head'].get('dang',0)} (0 *drat/dratted/dash* in top 100).",
    ])

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"T7a vs T7b Fisher p (freq): {t7_audit['fisher_p_freq_dissociation']:.3e}")
    print(f"T7a vs T7b Fisher p (bare KWIC): {t7_audit['fisher_p_kwic_bare_dissociation']:.3e}")
    print(f"GloWbE G1 verified non-dash minced full NPs: {g1_cls['verified_non_dash_tokens']} tokens / {g1_cls['verified_non_dash_types']} types")
    print(f"GloWbE G2 clean non-dash minced acc pron: {g2_cls['clean_non_dash_minced_acc_tokens']} (vs G4 = {g4_finite_curse})")


if __name__ == "__main__":
    main()
