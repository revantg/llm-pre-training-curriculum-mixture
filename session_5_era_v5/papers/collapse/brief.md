# How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model Collapse
arxiv 2404.05090v1 [cs.LG], 07 Apr 2024 (no later version on arXiv). Authors: Seddik, Chen, Hayou, Youssef, Debbah (TII / NYUAD / Simons / Khalifa).
Read via: HTML first (`https://arxiv.org/html/2404.05090v1` + local `paper.html`); PDF for captions/Table 1 and garbled math; inspect_image on every saved figure. TeX not needed.

## Teach this first

Model collapse is what happens if tomorrow’s LLM is trained on yesterday’s LLM output. The tails of the real distribution quietly vanish: rare words, rare constructions, rare languages. After enough generate-train cycles the next-token distribution for a given context becomes a Dirac spike — the model only ever emits one token. The authors call that *total collapse*. V5 will inject synthetic tokens into scarce lanes (agentic ~63× over unique supply; Indic D = 15% of the Indic lane). This paper is the citation that says “how much real must stay in the mix, or the lane forgets itself.”

They study only the *statistical* error: finite samples cannot recover a discrete distribution exactly. They deliberately ignore the *functional* error (the network is not expressive enough). Their theoretical model is a linear Softmax next-token classifier with one-hot context embeddings, so the MLE is just the empirical token counts given that context. Every generation is unbiased: in infinite data it would recover the true p. Collapse is therefore a finite-sample phenomenon, not a bias. For V5 that means even a perfect teacher, if you only train on its finite samples and throw away the real ones, will still collapse.

Two training loops. *Fully synthetic*: generation m trains only on samples from generation m−1. This is a Markov chain on the probability simplex with absorbing states at the vertices. Total collapse is almost sure. Expected time to absorption is at least order n (samples per context) and at most order n²; simulations say closer to O(n). *Partially synthetic*: every generation is trained on a fixed real corpus of size N plus n fresh synthetic samples from the previous model. Then the expected L1 drift away from generation 1 is bounded independently of how many generations you run — provided n is small enough. V5’s “always-on real floor” is exactly this second loop.

The usable bound is equation (11): to keep E‖p^(m) − p^(1)‖₁ < ε you need n ≲ 2π e⁻² min[s−2, log(√2 π N ε / (6 e s))]. In words: synthetic count per context must be *logarithmic* in (real count × tolerance / vocab size). The paper’s own gloss: “the amount of synthetic data should be exponentially smaller compared to real data.” That is the sentence a reviewer will throw at an agentic 40B-from-0.63B unique plan.

They then simulate two more realistic loops. Sampling only from the last K models *delays* collapse (mean absorption time 17 → 95 → 216 as K goes 1 → 5 → 10) but does not stop it. Mixing uniformly over *all* past models plus the original data (their “Randomly Sampled Data”, window = m) plateaus: 100 runs over 500 generations produced only one Dirac. For V5, a web crawl that still contains the original human documents is closer to window = m; a closed agentic pipeline that only keeps the last teacher’s rollouts is closer to K = 1.

A tiny GPT-2 (nanoGPT, char-level Shakespeare, vocab 65) reproduces the same qualitative split. Pure synthetic: L1 from generation 1 climbs ~0.43 → ~0.78 over 9 generations and val loss plateaus rise Gen 1 ~1.45 → Gen 10 ~1.90, with Gen 10 overfitting. 50/50 real/synth: L1 flat, val-loss gap saturates after Gen 3 (~1.46 vs ~1.53–1.57). 20% synth / 80% real: all ten generations sit on top of each other at val loss ~1.45–1.47. So “some real in every generation” is the empirical stop condition, and 80% real is the mix that actually erased generation-to-generation loss drift in their only neural experiment.

What this is *not*: a mixture-search paper, a quality ranking of Phi-style textbooks, or a 1–10T scaling result. The theory is one context at a time, one-hot features, unbiased MLE. The neural run is a 8-layer 256-d character model on a play. Use it to defend a *real-data floor* and to attack *closed self-consuming loops*. Do not use it to pick 24/2/6/6/16/12/34.

## Method, in order

