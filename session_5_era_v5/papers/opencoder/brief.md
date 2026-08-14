# OpenCoder: The Open Cookbook for Top-Tier Code Large Language Models
arxiv 2411.04905v3, 20 Mar 2025, cs.CL. Huang, Cheng, Liu, Hao, Song, Xu, Yang, Liu, Zhang, Chai, Yuan, Zhang, Fu, Liu, Zhang, Wang, Qi, Xu, Chu (INF / M-A-P / NJU).
Read via: HTML v3 first (`opencoder_v3.html` + https://ar5iv.labs.arxiv.org/html/2411.04905), PDF only as figure-asset backup. TeX not needed. Every figure inspected from pixels via `inspect_image`.

## Teach this first
OpenCoder is not a new architecture paper. It is a fully open *code* LLM cookbook: 1.5B and 8B models, a reproducible 960B-token corpus called RefineCode, the cleaning pipeline, annealing mix, SFT mix, ablations, and intermediate checkpoints. The authors' claim is that the missing ingredient in open code models is not another architecture tweak but (1) code-specific cleaning and file-level dedup, (2) recalling *code-related text* from the web, and (3) a small amount of high-quality synthetic data in the anneal and SFT, not the main pretrain. That is the V5-relevant claim: quality and *when* you spend the good data matter more than raw code share.

RefineCode is ~90% raw code (GitHub to Nov 2023 + Stack v2 non-GitHub + Jupyter) and ~8% code-related web (FastText-recalled Common Crawl / FineWeb / SkyPile / AutoMathText + GitHub text files). They keep 607 languages, then *downsample* Java 449GB→200GB and HTML 474GB→64GB because volume ≠ signal. After sampling they have ~730B pretrain tokens; the published corpus is 960B including the web recall. A 1.5B trained on RefineCode vs The Stack v2 hits the same MBPP Pass@1 ~3× faster (Fig. 1 middle). V5 takeaway: do not treat "more GitHub" as a free lunch; HTML/Java dumps and hex/short files waste the code lane.

Dedup is the first-class design choice. GitHub is ~75% exact-duplicate files. They SHA256-exact-dedup first (keep highest stars + newest commit), then 5-gram / 2048-MinHash / LSH (16 bands × 128 rows) fuzzy dedup, which drops another 6% of files. On 485M Python files, *file-level* keeps 32.74B tokens (2.4%); *repo-level* keeps 99.47B (7.5%) — 3× more tokens — and still leaves 52B character-identical files inside repos. Training two 1.5B models, file-level wins HumanEval and MBPP at every matched budget and peaks around 34B tokens at levels repo-level never reaches at 100B (Fig. 8). Chunk-level (pack to 4096 then MinHash) after file-level removes only 0.04B and does not help. V5 takeaway: "repo packing" is not a substitute for file-level exact+fuzzy dedup; keeping near-duplicate files inside a repo is wasted repeat, not long-context signal.

They do **not** pack repositories as training examples. Appendix A says pretrain data is *randomly concatenated and cut into context-length chunks* (4096, later 8192 for the 8B), then full attention inside the chunk. Context is 4k (1.5B) / 8k (8B), with the 8B's first 130k steps still at 4k. There is no 32k/128k phase and no repo-level completion objective. V5's 6% long-ctx slot and any "pack whole repos" story are unsupported here; the paper that actually ships a strong open 8B code model wins HumanEval/MBPP with file-level self-contained code and 4–8k packing.

Anneal is a real, reserved, high-quality phase, MiniCPM-style WSD: after 2.0T (1.5B, 4 epochs) or 2.5T (8B, 3.5 epochs) they decay LR 3e-4 → 1e-5 over **100B extra tokens**. Table 3 mix: RefineCode 83.94B (they say 84% "original distribution" to avoid catastrophic forgetting), Algorithmic Corpus 12.44B (keyword sample: `leetcode` / `def solution` / `class solution`), verified synthetic snippets 2.71B, code textbooks 0.91B. Ablating the HQ slice (algo + synth) collapses the 1.5B anneal curve: HumanEval stays ~0.32–0.35 instead of climbing to ~0.47; MBPP plateaus ~0.42 instead of ~0.52 (Fig. 9). V5 takeaway: hold a real anneal reserve; put algorithmic / verified / textbook code there, not only more web; keep most of the mix on the original distribution so the model does not forget.

Stars are a bad filter. Training 1.5B on `stars>=5` vs original: filtered data has *lower training loss* (easier / less diverse) but *worse* HumanEval (~0.12 vs ~0.18 at 100B) and MBPP (~0.14 vs ~0.20) (Figs. 10–11). Diversity beats "looks famous." V5 should not use GitHub stars, or any single popularity proxy, as a quality gate on Indic / agentic / low-resource lanes.

SFT is two-stage and mostly synthetic. Stage 1 (~4.0M): RealUser 0.7M + Diverse-Instruct 2.3M + filtered Infinity-Instruct 1.0M, one epoch, bs 4096, LR 2e-5. Stage 2 (~367k): McEval-Instruct 36k + Evol 111k + Educational 110k + Package 110k, three epochs, bs 512, LR 5e-5. Mixing the two stages and shuffling them *loses* (Table 10: HE 55.5 vs 70.1 for staged 1.5B). Package-Instruct exists specifically because pretrain code is stale on NumPy/pandas/TF APIs — tool-use SFT, not agent trajectories. Decontam: drop HumanEval/MBPP entry points + 10-gram overlap. V5 should not dump all SFT into one shuffle; reserve a small high-quality code-SFT tail.

## Method, in order
1. **Collect raw code.** GitHub to Nov 2023 + Stack v2 non-GitHub + Jupyter. Drop files >8 MB. Keep 607 linguist languages.
2. **Exact dedup.** SHA256; among identical files keep highest stars + newest commit. ~75% of files are exact dupes.
3. **Fuzzy dedup.** 5-gram, 2048 MinHash, LSH 16×128. Drop 6% more files. File-level, not repo-level.
4. **Transform, do not drop.** Strip leading copyright comments (~15% of files). Regex-replace PII with `<name>` / `<password>`.
5. **Heuristic filter.** Three families: natural-language (size, lines), general-code (variables, function length), language-specific for Python/C/C++/C#/Java/JS/Go/HTML (~130 rules). Principle: remove hex / too-short / no-logic files without shifting the global distribution. Inspired by Phi-1 / Gunasekar et al. 2023 and StarCoder/RedPajama rules.
6. **Sample.** Java 449→200 GB, HTML 474→64 GB. ~730B tokens enter the main pretrain mix.
7. **Recall code-related web.** Seed 500k AutoDS-annotated CC pages → FastText (BPE, so Chinese tokenizes) → recall CC → domains with >10% code pages → manual URL annotation (e.g. `stackoverflow.com/questions` keep, `/jobs` drop) → re-seed. Three iterations → ~220 GB from CC. Same pipeline on FineWeb, SkyPile, AutoMathText → 330 GB total web. Separate classifier on GitHub text files → +178 GB. Published RefineCode web slice is 74B tokens (~8%).
8. **Anneal 100B.** 84% original RefineCode + 12.44B algo keyword sample + 2.71B LLM-synthesized self-contained functions *that pass their own tests* (multi-language, Phi-1 CodeExercises style) + 0.91B Qwen2-72B textbooks over hqcode (GPT-4o-mini tasks).
9. **Pretrain.** WSD: 8B-token / 2k-step warmup, peak LR 3e-4, constant, then exponential decay to 1e-5 over the 100B anneal. 1.5B: 2T / 4 epochs, micro-bs 4, global 1024, 256×H800, 28,034 GPU-h. 8B: Llama-3.1-8B-like, vocab 96640 (inf-llm tokenizer), 2.5T / 3.5 epochs + 100B decay; first 130k steps seq 4096 / gbs 2048, then seq 8192 / gbs 1024 / TP 2; 512×H100, 96,000 GPU-h. Packing = random concat + cut to context.
10. **Two-stage SFT.** Stage 1 diverse / user / Infinity; Stage 2 small HQ code (McEval, Evol, educational-with-tests, package-from-PyDoc). Decontaminate HE/MBPP. No RLHF / DPO reported.

## Assumptions
- **Code-specialist mix (~90% code + ~8% code-web) transfers to a general V5 mix.** Hides that 24% code in a 7-lane model is a different optimization problem; they never sweep code vs web vs STEM shares.
- **HumanEval / MBPP / MultiPL-E are the right north stars.** Hides repo-level, agentic, long-ctx, and Indic. File-level self-contained functions are *selected for* by these benches.
- **File-level > repo-level generalizes past Python 1.5B.** Ablations are 1.5B on Python only. A 1–10T multilingual run that needs cross-file APIs might want *some* repo signal — they did not test that.
- **Random 4k/8k concat is enough context.** Hides V5 long-ctx (needle, 32k–128k, agent traces). They never measure long-context.
- **84% original-distribution anneal is required.** They say the 84/16 split "might not be ideal" given compute. Hides the true HQ reserve size.
- **Synthetic anneal/SFT is safe if unit-tested.** Snippets are kept only if tests pass; textbooks are not executed. Collapse / bias from teacher (Qwen2-72B, "strong LLM") is unmeasured. Silent on Indic teachers.
- **Chinese web recall ≈ a recipe for Indic.** They manually tag Chinese code/math domains because Chinese CC is scarce. Indic is scarcer and not studied.
- **Stars-as-tiebreak is OK even though stars-as-filter is bad.** Exact/fuzzy dedup still prefers the highest-star copy. That can still skew toward popular English GitHub.
- **SFT package docs fix tool use.** This is API-freshness SFT, not agent trajectories. Will not fund an agentic lane.

## Numbers we can cite
- RefineCode size · 960B tokens, 607 langs, ~130 rules, ~75B web tokens · published corpus · Table 2, Table 15, §2.1.
- RefineCode mix · GitHub 755B (78.4%) + Jupyter 11B (1.1%) + Stack v2 120B (12.5%) + CC 13B (1.4%) + SkyPile 3B (0.3%) + FineWeb 55B (5.7%) + AutoMathText 3B (0.3%) · Table 2.
- Pretrain tokens after sampling · ~730B · Java 449→200 GB, HTML 474→64 GB · §2.1.1 Data Sampling.
- Exact-dupe rate · ~75% of GitHub files · §2.1.1 Deduplication.
- Fuzzy drop · 6% file volume · 5-gram, 2048 MinHash, LSH 16×128 · §2.1.1.
- File vs repo Python · file 32.74B (2.4% of 485,817,123 files, 30.5M kept) vs repo 99.47B (7.5% of 11.0M repos, 7.48M kept) · 1.5B train · Table 9 §6.1.
- Repo still contains 52B char-identical tokens; file-after-repo would drop another 68B (68.4%) · §6.1.
- Chunk after file · 32.74B → 32.70B (−0.04B); chunk-only keeps 324.70B (worse than repo) · Table 13 appendix.
- RefineCode vs Stack v2 efficiency · 1.5B, MBPP Pass@1, 0–600B · RefineCode ~3× fewer tokens to ~25% and ends ~34 vs ~28 · Fig. 1 middle (pixel; no printed y).
- OpenCoder-8B-Base HumanEval · 66.5 zero-shot Pass@1 · 8B, 2.5T+100B · Table 6 / Fig. 1 right.
- OpenCoder-8B-Base other · HE+ 63.4, MBPP 79.9, MBPP+ 70.4, MBPP 3-shot 60.6, BigCodeBench full 40.5 / hard 9.5 · Table 6.
- OpenCoder-1.5B-Base · HE 54.3, HE+ 49.4, MBPP 70.6, MBPP+ 58.7 · 1.5B, 2T+100B, no web-recall in this size · Table 6.
- OpenCoder-8B-Instruct · HE 83.5, HE+ 78.7, MBPP 79.1, MBPP+ 69.0, BigCodeBench 40.3 / 16.9, LiveCodeBench 23.2 (2305–2409) · Table 7. Chat HE 83.5 is also Table 1.
- MultiPL-E 8B-Instruct avg 71.0 (Py 83.5, Java 72.2, C++ 61.5, C# 75.9, TS 78.0, JS 79.5, PHP 73.3, Bash 44.3) · Table 8. Qwen2.5-Coder-7B-Instruct is higher (avg 76.5, HE 88.4).
- Anneal mix · 83.94 + 12.44 + 2.71 + 0.91 = 100B; 84% original by design · Table 3 §2.2.
- Synthetic share of anneal · 3.62B / 100B = 3.62% · Table 3.
- Repeat factor · 8B sees 2.5T from ~730–960B unique ≈ 2.6–3.5 epochs; paper says 3.5 epochs on 2.5T · §3.2.
- SFT counts · Stage1 0.7+2.3+1.0 = 4.0M; Stage2 36+111+110+110 = 367k · Table 5. Fig. 1 left prints "4.5M high-quality examples".
- Two-stage vs mix, 1.5B-Instruct · Stage1+2 HE 70.1 / HE+ 64.0 / MBPP 74.6 / MBPP+ 64.8 / BigCodeBench 31.5 / Code Arena 6.9 vs Mix 55.5 / 51.2 / 52.0 / 58.7 / 23.9 / 3.8 vs Stage1-only 52.4 / 48.1 / 68.7 / 57.4 / 22.1 / 5.3 · Table 10 §6.4.
- Stars filter · `stars>=5` vs original, 1.5B, 100B tokens · original wins HE and MBPP; filtered has lower CE loss · Figs. 10–11, §6.3.
- Context · 1.5B 4096 RoPE θ=10k; 8B 8192 RoPE θ=500k; first 130k 8B steps at 4096 · Table 4, §3.2.
- LR / batch · peak 3e-4, anneal to 1e-5; warmup 8B / 2k steps; 8B global bs 1024 (2048 in the 4k phase) · §3.2.
- SFT LR · stage1 2e-5 / 1 epoch / bs 4096; stage2 5e-5 / 3 epochs / bs 512; cosine, 100 warmup · §4.3.
- Compute · 1.5B 28,034 H800-h; 8B 96,000 H100-h · §3.2.
- Copyright / PII · >15% files have leading copyright; PII replaced · §2.1.1 Transformation.
- Web recall loop · 500k seeds, 3 iterations, domain if >10% pages code-like · §2.1.2.
- McEval · ~2,000 multilingual gen samples, 40 langs; MdEval ~1.2k repair samples, 18 langs · §5.2. Pixel averages: McEval OpenCoder-8B-Inst ~50 vs Qwen2.5-Coder-7B-Inst ~60; MdEval ~40 vs ~63 (Figs. 6–7, no printed numbers).

## Figures
- **Fig. 1** (`opencoder_figure1_v4.png` / `papers/opencoder/opencoder_figure1_v4.png`). Three-panel teaser. Left infographic: "130 rules for filtering code files", "75B code related web tokens", "4.5M high-quality examples". Middle: line chart, y = MBPP Pass@1 (%) for 1.5B (0–35), x = Training Tokens (Billion) 0–600; green RefineCode vs gray Stack v2; "3× faster" arrow at ~25% from ~165B to ~400B; no error bars; RefineCode ends ~34, Stack v2 ~28 (pixel). Right: scatter HumanEval zero-shot Pass@1 of 6B+ *base* models vs time (2023-05 / 2024-02 / 2024-11); green dashed "fully open" frontier; OpenCoder-8B **66.5** (green, bold) above Qwen2.5-Coder-7B 61.6. Takeaway: cleaner data is more token-efficient; 8B base HE 66.5 is the fully-open frontier they advertise.
- **Fig. 2** (`opencoder_pretrain.png`). Two dashed pipelines, no numbers. (a) Raw code: Preprocessing → Deduplication → Transformation → Filtering → Data Sampling → Code Corpus. (b) Web: Code Seed (Positive / Negative) → FastText training → Classifier → Recall From Common Crawl → Web Corpus → Code-related Domain Discovery → Url Annotation (SO `/questions` keep, `/jobs` drop) looping back to seed. Takeaway: web recall is an iterative classifier+human-URL loop, not a one-shot filter.
- **Fig. 3** (`compare_refinecode_stack_v2.png`). Side-by-side PCA (no axis labels/ticks) of CodeBERT embeddings. Left Python, right C++. Green = RefineCode, blue = Stack v2. Dashed ellipses mark blue-only outliers: "Low Quality: Too Short Code" / "Pure Hex data" vs "High Quality: Educational Code" in the dense core. Takeaway: RefineCode is Stack v2 with the short/hex tail cut off.
- **Fig. 4** (`figures/opencoder_program_distribution_v2.png`). Grouped log bar chart, title "Programming Language Distribution (Sorted by File Size)". Left y Total File Size (GB), right y Number of Files. Green = GB, gray = file count. Top: HTML, Java, C#, PHP, JavaScript, Python, Cpp, C, Markdown, TypeScript, … Pascal. No printed values; HTML/Java dominate GB; HTML has fewer files than Java (large files). Before sampling (caption). Takeaway: head is web/enterprise langs; they later cut HTML/Java for that reason.
- **Fig. 5** (`sft_fig.png`). Three color-coded SFT synth pipelines, no counts. (a) green Diverse: Filtered Web Corpus → Task-specific Prompt Engineering → Diverse Instruction → Answer Generation → Large-scale Diverse-Instruct. (b) blue Educational: Seed → LLM Prompt → Test-case Generation → Code Verification → Educational-Instruct (only path with execution). (c) yellow Package: Pretrain Corpus → Package Corpus Retrieval → Reference Library → LLM Prompt → Package-Instruct. Takeaway: three different synth *purposes*; only educational is unit-tested.
- **Fig. 6** (`figures/mceval_bars.png`). 4-panel clustered bars, 40 groups (Average + 39 langs), 6 models. Legend: OpenCoder-8B-Instruct (orange), CodeGemma-7B-It, DS-Coder-V1-6.7B-Instruct, CodeLlama-7B-Instruct, CodeQwen1.5-7B-Chat, Qwen2.5-Coder-7B-Instruct (white). Y ticks only 0 and 50; no error bars, no labels. Pixel Average ~50 OpenCoder vs ~60 Qwen2.5. OpenCoder beats Llama/Gemma almost everywhere; Qwen2.5 is tallest in most langs. Takeaway: 8B-Instruct is multilingual-competitive at 7–8B, not SOTA vs Qwen2.5-Coder.
- **Fig. 7** (`figures/mdeval_bars.png`). 2-panel clustered bars, 19 groups (Average + 18 langs), 5 models: OpenCoder-8B-Instruct (orange), CodeLlama-7B, Yi-Coder-1.5B-Chat, DS-Coder-1.3B-Instruct, Qwen2.5-Coder-7B-Instruct (white). Y ticks 0/50; no error bars. Pixel Average ~40 OpenCoder vs ~63 Qwen; OpenCoder leads the small open set, trails Qwen almost everywhere except F#. Takeaway: debugging/repair is not the paper's win vs Qwen.
- **Fig. 8** (`figures/dedup_comparison.png`). Two line charts, HumanEval-Pass@1 and MBPP-Pass@1 vs tokens 0–100B. Green File-Level vs blue Repo-Level. No error bars. File-level ends ~34B at HE ~0.19 / MBPP ~0.20; repo-level at ~100B is still only HE ~0.17 / MBPP ~0.14. Takeaway: file-level is more token-efficient; repo-level's extra tokens are near-dupes.
- **Fig. 9** (`figures/decay_comparison.png`). Same axes pair, anneal 0–100B. Green With High-Quality Data vs blue Without (no algo/synth). Green HE ~0.33→~0.47, MBPP ~0.48→~0.52; blue HE stuck ~0.32–0.35, MBPP ~0.37–0.42. Gap does not close. No error bars. Takeaway: HQ anneal data is not optional.
- **Fig. 10** (`figures/stars_comparison.png`). Same axes, 0–100B. Green Original Data vs blue Filtered Data (`stars>=5`). Original HE ~0.18 / MBPP ~0.20 at 100B; filtered ~0.12 / ~0.14 and plateaus. No error bars. Takeaway: star filter hurts downstream.
- **Fig. 11** (`loss_vis.png`). Left: Loss vs tokens 0–100B, same two series; filtered (blue) loss ~0.25–0.30 *lower* the whole way (ends ~0.78 vs ~1.05). Right: unlabeled 2D embedding scatter; filtered occupies the core, original has a green halo of outliers. Caption: stars reduce diversity and therefore training loss. Takeaway: lower loss ≠ better model when you deleted the diverse tail.
- **Fig. 12** (`figures/dedup_comparison_2.png`). Same HE/MBPP axes; three series: File-Level green, Repo-Level blue, Repo&Chunk-Level orange. File-level still dominates at ≤35B; repo+chunk beats repo after ~50B but never catches file-level. No error bars. Takeaway: do not replace file-level with chunk-level packing dedup.

## Implementation nits
- Models: 1.5B (24L, d=2240, 14/14 heads, SwiGLU, 4k) and 8B (32L, d=4096, 32 heads / 8 KV, Llama-3.1-8B-like, 8k). Vocab 96,640, inf-llm tokenizer. RoPE θ 10k / 500k.
- WSD (MiniCPM): warmup 8B / 2k steps, constant 3e-4, exp decay to 1e-5 over 100B.
- Packing: random concat → cut to 4096 (or 8192); full attention inside chunk. Not repo-contiguous.
- Dedup knobs: SHA256 exact; MinHash 2048; LSH bands=16, rows=128; 5-grams. Tie-break: max stars, newest commit.
- Filters: ~130 rules; language-specific only for 8 langs. Drop >8 MB. Downsample Java/HTML only.
- Web recall: FastText on BPE tokens; 500k AutoDS seeds; 3 loops; domain threshold 10%; manual URL prefixes (Table 14 Chinese code/math domains).
- Anneal HQ seeds: keyword `leetcode` / `def solution` / `class solution`; synth functions must pass generated tests; textbooks from hqcode + Qwen2-72B-Instruct.
- SFT synth: T=1.0 for diverse questions; educational path uses a seed scorer + interpreter; package path uses PyDoc on current libs.
- Decontam: HE/MBPP entry points + 10-gram overlap.
- Eval: OpenCodeEval (https://github.com/richardodliu/OpenCodeEval); LiveCodeBench split 2305–2409; MultiPL-E via Qwen2.5-Coder eval code.
- Release: https://opencoder-llm.github.io — weights, pipeline, RefineCode, SFT set, intermediate ckpts.
- Failed / not helpful: repo-level dedup; chunk-level dedup; stars>=5 filter; shuffling Stage1+Stage2 SFT.

## Follow-on papers
- MiniCPM (Hu et al. 2024) · WSD + anneal recipe OpenCoder copies · sets the 100B / decay-to-1e-5 template V5 already uses.
- The Stack v2 / StarCoder2 (Lozhkov et al. 2024a) · 900B, 619 langs, ~15 rules, ~30B web · RefineCode is the "same shape, more rules, more web, language-specific filters" delta.
- StarCoder / SantaCoder (Li et al. 2023; Allal et al. 2023) · file-level MinHash and "stars are a bad filter" · OpenCoder's §6.1–6.3 are controlled replications; V5 should not reopen those.
- DeepSeek-Coder (Guo et al. 2024) · claims repo-level dedup · OpenCoder's Table 9 / Fig. 8 is the direct counter-number.
- Phi-1 / CodeExercises (Gunasekar et al. 2023) · verified synthetic functions in anneal · 2.71B is the OpenCoder-scale copy; quality bar = tests pass.
- DeepSeekMath (Shao et al. 2024) + AutoDS (Zhang et al. 2024b) · FastText recall of domain web · template for V5 Indic/STEM web recall, not a token number to copy.
- Qwen2.5-Coder (Hui et al. 2024) · 23.5T, HE-chat 88.4, closed data · ceiling OpenCoder does not beat; do not cite OpenCoder as multilingual SOTA.
- OctoPack (Muennighoff et al. 2024a) · commit-pack instruction data · alternative SFT seed if V5 wants real diffs instead of synth QA.

## Assignment mapping
1. **Budget share per lane (sum 100%).** Challenges / mostly silent. OpenCoder is a code specialist: RefineCode is 90.9% raw code + 7.7% code-web + 0.3% AutoMathText (Table 2), trained as essentially a 100% code(+code-web) run. It does **not** justify V5 main 24/2/6/6/16/12/34. Usable sentence: quality-adjusted code, not a 24% share, is what moved HE from Stack-v2's ~28 to RefineCode's ~34 MBPP at 1.5B/600B (Fig. 1). If V5 keeps 24% code, the paper says spend it on RefineCode-style cleaned file-level data + ~8% of that lane as code-related web, and downsample HTML/Java-like sludge.
2. **Indic split (verified / unverified / translated / synthetic).** Silent. Closest analogue is Chinese: SkyPile 3B + manual Chinese code/math domain list (Table 14) because "scarcity of Chinese data" (§2.1.2). No Hindi/Indic, no verified/unverified split. Do not cite this paper for the 40/25/20/15 Indic slice.
3. **Agentic, reasoning, long-context as first-class slots.** Mixed.
   - *Reasoning:* partial support. Anneal Algorithmic Corpus 12.44B + 2.71B verified snippets; eval on LiveCodeBench 23.2 (8B-Instruct, Table 7). Not a named reasoning *lane*.
   - *Agentic:* silent as a slot. Package-Instruct 110k is API-freshness / tool-call SFT ("undermines the model's ability to use tool calls", §4.1), not trajectories. Abstract name-drops "agent systems" only.
   - *Long-context:* challenges V5 6% long-ctx + repo packing. They pack by *random concat into 4k/8k chunks* (Appendix A) and explicitly prefer *file-level* over repo-level data. No 32k phase, no repo-completion bench. Quote: "During pretraining, data is first randomly concatenated and segmented into chunks of context length" (Appendix A). V5 long-ctx must come from somewhere else.
4. **Protected always-on floor (Indic + agentic + reasoning).** Silent on those three. The nearest mechanism is anneal *distribution lock*: "we ensure that 84% of the annealing data comes from the original distribution of RefineCode" because "a significant distribution shift can lead to catastrophic forgetting" (§2.2). That supports a floor against starving the *main* distribution, not the scarce lanes. Also: do not star-filter scarce lanes (Figs. 10–11).
5. **Anneal reserve.** Supports, strongly. 100B reserved HQ decay after 2.0–2.5T (~4% of tokens); mix Table 3; ablating HQ (algo+synth) drops HE/MBPP and the gap does not close (Fig. 9, §6.2). They also say 84/16 "might not be ideal." V5 anneal 20/8/18/8/28/10/8 can cite this for *holding HQ code + verified synth for cooldown*, and for keeping a large original-distribution ballast. Code textbooks + unit-tested snippets are the concrete "best data" to hold back.
6. **Lane tied to benches.** Supports for the *code* lane only. They fund HumanEval / HE+, MBPP / MBPP+, BigCodeBench (complete + instruct), LiveCodeBench, MultiPL-E, McEval (40-lang gen), MdEval (18-lang repair), Code Arena (Table 10). No Indic, no long-ctx, no agent-bench. A V5 24% code share should be graded on this set, not on MMLU.
7. **Demand vs unique supply; repeat vs synthesize.** Supports. Unique RefineCode 960B (730B after sample) vs 2.5T seen = **3.5 epochs of repeat** on the 8B (§3.2); 1.5B is 4 epochs on 2T. File-level Python unique is only 32.74B — a 2T code demand on Python-like data is ~60× repeat if you do not add other langs/web. They synthesize **little** in pretrain (3.62B anneal = 3.6% of anneal, ~0.14% of 2.5T) and **a lot** in SFT (most of 4.5M). Quote: file-level "retained tokens" 32.74B (2.4%) vs repo 99.47B (Table 9). V5 code 1.1T unique vs 24% of 2T = 480B demand is *under* unique if the 1.1T is real; the paper's lesson is still "repeat cleaned unique 2–4×, synthesize only a few percent at anneal, synthesize the SFT tail." Agentic 40B vs 0.63B unique is outside this paper.

## What not to overclaim
- OpenCoder does not bless 24% code or 6% long-ctx. It is a ~100% code, 4–8k, file-level model. Using it to raise the code share or to justify repo packing is a category error.
- 8B-Instruct HE 83.5 is *not* SOTA even in-table: Qwen2.5-Coder-7B-Instruct is 88.4 HE and 76.5 MultiPL-E avg, trained on 23.5T closed data (Tables 1, 7, 8). Cite OpenCoder for the *open pipeline*, not the ceiling.
- File-level > repo-level is a 1.5B Python HumanEval/MBPP result with no error bars. It is not a proof that V5 should never train on concatenated repositories or long agent traces.
