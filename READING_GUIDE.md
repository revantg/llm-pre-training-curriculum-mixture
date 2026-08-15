# Reading Guide — which papers actually solve this assignment

Fourteen papers were read in full for the Session 5 mixture-and-curriculum spec. This ranks them by **what changed a number in `session_5_era_v5/SOLUTION.md`**, not by general quality.

If you are writing this assignment yourself, the short answer is at the bottom: **read three papers**.

---

## Tier 0 — prerequisite, not a scoring paper

### 0. Training Compute-Optimal Large Language Models (Chinchilla) — `2203.15556`
*Hoffmann et al., DeepMind 2022* · **not read for this spec; no brief on disk**

Read this only if you intend to *defend* the constants you quote from `2305.16264`. It changes no number here, and no assignment clause asks for a compute-optimality argument — but it is the functional form everything else is fitted to:

```
L(N, D) = E + A/N^alpha + B/D^beta
```

The spec quotes **A = 521, B = 1488, E = 1.87, alpha = beta = 0.3527** from Muennighoff. Those are parameters *of Chinchilla's equation*. You can cite them without reading this paper; you cannot answer "what is B?" without it.

**A cautionary note from our own process.** An earlier draft claimed 2.000T was "0.83x compute-optimal, since Chinchilla-optimal for 120B is about 2.4T." That came from the remembered ~20-tokens-per-parameter heuristic, and the red team correctly flagged it as folklore in a document graded on sourcing. The repair was not to read Chinchilla but to use Muennighoff's **fitted** relation `U_N = 0.051 * U_D`, giving 2.353T and therefore **0.85x**. The heuristic was nearly right (120B x 20 = 2.4T); its provenance was not.

**The limitation is the useful part.** Chinchilla assumes **unique, single-epoch** data — its framework presumes you have enough tokens. That assumption is precisely what fails on a 0.627B agentic pool against 40B of demand, and it is why `2305.16264` had to be written. Reading Chinchilla shows you where this assignment's central problem starts.

**Read:** sections 3-4 and the parametric fit. Skip the Chinchilla-vs-Gopher benchmark tables.
**Do not read Kaplan et al. `2001.08361`** first — Chinchilla supersedes it, and starting there is a reliable way to absorb the wrong token-to-parameter ratio.

| | |
|---|---|
| Changes a number in this spec? | No — `2305.16264` covers the one place it would |
| Needed to *defend* a number? | Yes — you cite its functional form |
| Required by any assignment clause? | No |
| Order | Before Tier 1, if at all. The fourth paper you read, not one of the first three. |

---

## Tier 1 — the three that decide the shape of your answer

### 1. Scaling Data-Constrained Language Models — `2305.16264`
*Muennighoff et al., NeurIPS 2023* · brief: `papers/scaling-dc/brief.md` (489 lines)

The single most useful paper in the set. It fits a closed form for the value of a repeated token:

```
D' = U + U·R*·(1 − e^(−R/R*))        R* = 15.387756
```

fit on **182 runs, 7M–9B params, 1–500 epochs** (A=521, B=1488, E=1.87, α=β=0.3527), where `R` is repetitions beyond the first.

The constant that matters is the **asymptote**: `U·(1 + R*) = 16.39·U`. A pool can never contribute more than 16.39× its unique tokens, however often you repeat it.

**What it does for the spec.** It converts the agentic problem from a vague ratio into a hard statement: a 0.627B pool yields at most **10.28B** effective tokens ever, against 46.0B of demand, so **≥78% of that lane must be generated regardless of epoch count**. Repetition can close only 21 percentage points. It also replaces remembered Chinchilla with their fitted `U_N = 0.051·U_D` → 120B is compute-optimal at **2.353T**, so 2.000T is 0.85×.

**Caveat to carry.** The un-approximated form fits marginally better (R² 0.7988 vs 0.7722) and implies a cap nearer 95×, so 16.39× is the conservative of two near-equivalent fits. The extrapolation axis is **model scale** — the fit tops out at 9B.

