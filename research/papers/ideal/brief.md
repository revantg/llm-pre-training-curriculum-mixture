# IDEAL: Data Equilibrium Adaptation for Multi-Capability Language Model Alignment

arXiv **2505.12762v1** [cs.AI], 19 May 2025 (v1 only). CC BY-NC-SA 4.0.
Authors: Chenlin Ming, Chendi Qu, Mengzhang Cai, Qizhi Pei, Zhuoshi Pan, Yu Li, Xiaoming Duan, Lijun Wu, Conghui He (SJTU / Shanghai AI Lab / RUC / Tsinghua).
**Read via:** local PDF `paper.pdf` (22 pp, copied from `~/Downloads/IDEAL 2505.12762v1.pdf`) · `https://arxiv.org/abs/2505.12762` (abstract, worked) · `https://arxiv.org/html/2505.12762v1` (**full text + all 5 figures, worked** — saved as `paper.html`, MathML-stripped to `paper_clean.txt`, figures in `figs/`). No TeX source needed. **No code released** (the only GitHub links in the bibliography are OpenCompass and the HF alignment-handbook).
**Vision:** `xd://inspect_image` is **not mounted** in this session. Exact error, after one retry: `No such tool device: xd://inspect_image. Mounted: ast_edit, debug, browser, web_search, workflow, mcp__browsermcp_*, mcp__chrome_devtools_*, mcp__cloudflare_*, mcp__langfuse_*, mcp__pencil_*.` All five figures were instead decoded **inline as images** through `read` (native vision, not OCR) and are reported from pixels below.

---

## VERDICT

**(a) In scope or out of scope? — OUT OF SCOPE. This is a post-training (SFT) paper, not a pretraining-data, mixture, curriculum or annealing paper.**
Every experiment is supervised fine-tuning of **LLaMA-3.1-8B** on **23.8k–66k instruction samples** for **1 or 3 epochs** on 8×A100. There is no pretraining run, no token budget, no LR decay leg, no anneal, no curriculum ordering, no packing, no sequence-length policy, no multilingual data, no long-context data, and no agentic/tool-use trajectory data. Its five "domains" are math / code / reasoning / instruction-following / TrustAI — none of our seven lanes as we define them. `SOLUTION.md` line 3 states the scope explicitly: *"SFT, RLVR and preference training are out of scope."* IDEAL is on the far side of that line by its own title and abstract.

**(b) Which of the ten open weaknesses does it touch? — One, weakly: #8 (validation design).** And it touches it as a *caution*, not as a number. It offers an alternative mixture-search instrument (one influence/second-order gradient pass on a held-out reference set, requiring ~1 training run per iteration instead of CLIMB's 112) and one genuinely transferable methodological warning: **its own headline gain attenuates 3.2× when the evaluation basket is doubled from 4 to 8 benchmarks** (see below). It touches **none** of #1 agentic supply, #2 Indic tier C, #3 reasoning trace shape, #4 long-context / multi-doc, #5 anneal size, #6 difficulty ladder, #7 reasoning-length split, #9 seam width, #10 the OPUS floor.

**(c) Does it CONFIRM, CHALLENGE or REFINE any number in `SOLUTION.md`? — No. Not one.**

| Candidate | Section | Finding |
|---|---|---|
| The **4-epoch repetition ceiling** (§1.2 trace-shaped 4.00 ep; §3 "at 4 epochs that is 2.508B = 0.125% of 2T"; §4 long-trajectory reserve "3.89 epochs, inside the 4-epoch ceiling"; §5 "the entire 627M pool at ≥4 epochs") | §1.2 / §3 / §4 / §5 | **Not a confirmation.** IDEAL *re-cites* Muennighoff for it (line 233: *"according to Muennighoff's findings [43], repeating existing data up to four times yields a performance improvement that is largely equivalent to introducing the same amount of new data"*) and adds no measurement of its own. Citing IDEAL here would be citing a citation, from a weaker and out-of-scope source. **See the follow-on section — the primary is the prize.** |
| §7 proxy protocol, threshold design | §7 | **Weak challenge at best.** The 7.01%→2.17% attenuation cautions that a mixture win measured on a narrow named basket shrinks on a broad one. But it is measured at SFT scale, and §7 already carries Spark Joy's n=1 noise band (0.60pp MMLU / 0.86pp core avg) doing the same job in-domain. |
| §1 "search the mixture" framing (CLIMB) | §1 / §7.1 | **No new information.** IDEAL reports DoReMi and DOGE being unstable, but transplanted into SFT; `SOLUTION.md` already discounts DoReMi via CLIMB's own Table 1 (DoReMi 59.16 vs CLIMB 60.41) at pretraining scale, which is the relevant setting. |
| §5 protected floor ("a lane absent from the objective dies") | §5 | **Do not cite — trap.** See "two traps" below. |

