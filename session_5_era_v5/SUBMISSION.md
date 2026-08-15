# V5 Pretraining Mixture and Curriculum

**~120B parameters · 2.000T main run · +80B anneal · 2.080T total**

Every number below is either recomputed arithmetic, a constant read out of the course widgets, or a published result with its measurement scale attached. Where a number is mine and unevidenced, it says so at the point of use. Section 14 lists what I think is weakest, before a reviewer has to find it.

**What this claims:** the highest specification band — a concrete proxy at 1B/3B with named confirm/refute metrics (section 13). It does **not** claim the top band: no proxy has been run. Nothing here is backed by a training run of mine.

---

## 0. The plan on one screen

| lane | share | demand | real supply | epochs | verdict | must win |
|---|---|---|---|---|---|---|
| web | **33.85%** | 693.9B | 4691.0B | 0.15 | covered | HellaSwag, ARC-e, WinoGrande |
| code | **23.95%** | 497.4B | 1103.0B | 0.45 | covered | HumanEval, MBPP |
| Indic | **15.80%** | 333.5B | 113.9B | **2.93** | repeat + synthetic | IndicXTREME, XCOPA, TyDiQA-GoldP |
| STEM | **11.45%** | 236.3B | 146.0B | **1.62** | repeat | MMLU-STEM, ARC-c |
| reasoning | **8.50%** | 181.7B | 85.1B | **2.13** | repeat | GSM8K, MATH |
| long-context | **4.45%** | 91.2B | 40.0B | **2.28** | repeat | MDQA, RULER |
| agentic | **2.00%** | 46.0B | 0.627B | **73.4** | **generate 94.5%** | BFCL AST-match |
| | **100.00%** | **2080.0B** | | | | |

Shares are of the main run; demand adds each lane's slice of the 80B anneal. Total closes to 2080.0B exactly.

**One lane does not comply with its own supply.** Agentic is discussed in section 6 rather than buried.

---

## 1. Budget

**2.000T on ~120B params is 0.85x compute-optimal.** Optimal is 2.353T, from the relation `U_N = 0.051 * U_D` fitted by Muennighoff et al. (2305.16264, *Scaling Data-Constrained Language Models*).

That constant is a refit of **Chinchilla's own C4 IsoFLOP runs**, so it is not an independent check on Chinchilla — it is Chinchilla's data with a published coefficient rather than the remembered "20 tokens per parameter" heuristic, which agrees closely anyway (2.4T vs 2.353T). Deliberately under-trained per-parameter: the 0.353T given up buys the scarce-lane shares in section 3.

**Anneal = 80B = 3.85% of total**, which is OpenCoder's published ratio. The one structural choice with real precedent inherits it rather than inventing a number.

---

## 2. Lane shares and how they were set

Shares are the exact time-average of the five stage profiles in section 9, so the curriculum and the mixture are the same object viewed two ways.

Six lanes deviate from the course preset. **Only two are choices.**

| lane | preset | mine | delta | why |
|---|---|---|---|---|
| reasoning | 6.00 | **8.50** | +2.50 | choice — see below |
| long-context | 6.00 | **4.45** | -1.55 | choice — capability bought by packing, not share |
| STEM | 12.00 | 11.45 | -0.55 | funds the above |
| Indic | 16.00 | 15.80 | -0.20 | funds the above |
| web | 34.00 | 33.85 | -0.15 | funds the above |
| code | 24.00 | 23.95 | -0.05 | funds the above |
| agentic | 2.00 | 2.00 | 0.00 | floor-pinned |

The four small negatives are arithmetic closing, not four separate judgements: they release 0.95pp / 19B to fund reasoning.

**Why reasoning is 8.50 and not 6.00.** Widget 1 sets `WEIGHTED_MIN = 8` with the comment *"a lane needs at least this share to move its benchmarks."* At 6.00 the lane is below the threshold the course itself defines, so it is unfunded by the course's own rule. 8.00 is the threshold; **8.50 carries 0.5pp of margin** so rounding in the stage profiles cannot drop it back under.

**Why long-context is 4.45 and below that same threshold.** Because share is the wrong instrument here. Long-context ability is bought by the packing policy in section 9, which lifts effective >=4k exposure to **17.7%** across every lane. Spending 6.00% of the budget on a 40B pool would mean 3.1 epochs on books to buy what packing buys from tokens already paid for.

---

## 3. Supply ledger

Built from the 32 datasets in widget 9, summed per lane. **Two values disagree with the course's `SUPPLY_T` constant, and the inventory wins.**

| lane | `SUPPLY_T` | inventory | used | note |
|---|---|---|---|---|
| web | 4500B | **4691B** | 4691B | constant understates; harmless |
| code | 1100B | **1103B** | 1103B | agrees |
| Indic | 276B | **275.9B** | **113.9B real** | 162.0B of it is tagged `synth` and is counted separately |
| STEM | 250B | **146.0B** | 146.0B | **correction** — see below |
| reasoning | 85B | **85.1B** | 85.1B | agrees |
| long-context | 100B | 100.0B | **40.0B independent** | **correction** — see below |
| agentic | 0.63B | **0.627B** | 0.627B | agrees |

