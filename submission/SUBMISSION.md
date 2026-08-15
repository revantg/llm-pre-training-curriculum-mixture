# V5 Pretraining Mixture and Curriculum

**~120B parameters · 2.000T main run · +80B anneal · 2.080T total**

Every number is recomputed arithmetic, a constant read out of the course widgets, or a published result with its measurement scale attached. Where a number is mine and unevidenced it says so in place. Section 14 lists what is weakest.

**What this claims:** the highest specification band — a concrete 1B/3B proxy with named confirm/refute metrics (§13). Not the top band: **no proxy has been run.**

**Prerequisite status:** the data gate of §12 is **specified, not passed** — decontamination is unrun and three agentic licences need review. On the criteria's own sequencing this mixture is not yet trustworthy. That is stated here rather than 84% of the way in.

---

## 0. The plan on one screen

| lane | share | main | anneal | demand | real supply | epochs | verdict | must win |
|---|---|---|---|---|---|---|---|---|
| web | **33.85%** | 677.0B | 16.9B | 693.9B | 4691.0B | 0.15 | covered | HellaSwag, ARC-e, WinoGrande |
| code | **23.95%** | 479.0B | 18.4B | 497.4B | 1103.0B | 0.45 | covered | HumanEval, MBPP |
| Indic | **15.80%** | 316.0B | 17.5B | 333.5B | 113.9B | **2.93** | repeat + synthetic | IndicXTREME, XCOPA, TyDiQA-GoldP |
| STEM | **11.45%** | 229.0B | 7.3B | 236.3B | 146.0B | **1.62** | repeat | MMLU-STEM, ARC-c |
| reasoning | **8.50%** | 170.0B | 11.7B | 181.7B | 85.1B | **2.13** | repeat | GSM8K, MATH |
| long-context | **4.45%** | 89.0B | 2.2B | 91.2B | 40.0B | **2.28** | repeat | MDQA, RULER |
| agentic | **2.00%** | 40.0B | 6.0B | 46.0B | 0.627B | **73.4** | **generate 94.5%** | BFCL AST-match |
| | **100.00%** | 2000.0B | 80.0B | **2080.0B** | | | | |

`demand = share x 2000B + anneal slice`, so every row is auditable without turning to §8.

**One lane does not comply with its own supply.** Agentic is §6, not buried.

---

## 1. Budget

**2.000T on ~120B params is 0.85x compute-optimal.** Optimal is 2.353T from `U_N = 0.051 * U_D`, fitted by Muennighoff et al. (2305.16264). That constant is a refit of **Chinchilla's own C4 IsoFLOP runs** — not an independent check on Chinchilla, just its data with a published coefficient rather than the remembered "20 tokens per parameter" heuristic, which agrees anyway (2.4T vs 2.353T). The 0.353T given up buys the scarce-lane shares in §3.

**Anneal = 80B = 3.85% of total**, OpenCoder's published ratio. The one structural choice with precedent inherits it.

---

## 2. Lane shares

Shares are the exact time-average of the §9 stage profiles, so curriculum and mixture are one object. Six lanes deviate from the course preset; **only two are choices.**

| lane | preset | mine | delta | why |
|---|---|---|---|---|
| reasoning | 6.00 | **8.50** | +2.50 | choice |
| long-context | 6.00 | **4.45** | -1.55 | choice — capability bought by packing, not share |
| STEM | 12.00 | 11.45 | -0.55 | funds the above |
| Indic | 16.00 | 15.80 | -0.20 | funds the above |
| web | 34.00 | 33.85 | -0.15 | funds the above |
| code | 24.00 | 23.95 | -0.05 | funds the above |
| agentic | 2.00 | 2.00 | 0.00 | floor-pinned |

The four negatives are arithmetic closing, not four judgements: together they release 0.95pp / 19B.

**Reasoning at 8.50, not 6.00.** Widget 1 sets `WEIGHTED_MIN = 8`, commented *"a lane needs at least this share to move its benchmarks."* At 6.00 the lane is unfunded by the course's own rule. 8.00 is the threshold; **8.50 carries 0.5pp** so stage-profile rounding cannot drop it under.

**Long-context at 4.45, below that same threshold**, because share is the wrong instrument: packing (§9) lifts effective >=4k exposure to **17.7%** across every lane. Spending 6.00% on a 40B pool means 3.1 epochs on books to buy what packing buys from tokens already paid for.

---

## 3. Supply ledger

From the 32 datasets in widget 9, summed per lane. **Two values disagree with the course's `SUPPLY_T` constant and the inventory wins.**

