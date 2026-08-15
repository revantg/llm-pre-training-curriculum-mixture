> # SUPERSEDED — DO NOT GRADE THIS FILE
>
> This is **v4**, an intermediate iteration retained only as an audit trail.
> closed the v3 FATALs; **still contains the retracted 0.83x Chinchilla folklore**.
>
> **The deliverable is [`submission/SUBMISSION.md`](../../submission/SUBMISSION.md).**
> Numbers here are known to be stale and several were retracted. See
> [`iterations/README.md`](README.md) for what changed and why.

---

# V5 Data Mixture and Curriculum Specification

**Scope.** The main pretraining run and the anneal — the decay leg of the same run, same next-token CE objective. SFT, RLVR and preference training are out of scope.

**Budget.** ~120B parameters · main run **2.000T** tokens · anneal **+80B** · total **2.080T**.
**Selector.** OPUS, keep ~40% of candidates (~6× effective tokens), with the per-lane floor fixed in §5.

Why 2.000T: Chinchilla-optimal for 120B is ≈2.4T, so this is **0.83× compute-optimal** on unique tokens — deliberately *not* an overtrained run. With OPUS's ~6× effective multiplier the model sees ~12T effective tokens, which *is* ~5× past optimal; that is a selection-efficiency claim, not a unique-token claim, and the two must not be conflated. 2T is also the budget kindest to scarce supply: at 10T the agentic gap widens from 40B-vs-0.627B to 200B-vs-0.627B.

---

## 1. Main-run lane shares

Shares are the **exact** time-average of the stage profiles in §6 and sum to 100.00.

| Lane | Share | Demand | Unique supply | Pre-selector | Post-selector (40%) | Verdict |
|---|---|---|---|---|---|---|
| General web | **33.85%** | 677.0B | 4.500T | 0.15× | 0.38× | covered |
| Code | **23.95%** | 479.0B | 1.100T → **362B** effective | 0.44× → **1.32×** | 3.31× | **repeat** |
| Indic | **15.80%** | 316.0B | 276.0B | 1.14× | 2.86× | repeat |
| STEM / math | **11.45%** | 229.0B | 250.0B | 0.92× | 2.29× | repeat |
| Reasoning | **8.50%** | 170.0B | 85.1B | 2.00× | 4.99× | repeat |
| Long-context (curated) | **4.45%** | 89.0B | 100.0B | 0.89× | 2.23× | repeat |
| Agentic | **2.00%** | 40.0B | **0.627B** | **63.8×** | 159.5× | **must generate** |

**Two accounting disclosures a reviewer will otherwise find first.**

*Selector-adjusted supply.* OPUS accepts ~40% of what it is offered, so a pre-selector ratio understates repetition. At 40% acceptance **code, STEM and long-context all move from covered to repeat**, and reasoning reaches 4.99× — effectively Two-Phase's measured 6-epoch ceiling with no headroom. The counter-argument is real and we rely on it: a *rejected* token is not consumed, so it returns to the candidate pool at a later iteration under a different model state. Unique supply is therefore not destroyed at 40%, and the pre-selector column is the correct one for supply *existence*. The post-selector column is the correct one for **schedule risk**, and we plan against both.

*Code supply is smaller than the headline.* At OpenCoder's own file-level retention ratio (32.74B / 99.47B = 32.9%) the 1.100T code pool delivers ≈**362B** unique tokens, so 479B of demand is **1.32× repeat**, not covered. We accept file-level dedup anyway: it wins HumanEval and MBPP at every matched budget (OpenCoder Fig 8, Table 9) and repo-level's extra 67B contains 52B of character-identical text.

**Filters applied before any lane enters.** Natural Common Crawl is **64.44% Low** quality; a weighted scheme that zeroes Low and upsamples High lifts MMLU **42.94 → 56.10** (Two-Phase Tables 16–17). The same ablation costs code **19.25 → 17.41**, so the filter is applied to the web lane only, not to code. Popularity is never a gate: OpenCoder's `stars>=5` filter produced *lower* training loss and *worse* HumanEval (~0.12 vs 0.18) and MBPP (~0.14 vs 0.20) at 100B (Figs 10–11).

### 1.1 Why reasoning is 8.5% and what actually fills it

The course preset is 6%. Widget 1 sets `WEIGHTED_MIN = 8` — *"a lane needs at least this share to move its benchmarks."* At 6% the reasoning lane is **starved by the course's own rule** while being asked to win AIME, GPQA, HLE and BBH. 8.5% is the smallest share that clears the funding line. That is an arithmetic forcing, not a preference.

The lane is **not** homogeneous, and the inventory says so:

| Component | Inventory datasets | Unique | Allocation | Epochs |
|---|---|---|---|---|
| Trace-shaped | OpenThoughts2 **3B**, OpenMathReasoning **2B**, OpenR1-Math **1.6B**, NuminaMath **0.5B** | **7.1B** | 28.4B | **4.00** |
| Academic reasoning text | AON / D5 Academic-Reasoning-Overflow (V4 corpus) | **78B** | 141.6B | **1.82** |