1. Fix vocabulary size s, context length ℓ, at most c ≤ s^ℓ contexts. True next-token law given context j is p_{jk} = P(Y=k | X=j).
2. Represent contexts and tokens as one-hot vectors. Train a linear Softmax by categorical cross-entropy (eq. 1). The minimizer is the empirical frequency of token k in the N samples that share context j (eq. 2). Call this p^(1). Ground truth is p^(0) := p.
3. Recursion (eq. 5): p^(m) is the empirical frequency of a mixture of samples drawn from earlier models. n_t^(m) = how many of generation m’s training tokens came from model t.
4. Fully synthetic: n_t^(m) = n · 1{t = m−1}. Chain on the n-grid of the simplex; vertices {δ_i : p_i > 0} are absorbing, so collapse is a.s.
5. Track three scalars: ‖p^(m)‖_∞ (max token prob), σ_m = ‖p^(m)‖₂² (sum of squares; 1 iff Dirac), S_m = E[σ_m]. Drift metric is L1, which is twice total variation.
6. Theorem 1: closed form S_m = 1 − (1−1/n)^m (1−S_0); sandwich on collapse probability ρ_m; sandwich on expected absorption time T.
7. Proposition 1: P(lim p^(m) = δ_i) = p_i. Early collapse = tails die; late collapse = one token remains, the one that started with the most mass.
8. Partially synthetic: every m ≥ 2 trains on the *same* real corpus of size N plus n new samples from p^(m−1). Theorem 2: exact S_m in terms of α = n/(N+n). If n ≪ N then S_m ≈ S_0. Even if n ≫ N, S_m stays O(S_0) for large N (does not walk to 1).
9. Theorem 3: E‖p^(m)−p^(1)‖₁ < (1/N) √(π n / 2) G_n(s), independent of m. Invert to the max-n bound (11).
10. Extra loops (simulations only): *Most Recent Models* — last K teachers, n/K samples each; *Randomly Sampled Data* — each of n tokens drawn uniformly from {real} ∪ {all past models}.
11. GPT-2 check: train a nanoGPT on tiny Shakespeare for 2000 steps, treat that checkpoint as p^(0), then recurse with the same architecture under fully-synth / 50-50 / 20-80 mixes. Report L1 averaged over 300 random contexts from p^(0), plus val loss vs iteration for generations 1–10.

## Assumptions

- One-hot context embeddings, linear Softmax, exact MLE · hides transformer geometry, in-context learning, and any teacher that is *not* an empirical count. Indic / agentic “teachers” in V5 are themselves biased generators.
- Analysis is for a *single pre-fixed context*. Uniform collapse over all contexts is left open (footnote 1). Low-resource Indic contexts have tiny N per context, which is exactly the regime they say collapses fast.
- Every p^(m) is unbiased, E p^(m) = p. Collapse is variance, not bias. A Phi-style textbook teacher that *shifts* the distribution is outside the theorem.
- Functional approximation error is excluded by design. The GPT-2 run tries to minimise it by freezing architecture and calling the first checkpoint “ground truth.” A 1–10T V5 model is in the opposite regime.
- Real data in the partial loop is *the original corpus, reused every generation*, not a fresh human draw and not a filtered crawl. V5 “web 34%” is not this N.
- Tokens inside one context are i.i.d. multinomial. Long-context and agentic trajectories are the opposite of that.
- Vocabulary s is treated as known and static. Indic scripts, code tokenisers, and tool-call vocabularies change the s that appears in (11).
- “Synthetic” here means *self-samples of the previous student*, not high-quality data generated by a stronger frozen teacher. Cosmopedia / Phi / agent rollouts from a better model are a different object.

## Numbers we can cite