| lane | `SUPPLY_T` | inventory | used | note |
|---|---|---|---|---|
| web | 4500B | **4691B** | 4691B | constant understates; harmless |
| code | 1100B | **1103B** | 1103B | agrees |
| Indic | 276B | 275.9B | **113.9B real** | 162.0B tagged `synth`, counted separately |
| STEM | 250B | **146.0B** | 146.0B | **correction** |
| reasoning | 85B | **85.1B** | 85.1B | agrees |
| long-context | 100B | 100.0B | **40.0B independent** | **correction** |
| agentic | 0.63B | **0.627B** | 0.627B | agrees |

**STEM is 146B, not 250B.** Widget 9 has no `stem` lane; its STEM sets sit inside `general`: `proof-pile-2` 55B + `D4 STEM (V4)` 49B + `peS2o` 42B. The 250B is a course constant the itemised inventory does not support. STEM's verdict changes from *covered* to **1.62 epochs** — inside the near-free band, so the share stands, but the verdict was wrong.

**Long-context has 40B independent, not 100B.** Its two sets are `Repo-packed code (32K+)` 60B and `Book-length corpora (packed)` 40B. The first is permissive tier-B packed code — a **view of the code pool**, not new tokens — so counting it in both lanes double-counts 60B. The lane is charged 40B of books plus a declared claim on code already bought: **2.28 epochs**.

### 3.1 What repeating costs

Priced by the fitted law in 2305.16264: `D' = U + U * R* * (1 - exp(-R/R*))`, **R\* = 15.39** over 182 runs, 7M-9B params, 1-500 epochs.

**No real pool here is repeated past 4 epochs**, the figure that source states five ways as downstream-insignificant: Indic 2.93, long-context 2.28, reasoning 2.13, STEM 1.62, and the agentic and trace pools capped at exactly 4.00 (§6.1, §11). Loss at 4 epochs is **6.9%**. The agentic *lane* reads 73.4 epochs in §0 because that is demand over pool; the pool is served 4 times and the remainder generated, not repeated.

The real ceiling is the **asymptote**: `U` unique tokens yield at most `U * (1 + R*) = 16.39 * U` effective tokens at any epoch count. Two caveats travel with it everywhere, including §6 — it is the **conservative of two published fits** (the better-fitting form, R^2 0.7988 vs 0.7722, implies nearer **95x**), and it bounds **value, not safety**, since reaching it needs ~80 epochs and 44 epochs measured a 6.8-point downstream collapse.

**Scale caveat:** that fit tops out at **9B** and we are at 120B. The extrapolation axis moved from pool size to model scale; §5.2 gives a case where scale reverses a related result's sign.

### 3.2 Non-natural tokens, by who made them

| provenance | tokens | of 2.080T |
|---|---|---|
| existing published synthetic — Sangraha synthetic (tier D), CC-BY-4.0 | 105.7B | 5.08% |
| existing published **distilled** — OpenThoughts2 3.0B + OpenR1-Math 1.6B at the 4-epoch trace cap | 18.4B | 0.88% |
| *subtotal: exists already, someone else made it* | *124.1B* | ***5.97%*** |
| **generated by us** — agentic 43.5B + anneal verified-synthetic 4.4B | 47.9B | **2.30%** |
| **total non-natural** | **172.0B** | **8.27%** |

The distilled row belongs because the inventory calls those sets *"distilled at scale"* and *"R1-distilled"* — model output by the same standard that puts Sangraha in row 1, and **64.8% of the 28.4B trace budget**. The split is load-bearing: **we fabricate 2.30%**; the larger 5.97% is licensed published text used at 0.65 epochs, a sourcing decision rather than a generation risk.

---

## 4. Lane to benchmark, causally

| lane | benchmark | the causal claim |
|---|---|---|
| web | HellaSwag, ARC-e, WinoGrande | 0.15 epochs on 4.7T means supply-saturated; share above ~30% buys nothing and is held as ballast against mixture shift (§8) |
| code | HumanEval, MBPP | 23.95% is OpenCoder's code-heavy regime; below ~20% pass@1 falls with share on their curve |
| Indic | IndicXTREME, **XCOPA**, **TyDiQA-GoldP** | NVIDIA separated two multilingual mixtures by **2.31 pts** on these; they respond to multilingual share where MMLU does not |
| STEM | MMLU-STEM, ARC-c | 1.62 epochs over 146B of proof-pile-2 / peS2o / D4; the only lane whose tokens are mostly formal notation |
| reasoning | GSM8K, MATH | 8.50% clears `WEIGHTED_MIN = 8`; the 28.4B trace budget (§11), not the 181.7B lane, carries chain-of-thought form |
| long-context | **MDQA**, RULER | bought by packing (17.7% effective >=4k), not by the 4.45% share; see §14 item 2 |
| agentic | **BFCL AST-match** | AST-match rather than SWE-bench because 94.5% of the lane is generated and AST-match measures call form, which generation can teach; SWE-bench secondary |

