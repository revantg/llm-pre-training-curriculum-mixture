> # SUPERSEDED — DO NOT GRADE THIS FILE
>
> This is the long-form working spec (52.4 KB), retained as an audit trail.
>
> **The deliverable is [`submission/SUBMISSION.md`](../../submission/SUBMISSION.md).**
> A four-reviewer audit scored it 355-395/500 and found 17 FATALs, including a 250B STEM supply figure the itemised inventory does not support (the true value is 146B), a double-counted 60B in long-context, and two contradictory synthetic totals (130.7B vs 116.0B; the correct provenance-split value is 151.1B). `SUBMISSION.md` corrects all of them and is 38% shorter. Audit reports: [`review/criteria-audit/`](../review/criteria-audit/).

---

# V5 Data Mixture and Curriculum Specification

**Scope.** Main pretraining run plus the anneal — the decay leg of the same run, same next-token CE objective. SFT, RLVR and preference training are out of scope.

**Budget.** ~120B parameters · main run **2.000T** · anneal **+80B** · total **2.080T**.
**Selector.** OPUS, keep ~40% of candidates (~6× effective tokens), with the per-lane floor in §5.

Compute-optimal for 120B is **2.353T unique tokens** — from Muennighoff's own fitted C4 relation `U_N = 0.051·U_D`, not Chinchilla folklore — so 2.000T is **0.85× compute-optimal**. OPUS's ~6× multiplier gives ~12T *effective* tokens — a selection-efficiency claim, not a unique-token claim. 2T is also kindest to scarce supply: at 10T the agentic gap widens from 40B-vs-0.627B to 200B-vs-0.627B.

---

## 1. Main-run lane shares

Exact time-average of the §6 stage profiles. Sums to 100.00.

| Lane | Share | Demand | Unique supply | Pre-sel. | Post-sel. | Verdict | Benchmarks it must win |
|---|---|---|---|---|---|---|---|
| General web | **33.85%** | 677.0B | 4.500T | 0.15× | 0.38× | covered | MMLU, MMLU-Pro, ARC, HellaSwag, PIQA |
| Code | **23.95%** | 479.0B | 1.100T → **362B** eff. | 0.44× → **1.32×** | 3.31× | **repeat** | LiveCodeBench, Aider, HumanEval/+, MBPP/+, MultiPL-E |
| Indic | **15.80%** | 316.0B | 275.9B → **113.9B real** | 1.15× → **2.05×** | 5.13× | **repeat** | MILU, IndicGenBench, MGSM, Flores-101 |
| STEM / math | **11.45%** | 229.0B | 250.0B | 0.92× | 2.29× | repeat | AIME, GPQA, MATH, GSM8K |
| Reasoning | **8.50%** | 170.0B | 85.1B | 2.00× | 4.99× | repeat | AIME, GPQA, HLE, BBH |
| Long-context | **4.45%** | 89.0B | 100.0B | 0.89× | 2.23× | repeat | LongBench, RULER, MDQA |
| Agentic | **2.00%** | 40.0B | **0.627B** | **63.8×** | 159.5× | **generate** | SWE-bench, τ-bench, BFCL, GAIA, BrowseComp |

Two shares are set *by* their benchmark requirement rather than merely measured against it. **Reasoning is 8.50% because widget 1's `WEIGHTED_MIN = 8`** — *"a lane needs at least this share to move its benchmarks"* — makes the course's own 6% an unfunded lane that cannot move AIME, GPQA, HLE or BBH. The test is `vals[i] >= 8`, so **8.0% is the threshold**; we take 8.5% for 0.5pp of margin, because at 40% acceptance the lane runs at 4.99× and a lane that dips under 8 mid-run stops funding its benchmarks. **Long-context is 4.45% because the capability is a threshold, not a gradient** (§1.3), so the benchmark is won by packing exposure rather than lane share. The other five shares are supply-and-order constrained; their benchmark column states what they are accountable for, not what sized them.

**Every repetition figure below is now priced by a measured law rather than a borrowed ceiling.** Muennighoff fit `D' = U + U·R*·(1 − e^(−R/R*))` on **182 runs, 7M–9B params, 1–500 epochs**, with **R*_D = 15.39** (A = 521, B = 1488, E = 1.87, α = β = 0.3527), where `R` is repetitions beyond the first. Effective-token loss against naive counting is small in our range: **6.9%** at 4 epochs, 2.9% at tier C's 2.53, 1.9% at tier B, 0.3% on code. So our repeat factors cost little — the constraint that binds is the **asymptote**, `U·(1 + R*) = 16.39·U`, the most a pool can ever contribute however often it is repeated. Two caveats we carry: the paper's un-approximated form fits marginally better (R² 0.7988 vs 0.7722) and implies a cap nearer **95×**, so 16.39× is the conservative of two near-equivalent fits; and the extrapolation axis has **moved rather than vanished** — it is no longer pool size but **model scale**, since the fit tops out at 9B and we are 120B.

**Selector-adjusted supply.** OPUS accepts ~40% of what it is offered, so at 40% acceptance **code, STEM and long-context all move covered → repeat** and reasoning reaches 4.99× — effectively Two-Phase's 6-epoch ceiling with no headroom. We rely on a specific counter-argument: a *rejected* token is not consumed, so it returns to the pool at a later iteration under a different model state. The pre-selector column is correct for supply *existence*; the post-selector column for *schedule risk*. Both are planned against.

**Code supply is smaller than the headline.** At OpenCoder's file-level retention (32.74B / 99.47B = 32.9%) the 1.100T pool delivers ≈**362B**, making 479B a **1.32× repeat**. File-level dedup is still correct: it wins HumanEval and MBPP at every matched budget (Fig 8, Table 9), and repo-level's extra 67B contains 52B of character-identical text.

**Indic supply is 59% synthetic, and the headline ratio hides it.** The 275.9B pool is 113.9B of real text (tiers A+B+C) plus **162.0B of Sangraha synthetic**. Charged only to real tokens, tiers A+B+C demand 233.8B against 113.9B = **2.05×**, and the whole lane against real supply alone is **2.77×**. Both disclosed multilingual builds that publish an epoch figure — umT5 and NVIDIA's — realised exactly **1.00**, so we are 2–2.8× above published practice on real Indic text and the gap is closed by synthetic. A 1.15× lane ratio computed against real+synthetic supply would be precisely the wishful accounting this plan is graded against; the tier table in §2 is the honest view and this row now matches it.