**STEM is 146B, not 250B.** Widget 9 has no `stem` lane; its STEM datasets sit inside `general`: `proof-pile-2` 55B + `D4 STEM (V4)` 49B + `peS2o` 42B = **146.0B**. The 250B is a course constant the itemised inventory does not support. Consequence: STEM's verdict changes from *covered* to **1.62 epochs**. The share stands — 1.62 is inside the near-free band of section 3.1 — but the verdict was wrong and is now stated correctly.

**Long-context has 40B of independent supply, not 100B.** The lane's two datasets are `Repo-packed code (32K+)` 60B and `Book-length corpora (packed)` 40B. The first is *permissive tier-B packed code* — a **view of the code pool**, not new tokens. Counting it in both lanes double-counts 60B. Long-context is therefore charged 40B of independent books plus a declared claim on code tokens already bought, giving **2.28 epochs** on the books.

### 3.1 What "repeat" costs

Repetition is priced by the fitted law in 2305.16264: `D' = U + U * R* * (1 - exp(-R/R*))`, with **R\* = 15.39** over 182 runs, 7M-9B params, 1-500 epochs.

**No real pool in this plan is repeated past 4 epochs**, the figure that source states five ways as downstream-insignificant: Indic 2.93, long-context 2.28, reasoning 2.13, STEM 1.62, and the agentic and reasoning-trace pools capped at exactly 4.00 (sections 6.1 and 11). Effective-token loss at 4 epochs is **6.9%**.

The agentic *lane* shows 73.4 epochs in section 0 because that is demand over pool; the pool itself is served 4 times and the remainder is generated, not repeated. The binding constraint is not the near-term loss but the **asymptote**: a pool of `U` unique tokens yields at most `U * (1 + R*) = 16.39 * U` effective tokens however many epochs are spent. Two caveats travel with that ceiling wherever it is used, including section 6: it is the **conservative of two published fits** — the better-fitting form (R^2 0.7988 vs 0.7722) implies nearer **95x** — and it bounds **value, not safety**, since reaching it needs ~80 epochs and 44 epochs measured a 6.8-point downstream collapse.

**Scale caveat, stated because it matters:** that fit tops out at **9B parameters** and we are at 120B. The extrapolation axis moved from pool size to model scale; it did not vanish. Section 5 gives a case where scale reverses the sign of a related result.

### 3.2 Non-natural tokens, split by who made them

The one blended "synthetic mass" number is misleading, because two very different things were being added together.

| provenance | tokens | of 2.080T |
|---|---|---|
| existing published synthetic — Sangraha synthetic (Indic tier D), CC-BY-4.0 | 105.7B | 5.08% |
| existing published **distilled** — OpenThoughts2 3.0B + OpenR1-Math 1.6B, served at the 4-epoch trace cap | 18.4B | 0.88% |
| *subtotal: already exists, someone else made it* | *124.1B* | ***5.97%*** |
| **generated by us** — agentic 43.5B + anneal verified-synthetic 4.4B | 47.9B | **2.30%** |
| **total non-natural** | **172.0B** | **8.27%** |

The distilled row belongs because the inventory calls those two datasets *"distilled at scale"* and *"R1-distilled"* — model output by the same standard that puts Sangraha synthetic in row 1. They are **64.8% of the 28.4B trace budget**.

The distinction is load-bearing: **we fabricate 2.30% of the run**, and a further 5.97% is non-natural text somebody else made and published. The larger slice is a published corpus with a licence, used at 0.65 epochs, which is a sourcing decision rather than a generation risk.

---

## 4. Lane to benchmark, causally

Each row states what the share is *for*, not which benchmarks the lane is vaguely near.

| lane | benchmark | the causal claim |
|---|---|---|
| web | HellaSwag, ARC-e, WinoGrande | 0.15 epochs on 4.7T means these are supply-saturated; share above ~30% buys nothing and is held only as ballast against mixture shift (section 8) |
| code | HumanEval, MBPP | 23.95% is OpenCoder's code-heavy regime; below ~20% pass@1 falls with share on their curve |
| Indic | IndicXTREME, **XCOPA**, **TyDiQA-GoldP** | NVIDIA separated two multilingual mixtures by **2.31 pts** on these; they respond to multilingual share where MMLU does not |
| STEM | MMLU-STEM, ARC-c | 1.62 epochs over 146B of proof-pile-2 / peS2o / D4; this is the only lane whose tokens are mostly formal notation |
| reasoning | GSM8K, MATH | 8.50% clears `WEIGHTED_MIN = 8`; the 28.4B trace budget of section 11, not the 181.7B lane, is what carries chain-of-thought form |
| long-context | **MDQA**, RULER | bought by packing (17.7% effective >=4k), not by the 4.45% share; see the honest gap in section 14 |
| agentic | **BFCL AST-match** | primary metric is AST-match rather than SWE-bench because 94.5% of the lane is generated and AST-match measures call form, which generation can teach; SWE-bench is secondary |

---

## 5. Indic, across all four tiers

The four tiers are the assignment's: **verified / unverified / translated / synthetic**. Real supply per tier, from widget 9:

- **A verified** — Sangraha (verified), 64.0B, `conf`, CC-BY-4.0
- **B unverified** — Sangraha (unverified) 24.0B + IndicCorpV2 20.9B = **44.9B**
- **C translated** — BPCC (parallel) 3.0B + Samanantar 2.0B = **5.0B**
- **D synthetic** — Sangraha (synthetic), **162.0B**, tagged `synth`, CC-BY-4.0

Real A+B+C = **113.9B** against a lane demand of **333.5B**.

### 5.1 The split is one declared cap, not four hand-picked numbers

I declare a single epoch cap **N on the real tiers** and let every tier share fall out of it — the UniMax mechanism (2304.09151). That makes the split falsifiable by one number instead of four.

A 15.80% share forces a frontier, and there is no point on it that is both low-repetition and low-synthetic:

| N on real tiers | tier D | D epochs | lane synthetic |
|---|---|---|---|
| 1.00 | 219.6B | 1.36 | 65.8% |
| 1.50 | 162.7B | 1.00 | 48.8% |
| **2.00 (chosen)** | **105.7B** | **0.65** | **31.7%** |
| 2.50 | 48.8B | 0.30 | 14.6% |
| 2.93 | 0B | — | 0.0% |

**Chosen N = 2.00:**

| tier | tokens | share | epochs |
|---|---|---|---|
| A verified | 128.0B | **38.38%** | 2.00 |
| B unverified | 89.8B | **26.93%** | 2.00 |
| C translated | 10.0B | **3.00%** | 2.00 |
| D synthetic | 105.7B | **31.69%** | 0.65 |
| | 333.5B | 100.00% | |

**Real 68.31% / synthetic 31.69%.**

### 5.2 Why N = 2.00 and not 1.00

N=1 is the best-tested cap. NVIDIA's own cap experiment found **N=1 beats N=2 beats N=4** on MMLU (28.30 / 28.00 / 26.60) when shrinking sources from 18.7B to 1.5B. On that evidence alone, lower is better.

I do not choose N=1 because the frontier shows it costs **65.8% synthetic** — trading a measured repetition risk for a much larger unmeasured generation risk. N=2.00 keeps translated tier C at 2.00 epochs, down from an earlier 2.53, and holds every real tier inside the 4-epoch near-free band.

**Two caveats I will not hide.**

First, the confound in that experiment: raising the cap also flattens the mixture toward uniform, so the authors offer both explanations and I cannot separate them. They also explicitly decline to transfer the result to synthetic data, so it constrains tier C but **not** tier D.

Second, and worse for me: **UniMax measured the axis I would rather call untested.** Their held-out CE at ~4.7 epochs is +0.000 at 1.2B, +0.000 at 3.7B, and **+0.071 at 13B** — and the 13B model ends *worse* than the 3.7B on the over-repeated language while every English curve improves. Their section 5.1: *"overfitting only emerges with scale... conspicuous at XXL size."* The effect I am relying on being small **grows with scale, and I am at 120B.** This is the single strongest argument against my Indic share, it is in my own evidence base, and it is why H3 in section 13 is specified at 3B rather than 1B.

### 5.3 One epoch is the published convention, and I am at 2.00

Both disclosed multilingual builds serve their multilingual slice at **exactly 1.00 epoch** — umT5 (48.2B of 48.4B) and NVIDIA (6.00B of 6.00B) — because the cap binds there. My real tiers run at 2.00x that convention.

One-epoch Indic would need a **5.48%** share. The course's own floor is `indic >= 12`. **So one-epoch Indic is unreachable at any legal share**; the tension is in the assignment, not in my choice. I note it rather than claim my number matches practice.

---

## 6. Agentic: the one number that does not comply

**2.00% = 46.0B demanded against a real pool of 0.627B.** A 73.4x gap. I am flagging this myself because the wishful-accounting failure the criteria describe is doing this *quietly*.

**The pool, in full** (9 datasets, widget 9): SWE-Gym 150M, SWE-smith 120M, OpenHands rollouts 90M, ToolBench 80M, ToolACE 60M, Glaive v2 50M, Nexus 30M, xLAM/APIGen 25M, Hermes 22M.

Two things about it that make the gap worse than the headline:

- **20.7% of the pool is already generated.** Tier-D entries (Glaive v2, ToolBench) are LLM-produced. Against genuinely-collected trajectories only (0.497B), the gap is **92.6x**.
- **Zero tokens are `conf`.** Every agentic dataset is `approx`. This is one of two lanes with no confirmed tokens at all (section 12).

### 6.1 The epoch cap on the pool, and why 4

The real pool is served at a **declared cap of 4 epochs**, which sets the generated share. The frontier, with effective tokens from the section-3.1 law and the *measured* downstream evidence in the right column:

| epochs | raw served | effective | efficiency | generated % | measured downstream evidence |
|---|---|---|---|---|---|
| 1 | 0.627B | 0.627B | 100.0% | 98.6% | safe |
| **4 (chosen)** | **2.508B** | **2.336B** | **93.1%** | **94.5%** | **safe — "differences insignificant up to around 4 epochs (25% budget)"** |
| 8 | 5.016B | 4.153B | 82.8% | 89.1% | past the line; downstream "starts dropping", magnitude unmeasured |
| 16 | 10.032B | 6.636B | 66.1% | 78.2% | unmeasured |
| 32 | 20.064B | 8.989B | 44.8% | 56.4% | approaching the 44-epoch collapse: 19-task mean **20.9 to 14.1** |