**(d) Keep or drop? — DROP. Do not cite it in the submission.**
Per the rubric's **E3** (*"a tightly argued short plan will score well while padding earns nothing"*) and the **PADDING** severity label (*"correct but irrelevant to R1–R8 / E4–E11"*), a tenth paper that defends no number is a net loss of marks. It also cannot lift **E11**: the ceiling tiers ask for a concrete proxy at **1B or 3B** with a **named confirm/refute metric** for a *pretraining mixture*, and IDEAL supplies an 8B SFT influence method whose own metric it shows to be basket-sensitive. Worse, citing an explicitly-SFT paper hands a reviewer the cheapest possible hit — *"your own line 3 says SFT is out of scope"* — on a document whose entire grade is **E1**, holding up when pushed on every number. There is exactly one sentence in it worth having, and it is optional; it is drafted at the end in case the author overrules this.

---

## What the paper actually is

**Problem.** Given a fixed pool of per-domain SFT sets already known to be individually good, naive concatenation produces imbalanced capabilities ("the bucket effect"), and nobody knows how much of each domain to include.

**Method.** A bi-level problem. Introduce `β ∈ ℝⁿ`, one scalar per domain, where `β_i > 0` upsamples domain *i* and `β_i < 0` downsamples it (Eq. 1). Outer objective is the loss on a small held-out **reference set** `D_ref`, `min_β Q(β) := L(D_ref, θ*(β))` (Eq. 2). Lemma 1 gives `∂θ*/∂β_j` as an inverse-Hessian–gradient product (Eq. 4), so at `β = 0` the per-domain influence is `−(∂L(D_ref,θ*)/∂θ*)ᵀ ∇²L(D_tr,θ*)⁻¹ ∇L(D_j,θ*)` (Eq. 5). The Hessian is made tractable by K-FAC: block-diagonal per MLP layer, `Hˡ ≈ E(xˡxˡᵀ) ⊗ E(δˡδˡᵀ)` (Eq. 6), then eigendecomposed (Eqs. 7–8), keeping only low-variance ("important") layers. Because dropping layers shrinks the magnitude, a **hand-set scaling constant `m`** rescales the result so the largest `|β|` equals `m` exactly: `γ = m / max|α|`, `β = −γ⊙α` (Eq. 9). Algorithm 1 then loops: train → evaluate → compute β → resize each domain by `(1+β_i)` via random up/down-sampling → repeat.

**The load-bearing consequence of Eq. 9, which the paper never states:** the domain with the largest influence *always* moves by exactly `±m`, whatever the gradients are. The step size is not learned; it is a hyperparameter, and the "optimisation" is a fixed-magnitude nudge in a gradient-ranked direction.

## Implementation nits

| Item | Value (Appendix A, "Training Setting") |
|---|---|
| Base model | **LLaMA-3.1-8B**, full fine-tuning (not LoRA) |
| Batch size / LR | 256 / max **2e-5**, **cosine decay** |
| Epochs | **1 and 3** (both reported) |
| Hardware / eval | **8×A100** / OpenCompass |
| Seeds | *"each experiment is repeated 5 times, and the average value is calculated"* — **means only, no spread published anywhere** |
| IDEAL hyperparameters | `m = 0.15`, sample factor `σ = 0.5` |
| §4.2 training set | math 10.0k (GSM8K + GPT-4 CoT) · code 5.3k (sampled from Tulu-Code 35k) · reasoning 6.5k (BBH, answers regenerated by GPT-4) · instruction 2.0k (IFEval + WizardLM Evol-Instruct) = **23.8k samples** |
| §4.3 training set | 5 domains × ~5k = **~25k**; control `D₀(FULL)` ≈ **66k**; TrustAI = TruthGen + GPT-4 CoT |
| Token budget | **never reported, in any unit.** [INFERENCE] at a generous 1k tokens/sample the §4.2 set is ~24M tokens — **~87,000×** smaller than our 2.080T |
| Sequence length | never stated |
| Code | **not released** |

