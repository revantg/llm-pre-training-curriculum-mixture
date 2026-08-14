# V5 Data Mixture and Curriculum Specification

**Scope.** Main pretraining run plus the anneal — the decay leg of the same run, same next-token CE objective. SFT, RLVR and preference training are out of scope.

**Budget.** ~120B parameters · main run **2.000T** · anneal **+80B** · total **2.080T**.
**Selector.** OPUS, keep ~40% of candidates (~6× effective tokens), with the per-lane floor fixed in §5.

Chinchilla-optimal for 120B is ≈2.4T, so 2.000T is **0.83× compute-optimal on unique tokens** — not an overtrained run. OPUS's ~6× multiplier means ~12T *effective* tokens, which is a selection-efficiency claim, not a unique-token claim. 2T is also kindest to scarce supply: at 10T the agentic gap widens from 40B-vs-0.627B to 200B-vs-0.627B.

---

## 1. Main-run lane shares

Exact time-average of the §6 stage profiles. Sums to 100.00.

| Lane | Share | Demand | Unique supply | Pre-selector | Post-selector | Verdict |
|---|---|---|---|---|---|---|
| General web | **33.85%** | 677.0B | 4.500T | 0.15× | 0.38× | covered |
| Code | **23.95%** | 479.0B | 1.100T → **362B** eff. | 0.44× → **1.32×** | 3.31× | **repeat** |
| Indic | **15.80%** | 316.0B | 276.0B | 1.14× | 2.86× | repeat |
| STEM / math | **11.45%** | 229.0B | 250.0B | 0.92× | 2.29× | repeat |
| Reasoning | **8.50%** | 170.0B | 85.1B | 2.00× | 4.99× | repeat |
| Long-context (curated) | **4.45%** | 89.0B | 100.0B | 0.89× | 2.23× | repeat |
| Agentic | **2.00%** | 40.0B | **0.627B** | **63.8×** | 159.5× | **must generate** |

**Selector-adjusted supply.** OPUS accepts ~40% of what it is offered, so at 40% acceptance **code, STEM and long-context all move covered → repeat**, and reasoning reaches 4.99× — effectively Two-Phase's 6-epoch ceiling with no headroom. We rely on a specific counter-argument: a *rejected* token is not consumed, so it returns to the pool at a later iteration under a different model state. The pre-selector column is therefore correct for supply *existence*; the post-selector column is correct for *schedule risk*. Both are planned against.

**Code supply is smaller than the headline.** At OpenCoder's file-level retention (32.74B / 99.47B = 32.9%) the 1.100T pool delivers ≈**362B**, so 479B is **1.32× repeat**. We accept file-level dedup anyway: it wins HumanEval and MBPP at every matched budget (Fig 8, Table 9) and repo-level's extra 67B contains 52B of character-identical text.

**Filters.** Natural CC is **64.44% Low**; zeroing Low and upsampling High lifts MMLU **42.94 → 56.10** (Two-Phase Tables 16–17). The same ablation costs code **19.25 → 17.41**, so it is applied to web only. Popularity is never a gate: `stars>=5` gave lower training loss and worse HumanEval (~0.12 vs 0.18) and MBPP (~0.14 vs 0.20) at 100B.

### 1.1 Every deviation from the course preset, and how it is funded

Six lanes differ. Only two are choices; the rest are the arithmetic closing.

| Lane | Course | v5 | Δ | Tokens |
|---|---|---|---|---|
| Reasoning | 6.00 | **8.50** | **+2.50** | +50.0B |
| Long-context | 6.00 | **4.45** | **−1.55** | −31.0B |
| STEM | 12.00 | 11.45 | −0.55 | −11.0B |
| Indic | 16.00 | 15.80 | −0.20 | −4.0B |
| Web | 34.00 | 33.85 | −0.15 | −3.0B |
| Code | 24.00 | 23.95 | −0.05 | −1.0B |
| Agentic | 2.00 | 2.00 | 0.00 | 0 |

Reasoning's +2.50pp is funded by long-context's −1.55pp plus **0.95pp (19B)** drawn from STEM, Indic, web and code. The 0.95pp is a real cost, and it lands hardest on **STEM, the 0.92× lane with no headroom** — that is the weakest consequence of raising reasoning, and it is why H4′ in §7 monitors STEM. Indic stays above its course floor (15.80 ≥ 12); agentic sits exactly on its floor.

### 1.2 Reasoning is 8.5%, and what actually fills it

Widget 1 sets `WEIGHTED_MIN = 8` — *"a lane needs at least this share to move its benchmarks."* At the course's 6% the reasoning lane is **starved by the course's own rule** while being asked to win AIME, GPQA, HLE and BBH. 8.5% is the smallest share clearing that line. Arithmetic forcing, not preference.

| Component | Inventory datasets | Unique | Allocation | Epochs |
|---|---|---|---|---|
| Trace-shaped | OpenThoughts2 **3B**, OpenMathReasoning **2B**, OpenR1-Math **1.6B**, NuminaMath **0.5B** | **7.1B** | 28.4B | **4.00** |
| Academic reasoning text | AON / D5 Academic-Reasoning-Overflow (V4 corpus) | **78B** | 141.6B | **1.82** |

