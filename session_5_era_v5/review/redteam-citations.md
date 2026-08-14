# Red-team review — CITATIONS and EVIDENCE CHAIN
### Target: `SOLUTION_v3.md` (V5 Data Mixture & Curriculum Specification)
### Reviewer: RedTeamCitations · graded backwards from `local://rubric.md` (R0–R8 / E1–E11)

---

## 0. Verdict in one paragraph

This is the most heavily-evidenced version of this document I have seen, and most of its numbers survive a direct check against the nine briefs. **That is not the problem.** The problem is threefold. (1) **Two whole requirements are absent**: R6/E10 (difficulty *and* reasoning-length bands, each with a concrete example — stated **twice** in the assignment, so double-weighted) and R8 (point cleaning at the starved slots — the string `clean` appears **zero** times in the spec). (2) **R3 fails for two of the three slots it explicitly names**: the agentic slot cites all nine inventory datasets with token counts, but the **reasoning** and **long-context** slots cite *no* inventory dataset at all — `OpenThoughts2`, `OpenMathReasoning`, `NuminaMath`, `OpenR1-Math`, `AON`, `Repo-packed code`, `Book-length corpora` appear **zero times**. (3) **Fourteen findings are FATAL**, of which **five are citation-level**: a relative-percentage gain presented as absolute points (`+3.4` should be `+1.74`), a four-number series attributed to the wrong axis (Spark Joy Language Understanding), a misreported epoch maximum that contradicts its own next clause (Spark Joy 0.89/1.12), a commented-out LaTeX line quoted as a "Published analogue" (MiniMax-01), and one unsourced quotation (Nemotron-4).

Against E2 specifically — "you are grading the evidence chain itself" — the spec's failure mode is **not fabrication**. Exactly **one** quoted string in the whole document is untraceable to the evidence base (Nemotron-4's *"majority already-seen tokens reweighted"*, §4). The failure mode is **evidence that is real but attached to the wrong number**: papers measured at 1B on English web being used to price a 120B seven-lane mixture, and — worst under E6 — a benchmark column that is pure labelling, with the course's own ≥8% funding rule (`WEIGHTED_MIN=8`, widget 1) never once invoked, even though **two lanes sit below it**.

---

## 1. Arithmetic audit — recomputed from scratch

All recomputation done independently from the stage table and the course-given supply vector. Verified numbers are marked ✓.

### 1.1 What closes

| Check | Spec | Recomputed | |
|---|---|---|---|
| Stage rows Seed/General/Reasoning/Long-ctx sum to 100 | 100 each | 100 / 100 / 100 / 100 | ✓ |
| Time-average of stage profiles | — | 33.85 / 23.95 / 8.5 / 4.45 / 15.8 / 11.45 / 2.0 = **100.00** | ✓ |
| Demand at 2T | 677/479/170/89/316/229/40 B | identical (uses unrounded shares) | ✓ |
| Supply ratios | 0.15/0.44/2.00/0.89/1.14/0.92/63.5× | 0.150/0.435/2.000/0.890/1.145/0.916/63.49× | ✓ |
| Indic tiers 40/30/8/22 → 126.4/94.8/25.3/69.5B | 1.98/2.11/5.06/0.43× | 1.975/2.111/5.056/0.429× | ✓ |
| Composer default tier C: 63.2B / 5.0B | 12.6× | 12.64× | ✓ |
| Agentic unique 360M + 267M | 0.63B | **627M** exactly (widget 9) | ✓ |
| 4 epochs → 2.52B = 0.126% of 2T | ✓ | 2.508B = 0.1254% | ✓ |
| Agentic exposure 40 + 4.96 = 44.96B, ~94% generated | ✓ | 2.508/44.96 = 5.6% real | ✓ |
| Anneal component table sums to 80.0B | ✓ | 48+9.6+8+6.4+4+1.6+2.4 = 80.0 | ✓ |
| Anneal ballast 60% at main proportions + 40% adders | — | web 20.31 / code 22.37 / indic 21.48 / reason 15.10 / STEM 8.87 / agentic 6.20 / long 2.67 / synth 3.0 = **100.0** | ✓ |
| Anneal-leg epochs 0.062 / 0.142 / 0.021 / 0.028 | ✓ | 0.0623 / 0.1421 / 0.0216 / 0.0285 | ✓ |
| Agentic anneal epochs ~7.9 / ≈13.8 | ✓ | 4.96/0.627 = 7.91; 4.96/0.36 = 13.78 | ✓ |
| Main→anneal mixture shift ½·L1 | 19.5% | **19.48%** | ✓ |
| Spark Joy shift ½·L1 | 41.1% | **41.05%** | ✓ |
| Hunyuan 5% vs OPUS 40% = 8× stricter | 8× | 8× ✓ (**note: `EVIDENCE_MAP.md` line 83 says "10× stricter" — the spec is right, the evidence map is wrong**) | ✓ |
| Probe cost 6ND: 40B×120B = 2.9e22 vs 1.44e24 = 1/50 | ✓ | 2.88e22 / 1.44e24 = 1/50; 12 probes = 24% | ✓ |
| Cluster A percentages (all six) | 1.96/1.48/3.85/4.00/4.76/1.96 | all reproduce | ✓ |
| Kill-criterion 0.5% = 10B, 2.5B real, 75% synth | ✓ | ✓ | ✓ |

### 1.2 What does NOT close

**A1 — FATAL. The §1 table sums to 100.2%, not 100.0%.**
`33.9 + 24.0 + 15.8 + 11.5 + 8.5 + 4.5 + 2.0 = 100.2`. The sentence directly under the table — *"they sum to 100.0%"* — is **false as printed**. The underlying unrounded profile does sum to 100.00, so this is round-half-up inflation on four lanes at once, but **R1 is the requirement to state a share for every slot summing to 100** and the headline table fails it. A reviewer's first act is to add the column.

**A2 — FATAL. The §6 anneal row sums to 97, and §6 claims "Each row sums to 100%".**
`20+22+15+3+22+9+6 = 97`. The missing 3 is the *verified-synthetic* bucket from §4, which has no column in the §6 table. Reconcilable, but as printed it is a broken table with a false claim attached.

**A3 — FATAL. `+3.4 average` is a RELATIVE percentage presented as absolute points, in a list of absolute points.**
§6: *"Order alone, at identical weights, is worth **+3.4 average** — … GSM8K **30.86 → 40.33**, code **35.55 → 38.33**, MMLU essentially flat (56.49 → 56.28)"*.
Two-Phase Table 4: Two-Phase avg **52.86** vs BASE-RO **51.12**. `52.86 − 51.12 = +1.74` absolute. `52.86/51.12 − 1 = +3.40%` relative. The companion figure in the same brief confirms the convention: *"Compounded two-phase vs ND: **+17%** (52.86 vs 45.17)"* — 52.86/45.17 = +17.0% relative, absolute +7.69.
So the headline ordering gain is **+1.74 points, not +3.4**, and it is printed immediately beside `+9.47` and `+2.78` absolute deltas. This is the single most misleading number in the document. Inherited verbatim from `two-phase/brief.md` line 49, which writes "+3.4 avg" without the `%`.

**A4 — FATAL. Spark Joy's Language Understanding series is attributed to the wrong axis.**
§4: *"Language Understanding was still negative at every phase length (**−0.47 / −1.11 / −1.44 / −1.17** on **LAMBADA / HellaSwag / Winograd / WinoGrande**)"*.
Those four numbers are the deltas at the **four phase lengths** (5% / 10% / 20% / 30% = 50 / 100 / 200 / 300B), i.e. `61.52 → 61.05 / 60.41 / 60.08 / 60.35` (spark-joy brief, phase-length sweep table). LAMBADA / HellaSwag / Winograd / WinoGrande are the *constituent tasks* of the Language Understanding **category** — the paper publishes **no** per-task breakdown. The spec has fused two separate facts into a fabricated per-benchmark table. The conclusion drawn is still correct; the evidence as presented does not exist.

**A5 — FATAL. Spark Joy epoch "peak" is wrong, and it contradicts the next clause of its own sentence.**
§4: *"their Domain-Specific bucket **peaks at 0.89 epochs** and Code at **1.12** across the whole run"*, then immediately: *"the 30% arm, **where the reserve first crosses 1.0 epoch**"*.
Both cannot be true. Per the derived epoch table (spark-joy brief): Domain Specific = 0.50 / 0.60 / 0.69 / **0.89** / **1.08**; Code = 1.00 / 1.03 / 1.06 / **1.12** / **1.18**. The **peaks are 1.08 and 1.18** (30% arm). 0.89 / 1.12 are the **20%-arm** values. Also — the brief flags that *"The paper does not publish this table; it follows from Tables 2 and 4"* and that the 30%-arm regression is *"a correlation, not their claim (they attribute the regression to distribution shift)"*. The spec calls it **"Spark Joy's finding"**. It is the brief author's derivation, presented as the paper's result.