Note that three of the five training sets are **GPT-4-regenerated or GPT-4-authored** (reasoning, math CoT, TrustAI), which the Limitations appendix half-concedes: *"the method relies on high-quality training datasets."*

## Every quantitative result

**Table 1 (§4.2, 4 benchmarks: GSM8K / HumanEval / BBH / IFEval).** Base model average 39.55.

| Setting | Joint `D₀` | Random | DoReMi `D₁`/`D₂` | DOGE `D₁`/`D₂` | **IDEAL `D₁`/`D₂`** |
|---|---|---|---|---|---|
| Epoch=1 | 54.79 | 55.64 / 54.21 | 53.82 / 55.17 | 54.71 / 53.37 | **56.28 / 57.87** |
| Epoch=3 | 55.35 | 55.97 / 54.76 | 55.05 / 56.25 | 55.96 / 56.87 | **58.05 / 59.23** |

- **The headline "7%" is relative, on epoch=3 only:** 55.35 → 59.23 = **+3.88 absolute = +7.01% relative**. At epoch=1 it is +3.08 absolute = +5.62% relative. Verified arithmetic.
- **6 of the 12 non-IDEAL mixture-perturbation cells land *below* the un-tuned Joint blend** (Random² and DoReMi-`D₁` at both epoch settings, DOGE-`D₁` and DOGE-`D₂` at epoch=1). All 4 IDEAL cells are above. This is the paper's real contribution and it is a *negative* result about the other methods.
- Best single cell: HumanEval **50.61** (IDEAL `D₂`, epoch=1) vs Joint 41.26 vs base 27.44.
- Specific-SFT single-domain models collapse elsewhere: math-only scores **0.00** HumanEval; code-only scores **2.99** BBH at epoch=1 (base 62.13).

**Table 2 (§4.3, 5 domains, 8 benchmarks).** Base avg 30.54; Joint `D₀` (~25k) **54.03**; Joint `D₀(FULL)` (~66k) **53.94**; IDEAL `D₁` 54.58, `D₂` **55.20**.
- **Data volume matters little:** 2.8× more data (25k → 66k) moved the average **−0.09**. This is the cleanest result in the paper.
- **The gain attenuates 3.2× when the basket doubles:** +7.01% relative / +3.88 absolute on 4 benchmarks → **+2.17% relative / +1.17 absolute** on 8. Verified; the paper states "only 2.1%" itself and attributes it to `D_ref` becoming "more generalized, potentially losing the unique characteristics of individual datasets" — i.e. it is conceding reference-set specificity drives the headline number.

**Table 3 (volume-matched control).** Upsampling DoReMi/DOGE to IDEAL's token volume: DoReMi 55.17 → 55.36, DOGE 53.37 → 53.81, both still far under IDEAL 57.87. So IDEAL's win is not merely "more data" — a well-designed control, and it is the one place the paper defends itself properly.

**Table 4 (§4.3 β values and sizes).**

| | Math | Code | Reason | Instr | TrustAI |
|---|---|---|---|---|---|
| "β" (×10⁻⁵) `D₁` | 7.34 | **84.30** | 15.74 | 18.02 | **−5.80** |
| "β" (×10⁻⁵) `D₂` | 4.24 | **73.24** | 13.45 | 15.74 | **−4.17** |
| #Size `D₁` | 4.9k | 5.5k | 4.9k | 4.9k | 4.7k |
| #Size `D₂` | 4.9k | **6.3k** | 5.0k | 5.1k | 4.7k |

Code is the only domain the method ever really moves (+14.5% per iteration, 5.5k→6.3k); TrustAI is the only one cut. Reconstructed exactly: applying `γ = 0.15/max|α|` to the tabulated values gives `β_D2 = [0.0087, 0.15, 0.0275, 0.0322, −0.0085]`, and `D₁ × (1+β)` predicts `D₂` as `[4.94, 6.33, 5.04, 5.06, 4.66]k` against the reported `[4.9, 6.3, 5.0, 5.1, 4.7]k` — **max error 0.043k across all five domains.**

## Figures — all five inspected from pixels