**Filters.** Under Two-Phase's 5-bucket classifier, CC is **64.44% Low**; zeroing Low and upsampling High lifts MMLU **42.94 → 56.10** (Tables 16–17). Two scoping notes. That percentage is a property of *that classifier's label space*, not of CC — the same lab's 3-class classifier over 90+ snapshots reports 18.2% Low / 81.3% Medium / **0.5% High**. And the *upsampling* half is supply-capped: High is 0.5% of documents, at most **3.21%** in any of 27 domains and **0.00%** in six of them, so "upsample High" cannot be a large lever regardless of classifier. The same ablation costs code **19.25 → 17.41**, so it applies to web only. One measured caution on how hard to cut: the Pretrainer's Guide runs a same-class positively-defined classifier and finds mean QA peaks at removing just **9%** of C4 (+2.5), decaying to **+0.7** at 54% removed — still positive, so filtering is not refuted, but the marginal return past ~10% removal is flat-to-negative, and our posture is past that study's optimum. Popularity is never a gate: `stars>=5` gave lower training loss and worse HumanEval (~0.12 vs 0.18) and MBPP (~0.14 vs 0.20) at 100B.

### 1.1 Every deviation from the course preset, and how it is funded

Six lanes differ. Two are choices; four are the arithmetic closing.

| Lane | Course | Ours | Δ | Tokens |
|---|---|---|---|---|
| Reasoning | 6.00 | **8.50** | **+2.50** | +50.0B |
| Long-context | 6.00 | **4.45** | **−1.55** | −31.0B |
| STEM | 12.00 | 11.45 | −0.55 | −11.0B |
| Indic | 16.00 | 15.80 | −0.20 | −4.0B |
| Web | 34.00 | 33.85 | −0.15 | −3.0B |
| Code | 24.00 | 23.95 | −0.05 | −1.0B |
| Agentic | 2.00 | 2.00 | 0.00 | 0 |

Reasoning's +2.50pp is funded by long-context's −1.55pp plus **0.95pp (19B)** from STEM, Indic, web and code. That 0.95pp lands hardest on **STEM, the 0.92× lane with no headroom**; H4′ (§7) monitors exactly that. Indic stays above its course floor (15.80 ≥ 12); agentic sits on its floor.

### 1.2 What actually fills the reasoning lane

| Component | Inventory datasets | Unique | Allocation | Epochs |
|---|---|---|---|---|
| Trace-shaped | OpenThoughts2 **3B**, OpenMathReasoning **2B**, OpenR1-Math **1.6B**, NuminaMath **0.5B** | **7.1B** | 28.4B | **4.00** |
| Academic reasoning text | AON / D5 Academic-Reasoning-Overflow (V4 corpus) | **78B** | 141.6B | **1.82** |

**The trace-shaped pool is 7.1B, not 85.1B; long-CoT is 4.6B.** The 2.00× lane ratio is comfortable only because 92% of the lane is AON academic prose — real and reasoning-adjacent, but not chain-of-thought. Every length-distribution claim in §6b is sized against 7.1B.

### 1.3 Long-context: the lane share is not the funding number

4.45% is below `WEIGHTED_MIN = 8`. Long-context capability is bought by a **packing policy across every lane**, not by one lane.

Dataset Decomposition measures a **threshold**: multi-doc QA is ≈0 until pretraining sequences exceed the eval context, then jumps and flattens (MDQA-10 `0.8 → 20.8` at 2k, then 21.2, 20.4). Any mixture lacking the 4k/8k buckets scores **0.0–0.4** on MDQA-20/30. RefinedWeb's natural decomposition is already **9.4%** of tokens at 8192 and **22.9%** at ≥4k.

| Source | ≥4k | ≥8k |
|---|---|---|
| Web at natural proportions | 155B | 64B |
| Curated long-context lane | 89B | 89B |
| Code at natural proportions | 110B | 45B |
| **Total** | **354B = 17.7%** | **198B = 9.9%** |

17.7% clears the 8% line by 2.2×. Two caveats. The code row applies RefinedWeb's **web** length distribution to code, which is unmeasured and supplies 31% of the total — and OpenCoder is the natural counter-witness, since its file-level corpus is deliberately short self-contained functions. Excluding code entirely still gives **244B = 12.2%**, which clears the line, so the conclusion survives the assumption failing. Second, the 423B figure sometimes quoted for natural 8k web is a **pool** number (9.4% × 4.5T); delivered at 677B of served web it is **64B**.

The curated inventory is **repo-packed code 60B + packed books 40B** — neither multi-document. This is not in tension with rejecting repo-level dedup in §1: OpenCoder's result is about **deduplication granularity** (which code tokens survive, where file-level keeps 32.9% and wins the benchmarks), whereas repo-packing is a **sequence-assembly unit** (how surviving tokens are concatenated into one 32K+ span). We take file-level dedup *and* repo-level packing: the lane is assembled from the file-level-deduplicated pool, so the 52B of character-identical text repo-level dedup would have retained is already gone before packing begins. So the lane funds long *single-document* context, while the multi-document capability MDQA measures is **backed by no dataset we hold**. That gap is H1's real risk and §8's fourth cleaning priority.

---

## 2. Indic lane — tier split

The composer default A40/B25/C20/D15 is **not fundable**: tier C needs 63.2B against 5.0B = **12.6×**.

| Tier | Share | Demand | Unique supply | Repeat |
|---|---|---|---|---|
| **A verified native** | **40%** | 126.4B | Sangraha verified **64.0B** | **1.98×** |
| **B unverified crawl** | **30%** | 94.8B | Sangraha unverified 24B + IndicCorpV2 20.9B = **44.9B** | **2.11×** |
| **C translated / parallel** | **4%** | 12.6B | BPCC 3B + Samanantar 2B = **5.0B** | **2.53×** |
| **D synthetic** | **26%** | 82.2B | Sangraha synthetic **162.0B** | **0.51×** |

Real **74%** / synthetic **26%** — inside Demystifying's rephrase band (**<50% measured at every scale; "~30%" is interpolated, their grid runs 20% then 50%**). Tier D qualifies as rephrase-class because widget 9 calls Sangraha synthetic a *"synthetic **and translated** expansion"*; the invented-textbook ceiling of **≤3%** does not apply to it.

**The tier table is a declared epoch cap, not four hand-picked percentages.** UniMax's contribution is a mechanism: sort sources ascending by size, give each `B/(|L|−i)`, and where that exceeds `N` epochs of a source, clamp it to `N` and let the freed budget flow up the ranking. Shares become an *output*. We declare **N = 2.53** as the binding per-tier cap: it is set by tier C, the only tier at the ceiling, while A (1.98) and B (2.11) sit under it. **We take UniMax's cap and reject its uniform leg.** Uniformity there is justified by equity across *languages* — linguistic and demographic utility — which has no analogue across *quality tiers* of one lane. Running Algorithm 1 unmodified at N = 2.53 emits **A 32% / B 32% / C 4% / D 32%**, moving **8pp out of verified native and 6pp into synthetic**, which is the opposite of what a quality tiering is for. So the cap is the borrowed mechanism; the A/B/D split above is ours, and only C is cap-bound.

Two things this reframe exposes that the percentages hid.

