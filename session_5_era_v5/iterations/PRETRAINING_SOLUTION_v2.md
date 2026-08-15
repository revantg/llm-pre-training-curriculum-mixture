> # SUPERSEDED — DO NOT GRADE THIS FILE
>
> This is **v2**, an intermediate iteration retained only as an audit trail.
> first full draft; superseded before any adversarial review.
>
> **The deliverable is [`../SOLUTION.md`](../SOLUTION.md).**
> Numbers here are known to be stale and several were retracted. See
> [`iterations/README.md`](README.md) for what changed and why.

---

# V5 Pretraining Mixture & Curriculum — v2 (Pretraining + Anneal Only)

**Scope:** Main pretraining run + anneal/mid-training decay leg of that same run (same next-token CE, low LR, curated reserve). SFT/RLVR/DPO out of scope. Model ~120B, Main **2T**, Anneal **+80B (4%)**, OPUS keep ~40% (~6× effective).

## 1. Main-Run Lane Shares

| Lane | Share | Demand @2T | Unique Supply | Verdict | Benchmarks |
|---|---|---|---|---|---|
| General web | **34%** | 680B | 4.5T | 0.15× covered | MMLU, MMLU-Pro, ARC, HellaSwag |
| Code | **24%** | 480B | 1.1T | 0.44× covered | LiveCodeBench, Aider, HumanEval, MBPP, MultiPL-E |
| Indic | **16%** | 320B | 276B (114B real / 162B synth) | 1.16× repeat | MILU, IndicGenBench, MGSM (multilingual), Flores-101 |
| STEM / math | **12%** | 240B | 250B | 0.96× covered | AIME, GPQA, MATH, GSM8K |
| Reasoning traces | **6%** | 120B | 85B | 1.4× repeat | AIME, GPQA, HLE, BBH |
| Long-context | **6%** | 120B | 100B + 423B natural 8k-contiguous* | 1.2× repeat / reframed | long-eval (LongBench, RULER, MDQA) |
| Agentic | **2%** | 40B | **0.63B** | **63× — must generate** | SWE-bench, τ-bench, BFCL, GAIA, BrowseComp |

*Long-context "supply" reframed by Dataset Decomposition: natural web alone is **9.4% at exactly 8192** and **22.9% at ≥4k** — more than 6%. At 2T that's ~423B genuine 8k-contiguous tokens at zero cost via binary decomposition vs our 0.1T inventory. Lane is a packing decision, not a scarcity.

**Web filtering (Two-Phase):** Natural CC is **64% Low**; zeroing Low lifts MMLU **42.94→56.10**. Do it. Never gate on popularity: `stars>=5` gives *lower* loss but *worse* HumanEval/MBPP (OpenCoder Figs 10-11).

**Code dedup (OpenCoder):** ~75% exact duplicates; file-level **32.74B** Python vs repo-level **99.47B** — file-level *wins* at every budget. Use file-level; random concat into 4k/8k, not repo packing.

**Confidence:** web 34% **high**; code 24% **high** fundable / **medium** exact %; STEM 12% **medium-high** (zero headroom); reasoning 6% **medium-high**; long 6% **low-medium** (revised below); agentic 2% **low** (crisis).

## 2. Indic Split — Rebalanced (Composer Default Not Fundable)

Composer A40/B25/C20/D15 fails: C needs 64B vs **5B** unique (**12.8×**).

| Tier | Share of Indic lane | Demand | Supply | Repeat | Source |
|---|---|---|---|---|---|
| **A verified native** | **40%** | 128B | 64B | 2.0× | Sangraha verified |
| **B unverified crawl** | **30%** | 96B | 44.9B | 2.1× | Sangraha unverif + IndicCorpV2 |
| **C translated / parallel** | **8%** | 25.6B | 5B | 5.1× | BPCC + Samanantar |
| **D synthetic** | **22%** | 70.4B | 162B | 0.43× | Sangraha synthetic (rephrased) |

D at 22% < Demystifying **~30% rephrase ceiling** (<50% always); invented textbooks ceiling is **≤3%**, so D must be *rephrased verified Indic*, not invented.

**Hazards:** (1) App D.2 uncovered unigrams + frozen English tokenizer spike per-token loss → V4 Hindi×frozen 150× grad event; need Indic-aware tokenizer + unfrozen embeddings. (2) PrefCurriculum Fig 6b: a global PD/difficulty sort front-loads culture-heavy text (low-PD more cultural 0.69 vs 0.59) — native Indic would be front-loaded then starved; PD Spearman 0.41, weak-model-dominated, so tokenizer artefacts sort Indic. Mitigation: score per-lane, never globally. (3) MAP-Neo cuts Chinese 25%→8.5% entering mid-training — the one low-resource precedent goes opposite our 16%→28% raise; only counter-precedent is Yi-Lightning qualitative.