---

## 5. Indic, across all four tiers

Tiers are the assignment's — **verified / unverified / translated / synthetic** — with real supply from widget 9:

- **A verified** — Sangraha (verified) **64.0B**, `conf`, CC-BY-4.0
- **B unverified** — Sangraha (unverified) 24.0B + IndicCorpV2 20.9B = **44.9B**
- **C translated** — BPCC (parallel) 3.0B + Samanantar 2.0B = **5.0B**
- **D synthetic** — Sangraha (synthetic) **162.0B**, tagged `synth`, CC-BY-4.0

Real A+B+C = **113.9B** against a lane demand of **333.5B**.

### 5.1 One declared cap, not four hand-picked numbers

I declare a single epoch cap **N on the real tiers** and let every share fall out of it — the UniMax mechanism (2304.09151) — so the split is falsifiable by one number instead of four. A 15.80% share forces a frontier with no point that is both low-repetition and low-synthetic:

| N on real tiers | tier D | D epochs | lane synthetic |
|---|---|---|---|
| 1.00 | 219.6B | 1.36 | 65.8% |
| 1.50 | 162.7B | 1.00 | 48.8% |
| **2.00 (chosen)** | **105.7B** | **0.65** | **31.7%** |
| 2.50 | 48.8B | 0.30 | 14.6% |
| 2.93 | 0B | — | 0.0% |

| tier | tokens | share | epochs |
|---|---|---|---|
| A verified | 128.0B | **38.38%** | 2.00 |
| B unverified | 89.8B | **26.93%** | 2.00 |
| C translated | 10.0B | **3.00%** | 2.00 |
| D synthetic | 105.7B | **31.69%** | 0.65 |
| | 333.5B | 100.00% | |

**Real 68.31% / synthetic 31.69%.**

### 5.2 Why N = 2.00 and not 1.00

N=1 is the best-tested cap: NVIDIA's cap experiment found **N=1 beats N=2 beats N=4** on MMLU (28.30 / 28.00 / 26.60) shrinking sources 18.7B to 1.5B. On that alone, lower is better. I do not choose it because the frontier prices N=1 at **65.8% synthetic** — trading a measured repetition risk for a larger unmeasured generation risk. N=2.00 puts translated tier C at 2.00 epochs and holds every real tier inside the 4-epoch band.

Two caveats. The experiment's **confound**: raising the cap also flattens toward uniform, the authors offer both explanations, and they decline to transfer the result to synthetic data — so it constrains tier C, **not** tier D.

Worse for me: **UniMax measured the axis I would rather call untested.** Held-out CE at ~4.7 epochs is +0.000 at 1.2B, +0.000 at 3.7B, **+0.071 at 13B** — and the 13B model ends *worse* than the 3.7B on the over-repeated language while every English curve improves. Their §5.1: *"overfitting only emerges with scale... conspicuous at XXL size."* The effect I need to be small **grows with scale, and I am at 120B.** Strongest argument against §5, from my own evidence base; it is why H3 runs at 3B.

### 5.3 One epoch is the convention; I am at 2.00

Both disclosed multilingual builds serve their multilingual slice at **exactly 1.00 epoch** — umT5 (48.2B of 48.4B) and NVIDIA (6.00B of 6.00B). My real tiers run 2.00x that. One-epoch Indic needs a **5.48%** share, but the course floor is `indic >= 12`, so **one-epoch Indic is unreachable at any legal share.** The tension is in the assignment, not the choice.

---

## 6. Agentic: the one number that does not comply

**2.00% = 46.0B against a real pool of 0.627B**, a 73.4x gap. Flagged here because the failure the criteria name is doing this *quietly*.

**The pool in full** (9 sets, widget 9): SWE-Gym 150M, SWE-smith 120M, OpenHands rollouts 90M, ToolBench 80M, ToolACE 60M, Glaive v2 50M, Nexus 30M, xLAM/APIGen 25M, Hermes 22M. Two facts make it worse than the headline: **20.7% is already generated** (tier-D Glaive v2 and ToolBench are LLM-produced, so against genuinely-collected trajectories alone — **0.497B** — the gap is **92.6x**), and **zero tokens are `conf`** — one of two lanes with none.

### 6.1 The epoch cap, and why 4

