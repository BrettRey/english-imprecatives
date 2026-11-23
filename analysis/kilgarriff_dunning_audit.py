#!/usr/bin/env python3
"""
Kilgarriff (2001, 2005, 2009) and Dunning (1993) corpus-statistical audit for
English subjectless imprecatives and benedictives.

Computes:
1. Dunning (1993) 2x2 base-rate conditioning P(PP | T2+T3) and log-likelihood G^2
   (strictly as a descriptive sparse-event association/surprise score, not an
   independent-token p-value), plus exact binomial 95% upper bounds separating
   high-information zeros from low-power zeros.
2. Kilgarriff (2001, 2005, 2009) cross-corpus per-million-word (pmw) rate
   calibration, expected BNC2014 counts at TV Corpus rates, known-item genre
   baselines (fuck it, fuck you, damn it, bless you), and Spoken BNC2014
   conversation-level dispersion from Sketch Engine Reference IDs.
3. Bottom-up head-discovery scan across all 4.0M CLAWS5-tagged tokens of
   BNC Baby XML (utterance/clause-initial bare word + accusative/target NP),
   checking whether living imprecative/benedictive heads outside the 13-head
   sampling frame emerge.
"""
import csv
import json
import math
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BNC_BABY_ZIP = Path("/Users/brettreynolds/corpora/bnc1994/baby/2553.zip")
BNC2014_RAW = ROOT / "data" / "bnc2014" / "raw"
OUT_JSON = ROOT / "data" / "kilgarriff_dunning_summary.json"


def dunning_g2(k11: int, k12: int, k21: int, k22: int) -> float:
    """Dunning (1993) log-likelihood ratio G^2 = 2 * sum O * log(O / E)."""
    row1 = k11 + k12
    row2 = k21 + k22
    col1 = k11 + k21
    col2 = k12 + k22
    n = row1 + row2
    if n == 0:
        return 0.0
    total = 0.0
    for o, r, c in [
        (k11, row1, col1),
        (k12, row1, col2),
        (k21, row2, col1),
        (k22, row2, col2),
    ]:
        if o > 0:
            e = r * c / n
            total += o * math.log(o / e)
    return 2.0 * total


def binom_zero_upper_95(n: int) -> float:
    """Exact Clopper-Pearson 95% upper bound for 0/n: 1 - 0.05^(1/n)."""
    if n <= 0:
        return 1.0
    return 1.0 - (0.05 ** (1.0 / n))


def run_dunning_pp_analysis():
    # From Table 3 (T2 + T3 raw pronoun hits) and Table 5 (T7a/T7b shared-pronoun audited)
    # Note: T2+T3 denominators are raw (include literal uses on homophonous heads).
    heads = {
        "damn": {"t2": 1400, "t3": 295, "to_hell_shared": 32, "for_ving_shared": 11},
        "fuck": {"t2": 6869, "t3": 3237, "to_hell_shared": 0, "for_ving_shared": 17},
        "screw": {"t2": 1936, "t3": 1212, "to_hell_shared": 0, "for_ving_shared": 13},
        "bless": {"t2": 2431, "t3": 1223, "to_hell_shared": 0, "for_ving_shared": 6},
        "curse": {"t2": 247, "t3": 120, "to_hell_shared": 0, "for_ving_shared": 1},
        "darn": {"t2": 25, "t3": 12, "to_hell_shared": 0, "for_ving_shared": 1},
        "blast": {"t2": 127, "t3": 318, "to_hell_shared": 1, "for_ving_shared": 0},
        "sod": {"t2": 26, "t3": 27, "to_hell_shared": 0, "for_ving_shared": 0},
        "bugger": {"t2": 16, "t3": 67, "to_hell_shared": 0, "for_ving_shared": 0},
    }
    per_head = {}
    for h, d in heads.items():
        denom = d["t2"] + d["t3"]
        per_head[h] = {
            "t2_t3_raw": denom,
            "to_hell_shared": d["to_hell_shared"],
            "to_hell_per_1k": round(1000.0 * d["to_hell_shared"] / denom, 2),
            "for_ving_shared": d["for_ving_shared"],
            "for_ving_per_1k": round(1000.0 * d["for_ving_shared"] / denom, 2),
        }

    # 2x2 Dunning G^2: damn vs. (fuck + screw + bless) on to hell and for V-ing
    damn_n = heads["damn"]["t2"] + heads["damn"]["t3"]  # 1,695
    fsb_n = sum(heads[h]["t2"] + heads[h]["t3"] for h in ("fuck", "screw", "bless"))  # 16,908
    fsb_for = sum(heads[h]["for_ving_shared"] for h in ("fuck", "screw", "bless"))  # 36

    g2_to_hell_raw = dunning_g2(32, damn_n - 32, 0, fsb_n)
    # Conservative sensitivity: even if 50% of fuck+screw+bless T2+T3 were literal contamination
    fsb_n_half = fsb_n // 2
    g2_to_hell_half = dunning_g2(32, damn_n - 32, 0, fsb_n_half)
    g2_for_ving_raw = dunning_g2(11, damn_n - 11, fsb_for, fsb_n - fsb_for)

    zeros = {
        "to_hell_fsb_raw_16908": {"n": fsb_n, "upper_95_pct": round(100 * binom_zero_upper_95(fsb_n), 4)},
        "to_hell_fsb_half_8454": {"n": fsb_n_half, "upper_95_pct": round(100 * binom_zero_upper_95(fsb_n_half), 4)},
        "tier1_primary6_148": {"n": 148, "upper_95_pct": round(100 * binom_zero_upper_95(148), 2)},
        "tv_primary6_53": {"n": 53, "upper_95_pct": round(100 * binom_zero_upper_95(53), 1)},
        "bnc2014_yay_boo_17": {"n": 17, "upper_95_pct": round(100 * binom_zero_upper_95(17), 1)},
        "tv_d3_yay_boo_13": {"n": 13, "upper_95_pct": round(100 * binom_zero_upper_95(13), 1)},
        "bnc2014_b2_2_euphemisms_11": {"n": 11, "upper_95_pct": round(100 * binom_zero_upper_95(11), 1)},
    }

    return {
        "per_head_rates": per_head,
        "damn_vs_fsb_2x2": {
            "damn_t2_t3": damn_n,
            "fsb_t2_t3_raw": fsb_n,
            "to_hell_g2_raw": round(g2_to_hell_raw, 1),
            "to_hell_g2_half_denom": round(g2_to_hell_half, 1),
            "for_ving_g2_raw": round(g2_for_ving_raw, 1),
        },
        "zero_upper_bounds_95": zeros,
    }


