# Nemotron-CLIMB: CLustering-based Iterative Data Mixture Bootstrapping for Language Model Pre-training
arxiv:2504.13161v2 [cs.CL] 30 Nov 2025 · NeurIPS 2025 Datasets and Benchmarks · Diao, Yang, Fu, Dong, Su, Kliegl, Chen, Belcak, Suhara, Yin, Patwary, Lin, Kautz, Molchanov (NVIDIA / Georgia Tech)
Read via: **HTML v2** (`https://arxiv.org/html/2504.13161v2` + local `html_v2.html`) for structure/abstract/method; **PDF** (`climb.pdf` → pdftotext) for every table, appendix number, and caption; **inspect_image** on all 9 figures (not OCR). TeX source not needed.

## Teach this first

Web crawls do not come with domain labels. “The Pile-style” labeled mixes are expensive to make and still do not tell you *how much* of each domain to feed a model. CLIMB’s claim is that you can invent the domains yourself by embedding and clustering the raw corpus, then *search* the mixture weights with a cheap proxy model plus a predictor, instead of guessing percentages. That is the whole paper. For V5 it is a method for setting the seven lane shares, not a source of those shares.

They first train a phase-1 foundation (62M / 350M / 1B) on 10T tokens of DCLM + TxT360 with a warmup-stable-decay schedule, then do the interesting work in the decay / continuous-pretrain stage. Mixture search itself uses 62M or 350M proxies; the mixture they find is then used to continue-train the target on 40B tokens (main tables) or 400B tokens (SOTA comparison). For V5 this is exactly the “phase-1 general, then mid-train / anneal on a searched mix” story, not a from-scratch 2T recipe.

Clustering is hierarchical and quality-gated. Stella embeddings → k-means with K_init = 1000 → FastText quality scores (Nemotron-340B labels on 1M docs, four 0–5 axes) prune to 240 clusters at threshold 3.0 → merge by centroid distance 1.5 into ~21 super-clusters (~800B tokens from Nemotron-CC HQ + SmolLM-corpus). ClimbLab later redoes this on the combined corpora into 20 clusters / 1.2T. For V5: do not treat “web” as one lane internally; cluster it, then assign cluster mass to code / STEM / reasoning / general. Indic will not appear as a cluster unless Indic text is in the embedding space.

The search is iterative, not one-shot. Iteration 1 trains 64 random Dirichlet mixtures on the proxy. A LightGBM predictor then ranks the rest of the simplex; later iterations sample 32 then 16 configs only from the predicted top-N, train those proxies, and refit the predictor. RegMix is explicitly “CLIMB with K = 1.” Figure 3’s t-SNE and Figure 5’s MMLU curves are the visual proof that iteration 2–3 still move the needle. For V5: a single RegMix/DoReMi pass is not enough; budget 3 iterations at roughly 4:2:1 search count.

The mixture that wins is sparse, target-dependent, and *not* “only in-domain.” Continuous-pretrain general-reasoning puts most mass on C19/C18/C8/C9 (history-economy + science + earth-science). STEM wants C7+C8 (~97%). Social sciences wants C11 (~61%). Similarity-to-benchmark is useful but not sufficient: C8 is less similar to MMLU-STEM than C7, yet gets 61% weight. For V5 this both supports a protected complementary floor (do not starve useful out-of-domain clusters) and challenges a rigid 8% floor on every named lane if the search would have set it to zero.

ClimbMix (400B, from-scratch) is a different animal from the 40B continuous mix. From scratch they need a more balanced 20-cluster distribution (C12 ~28%, C6 ~20%, C7 ~16% at iter 3). Continuous pretrain can concentrate because phase-1 already taught general language. For V5: the main 2T preset should look more like ClimbMix (spread); the anneal reserve should look more like the continuous-pretrain mix (concentrate on the lanes you still need to win).

They do not study Indic, agentic trajectories, long context, or synthetic:real ratios. Code exists as cluster C20 (“Python, Code”) and is driven to ~0 in the general-reasoning mix. There are no error bars (checklist Q7 = No). Scale is 1B / 400B, not 1–10T. Use the *method* and the continuous-vs-from-scratch contrast; do not copy their percentages into the V5 README.

## Method, in order