| epochs | raw served | effective | efficiency | generated % | measured downstream evidence |
|---|---|---|---|---|---|
| 1 | 0.627B | 0.627B | 100.0% | 98.6% | safe |
| **4 (chosen)** | **2.508B** | **2.336B** | **93.1%** | **94.5%** | **safe — "differences insignificant up to around 4 epochs (25% budget)"** |
| 8 | 5.016B | 4.153B | 82.8% | 89.1% | past the line; downstream "starts dropping", magnitude unmeasured |
| 16 | 10.032B | 6.636B | 66.1% | 78.2% | unmeasured |
| 32 | 20.064B | 8.989B | 44.8% | 56.4% | approaching the 44-epoch collapse: 19-task mean **20.9 to 14.1** |

**4 epochs, because that is where the evidence stops.** The efficiency column prices **value, not safety** — how much information a token still carries, not whether repeating it damages the model. Choosing 8 would cost 5.4pp of generated share and buy no evidence: any efficiency threshold selecting it is retrofitted, since efficiency crosses 80% at ~8.9 epochs and no such threshold exists in the evidence base.

**Allocation:** 2.508B raw / 2.336B effective; **generated = 43.49B = 94.5% of the lane.**

### 6.2 Can the lane be filled from real data at all

Under the conservative fit the asymptote caps the pool at `0.627B * 16.39 = 10.28B` effective tokens ever — below the 46.0B demanded — so no epoch count fills it. **But my own footnote weakens that:** the better-fitting form implies ~95x, giving 59.6B, which *exceeds* the lane. Honest statement: under the conservative fit the lane cannot be filled; under the better-fitting one it could in principle, at hundreds of epochs, a regime nobody has tested and which the same paper's scale result argues against. I previously wrote "provably not fillable" against the conservative fit alone; **withdrawn.**

### 6.3 Why the share stays at 2.00%

Not because I can defend it on supply. **I cannot** — on my own cited ceilings the defensible band is **0.125-0.376%**, so 2.00% is 5-16x outside it. It stays because widget 1 hard-codes `{key:"agentic", floor:2}` and `normalize()` returns no legal mixture below it; I verified that in the widget source. If the floor were removable I would set 0.4% and return 33B to STEM and reasoning. A reviewer may fairly reply that the honest move was to argue the floor down rather than comply and confess, and I have no rebuttal beyond the constraint being stated as hard. **Lowest-confidence number in the plan.**

---

## 7. The protected floor

**Indic >= 6.0% and agentic >= 2.0%, per lane, 8.0% together.** Enforced in every length bucket, every curriculum cycle and inside the anneal — not on the run average, since a lane can hit its average while vanishing from the last 80B.

**Why 6.0%.** The floor must be one the **selector** cannot cross, and the selector has its own constant: widget 3's per-iteration OPUS selector hard-codes `LANE_FLOOR = 0.08`, commented *"8% of trained tokens reserved for Indic + agentic"*, and force-promotes scarce batches until that ratio is met. A floor of 5.5 + 2.0 = 7.5% sits **below** it, so the selector would override my declaration every iteration and the floor would be decorative. Indic at 6.0% makes the combined floor **exactly 8.0%**.

Three Indic numbers do different work: **5.48%** is what one epoch costs (113.9B / 2080B), **6.0%** is the always-on floor meeting `LANE_FLOOR`, **15.80%** is the served share. The course's separate `indic >= 12` binds above all three.

The real-token clause is **scoped to supply**, since unscoped it is meaningless: **Indic** 6.0% = 124.8B against 113.9B real = **1.10 epochs, binds**; **agentic** 2.0% = 41.6B against 0.627B = **66.4 epochs, cannot bind**, so there the floor protects presence, not freshness.

**Reasoning is excluded.** Widget 3 marks it `scarce:false` and it scores 0.818 on the English-supply proxy — third of seven, above web at 0.776. A floor for a non-scarce lane is a share.

---

## 8. The anneal and the reserve

**80B = 50B ballast (62.5%) + 30B reserve (37.5%).** The reserve is held back from the main run and spent only in the decay leg:

| component | tokens | selectivity |
|---|---|---|
| Tier-A Indic | 9.6B | top 15% of verified |
| Algorithmic code | 6.4B | top 0.6% of 1103B |
| Verified synthetic reasoning | 4.4B | generated, verified |
| Agentic env-verified | 3.6B | generated, execution-checked |
| Long reasoning traces | 3.0B | 65% of a 4.6B pool |
| HQ STEM | 1.6B | top 1.6% of 146B |
| Long agent trajectories | 1.4B | 3.89 epochs |
| | **30.0B** | |