def run_kilgarriff_calibration():
    tv_m = 325.0
    bnc_m = 11.832919
    ratio_size = tv_m / bnc_m  # 27.466x

    # Known-item genre calibration (raw string frequencies in TV vs Spoken BNC2014)
    # Note: TV T1a/T2 counts are per-head exact pairs; BNC2014 key_pairs from bnc2014_summary.json
    genre_pairs = {
        "fuck it": {"tv_raw": 1842, "bnc14_raw": 138},
        "fuck you": {"tv_raw": 6869, "bnc14_raw": 94},
        "damn it": {"tv_raw": 20107, "bnc14_raw": 140},
        "bless you": {"tv_raw": 2431, "bnc14_raw": 92},
        "sod it": {"tv_raw": 129, "bnc14_raw": 16},
        "screw it": {"tv_raw": 1625, "bnc14_raw": 21},
    }
    genre_cal = {}
    for k, v in genre_pairs.items():
        tv_pmw = v["tv_raw"] / tv_m
        bnc_pmw = v["bnc14_raw"] / bnc_m
        # Kilgarriff (2009) simple maths ratio with smoothing N=1 pmw
        sm_ratio = (bnc_pmw + 1.0) / (tv_pmw + 1.0)
        genre_cal[k] = {
            "tv_raw": v["tv_raw"],
            "tv_pmw": round(tv_pmw, 2),
            "bnc14_raw": v["bnc14_raw"],
            "bnc14_pmw": round(bnc_pmw, 2),
            "bnc14_over_tv_raw_ratio": round(bnc_pmw / tv_pmw, 2),
            "kilgarriff_simple_maths_n1": round(sm_ratio, 2),
        }

    # Expected BNC2014 counts at TV rates for rare frames
    # T7a: 75 audited (75-94 total est.); T7b: 53 audited (53-80 total est.); F3: 61/100 * 223 = ~136 est.
    rare_cal = {
        "to_hell": {
            "tv_est_range": [75, 94],
            "tv_pmw_range": [round(75 / tv_m, 2), round(94 / tv_m, 2)],
            "bnc14_expected_at_tv_rate": [round(75 / ratio_size, 1), round(94 / ratio_size, 1)],
            "bnc14_observed": 1,
            "bnc14_pmw": round(1 / bnc_m, 2),
        },
        "for_ving": {
            "tv_est_range": [53, 80],
            "tv_pmw_range": [round(53 / tv_m, 2), round(80 / tv_m, 2)],
            "bnc14_expected_at_tv_rate": [round(53 / ratio_size, 1), round(80 / ratio_size, 1)],
            "bnc14_observed": 3,
            "bnc14_pmw": round(3 / bnc_m, 2),
        },
        "fuck_euphemisms_f3": {
            "tv_est_verified": round(223 * 0.61),
            "tv_pmw_est": round((223 * 0.61) / tv_m, 2),
            "bnc14_expected_at_tv_rate": round((223 * 0.61) / ratio_size, 1),
            "bnc14_observed": 0,
            "bnc14_pmw": 0.0,
        },
    }

    # Conversation-level dispersion in Spoken BNC2014 raw concordance CSVs
    disp = {}
    for p in sorted(BNC2014_RAW.glob("concordance_*.csv")):
        with p.open(encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        query = ""
        header_idx = None
        for idx, r in enumerate(rows):
            if r and r[0] == "query":
                query = r[1] if len(r) > 1 else ""
            if r and r[0] == "Reference":
                header_idx = idx
                break
        if header_idx is None:
            continue
        data_rows = rows[header_idx + 1 :]
        texts = set()
        for r in data_rows:
            if not r:
                continue
            parts = r[0].split(",")
            if len(parts) >= 2:
                texts.add(parts[1].strip())
        disp[p.name] = {
            "query": query[:90],
            "rows": len(data_rows),
            "unique_conversations": len(texts),
        }

    return {
        "corpus_size_ratio_tv_to_bnc14": round(ratio_size, 2),
        "known_item_genre_calibration": genre_cal,
        "rare_frame_rate_calibration": rare_cal,
        "bnc2014_concordance_dispersion": disp,
    }


def run_bnc_baby_bottom_up_discovery():
    """
    Bottom-up head discovery across all 182 XML files (~4.0M tokens) of BNC Baby:
    Find every clause/utterance-initial word (start of <s> or right after
    sentence-internal punctuation/interjection like 'oh') directly followed by
    an accusative pronoun (him, her, them, me, us) or 'you'/'it', excluding
    ordinary auxiliaries, prepositions, conjunctions, and common imperatives,
    and also specifically check a wide candidate set of classic English
    imprecative/optative verbs (blow, stuff, bother, rot, perish, stone,
    strike, confound, hang, curse, blast, damn, bless, fuck, sod, bugger,
    screw, drat, darn, dash, dang, plague, pox, devil, hell, bother, etc.).
    """
    # Step 1: Collect ALL utterance-initial (or post-oh/well/punct) w1 + acc_pron (him/her/them/me/us/you)
    # where w1 is tagged VVB, VVI, ITJ, or NN1 (base/uninflected form, no subject before it).
    acc_prons = {"him", "her", "them", "me", "us", "you"}
    # Also scan specifically for a broad literature-suggested expansion set across ALL NP starters
    extra_probes = {
        "blow", "stuff", "bother", "rot", "perish", "stone", "strike",
        "confound", "plague", "pox", "devil", "burn", "boil", "hang",
        "shag", "wank", "bollocks", "piss", "shit",
    }
    np_starters = {"it", "you", "him", "her", "them", "me", "us", "this", "that", "these", "those", "the", "my", "your", "his", "her", "their", "our"}
    lead_ins = {"oh", "well", "ah", "and", "but", "or", "so", "now"}

    init_acc_counts = Counter()
    init_acc_files = defaultdict(set)
    init_acc_examples = defaultdict(list)
    word_total_counts = Counter()
    total_tokens = 0
    extra_hits = defaultdict(list)

    with zipfile.ZipFile(BNC_BABY_ZIP) as zf:
        xml_names = [n for n in zf.namelist() if n.endswith(".xml") and "/Texts/" in n]
        for xname in sorted(xml_names):
            fid = Path(xname).stem
            root = ET.fromstring(zf.read(xname))
            for s in root.iter("s"):
                toks = []
                for elem in s:
                    tag = elem.tag
                    if tag == "w":
                        w = (elem.text or "").strip().lower()
                        c5 = elem.attrib.get("c5", "")
                        if w:
                            toks.append(("w", w, c5))
                            word_total_counts[w] += 1
                            total_tokens += 1
                    elif tag == "c":
                        p = (elem.text or "").strip()
                        toks.append(("c", p, elem.attrib.get("c5", "")))
                # Inspect clause/utterance-initial positions
                n = len(toks)
                for i in range(n - 1):
                    kind, w, c5 = toks[i]
                    if kind != "w":
                        continue
                    # Determine if utterance/clause initial (start, or after punct, or after oh/well/and/but)
                    is_init = (
                        i == 0
                        or (toks[i - 1][0] == "c" and toks[i - 1][1] in {",", ";", ":", "!", "?", "--", "—", "-", "‘", "“", '"', "'"})
                        or (toks[i - 1][0] == "w" and toks[i - 1][1] in lead_ins and (i == 1 or toks[i - 2][0] == "c"))
                    )
                    if not is_init:
                        continue
                    # Next token must be word
                    if toks[i + 1][0] != "w":
                        continue
                    nxt, nxt_c5 = toks[i + 1][1], toks[i + 1][2]
                    # Broad bottom-up scan for ITJ or bare VVB/VVI + acc pronoun
                    if nxt in acc_prons and any(t in c5 for t in ("ITJ", "VVB", "VVI", "NN1")):
                        init_acc_counts[w] += 1
                        init_acc_files[w].add(fid)
                        if len(init_acc_examples[w]) < 4:
                            ctx = " ".join(t[1] for t in toks[max(0, i - 2) : min(n, i + 7)])
                            init_acc_examples[w].append(f"{fid}: {ctx}")
                    # Probe extra literature heads across all NP starters
                    if w in extra_probes and nxt in np_starters and any(t in c5 for t in ("ITJ", "VVB", "VVI", "NN1", "NN2")):
                        ctx = " ".join(t[1] for t in toks[max(0, i - 2) : min(n, i + 7)])
                        extra_hits[w].append(f"{fid} [{c5}]: {ctx}")

    # Compute Dunning G^2 for sentence-initial + acc_pron association across all discovered heads
    total_init_acc = sum(init_acc_counts.values())
    ranked = []
    for w, cnt in init_acc_counts.items():
        if cnt < 2:
            continue
        w_tot = word_total_counts[w]
        g2 = dunning_g2(cnt, w_tot - cnt, total_init_acc - cnt, total_tokens - w_tot - total_init_acc + cnt)
        # Keep only positive enrichment (observed > expected)
        if cnt > (w_tot * total_init_acc / total_tokens):
            ranked.append({
                "word": w,
                "count": cnt,
                "files": len(init_acc_files[w]),
                "total_word_freq": w_tot,
                "pct_of_word": round(100.0 * cnt / w_tot, 1),
                "g2": round(g2, 1),
                "examples": init_acc_examples[w],
            })
    ranked.sort(key=lambda x: (-x["g2"], -x["count"]))

    return {
        "bnc_baby_tokens": total_tokens,
        "total_init_acc_tokens": total_init_acc,
        "top_40_by_g2": ranked[:40],
        "extra_probe_raw_counts": {k: len(v) for k, v in sorted(extra_hits.items())},
        "extra_probe_samples": {k: v[:12] for k, v in sorted(extra_hits.items()) if v},
    }


def main():
    out = {
        "dunning_pp": run_dunning_pp_analysis(),
        "kilgarriff_calibration": run_kilgarriff_calibration(),
        "bnc_baby_bottom_up": run_bnc_baby_bottom_up_discovery(),
    }
    # Write license-safe aggregate JSON (omit raw BNC Baby context snippets from persisted JSON)
    safe_out = {
        "dunning_pp": out["dunning_pp"],
        "kilgarriff_calibration": out["kilgarriff_calibration"],
        "bnc_baby_bottom_up": {
            "bnc_baby_tokens": out["bnc_baby_bottom_up"]["bnc_baby_tokens"],
            "total_init_acc_tokens": out["bnc_baby_bottom_up"]["total_init_acc_tokens"],
            "top_40_by_g2": [
                {k: v for k, v in row.items() if k != "examples"}
                for row in out["bnc_baby_bottom_up"]["top_40_by_g2"]
            ],
            "extra_probe_raw_counts": out["bnc_baby_bottom_up"]["extra_probe_raw_counts"],
        },
    }
    OUT_JSON.write_text(json.dumps(safe_out, indent=2), encoding="utf-8")

    print("=== 1. DUNNING 2x2 PP CONDITIONING ===")
    print(json.dumps(out["dunning_pp"], indent=2))
    print("\n=== 2. KILGARRIFF CROSS-CORPUS RATE CALIBRATION & DISPERSION ===")
    print(json.dumps(out["kilgarriff_calibration"], indent=2))
    print("\n=== 3. BNC BABY BOTTOM-UP DISCOVERY (TOP 30 BY G^2) ===")
    for row in out["bnc_baby_bottom_up"]["top_40_by_g2"][:30]:
        print(f"  {row['word']:12s} cnt={row['count']:3d} files={row['files']:2d} tot={row['total_word_freq']:5d} ({row['pct_of_word']:4.1f}%) G2={row['g2']:7.1f} | {row['examples'][0]}")
    print("\n=== 4. EXTRA CANDIDATE PROBES IN BNC BABY ===")
    for k, v in out["bnc_baby_bottom_up"]["extra_probe_samples"].items():
        print(f"  {k} ({out['bnc_baby_bottom_up']['extra_probe_raw_counts'][k]}):")
        for ex in v[:6]:
            print(f"    - {ex}")


if __name__ == "__main__":
    main()
