# Session 5 · cross-paper evidence map

Nine papers, read in full, every figure inspected. Per-paper briefs in `papers/<slug>/brief.md`.

| Slug | Paper | Scale actually tested | Role |
|---|---|---|---|
| climb | Nemotron-CLIMB 2504.13161v2 | ≤1B params, 40B–400B, English | *Search* the mixture instead of guessing it |
| two-phase | Two-Phase Pretraining 2412.15285v1 | 8B/25B, 1T–15T, English | Phase-1 vs Phase-2; epoch ceilings |
| opencoder | OpenCoder 2411.04905v3 | 1.5B/8B, 2.0–2.5T +100B anneal | Code cookbook; HQ anneal |
| synthetic | Demystifying Synthetic 2510.01631v1 | 100M–3B, ≤200B, English CC | Safe synth:real ratios by type |
| collapse | Model Collapse 2404.05090v1 | theory + 8×256 nanoGPT | Why a closed synth loop dies |
| midtrain-survey | Mid-Training Survey 2510.06826v1 | 17 frontier runs ledger | Taxonomy: anneal is 1–5% vs 9–51% |
| spark-joy | Spark Joy 2406.03476v1 | 7B, 1T, 50B–300B sweeps | Sub-10% anneal calibration + sans-math floor proof |
| pref-curriculum | Preference Curriculum 2501.13126v2 | 1.3B/3B, 100B/1T | Order is a domain re-timer; needs a floor |
| dataset-decomp | Dataset Decomposition 2405.13226v2 | 1B–7B, ≤1.1T, 64–8192 ctx | Long-context packing + ordering |

---

## The 7 assignment items, cross-referenced

### 1. Budget share for every capability lane (sum 100%)

| Paper | Verdict | Usable evidence |
|---|---|---|
| climb | **challenges hand-set, supports searching** | 112 proxy runs 60.41 vs RegMix 59.37 / DoReMi 59.16 / Random 57.93 (Table 1); 62M ≈ 350M |
| two-phase | silent on 7-lane cut | P1≈77% web-ish/20% code; P2≈54% web-ish/24% math/20% code |
| opencoder | **challenges** 24% | 90.9% code +7.7% code-web — a specialist |
| synthetic | silent | English CC only |
| collapse | silent | no lanes |
| midtrain-survey | **partially supports** | SmolLM2 anneal 58/24/14/4; Llama3 50/17/25/8; MAP-Neo 74.5/8.5/17; MiMo ~70% math+code; no 7-lane run exists; long-context never a lane % |
| spark-joy | **supports shape, challenges our 8% web** | Base 34.35/36.70/7.17/21.78 → DU 0/30/35/35; filtered web held at 30% (0.82×) to avoid shift. Our anneal 8% web is 0.24× — far more aggressive. Split web into raw vs filtered-HQ |
| pref-curriculum | **silent, mildly cautionary** | `∫α=1/n` fixes shares; no source % given beyond 500B zh/500B en. Lane shares and timing are separable |
| dataset-decomp | **challenges long-context share** | Natural web is 9.4% at 8192, 22.9% ≥4k; raising 8k from 9.4%→25% moved MDQA 21.9→22.1 (noise). 6% lane below natural supply; only additive if content differs |

**What the README can say:** no paper hands us 24/2/6/6/16/12/34. Two defensible moves: (a) declare shares and defend each against benchmark+supply, (b) commit to a CLIMB-style search at 1B/3B with each lane's benchmark in the objective. Prefer (b) as validation on top of (a).

### 2. Indic split across verified / unverified / translated / synthetic

All nine papers are **silent on Indic** — no Indic clustering, filtering, or eval. The only transferable constraint is on **D (synthetic)** from `synthetic`: rephrase ~30% (<50%), textbooks ≤3%.

Three named hazards:
- `synthetic` App D.2 + V4: Indic D + frozen English tokenizer ≈ 150× grad spike (uncovered unigrams spike loss).
- `two-phase`: English 5-bucket CC quality classifier — not a verified Indic rule.
- `opencoder`: scarce-language answer was manual Chinese domain annotation (SkyPile) — Indic scarcer, unstudied.
- `pref-curriculum`: low-PD text is *more* culturally dependent (0.69 vs 0.59) — a global PD sort would front-load native Indic and then starve it; PD ranking is dominated by weak-model PPL (Spearman 0.41 between PD variants), so a 100M model's PPL on Devanagari is a tokenizer artefact.
- `midtrain-survey`: MAP-Neo *cuts* Chinese 25%→8.5% entering mid-training — the one quantitative low-resource precedent goes opposite our 16%→28% raise. Only counter-precedent is Yi-Lightning ("emphasis on low-resource multilingual") with no %.