- Total collapse is almost sure under fully synthetic training · absorbing Markov chain on the simplex · §3.1, before Thm 1.
- S_m = 1 − (1−1/n)^m (1−S_0) · fully synthetic, any n, m · Thm 1 / eq. (6).
- Collapse probability: 1 − n(1−S_0)(1−1/n)^m ≤ ρ_m ≤ 1 − [(1−S_0)/(1−1/s̃)](1−1/n)^m · Thm 1 / eq. (7).
- Expected absorption time: 1 + [(1−S_0)/(1−1/s̃)](n−1) ≤ E[T] ≤ 1 + (1−S_0) n (n−1) · so Ω(n) and O(n²); Fig 2 suggests the truth is near the linear lower bound · Thm 1 / eq. (8) + §3.1 + Fig 2.
- P(the chain dies on token i) = p_i · Prop 1. Formalises Shumailov’s early (tails die) vs late (one atom left) collapse.
- α := n/(N+n) is the synthetic *weight* in the partial mix, not a token budget share · Thm 2.
- If n ≪ N then S_m ≈ S_0; even n ≫ N gives S_{m+1} ≈ 1/N + (2+1/N)^{−1}(1−1/N)(2−1/N)S_0 → S_0 for large N · Thm 2 discussion. Mixing real data every generation prevents S_m → 1.
- E‖p^(m)−p^(1)‖₁ < N^{−1} √(π n / 2) G_n(s), *independent of m* · Thm 3. C_0 = e³/(2π) ≈ 3.19, C_1 = 6e/π^{3/2} ≈ 2.93 · eq. (10).
- Sufficient n for E L1 < ε: n ≤ 2π e^{−2} min[s−2, log(√2 π N ε /(6 e s))] · eq. (11) / §3.2. Authors’ gloss: synthetic “exponentially smaller” than real.
- Fig 2 fully-synth sims · vocab s = 600, S_0 ∈ {0.01, 0.1, 0.5, 0.7} with support s̃ ∈ {181, 29, 10, 9}, n ∈ {10, 50, …, 400}, 100 runs. Mean T at n = 400 ≈ 840 / 755 / 585 / 375 (pixel read-off, ±15). Higher S_0 (peakier start) collapses faster. Red dashed line = Thm 1 lower bound; points sit above it, roughly linear in n.
- Fig 3 partial-synth · N = 100 real, n ∈ {1, 10, 100, 500} additional synth, 50 generations, 100 runs, s = 600, s̃ = 52, S_0 = 0.1. Mean σ_m stays ~0.10–0.11 (theory dashed matches). Mean L1 plateaus ≈ 0.02 / 0.08 / 0.17 / 0.20 as n grows. More synth ⇒ more drift, but drift saturates rather than walking to 2.
- Fig 4 partial-synth, n = 10, N = 100, S_0 ∈ {0.01, 0.1, 0.5, 0.7} with s̃ ∈ {484, 52, 22, 16}. Mean σ_m sits at S_0. Mean L1 plateaus *fall* as S_0 rises: ≈ 0.15 / 0.083 / 0.038 / 0.027. Peakier real distributions drift less once real data is always in the mix.
- GPT-2 L1, 300 random contexts from p^(0) · pure synth rises ~0.43 → ~0.78 over generations 1–9; 50/50 and 20/80 stay flat near 0.43 · Fig 5 top-left / §4.1. Bands: red widens to ~0.72–0.84 by m=9; mixed bands stay ~0.38–0.48.
- GPT-2 val loss, log-x iterations ~1–20 · pure synth plateaus Gen 1 ≈ 1.45 … Gen 10 ≈ 1.90, Gen 10 upturns (overfit) · Fig 5 top-right. 50/50: Gen 1 ≈ 1.46, Gen 3–10 clustered ≈ 1.53–1.57, gap saturates · Fig 5 bottom-left. 20/80: all 10 gens indistinguishable, final ≈ 1.45–1.47 · Fig 5 bottom-right.
- Window experiment · n = 10, 500 gens, 100 runs, s = 600, s̃ = 52, S_0 = 0.1 · Fig 6. K=1 (fully synth): σ_m → 1 by m≈40, mean T = 17. K=5: mean T = 95. K=10: mean T = 216, σ_m still ~0.85–0.9 at m=500. Window = m (uniform over history, includes real): σ_m flat ≈ 0.25, L1 plateau ≈ 0.9, only one Dirac in 100×500.
- GPT-2 architecture (Table 1 / App. C): context 128, emb 256, 8 layers, 4 heads, vocab 65, dropout 0.2, lr 10^{-3}, batch 256, max 2000 iters. Character tokenizer on tiny Shakespeare. Code: nanoGPT.

## Figures

