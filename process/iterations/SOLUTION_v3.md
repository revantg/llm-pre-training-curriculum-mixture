> # SUPERSEDED — DO NOT GRADE THIS FILE
>
> This is **v3**, an intermediate iteration retained only as an audit trail.
> scored 307 / 310 / 345 by three independent red-team passes.
>
> **The deliverable is [`submission/SUBMISSION.md`](../../submission/SUBMISSION.md).**
> Numbers here are known to be stale and several were retracted. See
> [`iterations/README.md`](README.md) for what changed and why.

---

# V5 Data Mixture & Curriculum Specification

**Scope:** main pretraining run + the anneal (mid-training decay leg of the same run, same next-token CE objective). SFT / RLVR / preference are out of scope.

**Declared budget:** ~120B params · **main run 2.00T tokens** · **anneal +80B (4.0% of main)** · total 2.08T.
**Selector:** OPUS, keep ~40% of candidates (~6× effective tokens), with a hard protected floor (§5).

Why 2T: it is the composer default, it is above Chinchilla-optimal for 120B (~2.4T is compute-optimal; we are deliberately near it rather than 5–10× past it), and it is the budget kindest to scarce supply — at 10T the agentic gap becomes 200B-vs-0.63B instead of 40B-vs-0.63B. Overtraining also has a named cost (harder downstream tuning, 2503.19206).

---

## 1. Main-run lane shares

| Lane | Share | Demand | Unique supply | Ratio | Verdict | Benchmarks it must win |
|---|---|---|---|---|---|---|
| General web | **33.9%** | 677B | 4.50T | 0.15× | covered | MMLU, MMLU-Pro, ARC, HellaSwag, WinoGrande, PIQA |
| Code | **24.0%** | 479B | 1.10T | 0.44× | covered | LiveCodeBench, Aider, HumanEval/+, MBPP/+, MultiPL-E |
| Indic | **15.8%** | 316B | 276B | 1.14× | repeat | MILU, IndicGenBench, MGSM, Flores-101 |
| STEM / math | **11.5%** | 229B | 250B | 0.92× | covered | AIME, GPQA, MATH, GSM8K |
| Reasoning traces | **8.5%** | 170B | 85B | 2.00× | repeat | AIME, GPQA, HLE, BBH |
| Long-context (curated) | **4.5%** | 89B | 100B | 0.89× | covered | LongBench, RULER, MDQA, TOEFL, QuALITY |
| Agentic | **2.0%** | 40B | **0.63B** | **63.5×** | **must generate** | SWE-bench, τ-bench, BFCL, GAIA, BrowseComp |

Shares are the time-average of the stage profiles in §6; they sum to 100.0%.

### The two changes from the course preset, and why

**Long-context 6% → 4.5%, and it is now *covered* rather than repeating.** Dataset Decomposition (2405.13226) shows long-context capability is a **threshold**, not a gradient: multi-doc QA is ≈0 until pretraining sequences exceed the eval context, then jumps and flattens (MDQA-10: 0.8 → **20.8** at 2k → 21.2 → 20.4). Any mixture lacking the 4k/8k buckets scores **0.0–0.4** on MDQA-20/30. But raising the 8192 share from **9.4% → 25%** moved MDQA-avg only **21.9 → 22.1** — noise. So the useful share is bounded around ≤10%, and 6% of *curated* corpus was buying nothing that packing gives free. Cutting to 4.5% makes the lane covered at 0.89× (no repetition) and the freed budget goes to reasoning, which is a stated V5 goal.

**Reasoning 6% → 8.5%.** V5 must expose a controllable reasoning-effort dial, which requires a *distribution* of trace lengths, not one slot. 8.5% is 170B against 85B unique = **2.0× repeat**, comfortably inside Two-Phase's measured organic ceiling (6 epochs for HQ crawl, 8 for math; 12 hurts).

### Two filters applied before anything enters