**The trace-shaped pool is 7.1B, not 85B**, and the long-CoT portion is **4.6B**. Any claim about a reasoning-length distribution must be sized against 7.1B. The 2.00× lane headline is true only because 92% of the lane is AON academic text, which is real reasoning-adjacent prose but is **not** chain-of-thought. We state this rather than let the lane's comfortable ratio hide it.

### 1.2 Long-context: the lane share is not the funding number

Long-context at 4.45% is **below `WEIGHTED_MIN = 8`**, and a reviewer will open the composer and say so. The answer is that long-context capability is not bought by a lane; it is bought by a **packing policy applied to every lane**.

Dataset Decomposition measures the capability as a **threshold**: multi-document QA is ≈0 until pretraining sequences exceed the eval context, then jumps and flattens (MDQA-10 `0.8 → 20.8` at 2k, then 21.2, 20.4). Any mixture lacking the 4k/8k buckets scores **0.0–0.4** on MDQA-20/30. And RefinedWeb's *natural* decomposition is already **9.4%** of tokens at exactly 8192 and **22.9%** at ≥4k.

Effective exposure under our mixture, with binary decomposition preserving natural spans:

| Source | ≥4k | ≥8k |
|---|---|---|
| Web lane at natural proportions | 155B | 64B |
| Curated long-context lane (all ≥4k) | 89B | 89B |
| Code lane at natural proportions | 110B | 45B |
| **Total** | **354B = 17.7% of the run** | **198B = 9.9%** |

**17.7% clears the 8% funding line by 2.2×.** The 4.45% curated lane is the *top-up* that guarantees the ≥8k buckets are non-empty, not the whole story. Correction to an earlier draft of this plan: the 423B figure for natural 8k web is a **pool** number (9.4% × 4.5T); the *delivered* amount at 677B of served web is **64B**, which is less than the 100B curated inventory, not more.

---

## 2. Indic lane — tier split

The composer default A40 / B25 / C20 / D15 is **not fundable**: tier C would need 63.2B against 5.0B unique = **12.6×**.

| Tier | Share of lane | Demand | Unique supply | Repeat |
|---|---|---|---|---|
| **A verified native** | **40%** | 126.4B | Sangraha verified **64.0B** | **1.98×** |
| **B unverified crawl** | **30%** | 94.8B | Sangraha unverified 24B + IndicCorpV2 20.9B = **44.9B** | **2.11×** |
| **C translated / parallel** | **8%** | 25.3B | BPCC 3B + Samanantar 2B = **5.0B** | **5.06×** |
| **D synthetic** | **22%** | 69.5B | Sangraha synthetic **162.0B** | **0.43×** |

Real **78%** / synthetic **22%**, inside Demystifying Synthetic's rephrase band (**<50% at every scale measured; ~30% is interpolated, since their grid runs 20% then 50%**). Tier D is legitimate specifically because widget 9 describes Sangraha synthetic as *"synthetic **and translated** expansion"* — rephrase-class, not invented-textbook class, whose ceiling is **≤3%**.

**Premise we are exposing rather than hiding:** tier C's 5.0B counts only BPCC and Samanantar. Widget 9's 162B synthetic set contains a *translated* component that arguably belongs to tier C. If it does, the 12.6× that forced this rebalance shrinks, and C could return toward the course's 20%. We keep 8% because the parallel-corpus fraction is not separable from the inventory as published — and we flag it as the weakest premise in §2.

**Three hazards, since no paper in the evidence base studied Indic.**

1. **Tokenizer × frozen embeddings.** Demystifying App. D.2 shows uncovered unigrams spiking per-token loss under a frozen English tokenizer — measured on English CC with a Llama-3 tokenizer, with no frozen-embedding condition and no Indic script, so the mechanism transfers by analogy only. The V4 incident is the real evidence: a sudden Hindi increase against frozen embeddings drove gradient norm ~150×. Mitigation: Indic tokenizer coverage fixed before the run, embeddings never frozen across an Indic share change, every Indic transition blended (§6).
2. **The quality classifier does not transfer.** Two-Phase's 5-bucket rule is an English CC classifier. It may not gate tier B until validated on Devanagari and Dravidian scripts with native-speaker labels.
3. **Never score Indic on a global utility median.** Preference Curriculum's Fig 6b shows a global PD sort putting **88% of arXiv** and **66% of GitHub** in the first half and **86% of Wikipedia** in the second, while §3.5 of the same paper claims it "does not skew towards specific sub-domains." Its PD is also weak-model-dominated. All utility scoring is therefore **per-lane**, never on a global median.

**Honest precedent.** The one quantitative low-resource precedent runs the other way: MAP-Neo cuts Chinese **25% → 8.5%** entering mid-training. Our anneal raises Indic 15.80% → 21.88%. The only supporting precedent, Yi-Lightning's "emphasis on low-resource multilingual support," discloses no percentages. We are writing this number first, not following the field — which is why H5 in §7 exists to refute it.

---

## 3. Agentic lane — the plan's one non-compliant number