**The trace-shaped pool is 7.1B, not 85B; long-CoT is 4.6B.** The 2.00× lane ratio is comfortable only because 92% of the lane is AON academic prose, which is real and reasoning-adjacent but is **not** chain-of-thought. Any length-distribution claim is sized against 7.1B (§6b).

### 1.3 Long-context: the lane share is not the funding number

4.45% is **below `WEIGHTED_MIN = 8`**. The answer is that long-context capability is bought by a **packing policy across every lane**, not by one lane.

Dataset Decomposition measures a **threshold**: multi-doc QA is ≈0 until pretraining sequences exceed the eval context, then jumps and flattens (MDQA-10 `0.8 → 20.8` at 2k, then 21.2, 20.4). Any mixture lacking the 4k/8k buckets scores **0.0–0.4** on MDQA-20/30. RefinedWeb's *natural* decomposition is already **9.4%** of tokens at 8192 and **22.9%** at ≥4k.

| Source | ≥4k | ≥8k |
|---|---|---|
| Web at natural proportions | 155B | 64B |
| Curated long-context lane | 89B | 89B |
| Code at natural proportions | 110B | 45B |
| **Total** | **354B = 17.7%** | **198B = 9.9%** |

**17.7% clears the 8% line by 2.2×.** The curated 4.45% is the top-up guaranteeing non-empty ≥8k buckets.

Two corrections to earlier drafts of this plan. The 423B figure for natural 8k web is a **pool** number (9.4% × 4.5T); *delivered* at 677B of served web it is **64B** — less than the 100B curated inventory, not more. And the curated inventory is **repo-packed code 60B + packed books 40B**, neither of which is multi-document; so the lane's job is *long single-document* context, and the multi-document capability MDQA measures is **not** funded by any dataset we hold. That gap is real and is H1's actual risk.

---

## 2. Indic lane — tier split

The composer default A40/B25/C20/D15 is **not fundable**: tier C needs 63.2B against 5.0B = **12.6×**.

| Tier | Share | Demand | Unique supply | Repeat |
|---|---|---|---|---|
| **A verified native** | **40%** | 126.4B | Sangraha verified **64.0B** | **1.98×** |
| **B unverified crawl** | **30%** | 94.8B | Sangraha unverified 24B + IndicCorpV2 20.9B = **44.9B** | **2.11×** |
| **C translated / parallel** | **8%** | 25.3B | BPCC 3B + Samanantar 2B = **5.0B** | **5.06×** |
| **D synthetic** | **22%** | 69.5B | Sangraha synthetic **162.0B** | **0.43×** |

Real **78%** / synthetic **22%** — inside Demystifying's rephrase band (**<50% measured at every scale; "~30%" is interpolated, their grid runs 20% then 50%**). Tier D qualifies as rephrase-class specifically because widget 9 calls Sangraha synthetic a *"synthetic **and translated** expansion"*; the invented-textbook ceiling is **≤3%** and does not apply.

**Premise exposed rather than hidden.** Tier C's 5.0B counts only BPCC and Samanantar. The 162B set contains a *translated* component that arguably belongs in tier C; if it is separable, the 12.6× that forced this rebalance shrinks and the course's 20% becomes fundable. We keep 8% because the parallel fraction is not separable as published — and this is the weakest premise in the document (§8 item 2).

**Three hazards, since no paper here studied Indic.**

1. **Tokenizer × frozen embeddings.** Demystifying App. D.2 shows uncovered unigrams spiking per-token loss under a frozen English tokenizer — but measured on *English* CC with a Llama-3 tokenizer, with no frozen-embedding condition and no Indic script, so it transfers by analogy only. The real evidence is V4: a sudden Hindi increase against frozen embeddings drove gradient norm ~150×. Mitigation: Indic tokenizer coverage fixed pre-run; embeddings never frozen across an Indic share change; every Indic transition blended (§6c).
2. **The quality classifier does not transfer.** Two-Phase's 5-bucket rule is an English CC classifier and may not gate tier B until validated on Devanagari and Dravidian scripts.
3. **Never score Indic on a global utility median.** Preference Curriculum's Fig 6b shows a global PD sort putting **88% of arXiv** and **66% of GitHub** early and **86% of Wikipedia** late, while the same paper's §3.5 claims it "does not skew towards specific sub-domains." All utility scoring is **per-lane**.

**Honest precedent.** The one quantitative low-resource precedent runs the other way: MAP-Neo cuts Chinese **25% → 8.5%** entering mid-training, while our anneal raises Indic 15.80% → 21.88%. The only supporting precedent (Yi-Lightning, "low-resource multilingual support") gives no percentages. H5 exists to refute us.

---

## 3. Agentic — the one non-compliant number

**Unique supply is 627M**: long trajectories 360M (SWE-Gym 150M, SWE-smith 120M, OpenHands 90M) and short function-call format data 267M (ToolBench 80M, ToolACE 60M, Glaive 50M, Nexus 30M, xLAM 25M, Hermes 22M). At 4 epochs that is **2.508B = 0.125% of 2T**.