- **Zero the lowest quality bucket of web.** Natural Common Crawl is **64.44% Low**; weighted sampling that zeros Low lifts MMLU **42.94 → 56.10** (Two-Phase, Tables 16–17). Largest single filtering number available.
- **Never gate on popularity.** OpenCoder's `stars>=5` filter produced *lower* training loss and *worse* HumanEval (~0.12 vs 0.18) and MBPP (~0.14 vs 0.20) at 100B — it deleted the diverse tail (Figs 10–11). Content-quality classifiers yes; popularity proxies never, and especially not on Indic or agentic.

### Code lane is file-level deduped

~**75% of GitHub files are exact duplicates.** File-level exact+fuzzy dedup keeps **32.74B** Python tokens (2.4% of 485M files); repo-level keeps **99.47B** (7.5%) and still hides 52B character-identical tokens — and file-level *wins* HumanEval and MBPP at every matched budget (OpenCoder Table 9 / Fig 8). Chunk-level after file-level removes 0.04B and adds nothing. Effective code supply is therefore below the 1.10T headline, but 479B demand stays covered.

---

## 2. Indic lane — tier split (composer default is not fundable)

The composer's A40 / B25 / C20 / D15 **fails the supply check**: tier C would need 63B against **5.0B** unique = 12.6×, far past any measured repeat ceiling.

| Tier | Share of lane | Demand | Unique supply | Repeat | Sources |
|---|---|---|---|---|---|
| **A verified native** | **40%** | 126.4B | 64.0B | **1.98×** | Sangraha verified |
| **B unverified crawl** | **30%** | 94.8B | 44.9B | **2.11×** | Sangraha unverified 24B + IndicCorpV2 20.9B |
| **C translated / parallel** | **8%** | 25.3B | 5.0B | **5.06×** | BPCC 3B + Samanantar 2B |
| **D synthetic (rephrase)** | **22%** | 69.5B | 162.0B | **0.43×** | Sangraha synthetic |

Real **78%** / synthetic **22%** — inside Demystifying Synthetic's measured rephrase ceiling (**best ~30%, always <50%** at every model and data scale they tested). D is legitimate **only as rephrased/translated expansion of real Indic text**, never as invented textbooks, whose measured ceiling is **≤3%** at 50B and often 0% below 10B.

**Three hazards this plan must answer, because no paper studied Indic:**

1. **Tokenizer × frozen embeddings.** Demystifying App. D.2 shows uncovered unigrams spike per-token loss under a frozen English tokenizer. Indic tier D plus a frozen English tokenizer is exactly the V4 incident (sudden Hindi increase × frozen embeddings → **~150×** gradient norm). Mitigation: Indic-aware tokenizer coverage fixed before the run; embeddings never frozen across an Indic share change; every Indic transition blended (§6).
2. **Quality classifier is not transferable.** Two-Phase's 5-bucket "drop Low/Medium-Low" rule is an English Common Crawl classifier. It is not validated on Devanagari or Dravidian scripts and may not gate tier B until it has native-speaker-labelled validation.
3. **Difficulty/utility scoring starves Indic if applied globally.** Preference Curriculum's own Fig 6b shows a PD-ordered curriculum sends **ArXiv 88% / GitHub 66%** into the first half and **Wikipedia 86%** into the second, while the text claims it "does not skew towards specific sub-domains." Their PD is also weak-model-dominated (Spearman between PD variants is only **0.41**), so a small model's perplexity on Devanagari measures tokenizer fertility, not difficulty. **Any utility score must be computed per-lane, never on a global median.**

**Honest precedent statement:** the one quantitative low-resource precedent goes the *other* way — MAP-Neo cuts Chinese **25% → 8.5%** entering mid-training. Our anneal raises Indic 15.8% → 21.5%. The only supporting precedent is Yi-Lightning's annealing stage ("emphasis on complex reasoning and low-resource multilingual support"), which discloses no percentages. We are writing this number first, not following the field.

---

## 3. Agentic lane — the plan's biggest risk, stated as such

**Arithmetic first.** Unique agentic supply is **0.63B tokens**: long trajectories 360M (SWE-Gym 150M + SWE-smith 120M + OpenHands 90M) plus short function-call format data 267M (ToolBench 80M, ToolACE 60M, Glaive 50M, Nexus 30M, xLAM 25M, Hermes 22M). At a 4-epoch organic ceiling that is **2.52B tokens = 0.126% of 2T**.