1. **Phase-1 foundation.** Train 62M / 350M / 1B decoder-only Transformers with next-token CE on 10T tokens (DCLM + TxT360), WSD schedule (MiniCPM-style), so later runs can resume in the stable stage and spend the decay stage on mixture research.
2. **Embed.** Map every document with `stella_en_400M_v5` (NovaSearch).
3. **Cluster fine.** FAISS k-means, K_init = 1000.
4. **Score and prune.** Train FastText classifiers on 1M Nemotron-340B annotations for quality, educational value, informational value, advertisement (0–5). Drop clusters whose mean score < 3.0 → K_pruned = 240.
5. **Merge.** Group remaining centroids at Euclidean distance 1.5 → K_enhanced ≈ 21 (main experiments, ~800B tokens) or 20 (ClimbLab, 1.2T).
6. **Pose mixture search as bi-level opt (Eq. 1–2).** Find α on the simplex (α_i ≥ 0, Σ α_i = 1) that maximises downstream score of a model trained under α. Approximate the inner train with a LightGBM predictor f_θ(α) fit on (mixture, proxy-score) pairs under a compute budget C.
7. **Iterate (Eq. 3–4), K = 3.**
   - Iter 1: sample 64 mixtures from a Dirichlet whose concentration follows cluster token counts; train 350M (main) or 62M proxies; fit predictor.
   - Iter k+1: rank unused α by f_θ; sample M new configs from Top_N; train those proxies; refit on all pairs so far.
   - Default compute split 4:2:1 = 64:32:16 = 112 proxy runs (100%). Ablations also try 150% / 200% and 6:1 or 2:2:1:1.
8. **Select.** Take the α* predicted best by the final LightGBM. Train the *target* on that mix for 40B (tables 1, 3, 6) or 400B (table 2, fig. 1).
9. **Objective.** Main: 0-shot accuracy on PIQA / ARC-E / HellaSwag *validation*; report test on those plus ARC-C, WinoGrande, SIQA (and wiki/lambda PPL). Domain runs: MMLU STEM / humanities / social-sciences val. MMLU test is 5-shot; everything else 0-shot via lm-eval-harness.
10. **ClimbLab / ClimbMix (from scratch).** Re-cluster Nemotron-CC + SmolLM-corpus into 20 clusters / 1.2T (ClimbLab). Re-run CLIMB-search. Pack the winning weights into a 400B extract (ClimbMix). Train a 1B *from scratch* (not continuous) and compare token-matched curves against ClimbLab-Random, Nemotron-CC-HQ, SmolLM, DCLM-baseline, FineWeb-Edu.

## Assumptions

- **English embedding space (`stella_en_400M_v5`) → clusters are English topical blobs.** Hides Indic: Hindi/Tamil/etc. will either collapse into one “non-English” cluster or be dropped by the quality FastText (trained on Nemotron-340B English-centric labels). You cannot search an Indic lane you never clustered.
- **Downstream score of a 62M–350M proxy, trained a short way, ranks mixtures for a 1B target.** Table 3 says 62M → 350M proxy only moves the 1B avg from 60.11 → 60.41. That is a small, English-reasoning-only transfer. Agentic / long-context / Indic proxies will not transfer the same way.
- **The calibration tasks (PIQA, ARC-E, HellaSwag, or one MMLU slice) are the thing you want.** Optimising social-sciences raises that slice ~5 pp and will *starve* code (C20 → 0) and possibly long-context prose. V5 has seven first-class lanes; a single-head predictor will sacrifice the ones not in the loss.
- **Sparse Dirichlet sampling is desirable.** They “intentionally bias towards sparse weights.” That makes heatmaps readable and amplifies a few clusters. It is a bad prior if V5 needs a protected 2% agentic / 12% Indic floor that search would otherwise set to 0.
- **Phase-1 10T already happened.** Continuous-pretrain mixtures can be peaky because general language is already in the weights. Copying those peaky weights into a from-scratch 2T run is the mistake they themselves warn about in §6.
- **Quality classifier (threshold 3.0) is domain-neutral.** Educational / informational FastText will over-keep STEM textbooks and over-drop conversational, code-comment, or Indic web text. That silently writes the lane shares before search even starts.
- **No repeats, no synthetic.** Every token is a unique web/curated document. Silent on the V5 fact that agentic unique supply is 0.63B against a 40B demand.
- **One run, no error bars.** Checklist Q7 is explicitly No. Sub-1 pp gaps (iterative CLIMB vs Best@N, 4:2:1 vs 2:2:1:1) are not shown to be significant.