Whole-plan exposure is 40.0B (main) + 6.0B (anneal) = **46.0B**, so the gap to quote is **73.4×**, not the 63.8% main-run figure.

**What the arithmetic defends**, at the ceilings this plan itself cites:

| Constraint | 4 epochs | 6 epochs |
|---|---|---|
| Organic only | 0.125% | 0.188% |
| Collapse 80/20 (drift *erased*) | 0.157% | 0.235% |
| Demystifying rephrase ≤30% | 0.179% | 0.269% |
| Collapse 50/50 (drift *flattened*) | 0.251% | 0.376% |

**The defensible band is 0.125%–0.376%. We ship 2.00%, which is 5–16× outside it.** Stated here, not buried.

**Why 2% is not ours to lower.** Widget 1 hard-codes `{key:"agentic", name:"Agentic / tool-use", floor:2}`, and `normalize()` will not let any slider below it. 2% is the course's floor, and Codex-class agentic work is a stated V5 goal. We pay for it with a declared generation program rather than write 2% quietly against a 627M inventory.

**Why this program is not the case Collapse refutes.**

1. **Environment-grounded.** Rollouts execute in a real harness seeded from SWE-Gym / SWE-smith / OpenHands; tool observations are **real environment output**. Demystifying's failing category is *invented textbooks* — this is a third category neither paper measured.
2. **Verifier-filtered.** Only test-passing traces are kept. Collapse's theorems assume **unbiased** self-samples; rejection sampling makes them biased, placing them **outside** the theorem. Outside a theorem is not proof of safety, and we do not claim it is.
3. **Frozen external teacher, ~8B.** Demystifying's teacher result bounds the budget: **Llama-3-8B beats 3B, and 70B does not beat 8B**. A finite teacher window only *delays* absorption (Collapse Fig 6), so the teacher is external and frozen, never self-sampled.
4. **Real trajectory tokens in every batch.** Collapse's 20/80 arm held for ten generations — on an 8×256 char-level nanoGPT over one Shakespeare play, vocab 65. Our ratio is 6/94, the *inverse*. This citation marks how far outside the measured region we are; it does not support us.
5. **Masking** per widget 5: loss on plan, tool-call JSON, recovery, final answer; **tool observations masked**. Training on observations teaches the model to invent tool results.

FIM is not offered as supply: it multiplies prediction targets per token and creates **zero new tokens**.

**Corpus-wide compliance.** Total synthetic mass is Indic tier D 69.5B + agentic generated 42.5B + verified synthetic 4.4B = **116.4B = 5.6% of 2.080T**, of which invented-textbook-class is **4.4B = 0.21%**, under the ≤3% ceiling. The plan is **compliant corpus-wide** and non-compliant only inside one 2% lane. That is the honest shape of the risk.

**Fallback that does not break the floor.** An earlier draft dropped agentic to 0.5% on proxy failure — which crosses the `floor:2` clamp invoked to justify it, and the §5 floor. Corrected: if H2 refutes, **the share stays at 2.00%** and its *composition* changes — generated trajectories are replaced by FIM-multiplied real trajectories plus format data, yielding a lane that teaches tool-call *format* rather than multi-step agency. The floor is honoured; the capability claim is withdrawn.

---

## 4. Anneal reserve — 80B

**62% original-distribution ballast + 38% reserved.**

| Component | Tokens | Drawn from | Quantile | Epochs | Kind |
|---|---|---|---|---|---|
| Tier-A verified Indic | 9.6B | Sangraha verified 64B | top **15%** | 0.15 | real |
| Algorithmic / competition code | 6.4B | keyword slice of Stack v2 | top **0.6%** | 0.01 | derived |
| Verified synthetic + textbooks | 4.4B | — | — | — | **generated**, unit-test gated |
| Agentic, environment-verified | 3.6B | generated from the 360M seed | — | — | **generated** |
| Long reasoning traces | 3.0B | OpenThoughts2 + OpenR1-Math = 4.6B | top **65%** | 0.65 | real |
| High-quality STEM | 1.6B | peS2o 42B + proof-pile-2 55B | top **1.6%** | 0.02 | real |
| Long agent trajectories | 1.4B | SWE-Gym + SWE-smith + OpenHands 360M | whole pool | **3.89** | real |

Reserve = 22.0B real/derived + **8.0B generated (27% of the reserve)**. Two components are data that **does not exist yet** and are labelled so; the algorithmic slice is *derived* from a pool we hold, by OpenCoder's keyword method.

Two honest notes. The long-CoT pool is only 4.6B, so a 3.0B reserve is **65% of it** — not a selective quantile, and calling it one would be false. The long-trajectory reserve runs at **3.89 epochs**, inside the 4-epoch ceiling but nowhere near "reweighted, not repeated." Earlier drafts computed reserve epochs against the *whole un-reserved lane*, which proves a reserve is safe by assuming it is not a reserve; the table above uses the pool each component actually draws from.

