# Red-team review — the NUMBERS in `SOLUTION_v3.md`

**Reviewer:** RedTeamNumbers · adversarial pass, graded backwards from `local://rubric.md` (assignment verbatim, 3300 chars, R0–R8 / E1–E11, maxPoints 500).
**Method:** every quantity recomputed independently. Every paper-attributed number checked against `papers/<slug>/brief.md`. Every supply figure checked against `widgets/widget_9_dataset_inventory.html` (line items, not the summary constants). Course constants checked against `widgets/widget_1_mixture_composer.html`, `widget_3_opus_selection.html`, `widget_6_reasoning_effort.html`, `widget_7_curriculum_stages.html`, `widget_8_mixture_shift_spike.html`.

**Bottom line.** The arithmetic is unusually clean for a document with this many numbers — roughly 90% of it reproduces exactly, and the hardest single computation in the spec (the ½·L1 mixture shift = 19.48%) is correct to two decimals. Citation fidelity is high: of ~60 paper-attributed figures I found **one** clear misattribution, **two** mis-sourcings, and no fabrications. But there are **13 FATAL findings**, and three of them are not rounding: the declared share column does not sum to 100, the supply ratios silently assume the selector accepts everything, and the anneal epoch counts are computed against a pool the spec itself says it does not draw from. Two explicitly enumerated assignment requirements (R6 difficulty/reasoning-length bands, R8 cleaning at starved slots) are **absent**, and R6 is stated twice in the source text.

---

## Part 1 — Section-by-section recomputation

Notation: `T` = course-given unique supply (widget 1 `SUPPLY_T`), all figures in B tokens unless stated.

### 1.1 The seven lane shares — do they sum to 100.0?

Stage weights 0.10 / 0.35 / 0.30 / 0.25 on the §6 profiles:

| Lane | 0.10·Seed | 0.35·General | 0.30·Reason | 0.25·Long | **time-avg** | declared |
|---|---|---|---|---|---|---|
| web | 5.40 | 14.35 | 8.10 | 6.00 | **33.85** | 33.9 |
| code | 1.30 | 7.00 | 8.40 | 7.25 | **23.95** | 24.0 |
| reason | 0.20 | 1.40 | 3.90 | 3.00 | **8.50** | 8.5 |
| long | 0.10 | 0.70 | 0.90 | 2.75 | **4.45** | 4.5 |
| indic | 1.60 | 5.95 | 4.50 | 3.75 | **15.80** | 15.8 |
| STEM | 1.20 | 4.90 | 3.60 | 1.75 | **11.45** | 11.5 |
| agentic | 0.20 | 0.70 | 0.60 | 0.50 | **2.00** | 2.0 |
| **sum** | | | | | **100.00** ✅ | **100.2** ❌ |

- The **unrounded** time-average sums to exactly 100.000 and reproduces the declared lanes to a maximum deviation of **0.05 pp** (not "within 0.6pp").
- The **printed** share column sums to `33.9+24.0+15.8+11.5+8.5+4.5+2.0 = 100.2`. Four lanes land on `.x5` and all four round up (+0.05 each = +0.20).
- **FATAL-1.** §1 states verbatim "they sum to 100.0%". As printed they sum to 100.2%. R1/E4 require a 100% partition; the sentence asserting it is false about its own table. Fix: print 33.8 / 24.0 / 15.8 / 11.5 / 8.5 / 4.5 / 2.0 (=100.1) or the exact 33.85/23.95/…/11.45.
- **WEAK-2.** "the weighted time-average reproduces §1 within 0.6pp on every lane" — the true bound is 0.05 pp, 12× tighter. A stated tolerance 12× looser than reality is evidence the check was never run, which is what makes FATAL-1 survive to v3.
- Row sums: Seed 100 ✅, General 100 ✅, Reasoning 100 ✅, Long 100 ✅.
- **FATAL-3.** §6 says "Each row sums to 100%". The **anneal row sums to 97** (20+22+15+3+22+9+6). The missing 3 is `verified-synthetic`, which exists in §4's effective mixture but has no column in §6's table. Either add the column or stop claiming every row sums to 100.
- Stage budgets: 200+700+600+500 = **2000** ✅; 10+35+30+25 = **100** ✅.

### 1.2 Demand = share × 2000B

| Lane | demand from **unrounded** share | spec | demand from **printed** share | delta |
|---|---|---|---|---|
| web | 677.0 | 677 ✅ | 678.0 | −1 |
| code | 479.0 | 479 ✅ | 480.0 | −1 |
| indic | 316.0 | 316 ✅ | 316.0 | 0 |
| STEM | 229.0 | 229 ✅ | 230.0 | −1 |
| reason | 170.0 | 170 ✅ | 170.0 | 0 |
| long | 89.0 | 89 ✅ | 90.0 | −1 |
| agentic | 40.0 | 40 ✅ | 40.0 | 0 |
| **total** | **2000.0** ✅ | | 2004 | |

- Demands are internally consistent and sum exactly to 2000B. **WEAK-1:** but they are computed from the unrounded shares, so the Share and Demand columns in the same table cannot both be right — a reviewer who multiplies 33.9% × 2T gets 678B, not the 677B printed beside it. Four of seven rows are off by 1B this way.

### 1.3 Supply ratios (as the spec computes them)

`677/4500 = 0.1504` ✅ 0.15× · `479/1100 = 0.4355` ✅ 0.44× · `316/276 = 1.1449` ✅ 1.14× · `229/250 = 0.916` ✅ 0.92× · `170/85 = 2.000` ✅ 2.00× · `89/100 = 0.890` ✅ 0.89× · `40/0.63 = 63.49` ✅ 63.5×.

Every one of these reproduces. **The problem is not the division, it is the denominator and the numerator.**

- **FATAL-5 — the ratio column contradicts the spec's own header line.** The spec declares in line 6: "**Selector: OPUS, keep ~40% of candidates**". Widget 3 is explicit that the 6× effective multiplier is defined on *trained* tokens (`~200B actual → ~1.2T effective`), i.e. the 40% keep is a real throughput tax on the pool: to **train** D tokens of a lane you must **offer** D/0.40. Recomputed on that basis:

  | Lane | demand | trainable pool at 40% accept | ratio | spec verdict | correct verdict |
  |---|---|---|---|---|---|
  | web | 677 | 1800 | **0.38×** | covered | covered |
  | code | 479 | 440 | **1.09×** | covered | **repeat** |
  | indic | 316 | 110.4 | **2.86×** | repeat (1.14×) | repeat, 2.5× worse |
  | STEM | 229 | 100 | **2.29×** | covered | **repeat** |
  | reason | 170 | 34 | **5.00×** | repeat (2.00×) | repeat, at the 6-epoch ceiling |
  | long | 89 | 40 | **2.23×** | covered | **repeat** |
  | agentic | 40 | 0.251 | **159×** | 63.5× | 159× |

  Three "covered" verdicts flip to "repeat", and reasoning lands at 5.0 epochs — against Two-Phase's measured 6-epoch HQ-crawl ceiling, i.e. no headroom left, not "comfortably inside".
  *Fair steelman, which the spec never makes:* a token OPUS rejects is not consumed, so it can be re-offered at a later iteration under a different model state, in which case the pre-selector accounting is defensible. That argument is available and is nowhere in the document. As written, §0 and §1 are in direct contradiction and the ratio column is the load-bearing artifact of the whole spec.

- **FATAL-12 — the code lane's own admitted supply cut is never quantified.** §1 says "Effective code supply is therefore **below the 1.10T headline**, but 479B demand stays covered." No number is given. Applying OpenCoder's own measured file-level/repo-level retention (32.74B / 99.47B = **32.9%**) gives effective code supply **362B against 479B demand = 1.32× repeat**, i.e. not covered. The spec names a reduction that could flip its verdict and then declines to compute it, while keeping the verdict.

- **WEAK-11 — total-run exposure is never reported.** Adding the anneal:

  | Lane | main+anneal | /T | | Lane | main+anneal | /T |
  |---|---|---|---|---|---|---|
  | web | 693.2 | 0.154× | | indic | 333.2 | **1.207×** |
  | code | 496.9 | 0.452× | | STEM | 236.1 | **0.944×** |
  | reason | 182.1 | **2.142×** | | long | 91.1 | 0.911× |
  | agentic | 44.96 | **71.4×** | | total | 2080.0 ✅ | |

### 1.4 Inventory reconciliation against widget 9 (rubric E7: "real supply from the inventory")

Recomputed from widget-9 line items:

| Slot | line items | sum | course constant | verdict |
|---|---|---|---|---|
| Code | Stack v2 900 + CommitPack 4 + D3 199 | **1103** | 1100 | ✅ |
| Agentic | 150+120+90+80+60+50+30+25+22 (M) | **627M** | 630M | ✅ |
| Reasoning | OpenThoughts2 3 + OpenMathReasoning 2 + NuminaMath 0.5 + OpenR1-Math 1.6 + **AON (V4) 78** | **85.1** | 85 | ✅ |
| Long-context | Repo-packed 32K+ 60 + Book-length 40 | **100** | 100 | ✅ |
| Indic | 64+24+162+20.9+3+2 | **275.9** | 276 | ✅ |
| Web + STEM | 1300+2600+42+55+164+627+49 | **4837** | 4500 + 250 = 4750 | ⚠ 87B unexplained |