Ballast is spent at main-run shares so the mixture does not lurch. Resulting anneal mixture, summing to **100.000**:

| web | code | Indic | STEM | reasoning | long-ctx | agentic |
|---|---|---|---|---|---|---|
| 21.156 | 22.969 | 21.875 | 9.156 | 14.563 | 2.781 | 7.500 |

**Mixture shift = 17.64%** (half the L1 distance from main-run shares) against the course preset pair's own **32.0%** — **44.9% gentler** than the comparison case.

**Two honest limits.** The top-0.6% and top-1.6% quantiles are **extrapolation**: the most aggressive published filter keeps 45.6%, another filters to the cleanest 25%, and nobody has measured a 0.6% slice. And the precedent is thin — Spark Joy's sweep is a **cruising-LR mixture swap, not a decay leg** (they never changed the learning rate), so it supports the mixture and not the schedule. Llama 3 405B annealed 40M tokens (0.00025%), five orders below mine; I rely on OpenCoder's ratio alone.

---

## 9. Curriculum: stages, seams, packing

| stage | tokens | web | code | Indic | STEM | reason | long | agentic |
|---|---|---|---|---|---|---|---|---|
| Seed | 200B | 45 | 18 | 14 | 12 | 6 | 3 | 2 |
| General | 700B | 38 | 24 | 15 | 12 | 6.5 | 2.5 | 2 |
| Reasoning | 600B | 30 | 25 | 16 | 12 | 11 | 4 | 2 |
| Long-context | 500B | 28.2 | 25 | 17.4 | 9.8 | 9.3 | 8.3 | 2 |
| Anneal | 80B | 21.156 | 22.969 | 21.875 | 9.156 | 14.563 | 2.781 | 7.500 |

Every row sums to 100 (the Anneal row to 100.000 — quoted to 3dp because 1dp does not close). The four main-run rows time-average to §0's shares **exactly** at weights 0.10 / 0.35 / 0.30 / 0.25: three stages are round values and the Long-context row is *solved* so the residual is zero.

**Seams.** Five stages, four boundaries, each a **20B linear cross-fade**: 4 x 20B = 80B = **4.0% of the main run**. Widget 8's spike model predicts **1.34x** frozen / **1.23x** unfrozen peak gradient norm at 20B against its red line `RED_T = 3.0`. Narrower crosses it; wider buys margin already held. This is the thinnest-supported number here — priced only by the course's own model, with no external measurement.

**Packing.** Binary dataset decomposition rather than concat-and-chunk, worth **+2.9 regular / +3.4 long-context** in DatasetDecomp (at 1B, matching our probe scale).

Bucket policy comes from a micro-replication I ran on a 342-document / 78,581-token corpus: concat-and-chunk gave mean in-document context **421.1** tokens against **3452.5** under decomposition with a >=256 floor — an **8.20x** separation against the published 1.45x, because that corpus is short-document-heavy. The same run showed a global >=256 floor **discards 44.9% of tokens**, so the floor applies **only to naturally-long lanes** (books, repo-packed code) and all buckets are kept for short-document lanes. A corpus statistic, not a model result.

---

## 10. Difficulty bands, with an example at each level

Six bands on widget 7's `DIFF[]` scale verbatim. Each specimen is a concrete piece of text at that level, composed for this document rather than quoted from a dataset — enough to see where each boundary sits.

| band | level | specimen |
|---|---|---|
| **B0** | Nursery | *"The cat sat on the mat. The mat was warm. The cat was happy."* |
| **B1** | Grade-school | *"Leaves look green because of chlorophyll. In autumn the tree stops making chlorophyll, so the yellow and orange colours that were always there start to show."* |
| **B2** | High-school | *"Balance: C3H8 + 5 O2 -> 3 CO2 + 4 H2O. If 2.2 g of propane (M = 44 g/mol) burns completely, how many grams of water form?"* |
| **B3** | Undergraduate | *"Show that if f is continuous on [a,b] and differentiable on (a,b) with f(a) = f(b), then there exists c in (a,b) with f'(c) = 0. State where continuity, as opposed to differentiability, is used."* |
| **B4** | Graduate | *"Let (X, S, mu) be a sigma-finite measure space. Prove that L^p(mu) is complete for 1 <= p < infinity, and exhibit a sequence in L^1 converging in measure but not in L^1 norm."* |
| **B5** | Research / PhD | *"Let M be a smooth compact manifold and f: M -> M an Anosov diffeomorphism. We show the SRB measure varies differentiably under C^3 perturbation, and give a counterexample when the hyperbolicity constant degenerates on a set of positive measure."* |

