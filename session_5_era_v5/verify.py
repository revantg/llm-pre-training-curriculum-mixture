#!/usr/bin/env python3
"""Re-derive every load-bearing number in SUBMISSION.md from widget_9_dataset_inventory.html.

Zero dependencies. Run:  python3 verify.py
The inventory is the source of truth; the course SUPPLY_T constant is NOT trusted.
"""
import re, sys, pathlib, collections

HERE = pathlib.Path(__file__).parent
INV = HERE / "widgets" / "widget_9_dataset_inventory.html"
LANES = ["web", "code", "indic", "stem", "reason", "longctx", "agentic"]
STEM_NAMES = {"proof-pile-2", "D4 STEM (V4)", "peS2o"}
SHARE = {"web":33.85,"code":23.95,"indic":15.80,"stem":11.45,"reason":8.50,"longctx":4.45,"agentic":2.00}
MAIN, ANNEAL, TOTAL = 2000.0e9, 80.0e9, 2080.0e9
W = [0.10, 0.35, 0.30, 0.25]
PROFILE = {"web":[45,38,30,28.20],"code":[18,24,25,25.00],"indic":[14,15,16,17.40],
           "stem":[12,12,12,9.80],"reason":[6,6.5,11,9.30],"longctx":[3,2.5,4,8.30],
           "agentic":[2,2,2,2.00]}
RESERVE = {"indic":9.6e9,"code":6.4e9,"reason":7.4e9,"agentic":5.0e9,"stem":1.6e9}

ok = fail = 0
def chk(label, got, want, tol=5e-3):
    global ok, fail
    good = abs(got - want) <= tol
    print(f"  {'PASS' if good else 'FAIL'}  {label:52} got {got:14.4f}  want {want:12.4f}")
    ok, fail = ok + good, fail + (not good)

def parse():
    src = INV.read_text(encoding="utf-8", errors="ignore")
    starts = [m.start() for m in re.finditer(r"\{g:'", src)]
    out = []
    for i, st in enumerate(starts):
        en = starts[i+1] if i+1 < len(starts) else src.find("];", st)
        blk = src[st:en]
        rec = {}
        for k in ("g","name","lic","tier","tag"):
            m = re.search(rf"\b{k}:'((?:[^'\\]|\\.)*)'", blk)
            rec[k] = m.group(1) if m else None
        m = re.search(r"\btokens:([0-9.eE+]+)", blk)
        rec["tokens"] = float(m.group(1)) if m else 0.0
        out.append(rec)
    return out