**A6 — FATAL. "Published analogue" is a commented-out LaTeX line that is not in the published paper.**
§6: *"**Published analogue:** MiniMax-01 uses **linear interpolation of source-specific weights** across mixture transitions."*
`midtrain-survey/brief.md` line 140: this string is *"commented in `4_long_context.tex`"* and the brief's explicit warning (line 229) is: *"several of the most quotable numbers … exist **only as commented-out LaTeX in the arXiv source and are absent from the published paper** — quoting them as survey text would be a citation error."* The spec cites no source at all and labels it **"Published"**. It may be defensible from the MiniMax-01 primary (2501.08313), but as written it is a citation error the brief pre-warned against.

**A7 — FATAL (internal contradiction). "Long-context stays ≥4% regardless" is violated by the spec's own anneal.**
§7.5 declares an unqualified floor: *"Long-context stays **≥4%** regardless, because 0% is the one setting proven catastrophic."* The §4 effective anneal mixture puts long-context at **2.7%**, and the §6 anneal row at **3%**. The spec breaks its own declared kill-criterion floor in the very mixture it ships.

**A8 — FATAL (unaddressed arithmetic). The supply table ignores OPUS's own 40% acceptance rate.**
§Header: *"OPUS, keep ~40% of candidates"*. §5: the floor exists precisely because *"an English-heavy proxy rejects nearly every Indic and agentic batch"*. So acceptance is real and lane-dependent. But the §1 `Unique supply` column is 100% of the pool. Re-price the same table against the tokens the selector will actually accept:

| Lane | Spec ratio | Ratio at 40% acceptance | Spec verdict | Actual verdict |
|---|---|---|---|---|
| Web | 0.15× | 0.38× | covered | covered |
| **Code** | 0.44× | **1.09×** | covered | **repeat** |
| **STEM** | 0.92× | **2.29×** | covered | **repeat** |
| **Long-ctx** | 0.89× | **2.23×** | covered | **repeat** |
| Indic | 1.14× | 2.86× | repeat | repeat (harder) |
| Reasoning | 2.00× | 5.00× | repeat | repeat (at the 6-epoch ceiling) |
| Agentic | 63.5× | 158.7× | must generate | must generate |

Three lanes flip from *covered* to *repeat*. E7 asks the plan to "size every lane against the **real supply**", and E8 asks it to say **plainly** where a share needs repeating. The one selector parameter the spec declares in its own header is excluded from the only table that does supply accounting. (The counter-argument — that the candidate stream is larger than the unique pool because OPUS re-scores repeats — is available and would rescue the table, but the spec never makes it.)

**A9 — WEAK. "Effective code supply is therefore below the 1.10T headline, but 479B demand stays covered."**
This sentence follows a paragraph asserting that file-level dedup retains **2.4%** of tokens where repo-level retains 7.5%. It then declines to produce a number. Either the 1.1T is already file-level deduped (in which case the OpenCoder paragraph does not modify the supply and is decorative), or it is not (in which case the coverage claim needs an actual figure). The inventory says The Stack v2 is *"BigCode's **deduplicated** permissive-source code corpus"*, which probably rescues it — but the spec never checks. This is the one place the spec invokes a 97.6% deletion and then waves.

**A10 — WEAK. The "2.4% of 485M files" gloss attaches the percentage to the wrong denominator.**
`opencoder/brief.md` line 49: *"file 32.74B (2.4% of 485,817,123 files, **30.5M kept**)"*. 30.5M / 485.8M = **6.3%**, not 2.4%. Likewise repo-level: 7.48M / 11.0M repos = 68%, not 7.5%. The 2.4% / 7.5% pair is self-consistent only as a **token**-retention ratio on a common base. "2.4% of 485M files" is therefore a wrong gloss carried through from the brief.

**A11 — WEAK. "Hundreds of billions" of natural 8k-contiguous tokens is a pool figure, not a delivered figure.**
§6: *"At our 2T against a 4.5T web pool, the natural 8k-contiguous tail is on the order of **hundreds of billions** of tokens."* 9.4% × 4.5T = 423B ✓ in the pool. But the run consumes only **677B** of web (0.15×), and at RefinedWeb-natural proportions that delivers **9.4% × 677B ≈ 64B** of D13-contiguous text — not "hundreds of billions". To actually deliver 423B you would need the web lane to be ~62% D13, which is a mixture nothing like "Natural" and which DD's own Table 1 says buys nothing (the ≥1k row, 25% at 8192, scores MDQA-avg 22.1 vs Natural's 21.9). The comparison "far more than the 100B curated long-context inventory" fails: **64B < 100B**.

**A12 — Not an error, but the spec left a defence on the table.** Widget 8's spike model (`peakFactor = 1 + [s/(1+1.5w)]·7·[1 + 20.4/(1+2w)]`) *prices* the seam width the spec calls unmeasured. At the spec's 20B band: **1.34×** with frozen embeddings, **1.23×** unfrozen — both far under the widget's `RED_T = 3.0` instability threshold. The model says ~**6B** already clears it frozen, ~**2B** unfrozen. §8's confession *"The 20B seam width is an order-of-magnitude choice, **not a measured one**"* is unnecessary self-harm: the course gave a model and the spec did not use it.

---

## 2. Master citation ledger — one row per cited claim

Verdicts: **accurate** / **misquoted** / **wrong-scale** / **paper-silent** / **paper-contradicts**.

### 2.1 Dataset Decomposition (2405.13226) — 1B–7B, ≤1.1T, English RefinedWeb, max ctx 8192

| # | Claim in spec | Brief location | Verdict | Sev |
|---|---|---|---|---|
| D1 | MDQA-10 `0.8 → 20.8 → 21.2 → 20.4` | Fig 5a, "the threshold, precisely" | **accurate** | — |
| D2 | Mixtures lacking 4k/8k buckets score `0.0–0.4` on MDQA-20/30 | Table 1, "≤2k" / "Mid" rows | **accurate** | — |
| D3 | 8192 share `9.4% → 25%` moved MDQA-avg `21.9 → 22.1` — "noise" | Table 1 Natural vs ≥1k; brief: *"is **noise** and must not be cited as a ranking"* | **accurate** — and the spec correctly labels it noise | — |
| D3b | …framed as "raising the 8192 share" | ≥1k is `0/0/0/0/24/24/24/24`; it **zeroes D6–D9** entirely | **misquoted** — not a one-variable change | WEAK |
| D4 | "the useful share is bounded around **≤10%**" | brief: *"the one number we most want (does 2%, 4%, or 6% suffice?) is **not measured**: the smallest non-zero long share they test is 9.4%"* | **paper-silent** | WEAK |
| D5 | MDQA-30 `19.6 → 24.6 (+5.0)`, MDQA-avg `23.0 → 28.0` | Table 2 Uniform vs Grow-P2×8 | **accurate** | — |
| D6 | Long-first `−3.5` regular / `−3.4` MDQA | Table 2 Shrink-P100 vs Uniform | **accurate** | — |
| D6b | Ordering result used to license a **content-difficulty** stage curriculum | brief assumption: *"Our difficulty ladder and DD's length ladder are **different axes that will fight**"* | **paper-silent on content ordering** | MISSING |
| D7 | `+2.9` regular / `+3.4` LC avg, `244 ms vs 304 ms`, cheapest prep | Table 5 | **accurate** | — |
| D8 | Doc-masking `51.5 → 52.4`, LC `27.5 → 27.1`, MDQA-30 `20.5 → 16.0` | Table 5 Baseline-8k+DM | **accurate** | — |
| D9 | RoPE 10k→100k: `+5.4` baseline, `+4.8` DD, regular unchanged | Table 4 | **accurate** — but see D9b | — |
| D9b | The `+4.8` cell is inside a documented internal inconsistency | brief: *"Table 4 lists DD≥256 @100k with MDQA **24.9**; Table 2's Uniform row is the **same configuration** and lists **23.0**"* | **misquoted by omission** | WEAK |
| D9c | Confidence table: "RoPE 100k … Measured at **1B–7B**" | Table 4 is **1B only** | **wrong-scale** | WEAK |
| D10 | `9.4%` at 8192 / `22.9%` ≥4k | Table 1 Natural | **accurate** | — |
| D11 | "if we only see long sequences toward the end … LR is too small" | assignment-mapping §5 quote | **accurate** | — |
| D12 | Grow-P2 1→8 cycles: MDQA `25.9 → 28.0`, CSR `60.9 → 62.8` | Table 2 | **accurate** | — |
| D12b | "so the anneal reserve is delivered in **4 interleaved sub-cycles**" | Grow-**P100** 1→8 cycles **degrades** MDQA `27.0 → 24.1`. Cycling is not universally good; it interacts with ramp aggressiveness | **paper-contradicts (partially)** | WEAK |
| D12c | Cycling *inside* an 80B anneal does not address DD's mechanism (inside the anneal the LR is small **throughout**) | — | logic gap | WEAK |
| D13 | Fig 8: ~8 spikes to 7.5–8.1, ramped run spike-free | Fig 8 | **accurate** | — |
| D13b | Attributed to "**short-first length ordering**" alone | brief: *"the two arms differ in **both packing and curriculum**, so the spike suppression is **not attributable to ordering alone**"*; also n=1, clipping deliberately disabled | **misquoted** | WEAK |
| D14 | Alg 1: "If a bucket is empty, we exclude it from sampling" | verbatim | **accurate** | — |

### 2.2 Two-Phase Pretraining (2412.15285) — 8B/25B, 1T–15T, English