## Numbers we can cite

- 1B CLIMB continuous 400B beats Llama-3.2-1B by **2.0 pp** avg (53.54 vs 51.56) on 12 reasoning tasks · 950M, 400B tokens, searched mix · Table 2 / abstract / §4.2.
- Domain specialist, Social Sciences: **+5 pp** over random (abstract); 1B CLIMB-iter3 = **41.79%** vs Best@N **40.66%** (+1.13) and vs Random **36.69%** · 40B continuous, 350M proxy, MMLU-SS · §5 / Fig. 5 / Table 5.
- 350M target, 40B continuous: CLIMB avg **54.83** vs RegMix **53.78** vs DoReMi **53.38** vs Random **52.17** vs Base **50.11** · 350M proxy · Table 1.
- 1B target, 40B continuous: CLIMB avg **60.41** vs RegMix **59.37** vs DoReMi **59.16** vs Random **57.93** vs Base **56.46** · 350M proxy · Table 1.
- ClimbMix 1B from scratch, 12-task avg: **46.36 / 48.28 / 50.67 / 51.35 / 51.97 / 52.43** at 32 / 80 / 160 / 240 / 320 / 400B tokens · Fig. 1 (numbers printed on the ClimbMix curve). Rank order stable: ClimbMix > ClimbLab-Random > Nemotron-CC-HQ > SmolLM > DCLM-baseline > FineWeb-Edu. No error bars.
- Search schedule: **64 + 32 + 16 = 112** proxy trainings (100%); 150% / 200% → 1B avg **60.72 / 61.12** · Table 3 Abl.comp.
- Compute split: **4:2:1 = 60.41** beats 6:1 = 60.05 and 2:2:1:1 = 60.14 · Table 3 Abl.allo / §5.
- Proxy size: 62M / 132M / 350M → 1B avg **60.11 / 60.19 / 60.41** · Table 3 Abl.proxy. 62M proxy still beats Random and matches/beats Best@N at 1B (Table 6: 60.11 vs Best@N 58.96 vs Random 57.93).
- Cluster granularity: K_init–K_enhanced 1000–15 is best in the sweep (**60.59**); 48–21 worst (**59.90**); 1000–21 default **60.41**; 2000–21 **60.24** · Table 3 Abl.clus.
- Init: Dirichlet **60.41** vs random **60.21** · Table 3 Abl.init.
- Predictor: LightGBM Spearman **0.94** on held-out 350M proxy pairs · Fig. 9 / §D.10.
- Clustering funnel: K_init **1000** → prune @ **3.0** → **240** → merge @ dist **1.5** → **21** super-clusters, **~800B** tokens (main) · §3.1 / §C.2. ClimbLab: **20** clusters, **1.2T**. ClimbMix: **400B**.
- Phase-1: **10T** tokens, three sizes, WSD, AdamW lr **5e-5 → 1e-5**, batch **2M** tokens, **256 H100**. Proxy ~**45 GPU-h**; target ~**6400 GPU-h** · §C.3–C.4.
- Continuous general-reasoning mix (350M proxy, iter 3): C19 **0.43**, C18 **0.22**, C9 **0.18**, C8 **0.13**, C16 **0.03** (sparse; most of 21 clusters = 0) · Fig. 7a / §D.7.
- MMLU-STEM mix iter 3: C8 **0.61** + C7 **0.36** = **0.97** · Fig. 7d / §D.2.
- MMLU-SS mix iter 3: C11 **0.61** · Fig. 7c.
- ClimbMix from-scratch iter 3 (20 clusters): C12 **0.28**, C6 **0.20**, C7 **0.16**, C10 **0.07**, C16 **0.07**, C17 **0.06**; top-3 ≈ **0.64** · Fig. 8.
- 350M MMLU-iter3: STEM **28.67%**, Humanities **29.56%**, SS **39.36%** · §5 (matches Fig. 5 pixel reads).
- 1B MMLU-SS: iter1 **40.18%** → iter3 **41.79%** · §5.
- C20 topic = “Python, Code”; C17 = “Role-Playing, Problem Solving, Mathematics, Algorithms”; C7 = “Physics, Accelerators, Materials…” · Table 4.

## Figures