def main():
    if not INV.exists():
        print(f"inventory not found: {INV}"); return 1
    inv = parse()
    print(f"parsed {len(inv)} datasets from {INV.name}\n")
    by = collections.defaultdict(list)
    for r in inv:
        by[{"general":"web","long":"longctx"}.get(r["g"], r["g"])].append(r)
    stem = [r for r in by["web"] if r["name"] in STEM_NAMES]
    web  = [r for r in by["web"] if r["name"] not in STEM_NAMES]
    real = {"web":sum(r["tokens"] for r in web),
            "code":sum(r["tokens"] for r in by["code"]),
            "indic":sum(r["tokens"] for r in by["indic"] if r["tag"] != "synth"),
            "stem":sum(r["tokens"] for r in stem),
            "reason":sum(r["tokens"] for r in by["reason"]),
            "longctx":sum(r["tokens"] for r in by["longctx"] if "Book" in r["name"]),
            "agentic":sum(r["tokens"] for r in by["agentic"])}

    print("== supply, re-derived from the itemised inventory ==")
    chk("STEM real supply (B) -- NOT the 250B constant", real["stem"]/1e9, 146.0)
    chk("real Indic A+B+C (B)", real["indic"]/1e9, 113.9)
    chk("long-context independent supply (B)", real["longctx"]/1e9, 40.0)
    chk("agentic pool (B)", real["agentic"]/1e9, 0.627)
    chk("web (B)", real["web"]/1e9, 4691.0)
    chk("code (B)", real["code"]/1e9, 1103.0)
    chk("reasoning (B)", real["reason"]/1e9, 85.1)

    print("\n== mixture closes ==")
    chk("lane shares sum", sum(SHARE.values()), 100.00)
    ballast = {l: 50.0e9*SHARE[l]/100 for l in LANES}
    ann = {l: ballast[l] + RESERVE.get(l, 0.0) for l in LANES}
    chk("reserve (B)", sum(RESERVE.values())/1e9, 30.0)
    chk("anneal total (B)", sum(ann.values())/1e9, 80.0)
    chk("anneal mixture sums", sum(100*ann[l]/ANNEAL for l in LANES), 100.000)
    demand = {l: MAIN*SHARE[l]/100 + ann[l] for l in LANES}
    chk("total demand (B)", sum(demand.values())/1e9, 2080.0)
    chk("mixture shift %", 0.5*sum(abs(100*ann[l]/ANNEAL - SHARE[l]) for l in LANES), 17.64, 0.01)

    print("\n== stage profiles time-average to the published shares ==")
    for l in LANES:
        chk(f"{l} time-average", sum(W[s]*PROFILE[l][s] for s in range(4)), SHARE[l], 1e-9)
    for s, nm in enumerate(("Seed","General","Reasoning","Long-context")):
        chk(f"{nm} row sums", sum(PROFILE[l][s] for l in LANES), 100.0, 1e-9)

    print("\n== epochs and verdicts ==")
    for l, want in [("indic",2.93),("stem",1.62),("reason",2.13),("longctx",2.28),("agentic",73.37)]:
        chk(f"{l} epochs", demand[l]/real[l], want, 0.01)

    print("\n== Indic tiers at the declared cap N = 2.00 ==")
    TA, TB, TC = 64.0e9, 44.9e9, 5.0e9
    synth_pool = sum(r["tokens"] for r in by["indic"] if r["tag"] == "synth")
    chk("Sangraha synthetic pool (B)", synth_pool/1e9, 162.0)
    N = 2.00
    tD = demand["indic"] - (TA+TB+TC)*N
    for nm, v in (("A", TA*N), ("B", TB*N), ("C", TC*N), ("D", tD)):
        chk(f"tier {nm} share %", 100*v/demand["indic"], {"A":38.38,"B":26.93,"C":3.00,"D":31.69}[nm], 0.01)
    chk("tier D epochs on the 162B pool", tD/synth_pool, 0.65, 0.01)
    chk("lane synthetic %", 100*tD/demand["indic"], 31.69, 0.01)

    print("\n== agentic ==")
    ag_real = real["agentic"]*8.0
    chk("real served at 8 epochs (B)", ag_real/1e9, 5.016)
    chk("generated % of lane", 100*(demand["agentic"]-ag_real)/demand["agentic"], 89.10, 0.05)
    chk("conservative asymptote 16.39x (B)", real["agentic"]*16.39/1e9, 10.28, 0.01)
    gen_d = sum(r["tokens"] for r in by["agentic"] if r["tier"] == "D")
    chk("tier-D generated share of pool %", 100*gen_d/real["agentic"], 20.7, 0.1)

    print("\n== non-natural tokens, by provenance ==")
    gen_us = (demand["agentic"]-ag_real) + 4.4e9
    chk("existing published synthetic % of run", 100*tD/TOTAL, 5.08, 0.01)
    chk("generated by us % of run", 100*gen_us/TOTAL, 2.18, 0.01)
    chk("total non-natural % of run", 100*(tD+gen_us)/TOTAL, 7.26, 0.01)

    print("\n== data gate ==")
    conf = sum(r["tokens"] for r in inv if r["tag"] == "conf")
    chk("inventory-wide confirmed %", 100*conf/sum(r["tokens"] for r in inv), 18.8, 0.1)
    for l in ("longctx","agentic"):
        rows = by[l]
        chk(f"{l} confirmed tokens (must be 0)", sum(r["tokens"] for r in rows if r["tag"]=="conf"), 0.0)
    chk("one-epoch Indic share % (the 5.5 floor)", 100*real["indic"]/TOTAL, 5.48, 0.01)

    print("\n== proxy cost ==")
    full = 6*120e9*TOTAL
    chk("1B x 10B arm, % of run", 100*(6*1e9*10e9)/full, 0.0040, 1e-4)
    chk("3B x 30B arm, % of run", 100*(6*3e9*30e9)/full, 0.0361, 1e-4)
    chk("14@1B + 6@3B x3 seeds, % of run", 100*(14*6*1e9*10e9 + 6*6*3e9*30e9)*3/full, 0.82, 0.01)

    print(f"\n{ok} passed, {fail} failed")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main())