- **WEAK-12 — the STEM 250B is not reconstructible.** The only STEM-shaped entries in widget 9 are peS2o 42B + proof-pile-2 55B + D4 STEM 49B = **146B**. At 146B, STEM demand 229B is **1.57× repeat**, not 0.92× covered — and 2.29× once the OPUS gate is applied. The confidence table half-anticipates this ("0.92× — almost no headroom if inventory is optimistic") but never does the arithmetic, so a reviewer who opens widget 9 gets a number the spec has no answer to. STEM is the lane with the second-thinnest margin in the plan and its supply figure is the least defensible.
- **WEAK-14 — the reasoning lane's 85B is 92% V4 legacy.** `AON (V4 corpus)` is 78B of the 85B. Genuine open reasoning-trace inventory is **7.1B**, of which genuinely *long* distilled traces are **≈4.6B** (OpenThoughts2 3B + OpenR1-Math 1.6B). The spec's "2.0× repeat, comfortably inside the 6-epoch ceiling" is computed against a pool whose composition it never discloses, and whose composition is the whole basis of its "distribution of trace lengths" argument.
- **WEAK-13 — tier C's 5.0B is an assumption, and it is the assumption that forces the biggest Indic deviation.** Widget 9 describes `Sangraha (synthetic)` (162B) as "Sangraha's **synthetic and translated** expansion" and labels it **tier C**. The spec assigns all 162B to tier D and leaves tier C = BPCC 3B + Samanantar 2B = 5.0B, which is what produces the 12.6× failure of the course default and the 20%→8% cut. If any material fraction of the 162B is translated (widget 9 says it is), tier C is fundable at 20% and the deviation is **not forced**. This is the single strongest attack on §2 and there is no prepared answer.

### 1.5 Indic tiers

| Tier | share | demand = share×316 | spec | supply | repeat | spec |
|---|---|---|---|---|---|---|
| A | 40% | 126.40 | 126.4 ✅ | 64.0 ✅ | 1.9750 | 1.98 ✅ |
| B | 30% | 94.80 | 94.8 ✅ | 24+20.9 = 44.9 ✅ | 2.1114 | 2.11 ✅ |
| C | 8% | 25.28 | 25.3 ✅ | 3+2 = 5.0 ✅ | 5.0560 | 5.06 ✅ |
| D | 22% | 69.52 | 69.5 ✅ | 162.0 ✅ | 0.4291 | 0.43 ✅ |
| | 100 ✅ | **316.00** ✅ | | | | |

- Real = 126.4+94.8+25.28 = 246.48 → **78.0%** ✅ / synthetic **22.0%** ✅.
- Course default check: C at 20% = 63.2B / 5.0 = **12.64×** ✅ "12.6×".
- Kill criterion "tier C → 4%, mass to D" closes: C = 12.64B/5.0 = **2.53×** (compliant), D = 26% → real 74.0% / synth 26.0%, still **< 30%** ✅. Credit — this is the only kill criterion in the document whose arithmetic actually closes.
- The 22% synthetic is compliant under **both** readings of Demystifying's ceiling: 22% of the lane < 30%, and 69.52B/2000B = **3.48%** of the run. The spec never states the second, weaker-to-attack reading.

### 1.6 Anneal component tokens

`80 × 0.60 = 48.0` ✅ · overlay 12+10+8+5+2+3 = **40%** ✅ · tokens 9.6 / 8.0 / 6.4 / 4.0 / 1.6 / 2.4 ✅ each · overlay sum 32.0 ✅ · total 48+32 = **80.0** ✅.

### 1.7 Effective anneal mixture

Ballast at unrounded main proportions × 48B, plus overlay:

| Lane | ballast | overlay | total | % of 80 | spec |
|---|---|---|---|---|---|
| web | 16.248 | — | 16.248 | 20.31 | 20.3 ✅ |
| code | 11.496 | 6.4 | 17.896 | 22.37 | 22.4 ✅ |
| reason | 4.080 | 8.0 | 12.080 | 15.10 | 15.1 ✅ |
| long | 2.136 | — | 2.136 | 2.67 | 2.7 ✅ |
| indic | 7.584 | 9.6 | 17.184 | 21.48 | 21.5 ✅ |
| STEM | 5.496 | 1.6 | 7.096 | 8.87 | 8.9 ✅ |
| agentic | 0.960 | 4.0 | 4.960 | 6.20 | 6.2 ✅ |
| v-synth | — | 2.4 | 2.400 | 3.00 | 3.0 ✅ |
| | 48.0 ✅ | 32.0 ✅ | **80.0** ✅ | **100.00** ✅ | 100.1 ⚠ |

**WEAK-4:** the printed percentages sum to 100.1 (rounding). The underlying tokens are exact.
**WEAK-19:** long-context 2.7% is a **pure residue** — it is the ballast share and nothing else, because no long-context component was reserved. It is presented in a table of designed numbers as though it were chosen.

### 1.8 Per-lane anneal epochs — FATAL-4

Against **full-lane** supply, the spec's figures reproduce exactly:
`17.184/276 = 0.0623` ✅ · `12.08/85 = 0.1421` ✅ · `2.136/100 = 0.0214` ✅ · `7.096/250 = 0.0284` ✅ · `4.96/0.627 = 7.91` ✅ "~7.9" · `4.96/0.360 = 13.78` ✅ "≈13.8".

But §4 also declares, three paragraphs later: "**the reserve is selected by a top-5% quality quantile within each lane**". And the components are named as *reserved subsets* — "Tier-A verified Indic", "**Long** reasoning traces", "**Long** agent trajectories". Recomputed against the pool the spec says it draws from:

| Reserved component | tokens | pool the spec names | epochs |
|---|---|---|---|
| Tier-A verified Indic | 9.6 | 5% of 64B = 3.2 | **3.00** |
| Long reasoning traces | 8.0 | 5% of 85B = 4.25 | **1.88** |
| Long reasoning traces | 8.0 | long-trace inventory ≈ 4.6B | **1.74** |
| Long agent trajectories | 4.0 | 5% of 0.627B = 0.031 | **128** |
| Algorithmic code | 6.4 | 5% of 1100 = 55 | 0.12 |
| High-quality STEM | 1.6 | 5% of 250 = 12.5 | 0.13 |

The claim "all far below one epoch, matching Spark Joy's finding that a working reserve is **reweighted, never repeated**" is **false for the two largest reserved components under the spec's own selection rule**, and the Spark Joy support it invokes (Domain-Specific peaks at 0.89 ep, Code at 1.12 ep; the 30% arm where the reserve first crosses 1.0 epoch is where five categories regress) then points the *other* way. Either the reserve is a top-5% quantile — in which case Indic tier A is at 3.0 epochs inside an 80B leg — or the epochs are honest and the top-5% rule is not being applied. The document asserts both.

Separately, the "long reasoning traces 8.0B" component **exceeds the entire long-trace inventory** (≈4.6B in widget 9) regardless of quantile. That is a supply violation on a reserved component, and it is invisible because the epoch column divides by 85B.

### 1.9 Mixture shift — 19.5% (½·L1)

| Lane | main | anneal | \|Δ\| |
|---|---|---|---|
| web | 33.85 | 20.31 | 13.54 |
| code | 23.95 | 22.37 | 1.58 |
| reason | 8.50 | 15.10 | 6.60 |
| long | 4.45 | 2.67 | 1.78 |
| indic | 15.80 | 21.48 | 5.68 |
| STEM | 11.45 | 8.87 | 2.58 |
| agentic | 2.00 | 6.20 | 4.20 |
| v-synth | 0.00 | 3.00 | 3.00 |
| **L1** | | | **38.96** |

**½·L1 = 19.48% → "19.5%" ✅ verified exactly.**
Comparators also verified: Spark Joy `34.35→0, 36.70→30, 7.17→35, 21.78→35` → L1 = 82.10, **½·L1 = 41.05 ✅ "41.1%"**. OpenCoder 84/16 disjoint overlay → ½·L1 = **16 ✅ "~16%"**. "Between the two and closer to the safe one" ✅ (3.5 vs 21.6).

**WEAK-20:** the metric is measured against a *time-average the model never trains on*. The seam the model actually experiences is Long-context stage → anneal, which is ½·L1 = **18.65%** by the same metric. The conclusion survives (18.65 is also closer to 16 than to 41.1), but the stated comparison is the wrong one, and the honest number is 1 pp lower — a free point the spec left on the table.
**Also unstated and free:** the *course preset pair* (24/2/6/6/16/12/34 → 20/8/18/8/28/10/8) is ½·L1 = **32.0%**. The spec's design cuts the course's own seam aggressiveness by 39% and never says so. That is the single best defence of the whole §4/§6 design and it is missing.
**Note on provenance:** ½·L1 is **not** the course's shift metric. Widget 8's model is a per-lane *sharpness* parameter (fraction of the Indic share cut at one seam) with `peakFactor = 1 + effSharp·A·effFrozen`, `A=7`, `F=21.4`; the ~150× figure corresponds to sharpness = 1.0, frozen embeddings, zero warmup band. ½·L1 is the spec's own construct (borrowed from the spark-joy brief). It is a reasonable construct, consistently applied, and I have no objection to it — but it is not traceable to the course, and under widget 8's metric the relevant quantity is the *Indic* jump (15.8→21.5, sharpness ≈ 0.36), which with unfrozen embeddings and no band gives `1 + 0.36×7 = 3.52×` — **above widget 8's own 3.0× instability threshold**. A ≥0.18B band clears it, so the 20B band is comfortably safe; the spec just never runs the course's own model on its own seam.