**Schedule.** B0-B1 concentrate in Seed, B2-B3 dominate General and Reasoning, B4-B5 rise through Long-context and are heaviest in the anneal where the top-quantile reserve lives.

**No paper supports this ladder**, and PrefCurriculum argues against the nearest analogue: a perplexity gap is not a difficulty axis. It is a scheduling device I am declaring, and H5 is the test that retires it.

---

## 11. Reasoning-length bands, with an example at each level

Four bands from widget 6, **the same problem at every band** so length is the only variable: *count the integers from 1 to 1000 divisible by 3 or by 5.* The answer is **467** at every band.

| band | steps | tokens | solve rate | budget |
|---|---|---|---|---|
| LOW | 2 | 37 | 61.5% | 15% = 4.26B |
| MEDIUM | 4 | 74 | 76.8% | 30% = 8.52B |
| HIGH | 6 | 161 | 90.9% | 35% = 9.94B |
| ULTRA | **14** | 346 | 95.3% | 20% = 5.68B |

Token counts and solve rates are re-derived from widget 6's curve, `acc(L) = 0.955 - 0.615 * exp(-L/tau)`, `tau = 0.18 * 346 = 62.28`.

**Budget is 28.4B of trace-shaped tokens, not the 181.7B lane**, and it is fully covered by real data: the lane's four non-AON sets — OpenThoughts2 3.0B, OpenMathReasoning 2.0B, OpenR1-Math 1.6B, NuminaMath 0.5B — total **7.1B**, and 28.4B / 7.1B = **exactly 4.00 epochs**, the same cap as §6.1. **No trace tokens are generated.** The other 78.0B of real reasoning supply is AON, a confirmed V4 corpus of academic prose (§14 item 1).

**LOW, verbatim, both steps:**
> 1. Inclusion-exclusion: floor(1000/3) + floor(1000/5) - floor(1000/15).
> 2. = 333 + 200 - 66.

**MEDIUM, verbatim, all four:**
> 1. Count multiples of 3 up to 1000: floor(1000/3) = 333.
> 2. Count multiples of 5 up to 1000: floor(1000/5) = 200.
> 3. Divisible by both 3 and 5 means divisible by 15: floor(1000/15) = 66, counted twice.
> 4. Inclusion-exclusion: 333 + 200 - 66 = 467.

**HIGH — distinguished by step 6, an independent check:**
> 5. Inclusion-exclusion: |A or B| = 333 + 200 - 66 = 467.
> 6. Check by complement: divisible by neither is about 1000 times (2/3) times (4/5) = 533, and 1000 - 533 = 467. Consistent.

**ULTRA — 14 steps, distinguished by a second structurally different verification (9-12) plus endpoint re-examination (13):**
> 9. Verify with blocks of 15: within each block, the values hit by 3 or 5 are {3,5,6,9,10,12,15}, that is 7 of every 15.
> 10. 1000 = 66 times 15 + 10, so full blocks contribute 66 times 7 = 462.
> 11. The remainder 991 to 1000 covers residues 1 to 10, and 993, 995, 996, 999, 1000 are divisible by 3 or 5, that is 5 more.
> 12. 462 + 5 = 467, which matches the inclusion-exclusion count.
> 13. Reconsider the endpoints: 1000 is included and is divisible by 5, already counted, and 1 is divisible by neither, correctly excluded.

**ULTRA capped at 20%** because it buys **+4.40pp** over HIGH for **2.149x** the tokens; widget 6's `isWasted` test flags a step wasted below 0.05 accuracy gain and ULTRA sits just above it — worth buying, not worth scaling. The 15/30/35/20 split is mine and unevidenced; only the ULTRA cap is course-derived.

---

## 12. The data gate

A **prerequisite**, not a nicety: a mixture is only as trustworthy as the cleaned and documented tokens behind it. Widget 9 gives a `lic` field and a confidence `tag` for all 32 datasets, so the gate is stated in the inventory's own terms.

### 12.1 Confirmed-token coverage

`conf` means measured in a real prior run; `approx` means estimated.

| lane | datasets | confirmed | approx | synth | verdict |
|---|---|---|---|---|---|
| reasoning | 5 | **91.7%** | 7.1B | — | passes |
| STEM | 3 | 33.6% | 97.0B | — | conditional |
| Indic | 6 | 31.9% | 25.9B | 162.0B | conditional |
| code | 3 | 18.0% | 904.0B | — | conditional |
| web | 4 | 16.9% | 3900.0B | — | conditional |
| **long-context** | 2 | **0.0%** | 40.0B independent (+60B code view, charged to code) | — | **fails** |
| **agentic** | 9 | **0.0%** | 0.627B | — | **fails** |