### 3. Agentic / reasoning / long-context as first-class slots

| Slot | Best support | Gap |
|---|---|---|
| Reasoning | `climb` MMLU slices; `two-phase` FLAN+CoT 1.3% of P2 → GSM8K +9.5; `opencoder` 12.44B algo in anneal; `midtrain-survey` 7 of last 9 models carry reasoning icon, Qwen3 5T & Pangu 3T reasoning phases | Never a large pretrain lane — always a small late slice |
| Agentic | **nothing at pretrain scale** — `opencoder` Package-Instruct 110k is API-freshness SFT, not trajectories | No paper trains agent trajectories at pretrain scale; `midtrain-survey` string `agent` occurs once (Agent-FLAN), Fig 1 legend has no agentic icon |
| Long-context | **supported as threshold, challenged as lane** — `dataset-decomp`: multi-doc QA ≈0 until pretrain length > eval context, then jumps and flats; natural web already 9.4% at 8192; `opencoder` random concat 4k/8k, file-level > repo-level; `midtrain-survey`: 11 of 17 runs have a dedicated long stage (0.14%–8.33%), mix 30–60% long, and it *follows* the anneal in 10 of 11 | No 32k training in `dataset-decomp` (max 8192); V5 6% unmeasured — 0% fails, ~9% saturates |

**What the README must own:** 6% long-context and "pack whole repos" are untested bets. Either cite Xiong et al. 2309.16039 for 32k or mark as explicit bet.

### 4. Protected always-on floor that OPUS cannot cross

| Paper | Verdict | Evidence |
|---|---|---|
| collapse | **supports real-data floor** | Same real N every generation bounds drift; 50% real flattens L1, **80% real erases drift** (Fig 5). Finite window only delays: mean T 17→95→216 for K=1→5→10 |
| spark-joy | **strongest floor proof** | 100B final phase sans-math: MMLU 29.71 (**-5.98 vs doing nothing**), Reading Comp 26.48 (**-10.54**), Core Avg 32.54 (-2.83). A final phase can *unlearn* below baseline |
| pref-curriculum | **supports need for floor, proves ordering alone starves** | Fig 6b: **ArXiv 88% low / 12% high, GitHub 66/34, Wikipedia 14/86**. A PD curriculum spends 88% of papers early and 86% of encyclopedias late while claiming "does not skew" — self-contradiction |
| climb | **supports spirit, challenges uniform 8%** | "Out-of-domain useful" — C8 0→0.13 for general reasoning; but sparse search drives code C20 → **0** when not in objective |
| synthetic | indirect | 100% synth worse or equal; 67% TXBK loses to CC |
| opencoder / midtrain-survey | continuity floor | Anneal retains **84% original dist** (OpenCoder) to avoid forgetting; survey: **60/40** (Zamba), **70/30** (Phi-4, Llama-3 probe), **84/16** still inside 10–40% overlay band |

**Sharpest sentence:** the floor must be a *real-token* floor in the selector's objective, and it must apply **in every bucket and every cycle** (DatasetDecomp's empty-bucket exclusion would otherwise drain scarce buckets after one cycle) and **in the anneal mix too**, not only the main run. "OPUS will figure it out" is refuted three ways.

### 5. Anneal reserve

All four non-collapse papers **support holding best data for the end**. They disagree on **how long** — the survey resolves it.

| Cluster | Run | Reserve as % of run | Mix overlay |
|---|---|---|---|
| **A terminal fast-decay** | MiniCPM 20B/1.02T **1.96%**, Hunyuan-A13B 300B/20.3T 1.48%, **OpenCoder 100B/2.6T 3.85%**, Pangu 0.4T/10T 4.00%, Hunyuan-Large 350B/7.36T 4.76% | New data 10–40% on old dist (OpenCoder 84/16, Zamba 60/40, Phi-4 70/30) |
| **B full second stage** | SmolLM2 1T/11T **9.03%**, Qwen3 5T/35.5T 14.08%, MiMo 16.67%, Zamba 51.28% | 5-stage curriculum machinery |
| MiniCPM WSD prescription | decay leg **~10%** | — |

Our **80B (4%) on 2T is Cluster A**, at the high end but inside the observed 1–5% band. Two-Phase's 40% is Cluster B — a different object, not comparable. Our staged Long-ctx→Anneal hop moves **32% of mass** — next to Zamba as most aggressive precedent (Spark Joy 41.1%), above OpenCoder's 16%.

