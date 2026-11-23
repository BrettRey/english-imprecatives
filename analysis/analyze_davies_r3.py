#!/usr/bin/env python3
"""Verify and summarize Round-3 Mark Davies mini-controls (C1a-C4)."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "davies" / "davies-r3-controls-2026-11-22-raw.txt"
OUT_JSON = ROOT / "data" / "davies" / "davies_r3_summary.json"
OUT_MD = ROOT / "analysis" / "davies-r3-results-summary.md"


def main():
    text = RAW.read_text(encoding="utf-8")
    sections = {}
    cur = None
    for line in text.splitlines():
        if line.startswith("=== ") and line.endswith(" ==="):
            cur = line.split()[1]
            sections[cur] = []
        elif cur is not None and line.strip():
            sections[cur].append(line.strip())

    # C2b: base-rate denominators for F1a
    c2b_by_head = Counter()
    c2b_total = 0
    for l in sections["C2b"]:
        if l.startswith("TOTAL"):
            c2b_total = int(l.split("\t")[1])
        else:
            _, form, freq = l.split("\t")
            c2b_by_head[form.split()[0].lower()] += int(freq)
    assert sum(c2b_by_head.values()) == c2b_total == 3261

    # C3a: all/both to hell (21 raw, 20 KWIC audited)
    # KWIC exclusions: #1 literal explosive blast; #4, #7, #10, #11, #18 finite/modal damn (5);
    # #6, #9, #13 overt God damn (3); remaining 11 are subjectless bare 'Damn you/them all/both to hell!'
    # (#14 is quoted 'was all ready to yell "damn you! Damn you all to hell!"' — keep note of 10 direct + 1 quoted = 11)
    c3a_excl_literal = {1}
    c3a_excl_finite = {4, 7, 10, 11, 18}
    c3a_god = {6, 9, 13}
    c3a_quoted = {14}
    c3a_kwic = [l.split("\t") for l in sections["C3a"] if len(l.split("\t")) == 5]
    assert len(c3a_kwic) == 20
    c3a_bare_direct = [r for r in c3a_kwic if int(r[0]) not in (c3a_excl_literal | c3a_excl_finite | c3a_god | c3a_quoted)]
    assert len(c3a_bare_direct) == 10
    assert len(c3a_bare_direct) + len(c3a_quoted) + len(c3a_god) + len(c3a_excl_finite) + len(c3a_excl_literal) == 20

    # C3b: all/both for V-ing (12 raw, 11 KWIC audited)
    # KWIC: #1,#2 duplicate subtitle line on You Me Her (fuck you both for chasing); #4 Black Mirror (fuck you all for thinking);
    # #3,#5,#7,#8,#10 bare bless you all (5; #7/#8 same episode/show Angel); #6,#9 overt God bless you all (2);
    # #11 bare damn you all (1)
    c3b_kwic = [l.split("\t") for l in sections["C3b"] if len(l.split("\t")) == 5]
    assert len(c3b_kwic) == 11
    c3b_god = {6, 9}
    c3b_bare = Counter()
    for r in c3b_kwic:
        n = int(r[0])
        if n in c3b_god:
            continue
        t = r[4].lower()
        if "fuck you" in t:
            c3b_bare["fuck"] += 1
        elif "bless you" in t:
            c3b_bare["bless"] += 1
        elif "damn you" in t:
            c3b_bare["damn"] += 1
    assert sum(c3b_bare.values()) + len(c3b_god) == 11

    # C4: GloWbE same-corpus positive control for G4
    c4_by_lemma = Counter()
    for l in sections["C4"]:
        if l.startswith("TOTAL"):
            continue
        _, form, freq = l.split("\t")
        c4_by_lemma[form.split()[1].lower()] += int(freq)
    assert sum(c4_by_lemma.values()) == 297

    summary = {
        "C1a_finite_fuck_screw_for_ving": 0,
        "C1b_phrasal_screw_over_for_ving": {"raw_lines": 2, "unique_utterances": 1, "show": "The Quad"},
        "C2a_thank_pron_for_ving": {"total_tokens": 15929, "displayed_types": 667},
        "C2b_f1a_base_denominators": {"total": c2b_total, "by_head": dict(c2b_by_head)},
        "C3a_all_both_to_hell": {
            "raw_total": 21,
            "raw_damn": 20,
            "raw_blast_literal": 1,
            "kwic_audited": 20,
            "bare_direct_damn": len(c3a_bare_direct),
            "quoted_damn": len(c3a_quoted),
            "god_damn": len(c3a_god),
            "finite_modal_damn": len(c3a_excl_finite),
            "literal_blast": len(c3a_excl_literal),
            "other_heads": 0,
        },
        "C3b_all_both_for_ving": {
            "raw_total": 12,
            "kwic_audited": 11,
            "bare_by_head": dict(c3b_bare),
            "god_bless": len(c3b_god),
            "unique_fuck_shows": 2,
        },
        "C4_glowbe_g4_positive_control": {
            "total": 297,
            "by_lemma": dict(c4_by_lemma),
            "types": 35,
            "varieties_attested": 20,
        },
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md = [
        "# Round-3 Mini-Control Results Summary (`C1a`–`C4`)",
        "",
        "- **C1a (TV Corpus finite/infinitival `fuck/screw + PRON + for V-ing` outside imprecative frame):** **0** hits.",
        "- **C1b (TV Corpus phrasal `fuck/screw PRON over for V-ing`):** **1** unique utterance (2 overlapping subtitle lines, *The Quad*: *orchestrated to screw me over for recruiting Bo*). Contrast **37** audited subjectless tokens (`T7b` + `C3b`: `fuck` 20+3, `screw` 14).",
        "- **C2a (TV Corpus `thank + PRON + for V-ing` benchmark):** **15,929** tokens across 667+ types (`thank you for coming` 3,408, `being` 1,161, `letting` 535, `helping` 479).",
        f"- **C2b (TV Corpus `F1a` base-rate denominators = {c2b_total:,} tokens):** `lucky` {c2b_by_head['lucky']:,} (0 with `for V-ing`), `silly` {c2b_by_head['silly']:,} (2 with `for V-ing`, 0.65%), `poor` {c2b_by_head['poor']:,} (0), `boo` {c2b_by_head['boo']:,} (0; incl. `boo me` 21, `boo him` 6, `boo her` 3), `yay` {c2b_by_head['yay']:,} (0; incl. `yay me` 32, `yay you` 4).",
        "- **C3a (TV Corpus intervening quantifier `all/both + to hell`, 21 raw / 20 KWIC):** **20 `damn`** (10 direct subjectless, 1 quoted, 3 overt `God`, 5 finite/modal) + 1 literal explosive `blast` (*Outsiders*); **0** for `fuck, screw, sod, bugger, curse, bless, darn, dang, eff, frak`.",
        f"- **C3b (TV Corpus intervening quantifier `all/both + for V-ing`, 12 raw / 11 KWIC):** **9 bare** (`bless` {c3b_bare['bless']}, `fuck` {c3b_bare['fuck']} [2 shows: *You Me Her* dup. line + *Black Mirror*], `damn` {c3b_bare['damn']}) + **2 overt `God bless`**.",
        f"- **C4 (GloWbE same-corpus positive control for `G4`):** **297 hits** across 35 types and all 20 varieties (`cursed` {c4_by_lemma['cursed']}, `damned` {c4_by_lemma['damned']}), validating `G4 = 0` for `dratted/danged/darned` in the exact same corpus and query interface.",
    ]
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    print("ALL ASSERTIONS PASSED:", json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