**Arithmetic first.** Unique supply is **627M**: long trajectories 360M (SWE-Gym 150M, SWE-smith 120M, OpenHands 90M) and short function-call format data 267M (ToolBench 80M, ToolACE 60M, Glaive 50M, Nexus 30M, xLAM 25M, Hermes 22M). At a 4-epoch ceiling that is **2.508B tokens = 0.125% of 2T**.

Whole-plan agentic exposure is **40.0B (main) + 6.0B (anneal) = 46.0B**, so the gap a reviewer should quote is **73.4×**, not the 63.8× main-run figure.

**What the arithmetic can actually defend**, at the ceilings this plan itself cites:

| Constraint | 4 epochs | 6 epochs |
|---|---|---|
| Organic only | 0.125% | 0.188% |
| Collapse 80/20 (drift *erased*) | 0.157% | 0.235% |
| Demystifying rephrase ≤30% synth | 0.179% | 0.269% |
| Collapse 50/50 (drift *flattened*) | 0.251% | 0.376% |

**The defensible band is 0.125%–0.376%. We are shipping 2.00%, which is 5–16× outside it.** This is the single number in the plan that fails its own evidence, and it is stated here rather than buried.

**Why 2% anyway.** Widget 1 sets `agentic floor: 2` as a hard clamp — the slider cannot go below it — and Codex-class agentic work is a stated V5 goal. We take the floor as a capability commitment and pay for it with a generation program, rather than quietly writing 2% against a 627M inventory.

**Why the generation program is not the case Collapse refutes.**

1. **Environment-grounded.** Rollouts execute in a real harness seeded from SWE-Gym / SWE-smith / OpenHands. Tool observations are **real environment output**, not model output. Demystifying's failing category is *invented textbooks*; this is a third category neither paper measured.
2. **Verifier-filtered.** Only traces whose tests pass are kept. Collapse's theorems assume **unbiased** self-samples; rejection sampling makes them biased, which places them **outside** the theorem. Being outside a theorem is not proof of safety, and we do not claim it is.
3. **Frozen external teacher, never self-samples.** Collapse Fig 6 shows a finite teacher window only *delays* absorption (mean 17 → 95 → 216 for K = 1/5/10). Demystifying's teacher result also constrains the budget: **Llama-3-8B beats 3B, and 70B does not beat 8B** — so an ~8B generator, not the largest available.
4. **Real trajectory tokens in every batch**, per Collapse's condition. Their 20/80 arm held for ten generations — on an 8-layer, 256-dim char-level nanoGPT over one Shakespeare play, vocab 65. Our ratio is 6/94, the inverse of the arm we cite. This citation does not support us; it marks how far outside the measured region we are.
5. **Masking**, per widget 5: loss on plan, tool-call JSON, recovery and final answer; **tool observations masked**. Training on observations teaches the model to invent tool results.

FIM is *not* offered as a supply argument: it multiplies prediction targets per token and creates **zero new tokens**, so it cannot close a 627M → 46B gap.

**The corpus-wide compliance number.** Total synthetic mass across the whole plan is Indic tier D 69.5B + agentic generated 42.5B + verified synthetic 4.4B = **116.4B = 5.6% of 2.080T**. Invented-textbook-class content alone is **4.4B = 0.21%**, under Demystifying's ≤3% ceiling. So the plan is **compliant corpus-wide** and non-compliant only inside one 2% lane. That is the honest shape of the risk.

**Fallback that does not break the floor.** An earlier draft dropped agentic to 0.5% on proxy failure — which violates the `agentic floor: 2` clamp invoked to justify 2% in the first place. Corrected: if H2 refutes, **the share stays at 2%** and its *composition* changes — generated trajectories are replaced by FIM-multiplied real trajectories plus format data, accepting a lane that teaches tool-call *format* rather than multi-step agency, and agentic capability moves to post-training (out of scope here). The floor is honoured; the capability claim is withdrawn.

---

## 4. Anneal reserve — 80B

**Structure: 62% original-distribution ballast + 38% reserved data.**

| Component | Tokens | Drawn from | Quantile | Epochs | Kind |
|---|---|---|---|---|---|
| Tier-A verified Indic | 9.6B | Sangraha verified 64B | top **15%** | 0.15 | real |
| Algorithmic / competition code | 6.4B | keyword slice of Stack v2 | top **0.6%** | 0.01 | derived |
| Verified synthetic + textbooks | 4.4B | — | — | — | **generated**, unit-test gated |
| Agentic, environment-verified | 3.6B | generated from the 360M seed | — | — | **generated** |
| Long reasoning traces | 3.0B | OpenThoughts2 + OpenR1-Math = 4.6B | top **65%** | 0.65 | real |
| High-quality STEM | 1.6B | peS2o 42B + proof-pile-2 55B | top **1.6%** | 0.02 | real |
| Long agent trajectories | 1.4B | SWE-Gym + SWE-smith + OpenHands 360M | whole pool | **3.89** | real |

Reserve = 22.0B real/derived + **8.0B generated (27% of the reserve)**. Two components are data that **does not exist yet** and are labelled as such; the algorithmic-code slice is *derived* from a pool we already hold, using OpenCoder's keyword method, not new acquisition.