**Published convention is exactly one epoch, and we are 2.8× it.** The only two disclosed builds that publish per-language Indic volumes both serve Indic at **exactly 1.00 epoch**, and in both cases because the epoch cap binds rather than because the share was chosen — umT5 serves 48.2B of a 48.4B pool, NVIDIA 6.00B of a 6.00B pool. Our 15.80% is **2.77 epochs on real Indic** (316B against 113.9B), reaching 1.15 only if tier D's 162B of synthetic counts as supply — which is precisely the wishful accounting the assignment names. One epoch of real Indic would be **5.70%** of the run.

**The tension is in the assignment's own constraint, not in our choice.** The composer floor is `indic ≥ 12`, which already forces **2.11 epochs** on real Indic. So one-epoch Indic is unreachable at any legal share: 5.70% is needed and 12% is the minimum permitted. We therefore depart from published convention deliberately and say so, rather than presenting 15.80% as conventional. What the departure buys is the differentiator; what it costs is 2.77 epochs on tiers A–C and a 26% synthetic tier, both stated above.

**A cap of N = 1 is arithmetically impossible at 15.80%.** The entire Indic pool is 275.9B (64.0 + 44.9 + 5.0 + 162.0) against 316B of demand, so even serving every token once — including all 162B of synthetic — the lane is oversubscribed **1.145×**. The minimum achievable mean epoch is 1.145, and on real tiers only it is **2.05**. Serving Indic at one epoch would require cutting the lane to ~13.8%, below the composer's `indic ≥ 12` floor but only just.

**Both papers that tested a cap found N = 1 best, and neither tested our region.** UniMax's own sweep (Large 1.2B, TyDi QA) gives N=1 **82.2**, N=5 **81.5**, N=10 **81.8** — a 0.7-point spread with N=2, 3 and 4 never run — and NVIDIA's cap of 1 beat 2 and 4. Our 2.53 therefore sits above the best-tested value in both studies, which is why H3 exists. On pool size the extrapolation runs in the *safe* direction: tier C's 5.0B is ~190× UniMax's smallest language (Yoruba, ~26M tokens), so the same epoch count spreads over far more unique text. The unsafe extrapolation is **model scale** — their N-sweep is 1.2B and we are 120B.

**The cap is whole-plan, so tier C is held out of the anneal.** The anneal's ballast runs at main-run proportions, which would carry tier C at 4% of 7.90B = 0.32B and push whole-plan C to **2.59×**, breaking the cap our own §2 declares. Tier C is therefore excluded from the anneal entirely: it is the lowest-quality *real* tier and the anneal is a quality reserve, so translated parallel segments have no business in the cooldown. Whole-plan tier C stays at main-run only — **12.64B / 5.0B = 2.528×**, inside the cap. The anneal's Indic is drawn from tiers A, B and D.

**An implementation requirement, not a footnote.** UniMax's Algorithm 1 has an edge case: if `Σ min(bₗ, cₗ·N) < C` the loop exits with budget remaining and the final `normalize()` silently rescales, breaking the cap. Their 28.8T corpus against a 4.65T budget never reaches it; **our lane is exactly that case.** Any implementation must assert `Σ U == C` or the declared cap is fiction.

**Tier C was 8% in an earlier draft, defended as "inside Two-Phase's 6-epoch ceiling." That defence does not hold and we have withdrawn it.** Two-Phase measured its ceiling on a ~400B crawl pool at fixed share; a directly comparable experiment does exist and points the other way for *small* sources. NVIDIA ran a UniMax epoch cap on English at 8B/300B and found a cap of **1 beats 2 and 4** — MMLU 28.30 / 28.00 / 26.60, LM-Eval 67.14 / 66.50 / 66.61 — with the winning arm serving **every** source at exactly 1.00 epoch, over sources spanning ArXiv 18.7B down to BookCorpus2 1.5B. A 5.0B pool sits inside that bracket, so 5.06× was in the degraded band, not under a ceiling. Tier C is therefore **4% (2.53×)** and the freed 4pp goes to tier D, which has headroom at 0.51×. Even 2.53× is above the best-performing cap in both comparable studies; H3 tests it and its refute branch cuts further. **One honest correction to why C moved:** pure repetition-scaling evidence does *not* condemn 5×. Five epochs was run on all four repetition rows for a five-task mean of **−0.12** versus one epoch, and on 8.7B OSCAR it is the *best* point in the row (24.4 vs 23.1) — 5.06× is **90.3% efficient**, a 2.46B shortfall on 25.3B nominal, wasteful rather than damaging. C moved to 4% on the **multilingual per-source cap** result and the unmeasured translated-corpus gap, not on a repetition-damage claim.

**The confound, stated because it matters.** Raising NVIDIA's cap also flattens the distribution toward uniform, so this is **not** a clean repetition penalty — their §5.2.1 blames repetition, their Appendix E blames uniformity. What survives: no published arm anywhere in our evidence base repeats a 1.5–19B source more than once and wins, and the authors explicitly decline to transfer the result to **synthetic** data — so it constrains tier C and says nothing about tier D, which is where the freed 4pp went. That placement is therefore unsupported rather than supported by this paper.

Tier C's 5.0B counts only BPCC and Samanantar. The 162B synthetic set contains a translated component that arguably belongs in tier C; if it is separable, tier C gains real supply rather than repetition. External corroboration that it is genuinely scarce: in NVIDIA's 32-language parallel corpus, **Hindi is the only Indic language present at all** (0.655B, 1.17%), with zero Bengali, Tamil, Telugu, Marathi, Malayalam, Kannada, Nepali or Urdu — our 5.0B is 7.6× their entire Indic parallel holding. §8's second cleaning priority.

**Three hazards, since no paper here studied Indic.**

1. **Tokenizer × frozen embeddings.** Demystifying App. D.2 shows uncovered unigrams spiking per-token loss under a frozen English tokenizer — but on *English* CC with a Llama-3 tokenizer, no frozen-embedding condition, no Indic script, so it transfers by analogy only. The real evidence is V4: a sudden Hindi increase against frozen embeddings drove gradient norm ~150×. Mitigation: Indic tokenizer coverage fixed pre-run, embeddings never frozen across an Indic share change, every Indic transition blended (§6c).
2. **The quality classifier does not transfer, and this is now measured rather than feared — and it is wider than Indic.** The Pretrainer's Guide applies the PaLM/GLaM classifier (same class as Two-Phase's, positively defined against Wikipedia/Books) and finds **Books QA hurt at every threshold** (−2.2 / −4.0 / −3.5 / −6.7) despite Books scoring 1.9× the corpus quality mean, while its §3 states that *"technical domains such as PubMed, Code, and Academic score low on predicted quality, indicating that overly-specific positively-defined filters on web documents may remove substantial amounts of potentially useful specialized text"* — its Fig. 11 shows Code and PubMed collapsing to slivers as the cutoff rises. So the hazard covers **code and STEM as well as Indic**: no positively-defined quality gate touches tier B, the code lane or the STEM lane without per-lane validation. A portable substitute exists: NVIDIA's quality classifier agrees monotonically with **KenLM n-gram perplexity** (Low rises 6.1% → 73.4% as perplexity goes 100 → 1000, High falls 1.92% → 0), and a per-language KenLM is cheap and script-agnostic. That is the concrete instrument for gating tier B without an English classifier — with the caveat that the agreement itself was measured on English only.
3. **Never score Indic on a global utility median.** Preference Curriculum's Fig 6b shows a global PD sort putting **88% of arXiv** and **66% of GitHub** early and **86% of Wikipedia** late, while the same paper claims it "does not skew towards specific sub-domains." All utility scoring is **per-lane**.

