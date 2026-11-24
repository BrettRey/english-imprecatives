"""Tally the 2026-11-23 TV Corpus Chart-view samples of the five frames behind
Table 2 (T1a, T2, T3, T4, T5), and estimate how much of the raw pronoun base
used in Section 5.3 is not the construction.

Input: data/davies/tv-frame-samples-2026-11-23-raw.txt (gitignored: corpus
text). Each sample line ends with ' || CODE', where CODE is
  I = subjectless imprecative or benediction (the construction)
  O = ordinary verb (subject present or understood addressee of a literal act)
  G = optative with an overt subject (God damn it, May the Lord bless ...)
  X = other (what the fuck you..., quoted or garbled, noun use)
  A = ambiguous
First-pass codes by Claude Opus 5.5, 2026-11-23; every code checked by the author.
"""
import json, re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "data/davies/tv-frame-samples-2026-11-23-raw.txt"
HEADS = "damn|bless|fuck|sod|bugger|screw|blast|curse|hang|drat|darn|dash|dang"
NODE = {
    "T1a": r"\b(%s)\s+it\b" % HEADS,
    "T2": r"\b(%s)\s+you\b" % HEADS,
    "T3": r"\b(%s)\s+(him|her|them|me|us)\b" % HEADS,
    "T4": r"\b(%s)\s+(the|this|that|these|those)\s" % HEADS,
    "T5": r"\b(%s)\s+(my|your|his|her|their)\s" % HEADS,
}

def load():
    frames, cur = defaultdict(list), None
    for line in RAW.read_text().splitlines():
        m = re.match(r"^## (T\w+)", line)
        if m:
            cur = m.group(1); continue
        m = re.match(r"^(\d+)\s.*\|\| ([IOGXA])$", line)
        if m and cur:
            text = line.rsplit("||", 1)[0]
            node = re.search(NODE[cur], text, re.I)
            frames[cur].append({
                "n": int(m.group(1)), "code": m.group(2),
                "head": node.group(1).lower() if node else None,
                "pron": node.group(2).lower() if node and node.lastindex and node.lastindex > 1 else None,
            })
    return frames

def main():
    frames = load()
    out = {"frames": {}, "pronoun_base_shares": {}}
    for f, rows in frames.items():
        assert len(rows) == 100, (f, len(rows))
        assert all(r["head"] for r in rows), (f, [r["n"] for r in rows if not r["head"]])
        c = Counter(r["code"] for r in rows)
        o_heads = Counter(r["head"] for r in rows if r["code"] == "O")
        out["frames"][f] = {"codes": dict(c), "ordinary_verb_heads": dict(o_heads.most_common())}
    # Section 5.3 base: T2 (you) + T3 restricted to him/her/them. Each sample is
    # 100 lines from a population of different size, so estimate each head's
    # construction share within each frame and weight by that frame's raw base.
    bases = json.loads((HERE.parent / "data/davies/tv_t2_t3_pronoun_bases.json").read_text())
    samples = {"T2": frames["T2"], "T3": [r for r in frames["T3"] if r["pron"] in ("him", "her", "them")]}
    fsb_raw = fsb_est = 0.0
    fsb_lines = 0
    for h in ("fuck", "screw", "bless", "damn"):
        raw = {"T2": bases["T2_you"][h],
               "T3": sum(bases["T3_by_pronoun"][h].get(p, 0) for p in ("him", "her", "them"))}
        rec = {"raw_base": sum(raw.values()), "by_frame": {}}
        est = 0.0
        for f in ("T2", "T3"):
            rows = [r for r in samples[f] if r["head"] == h]
            share = sum(r["code"] == "I" for r in rows) / len(rows)
            rec["by_frame"][f] = {"sample_lines": len(rows), "construction_share": round(share, 2), "raw_base": raw[f]}
            est += raw[f] * share
        rec["sample_lines"] = sum(v["sample_lines"] for v in rec["by_frame"].values())
        rec["est_construction_base"] = round(est)
        rec["construction_share"] = round(est / rec["raw_base"], 2)
        out["pronoun_base_shares"][h] = rec
        if h != "damn":
            fsb_raw += rec["raw_base"]; fsb_est += est; fsb_lines += rec["sample_lines"]
    out["pronoun_base_shares"]["fsb_pooled"] = {"raw_base": int(fsb_raw), "sample_lines": fsb_lines,
                                                "est_construction_base": round(fsb_est),
                                                "construction_share": round(fsb_est / fsb_raw, 3)}
    print(json.dumps(out, indent=1))
    (HERE / "tv_frame_samples.json").write_text(json.dumps(out, indent=1) + "\n")

if __name__ == "__main__":
    main()
