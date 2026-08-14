# R6 · Difficulty and reasoning-length bands · R7/E11 · Proxy protocol

Staging file for SOLUTION v4. Addresses the three requirements v3 failed:
**R6/E10** bands with a concrete example at each level (stated twice in the assignment),
**R7** commitment to 1B/3B proxy runs, **E11** named confirm-or-refute metric per hypothesis.

---

## 6a. Difficulty bands — B0 to B5

Band names and definitions are the course's own (`widgets/widget_7_curriculum_stages.html`, `const DIFF`). The **example** column is what R6 demands and the widget does not supply; each is a concrete artifact of that band, with the lane it comes from.

| Band | Level | Widget definition | Concrete example | Primary lane | Stage where it dominates |
|---|---|---|---|---|---|
| **B0** | Nursery | "simple children's sentences" | *"The cat sat on the mat. The mat was red."* | web | Seed |
| **B1** | Grade-school | "basic grade-school text" | *"Water boils at 100 degrees Celsius at sea level."* — plus arithmetic word problems with integer answers | web, Indic | Seed → General |
| **B2** | High-school | "high-school level material" | A Wikipedia article on photosynthesis; a 30-line Python script with one function and a loop | web, code, Indic | General |
| **B3** | Undergraduate | "undergraduate coursework" | A GSM8K-style multi-step word problem; a single-file module with tests; an `IndicGenBench` summarization pair | code, STEM, reasoning | Reasoning |
| **B4** | Graduate | "graduate-level texts" | An `AIME` competition problem with a worked solution; a `SWE-Gym` task with a repository checkout; a `peS2o` paper section | reasoning, STEM, agentic | Reasoning → Long-context |
| **B5** | Research / PhD | "research and PhD-grade papers" | A `GPQA Diamond` graduate physics item; a `FrontierMath` problem; a `proof-pile-2` formal proof; a full multi-file `SWE-smith` trajectory with recovery | reasoning, agentic, STEM | Long-context → **Anneal** |

**How the bands bind to the mixture.** The difficulty ladder is not a seventh lane; it is a filter applied *inside* every lane, and it is what the stage profiles in §6 are actually ramping. Two rules:

1. **Monotone floor, not a hard gate.** Each stage admits its band and everything below it, never bands above. Seed admits B0–B1; General B0–B2; Reasoning B0–B3; Long-context B0–B4; Anneal B0–B5. Removing low bands later would repeat Spark Joy's failure — their Language Understanding lane was **negative at every phase length** (−0.47 / −1.11 / −1.44 / −1.17) precisely because the bulk-web bucket that carries easy fluency text was zeroed.
2. **B5 is reserve-only.** B5 material is withheld from the main run and spent in the anneal. This is the same object as the anneal reserve in §4, expressed on the difficulty axis instead of the lane axis.

**Honest limit.** No paper in the nine studied a difficulty ladder directly, and one argues against the naive reading: Preference Curriculum's PD metric shows logical-reasoning requirement is **identical across its easy and hard halves (0.72 vs 0.72)**, and its "hard" half needs *less* scientific content (0.61 vs 0.70). So a difficulty ladder cannot be built from a perplexity-gap score. Ours is built from **source provenance and benchmark level**, which is a labelling decision, not a measured one. It is a design bet, flagged as such.

---

## 6b. Reasoning-length bands — LOW / MEDIUM / HIGH / ULTRA

These are the course's own four effort tiers (`widgets/widget_6_reasoning_effort.html`). All four solve the **same problem**, which is the worked example R6 asks for:

> **Problem (identical at every band):** How many integers between 1 and 1000 are divisible by 3 or 5?
> **Answer: 467** — correct at every band. Only the solve *rate* changes.

Token counts and solve rates below are **computed from the widget's own tokenizer and accuracy curve**, not estimated: regex `[A-Za-z]+|\d+|[^\sA-Za-z0-9]`, and `acc(L) = 0.955 − (0.955 − 0.34)·exp(−L/τ)` with `τ = 0.18 · ultra_tokens`.