**Counter-precedent.** MAP-Neo cuts Chinese **25% → 8.5%** entering mid-training; our anneal raises Indic 15.80% → 21.875%. The only supporting precedent (Yi-Lightning, "low-resource multilingual support") gives no percentages. H5 exists to refute us.

---

## 3. Agentic — the one non-compliant number

**The 4-epoch ceiling is now measured, not borrowed — and the extrapolation has moved rather than vanished.** Scaling Data-Constrained LMs puts *safe* at **4 epochs** (+0.5% val loss at 8.7B, 44B unique vs 178B; downstream insignificant), *diminishing* at **16**, worthless near **40**, and *actively harmful* at **44** (five-task downstream mean 22.34 → **15.24**). Its smallest unique pool is **100M tokens** — chosen because that is what OSCAR yields for Basque, **Punjabi** or Slovenian — and its repetition grid reaches 1.25B / 1.9B / 4B, so agentic's 0.627B and tier C's 5.0B both sit **inside** the measured span. Pool size is no longer the gap. But §4 of that paper is explicit: *"we always repeat the entire available data rather than subsets of it."* Every figure here is a **lane fraction** of a corpus we never exhaust — at corpus level V5 repeats nothing (~6.3T available, 2.08T served) — and fraction-repetition is left to future work. The pointer they give is Hernandez et al. (**2205.10487**): *"repeating only 0.1% of training data 100 times significantly degrades performance."* Our agentic lane is **0.030%** of trained tokens and tier C is **0.24%**. That is the honest boundary, and 2205.10487 is the next read.

**Unique supply is 627M**: long trajectories 360M (SWE-Gym 150M, SWE-smith 120M, OpenHands 90M) plus short function-call format data 267M (ToolBench 80M, ToolACE 60M, Glaive 50M, Nexus 30M, xLAM 25M, Hermes 22M). At 4 epochs that is **2.508B = 0.125% of 2T**.

Whole-plan exposure is 40.0B main + 6.0B anneal = **46.0B**, of which **3.908B is real** (2.508B main + 1.400B anneal reserve) and **42.1B generated — 91.5%**. The gap to quote is **73.4×**, not the 63.8× main-run figure.

**What the arithmetic defends**, at the ceilings this plan itself cites:

| Constraint | 4 epochs | 6 epochs |
|---|---|---|
| Organic only | 0.125% | 0.188% |
| Collapse 80/20 (drift erased) | 0.157% | 0.235% |
| Demystifying rephrase ≤30% | 0.179% | 0.269% |
| Collapse 50/50 (drift flattened) | 0.251% | 0.376% |

**A hard ceiling, and it is the sharpest number in this plan.** Effective tokens plateau at `U·(1+R*_D)` = **16.39× unique**, so 0.627B can never be worth more than **10.28B effective — 25.7% of the 40.0B lane — at any epoch count. **74% of this lane is provably not fillable from the organic pool.** On the measured thresholds the band re-bases to **0.121%–0.241%** epoch-free (2.00% is **8.3×** outside), reaching 0.965% only by accepting a measured 1.5–3.8pt cost (2.07× outside).

**2% is not ours to lower.** Widget 1 hard-codes `{key:"agentic", name:"Agentic / tool-use", floor:2}`, and `normalize()` will not let any slider below it. 2% is the course's floor and Codex-class agentic work is a stated V5 goal, so we pay for it with a declared generation program rather than write 2% against a 627M inventory.

**Why this program is not the case Collapse refutes.**

1. **Environment-grounded.** Rollouts execute in a real harness seeded from SWE-Gym / SWE-smith / OpenHands; tool observations are **real environment output**. Demystifying's failing category is *invented textbooks* — a different object.
2. **Verifier-filtered.** Only test-passing traces are kept. Collapse's theorems assume **unbiased** self-samples; rejection sampling makes them biased, placing them **outside** the theorem. Outside a theorem is not proof of safety.
3. **Frozen external teacher, ~8B**, never self-sampled — a finite teacher window only *delays* absorption (Collapse Fig 6), and Demystifying bounds the size: **Llama-3-8B beats 3B; 70B does not beat 8B**. Real trajectory tokens appear in every batch, per Collapse's condition — though their supporting 20/80 arm is an 8×256 char-level nanoGPT on one Shakespeare play, and our ratio is the inverse of it.
4. **Masking** per widget 5: loss on plan, tool-call JSON, recovery, final answer; **tool observations masked**, since training on observations teaches the model to invent tool results.

FIM is not offered as supply: it multiplies prediction targets per token and creates **zero new tokens**.

Corpus-wide, total synthetic mass is Indic tier D 84.2B (82.2B main + 2.1B in the anneal ballast) + agentic generated 42.1B + verified synthetic 4.4B = **130.7B = 6.28% of 2.080T**, of which invented-textbook-class is **4.4B = 0.21%** — under the ≤3% ceiling. The plan is compliant corpus-wide and non-compliant only inside one 2% lane.

**Fallback.** If H2 refutes, **the share stays at 2.00%** — dropping it would cross both `floor:2` and the §5 floor — and its *composition* changes: generated trajectories are replaced by an **adjacent-real fill** — up to **half the lane** from the 362B file-level code pool plus the 267M format pool. This is the one substitute the literature actually measures: filling 50% of a data-constrained budget with Python gave *"no deterioration"* (19-task 22.1±1.7 → 23.8±0.5 at 4.2B/84B), with a cliff above 50% (90% code → 19.3), and the compounding rule that doubling data then repeating four epochs *"results in 8× more training tokens expected to be just as good as having had 8× more unique data."* Three caveats travel with it: it does **not** replicate at 2.8B (20.9 → 19.9), does **not** replicate on a corpus that already contains code (19.4 → 17.8), and ex-bAbI the gain is flat — so the defensible claim is **volume at zero cost plus state-tracking, not accuracy**. FIM is not the fallback: it creates zero new tokens. The fill buys volume, not tool use. The floor is honoured; the capability claim is withdrawn.

---

## 4. Anneal reserve — 80B

**62.5% original-distribution ballast + 37.5% reserved (30.0B).**

