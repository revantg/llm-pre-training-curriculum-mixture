# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Session 5 · paper workspace

    Live notes while we read the five mixture / synthetic-data papers.
    Each paper gets a teaching cell after the deep-read lands.
    """)
    return


@app.cell
def paper_map(mo):
    mo.md(r"""
    ## Why these five papers

    The assignment is a defended V5 *recipe*. Each paper answers a different attack a reviewer will make.

    | Paper | Reviewer attack | What we need from it |
    |---|---|---|
    | **CLIMB** (2504.13161) | "You picked 24/16/2 by gut." | Can a proxy *search* a mixture, or only a human slider? Does search starve scarce lanes? Complement or rival to OPUS? |
    | **Two-Phase** (2412.15285) | "Why is anneal only ~2%?" | Real phase-1 / phase-2 split. What they hold back. Whether a short HQ second phase is enough. |
    | **Demystifying Synthetic** (2510.01631) | "Agentic needs 63× more tokens than exist. Just generate them." | Safe synth:real ratios. What synthetic actually buys. Where it hurts. |
    | **Model Collapse** (2404.05090) | "Synthetic Indic / agentic will collapse the model." | What they *prove* vs simulate. Real-data fraction that stops collapse. Whether the math even applies to trajectories / translated Indic. |
    | **OpenCoder** (2411.04905) | "24% code and 6% long-ctx are made up." | A published code cookbook: code share, anneal, synthetic code, repo packing. |

    Read order as they land: **idea → assumption → number → what it does to our spec**.
    I will walk each paper that way. Do not memorize abstracts.
    """)
    return


@app.cell
def two_phase_teach(mo):
    mo.md(r"""
    ## Paper 1 · Two-Phase Pretraining (2412.15285)

    NVIDIA / Stanford / BU. 8B models. Closest analog to V5 main-run vs anneal — and the analog that *breaks* if you treat their Phase-2 as our 2% cooldown.

    ### The idea, one sentence
    Most of the run is a *diversity* blend (lots of web). Then you switch to a *different* blend for a long final stretch: high-quality crawl only, lots of math and code, a sliver of task data. Order matters even when the weights are the same.

    ### The number that attacks our spec
    Same winning blend, Phase-2 share of a 1T run (Table 14):

    | P2 share | avg | GSM8K | code |
    |---|---|---|---|
    | 0% | 37.68 | 16.60 | 16.22 |
    | **10%** | 50.48 | 33.13 | 32.55 |
    | 20% | 51.58 | | |
    | 30% | 52.28 | | |
    | **40% (best)** | **52.86** | 40.33 | 38.33 |
    | 50% | 51.96 | 37.68 | 36.86 |

    Almost all of the capability jump appears by **10%**. 40% is best. 50% overfits. They **never tested anything between 0 and 10%**. Our ~2% anneal is 5× smaller than their smallest tested P2 and 20× smaller than their optimum.

    So: this paper **supports "hold the best data for the end"** and **challenges calling 2% an anneal in their sense**. Two different objects. Their P2 is a second pretraining *blend* lasting hundreds of billions of tokens. Ours is a reserved HQ low-LR slice.

    ### Other numbers worth keeping
    - Two-phase vs random order, *same* weights: **+3.4 avg**, almost all GSM8K **30.86 → 40.33** and code **35.55 → 38.33**. MMLU flat. Late quality helps sharp islands, not general knowledge.
    - Organic epoch ceilings: high-quality crawl peaks at **6**. Math in P2 peaks at **8**. That is a repeat ceiling on *large unique pools*. Agentic at 63× is not in this paper.
    - Quality-gating web: natural CC is **64% Low**. Zeroing Low lifts MMLU **42.94 → 56.10**.
    - Winning blends: P1 crawl 59 / code 20 / math 2.9. P2 High-crawl 31 / math 24 / code 20 / task 1.3. Not our 24/2/6/6/16/12/34.
    - Silent on Indic, agentic, long-context, OPUS floors.

    ### What not to say in the README
    Do not quote 40% as the V5 anneal. Do not use the 8-epoch ceiling as a synthesis budget.
    """)
    return


@app.cell
def collapse_teach(mo):
    mo.md(r"""
    ## Paper 2 · Model Collapse (2404.05090)

    TII / NYUAD. Statistical analysis, not a mixture recipe. This is the paper a reviewer uses to attack "just synthesize the agentic 63× hole."

    ### The idea, one sentence
    If tomorrow's model trains only on yesterday's model output, rare tokens die. After enough generate-train cycles the next-token law becomes a Dirac spike. They call that *total collapse*. Mixing the *same real corpus* into every generation stops the walk.

    ### Two loops
    - **Fully synthetic** — train only on the previous generation. Absorbing Markov chain. Collapse is almost sure. Expected time ~O(n) samples per context.
    - **Partially synthetic** — every generation sees a fixed real corpus of size N *plus* n fresh synth samples. L1 drift is bounded independently of how many generations you run, if n is small enough.

    ### The number that attacks our spec
    Equation (11), authors' gloss: **"the amount of synthetic data should be exponentially smaller compared to real data."** n (synth per context) must be *logarithmic* in (real count × tolerance / vocab).

    Toy GPT-2 (char Shakespeare, vocab 65) — the only neural check:
    - 100% synth: L1 0.43 → 0.78 over 9 gens; val loss 1.45 → 1.90
    - 50/50: L1 flat; val-loss gap saturates after gen 3
    - **20% synth / 80% real**: all ten gens sit on top of each other (~1.45–1.47)

    A finite teacher window (last K models only) *delays* collapse (mean T 17 → 95 → 216 as K = 1 → 5 → 10) but does not stop it. Keeping the whole history including real plateaus.

    ### What this does to V5
    - **Supports** an always-on real floor. Their N is our OPUS 8% scarce-lane floor, conceptually.
    - **Challenges** filling agentic 40B from 0.63B unique by self-synth. That closed loop is their K=1 case.
    - **Does not** attack Phi / Cosmopedia / a *stronger frozen teacher*. That is a different object. They never studied it.
    - **Does not** pick 24/2/6/6/16/12/34. Silent on lanes, Indic split, anneal length, benchmarks.

    ### What not to say
    Do not quote 50% or 80% as a universal collapse threshold. Those are two mix points on a 65-char nanoGPT. The theorem is a log bound, not a percentage.
    """)
    return


@app.cell
def opencoder_teach(mo):
    mo.md(r"""
    ## Paper 3 · OpenCoder (2411.04905v3)

    INF / M-A-P / NJU. Open *code* cookbook: 1.5B + 8B, RefineCode 960B, cleaning, 100B anneal, two-stage SFT. Not a general-mixture paper.

    ### The idea, one sentence
    The missing ingredient in open code models is not more GitHub. It is file-level cleaning, recalling *code-related web*, and spending a little verified synthetic data in the **anneal and SFT**, not the main pretrain.

    ### Do not use this paper to raise our 24% code share
    RefineCode is **90.9% raw code + 7.7% code-web**. They train a specialist. V5 is a 7-lane general model. Category error.

    ### Numbers that *do* transfer
    - GitHub is **~75% exact-duplicate files**. File-level dedup keeps **32.74B** Python tokens; repo-level keeps **99.47B** and still hides 52B identical files. File-level *wins* HE/MBPP at every budget (Fig. 8).
    - They do **not** pack repos. Random concat into **4k / 8k** chunks. No 32k phase. Our 6% long-ctx + "pack whole repos" is unsupported here.
    - Anneal: **100B** after 2.0–2.5T (~4% of tokens). Mix: **84% original RefineCode** + 12.44B algo + 2.71B unit-tested synth + 0.91B textbooks. Ablating HQ (Fig. 9): HE stuck ~0.32–0.35 instead of climbing to ~0.47.
    - Synth is **3.62% of anneal**, ~0.14% of 2.5T. SFT is where they synthesize a lot (4.5M, two stages). Shuffling the two SFT stages *loses* (HE 70.1 → 55.5).
    - `stars>=5` **hurts**. Lower train loss, worse HE/MBPP. Diversity beats fame.

    ### What this does to V5
    - **Supports** a reserved HQ code anneal (algo + unit-tested snippets + textbooks), with most of the mix staying on the original distribution.
    - **Supports** "repeat cleaned unique 2–4×; synthesize only a few percent at anneal; synthesize the SFT tail."
    - **Challenges** repo packing as the long-ctx story.
    - **Silent** on Indic, agentic trajectories, OPUS floors.

    ### What not to say
    "OpenCoder used ~100% code, so raise our code lane." "They pack repos." "8B-Instruct HE 83.5 is SOTA" (Qwen2.5-Coder-7B-Instruct is 88.4, 23.5T closed).
    """)
    return


@app.cell
def climb_teach(mo):
    mo.md(r"""
    ## Paper 4 · CLIMB / Nemotron-CLIMB (2504.13161v2)

    NVIDIA / Georgia Tech. NeurIPS 2025 D&B. A *method* for searching mixture weights over discovered clusters. Not a source of V5 lane percentages.

    ### The idea, one sentence
    Web crawls have no domain labels. Embed + cluster the raw corpus, then *search* the mixture with a cheap proxy + LightGBM predictor instead of guessing 24/16/2. RegMix is CLIMB with K=1. They run K=3.

    ### Two different animals
    - **Continuous pretrain** (after 10T phase-1): mixes go *peaky*. General-reasoning iter 3: C19 43% + C18 22% + C9 18% + C8 13%. STEM wants C7+C8 ≈ 97%.
    - **From-scratch ClimbMix** (400B): mixes stay *broader*. C12 28% + C6 20% + C7 16%. Top-3 ≈ 64%.

    V5 main 2T should look more like ClimbMix (spread). V5 anneal should look more like the continuous mix (concentrate). Copying Fig. 7's peaky weights into a from-scratch run is the mistake they warn about in §6.

    ### Numbers worth keeping
    - 1B / 400B continuous: **+2.0 pp** vs Llama-3.2-1B (53.54 vs 51.56) on 12 reasoning tasks.
    - 350M / 40B: CLIMB 54.83 vs RegMix 53.78 vs DoReMi 53.38 vs Random 52.17.
    - Search budget: **64 + 32 + 16 = 112** proxy runs, split **4:2:1**. 62M proxy almost as good as 350M (60.11 vs 60.41 on the 1B).
    - LightGBM Spearman **0.94**. Iteration 2–3 still moves MMLU (Fig. 5).
    - Similarity ≠ weight. C8 is less similar to MMLU-STEM than C7, yet gets **61%**. Out-of-domain clusters can be useful.

    ### What this does to V5
    - **Supports searching** the seven shares instead of defending them only by taste. Also supports tying each search head to the benches that lane must win.
    - **Supports a complementary floor** ("only in-domain is not optimal") and **challenges a rigid 8% on every named lane**. Their best mixes are intentionally sparse. Code cluster C20 → 0 under a reasoning-only predictor. If Indic/agentic are not *in the predictor loss* or hard-constrained, CLIMB will starve them.
    - **Silent** on Indic, agentic, long-ctx, synth:real. English embedder + English quality FastText. Indic will not appear as a cluster unless Indic text is in the embedding space.
    - **Silent** on 63× agentic synthesis. They never repeat.

    ### What not to say
    Do not paste C19=43% into the README as "CLIMB's web share." Do not claim they discovered code=24% or Indic=16%.
    """)
    return


@app.cell
def synthetic_teach(mo):
    mo.md(r"""
    ## Paper 5 · Demystifying Synthetic Data (2510.01631)

    FAIR / Meta + Virginia Tech + Cerebras. >1000 models, 100M–3B, up to 200B tokens. The measurement Collapse was missing.

    ### The idea, one sentence
    Not "is synthetic good." Instead: at what *mix*, of what *type*, at what *scale*. Answer comes as scaling laws, not one run.

    ### Three types — and they are not interchangeable
    - **HQ rephrase** — a 7B instructor rewrites a real CC doc as Wikipedia-style prose. Facts stay, style changes. **Needs a real source document.**
    - **QA rephrase** — same doc turned into Question/Answer pairs.
    - **TXBK (textbooks)** — invent a 10-chapter book from CC keywords, write chapters from the outline only. **New content, not a rewrite.**

    ### The headline is a mixture, not synthetic
    - Pure HQ or pure QA is **not faster** than raw CommonCrawl.
    - Pure TXBK is **worse**, with the collapse-like pattern.
    - **~1/3 rephrase + 2/3 natural web** reaches the same val loss **5–10× faster** at large budgets (pixels: ~4–6× in the *measured* 10–100B band). Lowest projected irreducible loss too.

    ### Best mix converges *below* 50%
    | Type | Best ratio |
    |---|---|
    | HQ rephrase | stably **~30%** synth (23–31% band, flattens 29–30%) |
    | QA | ~50% at tiny scale → **~30%** as N and D grow |
    | TXBK | **≤3%** at 50B; often **0%** below 10B |

    WRAP's 1:1 recipe **loses** to 30% here. Bigger *models* are *less* tolerant of high synth, not more.

    ### Bigger teacher is not better
    Llama-3-8B rephrase **beats** 3B. **70B does not beat 8B** on HQ (8B lowest across the sweep; 70B worst at 0.5–2%). Budget an ~8B generator, not the biggest one you have.

    ### What this does to V5
    - **Indic D = 15% of the Indic lane** (2.4% of a 2T run): **fine if D is rephrased verified Indic**; **reckless if D is invented textbooks**. TXBK never leaves the 0–3% band at these scales.
    - **Agentic 40B from 0.63B unique**: that is TXBK-class invention, not rephrase. Rephrase needs a real doc; we do not have 40B of real traces to rewrite. This is the cell they say "shows patterns predicted by model collapse."
    - **Silent** on lanes, OPUS, anneal schedule, benchmarks, Indic, code, long-ctx. Metric is English Pile/Wikitext CE.

    ### What not to say
    "Synthetic pretraining is 5–10× better." The 5–10× is tokens-to-equal-loss for ~30% rephrase + 70% web, English CE, ≤3B, big end extrapolated.
    """)
    return


if __name__ == "__main__":
    app.run()