The long-CoT pool is so small (4.6B) that a 3.0B reserve is **65% of it** — that is not a selective quantile, and calling it one would be false. The long-trajectory reserve runs at **3.89 epochs**, inside the 4-epoch ceiling but nowhere near "reweighted, not repeated."

**Effective anneal mixture:** web 21.16 / code 22.97 / Indic 21.88 / STEM 9.16 / reasoning 9.06 / agentic 7.50 / verified-synthetic 5.50 / long-context 2.78 = **100.00**.

### Why 80B

**Like-for-like, this is 80 / 2080 = 3.85% of total tokens — exactly OpenCoder's ratio** (100B of 2.6T). Every Cluster A figure is reserve ÷ *total*, so quoting "4% of the main run" against them would be apples-to-oranges.

- **Taxonomy.** The mid-training survey's Table II separates two objects. *Cluster A, terminal fast-decay 1–5%*: MiniCPM 1.96%, Hunyuan-A13B 1.48%, **OpenCoder 3.85%**, Pangu 4.00%, Hunyuan-Large 4.76%. *Cluster B, full second stage 9–51%*: SmolLM2 9.03% up to Zamba 51.28%. Ours is Cluster A. Two-Phase's "best 40%" is Cluster B and is a different intervention.
- **Absolute tokens.** Spark Joy swept 50B / 100B / 200B / 300B; MMLU peaks at 100B (43.19), core average at 200B (39.32), and **no point below 50B exists**. 80B sits between their two lowest measured points. **Caveat we must state: Spark Joy never changed the learning rate** — under pure rsqrt its final leg ran at ~89–100% of cruising LR, so it prices a *mixture swap*, not a *decay leg*. It bounds the useful size of a reweighted final phase; it does not validate our LR schedule.
- **Ablation.** OpenCoder Fig 9: remove the high-quality slice and HumanEval stalls at ~0.33 instead of climbing to ~0.47, and the gap never closes.

### Why 62% ballast

Every disclosed recipe overlays **10–40% new on old**: OpenCoder 84/16, Zamba 60/40, Phi-4 70/30, Llama-3's anneal probe 70/30. The survey's stated reason is that *"a mismatch between mid-training and pretraining corpora can lead to catastrophic forgetting and degraded generalization."*

Spark Joy is the cautionary case: they zeroed bulk web but deliberately held *filtered* web at 30% (0.82×) "to prevent a large distribution shift," and Language Understanding was **still negative at every one of the four phase lengths** (−0.47 / −1.11 / −1.44 / −1.17 at 5 / 10 / 20 / 30%; the paper publishes no per-task breakdown within that category). Our anneal therefore keeps web at **21.16%**, a **0.63× multiplier** — more aggressive than their 0.82× on filtered web, less aggressive than their 0.42× on total web. We are inside the bracket they tested, closer to the risky end, and H4 tests it.

**Measured aggressiveness: our main→anneal shift is 17.64% (½·L1).** The course's own preset pair (24/2/6/6/16/12/34 → 20/8/18/8/28/10/8) is **32.0%**. This design is **45% gentler than the course preset**, and gentler than Spark Joy's 41.05%. ½·L1 is our own construct, not a course metric, and it cannot see intra-lane quality shifts — the top-15% Indic quantile is invisible to it.

**Exposure is cyclic, not a single tail block.** Dataset Decomposition: *"if we only see long sequences toward the end of training, long sequence learning occurs only when the learning rate is too small."* Their `Grow-P2` gains from cycling (1 → 8 cycles, MDQA 25.9 → 28.0), but `Grow-P100` *degrades* under the same change (27.0 → 24.1), so cycling is not universally good — it interacts with ramp aggressiveness. We cycle the reserve in **4 sub-cycles** across the 80B and cycle long-context exposure through the whole main run, and we note the mechanism DD describes applies to the main run's LR decay, not to the interior of a leg where LR is already small.

---

## 5. The protected always-on floor

**Fixed as: 5.5% of accepted tokens for Indic and 2.5% for agentic — per lane, 8.0% together. Real tokens only. Enforced in every length bucket, every curriculum cycle, and in the anneal mixture.**

**The membership set is corrected from an earlier draft.** Widget 3 marks `indic: scarce:true` and `agentic: scarce:true`, and `reasoning: scarce:false`. Scoring each lane against the widget's English proxy `[0.70, 0.53, 0.33]` shows why:

| Lane | Score |
|---|---|
| code | 0.841 |
| **reasoning** | **0.818** |
| web | 0.776 |
| agentic | 0.602 |
| indic | 0.567 |

Reasoning scores **third-highest, above web** — at `keepFrac = 0.40` it is essentially never rejected. Adding it to the floor would have been an error twice over: it does not need protection, and an **aggregate** 8% across three lanes is satisfiable with 8% reasoning and **zero agentic tokens** — precisely the starvation the floor exists to prevent. Hence per-lane numbers.

Each clause exists because a specific result shows what breaks without it.