- **Fig 1** (`figures/generations-1.png`) — five simplex snapshots p^(0)…p^(40), s=3, ℓ=4, c=81, n=1000. Red points start as a filled blob, walk onto the triangle edges by gen 10, and sit on the three vertices by gen 40. Claim: fully synthetic training concentrates on Dirac atoms. No axes; opacity ≈ mass.
- **Fig 2** (`figures/case1.png`) — 2×4. Top: log(1+p_i) stems over tokens 0–600 for S_0 = 0.01/0.1/0.5/0.7 (s̃ = 181/29/10/9). Bottom: mean absorption generation vs n = 10…400 (blue ×, 100-run averages) plus red dashed Thm-1 lower bound. Claim: peakier starts (larger S_0) and smaller n collapse faster; empirical T is linear-ish in n and above the bound.
- **Fig 3** (`figures/case2_exp.png`) — 2×4, columns “1 / 10 / 100 / 500 additional samples”, N=100, 50 gens. Top: σ_m spaghetti (yellow) + empirical mean (red) + S_m theory (blue dashed) — means flat at ~0.11, variance grows with n. Bottom: L1 to p^(1) jumps then plateaus at ~0.02/0.08/0.17/0.20. Claim: real data every generation stops progressive collapse; extra synth only raises the *level* of the plateau.
- **Fig 4** (`figures/case2_exp_different_s0.png`) — 3×4, n=10, N=100. Row 1: same stem plots, s̃ = 484/52/22/16. Row 2: σ_m flat at S_0, theory matches. Row 3: L1 plateaus shrink as S_0 grows (~0.15 → ~0.027). Claim: once real data is mixed in, a peakier original actually drifts *less*.
- **Fig 5 top-left** (`figures/l1-1.png`) — GPT-2 ‖p^(m)−p^(1)‖₁ vs generation 1–9. Red = synthetic (rises ~0.43→0.78, band widens). Orange = 50/50 (flat). Green = 20/80 (flat, slight down-drift). Dash-dot bands; red fill only. Claim: mixing real data kills the drift that pure synth produces.
- **Fig 5 top-right** (`figures/val_generated-1.png`) — title `synthetic`. Val loss vs log iterations, Gen 1–10 (tab10). Plateaus strictly worsen with generation (1.45 → 1.90); Gen 10 upturns. Claim: recursive self-training degrades the scaling curve.
- **Fig 5 bottom-left** (`figures/val_mix_0.5-1.png`) — title `synthetic 50% - real 50%`. Same axes. Gen 1 ends ~1.46; Gen 3–10 bunched ~1.53–1.57. Claim: half real caps the damage; leftover gap is small and saturates.
- **Fig 5 bottom-right** (`figures/val_mix_0.8-1.png`) — title `synthetic 20% - real 80%`. All ten gens overlap, final ~1.45–1.47. Claim: 80% real is enough, in this toy, for generation-independent val loss.
- **Fig 6** (`figures/mixed_data_window.png`) — 3×4, window = 1 / 5 / 10 / m, n=10, 500 gens, 100 runs. Row 1 σ_m, row 2 L1, row 3 hist of T (means 17 / 95 / 216 / 98). K=1 absorbs immediately; larger K delays; window=m never absorbs (histogram empty, one Dirac in 100 runs). Claim: a finite teacher window only postpones collapse; keeping the whole history (including real) qualitatively changes the process.

Pixel values above are inspect_image read-offs (±0.01 on L1/loss, ±0.02 on σ, ±15 on T) except printed tick/legend numbers.

## Implementation nits

- Theory: no optimiser. Closed-form MLE = counts. n is *per-context* sample size, not corpus tokens.
- Sims Figs 2–4, 6: 100 independent runs; s = 600; typical (s̃, S_0) = (52, 0.1). Fig 2 n grid {10, 50, …, 400}. Fig 3 n ∈ {1,10,100,500}, N = 100, 50 gens. Fig 4 n = 10, N = 100, 50 gens. Fig 6 n = 10, 500 gens.
- GPT-2 / Table 1: nanoGPT decoder, ctx 128, d=256, 8 layers, 4 heads, dropout 0.2, Adam-style lr 1e-3, batch 256, 2000 iters, char vocab 65, tiny Shakespeare. First checkpoint is declared p^(0). Same hparams for every later generation. L1 averaged over 300 contexts sampled from p^(0). Mix ratios in the neural plots are 100/0, 50/50, 20/80 synthetic/real.
- No public experiment repo beyond the nanoGPT citation. License of the paper: CC BY 4.0.

## Follow-on papers