**Read it first. It tells you whether your plan is fundable before you write it.**

### 2. Two-Phase Pretraining — `2412.15285`
*NVIDIA / Stanford / BU* · brief: `papers/two-phase/brief.md`

Three separate assignment requirements in one paper.

- **Order** is worth **+1.74 absolute** average at identical weights (52.86 vs 51.12), and it lands on sharp capabilities — GSM8K 30.86 → 40.33, code 35.55 → 38.33 — while MMLU stays flat. The commonly-quoted "+3.4" is that same gain expressed as a *relative* percentage.
- **Epoch ceilings**: 6 for high-quality crawl, 8 for math, 12 hurts. Superseded as a mechanism by `2305.16264`, but it frames the question.
- **Web quality**: CC is 64.44% Low under their 5-bucket classifier; zeroing Low and upsampling High lifts MMLU **42.94 → 56.10**. The same ablation costs code 19.25 → 17.41, so apply it to web only.

Closest published analogue to main-run-vs-anneal.

### 3. Mid-Training of Large Language Models: A Survey — `2510.06826`
brief: `papers/midtrain-survey/brief.md` (231 lines)

Fastest value per page. It resolves the biggest apparent contradiction in the literature — **4% anneals vs 40% second phases are two different objects**:

- **Cluster A, terminal fast-decay, 1–5%**: MiniCPM 1.96%, Hunyuan-A13B 1.48%, OpenCoder 3.85%, Pangu 4.00%, Hunyuan-Large 4.76%
- **Cluster B, full second stage, 9–51%**: SmolLM2 9.03%, Qwen3 14.08%, Zamba 51.28%

Plus 17 named frontier recipes with real token counts, and the 10–40% new-on-old overlay convention. Also the best *map* into everything else. It has no experiments — treat every number as second-hand and chase the primary if you lean on it.

---

## Tier 2 — each fills a specific required slot

### 4. OpenCoder — `2411.04905`
brief: `papers/opencoder/brief.md`

The only complete published cookbook end to end. ~75% of GitHub files are exact duplicates; **file-level dedup keeps 32.74B Python tokens and beats repo-level's 99.47B at every matched budget**. The anneal is 100B after 2.5T with **84% original-distribution ballast**, 12.44B algorithmic, 2.71B unit-tested synthetic. Removing the high-quality slice stalls HumanEval at ~0.33 instead of reaching ~0.47, permanently. **`stars>=5` filtering hurts** — lower training loss, worse benchmarks.

### 5. Demystifying Synthetic Data — `2510.01631`
brief: `papers/synthetic/brief.md`

Your ceiling on generated data, and it is **type-dependent**:

| Type | What it is | Safe ceiling |
|---|---|---|
| Rephrase | rewrite a **real** document | ~30%, always <50% |
| Textbooks | invent from keywords | **≤3%** at 50B, often 0% |

Also: an **8B generator beats 3B, and 70B does not beat 8B**. Without this you have no principled bound on either a synthetic Indic tier or an agentic generation program. Note "~30%" is interpolated — their grid runs 20% then 50%.

### 6. Dataset Decomposition — `2405.13226`
*NeurIPS 2024* · brief: `papers/dataset-decomp/brief.md` (235 lines)

Long-context capability is a **threshold, not a gradient**: multi-document QA is ≈0 until training sequences exceed the eval context, then jumps and flattens. Any mixture lacking the 4k/8k buckets scores 0.0–0.4 on MDQA-20/30.

The reframe that matters: **natural web already supplies 9.4% of tokens at exactly 8192** and 22.9% at ≥4k, *if you decompose documents into power-of-two spans instead of concat-and-chunk*. Three wins that cost nothing — short→long ordering (**+5.0 MDQA-30**), RoPE base 100k (**+5.4**), and decomposition itself (+2.9 regular / +3.4 long-context).