| # | Claim | Brief location | Verdict | Sev |
|---|---|---|---|---|
| T1 | Natural CC is `64.44%` Low | Table 16 | **accurate** | — |
| T2 | Zeroing Low lifts MMLU `42.94 → 56.10` | Table 17 | **accurate** | — |
| T2b | "**zeros Low**" | The WS arm also **upsamples** High/Medium-High — it is not a pure zeroing | **misquoted (minor)** | WEAK |
| T2c | "Largest single filtering number available" — MMLU only | The **same** CC-only ablation shows **code 19.25 → 17.41 (−1.84)**. The spec quotes the win and omits the loss from the same two tables | **cherry-picked** | WEAK |
| T3 | Epoch ceilings: 6 HQ crawl, 8 math, 12 hurts | Fig 4 (48.3/51.2/55.4/**56.1**/55.7), Table 13 (51.49/51.92/**52.28**/51.63) | **accurate** | — |
| T3b | Used to license **2.0× on reasoning traces** | ceilings measured on **web crawl** and **math** with 161.5B–6.2T unique pools, 8B/1T English | **wrong-domain, but 2× is deep inside the band** | minor |
| T4 | "+3.4 average" ordering gain | Table 4 — **relative %**; absolute is **+1.74** | **misquoted** | **FATAL (A3)** |
| T5 | GSM8K `30.86 → 40.33`, code `35.55 → 38.33`, MMLU `56.49 → 56.28` | Table 4 | **accurate** | — |
| T6 | "Two-Phase's 'best 40%' is Cluster B and is not the same object" | brief: *"Two different objects: their P2 is a second pretraining **blend**"* | **accurate** | — |
| T7 | §2 hazard 2 — 5-bucket rule is an English CC classifier, unvalidated on Indic | brief assumption line | **accurate** | — |

### 2.3 OpenCoder (2411.04905) — 1.5B/8B, code specialist

| # | Claim | Brief location | Verdict | Sev |
|---|---|---|---|---|
| O1 | `~75%` of GitHub files are exact duplicates | §2.1.1 | **accurate** | — |
| O2 | File `32.74B` vs repo `99.47B`; 52B char-identical hidden | Table 9, §6.1 | **accurate** | — |
| O2b | "`2.4%` of 485M **files**" | 30.5M/485.8M = 6.3%; 2.4% is a **token**-retention ratio | **misquoted** | WEAK (A10) |
| O3 | File-level wins HE and MBPP at every matched budget | Fig 8 | **accurate** | — |
| O3b | Applied to a 120B general code lane | brief: *"a **1.5B Python** HumanEval/MBPP result with **no error bars**"* | **wrong-scale, caveat absent** | WEAK |
| O4 | Chunk-after-file removes `0.04B` | Table 13 | **accurate** | — |
| O5 | `stars>=5`: lower loss, HE `~0.12 vs 0.18`, MBPP `~0.14 vs 0.20` at 100B | Figs 10–11 (pixel reads) | **accurate** | — |
| O5b | "…and especially not on Indic or agentic" | paper has no Indic, no agentic | **paper-silent** (reasonable inference, flagged in §8) | minor |
| O6 | Fig 9: HE stalls `~0.33` vs climbing to `~0.47`, gap never closes | Fig 9 | **accurate** | — |
| O7 | Synthetic anneal snippets kept on unit-test pass, `2.71B` | Table 3 | **accurate** | — |
| O8 | OpenCoder anneal = `84%` original distribution; shift `~16%` | §2.2 / §III-C | **accurate** (16% is the upper bound of ½·L1) | — |
| O9 | OpenCoder 100B/2.6T = 3.85% in Cluster A | survey Table II | **accurate** | — |

### 2.4 Demystifying Synthetic (2510.01631) — ≤3B, ≤200B, English CC, CE loss only

| # | Claim | Brief location | Verdict | Sev |
|---|---|---|---|---|
| S1 | Rephrase ceiling "best `~30%`, always `<50%`" | §5.1, Fig 4 left | **accurate in substance** | — |
| S1b | Called a "**measured** rephrase ceiling" | brief: *"Fine grid … **skips 30%** (points are 20% and 50%). The '~30%' headline is **interpolated**"* | **misquoted** | WEAK |
| S1c | "at every model and data scale they tested" | ≤3B params, ≤200B tokens, **English CC only**, metric = Pile/Wikitext CE. Applied here to Indic | **wrong-scale/wrong-language** — but §2 opens *"no paper studied Indic"* ✓ | WEAK |
| S2 | Textbook ceiling `≤3%` at 50B, often 0% below 10B | Fig 4 right (pixels: 200M 0.35%, 1B 2.3%, **500M 3.1%**) | **accurate** (3.1% rounded down to "≤3%"); pixel-derived precision presented as hard | WEAK |
| S3 | §2 hazard 1: App. D.2 shows uncovered unigrams spike per-token loss under a frozen English tokenizer | Fig 7c / Fig 8 — spikes are on `.\n\n` in **English CC** with a **Llama-3 128k** tokenizer. The paper studies **no** frozen-embedding condition and **no** Indic script | **paper-silent on the mechanism claimed** | WEAK |
| S4 | Agentic §3.1: "Demystifying's failing cell is **textbooks** … This is a third category **neither paper measured**" | correct, and honestly declared | **accurate** | — |
| S5 | 8B-vs-70B teacher result | brief: Llama-3-8B > 3B; **70B ≱ 8B on HQ** | **the spec never cites this**, though it budgets a "frozen stronger teacher" in §3.3 | **MISSING** — a cheap, directly-relevant defence left unused |

### 2.5 Model Collapse (2404.05090) — theory + 8×256 nanoGPT, char-level Shakespeare, vocab 65

| # | Claim | Brief location | Verdict | Sev |
|---|---|---|---|---|
| C1 | Fully-synthetic self-training collapses almost surely; synthetic must be **logarithmic** in real | §3.1, eq. (11), *"exponentially smaller"* | **accurate** | — |
| C2 | Fig 6: finite teacher window delays only — mean T `17 → 95 → 216` for K = 1/5/10 | Fig 6 | **accurate** | — |
| C3 | "20% synth / 80% real produced **ten indistinguishable generations**" | Fig 5 bottom-right | **accurate** | — |
| C3b | Scale never stated anywhere in the spec | 8-layer / 256-d nanoGPT, **one Shakespeare play**, vocab 65, 2000 iters | **wrong-scale, caveat absent** — §8 lists error-bar gaps for 4 papers and omits Collapse's toy scale entirely | MISSING |
| C4 | §5: "50% real flattens L1, **80% real erases** generation drift" | Fig 5 | **accurate** | — |
| C4b | Cited as "**Collapse Thm 2/3**" | 50%/80% are the **nanoGPT experiment** (Fig 5), not Thm 2/3. Brief: *"Do not quote 50% or 80% real as a universal 'collapse threshold'… The theorem is a **logarithmic** n(N,s,ε), not a percentage"* | **misquoted (conflation)** | WEAK |
| C5 | "rejection against a real verifier is an external signal, **which is what breaks the absorbing chain**" | Theorems assume **unbiased** self-samples. Verifier rejection makes samples *biased*, which puts them **outside** the theorem — it does **not** follow that the chain is non-absorbing | **paper-silent** — but §8 declares it *"mechanistically sound and **unmeasured**"* ✓ | WEAK, honestly owned |
| C6 | "~0.2–0.25% … matching Collapse's 50/50 arm which flattened drift" | Fig 5 bottom-left: 50/50 flattens **L1** but leaves a persistent val-loss gap (1.46 → 1.53–1.57) | **accurate as stated** (L1) | — |

### 2.6 Mid-Training Survey (2510.06826) — **a survey. Zero experiments. Every number second-hand.**

The brief's line 229 is unambiguous: *"**Do not cite this survey as evidence for any number.** … Use Table II as an index, then cite the primary."* The spec cites it **directly, by section and table, eleven times, and names a primary arXiv ID in none of them.** That is the single largest systemic citation defect in the document.