**4 epochs, because that is where the evidence stops.** The efficiency column prices **value, not safety** — how much information a token still carries, not whether repeating it damages the model. The source is explicit: the 16.39x cap "is an upper bound on value, not on safety; reaching it needs ~80 epochs, and 44 epochs measured a 6.8-point downstream collapse." 4 epochs is the figure that paper states five separate ways as downstream-insignificant, and the only point here I can defend with a measurement rather than an interpolation.

Choosing 8 instead would cost 5.4pp of generated share and buy no evidence: any efficiency threshold that selects it is retrofitted, since efficiency crosses 80% at ~8.9 epochs and no such threshold appears in the evidence base.

**Allocation:** real pool at 4 epochs = 2.508B raw / 2.336B effective; **generated = 43.49B = 94.5% of the lane.**

### 6.2 Whether the lane can be filled from real data at all

Under the conservative fit, the asymptote caps that pool at `0.627B * 16.39 = 10.28B` effective tokens **ever** — less than the 46.0B demanded — so no epoch count fills it.

**But my own footnote weakens this.** Muennighoff reports a second, **better-fitting** parameterisation (R^2 0.7988 vs 0.7722) whose asymptote is nearer **95x**, giving 59.6B — which *exceeds* the lane. So the honest statement is:

> Under the conservative fit the lane provably cannot be filled from real data. Under the better-fitting form it could in principle, but only at hundreds of epochs, a regime nobody has tested and which the same paper's own scale result argues against.

I previously wrote "provably not fillable" against the conservative fit alone. That was overstated and is withdrawn.

### 6.3 Why the share stays at 2.00% anyway

Not because I can defend 2.00% on supply. **I cannot.** On my own cited ceilings the defensible band is **0.125-0.376%**, so 2.00% is 5-16x outside it.

It stays because widget 1 hard-codes `{key:"agentic", floor:2}` and `normalize()` will not return a legal mixture below it. I verified this in the widget source rather than asserting it. Within the course's constraint set there is no legal mixture with less agentic.

**This is the lowest-confidence number in the plan.** If the floor were removable I would set this lane to 0.4% and return 33B to STEM and reasoning. A reviewer is entitled to reply that the honest move was to argue the floor down rather than comply and confess; I think that is a fair charge and I do not have a rebuttal beyond the constraint being stated as hard.

---

## 7. The protected floor

**Indic >= 6.0% and agentic >= 2.0%, per lane, 8.0% together.** Enforced in every length bucket, every curriculum cycle, and inside the anneal — not just on the run average, because a lane can hit its average while vanishing from the last 80B.

**Where 5.5% comes from:** it is the share at which real Indic is served exactly once — 113.9B / 2080B = **5.48%**. Below it the lane is repeating tokens to hold a floor, which defeats the purpose of a floor.

**Why 6.0% and not the 5.48% one-epoch figure.** Because the floor has to be one the **selector** cannot cross, and the selector has its own constant: widget 3's per-iteration OPUS selector hard-codes `LANE_FLOOR = 0.08`, commented *"8% of trained tokens reserved for Indic + agentic"*, and its Always-On lane force-promotes scarce batches until that combined ratio is met. A floor of 5.5 + 2.0 = 7.5% would sit **below** it, so the selector would override my declared floor every iteration and the declaration would be decorative. Lifting Indic to 6.0% makes the combined floor **exactly 8.0%**, so my floor and the selector's agree and the Always-On lane never has to fight the mixture.

So there are three Indic numbers and they do different work: **5.48%** is what one epoch costs, **6.0%** is my always-on floor set to meet `LANE_FLOOR`, and **15.80%** is the served share. The course's separate `indic >= 12` selector floor (widget 1) binds above all of them, which is why section 5.3 concludes one-epoch Indic is unreachable at any legal share.

The real-token clause is **scoped to supply**, because an unscoped version is meaningless:

- **Indic** — 6.0% of 2080B = 124.8B against 113.9B real = **1.10 epochs. Binds.**
- **Agentic** — 2.0% = 41.6B against 0.627B = **66.4 epochs. Cannot bind**, so the floor here protects presence, not freshness.

**Reasoning is excluded** from floor protection. Widget 3 marks it `scarce:false`, and under the English-supply proxy it scores 0.818 — third of seven, above web at 0.776. A floor for a non-scarce lane is a share, not a floor.

---

## 8. The anneal and the reserve

**80B = 50B ballast (62.5%) + 30B reserve (37.5%).**

The reserve, held back from the main run and spent only in the decay leg:

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

Ballast is spent at main-run shares so the mixture does not lurch. Resulting anneal mixture:

| web | code | Indic | STEM | reasoning | long-ctx | agentic |
|---|---|---|---|---|---|---|
| 21.156 | 22.969 | 21.875 | 9.156 | 14.563 | 2.781 | 7.500 |

Sums to **100.000**.

**Mixture shift = 17.64%** (half the L1 distance from the main-run shares). The course preset's own two-phase pair shifts **32.0%**, so this is **44.9% gentler** than the comparison case.