### 1.10 Seam control

- `20B / 2000B = 1%` per seam ✅.
- **FATAL-10 — seam count.** Five stages (Seed, General, Reasoning, Long-context, Anneal) have **four** transitions: three stage boundaries plus the anneal seam. The spec says "5 seams". Total blended mass is 4×20 = **80B = 4% of the run**, not 5%. (If the run-start LR warmup is being counted, it is not a mixture-shift seam and does not belong in the list.)
- **WEAK-6 — "The 20B seam width is an order-of-magnitude choice, not a measured one" is false.** Two anchors exist in the material the spec is graded against: V4's own production fix was a **~3B-token 60/40 blend at every seam** (widget 8, "V4 REALITY" — our own run, the strongest possible evidence class), and Preference Curriculum's winning S-shape blends over **43.9% of the run ≈ 878B at 2T**. 20B sits between a measured 3B and a measured 878B. Declaring the region unmeasured when the course hands you a measured number from your own previous run is the kind of claim a reviewer will punish, because 20B is **6.7× the V4 band** with no stated reason.
- **WEAK-7 — the 20B anneal band collides with the 4 sub-cycles.** 20B is **25% of the 80B anneal leg**, and the "4 interleaved sub-cycles across the 80B" are 20B each. The blend band therefore consumes exactly the first sub-cycle. Two prescriptions in the same section, unreconciled.
- Corroborations verified: DD Fig 8 "~8 loss spikes to 7.5–8.1" at LR 1e-2 with clipping disabled ✅ · Pref-Curriculum S-shape `1/(1+exp(10(p−0.5)))`, 43.9% ✅, Z-shape hard switch worth ~1.1 avg less (54.7 − 53.6 = 1.1) ✅ · Spark Joy hard-switched 34.35pp with no LR change, no loss curve / perplexity / gradient norm ✅.

---

## Part 2 — The agentic accounting, end to end (rubric E9)

Every figure in §3 verifies:

| Claim | recomputation | verdict |
|---|---|---|
| long trajectories 360M | 150+120+90 = **360** ✅ | verified |
| short format data 267M | 80+60+50+30+25+22 = **267** ✅ | verified |
| unique 0.63B | 360+267 = **627M** ✅ (widget 9 exact) | verified |
| 4-epoch organic = 2.52B | 0.63×4 = 2.52 ✅ (0.627×4 = 2.508) | verified |
| = 0.126% of 2T | 2.52/2000 = **0.126%** ✅ | verified |
| anneal agentic 4.96B | 0.02×48 + 4.0 = **4.96** ✅ | verified |
| total 44.96B | 40 + 4.96 ✅ | verified |
| ~94% generated | (44.96−2.508)/44.96 = **94.4%** ✅ | verified |
| alt "0.2–0.25% = 4–5B at 50–67% real" | 2.508B real is **62.7%** of 4B and **50.2%** of 5B ✅ | verified, and well constructed |

**FATAL-11 — the headline gap is understated.** The spec's marquee number is `40B/0.63B = 63.5×`. The plan's actual agentic exposure is 44.96B, so the whole-plan gap is **44.96/0.627 = 71.4×**. The spec computes 44.96B two lines later and never divides. The number a reviewer will quote back is 71×, not 63.5×.

**Largest agentic share the arithmetic can defend** (requested explicitly). Real unique = 0.627B; "real" = organic tokens at the stated epoch ceiling:

| Constraint | at 4 ep (2.508B real) | at 6 ep (3.762B real) | at 8 ep (5.016B real) |
|---|---|---|---|
| organic only, 0% synth | 2.508B = **0.125%** | 3.762B = **0.188%** | 5.016B = **0.251%** |
| Collapse 80/20 (drift *erased*, Fig 5) | 3.135B = **0.157%** | 4.702B = **0.235%** | 6.270B = **0.314%** |
| Demystifying textbook ≤3% synth | 2.586B = **0.129%** | 3.878B = **0.194%** | 5.171B = **0.259%** |
| Demystifying rephrase ≤30% synth | 3.583B = **0.179%** | 5.374B = **0.269%** | 7.166B = **0.358%** |
| Collapse 50/50 (drift *flattened*) | 5.016B = **0.251%** | 7.524B = **0.376%** | 10.032B = **0.502%** |

- The **defensible band is 0.125% – 0.38%** of 2T (2.5B – 7.5B), taking 4–6 organic epochs and the loosest measured synthetic ceiling. 8 epochs is Two-Phase's *math* ceiling on a 161.5B unique pool, not a licence for a 0.63B pool, so the third column is generous.
- The spec's own "literature-compliant alternative" of **0.2–0.25%** sits exactly inside this band and is arithmetically correct. Credit: this is the most honest number in the document.
- The plan's 2% (44.96B) is **6.0× past the loosest compliant total** (7.524B) and **17.9× the 4-epoch organic real supply**.
- **MISSING-9 — the fallback is also non-compliant, and this is unstated.** The declared kill criterion drops agentic to 0.5% = 10B "= 2.5B real + 7.5B generated = **75% synth**" (checks out: (10−2.508)/10 = 74.9%). 75% synth violates every ceiling §3 has just cited — 30% rephrase, 50/50 flattens, 80/20 erases. So the plan has **no compliant fallback**; the only compliant option is the 0.2–0.25% it names and declines. A reviewer will ask "your Plan B is also 3× outside your own ceilings — what is Plan C?" and there is no answer.
- **FATAL-9 — the kill criterion breaches a course constant.** Widget 1 sets `agentic floor: 2`. §3 justifies 2% *because* "the composer floor encodes a capability commitment", then declares that on proxy failure "**agentic drops to 0.5%**". That breaks the very hard floor the paragraph invokes, and it breaks it below the floor the composer will not even let a slider reach. Also inconsistent with §5, which claims the floor "must be satisfied … in every curriculum cycle".
- **MISSING-1 — the best available defence is absent.** Plan-wide synthetic mass: Indic D 69.52 + agentic generated 42.45 + verified-synthetic/textbooks 2.4 = **114.37B = 5.5% of 2.08T**. Against Demystifying's corpus-wide 30% rephrase ceiling and ≤3% textbook ceiling, the whole plan is comfortably compliant *in aggregate*, and the entire collapse attack can be answered in one line. The spec never computes it. This is the highest-value missing number in the document.
- **E9 judgment.** The disclosure is genuinely loud — §3 is titled "the plan's biggest risk, stated as such", §8 repeats it, the confidence table rates it Low. The spec does not do this *quietly*, so it escapes the letter of E9. But E9's clause is "hands a large share to a lane that has almost no real data behind it **will lose marks**", and disclosure does not un-hand the share: 2% is 6–18× outside every measured ceiling the spec itself cites. Loud honesty converts a fail into a partial credit, not a pass.

**Verified as correct in §3's defence chain:** OpenCoder verified-synthetic snippets kept on unit-tests-pass at **2.71B** ✅ · Collapse Fig 6 window mean absorption **17 → 95 → 216** for K = 1/5/10 ✅ · Collapse 20% synth / 80% real → ten indistinguishable generations ✅ · "synthetic logarithmic in real" ✅ (eq. 11, authors' gloss "exponentially smaller") ✅ · FIM quote and "DeepSeek-V3 is the only surveyed run using it in mid-training" ✅ · "the word 'agent' appears once in the mid-training survey, as a dataset name" ✅ (Agent-FLAN).

---

## Part 3 — FLOP estimates (6ND)

| Claim | recomputation | verdict |
|---|---|---|
| 40B probe on 120B params ≈ 2.9e22 | 6 × 1.2e11 × 4.0e10 = **2.880e22** | ✅ |
| full 2T run ≈ 1.44e24 | 6 × 1.2e11 × 2.0e12 = **1.440e24** | ✅ |
| ~1/50 of a run | 2.88e22 / 1.44e24 = **0.0200 = 1/50** | ✅ exact |
| a dozen probes ≈ 25% of one run | 12 × 0.02 = **24.0%** | ✅ (23.1% against the 2.08T total) |

All four FLOP figures are correct, and the "1/50" is exact rather than approximate. Two notes:

- **WEAK-18 — the two probe protocols in the same sentence are 6× apart.** §7 item 3 cites Llama 3's 40B protocol *and* "OLMo 2 ran 19 such probes totalling 130B tokens". OLMo-2's probes averaged **6.8B**, so 19 of them cost **6.5%** of our run, not 25%. Both numbers are right; putting them in one sentence without reconciling makes the 25% look like the only option when the cheaper precedent is in the same citation.
- **MISSING-5 — the search cost is never computed, and it is the cheapest thing in the plan.** §7 item 1 commits to "112 configurations" with no scale and no cost. At CLIMB's cheap path (62M proxy, 40B tokens each): 112 × 6 × 6.2e7 × 4e10 = 1.67e21 = **0.12% of one run**. At 350M: **0.65%**. Saying so would pre-empt the obvious "you cannot afford 112 runs" push with two digits.
- **FATAL-2 — the Chinchilla sentence is reversed.** Line 8: "it is **above** Chinchilla-optimal for 120B (**~2.4T is compute-optimal**; we are deliberately near it rather than 5–10× past it)". 20 tokens/param × 120B = 2.4T ✅, but **2.00T < 2.4T**, so 2T is *below* compute-optimal, at 0.83×. The clause contradicts itself inside one parenthesis. It also sits oddly beside line 6's "~6× effective tokens", which would put the run at ~12T effective — 5× past Chinchilla, i.e. exactly the regime the sentence claims to avoid and exactly the regime 2503.19206 (cited in the same line) warns about. Either the 6× is real, in which case the overtraining argument reverses, or it is not, in which case §0 should not claim it.