| Clause | Evidence |
|---|---|
| A floor at all | Widget 3's English proxy rejects Indic (0.567) and agentic (0.602); V4 shipped an 8% always-on lane for Indic + agentic |
| **Hard** constraint, not a preference | CLIMB: the code cluster C20 goes to **exactly 0** under a reasoning-only objective. Any lane absent from the objective dies |
| Lanes also in the selector objective | CLIMB Figs 5/7: different objectives produce different winners |
| **Real** tokens only | Collapse's partial-synthetic bound requires the same real corpus every generation — at nanoGPT scale, so the direction transfers, the percentages do not |
| Per **bucket** and per **cycle** | Dataset Decomposition Alg 1: *"If a bucket is empty, we exclude it from sampling"* — a scarce lane can silently vanish after one cycle |
| In the **anneal** too | Spark Joy's sans-math arm: a 100B final phase that stops feeding a lane drove MMLU to **29.71 vs 35.69 baseline (−5.98)** and Reading Comprehension to **26.48 vs 37.02 (−10.54)**. Confound: they held proportions while shrinking the pool, so the magnitude is inflated; the direction holds |
| A small floor suffices | OLMo 2, via survey §III-C: *"it is not strictly necessary to have a large proportion of domain-specific data in the annealing mixture, just that domain-specific data is present"* |

**When does the floor bite?** Indic + agentic by stage is 18 / 19 / 17 / 17% and 29.4% in the anneal — so the 8% aggregate is slack by 2.1–3.7× throughout, and **this floor never binds under this mixture**. It is a backstop against OPUS drift, not an active constraint. Saying otherwise would oversell it. The composer's per-lane floors (`indic ≥ 12`, `agentic ≥ 2`) *are* binding constraints on the mixture, and both are honoured: 15.80 ≥ 12 and 2.00 = 2.

OPUS and the curriculum act on orthogonal axes — OPUS decides *whether* a token is served, the curriculum decides *when* — so they compose. Preference Curriculum is the published instance of the *when* axis and has **no floor of any kind**, which is why this one is ours to add.

---

## 6. Curriculum

Stage budgets: **Seed 200B → General 700B → Reasoning 600B → Long-context 500B**, then the **80B anneal**. Every row sums to 100.

| Stage | web | code | reason | long | indic | STEM | agentic | v-synth | Difficulty admitted |
|---|---|---|---|---|---|---|---|---|---|
| Seed (200B) | 54 | 13 | 2 | 1 | 16 | 12 | 2 | — | B0–B1 |
| General (700B) | 41 | 20 | 4 | 2 | 17 | 14 | 2 | — | B0–B2 |
| Reasoning (600B) | 27 | 28 | 13 | 3 | 15 | 12 | 2 | — | B0–B3 |
| Long-context (500B) | 24 | 29 | 12 | 11 | 15 | 7 | 2 | — | B0–B4 |
| **Anneal (80B)** | 21.2 | 23.0 | 9.1 | 2.8 | 21.9 | 9.2 | 7.5 | 5.5 | B0–B5 |

**Undeclared deviations, now declared.** The four main-lane shares that differ from the course preset by less than a point (STEM 12 → 11.45, Indic 16 → 15.80, web 34 → 33.85, code 24 → 23.95) are **not independent choices** — they fall out of solving the stage profiles to hit reasoning 8.5% and long-context 4.45% while every row sums to 100. Likewise the anneal's code / reasoning / STEM / agentic values are *derived* from the 62/38 construction, not chosen. Only four numbers in this plan are genuine deviations: reasoning up, long-context down, anneal size, and Indic tier rebalancing.

### 6a. Difficulty bands — B0 to B5

Definitions are widget 7's. The **example** column is what the assignment requires and the widget does not supply.

| Band | Level | Definition | Concrete example | Lane |
|---|---|---|---|---|
| **B0** | Nursery | simple children's sentences | *"The cat sat on the mat. The mat was red."* | web |
| **B1** | Grade-school | basic grade-school text | *"Water boils at 100 °C at sea level."* + integer-answer word problems | web, Indic |
| **B2** | High-school | high-school level material | A Wikipedia article on photosynthesis; a 30-line Python script with one loop | web, code, Indic |
| **B3** | Undergraduate | undergraduate coursework | A GSM8K-style multi-step word problem; a single-file module with tests; an IndicGenBench summarisation pair | code, STEM, reasoning |
| **B4** | Graduate | graduate-level texts | An AIME problem with a worked solution; a SWE-Gym task with a repo checkout; a peS2o paper section | reasoning, STEM, agentic |
| **B5** | Research / PhD | research and PhD-grade papers | A GPQA-Diamond physics item; a proof-pile-2 formal proof; a full SWE-smith trajectory with recovery | reasoning, agentic, STEM |

Two rules. **Monotone floor:** each stage admits its band *and everything below it* — never a hard gate. Dropping low bands late is what produced Spark Joy's negative Language Understanding at every phase length. **B5 is reserve-only:** withheld from the main run, spent in the anneal — the same object as §4's reserve, expressed on the difficulty axis.