**Two honest limits.** The top-0.6% and top-1.6% quantiles are **extrapolation**: the most aggressive published filter keeps 45.6% under one method, and another filters to the cleanest 25% — nobody has measured a 0.6% slice, so its quality is assumed, not known. And the precedent is thin: Spark Joy's sweep is a **cruising-LR mixture swap, not a decay leg** — they never changed the learning rate — so it supports the mixture choice and not the schedule. Llama 3 405B's anneal was 40M tokens (0.00025%), five orders of magnitude below mine; I am closer to OpenCoder's ratio and I am relying on that single precedent.

---

## 9. Curriculum: stages, seams, packing

| stage | tokens | web | code | Indic | STEM | reason | long | agentic |
|---|---|---|---|---|---|---|---|---|
| Seed | 200B | 45 | 18 | 14 | 12 | 6 | 3 | 2 |
| General | 700B | 38 | 24 | 15 | 12 | 6.5 | 2.5 | 2 |
| Reasoning | 600B | 30 | 25 | 16 | 12 | 11 | 4 | 2 |
| Long-context | 500B | 28.2 | 25 | 17.4 | 9.8 | 9.3 | 8.3 | 2 |
| Anneal | 80B | 21.156 | 22.969 | 21.875 | 9.156 | 14.563 | 2.781 | 7.500 |

Each row sums to 100 (the Anneal row to 100.000; it is quoted to 3dp because 1dp does not close). The four main-run rows time-average to section 0's shares **exactly** at weights 0.10 / 0.35 / 0.30 / 0.25. Three stages are set at round values and the Long-context row is *solved* so the average closes with zero residual.

**Seams.** Five stages have four boundaries. Each gets a **20B linear cross-fade**: 4 x 20B = 80B = **4.0% of the main run**. Widget 8's spike model predicts **1.34x** frozen / **1.23x** unfrozen peak gradient norm at 20B, against its own red line `RED_T = 3.0`. Narrower seams cross it; wider ones spend budget to buy margin already held.

This is the number with the thinnest support in the document: it is priced **only** by the course's own spike model, with no external measurement.

**Packing.** Binary dataset decomposition rather than concat-and-chunk, worth **+2.9 regular / +3.4 long-context** in DatasetDecomp's results (at 1B, which matches our probe scale).

Bucket policy, derived from a micro-replication I ran on a 342-document / 78,581-token corpus: concat-and-chunk gave mean in-document context **421.1** tokens versus **3452.5** under decomposition with a >=256 floor — an **8.20x** separation against the paper's published 1.45x, because that corpus is short-document-heavy. The same run showed a global >=256 floor **discards 44.9% of tokens**. So the floor is applied **only to naturally-long lanes** (books, repo-packed code) and all buckets are kept for short-document lanes. This is a corpus statistic, not a model result.

---

## 10. Difficulty bands, with a real example at each level

Six bands, using widget 7's `DIFF[]` scale verbatim: Nursery, Grade-school, High-school, Undergraduate, Graduate, Research/PhD. The specimen in each row is a concrete piece of text at that level, composed for this document rather than quoted from a dataset — enough for a reviewer to see where each band's boundary sits.

| band | level | a real example of the text admitted |
|---|---|---|
| **B0** | Nursery | *"The cat sat on the mat. The mat was warm. The cat was happy."* |
| **B1** | Grade-school | *"Leaves look green because of chlorophyll. In autumn the tree stops making chlorophyll, so the yellow and orange colours that were always there start to show."* |
| **B2** | High-school | *"Balance: C3H8 + 5 O2 -> 3 CO2 + 4 H2O. If 2.2 g of propane (M = 44 g/mol) burns completely, how many grams of water form?"* |
| **B3** | Undergraduate | *"Show that if f is continuous on [a,b] and differentiable on (a,b) with f(a) = f(b), then there exists c in (a,b) with f'(c) = 0. State where continuity, as opposed to differentiability, is used."* |
| **B4** | Graduate | *"Let (X, S, mu) be a sigma-finite measure space. Prove that L^p(mu) is complete for 1 <= p < infinity, and exhibit a sequence in L^1 converging in measure but not in L^1 norm."* |
| **B5** | Research / PhD | *"Let `M` be a smooth compact manifold and `f: M -> M` an Anosov diffeomorphism. We show the SRB measure varies differentiably under `C^3` perturbation, and give a counterexample when the hyperbolicity constant degenerates on a set of positive measure."* |

**Schedule.** B0-B1 concentrate in Seed (200B), B2-B3 dominate General and Reasoning, B4-B5 rise through Long-context and are heaviest in the anneal, where the top-quantile reserve of section 8 lives.

**No paper supports this ladder**, and one argues against a related idea: PrefCurriculum finds a perplexity gap is not a difficulty axis. The bands are a scheduling device I am declaring, and H5 in section 13 is the test that would retire them.

---

## 11. Reasoning-length bands, with a real example at each level

Four bands, from widget 6. **The same problem at every band**, so length is the only variable: *count the integers from 1 to 1000 divisible by 3 or by 5.* The answer is **467** at every band; only the trace length changes.