**Only 18.8% of inventory tokens are confirmed** (1205B of 6402B), and **the two lanes with zero are the two this plan leans on hardest for novel capability.** Every token count in §3 and §5 for those lanes is an estimate.

### 12.2 The gate, as thresholds

No lane enters the run until all four hold. Each is a threshold, not a checkbox:

| gate | threshold | current | status |
|---|---|---|---|
| licence | 100% of served tokens under a recorded, compatible licence | 32/32 recorded; **3 agentic entries** need review — SWE-Gym and SWE-smith are `task licenses` (per-task, not blanket), OpenHands rollouts `mixed` | **blocked** |
| confirmation | >= 50% of a lane's served tokens `conf`, else its figures carry an `approx` label at every point of use | reasoning 91.7%; **5 lanes below 50%**; long-context and agentic **0.0%** | labelled, not met |
| decontamination | 13-gram overlap with any §4 benchmark **< 0.1%** of the lane, anneal reserve first | **not run** | **blocked** |
| Indic provenance | per-tier attestation for 100% of the A/B/C tokens the split depends on | Sangraha's partition covers 88.0B of 113.9B (**77.3%**) | partial |

Decontamination is the one I would close first: the reserve is 30B of top-quantile selected text, quality selection actively concentrates benchmark-like material, and Spark Joy notes the anneal is where contamination has maximum leverage on final scores.

**Two of four are blocked outright.** On the criteria's own terms this mixture is not yet reviewable, and saying so beats implying a clean bill.

### 12.3 The cleaning programme, aimed at the starved slots

The course defines a slot as **starved** when its share is below `WEIGHTED_MIN = 8` (widget 1). On this mixture that is exactly two lanes, and they set the cumulative target:

| starved slot | share | pool now | pool needed | **cleaning target** |
|---|---|---|---|---|
| long-context | 4.45% | 40.0B independent | 91.2B for 1.00 epoch | **+51.2B** multi-document real text |
| agentic | 2.00% | 0.627B | 11.5B for the 4-epoch cap with zero generation | **+10.9B** collected trajectories |
| | | | | **62.1B total** |

**62.1B retires this plan's two worst weaknesses at once**: it takes long-context off repetition and eliminates all 43.5B of agentic generation. Priority is long-context — 51.2B of multi-document text is a collection-and-packing problem against sources that exist, whereas 10.9B of real trajectories is a **17.4x** expansion of every such corpus known to me. Nothing else is worth cleaning first: the five funded lanes sit at or under 2.93 epochs on real supply, so clean tokens there would displace tokens already paid for rather than replace generated ones.

---

## 13. Hypotheses and the proxy protocol

Every share above is a hypothesis; each row names what would refute it and what I would then do.

**Cost basis.** Full run = `6 * 120e9 * 2.080e12` = **1.498e24 FLOPs**. A 1B arm on 10B tokens is `6e19` = **0.0040%**; a 3B arm on 30B tokens is `5.4e20` = **0.0361%**. The whole programme — **14 arms at 1B plus 5 at 3B, three seeds each** — is **1.06e22 FLOPs = 0.71% of the run.** Verification is not the expensive part.

**Three seeds, not one.** The resolution floor here is +/-0.5pp at 1.5B and 0.60/0.86pp at 7B, so any threshold below ~1.0pt is unreadable at n=1. Every arm runs three seeds and every threshold is against the seed mean.

| id | hypothesis | scale | metric | confirm | refute | on refute |
|---|---|---|---|---|---|---|
| **H0** | the whole mixture beats the course preset | 1B, 2 arms | mean of 6 LM-Eval tasks | >= +0.8pt | <= -0.3pt | adopt the preset; this plan is wrong as a whole |
| **H1** | decomposition packing beats concat-and-chunk | 1B, 2 arms | MDQA | >= +2.0 | <= +0.4 | revert to concat-and-chunk, reclaim the bucket machinery |
| **H2** | 94.5% generated agentic still teaches call form | 1B, 3 arms | BFCL AST-match | >= +3.0 vs no-agentic | <= +1.0 | cut the lane to the 0.4% of §6.3 and return 33B |
| **H3** | Indic real tiers survive N = 2.00 | **3B**, 3 arms | held-out CE on Indic + XCOPA | CE gap <= 0.02 | CE gap >= 0.05 | drop to N = 1.50, synthetic to 48.8% |
| **H4** | an 80B anneal beats a 40B anneal | 3B, 2 arms | MMLU + GSM8K mean | >= +1.0pt | <= +0.2pt | halve the anneal, return 40B to the Reasoning stage |
| **H5** | the B0-B5 ladder beats difficulty-shuffled | 1B, 2 arms | GSM8K + MATH mean | >= +1.0pt | <= +0.2pt | delete §10 and shuffle |
| **H6** | 20B seams keep peak grad-norm under `RED_T` | 1B, 3 arms | peak grad-norm at boundary | < 2.0x | > 3.0x | widen to 40B, costing 4% more of the run |
| **H7** | the 15/30/35/20 length split beats uniform | 1B, 2 arms | GSM8K + solve-rate-vs-tokens | >= +0.8pt | <= +0.2pt | flatten to uniform 25% |