### 7. Does your data spark joy? — `2406.03476`
*Databricks Mosaic* · brief: `papers/spark-joy/brief.md` (225 lines)

The anneal-length sweep nobody else ran: **50B / 100B / 200B / 300B** (5/10/20/30% of 1T). MMLU peaks at 100B, core average at 200B, and **no point below 50B exists**.

Best argument for protecting a lane *inside* the anneal: their sans-math arm drove MMLU to **29.71 against a 35.69 baseline (−5.98)** and Reading Comprehension to 26.48 vs 37.02 (−10.54). **A short final phase can actively unlearn a lane it stops feeding.**

Important framing caveat: they never changed the learning rate. Under pure rsqrt the final leg ran at ~89–100% of cruising LR, so this prices a *mixture swap*, not a *decay leg*.

---

## Tier 3 — read these only because this assignment is Indic

### 8. Data, Data Everywhere — EMNLP 2024 main, pp. 10671–10695 (`2407.06380`)
*Parmar et al., NVIDIA* · brief: `papers/emnlp596/brief.md` (375 lines, **with `verify.py`**)

The only real Indic evidence in the entire set. Table 12 lists 52 languages with token counts, 9 of them Indic, totalling **6.00B** = 1.108% of their multilingual pool. Their 32-language parallel corpus contains **Hindi as the only Indic language** (0.655B), with zero Bengali, Tamil, Telugu, Marathi, Malayalam, Kannada, Nepali or Urdu.

It also killed a defence we were relying on: a UniMax epoch cap on English at 8B/300B found **N=1 beats N=2 and N=4** (MMLU 28.30/28.00/26.60) over sources spanning 18.7B down to 1.5B. **Confounded** — raising the cap also flattens toward uniform, and the authors give both explanations — so cite it for direction only, and never against synthetic data, which they explicitly disclaim.

Bonus findings: DoReMi drove 64.38% of a 300B budget onto a single 14.0B source (13.80 epochs) and finished worst of five arms. MMLU is reported **only at 8B**, "when the experimental setting allows for a non-random score." Their quality classifier agrees monotonically with **KenLM n-gram perplexity** — a cheap, script-agnostic substitute for an English classifier.

### 9. UniMax — `2304.09151`
*Chung et al., ICLR 2023* · brief: `papers/unimax/brief.md` (440 lines)

The **mechanism**, not a number. Sort sources ascending by size, give each `B/(|L|−i)`, clamp anything exceeding `N` epochs, let freed budget flow up the ranking. Shares become an *output* of one declared cap instead of four hand-picked percentages.

Their own sweep (1.2B, TyDi QA): N=1 **82.2**, N=5 81.5, N=10 81.8 — and N=2, 3, 4 were never run.

**Read 8 and 9 together.** Their strongest joint finding: the only two disclosed builds that publish per-language Indic volumes both serve Indic at **exactly 1.00 epoch**, in both cases because the cap binds — umT5 at 48.2B of a 48.4B pool, NVIDIA at 6.00B of a 6.00B pool.

---

## Tier 4 — read for the negative result

### 10. CLIMB — `2504.13161`
brief: `papers/climb/brief.md`

The sharpest floor argument available: **a lane absent from the search objective goes to exactly zero** (their code cluster C20). Also underwrites a cheap proxy plan — a 62M proxy ranks mixtures nearly as well as 350M (60.11 vs 60.41). It does **not** hand you lane percentages; its continuous-pretrain regime differs from a from-scratch run, and it says so.

### 11. A Pretrainer's Guide to Training Data — `2305.13169`
brief: `papers/pretrainers-guide/brief.md` (317 lines)

**Not** a repetition paper despite frequently being cited as one — no epoch experiment exists in it. 28 pretraining runs at **1.5B**, the closest published scale-match to a 1B/3B proxy plan, so its methodology admissions transfer even where its findings do not: single-shot, no seed replication, no error bars, and its own results cannot resolve below ~±0.5pp.