**Confidence:** 16% lane **medium-high**; rebalance 40/30/8/22 **medium**; C at 5.1× **medium-low** (short segments ≠ documents).

## 3. The Two Weak Lanes — Stated as Weak

### Agentic 2%
Organic at 5-epoch ceiling gives **3.15B ≈0.16% of 2T**. The other 92% must be generated — past every measured repeat ceiling and not rephrase (no source doc). Textbook-class invention is collapse-patterned (Demystifying) and absorbing (Collapse). **Resolution while staying in pretraining:** keep 2% but as **3.1B real + 36.9B environment-grounded, verifier-filtered rollouts from a frozen stronger teacher** (outside Collapse's self-consuming loop; verifier breaks absorbing chain). Mask per Widget 5: plan/calls/recovery green, observations grey. Gate on 1B/3B *agentic* proxy, not English CE. Fallback: drop to 0.6% if proxy fails.

**Confidence: low** — no pretrain-scale agentic paper exists.

### Long-Context 6%
OpenCoder never exceeds 8k, packs randomly, prefers file-level. **Dataset Decomposition** is the new evidence: at 1B, order alone **+5.0 MDQA-30** and RoPE 10k→100k **+5.4 MDQA** at zero tokens; threshold behavior — multi-doc QA ≈0 until pretrain length > eval context, then jumps and flats. **Any mix lacking D12/D13 scores 0.0–0.4** on MDQA-20/30; 9.4% at 8192 saturates (9.4%→25% moved MDQA 21.9→22.1). Natural web alone already supplies the floor; curated 0.1T retains distinct multi-doc reasoning job. Free wins dominate the lane.

**Confidence: low-medium** — floor is proven, 6% sufficiency unmeasured (smallest non-zero tested is 9.4%; 2/4/6% never measured).

## 4. Anneal Reserve — 80B (4% of Main)

| Component | Share | Tokens |
|---|---|---|
| Original-distribution ballast | **60%** | 48B |
| Tier-A verified Indic | 14% | 11.2B |
| Long reasoning traces | 10% | 8B |
| Algorithmic / competition code | 8% | 6.4B |
| Long agent trajectories | 5% | 4B |
| Verified synthetic + textbooks | 3% | 2.4B |

**Why 4%, not 2%:** Mid-Training Survey Table II splits mid-training into two clusters: **Cluster A terminal fast-decay 1–5%** (MiniCPM 1.96%, Hunyuan-A13B 1.48%, **OpenCoder 3.85%**, Pangu 4.00%, Hunyuan-Large 4.76%) vs **Cluster B full second stage 9–51%** (SmolLM2 9.03%, Qwen3 14.08%, Zamba 51%). Our 80B is Cluster A, high end but inside; Two-Phase 40% is Cluster B, incomparable. **Spark Joy sweep (7B/1T):** 50B/5% → 100B/10% → 200B/20% → 300B/30%; MMLU peaks at 100B, Core Avg at 200B. **No point below 50B exists.** Our 80B sits between 50B and 100B (inside), **40B is below every point**. Absolute knee at 50–100B, not fraction.

**Why 60% ballast:** Every disclosed recipe overlays **10–40% new on old**: Zamba 60/40, Phi-4 70/30, Llama-3 probe 70/30, Nemotron-4 "majority already-seen." Our 32% mass moved (68% continuity) sits next to Zamba as most aggressive precedent; Spark Joy filtered web held at 30% (0.82×) explicitly "to prevent large distribution shift." Also: **Hunyuan-Large anneal = top 5% quality tokens** — 10× stricter than OPUS 40%; reserve quantile should be much stricter than main.

**Reserve is reweighted, not repeated:** Spark Joy Domain bucket never exceeds **1.12 epochs** even at 30% leg; our anneal slices are 0.17/0.06/0.08/0.03 epochs for reason/long/Indic/STEM — safe.

**Hold, don't discover at 98%:** Lecture §9 + DatasetDecomp: cyclic curriculum exposes reserve **interleaved** (Grow-P2 1→8 cycles MDQA 25.9→28.0); monotone tail is inferior on CSR.

**Ablation:** OpenCoder Fig 9 — without HQ, HumanEval ~0.33 vs 0.47, gap never closes.

**Confidence:** holding a reserve **high**; 4% **medium-high** (one direct precedent + absolute-token reading of Spark Joy); internal mix **medium**.

## 5. Protected Always-On Floor

**Floor: 8% of every iteration's accepted tokens for Indic + agentic + reasoning, real tokens only, bypassing OPUS.**

Evidence converges three ways:
- **Spark Joy sans-math:** 100B final phase without math → MMLU **-5.98 vs doing nothing**, Reading Comp **-10.54**, Core Avg -2.83. A final phase can *unlearn* below baseline.
- **PrefCurriculum Fig 6b:** PD ordering sends **ArXiv 88% early, GitHub 66% early, Wikipedia 86% late** while claiming "does not skew" — self-contradiction; code/papers front-loaded, encyclopedia back-loaded.
- **Collapse:** same real N every generation bounds drift; finite window only delays (mean absorption 17→95→216 for K=1→5→10).
- **CLIMB:** code cluster C20 → **0** when not in objective; DatasetDecomp: empty buckets get odds 0 and vanish — so **"8% of run" is insufficient; it must be 8% in every bucket and every cycle**.

PrefCurriculum's S-shape gives a defensible **ramp shape**: **43.9% of run blended** (0.9→0.1 over p∈[0.28,0.72]), hard switch worthless. OPUS is orthogonal (whether vs when), so they compose.

**Confidence: high.**

## 6. Curriculum

| Stage | web | code | reason | long | indic | stem | Difficulty |
|---|---|---|---|---|---|---|---|
| Seed | 55 | 15 | 3 | 2 | 15 | 10 | B0–B1 |
| General | 45 | 20 | 6 | 3 | 16 | 10 | B1–B2 |
| Reasoning | 25 | 28 | 18 | 5 | 14 | 10 | B2–B3 |
| Long-context | 18 | 30 | 16 | 18 | 12 | 6 | B3–B4 |
| **Anneal** | 8 | 22 | 20 | 10 | 30 | 10 | B4–B5 |

Agentic at 2% floor throughout, Tier-A held for anneal. Widget 7 anchors kept.

- Two-Phase order alone +3.4 avg (GSM8K +9.5, code +2.8); CLIMB breadth early / concentration late; Widget 6 trace-length distribution.
- **DatasetDecomp refinement:** prefer **binary decomposition VSL** over concat-and-chunk (free +2.9 regular, +3.4 long-avg, 20% faster), RoPE **100k from scratch** (free +5.4 MDQA), and **Grow-P2×8** cyclic short→long (free +5.0 MDQA). Our Long-ctx before Anneal order is the *minority* order in survey (10 of 11 long stages follow the anneal; Pangu holds 32K through both) — state as deliberate choice to get long-context before LR decays, with cyclic exposure.
- **Seam:** 20B-token blended warmup at each of 5 transitions (period-correct: Spark Joy hard-switched 34pp with no LR change and no grad trace — silence, not safety; V4 150× spike; DatasetDecomp short-first suppresses spikes). Also: MidTrainSurvey notes MiniMax-01 linearly interpolates weights in transitions.

**Confidence:** stage order **medium-high**; anchors **medium**; difficulty ladder **medium**; 20B warmup **medium**.

## 7. Validation Plan

1. CLIMB-style proxy ranking first: **62M ≈ 350M** (60.11 vs 60.41), 112 configs at 4:2:1 beats baselines.
2. Every lane's benchmark in the objective — otherwise search zeroes Indic/agentic.
3. **1B then 3B** confirmation (lecture §12).
4. Spark Joy branching: **40B probe ≈1/50 of a 2T/120B run** (~2.9e22 of 1.44e24 FLOPs) — a dozen probes is ~1/4 of a run. Llama-3 40B/30% probe template: 50%-trained model, LR→0 over 40B.
5. Kill criteria declared up front: agentic falls back to 0.6% if proxy fails; Indic C cut 8%→4% if repeat degrades.

**Confidence: high.**

---

## Confidence Summary

| Item | Confidence | Weak Link |
|---|---|---|
| Run size 2T | **High** | Declaration |
| Web 34% + zero Low | **High** | — |
| Code 24% file-level | **High** fundable / **Medium** exact % | No 7-lane code sweep |
| STEM 12% | **Medium-high** | 0.96× — zero headroom |
| Reasoning 6% | **Medium-high** | Value shown only at ~1% slices |
| Indic 16% | **Medium-high** | — |
| Indic tiers 40/30/8/22 | **Medium** | No Indic paper |
| Indic C 5.1× | **Medium-low** | Short segments ≠ documents |
| **Long-context 6%** | **Low-medium** | Unmeasured 2/4/6%; free wins dominate |
| **Agentic 2%** | **Low** | 63×; verifier argument unmeasured |
| Anneal exists | **High** | — |
| Anneal 4% (80B) | **Medium-high** | One direct precedent; now stronger via survey Cluster A + Spark Joy absolute knee |
| Anneal internal mix | **Medium** | My shape; survey overlay 10–40% supports 32% |
| OPUS floor 8% real | **High** | — |
| Curriculum order | **Medium-high** | Anchors unvalidated at 120B; long-before-anneal is minority order |
| Seam warmup 20B | **Medium** | Width unmeasured |
| Proxy validation | **High** | — |

**Three numbers a reviewer should attack, in order:** agentic 2%, long-context 6%, Indic C 5.1×.