---

## Part 4 — Citation audit (paper-attributed numbers)

**Verified exact** (spot-list; ~60 figures checked, all matched the briefs unless flagged below):

Dataset Decomposition — MDQA-10 `0.8 → 20.8 → 21.2 → 20.4` ✅ · 0.0–0.4 on MDQA-20/30 without D12/D13 ✅ · 8k share `9.4% → 25%` moves MDQA-avg `21.9 → 22.1` ✅ and correctly labelled *noise* ✅ · MDQA-30 `19.6 → 24.6 (+5.0)`, MDQA-avg `23.0 → 28.0` ✅ · long-first `−3.5` regular / `−3.4` MDQA ✅ · `+2.9` regular / `+3.4` LC-avg, `244 vs 304 ms` ✅ · doc-masking `51.5→52.4`, LC `27.5→27.1`, MDQA-30 `20.5→16.0` ✅ · RoPE `+5.4` / `+4.8` ✅ · Grow-P2 1→8 cycles `25.9→28.0` MDQA and CSR `60.9→62.8` ✅ · natural `9.4%` at 8192, `22.9%` ≥4k ✅ · attention ~5% of FLOPs at 120B ✅ (brief: 5.3%) · empty-bucket exclusion quote ✅.
Two-Phase — `64.44%` Low; MMLU `42.94 → 56.10` ✅ · 6 epochs HQ crawl / 8 math / 12 hurts ✅ · order = `+3.4` avg, GSM8K `30.86→40.33`, code `35.55→38.33`, MMLU `56.49→56.28` ✅ · "best 40%" is a different object ✅.
OpenCoder — `~75%` exact-dupe files ✅ · file-level `32.74B (2.4% of 485M files)` ✅ · repo-level `99.47B (7.5%)` ✅ · `52B` char-identical ✅ · chunk-after-file `−0.04B` ✅ · stars≥5: HumanEval `~0.12 vs 0.18`, MBPP `~0.14 vs 0.20`, lower loss ✅ · Fig 9 HumanEval `~0.33 vs ~0.47`, gap never closes ✅ · `2.71B` verified snippets ✅ · 84/16 ✅ · 100B/2.6T = 3.85% ✅.
Spark Joy — 50/100/200/300B sweep ✅ · MMLU peak `43.19` at 100B, Core Avg `39.32` at 200B ✅ · no point below 50B ✅ · base `34.35/36.70/7.17/21.78` → DU `0/30/35/35` ✅ · filtered web held at 30% = `0.82×` with the "prevent a large distribution shift" quote ✅ · Domain-Specific `0.89` ep, Code `1.12` ep ✅ · 30% arm is where the reserve first crosses 1.0 and where five categories regress ✅ · sans-math MMLU `29.71 vs 35.69 (−5.98)`, RC `26.48 vs 37.02 (−10.54)`, Core Avg `−2.83`, 100B leg ✅ · `41.1%` shift ✅ · silence on loss/ppl/grad-norm ✅ · MMLU peak gap `0.60pp`, Core Avg `0.86pp` ✅.
Mid-Training Survey — Cluster A `1.96 / 1.48 / 3.85 / 4.00 / 4.76 / 1.96` ✅ all six · Cluster B `9.03 / 11.11 / 14.08 / 16.67 / 51.28` ✅ all five · overlay band `84/16, 60/40, 70/30, 75/25, 60/40, 70/30` ✅ · catastrophic-forgetting quote ✅ · Hunyuan-Large "5% of the highest-quality pre-training tokens" ✅ and **"8× stricter than OPUS's ~40%"** ✅ — note this *corrects* the brief and EVIDENCE_MAP, which both say 10× · OLMo-2 presence quote ✅ · MAP-Neo Chinese `25% → 8.5%` ✅ · Yi-Lightning qualitative, no percentages ✅ · Llama 3 8B `+24.0%` GSM8K / `+6.4%` MATH, "negligible uplift for the 405B model" ✅ · OLMo-2 `+10.6` ✅ · ABF θ≈10⁶ + YaRN `α(s)=0.1·ln s+1` ✅ · OLMo 2 `50B on 4T (1.25%)` / `100B on 5T (2%)` ✅ · Llama 3 probe: 50%-trained, LR→0 over 40B, 30/70 ✅ · 19 probes / 130B ✅.
Collapse — `17→95→216` ✅ · 50% flattens L1, 80% erases drift ✅ · logarithmic bound ✅ · Thm 2/3 framing ✅.
Preference Curriculum — Fig 6b ArXiv `88/12`, GitHub `66/34`, Wikipedia `14/86` ✅ · "does not skew towards specific sub-domains" self-contradiction ✅ · Spearman `0.41` ✅ · S-shape formula and `43.9%` ✅ · Z-shape `~1.1` worse ✅ · indistinguishable for first ~35%, loss worse for first ~40% ✅.
CLIMB — 62M `60.11` vs 350M `60.41` ✅ · `64+32+16 = 112` at 4:2:1 ✅ · RegMix `59.37` / DoReMi `59.16` / Random `57.93` ✅ · C20 → 0 ✅ · Figs 5/7 different objectives → different winners ✅ · from-scratch top-3 ≈ `64%` vs continuous one cluster at `43%` ✅ · checklist Q7 = No ✅.
Demystifying — rephrase `<50%` at every scale ✅ · textbooks `≤3%` at 50B, often 0% below 10B ✅ · App D.2 uncovered unigrams spike per-token loss ✅.

**Problems found:**

- **FATAL-6 — Spark Joy Language Understanding is misread.** §4 writes: "Language Understanding was still negative at every phase length (**−0.47 / −1.11 / −1.44 / −1.17 on LAMBADA / HellaSwag / Winograd / WinoGrande**)". Those four numbers are the LU **category deltas at the 5% / 10% / 20% / 30% phase lengths**. LAMBADA/HellaSwag/Winograd/WinoGrande are the four *constituent tasks* of that category, and the paper reports no per-task values. Four numbers have been attached to the wrong axis. The finding survives intact (LU is negative at every length ✅) but the parenthesis is wrong and a reviewer holding Table 6 will catch it in ten seconds.
- **WEAK-8 — an untraceable quotation.** §4: `Nemotron-4 "majority already-seen tokens reweighted."` Nothing in the survey brief supports this as a quotation; the survey's Nemotron-4 statement is that its second distribution "up-weights domains where the model underperforms". Either de-quote it as a paraphrase or cite Nemotron-4 2406.11704 directly.
- **WEAK-9 — "Published analogue" that is not published.** §6: "Published analogue: MiniMax-01 uses **linear interpolation of source-specific weights** across mixture transitions." The survey brief is explicit that this string exists **only as commented-out LaTeX in the arXiv source and is absent from the published paper**, with the instruction to cite MiniMax-01 2501.08313 instead. The claim is probably true; the sourcing as "published" is not.
- **WEAK-10 — right finding, wrong scale.** §5 leans on Collapse's "50% real flattens L1, **80% real erases** generation drift" as one of four supports for the floor. Those are two mix points on an **8-layer, 256-dim, char-level nanoGPT trained on one Shakespeare play**, and the brief says in terms: "Do not quote 50% or 80% real as a universal collapse threshold." The theorem is a *logarithmic* bound, not a percentage. §8's blanket error-bar disclaimer does not cover a scale gap of nine orders of magnitude.
- **WEAK-11 — "measured" overstates one ceiling.** "Demystifying Synthetic's **measured** rephrase ceiling (best ~30%…)". The fine grid **skips 30%** (points are 20% and 50%); ~30% is interpolated from the 20-vs-50 comparison plus the coarse 33% cell. "<50%" is measured; "~30%" is inferred.
- **WEAK-5 — the long-context inference reaches past its evidence in a way §8 does not cover.** §6 claims "This is where most long-context capability actually comes from … the natural 8k-contiguous tail is on the order of hundreds of billions of tokens … far more than the 100B curated long-context inventory." The *pool* arithmetic is right: 9.4% × 4500 = **423B** ✅. But the *trained* arithmetic is not stated and it inverts the comparison: at 677B of served web, 8k-contiguous exposure is `0.094 × 677 = 63.6B` — **less than the 100B curated inventory** — and the run's total mass at ≥8k is `(63.6+89)/2000 = 7.6%`, below the **9.4%** that is DD's lowest measured non-zero long share. So the mixture sits below every setting DD measured, on the one axis DD proved is a threshold. §8 admits "the 2–9% region is unmeasured" for the *lane*, but not that the *packing* argument replacing the lane also lands below the measured floor.
- **WEAK-16 — mismatched denominators.** "file-level … 32.74B Python tokens (**2.4% of 485M files**); repo-level keeps 99.47B (**7.5%**)". The 7.5% is of **11.0M repos**, not of files. Presented side by side, it reads as one series.
- **WEAK-3 — the anneal fraction is computed on a different base from its comparators.** 80/2000 = 4.0% is a fraction of the *main run*; every Cluster A figure the spec cites (1.96 / 1.48 / 3.85 / 4.00 / 4.76) is reserve ÷ *total* tokens. Like-for-like, our anneal is **80/2080 = 3.85%** — which happens to be exactly OpenCoder's figure and is a *better* number for the argument. The verdict ("Cluster A at its high end") does not change, but the comparison as written is apples-to-oranges.