**Figure 1 (`figs/data_distribution.png`) — schematic, contains no data.** A rendered 3-D "Data-proportion Space" loss surface (red peaks → green valleys), axis labelled `loss` rising from an origin `O` with two unlabelled proportion axes. **No tick values on any axis, no units, no error bars.** A blue triangle ("Random Initial Situation") sits above a purple star ("Optimized Situation") inside a dashed ellipse annotated "Case1", with a downward arrow between them. Below: two boxed bar charts over `D1 D2 D3 D4`, equal-height before, unequal after (D1 up, D2 down, D3 mid, D4 down), joined by a black arrow labelled "IDEAL". **Actual claim:** cartoon — IDEAL moves proportions downhill in loss. Nothing measured; this is an illustration, not evidence.

**Figure 2 (a)–(d) — the `m` sensitivity study, `D₁(IDEAL)`, 1 epoch.** Four separate bar charts, identical construction: y-axis labelled **`Metric`**, x-axis ticks `0 1 2 3` (bar index only — *not* a variable), shared legend `Joint SFT` (pink) / `IDEAL(m=0.3)` (pale yellow) / `IDEAL(m=0.15)` (teal) / `IDEAL(m=0.1)` (purple), value printed above each bar, dashed horizontal gridlines. **No error bars in any panel**, despite 5 runs per cell being averaged. Every y-axis is **truncated well above zero**, which visually magnifies small gaps.

| Panel | y-axis range / ticks | Joint SFT | m=0.3 | **m=0.15** | m=0.1 |
|---|---|---|---|---|---|
| (a) Mathematics | 63–70, step 1 | 66.62 | 67.58 | **68.01** | **65.50** |
| (b) Reasoning | 71.0–75.0, step 0.5 | 72.92 | **73.07** | 72.82 | 72.97 |
| (c) Instruction | ~35.5–41.5, step 1 | 38.36 | 38.35 | **39.78** | 37.71 |
| (d) Coding | ~39–47, step 2 | 41.26 | 42.68 | **44.51** | 41.68 |