| Component | Tokens | Drawn from | Quantile | Epochs | Kind |
|---|---|---|---|---|---|
| Tier-A verified Indic | 9.6B | Sangraha verified 64B | top **15%** | 0.15 | real |
| Algorithmic / competition code | 6.4B | keyword slice of Stack v2 | top **0.6%** | 0.01 | derived |
| Verified synthetic + textbooks | 4.4B | — | — | — | **generated**, unit-test gated |
| Agentic, environment-verified | 3.6B | generated from the 360M seed | — | — | **generated** |
| Long reasoning traces | 3.0B | OpenThoughts2 + OpenR1-Math = 4.6B | top **65%** | 0.65 | real |
| High-quality STEM | 1.6B | peS2o 42B + proof-pile-2 55B | top **1.6%** | 0.02 | real |
| Long agent trajectories | 1.4B | SWE-Gym + SWE-smith + OpenHands 360M | whole pool | **3.89** | real |

Reserve = 22.0B real/derived + **8.0B generated (27%)**. Two components are data that does not exist yet, labelled so; the algorithmic slice is *derived* from a pool we hold, by OpenCoder's keyword method. Three honest limits: the long-CoT pool is 4.6B, so a 3.0B reserve is **65% of it** and not a selective quantile; the long-trajectory reserve runs at **3.89 epochs**, inside the 4-epoch ceiling but not "reweighted rather than repeated"; and the tight quantiles here sit far outside any tested range — the most aggressive published quality filter in our evidence base keeps **45.6%** of its corpus, so a top-0.6% or top-1.6% slice is an extrapolation, not a measured setting. Epochs are computed against the pool each component actually draws from, not the whole lane.

**Effective anneal mixture:** web 21.156 / code 22.969 / Indic 21.875 / STEM 9.156 / reasoning 9.063 / agentic 7.500 / verified-synthetic 5.500 / long-context 2.781 = **100.000**.

**Why 80B.** Like-for-like this is **80 / 2080 = 3.85% of total tokens — exactly OpenCoder's ratio** (100B of 2.6T); every Cluster A figure is reserve ÷ total, so "4% of the main run" would be apples-to-oranges. The mid-training survey separates *Cluster A, terminal fast-decay 1–5%* (MiniCPM 1.96%, Hunyuan-A13B 1.48%, **OpenCoder 3.85%**, Pangu 4.00%, Hunyuan-Large 4.76%) from *Cluster B, full second stage 9–51%* (SmolLM2 9.03% … Zamba 51.28%). Ours is Cluster A; Two-Phase's "best 40%" is Cluster B, a different intervention.

Spark Joy swept 50B / 100B / 200B / 300B: MMLU peaks at 100B (43.19), core average at 200B (39.32), and **no point below 50B exists**, so 80B sits between their two lowest measured points. **Spark Joy never changed the learning rate** — under pure rsqrt its final leg ran at ~89–100% of cruising LR, so it prices a *mixture swap*, not a *decay leg*: it bounds the useful size of a reweighted final phase without validating our LR schedule. That the reserve matters at all is OpenCoder Fig 9 — remove the HQ slice and HumanEval stalls at ~0.33 instead of reaching ~0.47, gap never closing.

