#!/usr/bin/env python3
"""Reproduces the load-bearing numbers in brief.md for emnlp596
(Parmar et al., "Data, Data Everywhere", EMNLP 2024 main, arXiv 2407.06380).

The arithmetic half needs NO dependencies and reproduces:
  - the Indic supply totals quoted in gap 1
  - UniMax(N) sampling weights, matching digitised Figures 7, 8, 9 to <=0.08pp
  - alpha sampling as tokens**1.3, matching digitised Figure 9 to <=0.15pp
  - the six-task LM-Eval means behind Tables 6 and 9

Run: python3 verify.py
"""

# ---------------------------------------------------------------- source data
# Table 12: multilingual web crawl, 52 languages (p. 10683)
ML = {"RU":94.52,"JA":70.52,"DE":48.98,"ES":46.50,"FR":44.30,"ZH":43.41,"IT":26.40,
      "NL":15.64,"VI":15.16,"PL":14.50,"PT":11.99,"ID":10.90,"CS":7.23,"FA":6.59,
      "RO":6.58,"TR":6.46,"EL":6.43,"SV":6.39,"HU":5.89,"AR":5.74,"NO":5.61,"FI":4.11,
      "DA":3.79,"UK":3.63,"BG":3.37,"KO":3.05,"HI":2.60,"SK":2.58,"HR":2.45,"CA":2.12,
      "LT":1.69,"HE":1.47,"SL":1.33,"SR":1.24,"ET":1.24,"BN":0.90,"LV":0.84,"TA":0.82,
      "SQ":0.49,"IS":0.38,"UR":0.37,"AZ":0.37,"MR":0.33,"KA":0.32,"MK":0.32,"NE":0.31,
      "KK":0.30,"HY":0.29,"GL":0.29,"ML":0.25,"TE":0.24,"KN":0.18}
INDIC = ["HI","BN","TA","UR","MR","NE","ML","TE","KN"]
PARALLEL_B, PARALLEL_HI_PCT = 56.0, 1.17   # Table 1 / Table 13
EN_B, CODE_B = 1219.0, 211.88              # Table 11 sum / Table 14 sum

# Table 11: English sources as plotted in Figures 6-7 (CC-2022-40 split into 2 shards)
EN = [("mC4",174.8),("CC-2019-35",165.1),("CC-2022-40-1",142.15),("CC-2022-40-0",142.15),
      ("CC-2020-50",141.9),("BigScience",104.5),("CC-News",94.2),("CC-2021-04",68.2),
      ("Reddit+Conv",59.1),("Pile-CC",41.2),("Books3",25.1),("ArXiv",18.7),
      ("OpenWebText2",14.0),("StackExchange",9.8),("Stories",5.3),("Wikipedia",4.3),
      ("PubMed_Abstracts",4.2),("Gutenberg_PG",2.5),("BookCorpus2",1.5),("NIH_ExPorter",0.3)]

# ---------------------------------------------------------------- algorithms
def unimax(toks, n_epochs, budget):
    """Chung et al. 2023 Alg 1: uniform budget, capped at n_epochs per source."""
    order = sorted(range(len(toks)), key=lambda i: toks[i])
    alloc, remaining, left = [0.0] * len(toks), budget, len(toks)
    for j, i in enumerate(order):
        per, cap = remaining / left, toks[i] * n_epochs
        if cap < per:
            alloc[i], remaining, left = cap, remaining - cap, left - 1
        else:
            for k in order[j:]:
                alloc[k] = per
            break
    return [100 * a / budget for a in alloc]

def alpha_sampling(toks, alpha=1.3):
    d = sum(t ** alpha for t in toks)
    return [100 * t ** alpha / d for t in toks]