**No paper supports a content-difficulty ladder, and one argues against it.** Preference Curriculum's Fig 9 shows its "hard" half requires *less* scientific content (0.61 vs 0.70) and *less* cultural background (0.59 vs 0.69), with logical-reasoning requirement **identical at 0.72 / 0.72**; Fig 6b puts 88% of arXiv in the *easy* half. **A perplexity gap is not a difficulty axis.** This ladder is built from source provenance and benchmark level — a labelling decision, and a design bet. Dataset Decomposition's ordering result is a **length** ladder, a different axis that can fight this one.

### 6b. Reasoning-length bands

The course's four effort tiers, all solving the **same problem** — *how many integers in [1, 1000] are divisible by 3 or 5?* Answer **467**, correct at every band; only the solve rate changes. Token counts and rates are computed with widget 6's own tokenizer and curve `acc(L) = 0.955 − 0.615·exp(−L/τ)`, `τ = 0.18 · ultra_tokens`.

| Band | Steps | Trace tokens | Solve rate | First step of the example | Share of trace budget | Tokens |
|---|---|---|---|---|---|---|
| **LOW** | 2 | **37** | **61.5%** | *"Inclusion-exclusion: floor(1000/3) + floor(1000/5) − floor(1000/15)."* | 15% | 4.26B |
| **MEDIUM** | 4 | **74** | **76.8%** | *"Count multiples of 3 up to 1000: floor(1000/3) = 333."* | 30% | 8.52B |
| **HIGH** | 6 | **161** | **90.9%** | *"Let A = multiples of 3 and B = multiples of 5 inside [1, 1000]."* | 35% | 9.94B |
| **ULTRA** | 14 | **346** | **95.3%** | *"Restate the goal… then verify two independent ways."* | 20% | 5.68B |

These partition the **28.4B trace budget** from §1.1, not the whole 170B lane. ULTRA at 5.68B against 4.6B of long-CoT inventory is **1.23×** — fundable.

**Why ULTRA is the smallest band.** Widget 6's own curve says ULTRA buys **+4.40 points** over HIGH (95.3 vs 90.9) for **2.15×** the tokens, which trips the widget's *"wasted effort"* flag at +5.0. HIGH carries the largest share because that is where the curve is still buying accuracy per token.

**Why all four must exist.** The effort dial selects among behaviours the model was trained to produce. A model shown only long traces cannot answer briefly; one shown only short traces has nothing to select when asked to think. Cross-check: Two-Phase moved GSM8K **30.86 → 40.33** with reasoning-shaped task data at **1.3% of its second phase**, so a small well-placed slice is enough — 28.4B is not greedy. The 15/30/35/20 split is ours; only the ULTRA cap has course-data backing.

### 6c. Packing, position, and seams

- **Binary dataset decomposition, not concat-and-chunk.** Each document of length `l` is split into adjacent power-of-two spans; buckets hold single-document sequences, so no attention mask is needed and no tokens are wasted. It beats the baseline by **+2.9 regular / +3.4 long-context average** (DD Table 5). Document masking alone is not a substitute: it lifts regular 51.5 → 52.4 but drops long-context 27.5 → 27.1 and craters MDQA-30 **20.5 → 16.0**.
- **All buckets for short-document lanes; the ≥256 variant only where documents are naturally long.** We measured this on our own corpus (§7): a global ≥256 floor discarded **44.9%** of tokens. Applied to Indic snippets, QA-format agentic data or parallel corpora, that is exactly the per-bucket starvation §5's floor forbids.
- **RoPE base 100,000 from the start.** Free **+5.4 MDQA** on the baseline and +4.8 on the decomposed run, regular average unchanged (DD Table 4, **1B only**; Table 4's 24.9 for DD≥256@100k conflicts with Table 2's 23.0 for the same configuration, so treat the magnitude as approximate).
- **Training sequence length is 8192.** The curated long-context inventory is *32K+ packed*, so those sequences are decomposed into 8k spans. This plan therefore does **not** claim any capability beyond 8k; a 32k–128k extension is a separate budget and out of scope.
- **Seams: 4 transitions × 20B blended = 80B, 4% of the main run.** Five stages have four boundaries.
- **The seam width is priced, not guessed.** Widget 8's model gives `peakFactor = 1 + effSharp·A·effFrozen`. At a 20B band the predicted peak is **1.34× with frozen embeddings and 1.23× unfrozen**, against the widget's `RED_T = 3.0` instability threshold — and ~**6B** already clears it frozen. V4's ~150× corresponds to sharpness 1.0, frozen embeddings, zero band. Corroboration: DD Fig 8 shows the un-ramped arm throwing ~8 loss spikes to 7.5–8.1 while the ramped arm is spike-free, though those two arms differ in both packing *and* curriculum, so it is not attributable to ordering alone.
- **Ramp shape, not a step.** Preference Curriculum's winning S-shape blends over **43.9%** of its run and beats a hard switch by ~1.1 points — but that is a blend between two halves of *one corpus*, not between two mixtures, and 43.9% is 44× wider than our 1%-per-seam band. We take the *shape* claim and not the width. MiniMax-01 reportedly interpolates source weights linearly across transitions (primary 2501.08313; this detail is **not** in the mid-training survey's published text, only its source comments).