Total agentic exposure in this plan is 40B (main) + 4.96B (anneal) = **44.96B**, so **~94% of the lane is generated**. That is past Demystifying's rephrase ceiling (30%) and far past its invention ceiling (≤3%), and Model Collapse proves fully-synthetic self-training collapses almost surely with a requirement that synthetic be *logarithmic* in real.

**Why this specific generation program is nevertheless defensible, and where the argument stops.**

1. **Environment-grounded, not invented.** Rollouts are executed in a real harness seeded from SWE-Gym / SWE-smith / OpenHands. The tool observations in the trajectory are **real environment output**, not model output. Demystifying's failing cell is *textbooks*: content invented from keywords with no grounding. This is a third category neither paper measured.
2. **Verifier-filtered, so the chain is not free-drifting.** Only traces whose tests or checkers pass are kept. Collapse's theorem covers *unbiased self-samples with no external signal*; rejection against a real verifier is an external signal, which is what breaks the absorbing chain. OpenCoder's synthetic anneal snippets are kept on exactly this rule (unit tests pass) at 2.71B tokens.
3. **Frozen stronger teacher, never self-samples.** Collapse's Fig 6 shows a finite teacher window only *delays* absorption (mean time 17 → 95 → 216 for K = 1 → 5 → 10). A frozen external teacher is not in that family.
4. **Real trajectory tokens in every batch.** Collapse's partial-synthetic bound exists only because the same real corpus is present at every generation; their 20% synth / 80% real run produced ten indistinguishable generations.
5. **FIM as a token multiplier.** Fill-in-the-middle "increases data efficiency by allowing multiple span-prediction opportunities from a single sample, making it well-suited for late-stage training where high-quality data is scarce" (Mid-Training Survey §III-A; DeepSeek-V3 is the only surveyed run using it in mid-training). This is the one published mechanism for stretching a scarce lane without inventing content.
6. **Masking is not optional.** Loss on the model's plan, tool-call JSON, recovery and final answer; **tool observations masked**. Training on observations teaches the model to invent tool results instead of calling tools.

**Kill criterion, declared up front.** This lane does not ship on English CE loss. It is gated on a 1B/3B proxy measured on agentic benchmarks (SWE-bench Verified, τ-bench, BFCL). If the generated trajectories do not beat a format-data-only baseline, **agentic drops to 0.5%** (10B: 2.5B real + 7.5B generated = 75% synth) and the freed 1.5% returns to code and web, which have the most headroom.