- **Fig. 1** (`figs/final_data_comparison.png`) — line plot, x = Training Tokens (B) at 32/80/160/240/320/400, y = Average Performance (%) 44–52. Six dashed series: ClimbMix (purple circles, values printed 46.36→52.43), ClimbLab-Random (red squares), Nemotron-CC-HQ (blue triangles), SmolLM (tan diamonds), DCLM-baseline (green hexagons), FineWeb-Edu (orange pentagons). **Claim:** ClimbMix is strictly above every competitor at every budget; token-efficiency is large (ClimbMix hits ~50.7 at 160B; others need ~320–400B). **No error bars.** Y-axis truncated (~43.5+), which magnifies 1–3 pp gaps.
- **Fig. 2** (`figs/climb_concept_v6.png`) — top schematic (Web Data + thin Curated Data → CLIMB tree → Topic A/B/C “Optimized Data Mixture for Improving Task X”) plus bottom scatter: Average Reasoning Score (48–53) vs Model Size B params (0.2–1.2). Green diamonds = CLIMB (~0.35B ≈49, ~0.95B ≈53.5) vs gray circles SmolLM / Qwen2.5 / TinyLlama / AMD-OLMo / Llama-3.2. **Claim:** CLIMB Pareto-dominates the size–quality front; ~0.95B CLIMB beats ~1.2B Llama-3.2. n=2 green points, no error bars, token budget not on the axis.
- **Fig. 3** (`figs/search_tSNE.png`) — t-SNE Dim 1 vs Dim 2, no numeric ticks. Blue / orange / green hulls = Iteration 1 / 2 / 3 sampled configs; matching stars = CLIMB-iter1/2/3 selected mixes. **Claim:** search starts wide (blue amoeba) and contracts to the upper-right; selected stars migrate into the iter-3 clump. Qualitative only (t-SNE is not metric).
- **Fig. 4** (`figs/data-filtering-arc-new-v3.png`) — method cartoon. (a) Embed Texts → Cluster Embeddings → Merge Clusters. (b) Tree of 1st/2nd iteration configs; tables of cluster weights; “Train Proxy LMs” writes Target scores (46.2 then 48.3); “Prune with Predictor” greys a row (Pred 44.7) whose Target cell is empty. (c) “Use the predictor after K iterations…”. **Claim:** predictor pruning saves proxy trainings; iteration 2’s best (48.3) beats iteration 1’s (46.2). Numbers in the tables are illustrative.
- **Fig. 5** (`figs/mmlu_plot.png`) — three panels (a) STEM (y 26–33), (b) Humanities (27–33), (c) Social Sciences (34–42). x = CLIMB-iter1/2/3. Green = 1B, blue = 350M; solid = CLIMB iterations (monotonic up), dotted = Best@N, dashed = Random. **Claim:** iteration helps at both scales in all three MMLU slices; by iter 2–3 CLIMB exceeds Best@N even though Best@N uses a same-size proxy and CLIMB uses a 350M proxy. **No error bars.** Paper quotes 350M iter3 = 28.67 / 29.56 / 39.36 and 1B SS = 41.79.
- **Fig. 6** (`figs/supercluster_similarity_matrix.png`) — 4×21 heatmap, y = {arc-e, mmlu-humanities, mmlu-social-sciences, mmlu-stem}, x = Supercluster_1…21, color = cosine similarity of mean embeddings (0.50–0.82). Darkest cell 0.82 = STEM × Supercluster_7; palest 0.50 = humanities × Supercluster_20. Supercluster_19 and _7 are high across rows; _18 and _20 are low. **Claim:** relevance is selective, not uniform. Paper then shows (D.2) that similarity ≠ optimal weight (STEM: C7 most similar but C8 gets 61%).
- **Fig. 7** (`figs/weight-analysis-combined.png`) — five 3×21 heatmaps (rows = Iteration1–3, cols = C1–C21, cells sum to ~1). (a) 350M → general reasoning (C19 0.59→0.52→0.43, then C8/C9 appear). (b) humanities (C19 0.76→0.44, C11 0.03→0.37). (c) social sciences (C11 0.45→0.61; C19 drops to 0). (d) STEM (C7+C8 → 0.36+0.61). (e) 62M → general reasoning (same C19/C18/C8/C9 skeleton as (a)). **Claim:** mixtures are sparse and task-specific; a 62M proxy recovers the same important clusters.
- **Fig. 8** (`figs/weight-analysis-climbmix.png`) — 3×20 heatmap for ClimbMix from-scratch. Iter3: C12 0.28, C6 0.20, C7 0.16, C10 0.07, C16 0.07, C17 0.06. **Claim:** from-scratch wants a *broader* mix than continuous pretrain (top-3 ≈ 64%, not one cluster at 43% plus three friends). C8 spike at iter2 (0.07) dies at iter3 (0.01).
- **Fig. 9** (`figs/correlation_valid_acc.png`) — scatter True Acc vs Pred Acc, ticks 62–65, crimson fit + pink band, box “Correlation: 0.94”. Dense cloud at (64, 64); a few residuals ~0.5–0.6 pp near Pred≈63. **Claim:** LightGBM ranks mixtures well enough to replace most proxy trainings. Paper names this Spearman.