| band | steps | tokens | solve rate | budget |
|---|---|---|---|---|
| LOW | 2 | 37 | 61.5% | 15% = 4.26B |
| MEDIUM | 4 | 74 | 76.8% | 30% = 8.52B |
| HIGH | 6 | 161 | 90.9% | 35% = 9.94B |
| ULTRA | **14** | 346 | 95.3% | 20% = 5.68B |

Token counts and solve rates are re-derived from widget 6's own curve, `acc(L) = 0.955 - 0.615 * exp(-L/tau)` with `tau = 0.18 * 346 = 62.28`.

**Budget is 28.4B of trace-shaped tokens, not the 181.7B lane**, and that budget is fully covered by real data: the lane's four non-AON datasets — OpenThoughts2 3.0B, OpenMathReasoning 2.0B, OpenR1-Math 1.6B, NuminaMath 0.5B — total **7.1B**, and 28.4B / 7.1B = **exactly 4.00 epochs**, the same measured-safe cap used in section 6.1. **No trace tokens are generated.** The remaining 78.0B of real reasoning supply is AON, a confirmed V4 corpus of academic prose; section 14 returns to why that matters.

**LOW, verbatim, both steps:**
> 1. Inclusion-exclusion: floor(1000/3) + floor(1000/5) - floor(1000/15).
> 2. = 333 + 200 - 66.

**MEDIUM, verbatim, all four:**
> 1. Count multiples of 3 up to 1000: floor(1000/3) = 333.
> 2. Count multiples of 5 up to 1000: floor(1000/5) = 200.
> 3. Divisible by both 3 and 5 means divisible by 15: floor(1000/15) = 66, counted twice.
> 4. Inclusion-exclusion: 333 + 200 - 66 = 467.

**HIGH — the band's distinguishing feature is step 6, an independent check:**
> 5. Inclusion-exclusion: |A or B| = 333 + 200 - 66 = 467.
> 6. Check by complement: divisible by neither is about 1000 times (2/3) times (4/5) = 533, and 1000 - 533 = 467. Consistent.

**ULTRA — 14 steps. Its distinguishing feature is a second, structurally different verification (steps 9-12) plus explicit endpoint re-examination (step 13):**
> 9. Verify with blocks of 15: within each block, the values hit by 3 or 5 are {3,5,6,9,10,12,15}, that is 7 of every 15.
> 10. 1000 = 66 times 15 + 10, so full blocks contribute 66 times 7 = 462.
> 11. The remainder 991 to 1000 covers residues 1 to 10, and 993, 995, 996, 999, 1000 are divisible by 3 or 5, that is 5 more.
> 12. 462 + 5 = 467, which matches the inclusion-exclusion count.
> 13. Reconsider the endpoints: 1000 is included and is divisible by 5, already counted, and 1 is divisible by neither, correctly excluded.

**Why ULTRA is capped at 20%.** ULTRA buys **+4.40pp** over HIGH for **2.149x** the tokens. Widget 6's own `isWasted` test flags a step as wasted below 0.05 accuracy gain; ULTRA sits just above it, so it is worth buying but not worth scaling. The 15/30/35/20 split across the other three bands is mine and unevidenced; only the ULTRA cap is course-derived.

---

## 12. The data gate

The criteria make this a **prerequisite**: a mixture is only as trustworthy as the cleaned and documented tokens behind it. Widget 9 supplies a `lic` field and a confidence `tag` for all 32 datasets, so the gate can be stated in the inventory's own terms rather than in the abstract.

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

**Inventory-wide, only 18.8% of tokens are confirmed** (1205B of 6402B). **The two lanes with zero confirmed tokens are the two this plan leans on hardest for novel capability.** Every token count in sections 3 and 5 for those lanes is an estimate, and their supply figures should be read with that attached.

### 12.2 The gate I am declaring

No lane enters the run until all four hold:

1. **Licence recorded and compatible.** Available for all 32 datasets. Two entries need review before use: SWE-Gym and SWE-smith are `task licenses` (per-task, not blanket) and OpenHands rollouts are `mixed`. All three are in the agentic lane, which is also 0% confirmed.
2. **Token count confirmed, or the lane's numbers labelled `approx` wherever they appear.** Currently 5 of 7 lanes are majority-approx.
3. **Decontamination against every benchmark in section 4**, n-gram overlap at 13-gram, run on the anneal reserve first. Not yet performed. This is the gap I would close first: the reserve is 30B of top-quantile selected text, and quality selection actively concentrates benchmark-like material. Spark Joy notes the anneal is where contamination has maximum leverage on final scores.
4. **Per-tier provenance for Indic**, since the A/B/C/D split in section 5 is the whole defence and it rests on Sangraha's own verified / unverified / synthetic partition.

Each item is a **threshold, not a checkbox**:

| gate | threshold | current | status |
|---|---|---|---|
| licence | 100% of served tokens under a recorded, compatible licence | 32/32 recorded; **3 agentic entries** need review | **blocked** |
| confirmation | >= 50% of a lane's served tokens `conf`, else the lane's figures carry an `approx` label at every point of use | reasoning 91.7%; **5 lanes below 50%**; long-context and agentic at **0.0%** | labelled, not met |
| decontamination | 13-gram overlap with any section-4 benchmark **< 0.1%** of the lane, anneal reserve first | **not run** | **blocked** |
| Indic provenance | per-tier attestation for 100% of the A/B/C tokens the split depends on | Sangraha's own partition covers 88.0B of 113.9B (**77.3%**) | partial |

