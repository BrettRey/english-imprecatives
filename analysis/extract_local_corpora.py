#!/usr/bin/env python3
"""
Full-recall local corpus extractor for the English maledictive/benedictive NP paper.

Searches three local full-text corpora:
  1. CABNC TalkBank CHAT (UK spoken, 1,860 .cha files, 2.05M words) -- preserving
     BOTH cleaned text AND raw Jeffersonian prosodic/pause cues between head and NP!
  2. BNC Baby XML (UK spoken + fiction + news + academic, 182 XML files, ~4M words) --
     using CLAWS POS tags directly so full recall includes bare plurals, proper names,
     quantifiers, coordinated heads, and overt God-subject alternations!
  3. OANC (US spoken + written, 8,824 .txt files, ~15M words).

Outputs structured JSON + summary tables to data/local/ for transparent adjudication.
"""
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "local"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CABNC_DIR = ROOT.parent / "english-interjections" / "vendor" / "CABNC-0a28a11" / "data" / "cabnc_talkbank_chat"
BNC_BABY_ZIP = Path("/Users/brettreynolds/corpora/bnc1994/baby/2553.zip")
OANC_DIR = ROOT.parents[2] / "corpora" / "oanc" / "OANC-GrAF" / "data"

TRANSPARENT_HEADS = ["damn", "bless", "fuck", "sod", "bugger", "blast", "curse", "screw", "hang"]
MINCED_HEADS = ["drat", "darn", "dash", "dang"]
ALL_HEADS = TRANSPARENT_HEADS + MINCED_HEADS
ED_FORMS = ["damned", "blessed", "blasted", "cursed", "dratted", "darned", "dashed", "danged"]
UNIVERB = ["dammit", "goddammit"]
PRIMARY_6 = ["ouch", "oops", "ugh", "wow", "whoops", "yuck"]
DISCOURSE_3 = ["oh", "ah", "hey"]

PRON_2 = {"you", "ya", "ye"}
PRON_NON2 = {"him", "her", "them", "'em", "em", "me", "us"}
DEM = {"this", "that", "these", "those"}
DET_POSS = {"the", "my", "your", "his", "her", "their", "our", "all", "everyone", "everybody", "everything", "anyone", "anybody", "whoever"}
NEXT_NP_STARTERS = {"it"} | PRON_2 | PRON_NON2 | DEM | DET_POSS

# Jeffersonian boundary cues in raw CABNC lines between head and next word
JEFF_PAUSE_RE = re.compile(r"(\(\.\)|\(\d+(?:\.\d+)?\)|[.,?!;:]|↑|↓|⌈|⌉|⌊|⌋|\+/)")