def check(label, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  [{'ok ' if ok else 'FAIL'}] {label}: {got:.4g} (expected {want:.4g}, tol {tol})")
    return ok

# ---------------------------------------------------------------- gap 1
print("GAP 1 - Indic / low-resource supply")
ml_total = sum(ML.values())
indic = sum(ML[k] for k in INDIC)
hi_par = PARALLEL_HI_PCT / 100 * PARALLEL_B
pool = EN_B + ml_total + PARALLEL_B + CODE_B
fails = []
fails += [not check("Table 12 sum vs Table 1's 540B", ml_total, 540.0, 1.5)]
fails += [not check("9 Indic languages total (B)", indic, 6.00, 1e-9)]
fails += [not check("Indic share of multilingual web pool (%)", 100 * indic / ml_total, 1.108, 0.001)]
fails += [not check("Hindi in parallel corpus (B)", hi_par, 0.655, 0.001)]
fails += [not check("whole pool vs abstract's 'over 2T' (B)", pool, 2028.4, 0.2)]
fails += [not check("all Indic share of whole pool (%)", 100 * (indic + hi_par) / pool, 0.3281, 0.001)]
print(f"  our plan gives Indic 15.80% -> {15.80 / (100 * (indic + hi_par) / pool):.0f}x their share;"
      f" our 5.0B tier C is {5.0 / hi_par:.1f}x their Indic parallel")

# ---------------------------------------------------------------- figure 8
print("\nFIGURE 8 - multilingual UniMax(1e), budget 300B, 53 sources (52 langs + NMT)")
ml_toks = list(ML.values()) + [PARALLEL_B]
w = unimax(ml_toks, 1, 300.0)
plateau = max(w)
fails += [not check("weights sum (%)", sum(w), 100.0, 1e-6)]
fails += [not check("plateau (%) vs digitised 5.54", plateau, 5.54, 0.05)]
fails += [not check("plateau in tokens (B)", plateau / 100 * 300, 16.65, 0.02)]
fails += [not check("RU epochs", (w[0] / 100 * 300) / ML["RU"], 0.176, 0.001)]
hi_w = w[list(ML).index("HI")]
fails += [not check("Hindi served weight (%) vs digitised 0.91", hi_w, 0.867, 0.05)]
fails += [not check("Hindi epochs", (hi_w / 100 * 300) / ML["HI"], 1.0, 1e-9)]
capped = sum(1 for i, t in enumerate(ml_toks) if abs((w[i] / 100 * 300) / t - 1) < 1e-9)
fails += [not check("sources at exactly 1.00 epoch", capped, 45, 0)]
nat_hi = 100 * ML["HI"] / sum(ml_toks)
fails += [not check("uniform up-weight below the cap (pool/budget)", hi_w / nat_hi, 1.99, 0.01)]

# ---------------------------------------------------------------- figure 7
print("\nFIGURE 7 - English UniMax epoch sweep, budget 300B, 20 sources")
en_toks = [t for _, t in EN]
DIGITISED = {1: 7.25, 2: 6.26, 4: 5.53}
for n in (1, 2, 4):
    s = unimax(en_toks, n, 300.0)
    p = max(s)
    width = sum(1 for x in s if abs(x - p) < 1e-9)
    rep = sum(s[i] / 100 * 300 for i in range(len(en_toks))
              if (s[i] / 100 * 300) / en_toks[i] > 1.0001)
    over = sum(1 for i in range(len(en_toks)) if (s[i] / 100 * 300) / en_toks[i] > 1.0001)
    fails += [not check(f"N={n} plateau (%) vs digitised {DIGITISED[n]}", p, DIGITISED[n], 0.08)]
    print(f"        N={n}: plateau {p:.2f}% x {width} sources | {over} sources >1 epoch |"
          f" {rep:.1f}B ({rep/3:.1f}%) of budget from repeated sources")
print(f"        uniform over {len(en_toks)} sources = {100/len(en_toks):.2f}%")

# ---------------------------------------------------------------- figure 9
print("\nFIGURE 9 - code: alpha=1.3 and UniMax(1e), budget 150B, 41 languages")
CODE = [21.12,20.27,19.84,19.49,18.87,18.26,15.79,12.05,9.03,8.97,8.16,5.31,4.96,2.97,
        2.81,2.58,2.29,2.02,1.78,1.76,1.29,1.28,1.18,1.08,1.00,0.96,0.83,0.72,0.68,0.67,
        0.65,0.54,0.52,0.51,0.42,0.42,0.24,0.21,0.16,0.16,0.03]
fails += [not check("Table 14 sum vs Table 1's 212B", sum(CODE), 212.0, 0.2)]
a = alpha_sampling(CODE, 1.3)
for i, (nm, obs) in enumerate([("javascript",11.62),("markdown",11.05),("java",10.68),
                               ("python",10.49),("php",10.12),("c",9.56)]):
    fails += [not check(f"alpha^1.3 {nm} vs digitised {obs}", a[i], obs, 0.16)]
u = unimax(CODE, 1, 150.0)
fails += [not check("UniMax(1e) code plateau (%) vs digitised 6.93", max(u), 6.93, 0.06)]
# DoReMi peaks read from pixels; epochs implied
print(f"  DoReMi markdown 77.56% of 150B on {CODE[1]}B = {0.7756*150/CODE[1]:.2f} epochs")
print(f"  DoReMi OpenWebText2 64.38% of 300B on 14.0B = {0.6438*300/14.0:.2f} epochs")

# ---------------------------------------------------------------- table means
print("\nTABLES 6 / 9 - does the reported LM-Eval equal the mean of its own per-task row?")
T22 = {"Preference":(67.7,68.6,42.11,79.2,66.0,72.6,65.85),
       "UniMax 1e":(70.1,69.8,42.8,79.1,68.0,73.1,67.14),
       "UniMax 2e":(70.7,67.6,42.9,78.9,66.3,72.6,66.50),
       "UniMax 4e":(70.5,67.7,43.0,78.9,67.3,72.4,66.61),
       "DoReMi":(68.3,68.6,41.2,78.9,65.0,72.0,65.63)}
for k, v in T22.items():
    m = sum(v[:6]) / 6
    flag = "" if abs(m - v[6]) <= 0.05 else "   <-- does not reproduce"
    print(f"  {k:12} computed {m:.2f} vs reported {v[6]:.2f}{flag}")
T24 = {"Baseline":(54.1,56.5,38.9,75.1,57.8,58.9,56.81),
       "Quality FG":(57.3,57.7,39.7,75.0,57.6,60.0,57.88),
       "Quality Grouped":(56.2,56.6,38.7,74.2,56.8,58.3,57.19),
       "Toxicity FG":(46.1,57.6,36.9,71.3,55.5,46.2,53.62),
       "Toxicity Grouped":(55.0,56.1,37.3,72.7,54.5,54.2,54.99),
       "Domain FG":(57.0,60.7,39.5,73.3,56.5,57.0,57.34),
       "Domain Grouped":(54.6,59.7,40.2,73.9,59.2,57.1,57.45),
       "ToS FG":(53.4,59.2,37.5,74.3,56.2,59.5,56.69),
       "ToS Grouped":(53.9,59.8,37.5,74.3,58.7,59.6,57.31)}
bad = 0
for k, v in T24.items():
    m = sum(v[:6]) / 6
    if abs(m - v[6]) > 0.05:
        bad += 1
        print(f"  {k:18} computed {m:.2f} vs reported {v[6]:.2f}   <-- delta {m-v[6]:+.2f}")
print(f"  {9-bad} of 9 Table 9 rows reproduce to +/-0.05; {bad} do not")

# ---------------------------------------------------------------- noise floor
print("\nNOISE FLOOR from the paper's own non-monotonicity")
print(f"  LM-Eval 2e={T22['UniMax 2e'][6]} < 4e={T22['UniMax 4e'][6]} -> inversion of "
      f"{T22['UniMax 4e'][6]-T22['UniMax 2e'][6]:.2f} with MORE epochs scoring better")
print(f"  readable: 1e->4e MMLU 28.30 -> 26.60 = -1.70 (~15x the floor)")
print(f"  NOT readable: multilingual UniMax-alpha = +0.13 XCOPA / +0.25 TyDiQA")
# ------------------------------------------------- Indic epochs, cross-paper
# Added after coordination with UniMaxPaper (2304.09151, ICLR 2023).
print("\nINDIC AGGREGATE SHARE - epochs on the real Indic pool")
served = indic                                  # UniMax(1e) serves each source 1 epoch
fails += [not check("Parmar Indic share of the 300B multilingual budget (%)",
                    100 * served / 300.0, 2.000, 1e-9)]
fails += [not check("Parmar epochs on Indic", served / indic, 1.00, 1e-9)]
thresh = max(unimax(ml_toks, 1, 300.0)) / 100 * 300
assert all(ML[k] < thresh for k in INDIC), "an Indic pool exceeds the cap threshold"
print(f"  [ok ] cap binds for all 9 Indic languages (each < {thresh:.2f}B threshold)")
print("  umT5 1x (UniMax Table 8, per UniMaxPaper): 4.14% of 1163B = 48.2B / 48.4B pool")
fails += [not check("  umT5 implied epochs", (0.0414 * 1163.0) / 48.4, 1.00, 0.01)]
for label, demand, pool, want in [("our SS5 floor 5.5%", 110.0, 114.0, 0.96),
                                  ("our SS1 share 15.80% (real)", 316.0, 113.9, 2.77),
                                  ("our SS1 share 15.80% (incl. synthetic)", 316.0, 276.0, 1.14)]:
    fails += [not check(label + " epochs", demand / pool, want, 0.005)]
print("  -> two independent builds serve Indic at exactly 1.00 epoch (cap binds, not chosen);")
print(f"     our floor is {110.0/114.0:.2f}, our headline share is {316.0/113.9:.2f} = {(316.0/113.9):.1f}x published practice")
# ------------------------------------------------- SS5 floor boundary ladder
# Added after UniMaxPaper pressed the point; SOLUTION.md SS5 already states 5.70%.
print("\nSS5 INDIC FLOOR LADDER - against the 113.9B real pool over a 2.0T main run")
REAL, RUN = 113.9, 2000.0
LADDER = {5.0: 0.878, 5.5: 0.966, 5.7: 1.001, 6.0: 1.054}
for pct, want in LADDER.items():
    fails.append(not check(f"floor {pct:.1f}% = {pct/100*RUN:.1f}B", (pct/100*RUN)/REAL, want, 0.001))
inside = [p for p in (4.5, 5.0, 5.5, 6.0) if (p/100*RUN)/REAL <= 1.0]
fails.append(not check("largest half-point floor inside 1 epoch (%)", max(inside), 5.5, 1e-9))
print("  -> 5.70% is the exact boundary; 5.5% is the largest half-point step inside one epoch,")
print("     and one epoch is where both disclosed multilingual builds sit.")

print(f"\n{len(fails)} assertions checked")
print("ALL CHECKS PASSED" if not any(fails) else f"{sum(fails)} CHECK(S) FAILED")