- 2305.17493 Shumailov et al., *The Curse of Recursion* · names model collapse; Gaussian toy, no training · this paper is the discrete-LM version; do not cite Shumailov for a mix *ratio*.
- 2402.07712 Dohmatob, Feng, Kempe, *Model collapse demystified* · linear regression, test error grows linearly in generation · would change a V5 “synth tokens still scale” claim.
- 2404.03502 Dohmatob et al., *A tale of tails* · collapse as a broken scaling law · relevant if V5 expects 6× OPUS repeats of synth to behave like 6× real.
- 2307.01850 Alemohammad et al., MAD · empirical self-consuming image models; quality depends on fresh-real fraction · same qualitative lever, different modality.
- 2306.11644 Gunasekar et al., *Textbooks Are All You Need* · high-quality *teacher* synth, not self-consuming · the paper that would *defend* Indic/agentic synth if the teacher is frozen and stronger, which 2404.05090 does not study.
- 2402.17387 Fu et al. · TV bound for self-consuming diffusion · closest theory sibling; would matter if V5 treats image-like continuous data.
- 2311.12202 Guo et al. · linguistic diversity dies under synth recursion · qualitative support for protecting Indic tails.
- HuggingFaceTB/cosmopedia (Ben Allal 2024) · the actual large synth pretrain corpus people will compare against; quality-filtered teacher data, not the loop here.

## Assignment mapping

1. **Lane budget shares (code/agentic/reason/long/indic/stem/web sum 100%)** — *silent*. No capability lanes, no 24/2/6/6/16/12/34. Do not hang a headline % on this paper.
2. **Indic split verified / unverified / translated / synthetic** — *silent* on A/B/C. *Challenges* a large D if those tokens later become the training distribution: fully synthetic collapse is a.s. (Thm 1). A 15% synth *slice mixed every step with 85% real Indic* is closer to their 20/80 GPT-2 run, which did not drift — but only if the 85% stays in the hopper every generation.
3. **Agentic / reasoning / long-context as first-class slots** — *silent*. No datasets, no named slots. The statistical object is a single next-token conditional.
4. **Protected always-on floor OPUS cannot starve** — *supports*. Partial-synth theorems exist only because the same real corpus of size N is present at every generation. Quote: “collapse can be avoided if enough real data is injected into the recursive training process” (§3.2). The 8% scarce-lane floor is the V5 implementation of their N. Fig 5: 50% real already flattens L1; 80% real erases val-loss drift.
5. **Anneal reserve / HQ held back for cooldown** — *silent* as a schedule. Weakly related: their p^(0) is a high-quality real corpus that must remain available, not be overwritten. They do not study low-LR cooldown.
6. **Lanes tied to the benchmarks they fund** — *silent*. Metrics are S_m, L1, char-level val loss. No MMLU / HumanEval / Indic QA.
7. **Demand vs unique supply; where a share only works by repeating or synthesising** — *challenges the agentic 40B-from-0.63B (~63×) plan hard*. Fully synthetic training collapses a.s.; E[T] is only O(n) per context. Eq. (11) wants n synthetic *log* in N, i.e. “exponentially smaller compared to real data” (§3.2). A closed agentic loop that trains on its own rollouts is their Fully Synthetic / K=1 case (Fig 6, mean T = 17 at n=10). Repeating real tokens (OPUS 6×) is *not* the same as synthesising: repeats keep the same empirical p^(1), they do not start the absorbing chain. Indic/reason/long at ~1.2× repeat is on the safe side of this paper; agentic at 63× synth is not, unless a large frozen real (or stronger-teacher) pool is mixed in every step, à la their N or window=m.

## What not to overclaim

- Do not quote 50% or 80% real as a universal “collapse threshold.” Those are two mix points on a 65-char Shakespeare nanoGPT. The theorem is a *logarithmic* n(N, s, ε), not a percentage.
- Do not treat this as evidence against Phi / Cosmopedia / filtered teacher textbooks. The object of study is a *self-consuming* student, unbiased given finite counts. A stronger frozen teacher is outside every theorem.
- Do not scale Fig 5’s +0.45 val-loss (Gen 1 → 10, pure synth) to a 1–10T V5 run. The model is 8×256, 2000 steps, one play. The transferable claim is the *shape*: no real in the mix ⇒ monotone drift; real every generation ⇒ plateau.