def clean_chat(line: str) -> str:
    s = re.sub(r"^\*[A-Z0-9]+:\s*", "", line)
    s = re.sub(r"\x15[^\x15]*\x15", "", s)
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = re.sub(r"&=\S+", "", s)
    s = re.sub(r"[<>⌈⌉⌊⌋↑↓°∙+/.]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def check_cabnc_prosody_gap(raw_line: str, head: str, nxt: str) -> dict:
    """Inspect raw CHAT line between head and next word for Jeffersonian pause/contour cues."""
    body = re.sub(r"^\*[A-Z0-9]+:\s*", "", raw_line)
    body = re.sub(r"\x15[^\x15]*\x15", "", body)
    m = re.search(rf"\b{re.escape(head)}\b([^\w]*?)\b{re.escape(nxt)}\b", body, re.I)
    if not m:
        return {"matched": False, "gap": "", "has_boundary_cue": None, "next_capitalized": None}
    gap = m.group(1)
    # Check if next word starts uppercase (in CHAT, sentence/TCU boundary)
    after_start = m.end() - len(nxt)
    next_cap = body[after_start:after_start + 1].isupper()
    has_cue = bool(JEFF_PAUSE_RE.search(gap)) or next_cap
    return {"matched": True, "gap": gap, "has_boundary_cue": has_cue, "next_capitalized": next_cap}

def scan_cabnc():
    stats = {
        "files": 0, "utterances": 0, "tokens": 0,
        "head_totals": Counter(), "ed_totals": Counter(), "univerb_totals": Counter(),
        "primary_totals": Counter(), "god_head_hits": [],
        "head_np_candidates": defaultdict(list),
        "primary_np_candidates": defaultdict(list),
        "outside_attr_adv": defaultdict(list),
    }
    head_set = set(ALL_HEADS)
    ed_set = set(ED_FORMS)
    univerb_set = set(UNIVERB)
    prim_set = set(PRIMARY_6)

    for cha in sorted(CABNC_DIR.rglob("*.cha")):
        stats["files"] += 1
        fn = cha.name
        for lno, raw in enumerate(cha.read_text(errors="ignore").splitlines(), 1):
            if not raw.startswith("*"):
                continue
            stats["utterances"] += 1
            s = clean_chat(raw)
            toks = re.findall(r"[A-Za-z']+", s)
            low = [t.lower() for t in toks]
            stats["tokens"] += len(low)

            for i, w in enumerate(low):
                if w in head_set:
                    stats["head_totals"][w] += 1
                    nxt = low[i + 1] if i + 1 < len(low) else ""
                    prev = low[i - 1] if i > 0 else ""
                    if prev == "god" and nxt in NEXT_NP_STARTERS:
                        stats["god_head_hits"].append({"file": fn, "line": lno, "head": w, "next": nxt, "text": s[:150]})
                    if nxt in NEXT_NP_STARTERS:
                        pros = check_cabnc_prosody_gap(raw, w, nxt)
                        stats["head_np_candidates"][w].append({
                            "file": fn, "line": lno, "prev": prev, "next": nxt,
                            "prosody": pros, "text": s[:160], "raw_excerpt": raw[:180]
                        })
                    # Outside-construction prenominal/adverbial for damn & minced
                    if w in ("damn", "darn", "dang", "drat", "dash") and prev in ("that", "this", "these", "those", "a", "the", "my", "your", "his", "her", "so", "pretty", "too"):
                        stats["outside_attr_adv"][w].append({"file": fn, "line": lno, "prev": prev, "next": nxt, "text": s[:140]})
                elif w in ed_set:
                    stats["ed_totals"][w] += 1
                    if w in ("dratted", "darned", "danged", "dashed"):
                        stats["outside_attr_adv"][w].append({"file": fn, "line": lno, "text": s[:140]})
                elif w in univerb_set:
                    stats["univerb_totals"][w] += 1
                elif w in prim_set:
                    stats["primary_totals"][w] += 1
                    nxt = low[i + 1] if i + 1 < len(low) else ""
                    if nxt in NEXT_NP_STARTERS:
                        pros = check_cabnc_prosody_gap(raw, w, nxt)
                        stats["primary_np_candidates"][w].append({
                            "file": fn, "line": lno, "next": nxt,
                            "prosody": pros, "text": s[:160], "raw_excerpt": raw[:180]
                        })
    # Convert Counters/defaultdicts for JSON
    for k in ("head_totals", "ed_totals", "univerb_totals", "primary_totals"):
        stats[k] = dict(stats[k])
    for k in ("head_np_candidates", "primary_np_candidates", "outside_attr_adv"):
        stats[k] = dict(stats[k])
    return stats

def scan_bnc_baby():
    """Full-recall POS-tagged scan of BNC Baby XML (Conversation, Fiction, News, Academic)."""
    stats = {
        "files": 0, "tokens": 0, "by_genre_tokens": Counter(),
        "head_totals": Counter(), "ed_totals": Counter(), "univerb_totals": Counter(),
        "primary_totals": Counter(),
        "god_head_hits": [],
        "head_np_candidates": defaultdict(list),
        "primary_np_candidates": defaultdict(list),
        "outside_attr_adv": defaultdict(list),
    }
    head_set = set(ALL_HEADS)
    ed_set = set(ED_FORMS)
    univerb_set = set(UNIVERB)
    prim_set = set(PRIMARY_6)
    # POS prefixes that can start an NP in CLAWS5 (BNC): PNP (pron), DT0/AT0/DPS (det/poss),
    # NP0 (proper noun!), NN1/NN2/NN0 (bare noun/plural!), PNI (indef pron like everyone!), PNQ (whoever!)
    NP_POS_PREFIXES = ("PNP", "PNI", "PNQ", "DT0", "AT0", "DPS", "NP0", "NN1", "NN2", "NN0")

    with zipfile.ZipFile(BNC_BABY_ZIP) as zf:
        for name in sorted(zf.namelist()):
            if not (name.endswith(".xml") and "/Texts/" in name):
                continue
            parts = name.split("/")
            genre = parts[-2] if len(parts) >= 2 else "unknown"
            stats["files"] += 1
            fn = parts[-1]
            raw_xml = zf.read(name)
            try:
                root = ET.fromstring(raw_xml)
            except ET.ParseError:
                continue
            for s_el in root.iter("s"):
                s_num = s_el.attrib.get("n", "")
                items = []
                for el in s_el.iter():
                    if el.tag in ("w", "c") and el.text:
                        txt = el.text.strip()
                        if txt:
                            items.append((txt, el.attrib.get("c5", ""), el.attrib.get("pos", ""), el.tag))
                words_only = [(t, c5, pos) for t, c5, pos, tag in items if tag == "w"]
                stats["tokens"] += len(words_only)
                stats["by_genre_tokens"][genre] += len(words_only)
                sent_str = " ".join(t for t, _, _, _ in items)

                for i, (tok, c5, pos, tag) in enumerate(items):
                    if tag != "w":
                        continue
                    w = tok.lower()
                    # find immediate next element (noting if punctuation intervenes!)
                    intervening_punct = ""
                    j = i + 1
                    while j < len(items) and items[j][3] == "c":
                        intervening_punct += items[j][0]
                        j += 1
                    nxt_tok, nxt_c5, nxt_pos = (items[j][0].lower(), items[j][1], items[j][2]) if j < len(items) else ("", "", "")
                    # previous word
                    k = i - 1
                    while k >= 0 and items[k][3] == "c":
                        k -= 1
                    prev_tok, prev_c5 = (items[k][0].lower(), items[k][1]) if k >= 0 else ("", "")

                    if w in head_set:
                        stats["head_totals"][w] += 1
                        if prev_tok == "god" and any(nxt_c5.startswith(p) for p in NP_POS_PREFIXES):
                            stats["god_head_hits"].append({
                                "file": fn, "genre": genre, "s": s_num, "head": w,
                                "next": nxt_tok, "next_c5": nxt_c5, "sent": sent_str[:180]
                            })
                        # Full-recall NP check: NO sentence-ending punctuation between head and NP-starting POS
                        if nxt_c5 and any(nxt_c5.startswith(p) for p in NP_POS_PREFIXES) and not any(p in intervening_punct for p in ".?!"):
                            stats["head_np_candidates"][w].append({
                                "file": fn, "genre": genre, "s": s_num, "c5": c5,
                                "prev": prev_tok, "punct": intervening_punct,
                                "next": nxt_tok, "next_c5": nxt_c5, "sent": sent_str[:180]
                            })
                        if w in ("damn", "darn", "dang", "drat", "dash") and (c5.startswith("AJ") or c5.startswith("AV")):
                            stats["outside_attr_adv"][w].append({
                                "file": fn, "genre": genre, "s": s_num, "c5": c5, "sent": sent_str[:150]
                            })
                    elif w in ed_set:
                        stats["ed_totals"][w] += 1
                        if w in ("dratted", "darned", "danged", "dashed"):
                            stats["outside_attr_adv"][w].append({
                                "file": fn, "genre": genre, "s": s_num, "c5": c5, "sent": sent_str[:150]
                            })
                    elif w in univerb_set:
                        stats["univerb_totals"][w] += 1
                    elif w in prim_set:
                        stats["primary_totals"][w] += 1
                        if nxt_c5 and any(nxt_c5.startswith(p) for p in NP_POS_PREFIXES) and not any(p in intervening_punct for p in ".?!"):
                            stats["primary_np_candidates"][w].append({
                                "file": fn, "genre": genre, "s": s_num, "punct": intervening_punct,
                                "next": nxt_tok, "next_c5": nxt_c5, "sent": sent_str[:180]
                            })

    for k in ("by_genre_tokens", "head_totals", "ed_totals", "univerb_totals", "primary_totals"):
        stats[k] = dict(stats[k])
    for k in ("head_np_candidates", "primary_np_candidates", "outside_attr_adv"):
        stats[k] = dict(stats[k])
    return stats

def scan_oanc():
    stats = {
        "files": 0, "tokens": 0,
        "head_totals": Counter(), "ed_totals": Counter(), "univerb_totals": Counter(),
        "primary_totals": Counter(), "god_head_hits": [],
        "head_np_candidates": defaultdict(list),
        "primary_np_candidates": defaultdict(list),
        "outside_attr_adv": defaultdict(list),
    }
    head_set = set(ALL_HEADS)
    ed_set = set(ED_FORMS)
    univerb_set = set(UNIVERB)
    prim_set = set(PRIMARY_6)

    for p in sorted(OANC_DIR.rglob("*.txt")):
        stats["files"] += 1
        rel = str(p.relative_to(OANC_DIR))
        txt = p.read_text(errors="ignore")
        # tokenize keeping punctuation gaps via regex span
        matches = list(re.finditer(r"[A-Za-z']+", txt))
        stats["tokens"] += len(matches)
        for i, m in enumerate(matches):
            w = m.group(0).lower()
            if w not in head_set and w not in ed_set and w not in univerb_set and w not in prim_set:
                continue
            lo = max(0, m.start() - 55)
            hi = min(len(txt), m.end() + 75)
            ctx = re.sub(r"\s+", " ", txt[lo:hi]).strip()
            nxt = matches[i + 1].group(0).lower() if i + 1 < len(matches) else ""
            gap = txt[m.end():matches[i + 1].start()] if i + 1 < len(matches) else ""
            prev = matches[i - 1].group(0).lower() if i > 0 else ""

            if w in head_set:
                stats["head_totals"][w] += 1
                if prev == "god" and nxt in NEXT_NP_STARTERS and not any(c in gap for c in ".?!"):
                    stats["god_head_hits"].append({"file": rel, "head": w, "next": nxt, "ctx": ctx})
                if nxt in NEXT_NP_STARTERS and not any(c in gap for c in ".?!"):
                    stats["head_np_candidates"][w].append({
                        "file": rel, "prev": prev, "gap": gap.strip(), "next": nxt, "ctx": ctx
                    })
                if w in ("darn", "dang", "drat", "dash") and prev in ("that", "this", "these", "those", "a", "so", "pretty", "too"):
                    stats["outside_attr_adv"][w].append({"file": rel, "prev": prev, "next": nxt, "ctx": ctx})
            elif w in ed_set:
                stats["ed_totals"][w] += 1
                if w in ("dratted", "darned", "danged", "dashed"):
                    stats["outside_attr_adv"][w].append({"file": rel, "ctx": ctx})
            elif w in univerb_set:
                stats["univerb_totals"][w] += 1
            elif w in prim_set:
                stats["primary_totals"][w] += 1
                if nxt in NEXT_NP_STARTERS and not any(c in gap for c in ".?!"):
                    stats["primary_np_candidates"][w].append({
                        "file": rel, "gap": gap.strip(), "next": nxt, "ctx": ctx
                    })

    for k in ("head_totals", "ed_totals", "univerb_totals", "primary_totals"):
        stats[k] = dict(stats[k])
    for k in ("head_np_candidates", "primary_np_candidates", "outside_attr_adv"):
        stats[k] = dict(stats[k])
    return stats

def main():
    print("Scanning CABNC (UK spoken, raw Jeffersonian prosody)...")
    cabnc = scan_cabnc()
    (OUT_DIR / "cabnc_raw_extract.json").write_text(json.dumps(cabnc, indent=2), encoding="utf-8")

    print("Scanning BNC Baby (UK spoken + written, POS-tagged XML)...")
    bnc = scan_bnc_baby()
    (OUT_DIR / "bnc_baby_raw_extract.json").write_text(json.dumps(bnc, indent=2), encoding="utf-8")

    print("Scanning OANC (US spoken + written)...")
    oanc = scan_oanc()
    (OUT_DIR / "oanc_raw_extract.json").write_text(json.dumps(oanc, indent=2), encoding="utf-8")

    print("\n=== SUMMARY ===")
    for name, d in [("CABNC (UK spoken)", cabnc), ("BNC Baby (UK XML)", bnc), ("OANC (US)", oanc)]:
        print(f"\n[{name}] files={d['files']}, tokens={d['tokens']:,}")
        print("  Head totals:", d["head_totals"])
        print("  Univerbated:", d["univerb_totals"])
        print("  -ed forms:", d["ed_totals"])
        print("  God+head+NP hits:", len(d["god_head_hits"]), Counter(x["head"] for x in d["god_head_hits"]))
        print("  Raw head+NP candidates:", {k: len(v) for k, v in d["head_np_candidates"].items()})
        print("  Raw primary6+NP candidates:", {k: len(v) for k, v in d["primary_np_candidates"].items()})
        print("  Outside attr/adv hits:", {k: len(v) for k, v in d["outside_attr_adv"].items()})

if __name__ == "__main__":
    main()