**Effective anneal mixture:** web 21.16 / code 22.97 / Indic 21.88 / STEM 9.16 / reasoning 9.06 / agentic 7.50 / verified-synthetic 5.50 / long-context 2.78 = **100.00**.

**Why 80B.** Like-for-like this is **80 / 2080 = 3.85% of total tokens — exactly OpenCoder's ratio** (100B of 2.6T). Every Cluster A figure is reserve ÷ *total*, so "4% of the main run" would be apples-to-oranges. The mid-training survey separates *Cluster A, terminal fast-decay 1–5%* (MiniCPM 1.96%, Hunyuan-A13B 1.48%, **OpenCoder 3.85%**, Pangu 4.00%, Hunyuan-Large 4.76%) from *Cluster B, full second stage 9–51%* (SmolLM2 9.03% … Zamba 51.28%). Ours is Cluster A; Two-Phase's "best 40%" is Cluster B, a different intervention.

Spark Joy swept 50B / 100B / 200B / 300B: MMLU peaks at 100B (43.19), core average at 200B (39.32), and **no point below 50B exists**, so 80B sits between their two lowest measured points. **Caveat: Spark Joy never changed the learning rate** — under pure rsqrt its final leg ran at ~89–100% of cruising LR, so it prices a *mixture swap*, not a *decay leg*. It bounds the useful size of a reweighted final phase; it does not validate our LR schedule. The ablation that the reserve matters at all is OpenCoder Fig 9: remove the HQ slice and HumanEval stalls at ~0.33 instead of reaching ~0.47, gap never closing.