**Not fabricated, and checked:** 2503.19206 (overtraining) and 2309.16039 (Xiong et al.) are both real and both appear in the briefs' follow-on lists ✅. MILU / IndicGenBench / SWE-bench / τ-bench / BFCL / GAIA / BrowseComp appear in **none** of the nine papers and in none of the widgets — they are real benchmarks but are outside the evidence base, and the spec does not flag them as such (see MISSING-8).

---

## Part 5 — Deviations from the course preset: forced, or chosen?

Rubric rule 9: taste-only deviations are WEAK at minimum.

| Deviation | spec's stated reason | is the arithmetic forcing? | verdict |
|---|---|---|---|
| **long-ctx 6% → 4.5%** | DD threshold + `9.4→25%` moves MDQA-avg `21.9→22.1` (noise) ⇒ "useful share is bounded around ≤10%" | **No.** The cited evidence bounds the share from *above* at ~10% and says nothing between 0% and 9.4%. It cannot distinguish 6% from 4.5%; DD's own brief says the 2–9% region is unmeasured. Worse, 4.5% is below widget 1's `WEIGHTED_MIN = 8` ("a lane needs at least this share to move its benchmarks"), so by the course's own rule the lane is **starved** while §1 claims it must win five benchmarks. | **WEAK** — chosen, not forced; and it deepens a course-defined starvation |
| **reasoning 6% → 8.5%** | "a *distribution* of trace lengths, not one slot" | **No** as argued — that is taste. **Yes** if argued from the course: widget 1's `WEIGHTED_MIN = 8` makes 6% an unfunded lane and ≥8% a funded one, which forces the direction and roughly the size. The spec had an arithmetically forced justification available and used a qualitative one instead. Supply also worsens: 2.00× → 5.00× post-OPUS. | **WEAK** — right answer, wrong defence |
| **anneal 2% → 4% (80B)** | Cluster A 1–5%; Spark Joy has no point below 50B and 80B sits between 50B and 100B; OLMo-2 ships 50B/4T and 100B/5T | **Largely yes.** This is the best-defended deviation in the document: the absolute-token reading is correct, 40B is genuinely below every measured point, and the Cluster A/B distinction is real and correctly drawn. Only the denominator is sloppy (WEAK-3). | **DEFENSIBLE** |
| **Indic tiers 40/25/20/15 → 40/30/8/22** | tier C at 20% needs 63B against 5.0B = 12.6× | **Conditionally yes** — the arithmetic is exact *given* that tier C's supply is 5.0B. But that premise discards the translated half of a 162B set that widget 9 labels **tier C** and describes as "synthetic **and translated** expansion" (WEAK-13). The deviation is forced by an unexamined inventory assumption, not by the inventory. | **WEAK** — forced by an assumption, not by the data |
| **anneal web 8% → 20.3%** | Spark Joy held filtered web at 30% (0.82×) to prevent shift, and LU was still negative at every length | **Yes.** Cleanest evidence-to-number link in the spec. | **DEFENSIBLE** |
| **anneal long 8% → 2.7%** | none | not defended; and it is a residue, not a choice (WEAK-19) | **WEAK-17** |
| **anneal indic 28% → 21.5%** | discussed vs MAP-Neo, never framed as a deviation | not defended *as a deviation* | **WEAK-17** |
| **anneal agentic 8% → 6.2%** | none | not defended | **WEAK-17** |
| **anneal reason 18% → 15.1%** | none | not defended | **WEAK-17** |

Four of seven anneal lanes deviate from a course preset with no stated reason. Per rubric rule 9 that is four WEAKs, and they are cheap to fix because the effective mixture is a *derived* quantity — the spec could simply say so.

---

## Part 6 — Requirement-level findings not yet covered

- **FATAL-7 (R3).** "names the agentic and reasoning and long-context slots explicitly and **points each one at the datasets from the inventory** that will fill it." Agentic: nine datasets named with token counts ✅ (SWE-Gym 150M … Hermes 22M — all nine match widget 9 exactly). Indic: five named ✅ (not required, but credited). **Reasoning: zero inventory datasets named.** OpenThoughts2, OpenMathReasoning, NuminaMath, OpenR1-Math, AON appear nowhere in the spec. **Long-context: zero.** `Repo-packed code (32K+)` 60B and `Book-length corpora (packed)` 40B appear nowhere; the lane is referred to only as "the 100B curated long-context inventory". Two of the three slots the assignment names by hand are unpointed. This is the single most mechanical requirement in the assignment and it is 1-for-3.
- **FATAL-8 (R6 / E10, weighted twice).** The assignment says "lays out the **difficulty and reasoning-length bands with a concrete example for each**" and the evaluation paragraph repeats it as "**with a real example at each level**". The spec has a "Difficulty band" column reading `B0–B1 / B1–B2 / B2–B3 / B3–B4 / B4–B5` — **bare labels, no definitions, no examples** — and one sentence of reasoning-length ("Short and medium traces in the Reasoning stage; long traces reserved for the anneal") naming **3 of the course's 4 tiers** (`ultra` is missing), with no token ranges and no worked example. The source material is sitting in the widgets: widget 7 defines B0 Nursery "simple children's sentences" → B5 Research/PhD "research and PhD-grade papers", each with an example string; widget 6 gives low/medium/high/ultra with step counts, token counts and a fully worked problem. A requirement stated twice, with the raw material supplied, and not done.
- **FATAL-13 (R4 ambiguity — rubric rule 7 says ambiguity here is FATAL).** §5 fixes "**8% of every iteration's accepted tokens … for Indic + agentic + reasoning**" — an **aggregate** floor. The course's floors are **per-lane** (`indic ≥ 12`, `agentic ≥ 2`). An aggregate 8% can be satisfied entirely out of Indic while agentic goes to zero — i.e. the floor gives **no protection at all to the scarcest lane, which is the lane the floor exists for**. The spec never decomposes it. Mitigation, which is real: the §6 stage table pins agentic at exactly 2 in every stage and Indic ≥15, so the per-lane constraint survives in the mixture; and §5's per-bucket/per-cycle/real-token clauses are the operative content. But R4's verb is "fixes", and what is fixed is the weaker of the two available constraints.
- **MISSING-2 — the floor never binds, and this is not acknowledged.** Indic+agentic+reasoning by stage: Seed 20%, General 23%, Reasoning 30%, Long-ctx 29%, anneal 42.8%, main-run average 26.3%. The aggregate floor is slack by **2.5× to 5.4× everywhere**. So "the hard protected floor (§5)" advertised in line 6 can never actually be crossed by this mixture, and a reviewer asking "when does your floor bite?" gets no answer. The honest framing — that the 8% aggregate is inherited from V4 and is a backstop against selector pathology rather than a binding constraint, and that the *real* protections are the per-bucket and real-token clauses — is stronger and is not made.
- **MISSING-3 — no training sequence length is ever declared.** §6's entire packing argument is built on binary decomposition into D6…D13 buckets, i.e. a max context of **8192** (and DD trains nothing longer). But the long-context inventory the lane is drawn from is `Repo-packed code (**32K+**)` and packed book-length documents. A 32K sequence in an 8K run is decomposed into four 8K spans, which is fine — but it means the "long-context lane" is not long-context beyond 8K, the inventory's defining property is discarded, and §8's "Long-context evidence stops at 8192" reads as a limitation of the *literature* when it is also a limitation of the *plan*. The number that resolves this (the run's context length) is absent.
- **MISSING-6 (R8).** "Alongside the plan the cleaning continues toward the cumulative target, now aimed at **the slots the mixture shows to be starved**." The spec never identifies starved slots or points cleaning at them. It is a one-paragraph fix and the analysis is already implicit: by widget 1's ≥8% funding rule the starved slots are **long-context (4.5%)** and **agentic (2.0%)**; by supply the starved slots are **agentic (71×)**, **Indic tier C (5.06×)**, **reasoning long-trace inventory (8.0B reserved against ≈4.6B)** and **STEM if the 146B reconstruction is right**. Nothing in the document says "clean here next".
- **MISSING-8 (E6).** The benchmark column is labelling, not magnitude justification. Not one lane share in the document is derived from a benchmark requirement. The sharpest instance: long-context is cut to 4.5% and agentic held at 2.0% — both **below the course's own ≥8% "funds its benchmarks" line** — while the same table asserts they "must win" LongBench/RULER/MDQA/TOEFL/QuALITY and SWE-bench/τ-bench/BFCL/GAIA/BrowseComp respectively. E6 asks a reviewer to "see **why each number is what it is**" from the benchmark tie; here the benchmark tie actively contradicts two of the numbers, and the ≥8% rule is never mentioned.
- **MISSING-4 (E11).** No proxy has a numeric pass/fail threshold. "Does not beat a format-data-only baseline" and "degrades IndicGenBench" name metrics but no margins — and §8 itself establishes that the relevant noise floor is 0.6–0.9 pp single-seed, so an unquantified "beats" is not gradeable. E11's "highest" tier requires "names the metric that would confirm or refute their mixture"; metrics are named, decision rules are not.
- **MISSING-10.** Two anneal components point at nothing in the inventory: "Algorithmic / competition code **6.4B**" (widget 9's code slot is Stack v2 / CommitPack / D3 — there is no algorithmic or competition-code entry; OpenCoder's 12.44B keyword sample is a paper artifact, not our supply) and "Verified synthetic + textbooks **2.4B**" (no entry at all — it is data that does not exist yet, which is fine, but should be labelled *to be generated* like the agentic lane is).