| Band | Steps | Trace tokens | Solve rate | Example first step | Share of reasoning lane | Tokens |
|---|---|---|---|---|---|---|
| **LOW** | 2 | **37** | **61.5%** | *"Inclusion-exclusion: floor(1000/3) + floor(1000/5) − floor(1000/15)."* | 15% | 25.5B |
| **MEDIUM** | 4 | **74** | **76.8%** | *"Count multiples of 3 up to 1000: floor(1000/3) = 333."* | 30% | 51.0B |
| **HIGH** | 6 | **161** | **90.9%** | *"Let A = multiples of 3 and B = multiples of 5 inside [1, 1000]."* | 35% | 59.5B |
| **ULTRA** | 14 | **346** | **95.3%** | *"Restate the goal… then verify two independent ways."* | 20% | 34.0B |

Lane total 170.0B against 85B unique reasoning supply = **2.00× repeat**, inside Two-Phase's measured organic ceiling (6 epochs high-quality crawl, 8 epochs math; 12 hurts).

**Why this specific shape, and why ULTRA is capped at 20%.** The widget's own accuracy curve shows **ULTRA buys only +4.40 points over HIGH** (95.3% vs 90.9%) while costing **2.15× the tokens** (346 vs 161). The widget flags exactly this case as *"wasted effort"* — its threshold is a gain below 5.0 points. So ULTRA is the smallest band and its traces are concentrated in the anneal, reserved for problems where HIGH actually fails. HIGH carries the largest share because it is where the curve is still buying accuracy per token.

**Why all four bands must exist at all.** The effort dial is not created at inference time; it selects among behaviours the model was trained to produce. A model shown only long traces cannot answer briefly, and one shown only short traces has nothing to select when asked to think. This is the one place where the reasoning lane's *internal distribution* — not its share — is the deliverable.

**Cross-check against the papers.** Two-Phase reached GSM8K **30.86 → 40.33** with reasoning-shaped task data at **1.3% of its second phase**, i.e. the capability is reachable from a small, well-placed slice — which is why our 8.5% lane with a length distribution is defensible rather than greedy. Nobody published a trace-length distribution, so the 15/30/35/20 split is ours; the ULTRA cap is the only part with a course-data justification.

---

## 7. Proxy protocol — R7 and the E11 ceiling

E11 is tiered: a plan is *good*; a testable hypothesis is *excellent*; **naming the confirm-or-refute metric is *highest*; running it and returning numbers is *very highest*.** Each hypothesis below therefore carries a scale, a named metric, a numeric threshold, and the action on refutation.

Cost basis (6ND): a 40B-token probe on 120B params ≈ **2.9e22 FLOPs** against ≈ **1.44e24** for the full 2T run — about **1/50 of a run** per probe. Probes at 1B are ~1/120,000 of that. Branching protocol is Llama 3's: take a partially trained checkpoint, decay LR linearly to 0 over the probe, hold the candidate at **30% against 70% default mix**.

