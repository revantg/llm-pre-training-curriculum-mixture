# Data, Data Everywhere: A Guide for Pretraining Dataset Construction

**Slug:** `emnlp596`

## Identification (from the PDF itself, before any assessment)

| Field | Value |
|---|---|
| **Title** | Data, Data Everywhere: A Guide for Pretraining Dataset Construction |
| **Authors** | Jupinder Parmar\* (corresponding, jupinderp@nvidia.com), Shrimai Prabhumoye, Joseph Jennings, Bo Liu, Aastha Jhunjhunwala, Zhilin Wang, Mostofa Patwary, Mohammad Shoeybi, Bryan Catanzaro |
| **Affiliation** | **NVIDIA** (single affiliation, all nine authors) |
| **Venue** | Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (**EMNLP 2024, main track**), pages **10671–10695**, Miami, Florida, USA, November 12–16 2024. © ACL |
| **arXiv preprint** | **Yes — arXiv:2407.06380** (latest version 19 Oct 2024). Found and confirmed. I did **not** need the HTML: all 14 embedded figures extracted cleanly from the ACL PDF at native resolution (800×500 to 1400×700 px), which is better than ar5iv rendering. Numbers below are cited against the **ACL Anthology PDF** (the version of record). |
| **Same-lab sibling** | Shares four authors (Prabhumoye, Patwary, Shoeybi, Catanzaro) with `two-phase` (2412.15285), which is already load-bearing in our spec. The `two-phase` brief's own follow-on list names this paper ("*Parmar et al. 2024a … likely has licensing/provenance this paper omits*") — it was flagged and never read. Overlap analysed in §9 below. |

### Vision-tooling note (required disclosure)

`inspect_image` is **not mounted in this session**. Exact error, after one retry:

```
No such tool device: xd://inspect_image. Mounted: ast_edit, debug, browser, web_search, workflow, mcp__browsermcp_*, mcp__chrome_devtools_*, mcp__cloudflare_*, mcp__langfuse_*, mcp__pencil_*
```

Substitute used, which is genuine pixel-level vision and **not** OCR: `read` on the extracted PNG path decodes the image inline to the model. **All 14 embedded images (Figures 1–14) were inspected this way**, plus four rendered table pages at 200 dpi to settle text-extraction ambiguities. In addition, Figures 6, 7, 8 and 9 were **numerically digitised** by colour-tracing the plotted lines against detected axis ticks, and three of them **independently reproduced from the published algorithm** (see §7) — a stronger check than reading a plot by eye.

---

## 1. THE FOUR SILENT GAPS — answered first, with numbers

### Gap 1 — Indic / low-resource multilingual: **DELIVERS. This is the headline.**

This is the **first paper in our evidence base with named Indic languages and token counts.** All nine current briefs are silent; `two-phase` (same lab) says only "9 languages derived from Wikipedia and Common Crawl" and never lists them.

**Table 12** (multilingual web crawl, 52 languages, all from the CC-2022-40 snapshot except JA/ZH from mC4; p. 10683). Nine Indic languages are present:

| ISO | Language | Tokens (B) | ISO | Language | Tokens (B) |
|---|---|---|---|---|---|
| HI | Hindi | **2.60** | UR | Urdu | **0.37** |
| BN | Bengali | **0.90** | MR | Marathi | **0.33** |
| TA | Tamil | **0.82** | NE | Nepali | **0.31** |
| ML | Malayalam | **0.25** | TE | Telugu | **0.24** |
| KN | Kannada | **0.18** | | | |

- **Indic total = exactly 6.00B** (Indo-Aryan HI+BN+UR+MR+NE = 4.51B; Dravidian TA+ML+TE+KN = 1.49B).
- Table 12 sums to **541.41B** over 52 languages (Table 1 rounds this to 540B — consistent). So Indic is **1.108% of their multilingual web pool**.
- Head of the distribution for contrast: RU 94.52, JA 70.52, DE 48.98, ES 46.50, FR 44.30, ZH 43.41, IT 26.40.
- **Whole-corpus arithmetic:** English 1219.0B (Table 11, verified to sum to Table 1's six English rows exactly) + multilingual web 541.41B + parallel 56B + code 211.88B (Table 14, verified against Table 1's 212B) = **2028.4B**, matching the abstract's "over 2T tokens". **All Indic = 6.00 + 0.655 = 6.655B = 0.328% of the whole pool.**

**Native vs translated — they hold both, and never compare them.** Two separate multilingual sources:
- **Native web crawl**: 52 languages, 541.41B (Table 12).
- **Translated / parallel**: an *English-centric sentence-level parallel corpus of 32 languages*, **56B**, from CC-Matrix, CC-Aligned and ParaCrawl (§A.2, Table 13). **Hindi is the ONLY Indic language in it, at 1.17% = 0.655B. Bengali, Tamil, Telugu, Marathi, Malayalam, Kannada, Nepali and Urdu are all absent from the parallel corpus.**
- Format note that matters for tier C: parallel data is **not** served as raw sentence pairs. "*Multiple examples are formatted into a document using few-shot templates with the number of in-context examples from 0-10 following an exponentially decaying probability of selection*" (§A.2). Translated supply is wrapped in a synthetic prompt template before training.
- **There is no native-vs-translated value ablation.** In Figure 8 the whole parallel corpus is a *single data source* labelled `NMT`, competing against 52 individual languages, ranked 3rd by size (my digitisation reads its bar at **55.95B**, i.e. the 56B of Table 1). It receives whatever weight the sampling method gives one source. **The one thing we most wanted — is a translated token worth less than a native token — is not measured.**

**Upsampling above natural frequency: measured, and quantified exactly.** Three methods compared at **8B params / 300B tokens** on the multilingual set (**Table 7**, p. 10676):

| Method | XCOPA | TyDiQA-GoldP |
|---|---|---|
| Alpha sampling (α = 1.3) | 58.11 | 17.86 |
| **UniMax (1 epoch)** | **58.24** | **18.11** |
| DoReMi | 57.65 | 15.8 |

I reconstructed the winning arm from pixels and it is exactly `UniMax(N=1, budget=300B)` over 53 sources (§7): **plateau 5.55% = 16.65B**; every source below the cap is served at **exactly 1.00 epoch**; the 8 largest are cut to sub-epoch (RU **0.176 epochs**). Relative to natural token proportions the reweighting is **0.35×–0.76× down for the top 7** and a **uniform 1.99× up for everything from Italian (26.4B) downward** — because 597.41B pool ÷ 300B budget = 1.99. Hindi moves from a natural 0.435% to a served **0.867%** (= 2.60B = 1 epoch). All nine Indic languages together take **2.00% of the multilingual budget = 6.00B**.

> **So the answer to "did upsampling low-resource languages help?" is: yes, but the mechanism is truncating the head, not multiplying the tail.** The winning arm never gave any low-resource language more than one epoch. There is no arm in this paper in which a low-resource language is repeated.

**Tokenizer behaviour on non-Latin scripts: NOTHING measured.** SentencePiece, **vocabulary 256k** for both the 2B and 8B models (Appendix C), covering 52 natural + 41 programming languages. No fertility measurement, no per-script token-per-character analysis, no Devanagari or Dravidian discussion, no frozen-embedding condition. The 256k vocab is usable only as a *design precedent* at this scale, not as evidence.

**Measured degradation from repetition or synthetic substitution:**
- **Repetition: yes, on English, and it is the most valuable number in the paper for us.** See Gap-adjacent finding in §3.
- **Synthetic: nothing, and the authors explicitly disclaim transfer.** Limitations, verbatim: "*although the use of synthetic data has recently garnered lots of attention, we did not include any such source of data within our studies and aspects relating to quality selection and sampling of synthetic data may be different than what our findings suggest.*" **This forbids using the epoch finding against our tier D or the agentic generated mass.**