**Actual claims, read from the pixels:**
1. The four panels average to **54.79 (Joint), 55.42 (m=0.3), 56.28 (m=0.15), 54.47 (m=0.1)** — and 56.28 / 54.79 reproduce Table 1's `D₁(IDEAL)` and Joint epoch=1 rows **exactly**, so Figure 2 is internally consistent with Table 1.
2. **`m = 0.1` is worse than doing nothing: 54.47 vs Joint SFT 54.79 (−0.33).** An under-aggressive reweighting step is worse than not reweighting. The paper describes this only as "marginal gains", never as a regression below baseline.
3. **Panel (b) Reasoning: the recommended setting is the *worst* of the four bars** (72.82, below Joint's 72.92). The recommendation is an average-of-four decision that loses on one of the four domains — on a 4.0-point y-range with no error bars, so it is indistinguishable from noise either way.
4. Response to `m` is **non-monotone** with an interior optimum, on **three points** (0.1, 0.15, 0.3), n=5 averaged, no spread. This is the entire basis for `m = 0.15`, which then propagates to every headline number.

## Ablations, including the failures

- **`m` sweep** (Fig. 2): non-monotone, interior optimum, and the smallest setting **regresses below baseline**. Stated conclusion: *"The choice of m should be neither large nor too small."*
- **Volume-matched control** (Table 3): IDEAL's edge survives equalising data volume. Genuine and well-designed.
- **Volume vs distribution** (Table 2): 66k vs 25k = **−0.09**. Genuine.
- **Basket-breadth** (Table 2 vs Table 1): +7.01% → +2.17% relative. Reported honestly, and the most transferable thing in the paper.
- **Epoch=3 HumanEval regression:** best HumanEval falls 50.61 (ep=1) → 46.34 (ep=3).
- **Estimation-error appendix (C)** concedes three error sources: the model is *not* trained to the optimality Eq. 1 assumes; K-FAC block-diagonalisation is lossy; and `σ = 0.5` random subsampling injects bias. No sensitivity analysis for any of the three.

## Internal inconsistencies found

1. **Table 4's column labelled "β (×10⁻⁵)" cannot be the applied β.** Eq. 9 forces `max|β| = m = 0.15` by construction, and the observed Code volume change is **+14.5%** — consistent with `β_code = 0.15`, not with `8.43e-4`. The tabulated values are the pre-scaling gradient `α = ∂Q/∂β`. Mislabelled, and with no code release this is a reproducibility gap.
2. **The paper is inconsistent about whether total volume is held fixed across iterations.** `D₁ → D₂` reconstructs by direct application of `(1+β)` with **no** renormalisation (max error 0.043k). `D₀ → D₁` only reconstructs if the total is renormalised back to ~25k (or if `D₀` was ~4.8k/domain, not the stated 5k). Meanwhile §5.2 says the §4.2 total *grew* (23.8k → 25.3k, +6.3%). Three different volume conventions in one paper.
3. **The epoch/HumanEval claim is contradicted by its own table.** §4.2: *"This trend is also observed in the results of the Specific SFT models trained for three epochs, where the upper limit of scores on the HumanEval benchmark decreases as the number of training epochs increases."* Table 1's Specific/Coding HumanEval goes **37.20 (ep=1) → 41.46 (ep=3)**, an *increase*. Only the cross-method maximum falls.

## Threats to validity against a 2.0T / 120B seven-lane multilingual run

1. **Objective mismatch.** IDEAL optimises loss on a held-out *instruction* reference set after SFT. Our object is next-token CE over a 2.080T pretraining corpus with a decay leg. Nothing in Lemma 1 survives the change of objective.
2. **Scale.** 8B params / ~24M tokens [INFERENCE] / 1–3 epochs vs 120B / 2.080T. The method requires a full train-to-convergence per iteration; at our scale one iteration *is* the run, so the algorithm is inapplicable by construction — it is only cheap because SFT is cheap.
3. **Assumption 1 requires training to optimality.** Pretraining never reaches it, and Appendix C admits the gap even at SFT scale.
4. **`β` cannot express any commitment we actually make.** It is a single scalar per domain with no floor, no ceiling, no per-bucket or per-cycle constraint, no ordering, and no notion of a reserve. `SOLUTION.md` §5's per-lane real-token floor and §4's held-back reserve are inexpressible in it.
5. **Sample counts, not tokens.** Every quantity is `#Size` in thousands of samples. Our entire spec is token-denominated; there is no conversion.
6. **No scarcity regime.** All five domains have ample supply and are resized ±15% freely. Our binding problem is a lane at **73.4× demand over 0.627B unique**. IDEAL never encounters, models, or bounds a supply-limited lane.
7. **Reference-set overfitting is the method's mechanism, not a side effect.** `D_ref` *is* the objective, and the paper's own Table 1-vs-2 comparison shows the win shrinking 3.2× as `D_ref` broadens. Any transplant would inherit that.

## Two traps — arguments this paper looks like it supports, and does not

1. **Do NOT cite the `0.00` HumanEval / `2.99` BBH single-domain collapses as evidence for §5's protected floor.** Those are SFT catastrophic forgetting from fine-tuning an already-pretrained 8B model on 5.3k code samples for 1 epoch — not a pretraining lane being starved. `SOLUTION.md` §5 already carries Spark Joy's sans-math arm (MMLU 29.71 vs 35.69, RC 26.48 vs 37.02) from a **100B pretraining final phase at 7B**, which is the right object at the right scale. Swapping in IDEAL would trade a good citation for a bad one.
2. **Do NOT cite IDEAL for the 4-epoch repetition ceiling.** It is a bare re-citation of Muennighoff with no measurement attached. Cite the primary instead (next section).

## Follow-on citations that WOULD change one of our ten numbers

Three are worth chasing; all three are in IDEAL's bibliography and none is in the nine-paper evidence base. **Pointer 1 is already in flight** — a sibling agent has `papers/scaling-dc/` holding `2305.16264v5` (Muennighoff et al.), so do not double-dispatch it; the value of listing it here is that IDEAL independently identifies it as the load-bearing primary for our most-reused number.

1. **Muennighoff et al., "Scaling Data-Constrained Language Models", NeurIPS 36:50358–50376, 2023 (arXiv 2305.16264)** — IDEAL's ref [43], invoked for *"repeating existing data up to four times yields a performance improvement that is largely equivalent to introducing the same amount of new data."* **This is the primary for the 4-epoch ceiling that `SOLUTION.md` leans on in four places** — §1.2 (trace-shaped pool at 4.00 epochs), §3 (the whole 4-vs-6-epoch defensible-band table, and `2.508B = 0.125% of 2T`), §4 (long-trajectory reserve at 3.89 epochs "inside the 4-epoch ceiling"), §5 (627M pool at ≥4 epochs) — and it is also, on its face, the source of widget 1's `≤4×` "needs repetition" classifier threshold. Neither `SOLUTION.md` nor `EVIDENCE_MAP.md` cites it; the ceiling is currently defended by Two-Phase's 6/8-epoch results and the course widget. Reading it would put a primary, in-scope, pretraining-scale citation under our single most-reused number, and it also carries a repeat-value decay curve that could sharpen the 4-vs-6 band directly. **Highest-value pointer in this paper.**
2. **Chung et al., "UniMax: Fairer and More Effective Language Sampling for Large-Scale Multilingual Pretraining" (arXiv 2304.09151)** — a low-resource **multilingual pretraining** mixture paper built on an explicit **per-language epoch cap** rather than temperature sampling. That is precisely the instrument our Indic tier split needs: `SOLUTION.md` §2 concedes *"no paper here studied Indic"* and prices tier C at **5.06×** repetition on 5.0B of parallel corpora (weakness #2), with tier A at 1.98× and B at 2.11×. A published epoch-capped multilingual sampler would give the tier table a real precedent instead of a hazard list. **Second-highest-value pointer.**
3. **Chen et al., "Take the Bull by the Horns: Hard Sample-Reweighted Continual Training Improves LLM Generalization" (arXiv 2402.14270)** — named here from IDEAL's bibliography only; **not read**, so this is a lead, not evidence. It matters because weakness #6 (the B0–B5 difficulty ladder) is the one place `SOLUTION.md` §6a admits *"no paper supports a content-difficulty ladder and one argues against it."* A **continual-pretraining** paper that reweights by sample *hardness* is the closest published object to that ladder. Read it with a specific question: if its hardness signal is loss- or perplexity-based, it **reinforces** Preference Curriculum's objection (§6a: *"a perplexity gap is not a difficulty axis"*) rather than rescuing the ladder — in which case §6a's honest-limits paragraph gets stronger, not weaker. Either outcome changes what §6a can claim.

Also present in the bibliography: **"Data, Data Everywhere: A Guide for Pretraining Dataset Construction" (arXiv 2407.06380)** — **assessed separately as `emnlp596`; see that brief, which returned KEEP.** I had classified it from its title alone as a generic construction guide; that judgement is withdrawn. The sibling agent that read it in full reports it as the strongest evidence anyone has produced on the Indic gap — named Indic languages with token counts (9 Indic = exactly 6.00B of a 541.4B multilingual web pool), a measured epoch penalty on small sources that **challenges our tier C at 5.06×** (weakness #2), and independent corroboration of §5's Indic floor at exactly **1.00 epoch**. Route it through `emnlp596`, not through this brief. Genuinely lower value: DoReMi (Xie et al., NeurIPS 36, 2024 — no arXiv id given in this paper's bibliography) and DOGE, both already covered via the CLIMB brief; MATES (2406.06046) and Zhang et al. (2409.16986), pretraining data *selection* rather than mixture. **Nothing** in the bibliography concerns agentic/tool-use trajectory data at pretraining scale, multi-document long-context data, or measured anneal lengths — the three areas where we most need supply.

## If the drop is overruled: the only defensible sentence

One clause, in §7 beside the existing Spark Joy noise band, tagged as out-of-scale — and it is a caveat on our own protocol, not a defence of a share:

> A mixture win measured on a narrow basket is partly a property of the basket: IDEAL's multi-capability SFT search reports **+7.01% relative (+3.88 absolute)** over uniform blending on four benchmarks and only **+2.17% relative (+1.17 absolute)** on eight, a **3.2× attenuation** from broadening the reference set alone (2505.12762, Tables 1–2) — so H1–H7's thresholds are stated on the specific metric each hypothesis names, and a lane that wins its own metric while losing the core average is treated as refuted, not confirmed. *(Scale caveat: that is SFT on LLaMA-3.1-8B over ~24k instruction samples, ~5 orders of magnitude below this run and on a different objective; it is cited for the measurement hazard only, not for any share.)*

If §7 does not need this — and it largely does not, since Spark Joy's `n=1` 0.60pp/0.86pp band and the "inconclusive probe is not evidence for the plan" rule already cover the same ground — then **cite nothing from this paper.**