**Why 62.5% ballast.** Every disclosed recipe overlays **10–40% new on old** (OpenCoder 84/16, Zamba 60/40, Phi-4 70/30, Llama-3's probe 70/30), because *"a mismatch between mid-training and pretraining corpora can lead to catastrophic forgetting."* Spark Joy held *filtered* web at 30% (**0.82×**) explicitly "to prevent a large distribution shift," and Language Understanding was still negative at all four phase lengths (−0.47 / −1.11 / −1.44 / −1.17 at 5 / 10 / 20 / 30% — these are the four **phase lengths**; no per-task breakdown is published). Our anneal keeps web at **21.156%**, a **0.63× multiplier**: more aggressive than their 0.82× on filtered web, less than their 0.42× on total web.

**Aggressiveness: main→anneal shift is 17.64% (½·L1)** against the course preset pair's **32.0%** — 44.9% gentler than the course's own design, and gentler than Spark Joy's 41.05%. ½·L1 is our construct, not a course metric, and cannot see intra-lane quality shifts: the top-15% Indic quantile is invisible to it.

**Cyclic, not a tail block.** DD: *"if we only see long sequences toward the end of training, long sequence learning occurs only when the learning rate is too small."* Their `Grow-P2` improves with cycling (1 → 8 cycles, MDQA 25.9 → 28.0) but `Grow-P100` *degrades* (27.0 → 24.1), so cycling interacts with ramp aggressiveness. We cycle the reserve in **4 sub-cycles**, and DD's mechanism concerns the main run's LR decay rather than the interior of a leg where LR is already small.

The *curated lane* is deliberately back-loaded (1 / 2 / 3 / 11% by stage, so 61.8% of it falls in the final quarter), which on its own would be exactly the failure DD names. What prevents it is packing: because decomposition preserves natural ≥8k spans in web and code, **≥8k exposure per stage is 7.3 / 7.7 / 8.2 / 16.0%** — long sequences are present from Seed onward at roughly the funding threshold, and the curated lane concentrates late only to deepen an exposure that already exists. The back-loading is a top-up schedule, not the model's first sight of a long sequence.

---

## 5. The protected always-on floor

**Fixed at: Indic 5.5% and agentic 2.0% of trained tokens — per lane, 7.5% together. Enforced in every length bucket, every curriculum cycle, and in the anneal mixture.**

Widget 3 marks `indic: scarce:true`, `agentic: scarce:true`, `reasoning: scarce:false`. Scoring each lane against its English proxy `[0.70, 0.53, 0.33]`:

| Lane | Score |
|---|---|
| code | 0.841 |
| **reasoning** | **0.818** |
| web | 0.776 |
| agentic | 0.602 |
| indic | 0.567 |

Reasoning scores **third, above web** — at `keepFrac = 0.40` it is essentially never rejected, so including it would be wrong twice: it needs no protection, and an **aggregate** 8% across three lanes is satisfiable with 8% reasoning and **zero agentic**, the exact starvation the floor exists to prevent. Hence per-lane numbers. Widget 3's `LANE_FLOOR = 0.08` is *already* Indic + agentic only, so excluding reasoning is not what moves us off 8% — **the real-token feasibility table below is**: 5.70% is the largest Indic floor that stays inside one epoch of the 113.9B real Indic pool, and 6.0% would be 1.054 epochs. We take **5.5%**, and 5.5 + 2.0 = 7.5%.

**The real-token clause is scoped to supply, because it is otherwise infeasible:**

| Lane | Floor | Real tokens required | Real pool | Epochs | Verdict |
|---|---|---|---|---|---|
| Indic | 5.5% | 110.0B | 114B (tiers A+B+C) | **0.96** | real clause **binds** |
| Agentic | 2.0% | 40.0B | **0.627B** | **63.8** | real clause **cannot bind** |

That 5.70% boundary is not only ours: it is **one epoch of real Indic**, and one epoch is what both disclosed multilingual builds actually serve (umT5 48.2B/48.4B, NVIDIA 6.00B/6.00B). A floor derived internally as “the largest share inside one epoch” turns out to match observed practice at two labs, which is the strongest external support any number in this document has. So **Indic's floor is 5.5% of real tokens**, and **agentic's is 2.0% of lane tokens** whose real component is the entire 627M pool at ≥4 epochs (2.508B = 0.125%), the balance verified-generated. For agentic the floor guarantees *presence in every cycle*, not real-token volume.

| Clause | Why |
|---|---|
| **Hard** constraint, not a preference | CLIMB: the code cluster C20 goes to **exactly 0** under a reasoning-only objective — any lane absent from the objective dies. Lanes must also be *in* the selector objective (Figs 5/7: different objectives, different winners). A second, independent instance: NVIDIA's DoReMi arm drove **64.38%** of a 300B English budget onto a single 14.0B source (**13.80 epochs**) and ~77.6% of a 150B code budget onto markdown (5.74 epochs), finished worst of five arms, and was excluded from their code ablation outright because it *"does not allocate enough tokens to facilitate model learning for the remaining 42 languages"* — an unconstrained optimiser collapsing onto a small source is the failure this floor prevents |
| Per **bucket** and per **cycle** | DD Alg 1: *"If a bucket is empty, we exclude it from sampling"* — a scarce lane can vanish after one cycle. Our own measurement shows a global ≥256 bucket floor discards **44.9%** of a short-document corpus |
| In the **anneal** too | Spark Joy's sans-math arm: a 100B final phase that stops feeding a lane drove MMLU to **29.71 vs 35.69 baseline (−5.98)** and Reading Comprehension to **26.48 vs 37.02 (−10.54)**. They held proportions while shrinking the pool, so the magnitude is inflated; the direction holds |
| Domain absence has a **measured downstream cost** | Pretrainer's Guide, leave-one-domain-out at 1.5B: removing Common Crawl costs **Academic QA −5.9** while removing the *Academic* domain itself **improves** Academic QA by **+2.2** — an 8.1pp reversal; removing Code & Math costs **Common Sense −5.8**. Heterogeneity beats targeted data even on targeted evals. **Honest limit:** this supports a floor on *large or heterogeneous* lanes. For lanes the size of our agentic 2.0%, its two analogues (Social 1.2%, Wikipedia 2.1%) moved mean QA **+0.4** and **−0.3** — indistinguishable from zero at that study's ±0.5pp resolution. Those same small lanes swung *individual* eval families by 3–7pp, so the defensible claim for a small-lane floor is **per-eval capability insurance, not mean-performance insurance** |

**When does it bind?** Indic + agentic by stage is 18 / 19 / 17 / 17% and 29.4% in the anneal — slack by 2.3–3.9×, so **this floor never binds under this mixture**. It is a backstop against OPUS drift, not an active constraint. The composer's per-lane floors (`indic ≥ 12`, `agentic ≥ 2`) *are* binding, and both hold: 15.80 ≥ 12, 2.00 = 2.

OPUS and the curriculum act on orthogonal axes — *whether* a token is served versus *when* — so they compose. Preference Curriculum is the published instance of the *when* axis and has **no floor of any kind**.

---

## 6. Curriculum

**Seed 200B → General 700B → Reasoning 600B → Long-context 500B**, then the **80B anneal**.

| Stage | web | code | reason | long | indic | STEM | agentic | v-synth | Difficulty |
|---|---|---|---|---|---|---|---|---|---|
| Seed (200B) | 54 | 13 | 2 | 1 | 16 | 12 | 2 | — | B0–B1 |
| General (700B) | 41 | 20 | 4 | 2 | 17 | 14 | 2 | — | B0–B2 |
| Reasoning (600B) | 27 | 28 | 13 | 3 | 15 | 12 | 2 | — | B0–B3 |
| Long-context (500B) | 24 | 29 | 12 | 11 | 15 | 7 | 2 | — | B0–B4 |
| **Anneal (80B)** | 21.156 | 22.969 | 9.063 | 2.781 | 21.875 | 9.156 | 7.500 | 5.500 | B0–B5 |

Every row sums to 100.000, and the anneal row is §4's effective mixture, so §4 and §6 agree exactly. The anneal's code / reasoning / STEM / agentic values are *derived* from the 62.5/37.5 construction, not independently chosen.

Order is load-bearing: at identical weights it is worth **+1.74 absolute average** (52.86 vs 51.12, Two-Phase Table 4 — the frequently-quoted "+3.4" is that same gain as a *relative* percentage), and it lands on sharp capabilities: GSM8K **30.86 → 40.33**, code **35.55 → 38.33**, MMLU flat (56.49 → 56.28). CLIMB adds the shape rule — from-scratch mixtures stay broad (top-3 ≈ 64%) while continuous/late mixtures go peaky (one cluster at 43%) — so early stages spread and only the anneal concentrates.

### 6a. Difficulty bands

Definitions are widget 7's `DIFF[]`; the example column is ours.

| Band | Level | Definition | Concrete example | Lane |
|---|---|---|---|---|
| **B0** | Nursery | simple children's sentences | *"The cat sat on the mat. The mat was red."* | web |
| **B1** | Grade-school | basic grade-school text | *"Water boils at 100 °C at sea level."* + integer-answer word problems | web, Indic |
| **B2** | High-school | high-school level material | A Wikipedia article on photosynthesis; a 30-line Python script with one loop | web, code, Indic |
| **B3** | Undergraduate | undergraduate coursework | A GSM8K-style multi-step word problem; a single-file module with tests; an IndicGenBench summarisation pair | code, STEM, reasoning |
| **B4** | Graduate | graduate-level texts | An AIME problem with a worked solution; a SWE-Gym task with a repo checkout; a peS2o paper section | reasoning, STEM, agentic |
| **B5** | Research / PhD | research and PhD-grade papers | A GPQA-Diamond physics item; a proof-pile-2 formal proof; a full SWE-smith trajectory with recovery | reasoning, agentic, STEM |

**Monotone floor:** each stage admits its band *and everything below* — never a hard gate. Dropping low bands late is what produced Spark Joy's negative Language Understanding at every phase length. **B5 is reserve-only**, withheld from the main run and spent in the anneal: §4's reserve on the difficulty axis.

No paper supports a content-difficulty ladder and one argues against it: Preference Curriculum's Fig 9 shows its "hard" half needs *less* scientific content (0.61 vs 0.70) and *less* cultural background (0.59 vs 0.69), with logical-reasoning requirement **identical at 0.72 / 0.72**, and Fig 6b puts 88% of arXiv in the *easy* half. **A perplexity gap is not a difficulty axis.** This ladder is built from source provenance and benchmark level — a labelling decision and a design bet. DD's ordering result is a **length** ladder, a different axis that can fight this one.

### 6b. Reasoning-length bands

Widget 7 makes this a second, independent schedule: *"alongside difficulty: short, medium, long and ultra traces are separate rungs. A hard problem with a short trace and an easy one with an ultra trace are not interchangeable, so trace length is scheduled too."*

All four bands solve the **same problem** — *how many integers in [1, 1000] are divisible by 3 or 5?* Answer **467**, correct at every band; only the solve rate changes. Tokens and rates are computed with widget 6's own tokenizer and curve `acc(L) = 0.955 − 0.615·exp(−L/τ)`, `τ = 62.28`.

| Band | Steps | Trace tokens | Solve rate | First step of the worked example | Share | Tokens |
|---|---|---|---|---|---|---|
| **LOW** | 2 | **37** | **61.5%** | *"Inclusion-exclusion: floor(1000/3) + floor(1000/5) − floor(1000/15)."* | 15% | 4.26B |
| **MEDIUM** | 4 | **74** | **76.8%** | *"Count multiples of 3 up to 1000: floor(1000/3) = 333."* | 30% | 8.52B |
| **HIGH** | 6 | **161** | **90.9%** | *"Let A = multiples of 3 and B = multiples of 5 inside [1, 1000]."* | 35% | 9.94B |
| **ULTRA** | 14 | **346** | **95.3%** | *"Restate the goal… then verify two independent ways."* | 20% | 5.68B |

These partition the **28.4B trace budget** from §1.2, not the whole 170B lane. ULTRA's 5.68B against 4.6B of long-CoT inventory is **1.23×**.

**Why ULTRA is smallest.** Widget 6's curve gives ULTRA **+4.40 points** over HIGH (95.26 vs 90.86) for **2.149×** the tokens, tripping the widget's *"wasted effort"* flag at +5.0. HIGH takes the largest share because that is where the curve still buys accuracy per token.

**Why all four must exist.** The effort dial selects among behaviours the model was trained to produce: shown only long traces it cannot answer briefly; shown only short traces it has nothing to select when asked to think. Two-Phase moved GSM8K **30.86 → 40.33** with reasoning-shaped data at **1.3%** of its second phase, so a small well-placed slice suffices. The 15/30/35/20 split is ours; only the ULTRA cap is course-derived.

### 6c. Packing, position, seams

- **Binary dataset decomposition, not concat-and-chunk.** Each document of length `l` splits into adjacent power-of-two spans; buckets hold single-document sequences, so no attention mask is needed and no tokens are wasted. Worth **+2.9 regular / +3.4 long-context average** (DD Table 5). Document masking is not a substitute: it lifts regular 51.5 → 52.4 but drops long-context 27.5 → 27.1 and craters MDQA-30 **20.5 → 16.0**.
- **All buckets for short-document lanes; the ≥256 variant only where documents are naturally long.** Measured on our own 342-document corpus, a global ≥256 floor discards **44.9%** of tokens — applied to Indic snippets, QA-format agentic data or parallel corpora that is the per-bucket starvation §5 forbids.
- **RoPE base 100,000 from the start.** Free **+5.4 MDQA** on the baseline, +4.8 on the decomposed run, regular unchanged (DD Table 4, **1B only**; Table 4's 24.9 for DD≥256@100k conflicts with Table 2's 23.0 for the same configuration, so treat the magnitude as approximate).
- **Training sequence length is 8192.** The curated inventory is *32K+ packed*, so those sequences decompose into 8k spans. This plan claims **no** capability beyond 8k; a 32k–128k extension is a separate budget.
- **Seams: 4 transitions × 20B blended = 80B, 4% of the main run.** Five stages have four boundaries.
- **The seam width is priced.** Widget 8's `peakFactor = 1 + effSharp·A·effFrozen` predicts, at a 20B band, **1.34× frozen and 1.23× unfrozen** against `RED_T = 3.0`; ~**6B** already clears it frozen. V4's ~150× corresponds to sharpness 1.0, frozen embeddings, zero band. DD Fig 8's un-ramped arm throws ~8 loss spikes to 7.5–8.1 while the ramped arm is spike-free — though those arms differ in both packing *and* curriculum, so it is not attributable to ordering alone.
- **Ramp, not step.** Preference Curriculum's S-shape blends over **43.9%** of its run and beats a hard switch by ~1.1 points — but it blends two halves of *one corpus*, not two mixtures, and 43.9% is 44× wider than our 1%-per-seam band, so we take the shape and not the width. MiniMax-01 reportedly interpolates source weights linearly across transitions (primary **2501.08313**; the detail appears only in the survey's source comments, not its published text).

