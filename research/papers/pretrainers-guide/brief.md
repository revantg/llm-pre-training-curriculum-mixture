# `pretrainers-guide` — A Pretrainer's Guide to Training Data

**arXiv 2305.13169v2** (13 Nov 2023, 51 pp) · *A Pretrainer's Guide to Training Data: Measuring the Effects of Data Age, Domain Coverage, Quality, & Toxicity* · Longpre, Yauney, Reif, Lee, Roberts, Zoph, Zhou, Wei, Robinson, Mimno, Ippolito (MIT / Cornell / Google Research / OpenAI).
**Venue:** none in arXiv metadata — `Comments`, `Journal-ref` and `DOI` are all empty on the abs page; the source builds against `iclr2023_conference.sty`. Cite as arXiv preprint, not as a conference paper.
**Sources used:** PDF (`https://arxiv.org/pdf/2305.13169`, HTTP 200) · abs page · native arXiv HTML (`/html/2305.13169`, HTTP 200) · TeX source (`/e-print/2305.13169`, HTTP 200, 17 figure PDFs). All four routes worked. Assets in this directory.

> ### Correction, read first
> **This paper is not about data repetition, and the slug it was queued under (`repeat`) is a misnomer.** It contains no epoch experiment, no repetition sweep, and no multi-pass ablation. I grepped the complete TeX source for `epoch|repeat|repetition|duplicat|dedup|multiple times|unique token|data.constrain`: the only substantive hits are one preprocessing sentence (`main.tex:457` — C4 and the Pile are approximately deduplicated per Lee et al. 2022) and one sentence about repeating *their own experiments* (`main.tex:1015`). It therefore **cannot** replace the borrowed Two-Phase 6/8-epoch ceiling.
> The paper that does that work is **arXiv 2305.16264, *Scaling Data-Constrained Language Models*** (Muennighoff et al.) — an adjacent number, almost certainly the origin of the mix-up. It is being read separately by `ScalingDC`; nothing about repetition in this brief should be relied on over that read.
> The paper **is** in scope and does earn its place, on two axes that were genuinely open for us: **proxy/validation design at ~our proxy scale (weakness #8)** and **the domain-heterogeneity case for a per-lane floor (weaknesses #4/#10)**, plus a real, unasked-for caution on our **web quality filter**.

---

## 0. The repetition audit — answered first, because it is why the paper was queued

**Verdict: SILENT on all seven figures.** Not "weakly supportive" — silent. The paper never varies passes over data as an independent variable, never reports an epoch count, and trains with **dropout 0.0** (Table 5, App. C.1), so it also has nothing to say on Main's sub-questions about regularisation.

| # | Our figure | SOLUTION.md | Paper's verdict |
|---|---|---|---|
| 1 | **4 epochs** on the 0.627B agentic pool | §3, §5 | **SILENT** — smallest pool studied is ~10²× larger; no epoch variable |
| 2 | **4.00 epochs** on the 7.1B reasoning trace pool | §1.2 | **SILENT** — same |
| 3 | **5.06×** on Indic tier C's 5.0B | §2 | **SILENT** — and English-only (§8, "English vs Multilingual Data") |
| 4 | **2.11×** on Indic tier B | §2 | **SILENT** (see note) |
| 5 | **1.98×** on Indic tier A | §2 | **SILENT** (see note) |
| 6 | **1.32×** on code post-dedup | §1 "Code supply is smaller than the headline" | **SILENT** — Code & Math is a leave-one-out bucket, never a repetition arm |
| 7 | OPUS **~6× effective** | §0 Selector, §1 | **SILENT** — no selection-efficiency or acceptance-rate experiment |

### The one indirect observation, and why I am not scoring it as evidence

There *is* a latent multi-pass structure, and it is worth recording so nobody else re-derives it and over-claims:

- The token budget is **fixed across every arm**: batch 4096 × sequence length 512 × **88,064 steps = 184.68B tokens** (Table 5, App. C.1 — a single `Training Steps` value for LM-XL, not per-arm).
- The quality-filter arms shrink the pool to **90.6 / 83.9 / 73.3 / 45.6 %** of C4 (Table 15, App. E.2; also on the x-axis of Fig. 6).
- So the `T=0.7` arm makes **2.193× as many passes over its pool** as the Full Dataset arm — an assumption-free ratio — and still beats it: **+0.7 mean QA** (Fig. 6) and **+1.8 toxicity identification** (Table 15).

Five reasons this moves none of our seven numbers, and I would not put it in the submission:

1. **Confounded by construction.** The arm changes pool *quality* and pass count together; that confound is the entire point of the experiment. It cannot isolate repetition.
2. **Wrong pool magnitude.** Even the most aggressive arm's pool is ~71B tokens — **~113×** our agentic pool and **~10×** our reasoning trace pool. Our binding question is repetition at 10⁸–10⁹ unique tokens; this is 10¹¹.
3. **Wrong epoch range.** Absolute counts are ~1.2 → ~2.6 epochs [INFERENCE: uses the external ~156B-token figure for C4-en; the paper never states its corpus size]. That is *below* every ceiling we actually lean on (4×, 5.06×, ~6×).
4. **`% Data` may be documents, not tokens.** Table 15's column is headed `% Data` and Fig. 6 says "percentage of training data remaining". A quality filter preferentially removes short low-quality documents, so the token ratio need not equal the document ratio. Unresolved in the paper.
5. **Inside the noise.** +0.7 mean QA is single-run and sits within the ~±0.5pp resolution I bound in §2 below.

**Does this let us drop the borrowed Two-Phase 6/8-epoch ceiling? No.** Explicitly no. Nothing here is a directly-measured epoch ceiling at any scale, let alone at small unique-pool sizes. The scale-extrapolation weakness in our repetition column is untouched by this paper and stands exactly where it stood.

---

## 1. What the paper actually is

**Claim.** Pretraining-data design is undocumented and driven by unvalidated intuition; they run the largest published from-scratch data-ablation study to fix that. **28 × 1.5B-parameter** decoder-only LMs, plus a **20M** model for scale effects.

**Implementation nits** (all Table 5 / §2.4 / App. C unless noted):

| Item | Value |
|---|---|
| Models | **LM-XL 1.5B** (t5.1.1-XL-like), **LM-Small 20M** (t5.1.1-small-like), decoder-only, causal-decoder + full-LM objective |
| Codebase | **T5X** + TensorFlow on TPUs (8×8×8 for XL, 8×8 for Small) |
| Batch / seq len / steps | **4096 / 512 / 88,064** → **184.68B tokens**, identical for both sizes |
| Tokens per parameter | **123 at 1.5B** = **6.2× Chinchilla-optimal**. Ours is 16.7 = 0.83×. See threats (§6) |
| LR schedule | base LR **0.5**, decay factor 0.5, **1000 warmup steps**, steps-per-decay 20,000 (inverse-sqrt-family T5 schedule). **No cooldown/anneal leg at all** |
| Regularisation | **Dropout 0.0** |
| Corpora | **C4** (2019 CC snapshot, badwords filter *removed*) and **The Pile** (825 GB, 22 sources). Both approx-deduplicated per Lee et al. 2022 |
| Quality filter | The **PaLM/GLaM classifier** (0 = high quality → 1 = low); remove above T ∈ {0.975, 0.95, 0.9, 0.7}, plus an inverse filter |
| Toxicity filter | Jigsaw **Perspective API**, remove above T ∈ {0.95, 0.9, 0.7, 0.5, 0.3}, plus inverse, plus the C4 n-gram badwords list |
| Evaluation | **Always by finetuning**, then test. QA = union of MRQA + UnifiedQA (30 datasets; 27 in the domain study), partitioned into Wiki / Web / Books / Biomed / Academic / Common Sense / Contrast Sets |
| Code / artifacts | **None released.** No repo, no checkpoints, no data links anywhere in the paper |

**Implicit assumptions worth naming.** That a finetuned-QA delta is the right readout for a pretraining-mixture decision; that one run per configuration suffices (stated as a limitation, §8); that a document-level classifier score is a usable stand-in for "quality" (they disclaim ground truth, §2.2); and that English-only conclusions carry — which they explicitly decline to assert (§8).

---

## 2. Weakness #8 — validation design at 1B/3B. **The most useful thing in this paper for us.**

This is 28 from-scratch pretraining runs at **1.5B**, i.e. between our H1/H3–H7 (1B) and H2 (3B) probes. It is the closest published scale-match in our whole evidence base, so its methodology admissions are directly transferable in a way its findings are not.

### 2.1 Seeds, variance, error bars — the blunt answer

- **One run per configuration. No seed replication.** §8 Limitations is titled **"Compute Expense & Single Shot Experiments"**: *"We carefully curated the choice of experiments in advance, without the luxury of multiple rounds of reflection and repetition, common in many NLP experimental settings."*
- **No error bars, no CIs, no seed counts on any QA result.** I verified this from the pixels of Figs. 6, 7 and 8: cell values and a colorbar only (§5 figure inventory).
- The **only** dispersion anywhere is `RepBias ± 0.6–0.8` in Tables 3 / 14 / 15 — one metric, and it is a within-metric spread, not run-to-run variance.
- The **only** significance testing is on the *temporal* result: Pearson r with p < 0.05, and a one-sided Wald test that the slope exceeds zero (§4). Those are regressions over many (pretrain-year, eval-year) cells. **The arm-vs-arm deltas — the results structurally analogous to our mixture comparisons — carry no uncertainty quantification at all.**

**So: the paper does not give us a measured 1.5B noise floor, and we cannot claim one from it.** That is a straight negative on the best case Main hoped for.

### 2.2 What it *does* give: an internal resolution bound, and it corroborates our borrowed band

Fig. 8's mean-QA column is not monotone in how much data was removed:

| Removed | Share of corpus | Mean QA Δ |
|---|---|---|
| Social | **1.2%** | **+0.4** |
| Wikipedia | 2.1% | −0.3 |
| Books | 6.9% | −2.7 |
| Academic | **12.9%** | **+0.2** |
| Code & Math | **19.1%** | **−0.1** |
| CC | 26.9% | −4.8 |

Deleting **19.1%** of the corpus moved the mean by **−0.1**, while deleting **6.9%** moved it by **−2.7**. The paper reads this as composition mattering more than volume, which is fair. But it also means that at this scale, in this setup, **the mean-QA column cannot resolve differences below roughly ±0.5pp** — otherwise `No Academic +0.2` and `No Code −0.1` would be interpretable, and the paper itself declines to interpret them, hedging to *"all, or nearly all, the data"* (§6). `[INFERENCE — my bound from their dose-response, not a figure they report.]`

**This is worth real marks and it is honest:** our §7 thresholds are currently placed outside a **0.60pp / 0.86pp** band borrowed from Spark Joy **at 7B, n=1**. An independent ~±0.5pp resolution bound from a **1.5B, n=1** study lands in the same place at a scale far closer to our probes. It **corroborates** the borrowed band rather than replacing it — say exactly that, and do not upgrade it to "measured".

### 2.3 Single-metric thresholds are the fragile design — this hits H1 directly

For arms whose mean is ≈0, individual eval families swing hugely (Fig. 8):

- `No Wiki`: **Web −5.3**, **Contrast Sets +7.2**, mean **−0.3**.
- `No Code`: **Common Sense −5.8**, Web −3.1, Books +2.9, Contrast Sets +4.4, mean **−0.1**.
- `No Social`: Web −3.7, Common Sense −3.5, Academic +3.5, Contrast Sets +3.5, mean **+0.4**.

Single-run per-eval swings of ±3–7pp coexist with a null mean. Fig. 4's boxplots make the same point on the temporal axis: at misalignment = 1 the whisker spread over 5 datasets runs **~0.1 to ~6.3** around a mean of ~3.1.

**Consequence for §7.** H3 (IndicGenBench chrF **and** MILU), H4 (a 3-benchmark core average) and H4′ (GPQA + MATH) are correctly shaped. **H1 gates on MDQA-30 alone** and H7 on a single ratio — those are the two most likely to return an unreadable answer at 1B, and this paper is the citation that says so.

### 2.4 Readability at small scale — and the direct answer on SWE-bench-style evaluation

Two independent findings, and they point the same way:

**(a) They would not read a 1.5B model without finetuning.** §8: *"Our experiments focus on finetuned settings rather than zero- or few-shot prompting. This choice is motivated by **finetuning being more applicable for 1.5B parameter models** and also in many applied settings. We cannot establish how well these findings translate to prompted settings."* A team with 28 pretraining runs at 1.5B and Google-scale compute chose not to evaluate by prompting at that size.

**(b) A real effect was invisible 75× smaller.** Table 2 — temporal degradation per year of pretraining misalignment:

| | LM-Small (20M) | LM-XL (1.5B) |
|---|---|---|
| Pretraining TD, mean | **0.08** (r = 0.07) | **0.41** (r = 0.61) |
| Finetuning TD, mean | 2.36 (r = 0.81) | 2.84 (r = 0.76) |

§4: *"we do not find the same temporal degradation effects of pretraining were significant for LM-Small models"* — PubCLS r = 0.01† and AIC r = 0.18† fail p < 0.05. **A pretraining-data effect that is real and significant at 1.5B is undetectable at 20M.** Note the asymmetry: *finetuning* TD is readable at both sizes (2.36 vs 2.84); only the *pretraining-data* signal collapses. Pretraining-mixture effects are the fragile ones to measure small.

**On H2 specifically.** This corroborates our own concession and sharpens it. §7 already says *"SWE-bench Verified is near its noise floor at 3B"*; this paper adds that (i) the authors declined zero/few-shot readout even at 1.5B, and (ii) pretraining-attributable signal is exactly what shrinks fastest as the proxy shrinks. **SWE-bench Verified pass@1 on a 3B base model is the wrong instrument**, and the existing fallback — BFCL AST-match, a finetunable/format-checkable metric — is the right shape. This paper is a citation for making that the *primary* H2 metric rather than the escape hatch. It does not tell us the fallback will separate; it tells us the primary will not.

---

## 3. Weaknesses #4 / #10 — the per-lane floor and domain heterogeneity

A genuinely third, independent argument for the floor, alongside CLIMB's C20 → 0 and Collapse's real-corpus condition. But **narrower than hoped, and it must be cited with its limit or it becomes an E1 liability.**

### 3.1 Design and granularity

They partition the Pile's 22 sources into **9 domains** (Table 8) and pretrain LM-XL on the full set **minus each one**, nine models, finetuned for QA on Natural Questions, evaluated on 27 MRQA/UnifiedQA datasets grouped into 7 families.

Raw sizes (Table 8): CC 227 GB · Code & Math 135 GB · Books 118 GB · PubMed 109 GB · Legal 74 GB · OpenWeb 63 GB · Social 33 GB · Academic 60 GB · Wikipedia 6 GB; Base 825 GB.

**Does it resemble our lane structure?** Partly, and the mismatch matters. Nine buckets against our seven lanes is comparable *granularity*, and the smallest buckets (Social 1.2%, Wikipedia 2.1% of the deduped corpus) bracket our agentic 2.0% and sit near our long-context 4.45%. But these are **provenance buckets inside one English corpus, not capability lanes**: there is no agentic bucket, no long-context bucket, no non-English bucket, and **Code & Math is a single bucket** (GitHub + StackExchange + DM Mathematics) that merges what we split into code 23.95% and STEM 11.45%. So the *shape* of the experiment transfers; the lane taxonomy does not.

### 3.2 The leave-one-out numbers (Fig. 8, inspected from pixels; colorbar ±8, no error bars)

| Removed (share) | Wiki | Web | Books | Biomed | Academic | Common Sense | Contrast Sets | **Mean** |
|---|---|---|---|---|---|---|---|---|
| Full Dataset (100%) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | **0.0** |
| No Social (1.2%) | −0.8 | −3.7 | 2.6 | 0.1 | 3.5 | −3.5 | 3.5 | **+0.4** |
| No Wiki (2.1%) | −1.3 | −5.3 | 3.0 | 0.2 | 0.9 | −4.4 | 7.2 | **−0.3** |
| No Books (6.9%) | −3.5 | −6.3 | 1.0 | 0.0 | −1.6 | −6.5 | −4.4 | **−2.7** |
| No OpenWeb (6.9%) | −2.0 | −4.1 | 0.1 | −1.0 | 0.6 | −5.8 | −2.9 | **−1.4** |
| No Legal (9.0%) | −2.7 | −2.9 | 3.8 | 0.4 | 0.8 | −2.6 | −0.4 | **−0.6** |
| No Academic (12.9%) | −0.3 | −2.5 | 0.3 | −0.9 | 2.2 | −1.1 | 4.3 | **+0.2** |
| No PubMed (14.9%) | −0.3 | −3.0 | 3.9 | **−5.8** | −1.5 | −5.9 | 3.9 | **−1.2** |
| No Code (19.1%) | −0.5 | −3.1 | 2.9 | −1.2 | 1.2 | **−5.8** | 4.4 | **−0.1** |
| No CC (26.9%) | −3.2 | −6.2 | −2.9 | −4.6 | **−5.9** | **−8.0** | −5.2 | **−4.8** |

### 3.3 The strongest version of the claim — a removed lane hurting an unrelated eval

**The single best datum, and it is the paper's own headline:** removing **Common Crawl** costs **Academic QA −5.9**, while removing the **Academic** domain itself *improves* Academic QA by **+2.2** — an **8.1pp** reversal. §6: *"removing CC from the pretraining dataset reduces performance on downstream Academic QA tasks to a much greater extent than removing the Academic domain."* Their hypothesis is that CC/OpenWeb/Books already carry broad topical coverage, so deleting the targeted source deletes less than it appears to.

Second-best, and closer to our lanes: **removing Code & Math costs Common Sense −5.8** with a mean of only −0.1. Removing code hurt a reasoning eval with no obvious code content. **Removing PubMed costs Common Sense −5.9**, alongside the expected Biomed −5.8. And **every one of the nine arms loses on Web (−2.5 to −6.3)**, with 8 of 9 losing on Common Sense.

Also load-bearing for us: **the largest heterogeneous sources are the most valuable per token removed** — CC (26.9%) −4.8 and Books (6.9%) −2.7 are the two worst deletions, and Books is a *small* bucket. §6: *"these results suggest that more data is not necessarily as important a factor as a combination of heterogeneity and quality."*

### 3.4 The honest limit — state it or a reviewer will

**Two of nine leave-one-out arms beat the full dataset on mean QA** (`No Social +0.4`, `No Academic +0.2`) and a third ties (`No Code −0.1`). The paper's claim is therefore hedged, and correctly: *"the best mean performance still comes from models that train on **all, or nearly all**, the data. **The exceptions are the removal of targeted source domains like the Pile's Code or Academic**"* (§6).

So the transferable finding is asymmetric, and this is the part to be scrupulous about:

- **Supported:** a floor on **large and/or heterogeneous** lanes (CC, Books, OpenWeb). Deleting them is unambiguously costly, including on evals they do not obviously serve.
- **Not supported:** a floor on **small targeted** lanes justified by *mean* performance. The two closest analogues to our agentic 2.0% — Social at 1.2% and Wikipedia at 2.1% — produced mean deltas of **+0.4** and **−0.3**, i.e. indistinguishable from zero at the ±0.5pp resolution of §2.2.
- **Supported on a different axis:** those same small lanes moved *individual* eval families by 3–7pp in both directions. So the defensible claim for a small-lane floor is **"per-eval capability insurance"**, not "mean-performance insurance".

Our §5 floor is Indic 5.5% **and agentic 2.0%**. This paper supports the Indic half decently (a 5.5% multilingual lane is small-but-not-tiny, and heterogeneity is what it buys) and supports the agentic half **only** in the weaker per-eval form. Cite it that way. It is still a real addition, because our existing two arguments (CLIMB's C20 → 0; Collapse's real-token condition) are both about *mechanism* — a lane dying, or generated data drifting — whereas this is about *measured downstream cost of absence*. Different axis, genuinely additive.

---

## 4. The quality filter — an unasked-for finding that bears on §1's web filter and §4's reserve quantile

Our §1 "Filters" zeroes the **64.44% Low** bucket of natural CC on Two-Phase's 5-bucket English classifier (MMLU 42.94 → 56.10), and §2 hazard 2 concedes that classifier is unvalidated on Indic scripts. This paper runs the **PaLM/GLaM** quality classifier — a different instrument of the same class (positively-defined, anchored on Wikipedia/Books) — and finds three things we should price.

**(a) Aggressive filtering is concave and peaks early.** Fig. 6, mean QA vs the unfiltered baseline:

| Arm | Data kept | Mean QA Δ |
|---|---|---|
| Inverse T=0.5 (removes the *highest*-quality 27%) | 73% | **−3.1** |
| Full Dataset | 100% | 0.0 |
| **T=0.975** | **91%** | **+2.5** ← peak |
| T=0.95 | 84% | +1.0 |
| T=0.9 | 73% | +1.2 |
| T=0.7 | 46% | +0.7 |

Removing ~9% of the corpus gave the best result; removing **54%** gave only **+0.7**. §5: *"the average performance peaks at T = 0.975 for the QA tasks, greater quality filtering still outperforms the unfiltered baseline on average."* Still positive — so this does not refute filtering — but the marginal return past ~10% removal is flat-to-negative. Two implications: our web filter's very aggressive posture is past *this* study's optimum, and **§4's "top-5% quality quantile within each lane"** for the anneal reserve is a far more extreme cut than anything measured here (the closest arm, `Inverse T=0.5`, shows that discarding the *top* of the distribution costs −3.1, which is the complementary warning).

**(b) A global filter damages specific lanes, and not the ones you would guess.** Books QA is hurt at **every** threshold and monotonically: **−2.2 / −4.0 / −3.5 / −6.7**. §5: *"quality filtering provides the least benefit to QA tasks in these categories, even hurting the performance for Books"* — despite Books ranking among the highest-quality domains (Fig. 2: Books text quality **1.9×** the Pile mean, Wikipedia **3.0×**). Meanwhile the lowest-quality-scoring domains benefit most (Biomed +6.1, Academic +6.4 at T=0.975).

**(c) The classifier systematically deletes technical text.** §3: *"Technical domains such as PubMed, Code, and Academic score low on predicted quality, indicating that **overly-specific positively-defined filters on web documents may remove substantial amounts of potentially useful specialized text**."* App. D.2 / **Fig. 11** confirms it by running the classifier over the Pile: as the cutoff rises from 0 to 0.2, the **Code and PubMed** bands collapse to slivers while **CC, OpenWeb, Wikipedia and Legal** are largely retained. `[Read from Fig. 11 pixels — a stacked bar chart with no printed values; the paper gives no numbers in prose. Qualitative pattern is unambiguous; do not quote magnitudes.]`

**Why this matters to us more than to them.** Two of our seven lanes (code 23.95%, STEM 11.45%) are exactly the "technical, low predicted quality" categories this classifier deletes, and a third (Indic 15.80%) is non-English, which no reference-corpus-anchored English classifier scores fairly. §5's headline — *"one size does not fit all"* — and *"Optimizing on one measure of quality is not sufficient to predict or improve performance across domains"* upgrade our §2 hazard 2 from a reasonable worry into a **measured cross-domain result**, and extend it from Indic to code and STEM. That is the second-most valuable thing in the paper for us.

---

## 5. Data age — one note, then stop

Mostly out of scope: we cannot choose our corpus's collection date. One consequence is real and unpriced in our spec, and it is an **E6** point since E6 is about tying lanes to benchmarks.

Degradation is **asymmetric and bidirectional** (§4, Fig. 4): performance falls whether evaluation data predates *or* postdates the pretraining data, and *"newer models will perform less well on older evaluations"* — *"older evaluations may underestimate the capabilities of newer models."* Pretraining TD is **0.41 points per year of misalignment** at 1.5B (Table 2, mean over 5 tasks, r = 0.61, all five slopes p < 0.05), and it is **not** repaired by finetuning on temporally-matched data — which is the paper's most transferable structural claim: a pretraining-data property that downstream training cannot undo.

For us: our data would be 2025–2026 while MMLU (2020), ARC (2018), HellaSwag (2019), GSM8K (2021) and HumanEval (2021) are 4–8 years older. At 0.41 pts/year *for 1.5B and a much larger effect implied for larger models* (§4: *"this effect is worse for the larger, more capable models"*), a several-point systematic **under**-estimate on our own headline benchmarks is plausible. This does not change a single share, so it belongs in §9 as a one-line evaluation caveat, not anywhere else. Anything more is E3 padding.

**Out of scope entirely, and deliberately excluded:** everything about toxicity filtering and toxic generation (Fig. 5 left, Fig. 7, Fig. 13, Tables 3/14). Real results, no R0–R8 requirement touches them.

---

## 6. Figure inventory — all inspected from pixels

> **Tool note.** `inspect_image` is **not mounted in this session**. Attempted twice; exact error both times: `No such tool device: xd://inspect_image. Mounted: ast_edit, debug, browser, web_search, workflow, mcp__browsermcp_*, mcp__chrome_devtools_*, mcp__cloudflare_*, mcp__langfuse_*, mcp__pencil_*.` No vision device exists in that list. Substitute used: rasterised all 17 figure PDFs from the TeX source at 200 dpi (`pdftoppm -r 200`) into `figs/` and inspected each via `read`, which decodes images inline — genuine pixel inspection, not OCR. Every axis, tick and legend below was read from the rendered image.

| File / № | What it is | Axes, ticks, legend | Error bars | Claim |
|---|---|---|---|---|
| `slice_ablations_intro` **Fig. 1** | Pipeline schematic | Domain (Web/Code/Pubmed/Academic/Books/Wikipedia) × 2013–2022; right panel 5 named outcomes | — | Illustrative only; the right-hand bars are schematic, not data |
| `Domains_in_The_Pile` **Fig. 2a** | 14 features × 9 domains + C4 | Ratio-to-dataset-mean, gray dashed baseline = 1×; absolute mean printed right | none | Books is the outlier: profanity 4.3×, toxicity 3.5×, sexually explicit 4.1×, **and** text quality 1.9×. Wikipedia quality **3.0×**; Code/Academic/PubMed quality **0.3×** |
| `C4` **Fig. 2b** | Same features × Low/High Toxicity, High/Low Quality in C4 | as above | none | High-toxicity C4 docs: profanity 5.0×, 2.5× longer. Quality and toxicity are **not** aligned |
| `The_Pile` **Fig. 2c** | Same, Low/High Toxicity in the Pile | as above | none | Mirrors C4: 4.4× profanity, 3.5× toxicity, 3.5× length |
| `xl_time_pt_heatmap` **Fig. 3** | 5 panels, pretrain-year × eval-year | Pretrain 2013/2016/2019/2022 × eval years per task; colour normalised **per column** | none | Diagonal-ish best; e.g. PubCLS 2013-pretrain leads 2010–2014 evals (78.9/79.2/78.5) and loses 2016 (75.1 vs 76.3) |
| `temporal_degradation_xl` **Fig. 4** | Boxplot over 5 datasets | y "Relative Improvement (%)" 0–6 (ticks 1); x "Pretrain Year − Evaluation Year" −8…+12 | **boxplots** — median line, mean triangle, quartile box, whiskers. Across *datasets*, **not seeds** | Peak at misalignment 0 (mean ~3.45) and +1 (~3.13); falls both ways, steeper on the negative side. Whiskers at +1 span ~0.1–6.3 |
| `tox-filter_lm-xl-c4` **Fig. 5L** | Toxicity-filter trade-off, C4 | y Toxicity Identification −6…+2% (ticks 2); x Toxic Generation −60…+20% (ticks 10) | none | Monotone trade-off: T=0.3 reaches ~−52% generation at ~−5.2% identification; Inverse filter is best at identification (+1.4%) |
| `qual-filter_lm-xl-c4` **Fig. 5R** | Quality-filter trade-off, C4 | y −2…+3% (ticks 1); x −2…+14% (ticks 2) | none | Quality filtering raises **both** identification (to +1.8% at T=0.7) **and** toxic generation (+7 to +11%) |
| `qualonly_on_domains_cc` **Fig. 6** | Quality filter × 7 QA families | rows T with % kept; cols Wiki/Web/Books/Biomed/Academic/Common Sense/Contrast Sets/Average; colorbar **−6…+6** (ticks 2) | **none** | Peak mean **+2.5 at T=0.975 (91% kept)**; Books hurt at every threshold, worst **−6.7**; Inverse mean **−3.1** |
| `toxonly_on_domains_cc` **Fig. 7** | Toxicity filter × same | colorbar **−4…+4** (ticks 1) | **none** | Monotone harm: mean +0.2 / −0.7 / −1.2 / −2.0 / −2.7 as filtering rises; **Inverse +1.7** is the best arm |
| `domain_heatmap_xl` **Fig. 8** | Leave-one-domain-out × same | rows "No X (n%)"; colorbar **−8…+8** (ticks 2) | **none** | §3.2 table. No CC −4.8 worst; No Social +0.4 and No Academic +0.2 beat the baseline |
| `Features_across_C4_and_The_Pile` **Fig. 9a** | 14 features, C4 vs Pile | ratio, C4 = 1.0× | none | Pile docs **2.4×** longer, **1.9×** non-ASCII, **1.2×** quality, **1.8×** readability, 1.7× "has address" |
| `Features_Across_Time` **Fig. 9b** | 14 features × C4 2013/2016/2019/2022 | ratio to mean | none | Non-ASCII rises 0.8× → 1.3×; text quality falls 1.1× → 0.8×; toxicity falls 1.3× → 1.0× |
| `dates-histogram` **Fig. 10** | Year-mention distribution per C4 snapshot | y "Percentage of year mentions" 0–30% (ticks 10); x 2000–2022 | none | Each snapshot spikes hard at its own cutoff year (2013 → ~26%, 2016 → ~21%, 2022 → ~21%) |
| `Data_with_a_Quality_Cutoff` **Fig. 11** | Stacked per-domain survival | y "Number of examples" 0–1.3×10⁸; x "Filtering cutoff" 0 / 0.025 / 0.06 / 0.1 / 0.2; legend 9 domains | none | Total 1.30×10⁸ → 0.61×10⁸. **Code and PubMed collapse; CC, OpenWeb, Wiki, Legal largely retained.** No printed values |
| `xl_time_ft_heatmap` **Fig. 12** | Finetune-year × eval-year, 5 panels | as Fig. 3 | none | Replicates Luu et al. 2021: strong diagonal (PoliAff 2009–13 arm 100.0 on 2012–13, **53.1** on 2018) |
| `tox-filter_lm-xl-pile` **Fig. 13** | Toxicity-filter trade-off, Pile | y −6…+2%; x −60…+10% | none | Same shape as C4, compressed: T=0.3 at ~−31% generation, ~−2.7% identification |
| `figure-1.pdf` | **Unused leftover** — a 4-panel earlier version of Fig. 1, present in the source tarball but referenced by no `\includegraphics`. Inspected for completeness; contains no data | — | — | — |

**Aggregate:** 17 figures in the paper, **one** carries any dispersion information (Fig. 4, and it is across datasets not seeds). Zero carry seed counts or CIs.

---

## 7. Threats to validity against a 2.0T / 120B seven-lane multilingual run

1. **English only.** §8: *"Our analysis was limited to two English datasets. It's important to note that training composition is an even more crucial question for multilingual and non-English models."* The authors decline to extend their own conclusions to our central Indic problem.
2. **80× parameter gap, and the paper's own evidence says the gap matters.** 1.5B → 120B. Their 20M → 1.5B comparison shows a pretraining-data effect growing **5.1×** (0.08 → 0.41) and crossing from insignificant to significant. Effects here are lower bounds on ours in *direction*, with no basis for magnitude.
3. **Opposite side of Chinchilla.** They train **123 tokens/param (6.2× Chinchilla)**; we plan **16.7 (0.83×)**. In a heavily over-trained regime marginal unique data is worth less and pruning looks cheaper, which plausibly *flatters* their aggressive quality-filter arms. Our under-trained regime is the one where deleting unique tokens should hurt more — an argument for the *milder* filter their peak already recommends.
4. **No anneal, no curriculum, no ordering.** A single inverse-sqrt-family schedule (base LR 0.5, decay 0.5, 20k steps/decay), **no cooldown leg**. The paper is silent on our §4 anneal size, §6 stage order and §6c seams. Data composition is varied *globally for the whole run* — the one dimension our spec never treats as static.
5. **Readout mismatch.** Every result is post-finetuning QA (MRQA/UnifiedQA, finetuned on Natural Questions for the domain study). Our benchmark suite is base-model MMLU/GSM8K/HumanEval/MDQA/IndicGenBench. A finetuned-QA delta and a base-model benchmark delta are not interchangeable, and §8 says they *"cannot establish"* the translation.
6. **n = 1 everywhere**, so any single cell in §3.2 or §4 could be noise; only the large ones (|Δ| ≳ 3) should be leaned on.
7. **Unreproducible toxicity instrument** (§8, Perspective API drift) — irrelevant to us, but it is why nothing from the toxicity axis should be cited.
8. **No artifacts.** No code, checkpoints or data release; nothing here is independently verifiable or re-runnable by us.

---

## 8. VERDICT

**(a) In scope or out?** **IN SCOPE.** A pretraining-data-composition paper — 28 from-scratch pretraining runs whose independent variable *is* the data mixture. It is in-scope for a different question than the one it was queued for.

**(b) Keep or drop, given E3?** **KEEP — narrowly, for two claims and one caveat.** Cite it in **§7** (proxy design: single-shot, resolution bound, small-scale detectability, the SWE-bench readability argument), in **§1/§2** (the quality-filter concavity and the cross-domain filter damage), and add **one** clause in **§5** (domain-absence cost as a third floor argument, in its per-eval form). **Do not** cite it for repetition, do not cite it for the anneal, do not cite it for toxicity, and do not let it become a paragraph — three or four sentences plus two table rows is the whole earned footprint. Its highest-value contribution is **methodological**, which is exactly what E11's top tier rewards, and it lands on the two hypotheses we ourselves flagged as weakest (H1's single metric, H2's unreadable metric).

**(c) Which of the ten open weaknesses it touches**

| # | Weakness | Touched? |
|---|---|---|
| **8** | Validation design at 1B/3B | **YES — primary value.** Nearest published scale-match; single-shot admission; ±0.5pp resolution bound; 20M-vs-1.5B detectability; explicit refusal to prompt-evaluate at 1.5B |
| **10 / (4)** | The OPUS floor, per-lane | **YES — partial.** Supports floors on large/heterogeneous lanes; **null** on small targeted lanes by mean performance; supports small lanes only as per-eval insurance |
| **1** | Agentic 2.00% | **Weakly.** Its two smallest buckets (1.2%, 2.1%) are the only published analogues at that share, and both are ≈0 on mean QA. Cuts slightly *against* us |
| **2, 3, 5, 6, 7, 9** | Tier C repetition · reasoning traces · anneal 80B · B0–B5 ladder · length split · seam width | **NO — silent on all six** |
| **4** | Long-context / MDQA | **NO.** Sequence length is fixed at 512; no long-context or multi-document experiment exists |

**(d) Specific SOLUTION.md numbers it confirms, challenges, or refines**

| Section | Number | Effect |
|---|---|---|
| **§7** | 0.60pp / 0.86pp noise band (Spark Joy, 7B, n=1) | **CORROBORATES** at a much closer scale — an independent ~±0.5pp resolution bound at **1.5B**, n=1. Still borrowed, not measured |
| **§7 / H2** | "SWE-bench Verified is near its noise floor at 3B" | **CONFIRMS and strengthens.** They declined prompt-based readout at 1.5B; pretraining signal is what fades fastest small |
| **§7 / H1** | MDQA-30 as the sole H1 metric | **CHALLENGES.** Single-eval swings of ±3–7pp coexist with null means at this scale — H1 and H7 are the fragile gates |
| **§1 "Filters"** | Zero the 64.44% Low bucket | **REFINES / partially CHALLENGES.** A same-class classifier peaks at removing only ~9%; 54% removal returns +0.7 vs +2.5 |
| **§2 hazard 2** | "The quality classifier does not transfer" | **UPGRADES from assertion to measured result** — and extends the hazard from Indic to **code and STEM**, the low-predicted-quality technical domains |
| **§4** | Anneal reserve at a **top-5% within-lane quantile** | **CHALLENGES.** No arm here cuts nearly that hard; the complementary `Inverse T=0.5` arm shows discarding the top of the quality distribution costs **−3.1** mean QA |
| **§5** | Per-lane floor, Indic 5.5% + agentic 2.0% | **PARTIALLY SUPPORTS** — third independent argument, but only in per-eval form for the agentic half |
| **§9** | "No paper in the evidence base studied Indic" | **CONFIRMS** — §8 explicitly disclaims multilingual transfer |
| **§9** | New caveat available | Benchmark-age asymmetry: 2026 data scored on 2018–2021 benchmarks may be **under**-estimated (0.41 pts/yr at 1.5B, worse for larger models) |

---

## 9. Drafted insertions — spec voice, scale caveat attached

**→ §7, after "…so every threshold sits outside that band."**
> A second, closer bound agrees: the Pretrainer's Guide runs 28 **1.5B** pretraining ablations — our probe scale — and its leave-one-domain-out mean-QA column is non-monotone in dose (removing 19.1% of the corpus moves the mean **−0.1**; removing 6.9% moves it **−2.7**, Fig. 8), so that column cannot resolve below **≈±0.5pp**. Two independent studies at 7B and 1.5B therefore put the single-seed floor in the same place, and every threshold here clears it. Both are n=1: that paper's §8 is titled *"Compute Expense & Single Shot Experiments"* and reports no seed replication, no confidence intervals and no error bars on any QA result. **We are corroborating a borrowed floor, not measuring our own.**

**→ §7, replacing the H2 escalation sentence.**
> H2's metric is the weakest link, and the Pretrainer's Guide sharpens why: with 28 runs at 1.5B its authors evaluated **only** after finetuning, *"motivated by finetuning being more applicable for 1.5B parameter models"* (§8), and their pretraining-attributable temporal signal falls from 0.41 to **0.08 and out of significance** between 1.5B and 20M (Table 2) — pretraining-mixture effects are exactly what a smaller proxy stops resolving. So **BFCL AST-match becomes H2's primary metric** and SWE-bench Verified pass@1 the confirmatory one at 7B, rather than the reverse. Caveat: that is a 1.5B English finetuned-QA setting, so it argues the primary metric is unreadable without showing the fallback is readable.

**→ §2, appended to hazard 2.**
> This is now measured rather than feared, and it is wider than Indic. The Pretrainer's Guide applies the PaLM/GLaM quality classifier — same class as Two-Phase's, positively defined against Wikipedia/Books — and finds mean QA peaks at removing just **9%** of C4 (+2.5 at T=0.975) and decays to **+0.7** at 54% removed, while **Books QA is hurt at every threshold** (−2.2 / −4.0 / −3.5 / −6.7, Fig. 6) despite Books scoring 1.9× the corpus quality mean. Its §3 states that *"technical domains such as PubMed, Code, and Academic score low on predicted quality"* and App. D.2 shows the classifier stripping Code and PubMed while retaining web. **So the hazard covers code and STEM as well as Indic, and it argues our web filter should be validated against a milder cut.** At 1.5B, English, on finetuned QA — direction only.

---

## 10. Follow-on citations that would move one of the ten numbers

1. **arXiv 2305.16264 — *Scaling Data-Constrained Language Models*** (Muennighoff et al.). **The highest-value outstanding read**, and the paper this slug should have pointed at: repeated-token value, a safe epoch count, and the worthless-vs-harmful distinction. Owned by `ScalingDC`.
2. **Xie et al. 2023a (DoReMi)** — cited in §1 and §6 as corroborating the CC/OpenWeb/Books result. Already in our base via CLIMB's baselines (DoReMi 59.16); the domain-weight machinery is the relevant part for the floor.
3. **Lee et al. 2022, *Deduplicating Training Data Makes Language Models Better*** (`main.tex:457`) — the dedup method applied to both corpora here, and the natural companion to our §1 code-dedup ladder and OpenCoder's file-vs-repo result.
4. **Biderman et al. 2023 (Pythia)** — flagged in §9 as having *"trained on the Pile, with and without duplication."* That is a **direct duplication ablation with public checkpoints**, at 70M–12B. The single best public route to a *measured* small-pool repetition number that we could re-analyse ourselves rather than borrow.
5. **Chung et al. 2023** — the multilingual-balance citation §8 defers to when declining to generalise. Worth checking for a low-resource mixture number, since our Indic tier split has no direct precedent.
6. **Kreutzer et al. 2022** — multilingual corpora are dominated by low-quality text *"particularly for lower resource languages"* (§9). Directly relevant to Indic tiers B and C, and to whether a quality gate is even applicable there.
7. **Dodge et al. 2021** — documents that C4 filtering removes text from non-Western communities *"like India or Nigeria"* and recommends **against** filtering. A named counter-witness to applying our web filter to the Indic lane.
8. **Luu et al. 2021** — the source of the TD metric, if we ever want to price benchmark-age bias properly.

**Still unsourced after this read:** agentic/tool-use data at pretraining scale, multi-document long-context supply, and measured anneal lengths. This paper contributes nothing to any of the three.