**Stage / ordering interaction with multilingual weight: NOTHING.** Every ablation in this paper is a **single static sampling distribution held for the whole run.** There is no curriculum, no phase switch, no mixture change over time. It cannot speak to our Indic-up anneal.

**Aggregate Indic share, and a cross-paper convergence worth its own line.** Under the winning UniMax(1e) arm the nine Indic languages take **6.00B of the 300B multilingual budget = 2.000%**, which is **exactly 1.00 epoch** of the 6.00B pool — the cap binds for all nine, since every one is far below the 16.65B threshold. `UniMaxPaper` (2304.09151, ICLR 2023) reports the matching figure for umT5: **Indic 4.14% of 1.163T = 48.2B = exactly 1.00 epoch of a 48.4B pool** (their Table 8, 1× column, summed over 14 languages).

> **Two disclosed multilingual builds that publish per-language Indic volumes both serve Indic at exactly 1.00 epoch, in both cases because the epoch cap binds rather than because the share was chosen** — different labs, budgets 1.163T vs 300B, pools 8× apart. Neither chose its Indic share; supply chose it.

In the same metric — **epochs on the real Indic pool** — our spec reads:

| Build | Epochs on real Indic |
|---|---|
| umT5 1× | 1.00 |
| Parmar UniMax(1e) | 1.00 |
| **our §5 real-token floor (5.5%)** | **0.96** (110.0B against 114B of tiers A+B+C) |
| **our §1 headline share (15.80%)** | **2.77** (316B against 113.9B real; 1.14 only if Sangraha's 162B synthetic counts as supply) |

Two consequences, and the first is a **defence of §5 that was not previously in the evidence base**. Our 5.5% floor was derived purely internally as the largest Indic floor that stays inside one epoch of the real pool; it now **coincides with published practice at two independent labs**, so "one epoch of real Indic" stops being our arithmetic and becomes the observed convention. Second, it is pressure on §1: **15.80% is 2.8× what both published builds do**, and reaches a defensible 1.14 epochs only if tier D's synthetic mass counts as supply — the substitution E9 names as wishful accounting, and the same gap the v3 red-team logged as W9.

*Caveat that must travel with the 2.00%: this paper has **no combined whole-corpus run**. English, multilingual and code are ablated separately at 300B / 300B / 150B, so 2.00% is a share of the multilingual budget, not of a full seven-lane mixture. The only whole-corpus Indic figure available is the natural **0.328%**.*

### Gap 2 — Agentic / tool-use trajectory data at pretraining scale: **NOTHING.**

Zero. No tool use, no trajectories, no function calling, no agent benchmarks. The closest category is "Conversational" — 59.1B of Pushshift Reddit plus small dialogue corpora (§A.1) — which is dialogue, not agency. The one adjacent datum is a supply observation: **conversational text is 0.46% of web crawl documents** (Figure 2, printed on the bar), the smallest of eleven speech types, which the authors use to argue alignment is needed post-hoc. Nothing bears on our agentic 2.00% / 73.4× / 91.4%-generated problem.

### Gap 3 — Multi-document long-context: **NOTHING.**

**Context length is 4096 for both the 2B and the 8B model** (Appendix C). No long-context benchmark, no packing study, no sequence-length ablation, no MDQA-class eval. One structural precedent only, unevaluated: for code they "*pre-process the data further to concatenate all files of a particular language from a repository into a single long document to allow the model to attend across files*" (§A.3), and §3.1 says they "*formed repository-level contexts*". That is the same repo-packing choice our §1.3 makes, at production scale, but with **no ablation and no long-context metric** — precedent, not evidence.

### Gap 4 — Measured anneal / decay-leg lengths: **NOTHING.**

No anneal, no cooldown, no second phase, no mixture swap. LR schedules (Appendix C) are plain cosine with 1%-of-tokens warmup, decaying only **10×**: 2B **2.0e-4 → 2.0e-5**, 8B **3.0e-4 → 3.0e-5**. AdamW, β₁ 0.9, β₂ 0.95, weight decay 0.1; batch 256 (2B) / 1024 (8B). Nothing to compare against our 80B / 3.85% leg.

---

## 2. What the paper is

**Claimed problem.** Model developers do not disclose how raw sources become a pretraining set; prior open work (RefinedWeb, Dolma, FineWeb, Longpre et al.) covers only **data curation** and "*analyze only a small number of mostly English sources*". This is billed as "*the first systematic study across the entire pipeline*".

**Pipeline (Figure 1), four stages, one ablated at a time:** sources → **curation** (dedup + quality filter) → **selection** (DSIR) → **sampling** (weights per source) → final set. Plus a fifth contribution: classify **all ~90+ CC snapshots to August 2023** for toxicity / quality / domain / type-of-speech, then feed those attributes back into selection and sampling.

**There is no objective, no algorithm and no theory.** It is a grid of one-variable-at-a-time ablations with static sampling weights. Method statements are the standard next-token objective; the contribution is empirical.

**Setup.** Decoder-only transformers, **2B** (24 layers, hidden 2048, 16 heads) and **8B** (32 layers, hidden 4096, 32 heads); RoPE, SwiGLU, no bias terms, untied input–output embeddings, SentencePiece 256k, context 4096. Token horizons **150B–450B**. Evals: LM-Eval-Harness zero-shot **LAMBADA, ARC-easy, Race-H, PIQA, Winogrande, HellaSwag** (the "LM-Eval" column is the mean of these six — I verified this reproduces on 6 of 9 rows of Table 9 and on all three UniMax arms of Table 6); **MMLU** "*when the experimental setting allows for a non-random score*"; **HumanEval / MultiPL-E** for code; **XCOPA / TyDiQA-GoldP** for multilingual.

**Code/artefact links.** Domain classifier released: `huggingface.co/nvidia/domain-classifier`. Toxicity, quality and type-of-speech classifiers "*plan to publicly release … shortly*" (unreleased at publication). No data pipeline, no blend configs, no training code.

---

## 3. Every quantitative result

**Curation (2B, 300B tokens) — Table 2 / Table 18**
Raw text **57.18** → post-deduplication **58.93** → post quality filtering **59.50**. Per-task: LAMBADA 55.6→57.8→58.3, ARC-e 57.2→59.1→60.2, Race-H 39.9→39.9→41.0, PIQA 73.9→76.6→75.4, Winogrande 57.6→56.9→58.7, HellaSwag 58.9→63.3→63.5. (Note PIQA and Winogrande are non-monotone.)

**Dedup retention priority (2B, 300B) — Table 3 / Table 19**
Old-to-Recent **60.47** > Random **59.96** > Recent-to-Old **58.93**. **Prioritise keeping older documents**; the spread is 1.54 points.

**Selection / DSIR (2B, 165B, two CC snapshots) — Table 4 / Table 20**
Original CC 54.30 · DSIR 54.44 · Corpus DSIR 54.44 · **Source DSIR 54.71** · DSIR(80%) 54.55 · DSIR(87.5%) 54.25 · **DSIR(95%) 54.71**. Per-source beats per-corpus; the paper-recommended 95% retention is optimal. *All gains here are ≤0.41 — see the noise-floor discussion in §5.*

**DSIR target-set sensitivity — Table 5 / Table 21**
{Wikipedia, Books} **54.71** · {Wikipedia, Books, arXiv, NIH} 54.02 · {arXiv, NIH} 53.71. Adding a "high quality" source **costs 0.69**.

**Sampling, English (8B, 300B, 19–20 sources, 1219.0B pool) — Table 6 / Table 22 / Figure 7 — THE KEY RESULT**

| Method | LM-Eval | MMLU | UniMax plateau | Plateau width | Sources > 1 epoch | Budget drawn from repeated sources | Max epochs |
|---|---|---|---|---|---|---|---|
| Preference (hand-tuned) | 65.85 | 27.20 | — | — | — | — | — |
| **UniMax (1e)** | **67.14** | **28.30** | **7.25%** | 11 of 20 | **0** | **0.0B (0.0%)** | **1.00** |
| UniMax (2e) | 66.50 | 28.00 | 6.28% | 14 of 20 | 9 | 92.7B (30.9%) | 2.00 |
| UniMax (4e) | 66.61 | 26.60 | 5.55% | 17 of 20 | 8 | 100.4B (33.5%) | 4.00 |
| DoReMi | 65.63 | 26.90 | — | — | — | — | **13.80** |

The plateau / width / epoch columns are **mine**, from digitising Figure 7 and reproducing UniMax from its published algorithm (§7); the LM-Eval and MMLU columns are the paper's. Uniform over 20 sources would be 5.00%, so the 4e arm is nearly uniform — which is the paper's own second explanation for the degradation.

> Authors, verbatim (§5.2.1, verified against the rendered page): "*despite still outperforming both other methods, the performance of UniMax degrades as the maximum epoch hyperparameter increases. We hypothesize that as we have far more data tokens than the amount of training tokens, repeated epochs of data provide less utility than novel information. We suggest that practitioners choose the minimal value of the epoch hyperparameter that makes sense for their datasets and training budget.*"

**Sampling, multilingual (8B, 300B, 53 sources, 597.41B pool) — Table 7:** given in §1 above. Only UniMax(1e) was tested; **no epoch sweep on multilingual.**

**Sampling, code (8B, 150B, 41 languages, 211.88B pool) — Table 8 / Table 23**
Alpha(α=1.3) MultiPL-E **19.72** / HumanEval **20.73** · UniMax(1e) 19.33 / 20.12. DoReMi **excluded from the ablation entirely** because it "*placed over 80% of the weight on a single programming language*". Per-language (Table 23): HumanEval 20.72 vs 20.12; MP-Python 20.5 vs 19.3; MP-Java 23.4 vs 20.9; MP-JS 20.5 vs 19.9; MP-CPP 19.3 vs 19.3; **MP-Lua 14.5 vs 17.4**.

> **Lua is the tell.** UniMax loses on the four high-resource languages and **wins by +2.9 on Lua (1.00B, the smallest of the five evaluated)**. Alpha wins the aggregate because, in the authors' words (§5.2.3, verified from the rendered page): "*Given that we mainly evaluate on high resource languages, we find it natural that alpha sampling, which places high weight on high resource languages without dramatically undersampling low resource languages, performs best.*" **Which sampling method "wins" is determined by which languages are in the eval set.**

Also §5.2.3, a mechanism claim: "*we did not find there to be a strong transfer ability between programming languages as has been seen for multilingual languages*" — natural-language families transfer, programming languages do not. The cited basis for family transfer is K et al. 2020 / Hu et al. 2020 / Ye et al. 2023, not a measurement in this paper.

**Code curation (8B, 150B) — Table 17:** raw source code HumanEval 16.5 / MultiPL-E 15.9 → post quality filtering **20.7 / 19.2** (+4.2 / +3.3). The largest single effect in the paper.

**Attribute-bucketed sampling (2B, 165B, five CC snapshots) — Table 9 / Table 24**
Baseline (proportional-to-token-count over the 5 snapshots) **56.81**. Buckets defined either *fine-grained* (partition each source by attribute) or *grouped* (attribute buckets across the whole corpus); weights then set by **UniMax with the epoch cap at 2**.

| Attribute | Fine-grained | Δ | Grouped | Δ |
|---|---|---|---|---|
| Quality | **57.88** | **+1.07** | 57.19 | +0.38 |
| Domain | 57.34 | +0.53 | **57.45** | +0.64 |
| Type of speech | 56.69 | **−0.12** | 57.31 | +0.50 |
| Toxicity | 53.62 | **−3.19** | 54.99 | **−1.82** |

Rule the paper draws: broad-class attributes (domain, type of speech) are better *grouped*; document-characteristic attributes (quality) are better *fine-grained*. **Toxicity is the only attribute that hurts, in both settings.**

**Attribute-defined DSIR target sets — Table 10:** Original CC 54.90 · DSIR {Wikipedia, Books} 55.35 · DSIR {Low toxicity, High quality} **55.63**. *The baseline here (54.90) differs from Table 4's Original CC (54.30) and the paper never states Table 10's snapshot count — treat the +0.73 as within-table only.*

**Classifier quality (Appendix B).** Toxicity: DeBERTaV3 fine-tuned 1 epoch on 320k Jigsaw examples; **Pearson 0.8** vs Perspective API on 50k CC docs; **AUC-ROC 0.83** vs Perspective's 0.85 on 500 human-labelled docs. Domain: 27 classes, 1M CC + 500k Wikipedia, 2 epochs, **77.9%** accuracy vs Google NL API's 77.5%. Quality: 3 classes, 25k Surge AI-annotated CC docs (≥2 of 3 annotators agreeing), **83%** on 23k held out. Type of speech: 11 classes, same 25k, **79.5%**.

---

## 4. Figures — all 14 inspected from pixels

Extracted with PyMuPDF to `figs/pN-imgM.png`; each read inline. **No figure in this paper has an error bar, confidence band, or seed count. Every result is n=1.**

| # | File | Type / axes | What the pixels show |
|---|---|---|---|
| **1** | `p2-img0` (1232×229) | Schematic, no axes | Five-stage pipeline: source boxes (Books / Multilingual / Web Crawl / News / Scientific / Conversational / Source Code) → curation (coloured blocks shrinking; trimmed documents) → selection (documents with green ✓ / red ✗) → sampling (horizontal bars of unequal length) → final set (dot grid). Stage captions render black-on-black in the embedded image; recovered from the caption text. **No quantitative content.** |
| **2** | `p6-img0` (1000×700) | Bar. y `Percentage of Documents` 0–27, ticks /5; x 11 speech types | Values **printed on bars**: Websites 27.02, News 19.55, Blogs 17.23, Analytical Exposition 11.40, Explanatory Articles 9.78, Online Comments 6.52, Reviews 4.23, MISC 2.59, Boilerplate 0.70, Books & Literature 0.52, **Conversational 0.46**. Sums to **100.00**. ⚠ Body text claims these top three are "*over 65%*"; **they are 63.80%.** |
| **3** | `p6-img1` (1100×700) | Bar. y `Percentage of Documents` 0–8.55, ticks /2; x 27 domains | Printed: Arts & Entertainment 8.55, Health 6.17, Computers & Electronics 6.06, Business & Industrial 5.57, News 5.36, People & Society 5.33, Sports 5.00, Food & Drink 4.52, Jobs & Education 4.29, Home & Garden 4.18, Travel 3.79, Hobbies 3.47, Games 3.25, Books & Literature 3.05, Sensitive Subjects 3.02, Beauty 2.90, Autos 2.88, Finance 2.84, Shopping 2.72, Reference 2.55, Real Estate 2.53, Law & Government 2.45, Internet & Telecom 2.40, Adult 2.17, Online Communities 1.83, **Science 1.71**, Pets 1.41. Claim: technical domains (finance, law, science) are least represented — augment from SEC filings / Court Listener / academic papers. |
| **4** | `p7-img0` (1273×851) | Stacked bar, Low/Medium/High legend. y `Percentage of Documents` 0–100, ticks /20; x 27 domains sorted by descending High | **Digitised.** Max **High** in *any* domain is **Science 3.21%**; Health 1.92, Sensitive Subjects 1.71, Law & Government 1.71, People & Society 0.85, News 0.85, then ≤0.64 and **0.00 for the last six**. **Low**: Sensitive Subjects 8.5 (lowest), News 8.1, Food & Drink 8.8, Sports 9.0, Hobbies 9.2 … Reference 28.0, Computers 28.2, Games 35.5, **Online Communities 54.1, Adult 85.5**. Claim: technical domains hold the most high-quality content; adult / online communities the least. |
| **5** | `p7-img1` (1300×900) | Heatmap, values printed. Rows 27 domains (alphabetical); cols 10 toxicity bins (0.0,0.1]…(0.9,1.0]; colourbar `Percentage of Documents` ticks 20/40/60/80 | Rows sum to 100 (Adult: 17.03+6.09+4.74+4.19+4.10+4.42+5.20+6.91+10.60+36.72 = **100.00**). Cleanest: Real Estate 98.65 in the lowest bin, Jobs & Education 97.13, Finance 96.25, Travel 96.01, **Science 96.02**. Dirtiest: **Adult 17.03 lowest-bin / 36.72 in (0.9,1.0]**; Pets & Animals 70.68; Online Communities 73.93; **Sensitive Subjects 75.27** — the "high quality *and* high toxicity" case the paper uses to explain why toxicity filtering has hurt accuracy in prior work. |
| **6** | `p23-img0` (1400×500) | Twin-axis. Left (blue bars) `number of tokens (B)` 0–175 ticks /50; right (lines) `sampling weight (%)` 0–60+ ticks /20; x 20 English sources. Legend: Preference (light coral), UniMax 1e (crimson), DoReMi (dark maroon) | **Digitised; DoReMi trace sums to 100.2% → accurate.** **DoReMi puts 64.38% of a 300B budget on OpenWebText2, a 14.0B source = 13.80 epochs**, plus 24.56% on Reddit+Conv (1.25 epochs) and ≈0 on the other 17. UniMax 1e plateaus at 7.25% then tapers (ArXiv 6.15, OpenWebText2 4.66, StackExchange 3.26). ⚠ The body blames DoReMi's failure on weight "*heavily skewed towards web crawl snapshots*"; the figure shows the spike on **OpenWebText2**, the 13th-largest source. |
| **7** | `p23-img1` (1400×500) | Same twin-axis; right axis ticks 0/2/4/6; three UniMax arms (1e crimson, 2e rosy-brown, 4e red) | **Digitised and matched to a from-scratch UniMax simulation to ±0.08pp on all 57 points** (§7). Plateau falls and widens as the cap rises: **7.25% × 11 sources → 6.28% × 14 → 5.55% × 17** (uniform = 5.00%). Tail: NIH_ExPorter 0.02→0.04→0.09; BookCorpus2 0.52→1.02→2.04; Gutenberg 0.84→1.69→3.38. **This is the plot that shows raising the epoch cap converts the distribution toward uniform while simultaneously permitting repetition — the confound of the headline result.** |
| **8** | `p24-img0` (1400×500) | Same twin-axis; left 0–90+ ticks /20, right 0–20 ticks /5; x = 52 language codes **plus `NMT`** (3rd, bar = 55.95B ⇒ the 56B parallel corpus). Legend: Alpha Sampling, UniMax, DoReMi | **Digitised and reproduced exactly as UniMax(1e, 300B)** (§7). Cap **5.55% = 16.65B** on the top 8 (RU→IT); every source below it at **exactly 1.00 epoch**; RU down-weighted to **0.176 epochs**. DoReMi peaks at **DE ≈ 17.6%** and collapses to ≈0.03–0.1% across the entire low-resource tail — including all nine Indic languages. My tail readings floor out at ≈0.3% (5 px), so tail values are reported from the reproduction, not the trace. |
| **9** | `p24-img1` (1400×700) | Same twin-axis; left 0–21 ticks /2.5, right 0–80 ticks /10; x 41 programming languages | **Digitised; DoReMi sums to 100.8% → accurate. DoReMi puts ≈77.6% of a 150B budget on markdown, a 20.27B source = 5.74 epochs** (body text says "*over 80%*" — the plotted line centre reads 77.6%, so quote the text's claim as approximate). **Alpha reproduced exactly as `tokens^1.3` normalised** (±0.15pp on the head), confirming the α=1.3 formula. UniMax(1e) plateau 6.93% observed / 6.98% simulated = 10.48B, with 33 of 41 languages at exactly 1 epoch. |
| **10** | `p25-img0` (800×500) | **Pie**, labels printed, no axes | **Medium 81.3% · Low 18.2% · High 0.5%** across 90+ CC snapshots. Sums to 100.0. **The single most consequential number in this paper for our §1.** |
| **11** | `p25-img1` (1025×696) | Bar. y `Percentage of Documents` 0–85 ticks /20; x 10 toxicity bins | **Digitised** (values not printed; my trace sums to 98.6%, so ±0.3pp): (0,0.1] **85.7**, (0.1,0.2] 4.2, (0.2,0.3] 2.2, (0.3,0.4] 1.5, (0.4,0.5] 1.0, (0.5,0.6] 0.9, (0.6,0.7] 0.7, (0.7,0.8] 0.6, (0.8,0.9] 0.6, (0.9,1] 1.2. **≈92% of CC documents fall below the paper's 0.3 toxicity threshold.** |
| **12** | `p25-img2` (1300×900) | Stacked bar, Low/Medium/High. y `Percentage of Documents` 0–100 ticks /20; x 10 `KenLM Perplexity` bins (0,100]…(900,1000] | **Digitised. Monotone in both directions.** Low: **6.1 → 7.8 → 16.9 → 28.4 → 39.6 → 49.4 → 57.4 → 63.5 → 68.6 → 73.4**. High: 1.92 → 0.59 → 0.30 → 0.15 → 0 thereafter. Claim: the classifier and the n-gram LM "*have high agreement on documents which they classify as high or low quality*". **No correlation coefficient is reported for this pair** (unlike toxicity's Pearson 0.8). |
| **13** | `p25-img3` (1300×900) | Stacked bar, Low/Medium/High. y 0–100 ticks /20; x 11 speech types sorted by descending High | **Digitised** (my tick detection missed the 0 gridline; values rescaled so the un-occluded bars close to 100 — Websites checks at 99.93). Low: Explanatory Articles 15.4, **News 5.3**, Websites 18.1, Reviews 15.3, Analytical Exposition 21.0, Blogs 11.1, Conversational 23.4, Books & Literature 25.4, **Boilerplate 85.0, MISC 93.6**, Online Comments 39.2. **Max High in any speech type = Explanatory Articles 1.82%**, News 1.16, Websites 0.33, then 0. Claim: filter out web domains dominated by boilerplate/MISC. |
| **14** | `p25-img4` (1216×872) | Heatmap, values printed. Rows 27 domains; cols 11 speech types; colourbar `Percentage` 10–80 | Adult→MISC **84.72**; News→News **71.50**; **Sensitive Subjects→News 59.59**; Sports→News 58.81; Real Estate→Analytical Exposition 52.78; **Science→Explanatory Articles 41.28**; Law & Government→News 35.59. Confirms the §6.2 reading that "sensitive subjects" is mostly war/protest reporting rather than genuinely toxic content. |

---

## 5. Noise floor — derived from the paper's own non-monotonicity

The paper reports **no seeds and no error bars anywhere**. But it hands us a lower bound: on LM-Eval the UniMax arms run **1e 67.14 → 2e 66.50 → 4e 66.61**. The 2e/4e **inversion** means run-to-run (or arm-to-arm) variation is **at least ≈0.11 LM-Eval** with more epochs scoring *better*, so any ordering built on a gap of that size is unreadable. Consequences, applied without mercy:

- **Readable:** the 1e-vs-4e **MMLU** gap of **−1.70** (≈15× the implied floor); DoReMi's **−2.31 TyDiQA** vs UniMax; **toxicity bucketing −3.19 / −1.82**; **code curation +4.2 HumanEval**; **dedup priority spread 1.54**; **curation +2.32**; **quality-bucketed sampling +1.07**.
- **NOT readable — do not cite as evidence:** the entire multilingual method preference (**UniMax − alpha = +0.13 XCOPA / +0.25 TyDiQA**; the paper itself only claims "slightly outperforms"); every DSIR result (**+0.14 to +0.41**); domain and type-of-speech bucketing (**+0.50 to +0.64**); the code aggregate (**+0.39 MultiPL-E / +0.61 HumanEval**).

Independently, **three of the nine rows of Table 9 do not reproduce as the mean of their own per-task appendix values** (Table 24, verified by rendering p. 24 at 200 dpi): Baseline 56.81 vs computed 56.88; **Quality-grouped 57.19 vs 56.80 (−0.39)**; **Toxicity-fine-grained 53.62 vs 52.27 (−1.35)**. Six rows reproduce to ±0.02. Table 6's three UniMax arms all reproduce exactly (67.15 / 66.50 / 66.63), so **my headline numbers are internally verified** — but Table 9's aggregate column is not dependable to better than ~1 point.

**Minor text-vs-artefact mismatches found (a calibration signal, since our spec leans on this lab's sibling paper):** "over 65%" vs Figure 2's 63.80%; §4.2's "54.48" vs Table 4's 54.44; "the remaining 42 languages" vs Table 14's 41; Table 8's HumanEval 20.73 vs Table 23's 20.72; Table 20's ARC-easy "5.40" (should be 54.0); "over 80%" vs Figure 9's ≈77.6%. All small, none reverse a finding — but they mean **quote the table/figure, not the prose**.

---

## 6. Assumptions, explicit and implicit

- **Explicit (Limitations):** findings are bounded to their source distribution, learning algorithm and model configuration; not an exhaustive method ranking; **synthetic data entirely excluded and disclaimed for transfer**.
- **Implicit — supply exceeds budget.** English 1219.0B pool against a 300B budget (**4.06× surplus**), multilingual 597.41B against 300B (1.99×), code 211.88B against 150B (1.41×). **Repetition is always optional for them.** Our tier C (5.0B for 25.3B demand) and agentic (0.627B for 40B) have no surplus at all — repetition is forced. Their result therefore says *"do not repeat when you need not"*, which is strictly weaker than *"the k-th epoch costs X"*.
- **Implicit — one static distribution for the whole run.** No ordering, no phases, no LR interaction with the mixture.
- **Implicit — a language is a source.** Sampling operates over languages and over the parallel corpus as one blob. No provenance tiering within a language, which is exactly our Indic A/B/C/D axis.
- **Implicit — quality is a 3-class document property from an English-annotated classifier**, applied corpus-wide including to the 52 non-English languages, with **no non-English validation reported**.
- **Implicit — MMLU is unreadable below 8B/300B.** They report MMLU *only* for the 8B/300B English sampling runs and state it is used "*when the experimental setting allows for a non-random score*". Every 2B/165B and 2B/300B table omits it.

### Threats to validity against a 2.0T / 120B seven-lane multilingual run

1. **Scale gap of 15×–250×.** 8B/300B vs 120B/2.08T; 4096 context vs 8192. Direction only, never magnitude.
2. **n=1 throughout.** See §5.
3. **The headline epoch result is confounded.** Raising the cap 1→4 both permits repetition *and* flattens the distribution toward uniform (plateau 7.25% → 5.55%, uniform 5.00%). The paper offers the repetition explanation in §5.2.1 and the uniformity explanation in Appendix E — **two explanations, one result, same authors, same paper.** It is not a clean repetition penalty and must never be cited as one.
4. **Seven-lane structure absent.** No agentic, no long-context, no reasoning-trace lane, no STEM lane. Their categories are web/news/books/scientific/conversational/misc/multilingual/code.
5. **Eval set determines the winner.** Demonstrated within the paper (alpha wins code because the eval is high-resource; UniMax wins Lua). Any mixture conclusion here is conditional on an English-and-high-resource-heavy benchmark suite.
6. **No Indic evaluation.** XCOPA and TyDiQA-GoldP aggregates only; **no per-language multilingual results are published**, so Indic-subset sensitivity is unverifiable from this paper.

---

## 7. What I reproduced (the digitisation, and why it is trustworthy)

Rather than eyeball the sampling plots I traced each line by colour against detected axis ticks, then **re-derived the same curves from the published algorithms** and compared.

- **Figure 7 (English, 3 arms × 19 sources):** UniMax(N, B=300B) simulated from Chung et al.'s allocation rule over the Table 11 source list. **Agreement ±0.08pp on all 57 points**; observed sums 99.8 / 99.6 / 99.5 vs a simulated 100.00.
- **Figure 8 (multilingual, 53 sources):** UniMax(N=1, B=300B) over Table 12 + the 56B parallel corpus. **Agreement ±0.05pp on all 28 readable points**; simulation sums to exactly 100.0. Recovered plateau 5.551% = 16.65B.
- **Figure 9 (code, 41 languages):** UniMax(N=1, B=150B) matches to ±0.05pp; **alpha sampling matches `tokens^1.3` normalised to ±0.15pp on the head**, confirming the α=1.3 exponent operates on raw token counts.
- **Figure 6 (English, DoReMi):** trace sums to 100.2%, so the 64.38% OpenWebText2 spike is solid.
- **Bar-height cross-check:** the blue token bars in Figure 8 recover NMT = 55.95B (Table 1: 56B) and RU = 94.72B (Table 12: 94.52B). Table 14 sums to 211.88B (Table 1: 212B). Table 11 sums to 1219.0B and reconciles row-by-row with Table 1's six English categories.

Digitisation limits, stated: line-tracing resolves ≈0.06 pp/px, so **tail values below ≈0.3% are reported from the reproduction, not the trace**; where two lines overlap, the Alpha/Preference traces are contaminated (their sums come to 114–131%) and are used qualitatively only. Every number I quote in §3 and the Verdict is either printed in the paper, or from a curve whose trace sums to 100 ± 1%, or from the validated reproduction.

Artefacts saved under `session_5_era_v5/papers/emnlp596/`: `paper.pdf`, `figs/p*-img*.png` (14 native + 3× upscales + Figure 8 head/tail crops), `pages/page-{05,06,07,24}.png` at 200 dpi and the Table 6 / 7 / 8 / 24 crops used to settle extraction ambiguities.

**`verify.py` reproduces every load-bearing number in this brief and needs no dependencies** — `python3 verify.py` re-derives the Indic supply totals, the UniMax(N) weight vectors for Figures 7/8/9 against the digitised values, alpha sampling as `tokens^1.3`, the DoReMi epoch counts, and the six-task LM-Eval means behind Tables 6 and 9. It currently prints **ALL CHECKS PASSED** (36 assertions), and it is what caught the three Table 9 rows that do not reproduce.

---

## 8. Implementation nits worth keeping

- Curation = 128-bit-hash exact dedup + fuzzy dedup (Smith et al. 2022b) + **KenLM perplexity** + ~23 heuristic filters with published thresholds (**Table 15**: e.g. n-gram LM perplexity threshold 5000, non-alphanumeric fraction 0.25, boilerplate fraction 0.40, four hard constraints including "<50 or >100k words" and "mean word length <3 or >10"). Several are marked **English Only** — including the two word-count and common-English-word constraints, which is exactly where an Indic pipeline would need its own thresholds.
- Code filtering (**Table 16**, following StarCoder/SantaCoder): comment-character fraction 0.001–0.85, lines of code 5–20 000, characters-per-token ≥ 2.
- Reddit: longest thread per post only, usernames anonymised, Perspective API toxicity ≥ 0.5 dropped.
- ZH/JA came from mC4 rather than their own extraction "*as a consequence of the inability of our text extraction library to parse languages without spacing*" — a concrete, citable extraction-tooling failure mode for non-space-delimited scripts.
- **DSIR** is the only selection method ablated, chosen for low compute overhead as a Moore–Lewis descendant; recommended setting is per-source at 95% retention.

---

## 9. Overlap with `two-phase` (2412.15285) — Main's explicit question

**Verdict: complementary, not duplicative. Neither of the two numbers our spec attributes to `two-phase` originates here, and on one of them this paper is a challenge.**

| Our spec's claim | Where it really comes from | What this paper says |
|---|---|---|
| "Natural CC is **64.44% Low**" (§1 Filters) | **`two-phase` Table 16**, using the **Nemotron-CC 5-bucket classifier** (Su et al. 2024, 2412.02595) over 99 CC snapshots. **Not from this paper.** Cite `two-phase` as primary. | **Challenges the framing.** Same lab, **90+ CC snapshots**, their *own* 3-class DeBERTaV3 quality classifier (83% held-out accuracy): **18.2% Low / 81.3% Medium / 0.5% High** (Figure 10). Different classifier, different label space, different unit (documents here) — so not a contradiction of the *policy*, both papers agree quality gating helps. But "*natural CC is 64.44% Low*" as stated reads as a property of CC, and the same lab's broader analysis puts it at 18.2%. **Needs scoping to the 5-bucket classifier.** |
| "zeroing Low and upsampling High lifts MMLU **42.94 → 56.10**" (§1) | `two-phase` Tables 16–17. **Not from this paper.** | **Refines the supply side.** "Upsampling High" has a hard ceiling: **High is 0.5% of CC documents**, with a maximum of **3.21% in any of 27 domains** (Figure 4, Science) and **1.82% in any of 11 speech types** (Figure 13, Explanatory Articles). Six domains read **0.00% High**. |
| "Two-Phase's **6-epoch** ceiling on high-quality crawl; 8 for math; 12 hurts" | `two-phase` Figure 4 / Table 13. **Not here — this paper has no single-source epoch ceiling sweep.** | **Challenges its transfer to small sources.** `two-phase`'s 6 epochs is measured on high-quality *crawl* (a ~400B post-downsample pool) at a **fixed share**. This paper's epoch sweep is on **small** English sources (ArXiv 18.7B, OpenWebText2 14.0B, StackExchange 9.8B, Stories 5.3B, Wikipedia 4.3B, PubMed 4.2B, Gutenberg 2.5B, BookCorpus2 1.5B) whose share *rises* with the cap — and there **1 epoch beats 2 and 4**, with MMLU falling monotonically 28.30 → 28.00 → 26.60. **The two results are not in conflict, but they license opposite conclusions depending on source size — and our scarce lanes are small sources.** |
| "9 languages derived from Wikipedia and Common Crawl", flat 5% / 3.7% | `two-phase` §3.1 — never enumerated. | **Strictly dominates.** 52 languages with token counts, 9 of them Indic, plus a 32-language parallel corpus. This paper is where the multilingual detail lives. |
| DoReMi as a mixture optimiser | `two-phase` explicitly declines to use it (hand grid). | **Supplies the measurement `two-phase` skipped**: DoReMi degenerates to a single source in **two of three domains** — English OpenWebText2 64.38% (13.80 epochs), code markdown ≈77.6% (5.74 epochs) — and loses on English (LM-Eval 65.63 / MMLU 26.90, worst of five) and on multilingual (TyDiQA 15.8, **−2.31** vs UniMax). |

**Classifier-based vs heuristic selection (Main's other ask).** Both are used, in sequence: heuristics + **KenLM perplexity** during curation, then the DeBERTa classifiers for attributes, then DSIR for selection. The load-bearing result for us is **Figure 12**: the 3-class classifier and KenLM perplexity agree monotonically on English CC — Low rises **6.1% → 73.4%** across perplexity (0,100] → (900,1000], High falls **1.92% → 0**. Since a KenLM n-gram model is cheap to train per language on a small verified seed, **this is a concrete portable substitute for the untransferable English classifier in our §2 hazard 2** — with the caveat that the agreement itself is demonstrated on English only and no correlation coefficient is published for that pair. Note also that several Table 15 heuristics are explicitly flagged **English Only**, so the heuristic half does not transfer for free either.

---

## 10. VERDICT

### (a) Scope

**Squarely in scope. This is a pretraining-data / mixture paper — the most in-scope paper in the evidence base on the *sampling-weight* axis specifically.** It ablates curation, selection and **sampling weights over sources** on a >2T pool of English + multilingual + code at 2B/8B, and it is the only paper we hold with named Indic languages and token counts.

**One structural limit, stated plainly: it is a *mixture* paper, not a *curriculum* paper.** Every result is a single static distribution held for the whole run. It contributes to §1, §2 and §5 and contributes **nothing** to §4 (anneal) or §6 (curriculum, stages, seams, ordering).

### (b) Which of the ten open weaknesses it touches

| # | Weakness | Touched? | How |
|---|---|---|---|
| **2** | **Indic tier C at 5.06× on 5.0B parallel** | **Yes — most of all** | External supply corroboration (their whole 32-language parallel corpus has **0.655B Hindi and zero other Indic**); plus a measured penalty for repeating 1.5–18.7B sources that argues **against** us |
| **6** | Difficulty ladder B0–B5 unsupported | **Yes** | First evidence that **attribute-bucketed sampling works at all**: quality-bucketed **+1.07** fine-grained, and a rule for when to bucket per-source vs globally |
| **8** | Is a 1B/3B proxy the right instrument, and what metric is readable | **Yes, adversarially** | NVIDIA reports MMLU **only** at 8B/300B, "*when the experimental setting allows for a non-random score*" — our **H4 and H5 name MMLU at 1B**. Also supplies XCOPA / TyDiQA-GoldP as multilingual metrics that separated mixtures at 8B/300B |
| **10** | The OPUS floor | **Yes** | A **second, independent** instance of the CLIMB C20→0 failure: a learned mixture optimiser drove one source to 64.38% / ≈77.6% and lost, in two of three domains |
| **3** | Reasoning lane 4.00 epochs on 7.1B traces | **Partly** | Same small-source repetition penalty applies; 7.1B sits in their degraded band |
| 1 | Agentic 2.00% / 73.4× | No | Nothing agentic; and the authors disclaim synthetic transfer |
| 4 | Long-context / multi-document | No | Context 4096, no long-context eval |
| 5 | Anneal size 80B | No | No anneal exists in this paper |
| 7 | Reasoning-length split | No | — |
| 9 | Seam width 20B | No | No transitions exist |

**Four of ten, two of them among the four "all papers silent" gaps.**

### (c) Which SOLUTION.md numbers it confirms, challenges or refines — by section

**§2 Indic tier split A40 / B30 / C8 / D22 — the paper bears on it, unevenly.**

- **Tier C (8%, 25.3B demand, 5.0B supply, 5.06×) — CHALLENGED on repetition, SUPPORTED on scarcity.**
  - *Supported:* NVIDIA's production-scale multilingual build drew its parallel corpus from CC-Matrix + CC-Aligned + ParaCrawl and got **56B across 32 languages with Hindi the only Indic member at 1.17% = 0.655B, and zero Bengali / Tamil / Telugu / Marathi / Malayalam / Kannada / Nepali / Urdu** (Table 13, §A.2). Our tier-C pool of 5.0B (BPCC + Samanantar) is **7.6× larger** than what the generic sources yielded — which both vindicates "translated Indic is genuinely supply-limited" and shows our 5.0B depends **entirely** on AI4Bharat-specific corpora, not on anything a generic pipeline reaches.
  - *Challenged:* tier C is a **5.0B source**, in exactly the size band (1.5–18.7B) where this paper measures repetition hurting. **The available defence "5.06× is inside Two-Phase's 6-epoch organic ceiling" is weakened**, because that ceiling was measured on a ~400B pool at fixed share, whereas the small-source result here is that **1 epoch beat 2 and 4** with MMLU falling 28.30 → 26.60. This makes tier C a *better* attack surface than our §8 already says, and it strengthens the case for H3's refute branch (C → 4%).
  - *Unmoved:* **A40 / B30 / D22 get no ratio from this paper.** There is no provenance tiering within a language anywhere in it. Tier D is **explicitly out of scope** by the authors' own Limitations disclaimer on synthetic data.
- **The Indic-up anneal at 21.875% — NOT ADDRESSED. No support, no refutation.** This paper has no anneal, no phases and no mixture change over time. **H5 keeps MAP-Neo as its only counter-precedent.** The one adjacent signal, and it is only an analogy: upsampling a low-resource family member helped that member and cost the high-resource ones (**Lua +2.9; Java −2.5, Python −1.2**) — which is the shape of the trade H5 tests, measured on programming languages, in a static mixture, at 8B.
- **§2 hazard 2 ("the quality classifier does not transfer") — REFINED, and this is the cleanest gift in the paper.** Figure 12 gives a portable substitute: KenLM n-gram perplexity tracks the 3-class quality label monotonically (Low 6.1% → 73.4%; High 1.92% → 0). A per-language KenLM on a verified Indic seed is cheap and script-agnostic. Caveat: agreement shown on English only, no coefficient published, and several Table 15 heuristics are flagged **English Only**.
- **§2 hazard 3 ("never score Indic on a global utility median") — CONFIRMED by a second mechanism.** Table 9's rule is that document-characteristic attributes work **fine-grained** (per-source, **+1.07**) and are worse **grouped** (corpus-wide, **+0.38**). Our per-lane scoring is the fine-grained choice.

**§1 Filters — CHALLENGED on scoping, REFINED on supply.** "Natural CC is 64.44% Low" is a property of the Nemotron-CC 5-bucket classifier on `two-phase`'s snapshot set, not of CC: the same lab's 3-class classifier over 90+ snapshots reports **18.2% Low / 81.3% Medium / 0.5% High** (Figure 10). And "upsampling High" is supply-capped: **High is 0.5% of documents**, max **3.21%** in any domain, max **1.82%** in any speech type, **0.00%** in six domains.

**§1.3 long-context — weak precedent only.** NVIDIA also concatenated per-repository files into single long documents "*to allow the model to attend across files*" (§A.3), which is independent production precedent for our repo-packing choice — but at 4096 context with no long-context metric, so it does not answer the multi-document gap.

**§5 the protected floor — CONFIRMED, with a second independent instance.** Our §5 rests on CLIMB's code cluster C20 → 0. This paper shows the same pathology twice more, from a different optimiser: DoReMi concentrated **64.38% of a 300B English budget on a 14.0B source (13.80 epochs)** and **≈77.6% of a 150B code budget on markdown (5.74 epochs)**, was the **worst of five** English arms, lost multilingual TyDiQA by **2.31**, and was **excluded from the code ablation entirely** because it "*does not allocate enough tokens to facilitate model learning during training for the remaining 42 languages*". That last clause is our floor argument in NVIDIA's own words.

**§5's 5.5% Indic floor — INDEPENDENTLY CORROBORATED, and this is the best news in the paper for us.** The floor was derived purely internally as the largest Indic floor staying inside one epoch of the 113.9B real pool. This paper serves Indic at **exactly 1.00 epoch**, and umT5 does too (48.2B of a 48.4B pool). **Two independent labs land on the number we reasoned our way to**, so "one epoch of real Indic" is now observed convention rather than our arithmetic.

The derivation is *binding*, not a coincidence, and the spec already contains the boundary: §5 states 5.70% is the largest floor inside one epoch. I re-derived the ladder against the 113.9B real pool over a 2.0T main run — **5.0% = 0.878 ep · 5.5% = 0.966 ep · 5.70% = 1.001 ep (the exact boundary) · 6.0% = 1.054 ep** — so **5.5% is the largest half-point step that stays inside one epoch**, and one epoch is where both disclosed builds sit. Credit to `UniMaxPaper` for pressing the point; the numbers are ours and check out.

The same frame prices §1: **15.80% is 2.77 epochs on real Indic, 2.8× both published builds**, falling to 1.14 only if tier D's synthetic counts as supply — E9's named failure mode, and the v3 red-team's W9. Note *why* this frame is the right one: **percentages are not comparable across the three builds** (their budgets are 1.163T, 300B and 2.08T, and NVIDIA's is a multilingual-arm share with no combined run), whereas **epochs on the real pool are**. That is the common currency for any Indic comparison we make.

**§7 proxy protocol — CHALLENGED, usefully.** NVIDIA reports MMLU **only** at 8B/300B and omits it from every 2B/165B and 2B/300B ablation, on the stated ground that the setting must "*allow for a non-random score*". **H4 uses "core avg of MMLU + GSM8K + HumanEval" at 1B and H5 uses "MMLU as forgetting check" at 1B.** If MMLU is judged unreadable at 2B/300B by the people who ran it, it is not readable at 1B/100B. §7 already concedes this for H2/SWE-bench; the concession must extend to MMLU. Constructively: their 2B-readable set is the six-task LM-Eval mean (LAMBADA / ARC-easy / Race-H / PIQA / Winogrande / HellaSwag), and their 8B multilingual metrics **XCOPA and TyDiQA-GoldP** did separate mixtures (DoReMi −2.31 TyDiQA) — better-grounded small-scale candidates than MILU / IndicGenBench chrF, for which we have no sensitivity evidence at all. *Honest caveat: no per-language multilingual results are published, so Indic-subset sensitivity is unverified; XCOPA's Tamil and TyDiQA's Bengali/Telugu coverage is [INFERENCE] from the benchmarks' standard language sets, not from this paper.*

**§6a difficulty bands — PARTIALLY SUPPORTED for the first time.** Our §6a currently concedes "No paper supports a content-difficulty ladder and one argues against it". That concession can now be softened, precisely: attribute-bucketed sampling **beats an un-bucketed baseline by +1.07 LM-Eval** (2B/165B) when the attribute is a document-quality characteristic applied per-source. This does **not** validate a 6-level *difficulty* ordering (their quality attribute is 3-class) and it is **not** a curriculum (static weights, no ordering over time) — but "bucket the corpus by a document attribute and reweight" is no longer unprecedented.

### (d) Keep or drop

**KEEP — and it earns more space than any of the last four papers added.** Reasons, against E3:

1. It is the **only** paper in the base with Indic token counts, and it closes the single most valuable silent gap with real numbers (9 languages, 6.00B, 1.108% of a 541.4B pool, 0.328% of a 2028.4B corpus).
2. It supplies a **measured repetition penalty on small sources** (MMLU 28.30 → 26.60, 1 → 4 epoch cap, 8B/300B) — the instrument our spec lacks for tier C — and it points **against** us, which is worth more than a supporting citation: pre-empting it protects §2 and sharpens H3.
3. It supplies **three independent corroborations** of things we assert on thinner evidence: the floor argument (DoReMi ×2), the fine-grained per-lane scoring rule (+1.07 vs +0.38), and the portable classifier substitute (Figure 12).
4. It **challenges two live numbers** — the 64.44%-Low framing and MMLU-at-1B in H4/H5 — that a reviewer who has read the NVIDIA line of work would find on their own.

**What NOT to take from it, stated so the spec does not overreach:** the multilingual method preference (+0.13 / +0.25, inside the paper's own noise floor); any DSIR number; any anneal, curriculum, ordering, long-context or agentic claim; and **the epoch result as a clean repetition penalty** — it is confounded with a move toward uniform, and the authors disclaim transfer to synthetic data.

---

## 11. Draft inserts, in the spec's voice, with scale caveats attached

**§2, after the tier-C paragraph:**
> External corroboration for tier C's scarcity, and a warning about its repeat factor. NVIDIA's own >2T build (Parmar et al., EMNLP 2024 main, pp. 10671–10695; arXiv 2407.06380) assembled its parallel corpus from CC-Matrix, CC-Aligned and ParaCrawl and reached **56B across 32 languages with Hindi the only Indic member at 1.17% = 0.655B — and no Bengali, Tamil, Telugu, Marathi, Malayalam, Kannada, Nepali or Urdu at all** (Table 13). Our 5.0B is 7.6× that, which confirms translated Indic is genuinely supply-limited and confirms the 5.0B rests entirely on AI4Bharat corpora rather than anything a generic pipeline reaches. The same paper cuts against us on the repeat: at 8B/300B, raising a UniMax epoch cap from 1 to 4 on sources of 1.5–18.7B moved **MMLU 28.30 → 26.60 and LM-Eval 67.14 → 66.61** (Table 6), and the winning arm served every source at **exactly 1.00 epoch**. Tier C at 5.0B is in that size band, so the "5.06× is inside Two-Phase's 6-epoch ceiling" defence does not hold — that ceiling was measured on a ~400B crawl pool at fixed share. Two caveats: their epoch cap also flattens the distribution toward uniform (plateau 7.25% → 5.55% against a 5.00% uniform), so repetition is confounded with shape and the authors offer both explanations; and their pool exceeded their budget 4.06×, so their finding is "do not repeat when you need not", not a price for a forced repeat. H3 is the test.

**§2, hazard 2, replacing the last sentence:**
> The portable substitute is an n-gram model, not a transformer classifier. Parmar et al. Figure 12 shows their 3-class quality classifier and a **KenLM perplexity** filter agreeing monotonically on English CC — the Low share rises **6.1% → 73.4%** across perplexity (0,100] → (900,1000] while the High share falls **1.92% → 0**. A KenLM is cheap to train per language on a verified Indic seed and is script-agnostic, so tier B is gated on a per-language KenLM threshold calibrated against tier A, with the DeBERTa classifier used only once validated. The agreement itself is English-only and no correlation coefficient is published for that pair; note also that several of their document heuristics are flagged **English Only** (Table 15), so the heuristic half does not transfer for free either.

**§1, Filters, scoping the quality claim:**
> Scope note on the 64.44%. That figure is `two-phase` Table 16 under the **Nemotron-CC 5-bucket** classifier on its snapshot set, not a property of Common Crawl. The same lab's 3-class classifier over **90+ snapshots** reports **18.2% Low / 81.3% Medium / 0.5% High** (Parmar et al., Figure 10). The policy survives — both papers find quality gating helps — but the **High side is supply-capped**: 0.5% of documents corpus-wide, at most **3.21%** in any of 27 domains and **1.82%** in any of 11 speech types, and 0.00% in six domains. So "upsample High" is bounded by availability, and the load-bearing half of the filter is zeroing Low.

**§7, extending the readability concession:**
> The MMLU thresholds have the same problem H2 has. NVIDIA reports MMLU **only** at 8B/300B, "*when the experimental setting allows for a non-random score*", and omits it from every 2B/165B and 2B/300B ablation (Parmar et al., §2.2–2.3). H4's core average and H5's forgetting check therefore name a metric at 1B that its own practitioners judged unreadable at 2B. Both escalate: the 1B arm decides on the six-task LM-Eval mean (LAMBADA, ARC-easy, Race-H, PIQA, Winogrande, HellaSwag), which that paper treats as readable at 2B, and MMLU is only read at the 3B arm or above. For H3 and H5 the Indic metric adds **XCOPA and TyDiQA-GoldP**, which separated mixtures at 8B/300B by **2.31 points** (Table 7), alongside MILU and IndicGenBench chrF, for which no small-scale sensitivity has been published.

**§5, one clause added to the "Hard constraint" row:**
> …and DoReMi does the same twice more in a different lab's hands: **64.38% of a 300B English budget onto a 14.0B source (13.80 epochs)** and **≈77.6% of a 150B code budget onto markdown (5.74 epochs)**, worst of five English arms, and excluded from the code ablation outright because it "*does not allocate enough tokens to facilitate model learning during training for the remaining 42 languages*" (Parmar et al., Figures 6 and 9, §5.2.3).

**§5, a second clause for the floor's magnitude (this one defends the number, not the mechanism):**
> The 5.5% is also where disclosed practice sits, which turns our derivation from arithmetic into convention. Both multilingual builds that publish per-language Indic volumes serve Indic at **exactly 1.00 epoch** — umT5 at 4.14% of 1.163T = 48.2B against a 48.4B pool (UniMax Table 8, 1× column), and NVIDIA's 8B/300B run at 2.00% of its multilingual budget = 6.00B against a 6.00B pool (Parmar et al. Table 12 under UniMax(1e)) — and in both cases because the epoch cap binds, not because the share was chosen. Against our 113.9B real pool the floor ladder is **5.0% = 0.878 · 5.5% = 0.966 · 5.70% = 1.001 · 6.0% = 1.054 epochs**, so 5.5% is the largest half-point step inside one epoch and 5.70% is the boundary already stated above. The honest corollary, put here rather than left for a reviewer: §1's 15.80% is **2.77 epochs** on real Indic, 2.8× either build, and reaches 1.14 only if Sangraha's 162B synthetic counts as supply. Two caveats travel with the comparison: NVIDIA's 2.00% is a multilingual-arm share, since that paper has no combined whole-corpus run (its only whole-corpus Indic figure is a natural 0.328%), and **percentages are not comparable across builds at 1.163T / 300B / 2.08T — epochs on the real pool are the common currency.**

**§6a, softening the concession (optional):**
> One partial precedent does exist for bucketing by a document attribute and reweighting: quality-bucketed sampling beats an un-bucketed baseline by **+1.07 LM-Eval** when the buckets are cut **within each source** (2B/165B; Parmar et al. Table 9), against **+0.38** for corpus-wide buckets — which is why our bands are applied per lane. It is not a difficulty ordering (their attribute is 3-class quality) and not a curriculum (static weights, no ordering over training), so the design bet stands.

---

## 12. Follow-on citations that would move one of the ten numbers

- **Chung et al. 2023, UniMax (arXiv 2304.09151)** — the winning method here, and the only *published, named* algorithm we have for "cap every source at N epochs and spread the rest". Its own paper sweeps N with multilingual evals at mT5 scale. **Highest-value next read**: it could turn our Indic per-language spread and the tier-C repeat cap from arithmetic into a cited rule, and it is the natural formalism for our §5 floor.
- **Su et al. 2024, Nemotron-CC (arXiv 2412.02595)** — the 5-bucket classifier behind the 64.44%. Reading it would settle the 64.44%-vs-18.2% divergence and, critically, tell us whether it was ever validated off English. Already flagged in the `two-phase` brief; the divergence found here makes it more urgent.
- **AI4Bharat Sangraha / IndicCorpV2 papers** — still the only source for our A/B/C/D provenance tiers. This paper proves no generic pipeline reaches those volumes (6.66B vs our 276B), so the tier arithmetic lives or dies on those primaries.
- **Xie et al. 2023b, DSIR (arXiv 2302.03169)** and **Xie et al. 2023a, DoReMi (arXiv 2305.10429)** — lower priority. Every DSIR effect here is inside noise, and DoReMi is now twice-refuted; we would read them only to characterise *why* DoReMi degenerates, which bears on our §5 floor mechanism.
- **Longpre et al. 2023, "A Pretrainer's Guide" (arXiv 2305.13169)** — already being assessed in parallel as `repeat`. It is the direct antecedent for this paper's age/quality/toxicity axes and this paper's Old-to-Recent result (**60.47 vs 58.93**) is a scaled replication of its data-age finding.
- **Chen et al. 2021 HumanEval / Cassano et al. 2023 MultiPL-E** — only if we want per-language code-eval sensitivity for the Lua-style low-resource trade.