| # | Claim | Brief location | Verdict | Sev |
|---|---|---|---|---|
| M1 | Cluster A 1–5%: MiniCPM 1.96 / Hunyuan-A13B 1.48 / OpenCoder 3.85 / Pangu 4.00 / Hunyuan-Large 4.76 / OLMo-2 1.96 | Table II arithmetic | **accurate**, all six reproduce | survey-transcription |
| M2 | Cluster B 9–51%: SmolLM2 9.03 / Nemotron-4 11.11 / Qwen3 14.08 / MiMo 16.67 / Zamba 51.28 | Table II | **accurate** | survey-transcription |
| M2b | OLMo-2 quoted as "**per-100B run** = 1.96%" | brief flags Table II's "~600B" as *"**not** a 600B sequential phase"* — the spec's disaggregation is the **correct** reading | **accurate, and a genuine improvement over the survey** | ✓ credit |
| M2c | **Neither documented transcription error is repeated.** LLaMA3-405B "1 (40B)" is absent from the Cluster A list; §7.3 correctly uses **40B** for the *8B* probe (§3.1.3), not the 405B terminal anneal (40M). Granite 3.0's 60%-summing mix is not cited | — | **accurate — a clean pass** | ✓ credit |
| M3 | 10–40% overlay list: OpenCoder 84/16, Zamba 60/40, Phi-4 70/30, Hunyuan-Large long-text 75/25, SmolLM2 long 60/40, Llama-3 probe 70/30, Nemotron-4 *"majority already-seen tokens reweighted"* | §III-B / §III-C | first six **accurate**. The **Nemotron-4 quotation is unsourced**: the string `already-seen` occurs **0 times** in `midtrain-survey/brief.md` and **0 times** in `EVIDENCE_MAP.md`. The brief renders Nemotron-4's anneal behaviour differently — *"up-weights domains where the model underperforms"* (§III-B). Caveat in fairness: the brief is a summary, so the phrase **could** exist in the survey body; but it is **the one quoted string in the entire spec that is not traceable to anything in the evidence base**, and it is attributed to a named lab | **unsourced quotation** | **FATAL** |
| M3b | Two of the seven (**Hunyuan-Large long-text 75/25**, **SmolLM2 long 60/40**) are **long-context-stage** mixes, not anneal mixes. They are listed as evidence for an **anneal** ballast ratio | Table II separates Annealing and Long-context as distinct slots | **wrong-object** | WEAK |
| M4 | *"a mismatch between mid-training and pretraining corpora can lead to catastrophic forgetting"* | §III-C, verbatim | **accurate** | survey-transcription |
| M5 | Hunyuan-Large "5% of the highest-quality pre-training tokens"; 8× stricter than OPUS 40% | §III-B; 40/5 = 8 ✓ | **accurate** (and fixes EVIDENCE_MAP's "10×") | survey-transcription |
| M5b | Extended to a **per-lane** top-5% quantile | Hunyuan-Large's 5% is **global** | **paper-silent** — §8 confidence table owns *"One precedent, no ablation"* ✓ | minor |
| M6 | FIM quote, §III-A; "DeepSeek-V3 is the only surveyed run using it in mid-training" | §III-A + Fig 1 | **accurate** | survey-transcription |
| M6b | FIM offered as the mechanism for a **63× shortfall** | FIM creates more **prediction targets per token**; it creates **zero new tokens**. It cannot close a 0.63B → 40B gap. The survey supplies **no multiplier**, no measurement, no primary | **paper-silent on the quantity claimed** | WEAK |
| M7 | MAP-Neo Chinese `25% → 8.5%` | §III-B | **accurate** — and correctly presented as the honest counter-precedent ✓ | survey-transcription (primary 2405.19327) |
| M8 | Yi-Lightning "emphasis on complex reasoning and low-resource multilingual support", no percentages | §III-B | **accurate** | survey-transcription |
| M9 | §5 floor: OLMo 2 *"not strictly necessary to have a large proportion … just that domain-specific data is present"*, explicitly labelled **"via survey §III-C"** | §III-C | **accurate — and the only place the spec flags its own transcription** ✓ | ✓ credit |
| M10 | Llama 3 8B `+24.0%` GSM8K / `+6.4%` MATH, "negligible uplift for the 405B" | Table VII | **accurate** | survey-transcription |
| M11 | "Every large mid-training gain … (OLMo 2 +10.6, MiniCPM4, Gemma2-9B ~10%, SmolLM2) is ≤14B" | Table VII | **accurate** | — |
| M12 | ABF θ ≈ 10⁶ + YaRN α(s) = 0.1·ln s + 1 | §V-D | **accurate** | survey-transcription (primaries 2309.16039 / 2309.00071) |
| M13 | "The word 'agent' appears **once** in the mid-training survey, as a dataset name" | brief: *"occurs exactly once … as `Agent-FLAN`"* | **accurate** | ✓ credit |
| M14 | MiniMax-01 "linear interpolation of source-specific weights", labelled **"Published analogue"** | brief line 140: **commented out**, absent from the published paper | **paper-contradicts the word "Published"** | **FATAL (A6)** |
| M15 | OLMo 2 "50B on a 4T run (1.25%) and 100B on 5T (2%) **at 7B–32B**" | spark-joy brief follow-on: 7B = 3×50B from 4T (1.25%); 13B/32B = 3×100B **plus 1×300B** from 5T/7T (2% **and 6%**) | **misquoted** — the 32B also ran a **300B (6%)** leg, the largest OLMo-2 anneal, which argues the other way and is omitted | WEAK |
| M15b | Third-hand: OLMo 2 (2501.00656) is **not one of the nine papers**; it reaches the spec via the spark-joy brief's follow-on list | — | outside the evidence base | WEAK |

### 2.7 Spark Joy (2406.03476) — 7B, 1T, **data-only swap at cruising LR** (rsqrt, no decay)

**Framing defect (rubric-directed).** Spark Joy is the spec's primary defence for the anneal *length* (§4.2). It is **not an anneal in the low-LR sense**: brief §7 — *"they did not touch the learning rate … under a pure rsqrt, LR(1.0T)/LR(0.8T) ≈ **0.894**, so the DU leg ran at ~89–100% of the seam LR"*, and *"**this is not an anneal in the 'low LR cooldown' sense at all.** It is a mixture swap at cruising LR."* The spec's own §Scope defines its anneal as *"the mid-training **decay** leg"*. **The spec never states this mismatch anywhere.** Its §4.2 phase-length argument therefore prices a *different intervention* than the one it is buying. MISSING — and it is the most obvious question a reviewer will ask.

| # | Claim | Brief location | Verdict | Sev |
|---|---|---|---|---|
| J1 | Swept 50B/100B/200B/300B = 5/10/20/30% of 1T | Table 6 | **accurate** | — |
| J2 | MMLU peaks at 100B (**43.19**), Core Average at 200B (**39.32**) | Table 6 | **accurate** | — |
| J3 | "**no point below 50B exists**"; 80B sits between the two lowest; 40B is below every point | Fig 3 | **accurate, and honest** ✓ | — |
| J4 | Filtered web held at **30% (0.82×)** "to prevent a large distribution shift" | Table 4 + verbatim quote | **accurate** | — |
| J4b | The spec then puts its own web at 20.3% and never states **its own multiplier**: 20.3/33.85 = **0.60×**, i.e. **more aggressive than Spark Joy's 0.82×** and less aggressive than their total-web 0.42× | — | **MISSING** — the comparison it invites, unmade | MISSING |
| J5 | Language Understanding negative at every phase length | Table 6 | **accurate** | — |
| J5b | …`−0.47 / −1.11 / −1.44 / −1.17` **"on LAMBADA / HellaSwag / Winograd / WinoGrande"** | those are the four **phase lengths**; no per-task breakdown exists | **paper-contradicts (fabricated axis)** | **FATAL (A4)** |
| J6 | Sans-math: MMLU **29.71** vs 35.69 (`−5.98`), RC **26.48** vs 37.02 (`−10.54`), Core Avg **−2.83** | Table 7 | **accurate**, all three exact | — |
| J6b | Confound not mentioned | brief: *"they hold **proportions** at 30/35/35 while **shrinking the pool** … the surviving domain data is repeated harder"*; the *directional* finding survives, the magnitude does not | acceptable use, caveat absent | minor |
| J7 | Reserve "reweighted, never repeated"; DS **peaks at 0.89**, Code **1.12** | Peaks are **1.08 / 1.18** (30% arm). Also a **brief-derived** table the paper does not publish, and the 30%-arm regression is *"a correlation, **not their claim**"* | **misquoted** | **FATAL (A5)** |
| J8 | Mixture shift 41.1% | ½·L1 = 41.05 ✓ | **accurate** | — |
| J8b | Compared to the spec's 19.5% | Spark Joy's partition is **4 quality tiers**; the spec's is **8 capability lanes**. ½·L1 is not comparable across different partitions — a finer partition mechanically dilutes the statistic. Worse: the spec's **top-5% within-lane quantile reserve** is a large *intra-lane* distribution change that ½·L1 over lane shares cannot see at all | **wrong-object** | WEAK |
| J9 | "Spark Joy's silence is not evidence of safety — hard-switched 34.35pp with no LR change, no loss curve, no perplexity, no gradient norm" | brief verbatim | **accurate, and excellent** ✓ | — |
| J10 | MMLU peak = 0.60pp gap; Core Avg peak = 0.86pp; cite shapes not optima | brief | **accurate** ✓ | — |
| J11 | "Spark Joy's sans-math arm is the template for measuring a lane's contribution" | §3.4 | **accurate** | — |

### 2.8 Preference Curriculum (2501.13126) — 1.3B/3B, 100B/1T, English + Chinese, single seed

| # | Claim | Brief location | Verdict | Sev |
|---|---|---|---|---|
| P1 | Fig 6b: ArXiv **88%** / GitHub **66%** early, Wikipedia **86%** late, against §3.5's "does not skew" | Fig 6b verbatim | **accurate** — the strongest citation in the document ✓ | — |
| P2 | Spearman between PD variants is only **0.41** | Fig 11 | **accurate** | — |
| P2b | Used to argue PD is unreliable | The same paper's **Fig 4** shows all four PD variants land within **0.19** avg points (54.72 / 54.74 / 54.88 / 54.69) while the method is worth **+1.22 to +1.41**. The low Spearman **does not degrade the result**, and the spec does not address this counter | **oversold** | WEAK |
| P3 | "a small model's perplexity on Devanagari measures tokenizer fertility, not difficulty" | paper has **zero** multilingual analysis; nearest is a 50/50 zh/en corpus | **paper-silent** (stated flatly, not hedged) | WEAK |
| P4 | S-shape `f(p)=1/(1+exp(10(p−0.5)))` blends over **43.9%** of the run | derived from Eq 8 | **accurate** | — |
| P4b | Cited to defend a **20B (1%) seam band** — **44× narrower** than the evidence offered | — | **evidence does not support the number it is attached to** (E2) | WEAK |
| P4c | PDPC's `f(p)` blends between two **PD halves of one corpus**, not between two **mixtures** | — | **wrong-object** | WEAK |
| P5 | Hard switch (Z-shape) worth **~1.1** average points less | Table 3: 54.7 vs 53.6 | **accurate** | — |
| P5b | Z-shape 53.6 ≈ Random 53.5 — so the hard switch is worth **~0 vs no curriculum**; the 1.1 is S-vs-Z | omitted context | minor |
| P6 | "indistinguishable from random for the first ~35% … loss worse for the first ~40%" | Fig 3b (**3B**) and Fig 5a (**1.3B**) — **two different runs** merged into one sentence | **accurate numbers, merged settings** | minor |
| P7 | §5 row: "Preference Curriculum … offers **no starvation protection**" | brief: *"PDPC has **no floor of any kind**"* | **accurate** ✓ | — |
| P8 | **The spec never cites the +8.1 MMLU headline.** | Correct call — the Random baseline is at chance (27.7 vs 25%) | ✓ credit for restraint | — |
| P9 | **Not cited, and should have been:** PrefCurriculum proves PD is **not** a difficulty axis (logical-reasoning requirement identical **0.72/0.72**; high-PD needs *less* scientific content **0.61 vs 0.70**) | Fig 9 | relevant to R6; **unused** | MISSING |

### 2.9 CLIMB (2504.13161) — ≤1B params, 40B–400B **continuous** pretrain after a 10T phase-1, English

| # | Claim | Brief location | Verdict | Sev |
|---|---|---|---|---|
| L1 | 62M proxy ranks nearly as well as 350M (**60.11 vs 60.41** on the 1B target) | Table 3 Abl.proxy | **accurate** | — |
| L2 | 112 configs at 4:2:1 (64+32+16) beat RegMix **59.37**, DoReMi **59.16**, Random **57.93** at 1B | Tables 1, 3 | **accurate** | — |
| L2b | **The setting is not stated and does not match the use.** These are **40B continuous-pretrain** runs on top of a **10T phase-1**, at **≤1B params**, English, optimised on PIQA/ARC-E/HellaSwag. The spec proposes them to set a **from-scratch 2T, 120B, seven-lane, multilingual** mixture. The brief's explicit warning: *"Do not copy Fig 7's peaky continuous weights into a **from-scratch** V5 run"* | **wrong-scale / wrong-regime** | WEAK |
| L2c | **R7/E11 relevance:** CLIMB's proxy-transfer result is **62M/132M/350M → 1B**. The assignment asks for **1B and 3B** proxies. CLIMB measures **nothing at 3B** and nothing about transfer *from* 1B *to* 120B. The citation the validation plan leans on does not reach the scale the plan claims | **paper-silent at 3B** | WEAK |
| L2d | Cost of 112 proxy runs never priced (§7.3 prices only the anneal probes). CLIMB: ~45 GPU-h/proxy at 350M | **MISSING** | MISSING |
| L3 | "code cluster C20 → **0** under a reasoning-only objective" | Table 4 + §D | **accurate** — the best floor argument in §5 ✓ | — |
| L3b | "Otherwise the search zeroes agentic **and Indic**" | Indic was **never in CLIMB's corpus**; C20 is the only measured zeroing | **paper-silent on Indic** | minor |
| L4 | Figs 5/7: different objectives → different winners | ✓ | **accurate** | — |
| L5 | From-scratch top-3 ≈ **64%** vs continuous one cluster at **43%** | Fig 8 / Fig 7a | **accurate** | — |
| L6 | "CLIMB's own checklist answers 'No' to error bars" | Q7 = No | **accurate** ✓ | — |

---

## 3. R3 audit — "points each one at the datasets from the inventory"

Cross-checked against `widgets/widget_9_dataset_inventory.html`. Occurrence counts are `grep -ci` over `SOLUTION_v3.md`.

| Slot | Inventory datasets (token counts from widget 9) | Named in spec? |
|---|---|---|
| **Agentic** | SWE-Gym 150M, SWE-smith 120M, OpenHands 90M, ToolBench 80M, ToolACE 60M, Glaive 50M, Nexus 30M, xLAM 25M, Hermes 22M → **627M** | **✅ all nine, with token counts, split long-trajectory 360M / short-format 267M. Exemplary.** |
| **Reasoning** | OpenThoughts2 **3B**, OpenMathReasoning **2B**, NuminaMath **500M**, OpenR1-Math **1.6B**, AON (V4 corpus) **78B** → 85.1B | **❌ ZERO. All five strings occur 0 times.** |
| **Long-context** | Repo-packed code (32K+) **60B**, Book-length corpora (packed) **40B** → 100B | **❌ ZERO. Both strings occur 0 times.** |
| Indic | Sangraha verified 64B / unverified 24B / synthetic 162B, IndicCorpV2 20.9B, BPCC 3B, Samanantar 2B | ✅ all six named with counts (not an R3 slot, but credit) |
| Code | The Stack v2 900B, CommitPack 4B, D3 Code (V4) 199B | ❌ zero named |
| Web / STEM | FineWeb-Edu 1.3T, DCLM-Baseline 2.6T, peS2o 42B, proof-pile-2 55B, D1 164B, D2 627B, D4 STEM 49B | ❌ zero named |

**R3 is 1-of-3.** The assignment names exactly three slots and the spec funds one of them from the inventory.

### 3.1 — FATAL. The reasoning lane's *actual* trace supply is 7.1B, not 85B.

`AON (V4 corpus)` is **78B of the 85.1B** — the V4 run's already-trained reasoning slot, described in the widget as *"Lived reference for how many reasoning tokens the last cohort actually spent."* The genuinely new reasoning-trace supply is **7.1B**, and the **long**-CoT portion (OpenThoughts2 3B + OpenR1-Math 1.6B, the widget's *"very long traces"*) is **4.6B**.