Two real findings: **heterogeneity beats targeted data even on targeted evals** (removing Common Crawl costs Academic QA −5.9, while removing *Academic* improves it +2.2), and **aggressive quality filtering peaks at removing only ~9%**.

### 12. Preference Curriculum — `2501.13126`
brief: `papers/pref-curriculum/brief.md` (208 lines)

Read it to avoid the obvious mistake. A perplexity gap is **not** a difficulty axis — their "hard" half requires *less* scientific content (0.61 vs 0.70) with logical-reasoning requirement identical at 0.72/0.72. And ordering alone silently re-times whole domains with no floor: **88% of arXiv and 66% of GitHub land in the first half, 86% of Wikipedia in the second**, while the text claims no skew.

### 13. Model Collapse — `2404.05090`
brief: `papers/collapse/brief.md`

Constrains rather than informs. Fully synthetic self-training collapses almost surely; mixing the same real corpus every generation bounds the drift. But the only neural evidence is an 8×256 char-level nanoGPT on one Shakespeare play, vocab 65 — the weakest scale in the set. Use it for the *mechanism* (real tokens in every batch, never a closed loop), never for a percentage.

---

## Skip

**IDEAL — `2505.12762`.** Instruction-tuning data selection: LLaMA-3.1-8B, 23.8k–66k samples, 1–3 epochs. Wrong side of the pretraining boundary. It moves no mixture or curriculum number. Brief retained at `papers/ideal/brief.md` documenting why.

---

## If you are writing this yourself

**Read three: Scaling Data-Constrained → Two-Phase → Mid-Training Survey.** That is enough for a good spec. If you want a fourth, make it **Chinchilla (Tier 0)** — not for a number, but so the constants you quote from the first paper are defensible. Add OpenCoder and Demystifying Synthetic and it becomes excellent. Everything after that is defence-hardening.

**But start at `session_5_era_v5/papers/EVIDENCE_MAP.md`, not the papers.** The 14 briefs are dense rather than summary-level: figures described from pixels, every number with its setting and location, and an explicit list of what each paper is **silent** on. `emnlp596` ships a zero-dependency `verify.py` (36 assertions) so its numbers are re-checkable without trusting the brief.

### The honest meta-point

None of these is primarily a *curriculum-ordering* paper. Ordering evidence is thin and will stay thin — Two-Phase for order-alone, CLIMB for breadth-early-concentrate-late, Dataset Decomposition for short→long.

What the literature actually gives you is **whether your curriculum is fundable, and whether you could tell if it worked.** `2305.16264` answers the first. `2305.13169` answers the second. That is where the marks are.

### Mapping to the assignment requirements

| Requirement | Papers that actually help |
|---|---|
| R1 lane shares | CLIMB (search, not values) · Two-Phase (blends) · Mid-Training Survey (17 recipes) |
| R2 Indic tiers | **Data, Data Everywhere** · **UniMax** · Demystifying Synthetic (the D-tier ceiling) |
| R3 slots → inventory | none — this is your own inventory arithmetic |
| R4 protected floor | **CLIMB** (C20 → 0) · Pretrainer's Guide (heterogeneity) · Model Collapse (real tokens) |
| R5 anneal reserve | **Spark Joy** (length) · **OpenCoder** (structure) · Mid-Training Survey (taxonomy) |
| R6 difficulty + length bands | **none** — build from the course widgets; PrefCurriculum says what *not* to do |
| R7 1B/3B proxies | **CLIMB** (cheap proxies work) · **Pretrainer's Guide** (what is readable at 1.5B) |
| R8 cleaning starved slots | your own supply table |
| E7/E8 supply, repeat-or-generate | **Scaling Data-Constrained** (the asymptote) · Demystifying Synthetic (ceilings by type) |
| E11 confirm/refute metric | **Pretrainer's Guide** (±0.5pp floor) · Data, Data Everywhere (MMLU needs 8B) |