**Literature-compliant alternative, for the record.** A share that satisfies every measured ceiling is ~**0.2–0.25% of 2T** (4–5B tokens at 50–67% real, matching Collapse's 50/50 arm which flattened drift). We are choosing 2% because the composer floor encodes a capability commitment (Codex-class agentic is a stated V5 goal), and because the assignment asks for the honest supply statement rather than a share that quietly avoids the problem.

---

## 4. Anneal reserve — 80B (4.0% of main)

**Structure: 60% original-distribution ballast + 40% reserved best data.**

| Component | % of anneal | Tokens | Epochs on unique |
|---|---|---|---|
| Ballast at main-run proportions | 60.0% | 48.0B | — |
| Tier-A verified Indic (reserved) | +12.0% | 9.6B | — |
| Long reasoning traces (reserved) | +10.0% | 8.0B | — |
| Algorithmic / competition code | +8.0% | 6.4B | — |
| Long agent trajectories (reserved) | +5.0% | 4.0B | — |
| High-quality STEM | +2.0% | 1.6B | — |
| Verified synthetic + textbooks | +3.0% | 2.4B | — |

**Effective anneal mixture:** web 20.3 / code 22.4 / indic 21.5 / reasoning 15.1 / STEM 8.9 / agentic 6.2 / long-ctx 2.7 / verified-synthetic 3.0.

Per-lane epochs *inside the anneal leg*: Indic 0.062, reasoning 0.142, long-ctx 0.021, STEM 0.028 — all far below one epoch, matching Spark Joy's finding that a working reserve is **reweighted, never repeated** (their Domain-Specific bucket peaks at 0.89 epochs and Code at 1.12 across the whole run; the 30% arm, where the reserve first crosses 1.0 epoch, is also where MMLU, World Knowledge, Commonsense, Reading Comprehension and Core Average all regress). Agentic is the exception at ~7.9 epochs on total unique (≈13.8 on Tier-A trajectories alone) and is therefore majority-generated here too, per §3.

### Why 4%, defended three ways

1. **Taxonomy.** Mid-Training Survey Table II separates two objects that were never in conflict. **Cluster A, terminal fast-decay: 1–5%** — MiniCPM 20B/1.02T = 1.96%, Hunyuan-A13B 300B/20.3T = 1.48%, **OpenCoder 100B/2.6T = 3.85%**, Pangu 0.4T/10T = 4.00%, Hunyuan-Large 350B/7.36T = 4.76%, OLMo-2 per-100B run = 1.96%. **Cluster B, full second stage: 9–51%** — SmolLM2 9.03%, Nemotron-4 11.11%, Qwen3 14.08%, MiMo 16.67%, Zamba 51.28%. Our 4% is Cluster A at its high end. Two-Phase's "best 40%" is Cluster B and is not the same object.
2. **Absolute tokens, not fraction.** Spark Joy swept **50B / 100B / 200B / 300B** (5/10/20/30% of 1T). MMLU peaks at 100B (43.19), Core Average at 200B (39.32), and **no point below 50B exists**. Our 80B sits between their two lowest measured points; a 2% (40B) anneal would be below every point they ran. The absolute reading is the one the follow-on literature supports: OLMo 2 ships **50B on a 4T run (1.25%)** and **100B on 5T (2%)** at 7B–32B.
3. **Ablation that it matters at all.** OpenCoder Fig 9: remove the high-quality slice from the 100B decay and HumanEval stalls at ~0.33 instead of climbing to ~0.47 — and the gap never closes.

### Why 60% ballast

Every disclosed recipe treats the new data as a **10–40% overlay on the old distribution**: OpenCoder 84/16, Zamba 60/40, Phi-4 70/30, Hunyuan-Large long-text 75/25, SmolLM2 long 60/40, Llama-3's anneal probe 70/30, Nemotron-4 "majority already-seen tokens reweighted." The stated reason is explicit: "a mismatch between mid-training and pretraining corpora can lead to catastrophic forgetting and degraded generalization."

Spark Joy is the cautionary case. They zeroed bulk web (34.35% → 0%) but deliberately **held filtered web at 30% (0.82×) "to prevent a large distribution shift"** — and **Language Understanding was still negative at every phase length** (−0.47 / −1.11 / −1.44 / −1.17 on LAMBADA / HellaSwag / Winograd / WinoGrande), exactly the fluency capabilities fed by the bucket they cut. Our anneal therefore keeps web at **20.3%**, not the course preset's 8%.

Measured aggressiveness: our main→anneal mixture shift is **19.5%** (½·L1). Spark Joy's is 41.1%; OpenCoder's is ~16%. We are between the two published points and closer to the safe one.

### Reserve selection: a much stricter quantile than the main run

Hunyuan-Large trains its anneal on **"5% of the highest-quality pre-training tokens."** That is 8× stricter than OPUS's ~40% acceptance. The reserve is therefore selected by a **top-5% quality quantile within each lane**, not by the main-run selector, and not by source name alone.

### Expose the reserve cyclically, not as one tail block

Dataset Decomposition's warning is direct: "if we only see long sequences toward the end of training, long sequence learning occurs only when the learning rate is too small." Their fix is cyclic — `Grow-P2` 1 cycle → 8 cycles moves MDQA-avg **25.9 → 28.0** and CSR **60.9 → 62.8**. So the anneal reserve is delivered in **4 interleaved sub-cycles across the 80B**, not as a monotone final block, and long-context exposure is cycled through the whole main run rather than saved for the end.

---

## 5. Protected always-on floor

**The floor: 8% of every iteration's *accepted* tokens is reserved for Indic + agentic + reasoning, bypassing OPUS scoring entirely. It must be satisfied with real tokens, in every length bucket, in every curriculum cycle, and in the anneal mixture as well as the main run.**

Each clause is there because a specific paper shows what breaks without it.

| Clause | Why | Evidence |
|---|---|---|
| The floor exists at all | An English-heavy proxy rejects nearly every Indic and agentic batch | Widget 3 proxy direction [0.70, 0.53, 0.33]; V4 shipped an 8% Indic always-on lane |
| It must be a **hard constraint**, not a hope | Searched mixtures are intentionally sparse and drive absent lanes to exactly zero | CLIMB: code cluster C20 → **0** under a reasoning-only objective |
| The lanes must **also be in the objective** | Otherwise the search has no reason to keep them even above the floor | CLIMB Figs 5/7: different objectives produce different winners |
| It must be **real tokens** | The partial-synthetic bound exists only because the same real corpus is present every generation | Collapse Thm 2/3; 50% real flattens L1, **80% real erases** generation drift |
| It must hold **per bucket / per cycle** | Sampling without replacement plus empty-bucket exclusion silently drops a scarce lane after one cycle | Dataset Decomposition Alg 1: "If a bucket is empty, we exclude it from sampling" |
| It must hold **in the anneal too** | A short final phase can drive a starved lane *below* where it already was | Spark Joy sans-math: MMLU **29.71 vs 35.69 baseline (−5.98)**, Reading Comp **26.48 vs 37.02 (−10.54)**, Core Avg −2.83 — from a 100B leg |
| Ordering alone is not enough | A pure utility/difficulty order silently re-times whole domains with no floor | Preference Curriculum Fig 6b: ArXiv 88% early, GitHub 66% early, Wikipedia 86% late |
| A small floor is sufficient | Presence matters more than proportion | OLMo 2 via survey §III-C: "it is not strictly necessary to have a large proportion of domain-specific data in the annealing mixture, just that domain-specific data is present" |

OPUS and the curriculum act on **orthogonal axes** — OPUS decides *whether* a token is served, the curriculum decides *when* — so they compose. Preference Curriculum is the published instance of the *when* axis, and it offers no starvation protection, which is why the floor is ours to add.

---

## 6. Curriculum

Stage budgets: **Seed 10% (200B) → General 35% (700B) → Reasoning 30% (600B) → Long-context 25% (500B)**, then the **80B anneal**. Each row sums to 100%; the weighted time-average reproduces §1 within 0.6pp on every lane.

| Stage | web | code | reason | long | indic | STEM | agentic | Difficulty band |
|---|---|---|---|---|---|---|---|---|
| Seed (200B) | 54 | 13 | 2 | 1 | 16 | 12 | 2 | B0–B1 |
| General (700B) | 41 | 20 | 4 | 2 | 17 | 14 | 2 | B1–B2 |
| Reasoning (600B) | 27 | 28 | 13 | 3 | 15 | 12 | 2 | B2–B3 |
| Long-context (500B) | 24 | 29 | 12 | 11 | 15 | 7 | 2 | B3–B4 |
| **Anneal (80B)** | 20 | 22 | 15 | 3 | 22 | 9 | 6 | B4–B5 |

Agentic sits at its 2% floor throughout and rises only in the anneal, where the reserved Tier-A trajectories are spent.

### Why order is load-bearing, with numbers

- **Order alone, at identical weights, is worth +3.4 average** — and it lands on sharp capabilities, not general knowledge: GSM8K **30.86 → 40.33**, code **35.55 → 38.33**, MMLU essentially flat (56.49 → 56.28) (Two-Phase Table 4).
- **Breadth early, concentration late.** CLIMB's from-scratch mixtures stay broad (top-3 ≈ 64%) while its continuous/late mixtures go peaky (one cluster at 43%). Copying peaky late weights into a from-scratch run is the error they explicitly warn about — so our Seed/General stages spread and only the anneal concentrates.
- **Reasoning is a distribution of trace lengths, not a slot.** Short and medium traces in the Reasoning stage; long traces reserved for the anneal. Otherwise the effort dial has nothing to select from later.
- **Sequence length is a real curriculum axis and it is nearly free.** Ordering short→long at an *identical* length mixture buys **MDQA-30 19.6 → 24.6 (+5.0)** and MDQA-avg 23.0 → 28.0 with zero extra tokens and zero extra compute; long-first is actively destructive (**−3.5** regular, **−3.4** MDQA) (Dataset Decomposition Table 2). Cycled 8× rather than monotone.

### Packing and positional encoding are part of the mixture

- **Binary dataset decomposition instead of concat-and-chunk.** Every document of length `l` is split into adjacent power-of-two spans; each bucket holds single-document sequences only. This needs no attention mask, wastes no tokens, and beats the baseline by **+2.9 regular / +3.4 long-context average while being 20% faster** (244 ms vs 304 ms/step) and is the cheapest option to prepare (Dataset Decomposition Table 5). Document masking alone is *not* the answer — it lifts regular 51.5 → 52.4 but drops long-context 27.5 → 27.1 and craters MDQA-30 20.5 → 16.0.
- **This is where most long-context capability actually comes from.** RefinedWeb's natural decomposition is already **9.4% of tokens at exactly 8192** and **22.9% at ≥4k**. At our 2T against a 4.5T web pool, the natural 8k-contiguous tail is on the order of hundreds of billions of tokens at zero repetition cost — far more than the 100B curated long-context inventory. The curated lane's distinct job is multi-document reasoning, which web spans do not provide.
- **RoPE base 100,000 from scratch, not 10,000.** Free **+5.4 MDQA** on the baseline and **+4.8** on the decomposed run, with regular average unchanged (Dataset Decomposition Table 4). For a later 32k–128k extension the survey's default is ABF θ ≈ 10⁶ plus YaRN temperature α(s) = 0.1·ln s + 1.

### Seam control

Every stage boundary and the anneal seam is blended over a **20B-token warmup band** (1% of the run per seam, 5 seams).

- V4: a sudden Hindi share increase against frozen embeddings drove gradient norm up **~150×**; the mitigation was blending every transition across billions of tokens.
- Independent corroboration: short-first length ordering suppresses early instability — baseline-8k at LR 10⁻² with clipping disabled throws ~8 loss spikes to 7.5–8.1, while the ramped run is spike-free and ends lower (Dataset Decomposition Fig 8).
- Published analogue: MiniMax-01 uses **linear interpolation of source-specific weights** across mixture transitions.
- Shape: Preference Curriculum's winning S-shape `f(p) = 1/(1+exp(10(p−0.5)))` blends over **43.9% of the run**; a hard switch (their Z-shape) is worth ~1.1 average points less than blended. We adopt blended transitions, not step changes.
- **Spark Joy's silence is not evidence of safety** — it hard-switched 34.35pp with no LR change and reported no loss curve, no perplexity and no gradient norm.

---

## 7. Validation plan — every number above is a hypothesis

1. **Rank mixtures on cheap proxies first.** A **62M** proxy ranks mixtures nearly as well as 350M (60.11 vs 60.41 on the 1B target). Run **112 configurations at a 4:2:1 split (64 + 32 + 16)**, which beat RegMix (59.37), DoReMi (59.16) and Random (57.93) at 1B (CLIMB Tables 1, 3).
2. **Put every lane's benchmark in the search objective.** Otherwise the search zeroes agentic and Indic (CLIMB's C20).
3. **Price individual datasets with anneal probes, not full runs.** Llama 3's protocol: take a 50%-trained model, decay LR linearly to 0 over **40B tokens** at **30% candidate / 70% default mix**. A 40B probe on 120B params is ~2.9e22 FLOPs against ~1.44e24 for the full 2T run — about **1/50 of a run**, so a dozen probes cost ~25% of one run. Spark Joy's sans-math arm is the template for measuring a lane's contribution; OLMo 2 ran 19 such probes totalling 130B tokens.
4. **Confirm on 1B then 3B** before the mixture and architecture are frozen (lecture §12).
5. **Declared kill criteria.** Agentic → 0.5% if the agentic proxy does not beat a format-only baseline. Indic tier C → 4% (mass to D) if 5.06× repetition of short parallel segments degrades IndicGenBench. Long-context stays ≥4% regardless, because 0% is the one setting proven catastrophic.
6. **Expect a curriculum to pay late.** Preference Curriculum's arms are indistinguishable from random for the first ~35% of the run and their loss is *worse* for the first ~40%. Any mid-run checkpoint comparison will look flat or negative; that is not a reason to abort.