---

## 7. Proxy protocol — hypotheses with thresholds

Cost basis (6ND): a 40B probe on 120B params ≈ **2.9e22** FLOPs against ≈**1.44e24** for the full run — **1/50 of a run**, so twelve probes cost ~24%. CLIMB's 112-run search is priced separately at ~45 GPU-h per 350M proxy. Branching follows Llama 3: a partially trained checkpoint, LR decayed linearly to 0 over the probe, candidate at **30% against 70% default**.

Noise floor matters: Spark Joy's own peaks are **0.60pp** (MMLU) and **0.86pp** (core average) at n=1, so every threshold below is set outside that band.

| # | Hypothesis | Scale | Metric | Confirms | Refutes | Action on refute |
|---|---|---|---|---|---|---|
| **H1** | Long-context 4.45% + packing suffices (the 2–9% region is unmeasured) | 1B, 100B, arms 0 / 2 / 4.45 / 9.4% | **MDQA-30** | 4.45% arm ≥ **90%** of the 9.4% arm | **< 75%** | raise curated lane to 9.4%, take from web |
| **H2** | Verified-generated agentic trajectories transfer | **3B**, 40B branch, arms format-only / +verified / +unverified | **SWE-bench Verified pass@1**, **BFCL AST-match** | verified arm ≥ **+3.0 pts** over format-only | **< +1.0 pt** | keep 2% share, swap generated for FIM-multiplied real + format (§3) |
| **H3** | Indic tier C survives 5.06× repetition | 1B, 100B, arms C at 8 / 4 / 0% | **IndicGenBench chrF**, **MILU** | 8% arm ≥ 4% arm on both, within **1.0 pt** | 8% arm **> 1.0 pt below** on either | C → 4%, mass to D |
| **H4** | An 80B anneal beats 40B | 1B, branch at 96% / 98% | core average of MMLU + GSM8K + HumanEval | 80B ≥ **+1.0 pt** over 40B | **≤ 0 pt** | revert to 40B, bank the compute |
| **H5** | Raising Indic in the anneal does not cause the MAP-Neo effect | 1B, anneal Indic 21.9 / 15.8 / 8.5% | **MILU + Flores-101 chrF**; **MMLU** as forgetting check | Indic ≥ **+1.5 pts** and MMLU loses **≤ 1.0 pt** | MMLU loses **> 1.0 pt** | flatten Indic across the anneal |
| **H6** | A 20B seam holds the Indic transition | 1B, gradient-norm trace, bands 0 / 5 / 20B, embeddings unfrozen | **peak gradient-norm multiplier** | peak **< 3.0×** (widget 8 `RED_T`) | **> 3.0×** | widen until it clears |
| **H7** | The four length bands produce a controllable dial | 1B, 100B, arms 15/30/35/20 vs HIGH-only | **LOW:ULTRA trace-length ratio** and accuracy at each | ratio ≥ **4×** with ULTRA accuracy ≥ LOW | ratio **< 2×** | widen the band spread |

### What we actually ran

Full 1B/3B training is unavailable in this environment, so H1–H7 are specified and unrun. This plan claims the **"highest"** tier — concrete proxies with named metrics and numeric thresholds — and explicitly not "very highest."

Two things were executed and are reproducible from this repository.

**(a) The mixture is executable arithmetic.** Stage profiles time-average to the declared shares to within **0.05pp**; all rows sum to 100; every demand, ratio, tier repeat factor, reserve component, quantile, epoch count, the 17.64% shift and the 116.4B synthetic total are computed, not asserted.

**(b) A micro-replication of the packing claim the long-context decision rests on.** DD's average-context formula `Σl(l−1) / 2Σl` on a 342-document / 78,581-token corpus of our own papers and lecture notes:

| Arm | Sequences | Mean length | Avg in-document context |
|---|---|---|---|
| Original documents | 342 | 229.8 | 3486.5 |
| Concat-and-chunk @2048 | 380 | 206.8 | **421.1** |
| Decomposition, all buckets | 1,375 | 57.1 | 1917.6 |
| Decomposition ≥256 | 59 | 733.3 | **3452.5** |