**Honest status: this gate is specified, not passed.** Two of four are blocked outright. On the criteria's own terms the mixture is not yet trustworthy, and saying so is more useful than implying a clean bill.

### 12.3 The cleaning programme, aimed at the starved slots

Cleaning continues alongside the plan toward a cumulative target, and the mixture itself says where to point it. The course defines a slot as **starved** when its share sits below `WEIGHTED_MIN = 8` (widget 1). On this mixture that is exactly two lanes:

| starved slot | share | pool now | pool needed | **cumulative cleaning target** |
|---|---|---|---|---|
| long-context | 4.45% | 40.0B independent | 91.2B for 1.00 epoch | **+51.2B** multi-document real text |
| agentic | 2.00% | 0.627B | 11.5B for the 4-epoch cap with zero generation | **+10.9B** collected trajectories |
| | | | | **62.1B total** |

**62.1B is the cumulative target**, and it is the number that would retire this plan's two worst weaknesses at once: it takes long-context off repetition and eliminates all 43.5B of agentic generation. Priority is long-context, because 51.2B of multi-document text is a *collection and packing* problem against sources that exist, whereas 10.9B of real agent trajectories is a **17.4x** expansion of every such corpus known to me and is the harder ask by far.

Nothing else is worth cleaning first. The five funded lanes are at or under 2.93 epochs on real supply, so additional clean tokens there would displace tokens already paid for rather than replace generated ones.

---

## 13. Hypotheses and the proxy protocol

Every share above is a hypothesis. Each one below names the metric that would refute it and what I would do then.

**Cost basis.** Full run = `6 * 120e9 * 2.080e12` = **1.498e24 FLOPs**. A 1B-parameter arm on 10B tokens is `6e19` = **0.0040%** of the run; a 3B arm on 30B tokens is `5.4e20` = **0.0361%**. The whole programme below — **14 arms at 1B plus 5 at 3B, three seeds each** — costs **1.06e22 FLOPs = 0.71% of the run.** Verification is not the expensive part; not doing it is.

**Three seeds, not one.** The document's own resolution floor is +/-0.5pp at 1.5B and 0.60/0.86pp at 7B. Any threshold below ~1.0pt is unreadable at n=1, so every arm runs three seeds and every threshold below is stated against the seed mean.

| id | hypothesis | scale | metric | confirm | refute | on refute |
|---|---|---|---|---|---|---|
| **H0** | the whole mixture beats the course preset | 1B, 2 arms | mean of 6 LM-Eval tasks | >= +0.8pt | <= -0.3pt | adopt the preset; this plan is wrong as a whole |
| **H1** | decomposition packing beats concat-and-chunk | 1B, 2 arms | MDQA | >= +2.0 | <= +0.4 | revert to concat-and-chunk, reclaim the bucket machinery |
| **H2** | 94.5% generated agentic still teaches call form | 1B, 3 arms | BFCL AST-match | >= +3.0 vs no-agentic | <= +1.0 | cut the lane to the 0.4% floor argument in section 6.3 and return 33B |
| **H3** | Indic real tiers survive N = 2.00 | **3B**, 3 arms | held-out CE on Indic + XCOPA | CE gap <= 0.02 | CE gap >= 0.05 | drop to N = 1.50, synthetic to 48.8% |
| **H4** | an 80B anneal beats a 40B anneal | 3B, 2 arms | MMLU + GSM8K mean | >= +1.0pt | <= +0.2pt | halve the anneal, return 40B to the Reasoning stage |
| **H5** | the B0-B5 ladder beats difficulty-shuffled | 1B, 2 arms | GSM8K + MATH mean | >= +1.0pt | <= +0.2pt | delete section 10 entirely and shuffle |
| **H6** | 20B seams keep peak grad-norm under `RED_T` | 1B, 3 arms | peak grad-norm at boundary | < 2.0x | > 3.0x | widen to 40B, cost 4% more of the run |
| **H7** | the 15/30/35/20 length split beats uniform | 1B, 2 arms | GSM8K + solve-rate-vs-tokens | >= +0.8pt | <= +0.2pt | flatten to uniform 25% |

**H3 is at 3B on purpose.** It is the test of my most-contested number, and section 5.2 is the reason it cannot be run at 1B: UniMax measured the repetition effect as **absent at 1.2B** and conspicuous only at 13B. A 1B null would be unpublishable evidence in my own favour. 3B is the most I can specify and still be honest that even it may be under-powered — the effect they saw appears between 3.7B and 13B.

**MMLU appears only at 3B or above.** NVIDIA reports it solely at 8B, "when the experimental setting allows for a non-random score." H0/H2/H5/H7 therefore use the six-task LM-Eval mean and BFCL at 1B, and MMLU enters only at H4.