---

## Part 7 — PADDING (E3: "padding earns nothing")

| # | What | Why it earns nothing | Cut |
|---|---|---|---|
| P1 | §4 table column **"Epochs on unique"** — 7 rows, every cell `—` | An entirely empty column. The epochs are in the prose below it. | Delete the column |
| P2 | §6 "For a later 32k–128k extension the survey's default is ABF θ ≈ 10⁶ plus YaRN temperature α(s) = 0.1·ln s + 1" | §8 explicitly disclaims any 32k/128k claim. Serves no R1–R8 clause; it is a correct fact about a phase that is out of scope. | Delete the sentence (keep RoPE 100k, which is a real data-prep decision) |
| P3 | §6 step-time numbers `244 ms vs 304 ms`, "20% faster" | The confidence table concedes the speed half shrinks to ~5% at 120B, so the ms figures argue for nothing at our scale. The accuracy half (+2.9/+3.4) is load-bearing and should stay. | Cut the ms and the "20% faster" |
| P4 | §3 items 3 and 4 (Collapse window `17→95→216`; the 20/80 ten-generation run) | Four numbers refuting a self-consuming loop the plan does not propose. One clause ("we use a frozen external teacher and keep real trajectories in every batch, both outside Collapse's family") does the same work. | Merge into one item |
| P5 | The 23-row **Confidence summary** | Restates §1–§7 verdicts. It helps E1/E2 a little, but 23 rows of "Medium-high / no published sweep" is the largest non-gradeable block in the document. Only the closing line ("the three numbers a reviewer should attack first") earns marks. | Compress to ~6 rows + the closing line |
| P6 | §7 item 6 ("Expect a curriculum to pay late", ~35%/~40%) | True and well cited, but it is advice about reading mid-run evals, not a number in the mixture. Borderline — keep if compressed to one clause. | Compress |

Rough total cuttable: **15–20% of the document**, all of it without losing a single gradeable number. Note the counterpoint: §8 ("What this plan does not have evidence for") looks like padding and is **not** — under E2 it is one of the highest-value sections in the spec, and it pre-empts four reviewer attacks outright.

---

## Part 8 — Master table: every number in the spec, with verdict and defence

Defence key: **paper** = traceable to a brief · **course** = widget/lecture constant · **arith** = derived in-document · **taste** = asserted · **none** = undefended.