**Why 62% ballast.** Every disclosed recipe overlays **10–40% new on old** (OpenCoder 84/16, Zamba 60/40, Phi-4 70/30, Llama-3's probe 70/30), because *"a mismatch between mid-training and pretraining corpora can lead to catastrophic forgetting."* Spark Joy is the cautionary case: they held *filtered* web at 30% (0.82×) explicitly "to prevent a large distribution shift," and Language Understanding was **still negative at all four phase lengths** (−0.47 / −1.11 / −1.44 / −1.17 at 5 / 10 / 20 / 30% — these are the four *phase lengths*; the paper publishes no per-task breakdown within that category). Our anneal keeps web at **21.16%**, a **0.63× multiplier** — more aggressive than their 0.82% on filtered web, less than their 0.42× on total web. Inside the tested bracket, at the risky end; H4 tests it.

**Aggressiveness: our main→anneal shift is 17.64% (½·L1).** The course's own preset pair is **32.0%**, so this design is **45% gentler than the course preset** — and gentler than Spark Joy's 41.05%. ½·L1 is our construct, not a course metric, and it cannot see intra-lane quality shifts: the top-15% Indic quantile is invisible to it.

**Cyclic, not a tail block.** DD: *"if we only see long sequences toward the end of training, long sequence learning occurs only when the learning rate is too small."* Their `Grow-P2` improves with cycling (1 → 8 cycles, MDQA 25.9 → 28.0) but `Grow-P100` *degrades* (27.0 → 24.1), so cycling interacts with ramp aggressiveness and is not universally good. We cycle the reserve in **4 sub-cycles** and cycle long-context exposure through the whole main run — noting DD's mechanism concerns the main run's LR decay, not the interior of a leg where LR is already small.

---

## 5. The protected always-on floor

**Fixed at: Indic 5.5% and agentic 2.0% of trained tokens — per lane, 7.5% together. Enforced in every length bucket, every curriculum cycle, and in the anneal mixture.**

**Membership is corrected from earlier drafts.** Widget 3 marks `indic: scarce:true`, `agentic: scarce:true`, `reasoning: scarce:false`. Scoring each lane against the widget's English proxy `[0.70, 0.53, 0.33]`:

| Lane | Score |
|---|---|
| code | 0.841 |
| **reasoning** | **0.818** |
| web | 0.776 |
| agentic | 0.602 |
| indic | 0.567 |

Reasoning scores **third, above web** — at `keepFrac = 0.40` it is essentially never rejected. Including it would have been wrong twice: it needs no protection, and an **aggregate** 8% across three lanes is satisfiable with 8% reasoning and **zero agentic** — the exact starvation the floor exists to prevent. Hence per-lane numbers, and hence 7.5% rather than V4's 8%.

**The real-token clause is scoped to supply, because it is otherwise infeasible.** A floor demanding *real* tokens works for Indic and cannot work for agentic:

| Lane | Floor | Real tokens required | Real pool | Epochs | Verdict |
|---|---|---|---|---|---|
| Indic | 5.5% | 110.0B | 114B real (tiers A+B+C) | **0.96** | real clause **binds** |
| Agentic | 2.0% | 40.0B | **0.627B** | **63.8** | real clause **cannot bind** |

So: **Indic's floor is 5.5% of real tokens.** **Agentic's floor is 2.0% of lane tokens, of which the real component is the entire 627M pool at ≥4 epochs (2.508B = 0.125%), the balance being verified-generated.** For agentic the floor guarantees *presence in every cycle*, not real-token volume. Earlier drafts said "real tokens only" while also stating the lane is 94% generated — a direct contradiction, now resolved by scoping the clause.

Each remaining clause exists because a specific result shows what breaks without it.

| Clause | Evidence |
|---|---|
| **Hard** constraint, not a preference | CLIMB: the code cluster C20 goes to **exactly 0** under a reasoning-only objective — any lane absent from the objective dies |
| Lanes also in the selector objective | CLIMB Figs 5/7: different objectives, different winners |
| Per **bucket** and per **cycle** | DD Alg 1: *"If a bucket is empty, we exclude it from sampling"* — a scarce lane can vanish after one cycle. Our own measurement (§7) shows a global ≥256 bucket floor would discard **44.9%** of a short-document corpus |
| In the **anneal** too | Spark Joy's sans-math arm: a 100B final phase that stops feeding a lane drove MMLU to **29.71 vs 35.69 baseline (−5.98)** and Reading Comprehension to **26.48 vs 37.02 (−10.54)**. Confound: they held proportions while shrinking the pool, so the magnitude is inflated; the direction holds |
| A small floor suffices | OLMo 2 (via survey §III-C): *"not strictly necessary to have a large proportion of domain-specific data in the annealing mixture, just that domain-specific data is present"* |

**When does it bind?** Indic + agentic by stage is 18 / 19 / 17 / 17% and 29.4% in the anneal, so the aggregate is slack by 2.3–3.9× and **this floor never binds under this mixture**. It is a backstop against OPUS drift, not an active constraint; claiming otherwise would oversell it. The composer's per-lane floors (`indic ≥ 12`, `agentic ≥ 2`) *are* binding on the mixture, and both hold: 15.80 ≥ 12, 2.00 = 2.

OPUS and the curriculum act on orthogonal axes — *whether* a token is served versus *when* — so they compose. Preference Curriculum is the published instance of the *when* axis and has **no floor of any kind**, which is why this one is ours to add.

---

## 6. Curriculum

**Seed 200B → General 700B → Reasoning 600B → Long-context 500B**, then the **80B anneal**. Every row sums to 100.

| Stage | web | code | reason | long | indic | STEM | agentic | v-synth | Difficulty admitted |
|---|---|---|---|---|---|---|---|---|---|
| Seed (200B) | 54 | 13 | 2 | 1 | 16 | 12 | 2 | — | B0–B1 |
| General (700B) | 41 | 20 | 4 | 2 | 17 | 14 | 2 | — | B0–B2 |
| Reasoning (600B) | 27 | 28 | 13 | 3 | 15 | 12 | 2 | — | B0–B3 |
| Long-context (500B) | 24 | 29 | 12 | 11 | 15 | 7 | 2 | — | B0–B4 |
| **Anneal (80B)** | 21.2 | 23.0 | 9.1 | 2.8 | 21.9 | 9.2 | 7.5 | **5.5** | B0–B5 |

The anneal row carries the verified-synthetic column that §4 declares, so §4 and §6 agree at 100.00. The anneal's code / reasoning / STEM / agentic values are *derived* from the 62/38 construction, not independently chosen.

Order is load-bearing, with numbers: order alone at identical weights is worth **+1.74 absolute average** (52.86 vs 51.12 — Two-Phase Table 4; the frequently-quoted "+3.4" is that same gain expressed as a *relative* percentage) and it lands on sharp capabilities, GSM8K **30.86 → 40.33**, code **35.55 → 38.33**, with MMLU flat (56.49 → 56.28). CLIMB adds the shape rule: from-scratch mixtures stay broad (top-3 ≈ 64%) while continuous/late mixtures go peaky (one cluster at 43%), so our early stages spread and only the anneal concentrates.

### 6a. Difficulty bands — B0 to B5

Definitions are widget 7's `DIFF[]`. The **example** column is what the assignment requires and the widget does not supply.

| Band | Level | Definition | Concrete example | Lane |
|---|---|---|---|---|
| **B0** | Nursery | simple children's sentences | *"The cat sat on the mat. The mat was red."* | web |
| **B1** | Grade-school | basic grade-school text | *"Water boils at 100 °C at sea level."* + integer-answer word problems | web, Indic |
| **B2** | High-school | high-school level material | A Wikipedia article on photosynthesis; a 30-line Python script with one loop | web, code, Indic |
| **B3** | Undergraduate | undergraduate coursework | A GSM8K-style multi-step word problem; a single-file module with tests; an IndicGenBench summarisation pair | code, STEM, reasoning |
| **B4** | Graduate | graduate-level texts | An AIME problem with a worked solution; a SWE-Gym task with a repo checkout; a peS2o paper section | reasoning, STEM, agentic |
| **B5** | Research / PhD | research and PhD-grade papers | A GPQA-Diamond physics item; a proof-pile-2 formal proof; a full SWE-smith trajectory with recovery | reasoning, agentic, STEM |

**Monotone floor:** each stage admits its band *and everything below* — never a hard gate. Dropping low bands late is what produced Spark Joy's negative Language Understanding at every phase length. **B5 is reserve-only**, withheld from the main run and spent in the anneal — §4's reserve expressed on the difficulty axis.

**No paper supports a content-difficulty ladder, and one argues against it.** Preference Curriculum's Fig 9 shows its "hard" half needs *less* scientific content (0.61 vs 0.70) and *less* cultural background (0.59 vs 0.69), with logical-reasoning requirement **identical at 0.72 / 0.72**; Fig 6b puts 88% of arXiv in the *easy* half. **A perplexity gap is not a difficulty axis.** This ladder is built from source provenance and benchmark level — a labelling decision and a design bet. DD's ordering result is a **length** ladder, a different axis that can fight this one.

### 6b. Reasoning-length bands

Widget 7 is explicit that this is a second, independent schedule: *"alongside difficulty: short, medium, long and ultra traces are separate rungs. A hard problem with a short trace and an easy one with an ultra trace are not interchangeable, so trace length is scheduled too."*

All four bands solve the **same problem** — *how many integers in [1, 1000] are divisible by 3 or 5?* Answer **467**, correct at every band; only the solve rate changes. Token counts and rates are computed with widget 6's own tokenizer and curve `acc(L) = 0.955 − 0.615·exp(−L/τ)`, `τ = 0.18 · ultra_tokens`.

| Band | Steps | Trace tokens | Solve rate | First step of the worked example | Share | Tokens |
|---|---|---|---|---|---|---|
| **LOW** | 2 | **37** | **61.5%** | *"Inclusion-exclusion: floor(1000/3) + floor(1000/5) − floor(1000/15)."* | 15% | 4.26B |
| **MEDIUM** | 4 | **74** | **76.8%** | *"Count multiples of 3 up to 1000: floor(1000/3) = 333."* | 30% | 8.52B |
| **HIGH** | 6 | **161** | **90.9%** | *"Let A = multiples of 3 and B = multiples of 5 inside [1, 1000]."* | 35% | 9.94B |
| **ULTRA** | 14 | **346** | **95.3%** | *"Restate the goal… then verify two independent ways."* | 20% | 5.68B |

These partition the **28.4B trace budget** from §1.2, not the whole 170B lane. ULTRA's 5.68B against 4.6B of long-CoT inventory is **1.23×** — fundable.

**Why ULTRA is smallest.** Widget 6's curve gives ULTRA **+4.40 points** over HIGH (95.3 vs 90.9) for **2.15×** the tokens, tripping the widget's *"wasted effort"* flag at +5.0. HIGH takes the largest share because that is where the curve still buys accuracy per token.

**Why all four must exist.** The effort dial selects among behaviours the model was trained to produce: a model shown only long traces cannot answer briefly, and one shown only short traces has nothing to select when asked to think. Two-Phase moved GSM8K **30.86 → 40.33** with reasoning-shaped data at **1.3%** of its second phase, so a small well-placed slice suffices — 28.4B is not greedy. The 15/30/35/20 split is ours; only the ULTRA cap is course-derived.

### 6c. Packing, position, seams

- **Binary dataset decomposition, not concat-and-chunk.** Each document of length `l` splits into adjacent power-of-two spans; buckets hold single-document sequences, so no attention mask is needed and no tokens are wasted. Worth **+2.9 regular / +3.4 long-context average** (DD Table 5). Document masking is not a substitute: it lifts regular 51.5 → 52.4 but drops long-context 27.5 → 27.1 and craters MDQA-30 **20.5 → 16.0**.
- **All buckets for short-document lanes; the ≥256 variant only where documents are naturally long.** Our own measurement (§7) shows a global ≥256 floor discards **44.9%** of a short-document corpus — applied to Indic snippets, QA-format agentic data or parallel corpora that is precisely the per-bucket starvation §5 forbids.
- **RoPE base 100,000 from the start.** Free **+5.4 MDQA** on the baseline, +4.8 on the decomposed run, regular unchanged (DD Table 4, **1B only**; Table 4's 24.9 for DD≥256@100k conflicts with Table 2's 23.0 for the same configuration, so treat the magnitude as approximate).
- **Training sequence length is 8192.** The curated inventory is *32K+ packed*, so those sequences decompose into 8k spans. This plan claims **no** capability beyond 8k; a 32k–128k extension is a separate budget, out of scope.
- **Seams: 4 transitions × 20B blended = 80B, 4% of the main run.** Five stages have four boundaries.
- **The seam width is priced, not guessed.** Widget 8's model `peakFactor = 1 + effSharp·A·effFrozen` predicts, at a 20B band, **1.34× with frozen embeddings and 1.23× unfrozen**, against `RED_T = 3.0`; ~**6B** already clears it frozen. V4's ~150× corresponds to sharpness 1.0, frozen embeddings, zero band. Corroboration: DD Fig 8's un-ramped arm throws ~8 loss spikes to 7.5–8.1 while the ramped arm is spike-free — though those arms differ in both packing *and* curriculum, so it is not attributable to ordering alone.
- **Ramp, not step.** Preference Curriculum's winning S-shape blends over **43.9%** of its run and beats a hard switch by ~1.1 points — but that blends two halves of *one corpus*, not two mixtures, and 43.9% is 44× wider than our 1%-per-seam band. We take the shape, not the width. MiniMax-01 reportedly interpolates source weights linearly across transitions (primary **2501.08313**; this detail appears only in the survey's source comments, not its published text).