The spec's §1 raises reasoning to 8.5% *specifically* because *"V5 must expose a controllable reasoning-effort dial, which requires a **distribution of trace lengths**"* — and then never disaggregates. Re-price it:

- §4 reserves **"Long reasoning traces (reserved) +10.0% = 8.0B"** for the anneal.
- Against long-CoT supply of **4.6B** that is **1.74×** — inside the ceiling, fine.
- Against `OpenR1-Math` alone (1.6B, the only "very long trace" set) it is **5.0×**.
- The main run's 170B against a **7.1B** real-trace pool is **24×** unless the 78B AON block carries the trace distribution — which the spec never claims and the widget does not say.

**The 2.0× repeat headline is only true if V4's own output counts as reasoning-trace supply.** That is exactly the "wishful accounting" E9 names, applied to a lane the spec treats as comfortable.

### 3.2 — FATAL. The long-context lane's stated job is contradicted by its own inventory.

§1: *"The curated lane's distinct job is **multi-document reasoning**, which web spans do not provide."*
The inventory contains **no multi-document data**. It contains *"Whole repositories packed into 32K+ token sequences"* (60B) and *"Long documents and books packed to fill the context window"* (40B). Both are **single-source packed sequences**. Neither is MDQA-shaped. The lane's entire justification is unsupported by the lane's entire supply.

Two further collisions:
- **The spec cites OpenCoder to reject repo-level code (§1), then funds 60% of its long-context lane with repo-packed code.** Fig 8 says repo-level *"at ~100B is still only HE ~0.17 / MBPP ~0.14"* against file-level's 0.19/0.20. The spec's two lanes take opposite positions on the same evidence, and it never notices.
- The inventory is **32K+**; the spec correctly states *"Long-context evidence stops at 8192. Nothing here licenses a 32k or 128k claim"* — and then sizes a 4.5% lane whose supply is entirely 32K+ sequences. It scores its own supply as unlicensed.

### 3.3 — The anneal reserve points at three things that do not exist in the inventory.

| Reserve component | Tokens | Inventory backing |
|---|---|---|
| Tier-A verified Indic | 9.6B | ✅ Sangraha verified 64B, named |
| Long agent trajectories | 4.0B | ✅ SWE-Gym / SWE-smith / OpenHands 360M, named (11.1× on that pool) |
| Long reasoning traces | 8.0B | ⚠️ real (4.6B) but **unnamed** |
| High-quality STEM | 1.6B | ⚠️ peS2o 42B / proof-pile-2 55B exist but are **unnamed** |
| **Algorithmic / competition code** | **6.4B** | **❌ nothing.** No algorithmic/competition-code dataset exists in widget 9. OpenCoder's 12.44B Algorithmic Corpus is *their* keyword sample of *their* corpus, not ours |
| **Verified synthetic + textbooks** | **2.4B** | **❌ nothing.** Must be generated. **The spec never says so** — a direct E8 miss ("says plainly where a share can only be reached by … generating it") |