Quality quantile: Hunyuan-Large anneals on **top 5% quality tokens** — 10× stricter than OPUS 40%. Reserve quantile should be much stricter than main-run acceptance.

DatasetDecomp challenges monotone reserve: `Grow-P2` 1 cycle → 8 cycles takes MDQA 25.9→28.0; design reserve **cyclically interleaved**, not as a single tail block, or RC/CSR lose.

### 6. Each lane tied to benchmarks it must win

- `climb` **strongly**: different objectives → different winners (Fig 5/7); objective writes the mixture.
- `midtrain-survey` **Table VI** is the ready map: code→ HumanEval/MBPP/MultiPL-E; reasoning→ GSM8K/MATH/GPQA/BBH; long→ LongBench/RULER; **Indic→ MGSM 8-shot CoT, Flores-101** (only multilingual hook); general→ MMLU/MMLU-Pro/ARC/HellaSwag.
- `opencoder` code only (HE/MBPP/BigCodeBench/LiveCodeBench/MultiPL-E/McEval/MdEval); `spark-joy` math→MMLU/GSM8K, code→HumanEval, web→ Language Understanding (negative at every length); `pref-curriculum` encyclopedic→ MMLU-family (+8.1 from chance), commonsense flat.
- `synthetic` challenges method: whole surface is English CE loss ("loss is not our final goal").

**If objective is only MMLU-ish, search starves agentic and Indic.** Name a head per lane.

### 7. Demand vs unique supply

**Organic repeat bounded:** `two-phase` 6 epochs HQ / 8 math then hurts; `opencoder` ~3.5 epochs on 2.5T; `midtrain-survey` "a few times, diminishing returns." Our 6× effective and 1.2× on Indic/reason/long inside band. `Zamba` most datasets 1 epoch, select HQ 2 epochs — same.

**Synthesis much smaller than need:** `opencoder` 3.62% of anneal; `two-phase` synthetic GSM8K inside 1.3% task slice; `synthetic` rephrase ~30% ceiling, textbooks ≤3%, pools capped 100B; `collapse` synth logarithmic in real.

**Reframing from `dataset-decomp`:** long-context supply is not a separate corpus — it is a packing property. Natural D13 alone is **~423B** genuine 8k-contiguous tokens at zero cost vs our 0.1T inventory. Converts long-context from scarcity to data-prep decision (web 8k spans ≠ curated multi-doc reasoning, so 0.1T retains distinct job).

**Agentic is the crisis:** 2% of 2T = **40B vs 0.63B = ~63×**. Not repetition, not rephrase (no source doc), textbook-class → collapse-patterned and absorbing. FIM (DeepSeek-V3, only surveyed run using it in mid-training) is the one mechanism offered as a per-sample multiplier for scarce late-stage data.

Three honest options: (1) cut to ~0.15–0.2% (3.5 epochs of unique), move capability to SFT/RL; (2) keep 2% with environment-grounded, verifier-filtered rollouts from a frozen stronger teacher + real-token floor every batch; (3) declare as bet gated on 1B/3B agentic proxy. **Option 2+3 is strongest.**

---

## Cross-paper contradictions

1. **Anneal length: Cluster A 1–5% vs Cluster B 9–51%.** Different objects — fast decay vs second stage. Our 4% is A.
2. **Sparse vs floors: CLIMB zeroes lanes; V5 wants floors.** Put lane in objective or hard-constrain. Say which.
3. **Synthetic efficient (30% rephrase, 5–10×) vs collapses (a.s.).** Resolve by type and loop: n=1 rephrase mixed with real every step ≠ recursive self-training.
4. **Repo vs file code.** OpenCoder file-level wins; Zamba hybrid SSM and Granite MoE are third positions.
5. **Quality gates: aggressive (zero Low, +13.2) vs diversity (stars≥5 hurts).** Content-quality gates help, popularity proxies hurt. Never star-filter scarce lanes.
6. **mixture_shift vs stability:** `spark-joy` hard 34pp switch silent on grads; V4 150× spike, `dataset-decomp` short-first suppresses spikes — ramp, don't step.

## Where all nine are silent

Indic tiering beyond synthetic ceilings. Agentic trajectories at pretrain scale (only map is Agent-FLAN). Long-context beyond 8k (max trained 8192). OPUS per-iteration selection (CLIMB searches static weights; PrefCurriculum is static schedule — opposite axis). Repetition accounting for scarce lanes (only Zamba "1 epoch, HQ 2 epochs" and survey comment). Error bars — `climb` Q7=No, `spark-joy` n=1, `pref-curriculum` 1 seed, `dataset-decomp` single-seed except §3.2, `synthetic` no bars.