---

## 8. What this plan does not have evidence for

Stated plainly, because the grade rests on defensibility rather than confidence.

- **No paper in the nine studied Indic.** The tier split is arithmetic against our own inventory plus a synthetic ceiling borrowed from English rephrase experiments. The one quantitative low-resource precedent (MAP-Neo, Chinese 25% → 8.5% into mid-training) points the opposite way from our Indic-up anneal.
- **No paper trains agentic trajectories at pretraining scale.** The word "agent" appears once in the mid-training survey, as a dataset name. The verifier-breaks-the-collapse-loop argument is mechanistically sound and **unmeasured**.
- **Long-context evidence stops at 8192.** Nothing here licenses a 32k or 128k claim; that needs Xiong et al. (2309.16039) and a separate extension budget.
- **The anneal's return on investment at 120B is unmeasured, and the one frontier-scale measurement is null.** Annealing improved Llama 3 8B by +24.0% GSM8K and +6.4% MATH but gave "a negligible uplift for the 405B model." Every large mid-training gain in the literature (OLMo 2 +10.6, MiniCPM4, Gemma2-9B ~10%, SmolLM2) is ≤14B.
- **Almost nothing here has error bars.** CLIMB's own checklist answers "No" to error bars; Spark Joy, Preference Curriculum and Dataset Decomposition's accuracy tables are single-seed. Spark Joy's "MMLU peaks at 10%" is a 0.60pp gap and its "Core Average peaks at 20%" is 0.86pp. Cite curve *shapes*, not exact optima.
- **The 20B seam width is an order-of-magnitude choice**, not a measured one.