### 3.4 — FATAL. Nothing is actually "held back". R5's verb is defeated by the spec's own arithmetic.

The rubric is explicit: *"R5's object is 'held back.' Name what is withheld during the main run, not only what the anneal contains."* §4 is entirely a description of anneal contents. Worse, every "reserved" lane is **already over-consumed before the anneal begins**:

| "Reserved" | Main-run consumption | Anneal adds | Total epochs |
|---|---|---|---|
| Tier-A Indic | 126.4B / 64B = **1.98 ep** | +9.6B | **2.13 ep** |
| Reasoning traces | 170B / 85B = **2.00 ep** | +8.0B | **2.09 ep** |
| Agent trajectories | 40B / 0.63B = **63×** | +4.96B | **~71×** |

To genuinely withhold 9.6B of Sangraha-verified you must cap main-run Tier-A at 54.4B (0.85 epochs) — which breaks the 40% tier share the spec just defended. **"Reserve" here means "reweighted", not "held back".** The spec even says so, quoting Spark Joy's *"a working reserve is **reweighted, never repeated**"* — a sentence that, applied to its own table, indicts it: Tier-A Indic at 2.13 epochs and agentic at ~14 epochs inside the leg are exactly "repeated".

---

## 4. E6 audit — do the benchmarks justify the MAGNITUDE?

**FATAL. The course's own funding rule is never mentioned, and two lanes fail it.**

`widgets/widget_1_mixture_composer.html`:
```js
const WEIGHTED_MIN=8;   // a lane needs at least this share to move its benchmarks
...
SLOTS.forEach((s,i)=>{ (vals[i]>=WEIGHTED_MIN?funded:starved).push(s.name); });
```

| Lane | Spec share | ≥8%? | Benchmarks the spec says it "must win" |
|---|---|---|---|
| Web | 33.9 | ✅ | MMLU, MMLU-Pro, ARC, HellaSwag, WinoGrande, PIQA |
| Code | 24.0 | ✅ | LiveCodeBench, Aider, HumanEval/+, MBPP/+, MultiPL-E |
| Indic | 15.8 | ✅ | MILU, IndicGenBench, MGSM, Flores-101 |
| STEM | 11.5 | ✅ | AIME, GPQA, MATH, GSM8K |
| Reasoning | 8.5 | ✅ (just) | AIME, GPQA, HLE, BBH |
| **Long-context** | **4.5** | **❌ STARVED** | LongBench, RULER, MDQA, TOEFL, QuALITY |
| **Agentic** | **2.0** | **❌ STARVED** | SWE-bench, τ-bench, BFCL, GAIA, BrowseComp |

By the course's own composer, the two lanes with the longest benchmark lists **cannot move a single one of them**. And the spec's headline deviation — cutting long-context **6% → 4.5%** — moves that lane *further* below the line while keeping its five-benchmark claim intact. **The 8% rule is the single most obvious reviewer attack on this document and there is no prepared answer anywhere in it.**

Per E6/E3 this makes those two benchmark cells **decorative labelling → PADDING**. The rest of the column is barely better: outside the long-context threshold argument (D1/D2) and the Indic anneal discussion, **no benchmark in the table is used to justify the magnitude of its lane's share.** The column answers "what will we measure", not "why is this number what it is".

Also note: the widget's own `BENCH` map ties **long-context → `long-eval`** and **general web → `MMLU`** only. The spec's expanded lists come from midtrain-survey Table VI — legitimate, but survey-sourced and unattributed.

---

## 5. E9 audit — "quietly hands a large share to a lane that has almost no real data"

**Blunt answer as requested: the agentic section's three load-bearing citations are each stretched past their measured setting, and none of them supports a 94%-generated lane.**

| Argument | What it actually rests on | Does it license 94% generated? |
|---|---|---|
| **1. Environment-grounded, not invented** — "tool observations are **real environment output**" | Nothing. Explicitly declared *"a third category neither paper measured"* | **No** — honest, and honestly a hole |
| **2. Verifier-filtered breaks the absorbing chain** | Collapse's Theorems 1–3 assume **unbiased** self-samples on a **linear softmax over one-hot contexts**; the only neural check is an **8×256 nanoGPT on one Shakespeare play, vocab 65**. Verifier rejection makes samples **biased**, i.e. **outside the theorem** — which is not the same as "breaks the chain" | **No.** Being outside a theorem is not being safe |
| **2b. OpenCoder keeps synth on unit-test pass** | True — **2.71B tokens = 3.62% of a 100B anneal ≈ 0.11% of the 2.6T run**, on **Python functions with generated tests**. It is the smallest synthetic fraction in the entire evidence base | **No — it argues the opposite.** The one lab that did verifier-filtered synth at pretrain scale kept it at 3.6% of one leg. The spec cites it to defend 94% of a lane |
| **3. Frozen stronger teacher** | Collapse Fig 6 (K = 1/5/10, T = 17/95/216) shows finite windows **only delay**. "A frozen external teacher is not in that family" is correct and **unmeasured**. Demystifying's actual teacher finding — **70B ≱ 8B** — is never cited | **No** |
| **4. Real tokens in every batch** | Collapse's 20/80 arm — ten indistinguishable generations at **8×256 on Shakespeare**. The spec's ratio is **6/94**, the **inverse** of the arm it cites | **No. This citation points the wrong way.** The 50/50 arm still drifted in val loss; 80/20 was the arm that held. 6/94 is off the far end |
| **5. FIM as a token multiplier** | Survey §III-A, **no measurement, no primary, no multiplier**. FIM adds prediction targets per token; it adds **zero tokens** | **No — category error.** It cannot turn 0.627B into 40B |
| **6. Masking** | ✅ Matches widget 5 exactly (*"masked: user turns and tool observations"*) | Design correctness, not supply |

**Is loud disclosure sufficient?** Partly. The spec does everything E9's word "quietly" excludes: it prints 63.5×, prints "~94% of the lane is generated", declares Low confidence, states a kill criterion, and — genuinely unusual — publishes the **literature-compliant alternative (0.2–0.25%)** and says it is choosing not to take it. That is the honest-accounting behaviour the session is about.

But E9's sentence is *"hands a large share to a lane that has almost no real data behind it will **lose marks**"* — the penalty attaches to the **allocation**, and only the adverb "quietly" attaches to the disclosure. The spec is 10× above its own stated literature-compliant ceiling. Meanwhile the assignment-mandated composer floor is **2%**, so the spec has taken the floor as its target and defended it as a capability commitment. That is defensible — but the strongest available move (drop to 0.5–1%, take the composer floor as a floor rather than a ceiling, and route the rest to SFT/RL) is only present as a *failure* branch, not as the plan. **Verdict: E9 partially defended. The disclosure is excellent; the number is still the named failure mode.**

---

## 6. R6 / E10 — difficulty and reasoning-length bands. **Both absent. Stated twice, so weighted twice.**

**Difficulty bands.** The only appearance is a §6 table column reading `B0–B1`, `B1–B2`, `B2–B3`, `B3–B4`, `B4–B5`. `grep -c B0` = **1**. There is **no definition of any band and no example of any band**. The rubric is explicit: *"A spec that shows `B0–B1` in a table column with no example **FAILS** this."*

The source data exists and was not used — `widgets/widget_7_curriculum_stages.html`:
```js
{t:"B0", h:"Nursery",        e:"simple children's sentences"}
{t:"B1", h:"Grade-school",   e:"basic grade-school text"}
{t:"B2", h:"High-school",    e:"high-school level material"}
{t:"B3", h:"Undergraduate",  e:"undergraduate coursework"}
{t:"B4", h:"Graduate",       e:"graduate-level texts"}
{t:"B5", h:"Research / PhD", e:"research and PhD-grade papers"}
```

**Reasoning-length bands.** `grep -ci ultra` = **0**. The four course levels — **LOW** (near-direct, 2 steps) / **MEDIUM** (a few steps, 4) / **HIGH** (derive + check, 6) / **ULTRA** (deliberate + verify, 14) — are never named, never defined, and carry no step counts, no token counts and no worked example. `widget_6_reasoning_effort.html` supplies all four on one shared problem (count n ≤ 1000 divisible by 3 or 5 → **467**) with per-level token counts computed in code, and lecture §7 names them in prose. The spec's entire treatment is one sentence: *"Short and medium traces in the Reasoning stage; long traces reserved for the anneal."* Three unlabelled sizes where the course defines four named levels.

This is the spec's largest single point loss and it is **not a citation problem** — the material was sitting in the course's own widgets.

**Paper support for a difficulty ladder — there is none, and one paper contradicts it.** Per the parent's instruction: PrefCurriculum's Fig 9 shows high-PD text requires **less** scientific/technical content (0.61 vs 0.70) and **less** cultural background (0.59 vs 0.69), with logical-reasoning requirement **identical at 0.72/0.72**. Its Fig 6b puts 88% of arXiv and 66% of GitHub in the *easy* half. **PD is not a difficulty axis.** The spec is *clean* here — it never claims paper support for B0–B5 — but any future version that does would be misattributing. The correct citation for band **ordering** is Dataset Decomposition, and that is a **length** ladder, not a content ladder (see D6b).

---

## 7. R8 — cleaning aimed at the starved slots. **Absent.**