---

## 7. Proxy protocol

Cost basis (6ND): a 40B probe on 120B params ≈ **2.9e22** FLOPs against ≈**1.44e24** for the full run — **1/50 of a run**, so twelve probes cost ~24%. CLIMB's 112-run search is priced separately at ~45 GPU-h per 350M proxy. Branching follows Llama 3: a partially trained checkpoint, LR decayed linearly to 0 over the probe, candidate at **30% against 70% default**.

Spark Joy's own peaks are **0.60pp** (MMLU) and **0.86pp** (core average) at n=1, so every threshold is set outside that band.

| # | Hypothesis | Scale | Metric | Confirms | Refutes | Action on refute |
|---|---|---|---|---|---|---|
| **H1** | Long-context 4.45% + packing suffices | 1B, 100B, arms 0 / 2 / 4.45 / 9.4% | **MDQA-30** | 4.45% arm ≥ **90%** of the 9.4% arm | **< 75%** | raise curated lane to 9.4%, take from web |
| **H2** | Verified-generated agentic transfers | **3B**, 40B branch; format-only / +verified / +unverified | **SWE-bench Verified pass@1**, **BFCL AST-match** | verified arm ≥ **+3.0 pts** over format-only | **< +1.0 pt** | keep 2.00% share, swap generated for FIM-multiplied real + format (§3) |
| **H3** | Indic tier C survives 5.06× | 1B, 100B, arms C at 8 / 4 / 0% | **IndicGenBench chrF**, **MILU** | 8% arm within **1.0 pt** of the 4% arm on both | **> 1.0 pt below** on either | C → 4%, mass to D |
| **H4** | An 80B anneal beats 40B | 1B, branch at 96% / 98% | core average of MMLU + GSM8K + HumanEval | 80B ≥ **+1.0 pt** | **≤ 0 pt** | revert to 40B, bank the compute |
| **H4′** | Raising reasoning does not cost STEM | 1B, 100B, reasoning 8.5% vs 6.0% | **GPQA + MATH** | STEM loses **≤ 0.5 pt** | **> 1.0 pt** | return the 0.55pp to STEM |
| **H5** | Indic-up anneal avoids the MAP-Neo effect | 1B, anneal Indic 21.9 / 15.8 / 8.5% | **MILU + Flores-101 chrF**; **MMLU** as forgetting check | Indic ≥ **+1.5 pts**, MMLU loses **≤ 1.0 pt** | MMLU loses **> 1.0 pt** | flatten Indic across the anneal |
| **H6** | A 20B seam holds the Indic transition | 1B, gradient-norm trace, bands 0 / 5 / 20B, embeddings unfrozen | **peak gradient-norm multiplier** | peak **< 3.0×** (widget 8 `RED_T`) | **> 3.0×** | widen until it clears |
| **H7** | The four length bands give a controllable dial | 1B, 100B, 15/30/35/20 vs HIGH-only | **LOW:ULTRA trace-length ratio**, accuracy at each | ratio ≥ **4×**, ULTRA accuracy ≥ LOW | ratio **< 2×** | widen the band spread |