**H3 sits at 3B** because §5.2's result makes 1B useless for it: UniMax measured the repetition effect **absent at 1.2B** and conspicuous only at 13B, so a 1B null would be unpublishable evidence in my own favour. Even 3B may be under-powered — the effect appears between 3.7B and 13B.

**MMLU appears only at 3B or above.** NVIDIA reports it solely at 8B, "when the experimental setting allows for a non-random score", so H0/H2/H5/H7 use the six-task LM-Eval mean and BFCL at 1B and MMLU enters only at H4.

**The commitment.** No number here is trusted at full scale until its hypothesis clears at both 1B and 3B: §0's shares are provisional until H0, §5's cap until H3 at 3B, §8's anneal until H4 at 3B. On refute, the last column executes **before** the run starts. Where a result lands in neither band the value stands *provisionally* and the arm re-runs one scale up — it does not graduate to trusted. At **0.71% of the run** there is no budget argument for skipping the test.

**Nothing here has been run.** No model has been trained. That caps this submission below the top band by design; the alternative is claiming a result I do not have.

---

## 14. Where this is weakest

Three items carry numbers found nowhere else in this document.

1. **Reasoning is 8.50% but only 7.1B of the lane is trace-shaped.** 78B of the 85.1B real supply is AON — a confirmed V4 corpus, but academic prose, not chain-of-thought. The lane is large and the thing it is *named for* is small, arguably a worse instance of the criteria's concern than agentic, which is small and loudly flagged while this is large and easy to miss. Two-Phase got its gain from about **1.3%** of a phase being reasoning-shaped and I serve 28.4B/2080B = **1.37%** — so the plan may be adequate by accident, but the share is not what makes it so.
2. **Long-context has no multi-document data.** The inventory has packed books and packed repos; MDQA is multi-document. Packing raises effective context length; it does not manufacture cross-document retrieval structure. Training length is **8192** and nothing here licenses a 32k or 128k claim.
3. **Almost nothing has error bars.** CLIMB's own checklist says no; Spark Joy, PrefCurriculum and DatasetDecomp are single- or two-seed. DatasetDecomp publishes **+/-1.6 MDQA** over two seeds, which is why H1's confirm bound is +2.0 rather than the +1.85 I would otherwise have used.

The rest are stated where they arise and are listed here only so the set is complete: agentic 2.00% held by a hard-coded floor (§6.3, the lowest-confidence number in the plan); the Indic share against UniMax's scale result (§5.2, the strongest argument against §5); unmeasured 0.6% / 1.6% reserve quantiles and thin anneal precedent (§8); seam width priced only by the course's own model (§9); the unsupported B0-B5 ladder (§10); the 15/30/35/20 split (§11); the repetition law fitted at 9B and applied at 120B (§3.1); the gate specified and not passed (§12); and no proxy run (§13).

---

## Appendix: what to re-check first

Four numbers carry the most weight and are cheap to check by hand:

- **STEM 146.0B** — `proof-pile-2` 55 + `D4 STEM (V4)` 49 + `peS2o` 42 in widget 9. If wrong, §3 is wrong.
- **Real Indic 113.9B** — Sangraha verified 64 + unverified 24 + IndicCorpV2 20.9 + BPCC 3 + Samanantar 2, excluding the 162B tagged `synth`. If wrong, §5 is wrong.
- **Shares time-average to §0** at weights 0.10 / 0.35 / 0.30 / 0.25. If this fails, §2 and §9 disagree.
- **Anneal printed digits sum to 100.000.** If this fails, §8 is wrong.

Or run `python3 verify.py` — zero dependencies, **57 checks, 0 failing**. It **parses this document** and compares what it publishes against the inventory, so editing a number here breaks the suite. **33 DOCUMENT-vs-WORLD** checks test the document against the world; **24 STRUCTURAL** checks test the published numbers against each other and cannot tell you a share is a bad choice. Neither can confirm this mixture trains well — only §13's proxies could, and none has been run.