---

## 7. Proxy protocol

Cost basis (6ND): a 40B probe on 120B params ≈ **2.9e22** FLOPs against ≈**1.44e24** for the full run — **1/50 of a run**, so twelve probes cost ~24%. CLIMB's 112-run search is priced separately at ~45 GPU-h per 350M proxy. Branching follows Llama 3: a partially trained checkpoint, LR decayed linearly to 0 over the probe, candidate at **30% against 70% default**. Spark Joy's own peaks are **0.60pp** (MMLU) and **0.86pp** (core average) at n=1, so every threshold sits outside that band. **MMLU is not a 1B metric.** NVIDIA reports it only at 8B/300B, explicitly *"when the experimental setting allows for a non-random score,"* and omits it from every 2B run — so at 1B we gate on a six-task LM-Eval mean and defer MMLU to 3B and above. For the multilingual probes we add **XCOPA** and **TyDiQA-GoldP**, which separated their mixtures by **2.31 points** at 8B. A second, closer bound agrees: the Pretrainer's Guide runs 28 pretraining ablations at **1.5B** — our probe scale — and its leave-one-domain-out mean-QA column is non-monotone in dose (removing 19.1% of the corpus moves the mean **−0.1**, removing 6.9% moves it **−2.7**), so that column cannot resolve below **≈±0.5pp**. Two independent studies at 7B and 1.5B put the single-seed floor in the same place. Both are n=1. Where a result lands **between** the confirm and refute bounds the default is to **keep the specified value and re-run at the next scale up**, not to adopt either branch — an inconclusive probe is not evidence for the plan.

