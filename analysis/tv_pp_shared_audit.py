#!/usr/bin/env python3
"""Reconcile T7 queries on their shared pronouns using the existing line codes.

Input is the locally retained parsed export. Output contains aggregates and
line identifiers, not concordance text. No queries or new use-type coding.
"""
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/davies/tv_t1a_to_t8a_parsed.json"
OUTPUT = ROOT / "data/davies/tv_pp_shared_audit.json"
SHARED = {"you", "him", "her", "them"}
# Existing decisions from analyze_davies.audit_tv_t7a_t7b; unchanged.
CODES = {
    "T7a_to_hell": ({3, 49, 53, 67, 68}, {1, 6, 12, 13, 45}),
    "T7b_for_ving": ({5, 6, 10, 53, 71}, {3, 4, 23, 24, 39, 46, 54, 55, 57, 58, 59, 66, 67, 69}),
}


def reconcile(data):
    out = {}
    heads = r"damn|dang|blast|fuck|screw|sod|bugger|curse|hang|bless|darn|drat|dash"
    for query, tail in [("T7a_to_hell", r"to\s+hell"), ("T7b_for_ving", r"for\s+\w+ing")]:
        excluded, god = CODES[query]
        pattern = re.compile(rf"\b({heads})\s+(it|you|him|her|them|me|us)\s+{tail}", re.I)
        by_head = defaultdict(Counter)
        shows = defaultdict(set)
        all_shows = set()
        shared_shows = set()
        me_rows = []
        for row in data[query]["freq_table"]:
            head, pronoun, *_ = row["form"].lower().split()
            by_head[head]["raw"] += row["freq"]
            by_head[head]["raw_shared" if pronoun in SHARED else "raw_nonshared"] += row["freq"]
        for row in data[query]["kwic"]:
            matches = list(pattern.finditer(row["text"]))
            assert matches, (query, row["n"])
            # Rows 63/64 are overlapping contexts for distinct query matches.
            # Row 64 targets DAMN ME FOR AGREEING (one frequency-table hit),
            # whose start moves to position 63; DAMN YOU FOR ASKING is context.
            if query == "T7b_for_ving" and row["n"] == 64:
                match = next(m for m in matches if m[2].lower() == "me")
                assert match.start() == 63
            else:
                # Other repeated matches share head/pronoun and cannot change
                # these counts; row 63 targets the first of its two matches.
                assert len({(m[1].lower(), m[2].lower()) for m in matches}) == 1 or (query, row["n"]) == ("T7b_for_ving", 63)
                match = matches[0]
            head, pronoun = match[1].lower(), match[2].lower()
            d = by_head[head]
            d["displayed"] += 1
            d["displayed_shared" if pronoun in SHARED else "displayed_nonshared"] += 1
            if row["n"] in excluded or row["n"] in god:
                continue
            d["accepted_all"] += 1
            all_shows.add(row["show"])
            if pronoun in SHARED:
                d["accepted_shared"] += 1
                shows[head].add(row["show"])
                shared_shows.add(row["show"])
            if pronoun == "me":
                d["accepted_me"] += 1
                me_rows.append({"row": row["n"], "head": head, "show": row["show"]})
        for head, d in by_head.items():
            d["undisplayed_shared"] = d["raw_shared"] - d["displayed_shared"]
            d["undisplayed_nonshared"] = d["raw_nonshared"] - d["displayed_nonshared"]
            d["shared_shows"] = len(shows[head])
            assert d["undisplayed_shared"] >= 0 and d["undisplayed_nonshared"] >= 0
        totals = Counter()
        for d in by_head.values():
            totals.update(d)
        totals["shared_shows"] = len(shared_shows)
        totals["all_shows"] = len(all_shows)
        out[query] = {"by_head": dict(sorted(by_head.items())), "totals": dict(totals), "accepted_me_rows": me_rows}
    return out


if __name__ == "__main__":
    result = {"source": str(SOURCE.relative_to(ROOT)), "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "shared_pronouns": sorted(SHARED), "correction": "T7b row 64 targets me, not context you; undisplayed bounds exclude nonshared pronouns.", **reconcile(json.loads(SOURCE.read_text()))}
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({q: result[q]["totals"] for q in CODES}, indent=2))