| # | Hypothesis under test | Scale | Named metric | Confirms if | Refutes if | Action on refute |
|---|---|---|---|---|---|---|
| **H1** | Long-context at 4.5% is sufficient (the 2–9% region nobody measured) | 1B, 100B tokens, 4 arms: 0% / 2% / 4.5% / 9.4% | **MDQA-30 accuracy** (≈6k context) | 4.5% arm ≥ 90% of the 9.4% arm's score | 4.5% arm < 75% of it | raise to 9.4%, take from web |
| **H2** | Verified-generated agentic trajectories transfer | **3B**, 40B branch probe, 3 arms: format-only / +verified-generated / +unverified-generated | **SWE-bench Verified pass@1** and **BFCL AST-match** | verified arm beats format-only by ≥3 pts on SWE-bench Verified | gain < 1 pt | **drop agentic to 0.5%**, mass to code and web |
| **H3** | Indic tier C survives 5.06× repetition | 1B, 100B, 3 arms: C at 8% / 4% / 0% | **IndicGenBench chrF** + **MILU accuracy** | 8% arm ≥ 4% arm on both | 8% arm > 1 pt below on either | C → 4%, mass to D |
| **H4** | A 4% anneal beats 2% (below Spark Joy's smallest measured arm) | 1B, branch at 96% and 98% of run | **core-average** of MMLU + GSM8K + HumanEval | 4% arm ≥ 2% arm by ≥1.0 pt | ≤ 0 pt | revert to 2%, bank the compute |
| **H5** | Raising Indic in the anneal does not trigger the MAP-Neo effect | 1B anneal arms: Indic 21.5% / 15.8% / 8.5% | **MILU + Flores-101 chrF**, with **MMLU as the forgetting check** | Indic metrics win and MMLU loses ≤1 pt | MMLU loses >1 pt | flatten Indic across the anneal |
| **H6** | A 20B seam blend keeps the Indic transition stable | 1B, gradient-norm trace at the Indic seam, blends of 0B / 5B / 20B, embeddings **unfrozen** | **peak gradient-norm multiplier** vs pre-seam baseline | peak < 3× | peak > 3× | widen the band until it is |
| **H7** | Reasoning-length bands produce a controllable dial | 1B, 100B, arms: 15/30/35/20 split vs HIGH-only | **spread in trace length** between requested LOW and ULTRA, and accuracy at each | LOW/ULTRA trace-length ratio ≥ 4× with ULTRA accuracy ≥ LOW | ratio < 2× | widen the band spread |

H6's 3× threshold is the instability line from the course's own gradient-norm widget; H1's arms bracket the exact region Dataset Decomposition left unmeasured (their smallest non-zero long-share is 9.4% and the next step down is 0%).

### What we actually ran

Full 1B/3B training is not available in this environment, so H1–H7 remain specified-but-unrun; the spec claims the **"highest"** E11 tier, not "very highest," and says so.

Two things *were* executed and are reproducible from this repo:

**(a) The whole mixture is executable arithmetic, not asserted numbers.** Stage profiles time-average to the declared lane shares within 0.6pp on every lane; every row sums to 100; every demand, coverage ratio, Indic tier repeat factor, anneal component and per-lane anneal epoch count is computed. The 19.5% mixture shift is a computed ½·L1 distance.

**(b) A micro-replication of the packing claim that the long-context decision rests on.** Dataset Decomposition's average-context formula `Σl(l−1) / 2Σl` applied to a 342-document / 78,581-token corpus of our own papers and lecture notes:

| Arm | Sequences | Mean length | Avg in-document context |
|---|---|---|---|
| original documents | 342 | 229.8 | 3486.5 |
| concat-and-chunk @2048 | 380 | 206.8 | **421.1** |
| decomposition, all buckets | 1,375 | 57.1 | 1917.6 |
| decomposition ≥256 | 59 | 733.3 | **3452.5** |

Concat-and-chunk split **11.1%** of documents at a chunk boundary. The direction replicates — decomposition ≥256 carries **8.20×** the in-document context of concat-and-chunk — but our ratio badly overshoots the published **1.45×** (1344 vs 930), for two reasons we can name: our corpus is short-document-heavy (median 104 tokens vs RefinedWeb's 598 mean), and the ≥256 filter **discards 44.9% of our tokens** where on RefinedWeb it is nearly free.

That overshoot is the useful part, and it changes a design decision: **apply decomposition with all buckets to short-document lanes** (Indic snippets, QA-format agentic data, parallel corpora) **and the ≥256 variant only where documents are naturally long** (books, repo-level code, long CoT). A global ≥256 floor would silently delete almost half of the Indic lane — which is precisely the per-bucket starvation that §5's floor exists to prevent.