`grep -ci clean` over `SOLUTION_v3.md` = **0**. The assignment's closing sentence — *"Alongside the plan the cleaning continues toward the cumulative target, now aimed at the slots the mixture shows to be starved"* — has no counterpart in the spec. The analysis needed to satisfy it **already exists inside the document** (agentic 63.5×, Indic tier C 5.06×, reasoning 2.0×, STEM 0.92×) and is never converted into a cleaning directive. The composer even computes a `starved` list for free. One paragraph would close this.

---

## 8. Deviation ledger — the spec declares two deviations; there are twelve

Rubric rule 9: *"Every deviation from the course preset needs the strongest defence. Mark taste-only deviations WEAK at minimum."*

**Main preset** `24/2/6/6/16/12/34` → spec `24.0/2.0/8.5/4.5/15.8/11.5/33.9`:

| Lane | Course | Spec | Declared? | Defence |
|---|---|---|---|---|
| Reasoning | 6 | 8.5 | ✅ | Trace-length distribution + 2.0× inside epoch ceiling. **Weakened by §3.1** — the real trace pool is 7.1B |
| Long-ctx | 6 | 4.5 | ✅ | DD threshold + 9.4%→25% noise. **Weakened**: 2–9% region unmeasured, and 4.5% is below the course's 8% funding rule |
| STEM | 12 | **11.5** | ❌ | none — and STEM is the tightest lane at 0.92× ("almost no headroom" by the spec's own confidence table) |
| Indic | 16 | **15.8** | ❌ | none |
| Web | 34 | **33.9** | ❌ | none |

**Anneal preset** `20/8/18/8/28/10/8` (code/agentic/reason/long/indic/stem/web) → spec `22.4/6.2/15.1/2.7/21.5/8.9/20.3`:

| Lane | Course | Spec | Declared? | Defence |
|---|---|---|---|---|
| Web | 8 | 20.3 | ✅ | Spark Joy filtered-web-at-30%. **Strong** — the best-defended deviation in the document |
| **Long-ctx** | **8** | **2.7** | ❌ | **none — a 3× cut, and it violates §7.5's own "≥4% regardless" (A7)** |
| Agentic | 8 | 6.2 | ❌ | none (falls out of the 60/40 construction) |
| Reasoning | 18 | 15.1 | ❌ | none |
| Indic | 28 | 21.5 | ❌ | direction is defended (§2 honest-precedent), the **magnitude** is not |
| STEM | 10 | 8.9 | ❌ | none |
| Code | 20 | 22.4 | ❌ | none |

**Stage anchors** — `widget_7` ships five course stage profiles (`seed 55/15/3/2/15/10` … `anneal 8/22/20/10/30/10`). The spec's §6 table deviates from every one of them and never references the widget. Largest: long-ctx stage `lctx 18 → 11`, anneal `gen 8 → 20`, anneal `lctx 10 → 3`.

**Net:** the sentence *"The two changes from the course preset, and why"* is **inaccurate**. Ten further deviations ship undeclared, and one of them (anneal long-context) breaks a declared kill criterion.

---

## 9. R4 audit — the floor. **FATAL: the membership set is wrong and the floor is satisfiable with zero agentic tokens.**

§5: *"**8% of every iteration's accepted tokens is reserved for Indic + agentic + reasoning**"*, evidenced by *"Widget 3 proxy direction [0.70, 0.53, 0.33]"*.

The proxy vector is cited **correctly** — `widget_3_opus_selection.html`, `PROXY.english.vec = [0.70,0.53,0.33]` ✓. But two lines below it, the same file says:

```js
agentic: {vec:[0.34,0.50,0.30], scarce:true},
indic:   {vec:[0.18,0.26,0.92], scarce:true},
reasoning:{vec:[0.50,0.82,0.10], scarce:false},
const LANE_FLOOR=0.08;   // 8% of trained tokens reserved for Indic + agentic
```

**The course floor is Indic + agentic. Reasoning is explicitly `scarce:false`.** And the widget's own scoring function proves why — score = dot(domain, proxy):

| Lane | Score under the English proxy |
|---|---|
| code | **0.841** |
| **reasoning** | **0.818** ← third-highest, **above web** |
| web | 0.776 |
| agentic | 0.602 |
| indic | 0.567 |

At `keepFrac = 0.40` and noise ±0.07, **reasoning is never rejected.** The spec has added a lane that the selector *favours* into a floor built for the two lanes it *rejects*, and has not partitioned the 8%. Consequence: **a selector can satisfy "8% Indic + agentic + reasoning" with 8% reasoning and 0% of both scarce lanes** — the exact starvation the floor exists to prevent. The rubric: *"if aggregate across Indic+agentic+reasoning, state whether agentic's share sits inside or outside it. **Ambiguity here is FATAL.**"* This is worse than ambiguity; it is a floor that provably fails its scarcest member.

Secondary: the §5 evidence cell reads *"V4 shipped an **8% Indic** always-on lane"*. The course constant is *"always-on 8% for **scarce lanes**"* and the widget comment is *"Indic **+ agentic**"*. Minor narrowing, same direction of error.

Also unmentioned: the composer's **per-lane** floors (`indic: floor 12`, `agentic: floor 2`). The spec honours them numerically (15.8 ≥ 12, 2.0 ≥ 2) but never states Indic ≥ 12% as a binding constraint anywhere.

---

## 10. PADDING — E3 says padding earns nothing. Cut these.

| Item | Why it earns nothing | Cut |
|---|---|---|
| §1 benchmark column for **long-context** and **agentic** | Both lanes are below the course's own ≥8% funding rule; the lists cannot be won at these shares (§4 above) | Either raise the shares or state the funding conflict. As printed, decorative |
| §6 "Packing and positional encoding" — the **244 ms / 304 ms / 20% faster** half | Priced by the spec's own confidence table at **~5% of FLOPs at 120B**. It defends no mixture number | Keep `+2.9/+3.4` and the doc-masking counter-example; drop the timing |
| §6 ABF θ ≈ 10⁶ + YaRN α(s) | Explicitly for *"a later 32k–128k extension"* — out of the declared scope (main run + anneal) and out of the declared evidence ceiling (8192) | Cut or move to a "not in this budget" line |
| §Header 2503.19206 overtraining | One clause, no number, defends nothing. A survey follow-on pointer, not one of the nine | Cut |
| §3 point 5 (FIM) | Survey-transcribed, no primary, no measurement, and mechanically cannot close a token gap (M6b) | Cut, or restate as "more targets per token, zero new tokens — does not close the gap" |
| §4 Cluster B enumeration (five runs) | The spec's argument is *"our 4% is Cluster A"*. Cluster B's five members are needed only to establish that a second object exists; one example does that | Compress to one line |
| §8 bullet on 32k/128k | Restates the §6 ABF clause it should not have made | Cut with it |
| Confidence summary (21 rows) | Genuinely valuable for E1 — **not** padding. Retained | keep |

Counter-note for balance: §8 ("What this plan does not have evidence for") is the **highest-value section in the document** under E1/E2 and must not be shortened. It pre-empts six reviewer attacks, including the two hardest (405B null result, no Indic paper).

---

## 11. Findings by severity

### FATAL (14)
1. **A1** §1 table sums to **100.2%** while claiming 100.0% — breaks R1 on the headline table.
2. **A2** §6 anneal row sums to **97** while claiming "each row sums to 100%".
3. **A3** `+3.4 average` is a **relative %**; the absolute ordering gain is **+1.74**, printed beside absolute deltas (Two-Phase Table 4).
4. **A4** Spark Joy Language Understanding: `−0.47/−1.11/−1.44/−1.17` are **phase lengths**, not LAMBADA/HellaSwag/Winograd/WinoGrande. Fabricated axis.
5. **A5** "Domain-Specific **peaks at 0.89** epochs, Code at 1.12" — peaks are **1.08 / 1.18**; contradicts the next clause; and it is a brief-derived table sold as "Spark Joy's finding".
6. **A6** MiniMax-01 linear interpolation labelled **"Published analogue"** — it is **commented-out LaTeX absent from the published survey**.
7. **A7** §7.5 declares "Long-context stays **≥4% regardless**"; the spec's own anneal runs it at **2.7%**.
8. **A8** The §1 supply table ignores OPUS's declared **40% acceptance**; three lanes flip *covered → repeat*.
9. **§9** The protected floor's membership set contradicts widget 3 (`scarce: indic + agentic`; reasoning is `scarce:false` and **scores third-highest** under the English proxy). The aggregate 8% is satisfiable with **zero agentic tokens**.
10. **§3.1** Reasoning supply is **7.1B of real traces**, not 85B — 78B is the V4 run's own output. The 2.0× headline depends on counting V4 output as trace supply.
11. **§3.2** The long-context lane's stated job (multi-document reasoning) is contradicted by its entire inventory (repo-packed code 60B + packed books 40B), and 60% of it is the repo-level packing the spec cites OpenCoder to reject.
12. **§3.4** R5's verb defeated: every "reserved" lane is already at ≥1.98 epochs before the anneal. Nothing is held back.
13. **§6 / §7** R6+E10 (both band systems, stated twice) and R8 (cleaning at starved slots) are **entirely absent**.
14. **M3** Nemotron-4 *"majority already-seen tokens reweighted"* is an **unsourced quotation** — `already-seen` occurs 0 times in the paper brief and 0 times in the evidence map, and the brief renders that lab's behaviour differently. The only quoted string in the spec not traceable to the evidence base.

### WEAK (21)
D3b ≥1k is not a one-variable change · D4 ≤10% bound is unmeasured · D6b length-ladder ≠ content-ladder · D9b Table 2/Table 4 conflict on the +4.8 cell · D9c RoPE is 1B-only, claimed 1B–7B · D12b Grow-P100 8 cycles *degrades* · D12c cycling inside a low-LR leg misses DD's mechanism · D13b spike suppression not attributable to ordering alone · T2b "zeros Low" also upsamples · T2c code regresses 19.25→17.41 in the same tables · O2b 2.4%-of-files is the wrong denominator · O3b 1.5B Python result on a 120B lane · S1b "~30%" is interpolated, the grid skips it · S1c English CC → Indic · S2 pixel reads sold as hard numbers · C4b Fig 5 percentages cited as Thm 2/3 · M3b two long-context-stage mixes used as anneal evidence · M6b FIM cannot close a token gap · M15 OLMo-2's 300B/6% leg omitted · P2b 0.41 Spearman does not degrade PDPC's result · P4b 43.9% blend cited to defend a 1% band · J8b ½·L1 not comparable across partitions · L2b/L2c CLIMB is 40B-continuous ≤1B and measures nothing at 3B · **A9** code supply not recomputed · **A10** · **A11** 64B delivered, not "hundreds of billions" · §8 ten undeclared deviations.

### MISSING (11)
1. **Spark Joy is a data-only swap at ~90–100% of cruising LR.** The spec's anneal is a *decay* leg. Never stated — the most obvious attack on §4.2.
2. **The ≥8% funding rule** (widget 1) — never mentioned; two lanes fail it.
3. **The spec's own web multiplier (0.60×)** never computed, though it cites Spark Joy's 0.82×.
4. **Collapse's scale** (8×256 nanoGPT, one Shakespeare play) never stated; §8's error-bar list omits it.
5. **Demystifying's teacher result (70B ≱ 8B)** — directly relevant to §3.3's "frozen stronger teacher", uncited.
6. **Widget 8's spike model** prices the seam width the spec calls "not measured" (20B → 1.34×; ~6B already clears RED_T). Available defence unused.
7. **Cost of 112 CLIMB proxy runs** never priced.
8. **Whether Sangraha-synthetic is rephrase-class or textbook-class** — the widget's own text (*"synthetic **and translated** expansion"*) supports the spec's claim, and the spec never cites it.
9. **No confirm/refute threshold** on any named metric (E11 ceiling).
10. **PrefCurriculum Fig 9** (PD is not a difficulty axis) uncited, though it bears on B0–B5.
11. **Sans-math confound** (proportions held while the pool shrinks) unacknowledged.

### PADDING (7)
Long-context and agentic benchmark cells · DD timing numbers · ABF/YaRN 32k–128k clause (×2) · 2503.19206 · FIM bullet · Cluster B enumeration.

---

## 12. Requirement scorecard

| ID | Requirement | Status | Missing element |
|---|---|---|---|
| **R0** | Written spec, specific enough to defend | **PASS** | Unusually specific. Two arithmetic breaks (A1, A2) on the headline tables |
| **R1** | Share for every capability slot, sum 100 | **PARTIAL** | Printed table sums **100.2**; anneal row sums **97** |
| **R2** | Indic split A/B/C/D | **PASS** | Best-executed requirement: 40/30/8/22 derived from supply, composer default shown non-fundable at 12.6×, real/synth 78/22 checked against a ceiling |
| **R3** | Agentic + reasoning + long-context → inventory datasets | **PARTIAL (1/3)** | Agentic exemplary. **Reasoning and long-context name zero inventory datasets.** Reasoning's real trace pool is 7.1B; long-context's inventory contradicts its stated job |
| **R4** | Fixes the floor the selector cannot cross | **PARTIAL→FAIL** | Membership set contradicts widget 3; aggregate 8% satisfiable with **zero agentic**; no per-lane split |
| **R5** | Declares the anneal reserve held back | **PARTIAL** | Reserve **contents** declared in full; **withholding** never specified, and the arithmetic shows every reserved lane already at ≥1.98 epochs. Two components have no inventory backing |
| **R6** | Difficulty **and** reasoning-length bands, concrete example each | **FAIL** | `B0–B1` as a table column with **no definition and no example**; **no** LOW/MEDIUM/HIGH/ULTRA at all. Both source widgets unused |
| **R7** | 1B and 3B proxy commitment | **PASS** | §7.4 explicit. Weakened: CLIMB's transfer evidence tops out at 62M→1B and measures nothing at 3B |
| **R8** | Cleaning aimed at the starved slots | **FAIL** | `clean` occurs **0** times |
| **E1** | Survives push on every number | **PARTIAL** | Very strong on the anneal, Indic tiers and agentic. Six FATAL numbers and the 8% funding rule are undefended |
| **E2** | Reasoning + **evidence behind the choices** | **PARTIAL** | 60-plus citations, ~46 accurate. Systemic defect: **eleven survey-transcribed claims with no primary arXiv ID**, against the brief's explicit instruction |
| **E3** | Tight; padding earns nothing | **PARTIAL** | ~7 padding items (§10). §8 must be kept |
| **E4** | Defended share for every lane | **PARTIAL** | Web, code, Indic, agentic, long-context defended. **STEM 11.5% has no defence beyond a ratio**; reasoning's defence rests on a supply figure that is 92% V4 output |
| **E5** | Indic tiers stated | **PASS** | — |
| **E6** | Benchmarks explain **why each number is what it is** | **FAIL** | Only long-context has a benchmark→magnitude argument. Two lanes sit below the course's own funding threshold with full benchmark lists attached |
| **E7** | Sized against **real supply from the inventory** | **PARTIAL** | Supply vector used correctly, but at 100% acceptance (A8), against 85B reasoning that is 78B V4 output, and against a STEM figure only 146B of which is itemisable in widget 9 |
| **E8** | Says **plainly** where repeating or generating is needed | **PASS (strong)** | The document's best quality: 63.5×, "~94% generated", tier-C 5.06×, and a published literature-compliant alternative it declines. Two gaps: 6.4B algorithmic code and 2.4B verified-synthetic are never sourced or declared generated |
| **E9** | No large share to a lane with almost no real data | **PARTIAL** | Nothing quiet about it — but 2% is **10×** its own stated literature-compliant ceiling, and every supporting citation is stretched (§5) |
| **E10** | Bands with a real example at each level | **FAIL** | Same as R6. Double-weighted |
| **E11** | Tier ceiling | **"excellent", not "highest"** | §7 opens *"every number above is a hypothesis"* ✓ testable-hypothesis framing. Concrete 1B/3B proxy ✓. Named metrics for **2 of 7** lanes (agentic → SWE-bench Verified/τ-bench/BFCL vs a format-only baseline; Indic tier C → IndicGenBench). **No threshold on either.** No executed run |

**E11 tier reached: EXCELLENT.** Blocked from *highest* by the absence of any confirm/refute **threshold** and by five lanes having no named metric. Blocked from *very highest* by no executed proxy.

---

## 13. Estimated score

**≈ 310 / 500.**

Reasoning: R2/E5 and E8 are excellent and rare — the supply-first Indic derivation and the loud agentic accounting are exactly what the session is testing, and the §8 evidence-gap section pre-empts most of the review. R7 passes and the E11 "excellent" tier is genuinely reached. Against that: **two requirements are wholly absent** and one of them (R6/E10) is stated twice and therefore weighted twice; **R3 delivers one slot of three**; **R4's floor is provably ineffective for its scarcest member**; **E6 fails outright** because the benchmark column never justifies a magnitude and the course's own funding rule contradicts two lanes; and six citation-level FATALs sit in the parts of the document a reviewer reads first.

**Highest-value repairs, in order:**
1. Add the two band systems from `widget_7` and `widget_6`, with the examples (recovers R6 **and** E10 — the single largest gain available).
2. Fix `+3.4` → **+1.74 absolute**; fix the Language Understanding axis; fix the 0.89/1.12 "peaks"; delete "Published" from the MiniMax-01 line; make the §1 table sum to 100 and the §6 anneal row sum to 100.
3. Name the reasoning and long-context inventory datasets with token counts — and **state that reasoning's real trace pool is 7.1B, not 85B**. Own it rather than let a reviewer find it.
4. Split the 8% floor per lane (e.g. Indic 5% / agentic 2% / reasoning 1%) and cite widget 3's `scarce` set correctly.
5. Add one paragraph on cleaning aimed at agentic, Indic tier C and STEM (recovers R8).
6. Confront the `WEIGHTED_MIN = 8` funding rule head-on for long-context and agentic — a reviewer will open the composer.
7. Add a threshold to each kill criterion (e.g. "≥ +3 pts SWE-bench Verified over the format-only baseline at 3B") to reach the **highest** E11 tier.
8. State that Spark Joy is a cruising-LR data swap, and use widget 8's model to price the 20B seam instead of conceding it is unmeasured.