**The commitment.** No number in this document is trusted at full scale until its hypothesis has cleared at both 1B and 3B. Concretely: the shares in section 0 are provisional until H0 clears at 1B; the Indic cap of section 5 is provisional until H3 clears at **3B**; the 80B anneal of section 8 is provisional until H4 clears at 3B. If a hypothesis refutes, the *"on refute"* column is executed before the run starts, not after. A data decision is a hypothesis until a cheap experiment has tested it, and at **0.71% of the run** there is no budget argument for skipping the test.

**Where a result lands in neither band**, the value stands *provisionally* and the arm re-runs one scale up; it does not graduate to trusted. An undefined middle is not a licence to keep the number for free.

**Nothing here has been run.** No model has been trained. That is the honest position and it caps this submission below the top band by design; the alternative would be to claim a result I do not have.

---

## 14. Where this is weakest

Ordered by how much damage a reviewer could do.

1. **Agentic 2.00%.** 73.4x on the stated pool, 92.6x against genuinely-collected trajectories, 94.5% generated, 0% confirmed tokens, and my own ceilings support 0.125-0.376%. Held only by a hard-coded floor. Section 6.
2. **The Indic share versus UniMax's scale result.** My own evidence base contains a measurement that the repetition penalty **grows with scale** and is conspicuous at 13B while invisible at 1.2B. I am at 120B. This is the strongest argument against section 5 and I have no answer to it beyond running H3.
3. **Reasoning is 8.50% but only 7.1B of the lane is trace-shaped.** 78B of the 85.1B real supply is AON, a confirmed V4 corpus, but it is not chain-of-thought. So the lane is large and the thing the lane is *named for* is small — arguably a worse instance of the criteria's concern than agentic, because agentic is small and loudly flagged whereas this is large and easy to miss. Two-Phase got its gain from about 1.3% of a phase being reasoning-shaped, and I serve 28.4B/2080B = **1.37%**, so the plan may be adequate by accident; the share is not what makes it so.
4. **Long-context has no multi-document data.** The inventory has packed books and packed repos. MDQA is a multi-document benchmark. Packing raises effective context length; it does not manufacture cross-document retrieval structure. Training length is 8192 and nothing here licenses a 32k or 128k claim.
5. **The 0.6% and 1.6% reserve quantiles are unmeasured.** The most aggressive published filter keeps 45.6%.
6. **Seam width 20B is priced only by the course's own spike model.** No external measurement.
7. **The B0-B5 ladder has no paper behind it**, and PrefCurriculum argues against the nearest published analogue.
8. **The 15/30/35/20 length split is mine.** Only the ULTRA cap is derived.
9. **The repetition law is fitted to 9B and applied at 120B.** The extrapolation axis moved from pool size to model scale.
10. **The data gate is specified and not passed.** Decontamination has not been run, and three agentic licences need review. Section 12.
11. **Almost nothing has error bars.** CLIMB's own checklist says no; Spark Joy, PrefCurriculum and DatasetDecomp are single- or two-seed. DatasetDecomp publishes +/-1.6 MDQA over two seeds, which is why H1's confirm bound is set at +2.0 rather than the +1.85 I would otherwise have used.
12. **No proxy has been run.** Section 13 is a protocol, not a result.

---

## Appendix: what to re-check first

If you have five minutes, four numbers carry the most weight and are the cheapest to check by hand:

- **STEM 146.0B** — sum `proof-pile-2` 55 + `D4 STEM (V4)` 49 + `peS2o` 42 in widget 9. If this is wrong, section 3 is wrong.
- **Real Indic 113.9B** — Sangraha verified 64 + unverified 24 + IndicCorpV2 20.9 + BPCC 3 + Samanantar 2, excluding the 162B tagged `synth`. If this is wrong, section 5 is wrong.
- **Lane shares time-average to section 0** at stage weights 0.10 / 0.35 / 0.30 / 0.25. If this fails, sections 2 and 9 disagree.
- **Anneal mixture sums to 100.000** from 50B ballast at main-run shares plus the 30B reserve. If this fails, section 8 is wrong.

If you have one minute instead, `python3 verify.py` does all four and 50 more. Zero dependencies, **54 checks, 0 failing**. It **parses this document** and compares what it publishes against the inventory, so editing a number here breaks the suite:

- **33 DOCUMENT-vs-WORLD** — a figure scraped out of these tables against one derived from `widget_9_dataset_inventory.html`. This is the only class that tests the document. It is what returns 146.0B for STEM rather than the course's 250B constant, decomposes the Indic tiers from the inventory's `tier` and `tag` fields, and books the 18.4B of distilled traces.
- **21 STRUCTURAL** — published numbers against each other: shares sum to 100, stage rows time-average with zero residual, the anneal's *printed digits* close to 100.000, arm counts in the prose match the section-13 table. These catch self-contradiction and **cannot tell you a share is a bad choice.**

Two things worth stating plainly. An earlier version hardcoded every expected value and never opened this file, so it could not have detected the document silently reverting a correction; four such perturbations now trip failures. And three checks were mislabelled as independent where the quantity of interest cancelled algebraically — efficiency is `effective(U,ep)/(U·ep)`, in which `U` cancels — so they are now marked structural.

**Neither class can confirm this mixture trains well.** Only section 13's proxies could, and none has been run.