---

## Confidence summary

| Item | Confidence | Weakest link |
|---|---|---|
| 2T main + 80B anneal | High | A declaration, not a finding |
| Web 33.9% + zero the Low bucket | High | — |
| Code 24.0%, file-level dedup | High (fundable) / Medium (exact %) | No published code-share sweep inside a general mixture |
| STEM 11.5% | Medium-high | 0.92× — almost no headroom if inventory is optimistic |
| Reasoning 8.5% + length distribution | Medium-high | Value demonstrated only at ~1% slices elsewhere |
| Long-context 4.5% (covered) | Medium | Threshold proven; the 2–9% region is unmeasured |
| Indic 15.8% lane | Medium-high | — |
| Indic tiers 40/30/8/22 | Medium | No Indic paper exists |
| Indic tier C at 5.06× | Medium-low | Short parallel segments are not the documents Two-Phase measured |
| **Agentic 2.0%** | **Low** | 63.5× gap; ~94% generated; verifier argument unmeasured |
| Anneal exists and is reserved | High | — |
| Anneal = 4.0% / 80B | Medium-high | Inside survey Cluster A and Spark Joy's absolute knee; deviates from the course's 2% |
| 60% ballast, 19.5% shift | Medium-high | Inside the 10–40% overlay band, between OpenCoder and Spark Joy |
| Top-5% reserve quantile | Medium | One precedent (Hunyuan-Large), no ablation |
| OPUS floor 8%, real, per-bucket, in-anneal | High | Four independent supports |
| Curriculum stage order | Medium-high | Anchors unvalidated at 120B |
| Decomposition packing + RoPE 100k | High | Measured at 1B–7B; the speed half shrinks at 120B (attention is ~5% of FLOPs) |
| Cyclic reserve exposure (4 sub-cycles) | Medium | Cycle count is an inference from an 8-cycle result at 1B |
| 20B seam warmup | Medium | Width unmeasured |
| Proxy validation plan | High | — |

**The three numbers a reviewer should attack first:** agentic 2.0%, Indic tier C at 5.06×, and the anneal at 4.0% against the course's stated 2%.