| # | Hypothesis | Scale | Metric | Confirms | Refutes | Action on refute |
|---|---|---|---|---|---|---|
| **H1** | Long-context 4.45% + packing suffices | 1B, 100B; arms 0 / 2 / 4.45 / 9.4% | **MDQA-30 + RULER + LongBench** (all three) | 4.45% arm ≥ **90%** of the 9.4% arm on ≥2 of 3 | **< 75%** on ≥2 of 3 | raise curated lane to 9.4%, take from web |
| **H2** | Verified-generated agentic transfers | **3B**, 40B branch; format-only / +verified / +unverified | **BFCL AST-match** (primary), **SWE-bench Verified pass@1** (secondary) | verified arm ≥ **+3.0 pts** over format-only | **< +1.0 pt** | keep 2.00%, swap generated for FIM-multiplied real + format |
| **H3** | Indic tier C survives 2.53× | 1B, 100B; C at 4 / 2 / 0% | **IndicGenBench chrF**, **MILU**, **TyDiQA-GoldP** | 4% arm within **1.0 pt** of the 2% arm on ≥2 of 3 | **> 1.0 pt below** on ≥2 of 3 | C → 2%, mass to D |
| **H4** | An 80B anneal beats 40B | 1B, branch at 96% / 98% | six-task LM-Eval mean at 1B (MMLU only at 3B+) | 80B ≥ **+1.0 pt** | **≤ 0 pt** | revert to 40B |
| **H4′** | Raising reasoning does not cost STEM | 1B, 100B; reasoning 8.5% vs 6.0% | **GPQA + MATH** | STEM loses **≤ 1.0 pt** | **> 1.5 pt** | return the 0.55pp to STEM |
| **H5** | Indic-up anneal avoids the MAP-Neo effect | 1B; anneal Indic 21.9 / 15.8 / 8.5% | **MILU + Flores-101 chrF + XCOPA**; six-task LM-Eval mean as the forgetting check at 1B, **MMLU only at 3B+** | Indic ≥ **+1.5 pts**, forgetting check loses **≤ 1.0 pt** | loses **> 1.0 pt** | flatten Indic across the anneal |
| **H6** | A 20B seam holds the Indic transition | 1B; bands 0 / 5 / 20B, embeddings unfrozen | **peak gradient-norm multiplier** | peak **< 3.0×** (`RED_T`) | **> 3.0×** | widen until it clears |
| **H7** | The four length bands give a controllable dial | 1B, 100B; 15/30/35/20 vs HIGH-only | **LOW:ULTRA trace-length ratio** + GSM8K + MATH at each band | ratio ≥ **4×**, ULTRA accuracy ≥ LOW on both evals | ratio **< 2×** | widen the band spread |

H2's metric is the weakest link, and the Pretrainer's Guide sharpens why: across 28 pretraining ablations at 1.5B its authors evaluated **only after finetuning**, *"motivated by finetuning being more applicable for 1.5B parameter models"*, and their pretraining-attributable signal falls from 0.41 to **0.08 and out of significance** between 1.5B and 20M. Pretraining-mixture effects are exactly what a smaller proxy stops resolving. So **BFCL AST-match is H2's primary metric** — finetunable and format-checkable, therefore readable at 3B — and SWE-bench Verified pass@1 is reported as secondary evidence only, escalating to a 7B probe if the two disagree.

**What was executed.** Full 1B/3B training is unavailable here, so H1–H7 are specified and unrun: this plan claims the **highest** tier — concrete proxies with named metrics and numeric thresholds — and not "very highest." Two things were run and are reproducible from this repository. The mixture is **executable arithmetic**: stage profiles time-average to the declared shares within 0.05pp, all rows sum to 100.000, and every ratio, tier factor, reserve quantile, epoch count, the 17.64% shift and the 116.0B synthetic total are computed rather than asserted. And a **micro-replication of DD's packing claim** on a 342-document / 78,581-token corpus of our own papers: concat-and-chunk yields an average in-document context of **421.1** against decomposition-≥256's **3452.5** — direction confirmed at **8.20×**, well above the published 1.45×, because our corpus is short-document-heavy (median 104 tokens vs RefinedWeb's 598) and the ≥256 filter discards 44.9% of our tokens. That overshoot produced the bucket policy in §6c.

---

## 8. Cleaning, aimed at the starved slots

Starved by the course's ≥8% funding rule: **agentic (2.00%)**, and long-context on lane share (4.45%, though its 17.7% effective ≥4k exposure clears the line). Starved by supply: **agentic 73.4×**, **Indic tier C 2.53×**, **long-CoT** (5.68B ULTRA demand against 4.6B), **code post-dedup 1.32×**, **STEM 0.92×**.

| Priority | Slot | What cleaning buys |
|---|---|---|
| 1 | Agentic trajectories | The only lane where new cleaned tokens change the plan's worst number; every 100M real trajectory tokens cuts the generated fraction ~2 points |
| 2 | Indic tier C | Separating the translated fraction of Sangraha's 162B set dissolves the 12.6× premise and makes the course's 20% fundable (§2) |
| 3 | Long-CoT reasoning | The 4.6B pool binds both the ULTRA band and the anneal reserve |
| 4 | Multi-document long-context | Nothing in the inventory is multi-document, yet MDQA is the metric (§1.3) |
| 5 | STEM | 0.92× pre-selector, and §1.1 takes 0.55pp out of this lane |
| 6 | Code, at file level | The 32.9% retention ratio means cleaning changes the effective pool, not the headline |

Web needs no cleaning attention: at 0.15× supply is not the constraint, and the marginal work there is *filtering*, not acquisition.

---

## 9. Where this plan has no evidence, and what is most likely wrong

- **Indic is now partly evidenced, and the evidence is thin.** Two papers name Indic languages with token counts (UniMax 14 languages / 48.4B tokens of characters; NVIDIA 9 languages / 6.00B tokens) and both supply a per-language epoch-cap mechanism, but neither compares **native against translated against synthetic** value — the question our A/B/C/D split turns on — and neither reports tokenizer fertility on any Indic script. The one quantitative low-resource *staging* precedent still points against our Indic-up anneal.
- **No paper trains agentic trajectories at pretraining scale.** "Agent" appears once in the mid-training survey, as a dataset name. The verifier argument is reasonable and **unmeasured**, and 2.00% is 5–16× outside the band our own citations support.
- **Long-context evidence stops at 8192**, and nothing we hold is multi-document while MDQA is the metric.
- **The anneal's value at 120B is unmeasured and the one frontier-scale measurement is null.** Annealing gave Llama 3 8B +24.0% GSM8K and +6.4% MATH but *"a negligible uplift for the 405B model."* Every large published mid-training gain is ≤14B.
- **Scale gaps.** Collapse's percentages come from an 8×256 char-level nanoGPT on one Shakespeare play; DD's RoPE and ordering results are 1B; OpenCoder's dedup is 1.5B Python; Demystifying is ≤3B English CC on CE loss, and its "~30%" is interpolated from a grid that skips 30%.
- **Almost nothing has error bars.** CLIMB's checklist answers "No"; Spark Joy, Preference Curriculum and DD are single-seed. Cite curve shapes, not exact optima.
- **Eleven claims reach us through the mid-training survey rather than a primary.** Where a decision rests on one, the primary is named (MiniMax-01 2501.08313, Llama 3 2407.21783, MAP-Neo 2405.19327).

**Attack first:** agentic 2.00% (73.4×, 91.5% generated); Indic tier C (rests on tier C = 5.0B, ignoring a possibly-separable translated fraction); the reasoning lane's 7.1B trace pool against a 170B lane; and the absence of any multi-document data behind an MDQA claim.