**A threshold caveat we must own.** H2's metric is the weakest link: SWE-bench Verified is near its noise floor at 3B, and Spark Joy chose 7B precisely so metrics sat above the floor. If the 3B arm cannot separate, H2 escalates to a 7B probe or falls back to BFCL AST-match alone, which is readable at smaller scale.

### What we actually ran

Full 1B/3B training is unavailable here, so H1–H7 are specified and unrun: this plan claims the **"highest"** tier — concrete proxies with named metrics and numeric thresholds — and explicitly not "very highest."

Two things were executed and are reproducible from this repository.

**(a) The mixture is executable arithmetic.** Stage profiles time-average to the declared shares within **0.05pp**; all rows sum to 100; every demand, ratio, tier repeat factor, reserve component, quantile, epoch count, the 17.64% shift and the 116.4B synthetic total are computed, not asserted.

**(b) A micro-replication of the packing claim the long-context decision rests on.** DD's average-context formula `Σl(l−1) / 2Σl` on a 342-document / 78,581-token corpus of our own papers and lecture notes:

| Arm | Sequences | Mean length | Avg in-document context |
|---|---|---|---|
| Original documents | 342 | 229.8 | 3486.5 |
| Concat-and-chunk @2048 | 380 | 206.8 | **421.1** |
| Decomposition, all buckets | 1,375 | 57.1 | 1917.6 |
| Decomposition ≥256 | 59 | 733.3 | **3452.5** |