Concat-and-chunk split **11.1%** of documents at a chunk boundary. The direction replicates — decomposition ≥256 carries **8.20×** the in-document context — but that **overshoots the published 1.45×** (1344 vs 930) because our corpus is short-document-heavy (median 104 tokens vs RefinedWeb's 598 mean) and because the ≥256 filter **discards 44.9% of our tokens**, where on RefinedWeb it is nearly free.

The overshoot is the useful result: it is what produced the bucket policy in §6c. A first attempt at this measurement used mean *span* length instead of average *context* and reproduced the effect backwards — recorded here because it is the reason the metric definition matters.

---

## 8. Cleaning, aimed at the starved slots

The plan's own accounting names which slots are starved, on two independent definitions.

**Starved by the course's ≥8% funding rule:** agentic (2.00%) — and long-context (4.45%) on lane share, though its effective ≥4k exposure of 17.7% clears the line.

**Starved by supply:** agentic **73.4×**, Indic tier C **5.06×**, reasoning long-CoT (5.68B ULTRA demand against 4.6B), code post-dedup **1.32×**, STEM **0.92×** with no headroom.

Cleaning effort is therefore directed, in order:

1. **Agentic trajectories** — the only lane where new cleaned tokens change the plan's worst number. Harvest and verify execution traces; every 100M real trajectory tokens cuts the generated fraction by ~2 points.
2. **Indic tier C** — separate the translated fraction of Sangraha's 162B set from the synthetic fraction. If parallel-corpus tokens are separable, tier C's 12.6× premise dissolves and the composer's 20% becomes fundable (§2).
3. **Long-CoT reasoning** — the 4.6B long-trace pool is the binding constraint on the ULTRA band and on the anneal reserve.
4. **STEM** — 0.92× pre-selector and 2.29× post-selector means no headroom; cleaned peS2o and proof-pile-2 tokens are directly load-bearing.
5. **Code, at file level** — the 32.9% retention ratio means cleaning changes the effective pool, not just the headline.

Web needs no cleaning attention: at 0.15× it is the one lane where supply is not a constraint, and Two-Phase's evidence says the marginal work there is *filtering* (zero the Low bucket), not acquisition.

---

## 9. Where this plan has no evidence

- **No paper in the evidence base studied Indic.** The tier split is arithmetic against our inventory plus a synthetic ceiling borrowed from English rephrase experiments. The one quantitative low-resource precedent (MAP-Neo, Chinese 25% → 8.5%) points the opposite way from our Indic-up anneal.
- **No paper trains agentic trajectories at pretraining scale.** "Agent" appears once in the mid-training survey, as a dataset name. The verifier-breaks-the-loop argument is mechanistically reasonable and **unmeasured**, and 2% is 5–16× outside the band our own citations support.
- **Long-context evidence stops at 8192.** Nothing here licenses 32k or 128k.
- **The anneal's value at 120B is unmeasured, and the one frontier-scale measurement is null.** Annealing gave Llama 3 8B +24.0% GSM8K and +6.4% MATH but *"a negligible uplift for the 405B model."* Every large published mid-training gain is ≤14B.
- **Scale gaps we are relying across.** Collapse's percentages come from an 8×256 char-level nanoGPT on one Shakespeare play; DD's RoPE and ordering results are 1B; OpenCoder's dedup result is 1.5B Python; Demystifying is ≤3B on English CC with CE loss only, and its "~30%" is interpolated from a grid that skips 30%.
- **Almost nothing has error bars.** CLIMB's checklist answers "No"; Spark Joy, Preference Curriculum and DD's tables are single-seed. Spark Joy's MMLU peak is a 0.60pp gap. Cite curve shapes, not exact optima.
- **Eleven claims reach us through the mid-training survey rather than a primary.** Where a decision rests on one, the primary is named (MiniMax-01 2501.08313, Llama 3 2407.21783, MAP-Neo 2405.19327).

---

## 10. The numbers most likely to be wrong

| # | Number | Confidence | Why it might be wrong |
|---|---|---|---|
| 1 | **Agentic 2.00%** | **Low** | 73.4× gap; 94% generated; 5–16× outside our own cited band. H2 is the test; the fallback withdraws the capability claim, not the share |
| 2 | **Indic tier C 8% at 5.06×** | **Low-medium** | Rests on tier C = 5.0B, which ignores a possibly-separable translated fraction of the 162B set |
| 3 | **Reasoning 8.5%** | **Medium** | Forced by `WEIGHTED_MIN = 8`, but 92% of the lane is AON academic text, not traces; the trace pool is 7.1B |
| 4 | **Long-context 4.45%** | **Medium** | Threshold is proven, 0% is catastrophic, ~9.4% saturates — the 2–9% region is unmeasured. Defence rests on 17.7% effective exposure, not the lane |
| 5 | **Anneal 80B** | **Medium-high** | 3.85% of total matches OpenCoder exactly; weakened because Spark Joy's sweep is a cruising-LR swap, not a decay leg |
| 6 | **62% ballast / 0.63× web** | **Medium-high** | Inside the 10–40% overlay band; more aggressive on web than Spark Joy's 0.82× |
| 7 | **Per-lane floor 5.5 / 2.5** | **High** | Membership matches widget 3's `scarce` set; four independent supports. Honest caveat: it never binds under this mixture |
| 8 | **Difficulty bands B0–B5** | **Medium** | Definitions are the course's; the ladder itself has no paper support and PrefCurriculum argues a perplexity gap is not difficulty |
| 9 | **Length bands 15/30/35/20** | **Medium** | Only the ULTRA cap is course-derived; the rest is ours |
| 10 | **Decomposition + RoPE 100k** | **High** | Measured, cheap, and confirmed in our own micro-replication — though at a magnitude we could not reproduce |

**Attack these first: agentic 2.00%, Indic tier C, and the reasoning lane's 7.1B trace pool.**