## Implementation nits

- Embedder: `stella_en_400M_v5` (https://huggingface.co/NovaSearch/stella_en_400M_v5).
- Cluster: FAISS k-means, K_init=1000, prune 240 @ FastText mean≥3.0, merge Euclidean 1.5.
- FastText labels: 1M docs, Nemotron-340B, four scores 0–5 (quality / advertisement / informational / educational); prompt in App. D.11.
- Predictor: LightGBM regressor, L1+L2, max depth 4, min 5 samples/leaf, early stop after 20 stagnant rounds, separate val set.
- Search: 3 iters, 64/32/16, Dirichlet(token-count) init, sample M from predicted Top_N (exploration inside the elite set).
- Proxy: 350M main, 62M cheap path (App. D.9). Target eval at 62M / 350M / 1B (they also write 950M for the 400B CLIMB model in Table 2).
- Train: AdamW, 5e-5 stable → 1e-5 anneal, batch 2M tokens, 256×H100. Proxy ~45 GPU-h, 1B target ~6400 GPU-h.
- Eval: lm-eval-harness; MMLU 5-shot, all else 0-shot. Opt on PIQA+ARC-E+HellaSwag val (or one MMLU domain val).
- Data release: https://huggingface.co/collections/nvidia/climb-datasets-67e428bdb9aaced2acda191f — Nemotron-ClimbLab (1.2T / 20 clusters) and Nemotron-ClimbMix (400B).
- Source corpora: Nemotron-CC highest-quality bucket + SmolLM-corpus.
- Intentionally sparse sampling of α (D.8).
- No released training-from-scratch recipe beyond the two datasets; code claimed released in the NeurIPS checklist.

## Follow-on papers

- **2407.01492 RegMix** · mixture-as-regression, one iteration of (sample, train proxy, fit predictor). · CLIMB says this is K=1; V5 should not stop at one RegMix pass if it can afford 112 cheap proxies.
- **DoReMi (NeurIPS 2023, Xie et al.)** · Group-DRO on *named* domains to set resample weights. · Needs predefined domains; CLIMB’s point is that Common Crawl does not have them. Use DoReMi only *after* clustering, or not at all.
- **2404.06395 MiniCPM** · WSD schedule that lets you resume in stable and spend decay on data experiments. · This is why V5 can hold an anneal reserve and actually spend it at low LR.
- **2406.03476 Blakeney et al. “Does your data spark joy?”** · Domain upsampling in the *last* pretrain phase lifts GSM8K / MMLU / HumanEval. · Direct support for V5 anneal concentrating STEM/code/reason rather than web.
- **2412.02595 Nemotron-CC** · the HQ Common-Crawl bucket CLIMB clusters. · If V5’s web lane is not at least this filtered, ClimbMix-style gains will not transfer.
- **FineWeb-Edu (Penedo et al., NeurIPS D&B 2024)** · educational-value filter; *loses* to ClimbMix at every token budget in Fig. 1. · Edu-score-only web is not a substitute for mixture search.
- **DCLM / DataComp-LM (Li et al., NeurIPS 2024)** · also beaten by ClimbMix in Fig. 1; used as CLIMB’s own 10T phase-1. · Filtering ≠ mixing.
- **2502.10341 WebOrganizer** · classifier topic+format labels on web data. · Alternative to k-means; would change how V5 *defines* lanes, not just their %.
- **2306.11644 Phi / “Textbooks Are All You Need”** · the educational-heuristic baseline CLIMB says is not domain-aware. · Do not use a single edu score as the Indic or agentic filter.
- **OLMo 2 (2025)** · mid-train on HQ web + STEM refs + synthetic math + encyclopedic. · Same “hold best data for the end” idea as V5 anneal; CLIMB would *search* that mid-train mix.

## Assignment mapping

1. **Budget share for every capability lane (code / agentic / reasoning / long-context / Indic / STEM / general web = 100%).** **Challenges** hand-set shares; **supports** searching them. Usable sentence: continuous-pretrain general-reasoning mix is not 34% web — it is C19 43% + C18 22% + C9 18% + C8 13% (Fig. 7a, §D.8), while from-scratch ClimbMix is C12 28% + C6 20% + C7 16% (Fig. 8, §6). **Silent** on Indic and agentic as named lanes. Do not paste 24/2/6/6/16/12/34 as if CLIMB measured it.

2. **Indic split across verified / unverified / translated / synthetic.** **Silent.** Clustering + Nemotron-340B quality labels are English-web. Nothing here defends 40/25/20/15.

3. **Agentic, reasoning, long-context as first-class slots pointed at inventory.** **Supports** reasoning as a first-class optimisation head (PIQA/ARC-E/HellaSwag, plus MMLU slices) and shows the slot must be *pointed at clusters*, not at a vague “web” bucket. **Silent** on agentic trajectories and long-context corpora. Code is a cluster (C20 “Python, Code”, Table 4) that the general-reasoning search sets to 0 — i.e. if you do not put the lane in the predictor’s loss, it dies.

4. **Protected always-on floor OPUS cannot starve (Indic + agentic + reasoning).** **Supports the spirit, challenges the implementation.** D.2: “out-of-domain data are also useful”; C8 starts OOD for general reasoning and *gains* weight (0 → 0.13) across iterations; similarity-only filtering would have dropped it. Also: “using only in-domain data does not necessarily lead to optimal performance.” That is a vote for a complementary floor. **Challenges** a uniform 8% on every scarce lane: their best mixes are intentionally sparse and will zero lanes not in the objective (C20 code = 0 under general reasoning). If V5 wants Indic/agentic always-on, those terms must be *in the predictor target* or hard-constrained; CLIMB will not protect them for free.

5. **Anneal reserve: which best data is held back for cooldown.** **Supports.** They literally hold the searched HQ mix for the decay / continuous stage after 10T WSD phase-1, and they say from-scratch needs balance while continuous can concentrate on “a few important domains” (§6). Blakeney/OLMo-2 citations in §1 are the same mid-train idea. Usable contrast: ClimbMix (from-scratch, broader, Fig. 8) vs 40B/400B continuous (peaky, Fig. 7a). V5 anneal preset 20/8/18/8/28/10/8 is *closer* to their continuous specialist mixes (STEM ≈ C7+C8, SS ≈ C11) than the main 34% web preset is.

6. **Each lane tied to the benchmarks it is meant to win.** **Supports, strongly.** They fit α to PIQA/ARC-E/HellaSwag val and separately to MMLU-STEM / humanities / social-sciences val; Fig. 5 / Fig. 7 show different winners. Table 1 even shows the PIQA-ARC-Hella objective *transfers* to WinoGrande/SIQA/ARC-C. V5 should name the benchmark head per lane the same way (and not optimise only MMLU if it cares about HumanEval / long-ctx / Indic suites).

7. **Demand vs unique token supply; where a share only works by repeating or synthesising.** **Mostly silent.** They never repeat; ClimbLab is 1.2T unique clustered tokens, ClimbMix is a 400B extract, main clustering is ~800B. Fig. 1 is an *equal unique-token* bakeoff, not a repeat/synth study. Weak, transferable observation: after 160B the ClimbMix curve flattens (50.67 → 52.43 by 400B), so extra unique tokens of the *same mix* have diminishing returns — that does **not** license 63× synthetic agentic data. If V5’s agentic unique supply is 0.63B, CLIMB has nothing to say except “don’t pretend a cluster you don’t have.”

## What not to overclaim

- **Do not treat ClimbMix 52.43 or the 2.0 pp Llama-3.2 gap as a 1–10T / multilingual / agentic result.** Setting is English, ≤1B, ≤400B, 12 reasoning tasks, no error bars.
- **Do not copy Fig. 7’s peaky continuous weights into a from-scratch V5 run.** The authors say that concentration is only legal because phase-1 already happened (§6). From-scratch they themselves spread mass (Fig. 8).
- **Do not claim CLIMB discovered that code should be 24% or Indic 16%.** Code cluster C20 is zeroed by a reasoning-only predictor; Indic was never in the corpus they clustered.