Concat-and-chunk split **11.1%** of documents at a chunk boundary. The direction replicates — decomposition ≥256 carries **8.20×** the in-document context — but that **overshoots the published 1.45×** (1344 vs 930), because our corpus is short-document-heavy (median 104 tokens vs RefinedWeb's 598 mean) and the ≥256 filter **discards 44.9% of our tokens** where on RefinedWeb it is nearly free. The overshoot is the useful result: it produced the bucket policy in §6c. A first attempt used mean *span* length instead of average *context* and reproduced the effect backwards — recorded because it is why the metric definition matters.

---

## 8. Cleaning, aimed at the starved slots

The plan's own accounting names the starved slots on two independent definitions. **By the course's ≥8% funding rule:** agentic (2.00%), and long-context on lane share (4.45%, though its 17.7% effective ≥4k exposure clears the line). **By supply:** agentic **73.4×**, Indic tier C **5.06×**, long-CoT reasoning (5.68B ULTRA demand against 4.6B), code post-dedup **1.32×**, STEM **0.92×** with no headroom.

Cleaning is directed in that order:

1. **Agentic trajectories** — the only lane where new cleaned tokens change the plan's worst number. Every 100M real trajectory tokens cuts the generated fraction by ~2 points.
2. **Indic tier C** — separate the translated fraction of Sangraha's 162B set from the synthetic fraction. If it is separable, tier C's 12.6× premise dissolves and the course's 20% becomes fundable (§2).
3. **Long-CoT reasoning** — the 4.6B pool binds both the ULTRA band and the anneal reserve.
4. **Multi-document long-context** — nothing in the inventory is multi-document, yet MDQA is the metric. This slot needs data we do not have (§1.3).
5. **STEM** — 0.92× pre-selector, 2.29× post-selector; cleaned peS2o and proof-pile-2 tokens are directly load-bearing, and §1.1 takes 0.55pp out of this lane.
6. **Code, at file level** — the 32.9% retention ratio means cleaning changes the effective pool, not just the headline.

Web needs no cleaning attention: at 0.15× supply is not the constraint, and the marginal work there is *filtering*, not acquisition.

---

## 9. Where this plan has no evidence

- **No paper in the evidence base studied Indic.** The tier split is arithmetic against our inventory plus a ceiling borrowed from English rephrase experiments; the one quantitative low-resource precedent points the other way.
- **No paper trains agentic trajectories at pretraining scale.** "Agent" appears once in the mid-training survey, as a dataset name. The verifier argument is reasonable and **unmeasured**, and 2.00% is 5–16× outside the band our own citations support.
- **Long-context evidence stops at 8192**, and nothing we hold is multi-document while MDQA is the metric.
- **The anneal's value at 120B is unmeasured and the one frontier-scale measurement is null.** Annealing gave Llama 3 8B +24.0% GSM8K and +6.4% MATH but *"a negligible uplift for the 405B model."* Every large published mid-training gain is ≤14B.
- **Scale gaps we rely across.** Collapse's percentages come from an 8×256 char-level nanoGPT on one Shakespeare play; DD's RoPE and ordering results are 1B; OpenCoder's dedup is 1.5B Python; Demystifying is ≤3B English CC on CE loss only, and its "~30%" is interpolated from a grid that skips 30%.
- **Almost nothing has error bars.** CLIMB's checklist answers "No"; Spark Joy, Preference Curriculum and DD are single-seed. Spark Joy's MMLU peak is a 0.60pp gap. Cite curve shapes, not exact optima.
- **Eleven claims reach us through the mid-training survey rather than a primary.** Where a decision rests on one, the primary is named (MiniMax-01 2501.08313, Llama 3 2407.21783, MAP-Neo 2405.19327).

---

## 10. The numbers most likely to be wrong

| Number | Confidence | Why it might be wrong |
|---|---|---|
| **Agentic 2.00%** | **Low** | 73.4× gap, 94% generated, 5–16× outside our own band. H2 tests it; the fallback withdraws the capability claim, not the share |
| **Indic tier C 8% at 5.06×** | **Low-medium** | Rests on tier C = 5.0B, ignoring a possibly-separable translated fraction of the 162B set |
| **Long-context 4.45%** | **Low-medium** | Threshold proven and 0% catastrophic, but the 2–9% region is unmeasured *and* no inventory dataset is multi-document |
| **Reasoning 8.5%** | **Medium** | Forced by `WEIGHTED_MIN = 8`, but 92% of the lane is AON academic text; the trace pool is 7.1B, and the 0.95pp funding comes partly from a lane with no headroom |
| **Anneal 80B** | **Medium-high** | 3.85% of total matches OpenCoder exactly; weakened because Spark Joy's sweep is a cruising-LR swap, not a decay leg |
| **62% ballast / 0.63× web** | **Medium-high** | Inside the 10–40% overlay band; more aggressive on web than Spark Joy's 0.82× |
| **Floor 5.5% / 2.0%** | **High** | Membership matches widget 3's `scarce` set; real-token clause scoped to feasibility. Caveat: never binds under this mixture |
| **Bands B0–B5 and LOW–ULTRA** | **Medium** | Definitions and the ULTRA cap are course-derived; the ladder itself has no paper support and the 15/30/35/20 split is ours |
| **Decomposition + RoPE 100k** | **High** | Measured, cheap, confirmed in our own micro-replication — at a magnitude we could not reproduce |

**Attack first: agentic 2.00%, Indic tier C, the reasoning lane's 7.1B trace pool, and the absence of any multi-document data behind an MDQA claim.**