| # | Number | Recomputation / check | Verdict | Defence traceable? |
|---|---|---|---|---|
| 1 | 120B params | declaration | verified (given) | course |
| 2 | main run 2.00T | declaration | verified (given) | course |
| 3 | anneal +80B | 80/2000 = 4.0% | verified | paper (Cluster A) |
| 4 | 4.0% of main | ✅; like-for-like is 3.85% of 2.08T | **off-by-base** | paper, wrong denominator |
| 5 | total 2.08T | 2000+80 | verified | arith |
| 6 | OPUS keep ~40% | widget 3 | verified | course |
| 7 | ~6× effective tokens | widget 3 (200B→1.2T) | verified | course; **contradicts #10** |
| 8 | ~2.4T compute-optimal for 120B | 20×120B = 2.4T ✅ | verified | paper (Chinchilla) |
| 9 | "2T is **above** Chinchilla-optimal" | 2.0 < 2.4 | **FATAL-2, reversed** | none |
| 10 | "deliberately near it rather than 5–10× past" | at 6× effective the run is ~12T eff = 5× past | **contradicts #7** | none |
| 11 | 10T → 200B agentic | 0.02×10T | verified | arith |
| 12 | 2503.19206 overtraining | real paper, in briefs | verified | paper |
| 13 | web 33.9% | 33.85 | verified (rounds up) | arith |
| 14 | code 24.0% | 23.95 | verified (rounds up) | arith |
| 15 | indic 15.8% | 15.80 | verified exact | arith |
| 16 | STEM 11.5% | 11.45 | verified (rounds up) | arith |
| 17 | reason 8.5% | 8.50 | verified exact | arith |
| 18 | long 4.5% | 4.45 | verified (rounds up) | arith |
| 19 | agentic 2.0% | 2.00 | verified exact | course floor |
| 20 | "**they sum to 100.0%**" | printed sum = 100.2 | **FATAL-1** | arith, false |
| 21 | demand 677 / 479 / 316 / 229 / 170 / 89 / 40 | sum = 2000.0 ✅, all exact off unrounded | verified | arith |
| 22 | share×2000 vs printed demand | 678/480/230/90 ≠ 677/479/229/89 | **off-by-1B ×4** | arith, inconsistent |
| 23 | supply 4.5T / 1.1T / 276B / 250B / 85B / 100B / 0.63B | widget 1 ✅; widget 9 confirms all but STEM | verified except #24 | course |
| 24 | STEM 250B | widget-9 line items = 146B → 1.57× | **unsupported by inventory** | course constant only |
| 25 | ratios 0.15 / 0.44 / 1.14 / 0.92 / 2.00 / 0.89 / 63.5× | all reproduce | verified as computed | arith |
| 26 | verdicts covered/repeat/must-generate | ignore the 40% OPUS gate | **FATAL-5** | none |
| 27 | post-OPUS ratios (not in spec) | 0.38/1.09/2.86/2.29/5.00/2.23/159× | **missing** | — |
| 28 | "effective code supply below 1.10T" | never quantified; ≈362B at OpenCoder retention → 1.32× | **FATAL-12** | none |
| 29 | MDQA-10 0.8→20.8→21.2→20.4 | brief ✅ | verified | paper |
| 30 | 0.0–0.4 without 4k/8k buckets | brief ✅ | verified | paper |
| 31 | 9.4% → 25% moves 21.9→22.1 | brief ✅, correctly called noise | verified | paper |
| 32 | "useful share bounded ≤10%" | upper bound only; 2–9% unmeasured | **WEAK, over-read** | paper, partial |
| 33 | long-ctx 6→4.5 deviation | not forced; below course ≥8% funding line | **WEAK** | taste |
| 34 | reason 6→8.5 deviation | direction forced by widget-1 ≥8%, not cited | **WEAK** | taste |
| 35 | 170B vs 85B = 2.0× | ✅; 5.00× post-OPUS; 92% of pool is V4 AON | verified-as-stated | arith |
| 36 | 6 ep crawl / 8 math / 12 hurts | brief ✅ | verified | paper |
| 37 | CC 64.44% Low; MMLU 42.94→56.10 | brief ✅ | verified | paper |
| 38 | stars≥5: HE 0.12 vs 0.18, MBPP 0.14 vs 0.20 | brief ✅ | verified | paper |
| 39 | ~75% GitHub files exact dupes | brief ✅ | verified | paper |
| 40 | 32.74B (2.4% of 485M files) | brief ✅ | verified | paper |
| 41 | 99.47B (7.5%) | ✅ but 7.5% is of **repos** | **WEAK, mixed denominator** | paper |
| 42 | 52B char-identical | brief ✅ | verified | paper |
| 43 | chunk-after-file −0.04B | brief ✅ | verified | paper |
| 44 | composer A40/B25/C20/D15 | widget 1 ✅ | verified | course |
| 45 | tier C default 63B vs 5.0B = 12.6× | 63.2/5 = 12.64 | verified | arith |
| 46 | tier demands 126.4 / 94.8 / 25.3 / 69.5 | sum 316.0 ✅ | verified | arith |
| 47 | tier supplies 64.0 / 44.9 / 5.0 / 162.0 | widget 9 ✅ | verified | course |
| 48 | tier C supply = 5.0B (excludes translated half of Sangraha-synth) | widget 9 tags the 162B **tier C**, "synthetic **and translated**" | **WEAK-13, premise unexamined** | none |
| 49 | repeats 1.98 / 2.11 / 5.06 / 0.43× | all reproduce | verified | arith |
| 50 | real 78% / synth 22% | 246.48/316 ✅ | verified | arith |
| 51 | rephrase ceiling ~30%, always <50% | <50% measured; ~30% interpolated | **WEAK, "measured" oversold** | paper |
| 52 | textbook ceiling ≤3% @50B, 0% <10B | brief ✅ | verified | paper |
| 53 | ~150× V4 gradient spike | widget 8 ✅ (sharpness 1.0 + frozen + no band) | verified | course |
| 54 | Spearman 0.41 | brief ✅ | verified | paper |
| 55 | ArXiv 88 / GitHub 66 / Wikipedia 86 | brief ✅ | verified | paper |
| 56 | MAP-Neo Chinese 25→8.5 | brief ✅ | verified | paper |
| 57 | anneal raises Indic 15.8→21.5 | 17.184/80 = 21.48 ✅ | verified | arith |
| 58 | agentic 360M long-trajectory | 150+120+90 ✅ | verified | course (widget 9) |
| 59 | agentic 267M format data | 80+60+50+30+25+22 ✅ | verified | course |
| 60 | unique 0.63B | 627M ✅ | verified | course |
| 61 | 4-epoch ceiling | asserted; Two-Phase measured 6/8 on 100B+ pools | **WEAK (conservative, unsourced)** | taste |
| 62 | 2.52B = 0.126% of 2T | ✅ (0.627×4 = 2.508) | verified | arith |
| 63 | 44.96B total exposure | 40 + 4.96 ✅ | verified | arith |
| 64 | ~94% generated | 94.4% ✅ | verified | arith |
| 65 | 63.5× gap | whole-plan figure is **71.4×** | **FATAL-11, understated** | arith, incomplete |
| 66 | OpenCoder 2.71B verified snippets | brief ✅ | verified | paper |
| 67 | Collapse 17→95→216 | brief ✅ | verified | paper |
| 68 | 20% synth / 80% real, ten generations | brief ✅ (nanoGPT scale) | verified | paper |
| 69 | synthetic must be logarithmic in real | eq. 11 ✅ | verified | paper |
| 70 | agentic → 0.5% kill criterion | breaches course `agentic ≥ 2` floor | **FATAL-9** | none |
| 71 | 0.5% = 10B = 2.5 real + 7.5 gen = 75% synth | arithmetic ✅; 75% violates every cited ceiling | **verified but non-compliant** | arith |
| 72 | alt 0.2–0.25% = 4–5B at 50–67% real | 2.508B = 62.7% of 4B, 50.2% of 5B ✅ | **verified, best number in the doc** | arith + paper |
| 73 | defensible band (not in spec) | 0.125%–0.376% of 2T | **missing** | — |
| 74 | plan-wide synthetic (not in spec) | 114.37B = **5.5%** of 2.08T | **missing (MISSING-1)** | — |
| 75 | ballast 60% = 48.0B | ✅ | verified | paper (10–40% overlay band) |
| 76 | overlay 12/10/8/5/2/3% = 40% | ✅ sums to 32.0B | verified | arith |
| 77 | 9.6 / 8.0 / 6.4 / 4.0 / 1.6 / 2.4B | all ✅ | verified | arith |
| 78 | effective anneal 20.3/22.4/21.5/15.1/8.9/6.2/2.7/3.0 | all ✅ to 2 dp; printed sum 100.1 | verified (rounding) | arith |
| 79 | anneal epochs 0.062/0.142/0.021/0.028 | ✅ vs full lane; 3.00/1.88 vs the spec's own top-5% rule | **FATAL-4** | arith, wrong pool |
| 80 | agentic anneal ~7.9 ep / ≈13.8 on trajectories | 4.96/0.627 = 7.91; 4.96/0.360 = 13.78 ✅ | verified | arith |
| 81 | "long reasoning traces" 8.0B | exceeds ≈4.6B long-trace inventory | **FATAL (supply)** | none |
| 82 | algorithmic/competition code 6.4B | no inventory entry | **unsupported** | none |
| 83 | verified synthetic + textbooks 2.4B (3.0% of anneal) | 3.0% ✅; = 0.115% of run, compliant | verified | paper |
| 84 | Spark Joy 0.89 / 1.12 epochs | brief ✅ | verified | paper |
| 85 | Cluster A 1.96/1.48/3.85/4.00/4.76/1.96 | all six ✅ | verified | paper |
| 86 | Cluster B 9.03/11.11/14.08/16.67/51.28 | all five ✅ | verified | paper |
| 87 | Spark Joy 50/100/200/300B; peaks 43.19 @100B, 39.32 @200B | ✅ | verified | paper |
| 88 | OLMo 2 50B/4T = 1.25%, 100B/5T = 2% | ✅ | verified | paper |
| 89 | OpenCoder Fig 9 ~0.33 vs ~0.47 | ✅ | verified | paper |
| 90 | overlay precedents 84/16, 60/40, 70/30, 75/25, 60/40, 70/30 | all ✅ | verified | paper |
| 91 | Nemotron-4 "majority already-seen tokens reweighted" | not traceable as a quote | **WEAK-8** | none |
| 92 | Spark Joy web 34.35→0, filtered 30% (0.82×) | ✅ | verified | paper |
| 93 | LU −0.47/−1.11/−1.44/−1.17 "on LAMBADA/HellaSwag/Winograd/WinoGrande" | those are the **four phase lengths**, not four tasks | **FATAL-6** | paper, misread |
| 94 | our anneal web 20.3% | ✅ | verified | paper (best-defended deviation) |
| 95 | mixture shift 19.5% (½L1) | **19.48** ✅ exact | verified | arith |
| 96 | Spark Joy 41.1% | 41.05 ✅ | verified | paper |
| 97 | OpenCoder ~16% | 16.0 ✅ | verified | arith |
| 98 | (not in spec) course preset pair = 32.0%; Long-stage→anneal = 18.65% | both computed above | **missing** | — |
| 99 | Hunyuan top-5%, "8× stricter than 40%" | 40/5 = 8 ✅ (corrects the brief's "10×") | **verified + corrects source** | paper |
| 100 | 4 interleaved sub-cycles | DD used 8; §confidence admits it is an inference | **WEAK (declared)** | paper, partial |
| 101 | DD Grow-P2 1→8: 25.9→28.0, CSR 60.9→62.8 | ✅ | verified | paper |
| 102 | floor = 8% of accepted tokens | widget 3 `LANE_FLOOR=0.08`, lecture ✅ | verified | course |
| 103 | floor is **aggregate** over 3 lanes | course floors are per-lane (12 / 2) | **FATAL-13 (ambiguity)** | course, weakened |
| 104 | floor slack (not in spec) | min 20% in Seed vs 8% ⇒ never binds | **missing (MISSING-2)** | — |
| 105 | proxy direction [0.70, 0.53, 0.33] | widget 3 ✅ | verified | course |
| 106 | CLIMB C20 → 0 | ✅ | verified | paper |
| 107 | Collapse 50% flattens / 80% erases | ✅ but nanoGPT char-level scale | **WEAK-10, wrong scale** | paper |
| 108 | Spark Joy sans-math −5.98 / −10.54 / −2.83 from 100B | ✅ | verified | paper |
| 109 | stage budgets 200/700/600/500 | sums 2000 ✅, 100% ✅ | verified | arith |
| 110 | stage rows sum 100 (×4) | ✅ | verified | arith |
| 111 | anneal row sums 100 | **= 97** | **FATAL-3** | arith, false |
| 112 | B0–B5 difficulty bands | labels only, no definition, no example | **FATAL-8 (R6/E10)** | none |
| 113 | reasoning-length bands | 3 of 4 course tiers, no ranges, no example | **FATAL-8 (R6/E10)** | none |
| 114 | order worth +3.4 avg; GSM8K 30.86→40.33; code 35.55→38.33; MMLU 56.49→56.28 | all ✅ | verified | paper |
| 115 | top-3 ≈ 64% vs one cluster at 43% | ✅ | verified | paper |
| 116 | MDQA-30 19.6→24.6 (+5.0); MDQA-avg 23.0→28.0; −3.5/−3.4 long-first | all ✅ | verified | paper |
| 117 | +2.9 / +3.4 / 244 vs 304 ms | ✅ (speed is P3 padding at 120B) | verified | paper |
| 118 | doc-masking 51.5→52.4 / 27.5→27.1 / 20.5→16.0 | ✅ | verified | paper |
| 119 | 9.4% @8192, 22.9% ≥4k, "hundreds of billions" | 0.094×4500 = **423B** ✅ pool | verified | paper |
| 120 | "far more than the 100B curated inventory" | trained 8k web = **63.6B < 100B**; run mass ≥8k = 7.6% < DD's 9.4% floor | **WEAK-5, inverts when trained** | paper, partial |
| 121 | RoPE 100k: +5.4 / +4.8, regular unchanged | ✅ (baseline moved 51.3→51.5) | verified | paper |
| 122 | ABF θ≈10⁶, YaRN α(s)=0.1·ln s+1 | ✅ | **PADDING-2** | paper |
| 123 | 20B band = 1% per seam | ✅ | verified | arith |
| 124 | **5 seams** | 4 transitions; 4×20 = 80B = 4% | **FATAL-10** | arith, wrong |
| 125 | "20B width unmeasured" | V4 = ~3B (course); PrefCurr = 43.9% ≈ 878B | **WEAK-6, false** | none |
| 126 | S-shape 43.9%, Z-shape −1.1 | ✅ | verified | paper |
| 127 | MiniMax-01 "published analogue" | commented-out LaTeX, not published | **WEAK-9, mis-sourced** | paper, wrong venue |
| 128 | 62M 60.11 vs 350M 60.41 | ✅ | verified | paper |
| 129 | 112 = 64+32+16 at 4:2:1 | ✅ | verified | paper |
| 130 | RegMix 59.37 / DoReMi 59.16 / Random 57.93 | ✅ | verified | paper |
| 131 | probe cost 2.9e22 | 2.880e22 ✅ | verified | arith (6ND) |
| 132 | full run 1.44e24 | 1.440e24 ✅ | verified | arith |
| 133 | ~1/50 of a run | 0.0200 ✅ exact | verified | arith |
| 134 | dozen probes ~25% | 24.0% ✅ | verified | arith |
| 135 | OLMo 2: 19 probes, 130B | ✅ but averages 6.8B ⇒ 6.5% of run | **WEAK-18, unreconciled** | paper |
| 136 | 112-run search cost | 0.12% (62M) / 0.65% (350M) of one run | **missing (MISSING-5)** | — |
| 137 | Llama 3 probe: 50%-trained, 40B, 30/70 | ✅ | verified | paper |
| 138 | kill thresholds (numeric) | none anywhere | **MISSING-4 (caps E11)** | none |
| 139 | Llama 3 8B +24.0% GSM8K / +6.4% MATH; 405B negligible | ✅ | verified | paper |
| 140 | OLMo 2 +10.6; Gemma2-9B ~10%; all ≤14B | ✅ | verified | paper |
| 141 | MMLU peak gap 0.60pp; Core Avg 0.86pp | ✅ | verified | paper |
| 142 | attention ~5% of FLOPs at 120B | 5.3% ✅ | verified | paper |
| 143 | benchmarks per lane (MMLU…BrowseComp) | MGSM/Flores/LongBench/RULER/MDQA/TOEFL/QuALITY + code set traceable; MILU, IndicGenBench, SWE-bench, τ-bench, BFCL, GAIA, BrowseComp are outside the nine papers and the widgets | **WEAK (unflagged out-of-base)** | partial |
| 144 | ≥8% "funds its benchmarks" (widget 1 `WEIGHTED_MIN`) | long 4.5% and agentic 2.0% are **starved** by the course's own rule | **MISSING-8, never mentioned** | — |

---

## Part 9 — Requirement scorecard

| Req | Verdict | Specific missing element |
|---|---|---|
| **R0** written spec, "specific enough to defend" | **PASS** | Reads as a defensible spec, not notes. Deduct for the empty `Epochs on unique` column, the 100.2 sum, and no declared context length. |
| **R1** share for every capability slot | **PARTIAL** | All seven slots present with demand and supply, but the printed column sums to **100.2** while asserting 100.0 (FATAL-1). |
| **R2** Indic verified/unverified/translated/synthetic, not a headline number | **PASS** | Four tiers with demand, supply, repeat and named sources; tier reasoning is used downstream (anneal reserve, kill criterion), so it does not hide behind the lane %. Deduct for the unexamined tier-C = 5.0B premise (WEAK-13). |
| **R3** agentic + reasoning + long-context pointed at **inventory datasets** | **FAIL** | Agentic: 9 datasets ✅. **Reasoning: none. Long-context: none.** 1-for-3 on the most mechanical requirement in the assignment (FATAL-7). |
| **R4** **fixes** the floor the selector cannot cross | **PARTIAL** | 8% is fixed and the clause-by-clause evidence table is the best-argued part of §5. But the floor is **aggregate** over three lanes where the course's are per-lane, so agentic is unprotected (FATAL-13), and it never binds (MISSING-2). |
| **R5** declares the anneal reserve held back for the cooldown | **PASS** | Names *what* is withheld during the main run (Tier-A Indic, long reasoning traces, long agent trajectories — matching widget 7's three reserve categories), the 60/40 structure, the top-5% quantile, and cyclic exposure. Deduct for FATAL-4 (epochs) and the 8.0B long-trace supply violation. |
| **R6** difficulty **and** reasoning-length bands, concrete example each | **FAIL** | Bare `B0–B5` labels, no definitions, no examples; reasoning-length is one sentence naming 3 of 4 tiers with no ranges and no example. Material was in widgets 6 and 7 (FATAL-8). |
| **R7** commits to 1B and 3B proxy runs | **PASS** | §7 item 4 explicitly, plus the CLIMB search, the anneal-probe protocol and the FLOP budget. |
| **R8** cleaning aimed at the slots the mixture shows to be **starved** | **FAIL** | Not addressed at all (MISSING-6). |

| Crit | Verdict | Specific missing element |
|---|---|---|
| **E1** holds up when pushed on every number | **PARTIAL** | ~90% of the arithmetic and ~95% of the citations survive a hard push — genuinely strong. But 13 FATALs, and three of them (100.2 sum, OPUS-40% ratios, reserve-quantile epochs) are exactly what a reviewer reaches for first. |
| **E2** reasoning quality and evidence | **PASS** | The strongest dimension. Cluster A/B, absolute-vs-fraction anneal reading, verifier-vs-self-sampling, per-lane utility scoring, and §8's disclosures are all first-rate. It even corrects a source (8× not 10×). |
| **E3** tightly argued, padding earns nothing | **PARTIAL** | 15–20% cuttable (P1–P6), including an entirely empty table column. |
| **E4** defended share for every lane | **PARTIAL** | Main-run lanes defended; **four of seven anneal lanes deviate from the course preset with no reason given** (WEAK-17); two main-run deviations rest on taste when arithmetic was available. |
| **E5** Indic tiers stated | **PASS** | Fully. |
| **E6** benchmarks explain **why each number is what it is** | **FAIL** | No lane's magnitude is derived from a benchmark. Long-context 4.5% and agentic 2.0% sit below the course's own ≥8% funding line while claiming five benchmarks each; the rule is never mentioned (MISSING-8). |
| **E7** sized against **real supply from the inventory** | **PARTIAL** | Demand/supply/ratio for all 7 lanes and all 4 tiers — the right shape. But the ratios ignore the declared selector (FATAL-5), STEM's 250B is not reconstructible from widget 9 (WEAK-12), the reasoning pool is 92% V4 legacy (WEAK-14), code's admitted cut is unquantified (FATAL-12), and total-run exposure is never given. |
| **E8** says **plainly** where a share needs repeating or generating | **PASS** | The clearest dimension: "repeat"/"must generate" verdicts in the headline table, "**Arithmetic first**", "~94% of the lane is generated", "We are writing this number first, not following the field." Nothing is buried or hedged. |
| **E9** no wishful accounting on a supply-poor lane | **PARTIAL** | Disclosure is loud and specific, which is most of the defence. But the share is **6× past the loosest measured ceiling** and **17.9× the organic real supply**, the headline gap understates by 12%, and the fallback (75% synth) is also non-compliant. Loud honesty ≠ a defensible share. |
| **E10** bands with a real example at each level | **FAIL** | See R6. Stated twice in the source, so this costs twice. |
| **E11** tier reached | **EXCELLENT, partial HIGHEST** | "Testable hypothesis" is clearly met (§7's opening line is literally "every number above is a hypothesis"). "Highest" requires a concrete 1B/3B proxy **and** the metric that would confirm or refute: the experiments are concrete and the metrics are named, but **no numeric threshold or noise margin exists anywhere**, so the criteria are not gradeable (MISSING-4). "Very highest" (probe actually run, numbers brought back) — not attempted. |

### Estimated score

Requirement axis (R0–R8, equal weight): 0.85 + 0.85 + 0.85 + 0.40 + 0.60 + 0.80 + 0.10 + 0.90 + 0.00 = 5.35/9 = **0.594**
Criterion axis (E1–E11, equal weight): 0.65 + 0.85 + 0.70 + 0.75 + 0.95 + 0.35 + 0.65 + 0.90 + 0.55 + 0.10 + 0.55 = 7.00/11 = **0.636**
Mean = 0.615 → **≈ 307 / 500. Call it 300–320.**

**Reasoning.** The spec is well above average on the two dimensions that carry the most weight in the prose rubric — E2 (evidence) and E8 (plain repeat/generate statements) — and its arithmetic is far cleaner than the volume of numbers would predict; the ½·L1 = 19.48%, the anneal token table, the Indic tier grid and the agentic 0.2–0.25% alternative are all exactly right, and roughly sixty paper-attributed figures reproduce with a single misread. What caps it at ~60% is not sloppiness but **two absent requirements and one systematic accounting hole**: R6/E10 is enumerated twice in the assignment, has its raw material sitting in two widgets, and is simply not done; R8 is not addressed; and the supply ratios — the load-bearing artifact of the entire document — are computed as though the selector the spec declares in its own sixth line does not exist, which flips three "covered" verdicts and pushes reasoning to its measured epoch ceiling.

**Cheapest path from ~307 to ~400,** in descending marks-per-edit: (1) add the two band tables with examples from widgets 6 and 7 — R6 and E10 are two gradeable clauses for perhaps fifteen lines; (2) name the reasoning and long-context inventory datasets with token counts — R3 goes from FAIL to PASS in two lines; (3) state the post-OPUS ratio column, or state explicitly that rejected candidates are re-offered so unique supply is not consumed — either resolves FATAL-5; (4) add one paragraph on which slots cleaning targets next (R8); (5) fix the share column to sum to 100.0, fix the Chinchilla direction, fix the seam count to 4, and recompute the reserve epochs against the top-5% pool the spec itself specifies; (6) add numeric pass/fail thresholds with a noise margin to §7's kill criteria, which is what stands between "excellent" and "highest" on E11; (7) add the plan-wide synthetic fraction (5.5%) and the course-preset shift comparison (32.0% → 19.5%), both of which are free defensive wins already implied by the document's own numbers.
