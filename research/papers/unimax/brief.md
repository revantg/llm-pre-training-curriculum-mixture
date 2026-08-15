# UniMax: Fairer and more Effective Language Sampling for Large-Scale Multilingual Pretraining

arXiv:2304.09151 [cs.CL], submitted 2023-04-18 · **ICLR 2023** (source builds against `iclr2023_conference.sty` with `\iclrfinalcopy` uncommented, `src/main.tex:2-63`) · Hyung Won Chung\*, Noah Constant\*, Xavier Garcia\*, Adam Roberts, Yi Tay, Sharan Narang, Orhan Firat (\* equal contribution) · Google Research.

Read via: **ar5iv HTML** (`https://ar5iv.labs.arxiv.org/html/2304.09151`) for full body incl. Algorithm 1, Tables 1–8, Appendices A–F; **arXiv e-print TeX** (`src/main.tex`, 849 lines) to verify venue, Table 2's exact cells, and to run the grep-negatives; **all 17 figure PDFs** rasterised at 150 dpi to `figures/*.png` and read as pixels (`pdftoppm`), several also measured programmatically against their own gridlines. `xd://inspect_image` not needed.

---

> **STATUS as of final resync — read this before acting on §6.** `SOLUTION.md` §2 has since been **rewritten by the spec owner**, using this brief plus `EmnlpPaper`'s NVIDIA result. Tier C is now **4% / 2.53×** (not 8% / 5.06×), tier D is 26%, and §2 already carries the cap reframe, the Yoruba ≈26M-token pool comparison, the N ∈ {1,5,10} sweep, the model-scale caveat and the `Σ U == C` edge case — all findings from this brief, landed. **§6's draft insert is therefore SUPERSEDED and must not be applied**: it recommends 7.91% / N=5, and the owner went further to 4% / N=2.53 on the stronger evidence that no published arm repeats a 1.5–19B source and wins. §6 is retained only as the record of what this paper alone supported.
>
> **Two defects I found in the rewritten §2 and reported to the spec owner, both FATAL-class by the rubric's labels:**
>
> 1. **§2 line 91 claims a derivation that does not hold.** "The four percentages above are what that cap produces on our real pools" is false: Algorithm 1 at N=2.53 on our pools emits **A 32.00% (1.58×), B 32.00% (2.25×), C 4.00% (2.53×), D 32.00% (0.62×)** — only tier C matches, because the uniform leg flattens A/B/D toward equal thirds. The fix is one clause and it *strengthens* the argument: the cap sets C (the only tier at the ceiling) and we **deliberately reject** the uniform leg, because UniMax's uniformity is justified by equity across **languages** and has no analogue across **quality tiers** — applying it here would move 8pp from verified native into synthetic.
> 2. **The anneal breaks the newly declared cap.** If the anneal's Indic preserves the tier split, anneal Indic = 21.875% × 80B = 17.50B, anneal tier C = 0.70B, so whole-plan tier C = 12.64 + 0.70 = **13.34B = 2.668 epochs > 2.53**. Whole-plan per tier: A 2.084, B 2.228, **C 2.668**, D 0.535. Either declare **N = 2.67** whole-plan, or **hold tier C out of the anneal** (then C stays 2.528). §2 currently says neither, and until it does the declared cap is fiction.
>
> Independent of both: the **5.70% one-epoch boundary in §5 is the spec's own number**, stated verbatim at `SOLUTION.md:197` before either brief existed — neither I nor `EmnlpPaper` contributed it. What is new is its **status**: it was internal arithmetic with no external referent, and it now coincides with observed practice at two labs. Quote **0.966 epochs against the 113.9B denominator** (§5's table shows 0.96 because it uses the rounded 114B) so no reader thinks the pool moved.

## VERDICT — utility first

**(a) Is this useful for building our mixture/curriculum? YES — it is the most useful paper in the set for §2, and the only one that touches Indic at all.**

Three concrete things it gives us that nothing else does:

1. **It converts our hand-chosen tier-C 8% into a derived number.** Run their Algorithm 1 on our four tiers with our real pools (A 64.0 / B 44.9 / C 5.0 / D 162.0 B) and a 316B lane budget, and a declared cap of **N = 5 epochs outputs tier C = 7.91%**. Our 8% is that number to within 0.09pp. The tier share and the epoch cap are *the same object* viewed from two ends, and we can now say so with a published algorithm behind it.
2. **It gives us the only per-language low-resource repetition measurement in the evidence base**: N ∈ {1, 5, 10} → TyDi QA 82.2 / 81.5 / 81.8 (Table 2 right, Large 1.2B). At **5 epochs the cost is 0.7 pt with no monotone trend** — the closest thing we have to a direct test of tier C at 5.06×.
3. **It gives us a real Indic precedent number, and it cuts both ways.** umT5's 14 Indic languages get **4.14% of a 1.163T-token budget = 48.2B tokens = exactly 1.00 epoch** of the 48.4B-token Indic pool (Table 8, 1× column, summed). That is a *supply-limited* share, not a chosen one — the cap binds for all 14. Paired with the second disclosed build (see the joint statement below) it turns "one epoch of real Indic" from our arithmetic into observed convention, which **defends §5's 5.5% floor** and **puts real pressure on §1's 15.80%**.

**The joint statement, agreed verbatim with `EmnlpPaper` so both briefs read identically:** *the two disclosed multilingual builds that publish per-language Indic volumes both serve Indic at exactly 1.00 epoch, in both cases because the epoch cap binds rather than because the share was chosen.* umT5 at the 1× budget serves 48.2B against a 48.4B pool; Parmar et al. (EMNLP 2024, 8B) serve 6.00B against a 6.00B pool over 9 Indic languages. Two labs, budgets 3.9× apart (1.163T vs 300B), pools 8× apart, same answer. **Carry their caveat**: Parmar has no combined whole-corpus run — English, multilingual and code are ablated separately at 300B/300B/150B — so their 2.000% is a share of a multilingual-only budget and **must not be read as a lane share in our 7-lane sense**; their only whole-corpus figure is the natural 0.328%. That is exactly why the common currency here is **epochs on the real pool**, not percentages.

| build / plan | Indic served | real Indic pool | **epochs** |
|---|---|---|---|
| umT5, 1× budget (UniMax Table 8) | 48.2B | 48.4B | **1.00** |
| Parmar et al. UniMax(1e), multilingual arm | 6.00B | 6.00B | **1.00** |
| **our §5 real-token floor, 5.5%** | 110.0B | 113.9B (A+B+C) | **0.97** |
| **our §1 lane share, 15.80%** | 316.0B | 113.9B (A+B+C) | **2.77** |
| our §1 lane share, *if tier D's 162B synthetic counts as supply* | 316.0B | 275.9B | 1.15 |

Two consequences, and I had the second one backwards in the first draft of this brief.

- **§5 gains a defence it did not have.** Our 5.5% real-token floor is **0.966 epochs** of the 113.9B real Indic pool. The one-epoch boundary itself (**5.70%**, with 6.0% at 1.054) is **already in the spec verbatim at `SOLUTION.md:197`** and is not a contribution of either brief — what is new is that the boundary had no external referent and now coincides with observed practice at two independent labs. Upgrade §5 from "internally derived" to "internally derived and independently matched."
- **§1's 15.80% is under pressure and we should say so before a reviewer does.** Against *real* Indic it is **2.77 epochs, 2.8× what both published builds do**. It is only 1.15 epochs if Sangraha's 162B synthetic counts as Indic supply — which is precisely the substitution E9 names as wishful accounting, and the same gap the v3 red-team logged as W9. The honest sentence is that 15.80% buys 2.77 epochs of real Indic plus a synthetic tier, not 1.14 epochs of "Indic."

**(b) The decision it lets us make differently.** Stop defending the tier table as four percentages and defend it as **one declared per-tier epoch cap plus quality-ordered shares** — which is what §2 now does. On this paper's evidence alone the cap lands at **N = 5 → tier C = 7.91%** (see §4 for the full sweep); with `EmnlpPaper`'s NVIDIA arm added, the spec owner moved further to **N = 2.53 → tier C = 4%**, and that is the better call, because no published arm anywhere repeats a 1.5–19B source and wins. What this paper uniquely supplies to that decision is the *mechanism* (Algorithm 1, so shares become an output of a declared cap rather than four taste calls), the *inversion* (max tier-C share = N × 5.0B / 316B, which kills the composer's 20% at N = 12.64), and the *implementation guard* (`Σ U == C`, without which the cap is fiction on a supply-poor lane). Its limit: N = 2.53 sits in the gap UniMax never tested — the sweep is {1, 5, 10}, so 2, 3 and 4 are unmeasured.

**(c) SOLUTION.md numbers it touches, by section.**

| § | Number | Effect |
|---|---|---|
| §2 | tier C, now **4% / 2.53×** (was 8% / 5.06×) | **Supports the direction, and flags the residue.** This paper alone justifies at most N=5 → 7.91%; the move to 4% rests on `EmnlpPaper`'s NVIDIA arm, not on UniMax. What UniMax adds: 2.53 sits in its **untested gap** (sweep is {1,5,10}; 2, 3, 4 never run), and its measured penalty at the nearest tested point is only −0.7 pt at 1.2B, so 2.53× is comfortably inside anything it observed. **Two FATAL defects in the rewritten §2** — the N=2.53 derivation claim, and the anneal breaking the cap — are in the STATUS box above. |
| §1 | Indic lane **15.80% / 1.14×** | **CHALLENGES — corrected from an earlier draft of this brief.** The 1.14× only holds if tier D's 162B synthetic counts as supply. Against real Indic (A+B+C = 113.9B) it is **2.77 epochs, 2.8× both disclosed builds**, which serve exactly 1.00. Do not cite 1.14× as the defence; cite 2.77 and defend the synthetic substitution separately, or the E9 objection writes itself. |
| §5 | Indic real-token floor **5.5%** | **SUPPORTS — upgraded.** UniMax has no floor *mechanism*, but 5.5% of 2.0T = 110.0B = **0.966 epochs** of the 113.9B real pool, matching umT5's and Parmar's realised 1.00. (§5's table shows 0.96 because it uses the rounded 114B; quote 0.966 with the 113.9B denominator.) The **5.70%** boundary is the spec's own, already at `SOLUTION.md:197`; what this adds is external corroboration of its magnitude, not the number. |
| §2 | "composer default C=20% is not fundable (12.6×)" | **Confirms and strengthens** — 12.64 epochs on a published cap axis, not just arithmetic. |
| §2 | A 40 / B 30 / D **26** | **Challenges the shape, and we should refuse — explicitly.** Algorithm 1's uniform leg at the declared N=2.53 emits **A 32.00 / B 32.00 / D 32.00**, moving 8pp out of verified native into synthetic (at N=5 it is 30.70 each, −9.30pp from A). Their uniformity is justified by *linguistic/demographic equity across languages* (App. B), which has no analogue across quality tiers of one lane. Take the cap; reject the uniform leg **in writing** — §2 line 91 currently claims the cap *produces* 40/30/26, which it does not. |
| §2 | "no paper here studied Indic" | **Now false — fix it.** 14 Indic languages with character counts (Table 8); Bengali and Telugu are 2 of the 4 languages in the "lower-resource" panel (Fig. 4c, verified: bottom-4 = id/bn/te/sw). |
| §2 hazard 1 (tokenizer) | analogy-only | **Refines with real script evidence.** Devanagari vocabulary share: τ=1 **0.5%** → τ=3.33 **2.2%** → UniMax-N10 @1× **2.6%**, mT5 **1.3%** (Table 4). Raising N raises tail-script capacity. Their mitigation for uncovered units is **byte-level fallback on a 256,000-subword vocab** (App. C) — name it. |
| §7 **H3** | 1B, 100B, C at 8/4/0%, IndicGenBench chrF + MILU | **Challenges the design.** Their N-sweep found the repetition effect *absent* at 1.2B, and their headline is that over-repetition harm **grows with model scale** (Fig. 2b: yo overfits at XXL 13B, not at Large 1.2B, same τ). H3 at 1B is therefore likely underpowered for the harm it is testing. Add a **held-out CE-loss check on the tier-C slice** (the channel where the signature actually appears) and pre-commit an escalation to 3B. Independently corroborated: an 8B/300B external application of the same algorithm loses **1.70 MMLU going N=1 → 4** (§8), 2.4× UniMax's 1.2B penalty at a lower N. |
| §7 **H5** | Indic-up anneal 21.875% | **Silent — no help.** Zero occurrences of curriculum / anneal / stage / schedule / mid-train / cooldown in the source. MAP-Neo remains the only counter-precedent. |

**(d) KEEP.** Cite in §2 as the tier-C ceiling authority and the Indic precedent; cite in §7 to fix H3's scale.

**The one thing to be honest about.** Their per-language pools are *tiny*: the smallest is Yoruba at **≈0.1B characters ≈ 26M tokens** (ablation corpus) / **0.3B chars ≈ 75M tokens** (refreshed corpus), and the smallest row of all is `bg-Latn` at 0.1B chars ≈ 25M tokens. Our tier C is 5.0B tokens — **67× larger than their Yoruba and 200× larger than their smallest row**. Applying their N=5 result to a 5.0B pool is extrapolation. Unlike every other scale gap in our evidence base, **this one runs in our favour**: the same epoch count on a 67× larger unique pool is strictly less repetition pressure. The gap that runs *against* us is model scale (their N-sweep is 1.2B only), and that is the caveat that must be attached.

---

## 1. The algorithm, exactly

**Two prongs.** (i) Pre-allocate to under-represented datasets whatever *N* epochs of them costs; (ii) spend everything left **uniformly** across the languages that still have enough data. Not a temperature, not a share — a hard ceiling on epochs plus uniformity above it.

**Inputs** (§3, Algorithm 1, `main.tex:160-202`): per-language **character** count `c_l` for all `l ∈ L`; total **character budget** `C`; max epochs per language `N`. **Output**: sampling distribution `p_l`.

```
L ← sortByCount(L)              # ASCENDING — smallest corpus first
B ← C                           # remaining budget
i ← 0
for l in L:
    b_l ← B / (len(L) − i)      # equal split of what's LEFT among languages NOT YET assigned
    if b_l > c_l × N:           # uniform share would exceed N epochs of l
        U_l ← c_l × N           #   → cap it: give exactly N epochs
    else:
        U_l ← b_l               #   → l has enough data: give it the uniform share
    B ← B − U_l                 # residual redistribution happens HERE
    i ← i + 1
p ← normalize(U)
return p
```

**What is capped, per what unit.** The cap is on **epochs over one language's character corpus** — `U_l ≤ c_l × N`. Unit is a *language*, quantity is *characters*, and `N` is a global scalar, identical for every language. There is no per-language `N`.

**How the residual is redistributed.** Not by a second pass — by the *ascending sort plus the shrinking denominator*. Because languages are visited smallest-first, every language that hits its cap under-spends its notional share, and `B ← B − U_l` immediately returns the difference to the pool, while `len(L) − i` shrinks. The next (larger) language therefore computes `b_l` against a *larger* per-language share. The freed budget flows monotonically **up** the resource ranking and lands entirely on the languages large enough to absorb it, which all end up at the identical uniform value — the flat plateau in Fig. 1(b). Head languages are never re-prioritised relative to each other; they simply all sit at the same rate.

**Token↔character conversion** (§3.1): character counts, not tokens, are the size measure — deliberately, because tokenising 100+ languages requires a pre-tokeniser and fails on unspaced scripts. When comparing to token budgets they assume **4 characters per token**, following ByT5. A separate SentencePiece vocabulary is trained **per sampling strategy**, on the same distribution as training (§3.1, §4.2).

**Edge case the paper never hits and we do.** If `Σ min(b_l, c_l·N) < C` — the whole corpus is smaller than the budget — the loop ends with `B > 0` and `normalize(U)` silently rescales, so every language is served `U_l × C/ΣU` and **the cap is violated**. In UniMax's setting this cannot happen (28.8T chars of corpus vs a 4.65T-char budget). **In ours it happens at N=1**: our four tiers total 275.9B against a 316B lane, so Algorithm 1 leaves 40.1B unallocated and normalisation pushes every tier to 316/275.9 = **1.145 epochs**, not 1.000. Anyone porting Algorithm 1 to a supply-poor lane must check `ΣU == C` — this is exactly the E9 wishful-accounting trap, hiding inside a published algorithm.

**Temperature baseline, for contrast** (§3, Eqs. 1–2): `p_l = n_l / Σ n_l`, then `q_l = p_l^(1/τ) / Σ p_l'^(1/τ)`. Literature values (Table 1): mBERT 1.43, XLM 2.00, XLM-R 3.33, mT5 3.33, XLM-E 1.43. The paper's framing: "there is no guarantee that there exists a value of τ that achieves the desired balance on high- and mid-resource languages while still avoiding overfitting on the tail languages" (§3).

---

## 2. Setting and every number

### Corpora
| | Ablation corpus (§4.1) | Refreshed corpus (§6, Table 8) |
|---|---|---|
| Base | mC4 3.0.1, langid confidence re-filtered 0.7 → **0.95** | mC4 **3.1.0**, crawls through **Aug 2022** |
| Size | (not stated as a total; abstract says **29T chars / 107 languages**) | **28.8T chars, 9.0B documents** (+35% docs over mC4) |
| Languages | **107** = 101 languages + 6 Latin-script variants (§4.4) | 107 rows |
| Filtering effect | removes 6.1% of docs / 5.1% of chars; most-filtered Welsh 86%, Sindhi 85%, Luxembourgish 84% | + soft bad-word filters (0.1% pass-through); bad-words terms dropped if they filter >10% of a language (more than doubled the Chinese sub-corpus) |
| Used for | §4–5 ablations, Figs. 1–6 | umT5 final models, Table 3 |

Motivating data-quality fact (§4.1): only **40%** of documents in mC4 3.0.1's **Marathi** bucket were well-formed Marathi — 50% other languages, 10% non-language. This is an Indic language and it is the paper's own headline example of crawl mislabelling. Directly relevant to our tier B.

### Per-language corpus sizes — **the smallest pool in the study**
- **Ablation corpus: Yoruba ≈ 0.105B characters ≈ 26M tokens.** Derived from §1: English "roughly 9.7 trillion characters, which is over 92,000 times larger than the lowest resource language, Yoruba" → 9.7e12 / 92,000 = 105.4M chars. **Independently corroborated**: at τ=3.33 Yoruba's rate is 0.24% (Table 8); 0.24% × 4,653B-char 1× budget ÷ 0.105B = **106 epochs**, which reproduces §1's "repeated over 100 times" and Fig. 1(a)'s ≈101 at rank 106 measured from pixels. [INFERENCE, triple-corroborated]
- **Refreshed corpus (Table 8): Yoruba 0.3B chars ≈ 75M tokens** — smallest true language. Smallest row overall is `bg-Latn` **0.1B chars ≈ 25M tokens** (a Latin-script transliteration variant, not a language).
- Largest: English **13,396B chars** (refreshed) / 9.7T (original). Dynamic range within the study ≈ **45,000× to 134,000×**.
- **Indic slice, Table 8** (chars, B): hi 75, bn 34, ta 17, mr 13, ne 11, ur 11, ml 9.4, kn 6.9, te 5.9, gu 3.6, si 3.0, pa 2.2, sd 0.9, hi-Latn 0.7 → **193.6B chars = 48.4B tokens across 14 languages**.
  - At the **1/8** budget the uniform per-language share is 8.6B chars, so **7 of 14** Indic languages are epoch-capped (kn, te, gu, si, pa, sd, hi-Latn).
  - At the **1×** budget the uniform share is 149.8B chars, so **all 14 are capped** — hi (75B) included.
  - Summing Table 8's 1× column over those 14: **Indic = 4.14% of the umT5 budget = 48.2B tokens = 1.00 epoch** of the Indic pool. This is the only published Indic pretraining share we now hold, and it is supply-limited by construction.

### Budgets (derived; both independently corroborated against Table 8)
Batch **1024 sequences**; each sequence is a **568-token chunk** of corpus, split into 512 input + 114 target under T5 span corruption (§4.4). So corpus tokens consumed per step = 1024 × 568.

| Name | Steps × seq len | Tokens | Characters |
|---|---|---|---|
| **1/8** (all Figs. 1–6, Tables 5, 7) | 250,000 × 512 | **145.4B** | **581.6B** |
| **1/2** (Fig. 3, Table 2 left) | 1,000,000 × 512 | **581.6B** | **2.327T** |
| **1×** (umT5, Table 3; "over a trillion tokens") | 1,000,000 × 1024 | **1.163T** | **4.653T** |

Corroboration: Table 8's 1/8 column gives capped `af` 1.27% on 7.4B chars ⇒ C = 582.7B (derived 581.6B, 0.2% off); the 1× column gives capped `da` 2.83% on 132B ⇒ C = 4,664B (derived 4,653B, 0.24% off). Uniform-plateau boundaries also check out: at 1/8 the uniform share is 8.6B chars and `gl` (8.8B) is uncapped while `af` (7.4B) is capped; at 1× the share is 149.8B and `uk` (171B) is uncapped while `da` (132B) is capped. [INFERENCE, arithmetic from stated quantities]

### Models
Encoder-decoder, mT5 architecture except relative position embeddings are **not shared across layers**. Vocabulary **256,000** subwords with **byte-level fallback** (unknown → UTF-8 bytes). T5X, Adafactor (constant lr 0.01 for 10,000 steps then inverse-sqrt; second moment **not** factorised; momentum **on**), finetune lr 5e-5, loss normalised by real target tokens (App. C).

**Sizes: Large 1.2B, XL 3.7B, XXL 13B** (Tables 5, 7). umT5 adds Small and Base; **umT5-Large was dropped** for pretraining instability and underperformed umT5-Base on all metrics (§6 fn. 5).

### Epoch counts actually induced (derived from Table 8 τ=3.33 rate × budget)
| Setting | Yoruba epochs |
|---|---|
| τ=3.33, 1/8 budget (Fig. 2b) | **≈4.7** |
| τ=3.33, 1/2 budget (Fig. 3e) | **≈18.6** |
| τ=3.33, 1× budget, refreshed corpus | ≈37 |
| τ=3.33, 1× budget, ablation corpus (§1's claim) | **≈106** |
| UniMax, any budget, N=1 | **1.00 by construction** |

### N (max-epoch) values actually tested
**N = 1 everywhere in the main results.** The only sweep is **Table 2 right: N ∈ {1, 5, 10} → TyDi QA 82.2 / 81.5 / 81.8**, Large size. **N = 2, 3, 4 were never run.** Vocabulary analysis additionally reports UM1 and UM10 at 1× and 4× budgets (Table 4).

**Honest caveat on Table 2 right.** The paper does not state which character budget the N sweep used. Its N=1 value (82.2) matches neither the 1/8-budget Large UniMax (82.19, Fig. 4a) nor the 1/2-budget Large UniMax (83.1, Table 2 left). So the three N values are internally comparable but **not** cross-comparable to any other table in the paper. Quote the 0.7pt spread, not the absolute 82.2.

### Downstream results

**TyDi QA GoldP** (9 languages, in-language multitask finetune, per-language checkpoint selection on validation, validation metrics reported — no test set), average of EM and F1. **Pixel-exact from Fig. 4, confirmed to ≤0.04 against the per-language cells of Table 7:**

| | Large 1.2B | XL 3.7B | XXL 13B |
|---|---|---|---|
| **All 9** UniMax | **82.19** | **83.97** | **84.39** |
| τ=3.33 | 81.69 | 83.41 | 83.89 |
| τ=1 | 80.10 | 82.04 | 83.29 |
| Δ UniMax−τ3.33 | **+0.50** | **+0.56** | **+0.50** |
| Δ UniMax−τ1 | +2.09 | +1.93 | +1.10 |
| **Top-5 (en ru ar fi ko)** UniMax | 78.80 | 80.70 | 81.19 |
| τ=3.33 | 78.66 | 80.40 | 81.00 |
| τ=1 | 78.50 | 80.12 | **81.50** |
| **Bottom-4 (id bn te sw)** UniMax | **86.49** | **87.83** | **88.50** |
| τ=3.33 | 85.60 | 87.03 | 87.49 |
| τ=1 | 82.09 | 84.19 | 85.49 |
| Δ UniMax−τ3.33 on bottom-4 | **+0.89** | **+0.80** | **+1.01** |

**Per-language, XXL** (Table 7 / Fig. 5 left) — the two Indic languages in the suite:
| lang | τ=1 | τ=3.33 | UniMax | Δ vs τ=3.33 |
|---|---|---|---|---|
| **bn** Bengali [rank 37] | 83.8 | 86.6 | **89.5** | **+2.9** (largest gain in the suite) |
| **te** Telugu [rank 59] | 86.4 | **88.8** | 88.5 | **−0.3** |
| sw [62] | 85.2 | 86.2 | 86.6 | +0.4 |
| id [33] | 86.7 | 88.4 | 89.2 | +0.8 |
| ko [27] | 80.0 | 79.9 | 81.5 | +1.6 |
| en [1] | **79.1** | 77.8 | 78.1 | +0.3 |
| ru [2] | **82.9** | 81.3 | 81.0 | −0.3 |
| ar [15] | 82.7 | **83.4** | 83.1 | −0.3 |
| fi [23] | **83.1** | 82.7 | 82.2 | −0.5 |

> **Published-table defect worth knowing.** Table 7's "Avg" column disagrees with the mean of its own nine per-language cells in 4 of 9 rows, as **two exact transpositions**: Large τ=3.33 prints 82.0 (true 81.69) ↔ XL τ=1 prints 81.7 (true 82.04); Large UniMax prints 83.3 (true 82.23) ↔ XXL τ=1 prints 82.2 (true 83.32). Figure 4(a) carries the correct means in all nine cells. **Quote Figure 4, not Table 7's Avg column** — in particular, "UniMax 83.3 at Large" is wrong and would not survive a reviewer recomputing the row.

**WMT21 multilingual MT**, small track, 30 directions among 6 languages, finetune on the mixture, **training data subsampled to 1,000 examples per pair** to force reliance on pretraining, per-pair checkpoint selection **on test**, Serbian-target pairs excluded for script instability. chrF, pixel-exact from Fig. 6 left:

| | Large | XL | XXL |
|---|---|---|---|
| UniMax | **41.80** | **≈45.2** | **48.47** |
| τ=3.33 | 41.19 | ≈44.5 | 48.16 |
| τ=1 | 37.41 | ≈40.9 | 44.58 |
| Δ vs τ=3.33 | +0.61 | +0.68 | **+0.31** |
| Δ vs τ=1 | +4.39 | +4.28 | +3.89 |

**Additional benchmarks** (Table 5, τ=1 / τ=3.33 / UniMax):
- XNLI zero-shot, Large only: 74.8 / 78.2 / **78.3**
- XNLI translate-train: Large 82.0 / 82.3 / **82.7**; XL 84.1 / **85.0** / **85.0** (tie); XXL 85.1 / **85.5** / **85.5** (tie)
- XQuAD EM/F1: Large 71.0/82.6 / **71.6/83.2** / 71.6/83.1; XL 73.8/84.9 / 74.2/85.3 / **74.5/85.5**; XXL 75.1/86.0 / 75.4/86.3 / **75.6/86.4**

**Larger budget** (Table 2 left, Large, 1/2 budget): τ=1.0 81.2 / τ=3.33 82.8 / **UniMax 83.1**.

**umT5 vs mT5** (Table 3, 1× budget, refreshed corpus, translate-train except TyDi QA in-language):
| | XNLI | PAWS-X | XQuAD | MLQA | TyDi QA |
|---|---|---|---|---|---|
| Small | 72.0→**76.2** | 79.9→**87.2** | 49.4/64.5→**60.5/74.0** | 38.8/56.6→**41.8/60.7** | 62.7/74.0→56.6/70.0 |
| Base | 79.8→**80.8** | 89.3→**90.4** | 59.7/75.3→**67.3/79.8** | 48.5/67.6→**51.6/70.5** | 68.4/79.7→68.4/**81.0** |
| XL | 85.3→**86.5** | **91.0**→90.7 | 68.1/82.7→**75.0/86.1** | 56.6/75.1→**58.3/76.8** | 78.4/87.6→74.1/85.2 |
| XXL | 87.1→**87.8** | **91.5**→91.2 | 71.3/85.2→**77.9/88.2** | 58.3/76.9→**70.5/78.6** | 79.5/88.7→**81.2/89.7** |

**Attribution of that gain** (Table 6, App. E): refreshing mC4 alone is worth **+0.1** XNLI (77.6 → 77.7) against umT5-vs-mT5's **+1.0**, so the gain is attributed to sampling, not data freshness. Two clean losses to note: **umT5 loses TyDi QA at Small and XL** and PAWS-X at XL/XXL.

---

## 3. The five questions

### (a) Does it measure degradation from over-repeating a low-resource language? **YES — but the channel and the threshold are not what our H3 assumes.**

Three separate measurements, and they disagree about severity depending on channel and scale.

**Channel 1 — held-out pretraining CE loss (the sensitive one).** Fig. 2(b), τ=3.33, 1/8 budget, Yoruba at ≈4.7 epochs, measured from pixels against the figure's own gridlines:

| series | min loss | at step | final @250K | Δ |
|---|---|---|---|---|
| yo Large 1.2B | 1.768 | 243K | 1.768 | **+0.000** |
| yo XL 3.7B | 1.632 | 247K | 1.632 | **+0.000** |
| yo **XXL 13B** | **1.579** | **188K** | **1.650** | **+0.071** |
| en Large / XL / XXL | monotone | — | 1.521 / 1.368 / 1.268 | +0.000 |

And the sharpest single fact in the paper: **yo XXL's final loss (1.650) is worse than yo XL's (1.632)** — the 13B model ends up worse than the 3.7B model on the over-repeated language while every English curve improves monotonically with scale. Scale inversion, caused purely by repetition.

Longer train, Fig. 3(e), τ=3.33, 1/2 budget, **Large only**, Yoruba at ≈18.6 epochs: minimum **1.709 at ≈571K steps**, rising to **1.779 at 1M** — **+0.070 nats**, with **18 sawtooth teeth** between 400K and 1M (each tooth an epoch boundary over the tiny corpus). The paper says overfitting "emerges even for the Large model after around 300,000 steps"; from pixels the curve is still descending at 300K (1.762) and 500K (1.721), so **300K is where the sawtooth becomes visible, not where the loss turns** — quote ≈571K for the turn.

**So: at what epoch count does it appear?** ≈**4.7 epochs is already enough at 13B** (Fig. 2b) and ≈**18.6 epochs is enough at 1.2B** (Fig. 3e); **4.7 epochs is not enough at 1.2B or 3.7B** (Fig. 2b). The threshold is not an epoch count — it is an interaction of epoch count × model scale × steps taken. The paper's own words: "overfitting only emerges with scale: Large shows no obvious overfitting, XL shows weak overfitting, and it becomes conspicuous at XXL size" (§5.1).

**Channel 2 — downstream task metric (the insensitive one).** Table 2 right, Large 1.2B: **N=1 → 82.2, N=5 → 81.5, N=10 → 81.8.** A 0.7pt spread, **non-monotone** (N=10 beats N=5), and the paper's own gloss is "the effect is small."

**What this means for tier C at 5.06×.** Two readings, both worth stating:
- *Reassuring*: the only published measurement of a low-resource corpus at ~5 epochs costs **0.7 pt on TyDi QA** at 1.2B, on a pool **67× smaller** than tier C.
- *Cautionary*: that measurement was taken at exactly the scale where the paper says the harm is invisible, and it is invisible in the downstream metric even at 250K steps while being clearly present in held-out loss at 13B. **H3's design inherits both problems**: 1B scale, and downstream-only metrics (IndicGenBench chrF, MILU). It should add held-out CE loss on the tier-C slice and pre-commit an escalation to 3B.

**Also relevant**: the paper cites Hernandez et al. 2022 for the claim that "even repeating 0.1% of data 100 times can be as harmful as halving model size," and argues overfitting in one language is likely to hurt across the board (§5.1) — a cross-lane contagion argument our §2 does not currently make.

### (b) Is an explicit epoch cap better than share/temperature allocation? **Yes, consistently, but by a small margin over a *well-chosen* temperature — and the cap is not where the gain comes from.**

Margins vs the tuned baseline τ=3.33: TyDi QA all-9 **+0.50 / +0.56 / +0.50** (Large / XL / XXL); TyDi bottom-4 **+0.89 / +0.80 / +1.01**; WMT21 chrF **+0.61 / +0.68 / +0.31**; XNLI translate-train **+0.4 / 0.0 / 0.0**; XQuAD EM **+0.6 / +0.3 / +0.2**; XNLI zero-shot +0.1. Margins vs the untuned τ=1: **+1.10 to +2.09** TyDi all-9, **+3.01 to +4.40** TyDi bottom-4, **+3.89 to +4.39** WMT chrF. Per-pair win rates (Fig. 6 right): UniMax best on **≈88 / 80 / 72%** of WMT pairs at Large / XL / XXL; restricted to non-English targets (Fig. 8) **≈90 / 85 / 90%**, with τ=1 never winning.

Read honestly: **against a tuned temperature the cap buys ~0.5 pt and sometimes exactly zero; against a badly chosen temperature it buys 1–4.4 pt.** Its real value is that it removes the τ search and bounds the worst case — and note that both the average WMT margin (+0.61 → +0.31) and the per-pair win rate (88% → 72%) **shrink with scale**, even as the paper's abstract says "the benefits persist as scale increases." The loss-side benefit does not shrink; the task-side benefit does.

**And the decisive attribution — the cap is a safety rail, not a source of gains.** Fig. 5 right gives the per-language sampling rates (1/8 budget, N=1), measured from pixels:

| lang | UniMax | τ=3.33 | ratio | cap binding? | Δ TyDi @XXL vs τ=3.33 |
|---|---|---|---|---|---|
| bn | **1.78%** | 0.87% | 2.05× | **no** — last language on the uniform plateau | **+2.9** |
| id | 1.78% | 1.06% | 1.68× | no | +0.8 |
| ko | 1.78% | 1.20% | 1.48× | no | +1.6 |
| fi | 1.78% | 1.43% | 1.24× | no | −0.5 |
| ar | 1.78% | 1.70% | 1.05× | no | −0.3 |
| **te** | **0.56%** | 0.52% | 1.08× | **YES — capped at N=1** | **−0.3** |
| **sw** | **0.50%** | 0.50% | 1.00× | **YES — capped at N=1** | **+0.4** |

The two languages where the cap actually binds (te, sw) receive essentially the same exposure as under τ=3.33 and gain essentially nothing. Every large gain belongs to a language on the **uniform plateau**. **The cap prevents the τ blow-up; the uniform leg produces the wins.** For a tier whose pool cannot fill its uniform share — which is precisely our tier C — UniMax degenerates to temperature sampling and confers no measured advantage.

**Which leg a sub-corpus lands in is a property of the budget, not of the method.** The condition in Algorithm 1 is `b_l > c_l × N`, so:

> **A sub-corpus is capped iff its unique pool `c_l` is below `b/N`, where `b` is the uniform residual share.** At N=1 the threshold *is* `b` itself.

That makes "bn is uncapped" a fact about mC4 at the 1/8 budget, not about Bengali. Three regimes, same algorithm:

| regime | N | budget | pool | uniform share `b` | threshold `b/N` | capped |
|---|---|---|---|---|---|---|
| UniMax ablations, 1/8 (refreshed mC4) | 1 | 581.6B chars | 28.8T chars | 8.61B chars | 8.61B | **53 of 107** rows; bn (34B) **uncapped** |
| UniMax umT5, 1× | 1 | 4.653T chars | 28.8T chars | 149.8B chars | 149.8B | **86 of 107**; **all 14 Indic capped**, hi included |
| **Our Indic lane** | **5** | **316B tok** | **275.9B tok** | **97.0B** | **19.4B** | **1 of 4 — tier C only** (A 64.0, B 44.9, D 162.0 all clear 19.4B) |

`EmnlpPaper`'s paper (Parmar et al., EMNLP 2024, 8B/300B) supplies the fourth and most instructive regime and is the reason to state the rule generally: at N=1 with a 300B budget over a 597.41B pool of 53 sources, `b` = 16.65B, so the uniform leg covers **only the 8 largest sources** and the cap binds for **45**, including **Hindi (2.60B pool → 0.867%) and Bengali (0.90B → 0.30%), both at exactly 1.00 epoch** — the inverse of UniMax's own regime, where bn sits comfortably on the plateau. Their two rates reproduce their Table 12 pools exactly under the rule above, which is an independent confirmation of it. See their brief for that paper's own conclusions; the load-bearing consequence here is only this: **our tier C is in the capped leg, which is the leg where UniMax measured no advantage** — so the cap is doing bounding work for us, not performance work, exactly as §4 concludes.

### (c) Does it distinguish native vs translated vs synthetic data for a language? **NO. Clean, useful negative — and better than silence, because the authors name it as out of scope.**

- **"synthetic" appears zero times** in the source (`grep -c -i synthetic main.tex` → 0).
- **"parallel data" appears exactly once**, in the Conclusion, as explicitly declared future work: "Future work is needed to test if UniMax confers gains in other settings, such as: (i) encoder-only or decoder-only models, **(ii) models trained with parallel data**, and (iii) models with dedicated parameters per language" (`main.tex:454`). So the paper does not merely omit translated/parallel data — it names it as untested.
- All training data is one kind: CommonCrawl web text, CLD3-detected, langid-confidence ≥0.95. There is no tiering by provenance, no native/translated split, no quality classifier at all beyond the language-ID confidence threshold and the bad-word filters. `n_l` is a raw character count.
- The only native-vs-translated distinction anywhere is in **evaluation design**, and it cuts in a useful direction: they choose TyDi QA because its questions are "written from scratch by native speakers in each language, ensuring culturally relevant content and **the absence of 'translationese'**," and they explicitly "avoid benchmarks... constructed in English and translated post-hoc to other languages" (§4.3). That is a strong stated prior that translated text is a *distinct and inferior* distribution — asserted, not measured, and about eval rather than training. It is directional support for keeping tier C small and for **not** letting Algorithm 1's uniform leg treat C like A.

**Consequence for us:** our tier A/B/C/D ordering gets **no** support from this paper, and the paper's uniformity principle actively argues against it. Our §2 must say that the cap is imported and the quality ordering is not.

### (d) Does it say anything about *when* in training multilingual weight should be served? **NO. Hard negative.**

`grep -io "curricul\|anneal\|stag\|schedul\|mid-train\|two-phase\|cooldown\|later in training\|order of"` over the full source returns **zero matches**. The sampling distribution `p_l` is computed **once, before training, from static character counts**, and never revisited. There is no staging, no phase, no ramp, no late-phase upweighting, no ordering claim of any kind. Nothing here supports or refutes our anneal at Indic 21.875%; **MAP-Neo's 25% → 8.5% remains the only quantitative precedent and it still points the other way.**

Two adjacent facts are the closest thing to a temporal claim, and both are about *duration*, not *ordering*:
1. **The penalty is a function of steps taken, not just epoch count.** Fig. 3(e) is the same τ, same model, same corpus as a 250K run, and only the longer run turns up (min ≈571K). Repetition damage accrues with optimiser steps.
2. **The right cap depends on the budget.** "The optimal setting of N likely depends on the character budget, as for large enough budgets, UniMax-1 will see vanishingly little of the lowest-resource languages" (§5.3). Fig. 3(f) is the evidence: at the 1/2 budget with N=1, Yoruba ends at loss 1.92 against τ=3.33's 1.71 — under-served, because one epoch of a 0.3B-char corpus is nothing against a 2.33T-char budget.

**That second point is the one genuinely actionable consequence for our anneal**: `N` must be recomputed per leg, because the leg's budget changes. If our anneal's Indic component preserves the A40/B30/C8/D22 split, then anneal tier C = 8% × 21.875% × 80B = **1.40B**, whole-plan tier C = 25.28 + 1.40 = **26.68B = 5.34 epochs**, and a declared cap of N=5 is **violated by the anneal**. If instead the anneal's Indic is drawn only from tier A's top-15% quantile plus tier-D ballast, as §5's reserve table implies (Tier-A verified Indic 9.6B; "1.8B in the anneal ballast" for D), tier C stays at 25.28B. **§2 or §5 must say which** — a reviewer who does this multiplication will otherwise find a cap the plan breaks in its own cooldown.

### (e) Does it report tokenizer behaviour / fertility across scripts, especially non-Latin? **Partly — vocabulary composition and token-length distribution, YES; per-language fertility, NO.**

**What it gives (Table 4, App. A — token frequency %, one vocabulary per sampling strategy, 256,000 subwords each):**

| script | τ=1 | τ=3.33 | UM1 4× | UM10 4× | UM1 1× | UM10 1× | mT5 |
|---|---|---|---|---|---|---|---|
| Latin | 67.0 | 54.0 | 56.3 | 47.9 | 50.2 | 49.5 | 46.6 |
| Cyrillic | 17.7 | 13.0 | 12.0 | 14.6 | 14.1 | 12.6 | 10.7 |
| Han | 3.2 | 4.3 | 4.9 | 4.2 | 4.5 | 4.0 | 7.2 |
| Arabic | 2.8 | 4.6 | 5.6 | 4.2 | 4.5 | 4.6 | 3.0 |
| Greek | 1.3 | 1.9 | 3.1 | 1.5 | 2.0 | 1.3 | 2.1 |
| Hangul | 0.8 | 1.5 | 2.1 | 1.5 | 1.8 | 1.4 | 1.7 |
| **Devanagari** | **0.5** | **2.2** | **1.9** | **3.0** | **2.9** | **2.6** | **1.3** |
| Thai | 0.3 | 0.9 | 1.2 | 1.0 | 1.3 | 0.9 | 1.8 |

The three stated levers (§4.2, App. A): **higher τ**, **smaller UniMax budget**, and **higher N** each allocate vocabulary more uniformly across languages — "fewer tokens from higher-resource language scripts (e.g. Latin), more tokens from lower-resource language scripts (**e.g. Devanagari**), and a shift towards shorter tokens." Devanagari is the paper's own worked example. Concretely: **raising N from 1 to 10 at the 4× budget takes Devanagari 1.9% → 3.0% (+58% relative)**, and UniMax-1 at 1× gives Devanagari **2.9% vs mT5's 1.3% (2.2×)**.

Token lengths, same table: UniMax vocabularies are **longer** than mT5's overall (10+ char tokens 7.5% for UM1-1× vs 2.7% for mT5; 4-char 15.4% vs 21.8%), attributed to mT5's whitespace pre-tokeniser (UniMax trains on raw text, no pre-tokeniser). mT5 also has far more punctuation tokens (4.2% vs 0.4%), attributed to low-quality non-language documents that the 0.95 langid threshold removes.

**What it does not give:** no tokens-per-word or tokens-per-character measurement on actual text for any language — i.e. **no fertility numbers**. Vocabulary *composition* is a proxy for fertility, not a measurement of it. There is no frozen-embedding condition anywhere, so our §2 hazard 1 is still not directly addressed.

**The transferable engineering fact for hazard 1**: the vocabulary is **256,000 subwords with byte-level fallback enabled, so unknown tokens are decomposed into UTF-8 bytes** (App. C). That is the standard mitigation for the uncovered-unigram loss spike our §2 hazard 1 describes, and our spec should name it alongside "Indic tokenizer coverage fixed pre-run."

---

## 4. The replacement question: keep our tier percentages, or replace them with an epoch cap?

**Answer: keep the four percentages, adopt the cap as the constraint that *derives and defends* them, and explicitly refuse Algorithm 1's uniform leg.**

**The arithmetic.** Algorithm 1 with pools A 64.0 / B 44.9 / C 5.0 / D 162.0 B tokens (total 275.9B) and lane budget **C = 316.0B**, swept over N:

| N | A verified | B unverified | C translated | D synthetic | tier-C epochs | budget filled? |
|---|---|---|---|---|---|---|
| **1** | 23.20% (1.00×) | 16.27% (1.00×) | **1.81%** (1.00×) | 58.72% (1.00×) | 1.00 | **NO — 275.9B of 316B; 40.1B short** |
| 2 | 34.21% (1.69×) | 28.42% (2.00×) | 3.16% (2.00×) | 34.21% (0.67×) | 2.00 | yes |
| 3 | 31.75% (1.57×) | 31.75% (2.23×) | 4.75% (3.00×) | 31.75% (0.62×) | 3.00 | yes |
| **2.53** *(the spec's declared cap)* | **32.00%** (1.58×) | **32.00%** (2.25×) | **4.00%** (2.53×) | **32.00%** (0.62×) | 2.53 | yes |
| 4 | 31.22% (1.54×) | 31.22% (2.20×) | 6.33% (4.00×) | 31.22% (0.61×) | 4.00 | yes |
| **5** | **30.70%** (1.52×) | **30.70%** (2.16×) | **7.91%** (5.00×) | **30.70%** (0.60×) | 5.00 | yes |
| 6 | 30.17% (1.49×) | 30.17% (2.12×) | 9.49% (6.00×) | 30.17% (0.59×) | 6.00 | yes |
| 10 | 28.06% (1.39×) | 28.06% (1.97×) | 15.82% (10.00×) | 28.06% (0.55×) | 10.00 | yes |

**Finding 1 — the cap reproduces our tier C almost exactly.** At **N = 5, tier C = 7.91%**, against our hand-chosen **8.00%**. A 0.09pp difference. Our weakest number turns out to be the output of a published algorithm at a cap value that same paper tested.

**Finding 2 — but the cap gets A, B and D wrong, and we should say so.** At N=5 Algorithm 1 sets A = B = D = 30.70%, i.e. it takes **9.30pp out of verified native** and hands **+8.70pp to synthetic**:

| Tier | Ours | Algorithm 1 @ N=5 | Δ |
|---|---|---|---|
| A verified native | **40%** | 30.70% | **−9.30pp** |
| B unverified crawl | **30%** | 30.70% | +0.70pp |
| C translated | **8%** | 7.91% | −0.09pp |
| D synthetic | **22%** | 30.70% | **+8.70pp** |

That is a strictly worse plan, and the reason is structural: UniMax's uniform leg is justified by **equity across languages** — "linguistic utility" (Blasi et al. 2022) and, in App. B, demographic utility over L1 speakers. There is no equity argument for uniformity across *quality tiers of one language family*. Our tiers are ordered by trustworthiness (verified native > unverified crawl > translated > synthetic); treating them as equally deserving is exactly the wishful accounting E9 punishes. **Import the cap; refuse the uniform leg; write down why.**

**Finding 3 — the useful form is the inversion.** The maximum tier-C share admissible under a declared cap `N` is `N × 5.0B / 316B`:

| declared N | max tier C | verdict |
|---|---|---|
| 1 | **1.58%** | starves the tier |
| 2 | 3.16% | |
| 3 | 4.75% | within OpenCoder's ~3.5-epoch practice |
| 4 | 6.33% | within Two-Phase's 6-epoch HQ ceiling |
| **5** | **7.91%** | **our number; the largest N UniMax tested below 10** |
| 6 | 9.49% | at Two-Phase's 6-epoch HQ ceiling |
| 10 | 15.82% | UniMax's largest tested N |
| **12.64** | **20.00%** | **the course composer's default — above every ceiling we hold** |

Two sentences fall straight out of that table. Our **8% ⇒ N = 5.06**, so "8% and a declared cap of N=5" is internally inconsistent by 0.06 epochs — **set tier C to 7.91% and the cap is exact**. And the composer's **20% ⇒ N = 12.64**, which is 2.1× Two-Phase's 6-epoch HQ ceiling and 26% beyond the largest N UniMax ever ran. §2's opening line gets to stop saying merely "not fundable" and start saying "requires 12.64 epochs on a 5.0B pool, above every published ceiling in this document's evidence base."

**Finding 4 — the N=1 row exposes a trap.** Our four tiers total 275.9B, which is **less than the 316B lane budget**. Algorithm 1 therefore terminates with 40.1B unallocated, and `normalize(U)` rescales every tier by 316/275.9 = **1.145×** — so "UniMax with N=1" on our lane would silently deliver **1.145 epochs, not 1.000**. Any port of this algorithm to a supply-poor lane must assert `ΣU == C` before trusting the cap. (Our lane-level figure, 316/276 = **1.14×**, is the same quantity computed honestly, and it sits below umT5's own head-language epoch counts.)

**Scale reach — is 5.0B inside their evidence?** No. **Smallest per-language corpus tested: Yoruba ≈0.1B chars ≈26M tokens** (ablation corpus) / **0.3B chars ≈75M tokens** (refreshed); smallest row of any kind `bg-Latn` **0.1B chars ≈25M tokens**. Tier C at 5.0B tokens is **67× larger than their Yoruba and 200× larger than their smallest row**, so applying N=5 there is extrapolation — **in the safe direction**, since the same epoch count over 67× more unique text is strictly less repetition. The extrapolation that is *not* safe is model scale: their N-sweep ran at **1.2B only**, and their central finding is that repetition harm grows with scale. Attach that caveat, not a pool-size caveat.

---

## 5. Figures — read from pixels

Rasterised from the TeX-source PDFs at 150 dpi (`figures/*.png`); several measured programmatically against their own gridlines. **No figure in this paper has error bars.** Every configuration is a single run; the paper never reports seeds or variance. Cite curve *shapes* and gaps ≥0.5 pt, not exact optima.

- **Fig. 1(a)** `pretraining_epochs.png` — "Number of epochs" (y, **broken axis**: lower panel ticks 0/1/2/3, upper panel ticks 50/100) vs "Language rank" (x, ticks 0/50/100, data to ~107). Four series: τ=3.33 1/8 (pink dashed), UniMax 1/8 (magenta solid), τ=3.33 1× (light-purple dashed), UniMax 1× (dark-blue solid). **Measured**: UniMax 1/8 rises 0.06 (rank 5) → 0.91 (rank 40) → **flat at 1.00 from rank ~60 to 106**; UniMax 1× reaches 1.00 by rank ~40 and stays flat. τ=3.33 1× hits **2.64 epochs at rank 40** and **100 epochs at rank 106** (max ≈101); τ=3.33 1/8 crosses 1.0 near rank ~63 and reaches **≈6.9 at rank 100, ≈11.7 at rank 106**. **Claim**: the cap is exact and flat; temperature diverges monotonically into the tail. **Note**: head languages under UniMax sit *below* one epoch — the cap is a ceiling, never a floor. Deterministic quantity, so error bars are not applicable.
- **Fig. 1(b)** `main_figure_color_coded.png` — "Pretraining sampling rate [%]" (y, **broken axis**: lower 0/2/4, upper 25/50) vs language rank. **Measured**: τ=1 spikes to ≈48% at rank 0 (Table 8: en 46.58%) and is under 1% by rank ~10; **UniMax 1× is a flat plateau at 3.24%** to rank ~20 then steps down; **UniMax 1/8 plateaus at 1.77%** to rank ~40 then declines. The 1× plateau matches Table 8's 3.22% exactly. The 1/8 plateau reads 1.77% here vs Table 8's **1.48%** because **Fig. 1 is the §4.1 ablation corpus and Table 8 is the refreshed 3.1.0 corpus** — the refresh grew the tail, so more languages clear the uniform threshold and the plateau falls. Do not mix the two. **Claim**: uniform above the cap, capped below it.
- **Fig. 2(a)** `loss_temp1.png` — held-out CE loss (y, ticks 2/3/4) vs pretraining steps [K] (x, 0–250). Six series (yo/en × Large/XL/XXL). All monotone. yo ends ≈2.50/2.30/2.18; en ≈1.38/1.28/1.20. **Claim**: at τ=1 the low-resource language is under-served and **model scale barely closes a ~1.0–1.1 nat gap**.
- **Fig. 2(b)** `loss_temp3.png` — same axes (y ticks 1.5/2.0/2.5/3.0). **Measured**: yo Large 1.768 monotone; yo XL 1.632 monotone (flat over the last 50K); **yo XXL minimum 1.579 at 188K → 1.650 at 250K, +0.071**, with visible steps at ≈160/195/225K. en all monotone (1.521/1.368/1.268). **Claim**: over-repetition damage appears only at scale — and **yo XXL ends worse than yo XL**, a scale inversion. Note the paper calls XL "weak overfitting" but from pixels XL does not turn up within 250K; its signature is flattening plus the sawtooth.
- **Fig. 2(c)** `loss_um1e.png` — same axes (y to 3.5). yo Large/XL/XXL ≈1.84/1.63/1.55, ordered correctly by scale, **no upturn, no sawtooth**; en ≈1.53/1.41/1.30. yo−en gap at XXL ≈0.25 vs τ=1's ≈1.0. **Claim**: N=1 closes the head–tail loss gap with no overfitting. **Caveat the paper states**: losses are **not comparable across sampling strategies** because each has its own vocabulary — compare shapes within a panel only.
- **Fig. 3(d,e,f)** `loss_temp1_1M / loss_temp3_1M / loss_um1e_1M` — 1M steps (= 1/2 char budget), **Large only**, two series each. (d) τ=1: yo 3.7 → 2.32, en 2.75 → 1.28, monotone. (e) τ=3.33: **yo minimum 1.709 at ≈571K → 1.779 at 1M (+0.070), 18 sawtooth teeth from 400K**; en monotone to 1.397. (f) UniMax: yo → 1.92, en → 1.42, monotone. **Claim**: enough steps make the tail overfit even at 1.2B. **Second, unstated claim visible in (f)**: at this budget N=1 leaves yo at 1.92 while τ=3.33 reaches 1.71 — one epoch of a 0.3B-char corpus is too little against a 2.33T-char budget, which is precisely §5.3's warning that optimal N grows with budget.
- **Fig. 4(a,b,c)** `scaling_tydi / _high5 / _low4` — "Average of EM and F1" vs "Number of parameters [B]" (ticks 1–13). **Three data points per line** (1.2 / 3.7 / 13 B) joined by straight segments; truncated y-axes (a: 80–84.5; b: 78.4–81.6; c: 82–88.6) that magnify small gaps. Values table in §2 above; all nine cells of each panel reproduce the corresponding per-language means of Table 7 to ≤0.04. **Claims**: (a) UniMax best at every scale; (b) τ=1 **overtakes** UniMax on the top-5 at ≈10B; (c) the low-resource advantage is large and does not decay.
- **Fig. 5 left** `tydi_xxl_per_lang.png` — grouped bars, XXL only, 9 languages, three methods. **Y-axis starts at 75, not 0** — visually exaggerates the differences. Values in §2. **Claim**: the win is concentrated in bn/id/ko; τ=1 wins en and ru.
- **Fig. 5 right** `tydi_lang_pretraining_proportion.png` — "Sampling rate [%]", **broken axis** (lower 0/2, upper 25/50). **Measured** (table in §3b): UniMax plateau 1.78% for en…bn; **te 0.56% and sw 0.50% fall below the plateau — the only two languages where the cap binds**. τ=1 en ≈47.7% (matches §5.2's "47.7%"). **This is the load-bearing panel of the paper for our purposes**: paired with Fig. 5 left it shows the gains track the *uniform* leg and vanish where the *cap* binds.
- **Fig. 6 left** `scaling_wmt.png` — chrF (y ticks 38–48 by 2) vs params. Values in §2. Three points, straight interpolation, no error bars. **Claim**: UniMax best at all scales; margin over τ=3.33 shrinks 0.61 → 0.31 as scale grows.
- **Fig. 6 right** `wmt_best_method_bar.png` — 100%-stacked "Best method [%]" (ticks 0/50/100) by Large/XL/XXL. UniMax ≈88 / 80 / 72%; τ=3.33 ≈10 / 20 / 25%; τ=1 ≈2 / 0 / 3%. Underlying n ≈ 25 pairs, so granularity is ~4%. **Claim**: broad benefit, not a few outliers — but UniMax's win *rate* declines monotonically with scale.
- **Fig. 8** `wmt_best_method_bar_non_en_target.png` — same construction, ticks 0–100 by 20, non-English-target pairs only. UniMax ≈90 / 85 / 90%; τ=3.33 ≈10 / 15 / 10%; **τ=1 exactly 0% at every scale**. **Claim**: the benefit is strongest where English is not the target, and the scale-decline of Fig. 6 right disappears.
- **Fig. 7** `representation.png` — wide bar chart, **log y-axis on both sides** (ticks 0.1, 0.3, 1.0, 3.2, 10.0, 31.6, 100.0, 316.2, 1000.0), one bar per mT5 language sorted ascending, drawn from the 1.0 line, coloured **European (orange) / Non-European (blue)**. Most underrepresented (left): **zh ≈0.16, pa ≈0.27, yo ≈0.29, bn ≈0.30, hi ≈0.31**, then ar, jv, ha, ig, te, es, su, ps, gu, ur, am, lo, pt, ta ≈0.95. Most overrepresented (right): eo and la clipped at 1,000, then haw/gd/mi/sm ≈316–1000, is/co/ga/mt ≈100–150. The left end is almost entirely blue; the right end almost entirely orange (Mann–Whitney U=566, p<1e−5). **Claim**: mT5's distribution over-serves European languages by up to 900× and under-serves large Asian/African populations by up to ~7×. **For us**: eight Indic languages (pa, bn, hi, te, gu, ur, ta, ml/sd) sit in the underrepresented half — Indic is the canonical under-served group. App. B also notes **Odia, 33M native speakers, absent from mT5 entirely**. Deterministic ratio, no error bars.

---

## 6. Draft insert for §2

> **SUPERSEDED — do not apply.** `SOLUTION.md` §2 has since been rewritten and already contains a stronger version of this insert, landing tier C at **4% / N = 2.53** rather than the 7.91% / N = 5 that this paper alone supports. The text below is retained as the record of what UniMax *by itself* justifies, and because three of its clauses are not yet in §2 and should be: the **inversion table** (max tier-C share = N × 5.0B / 316B, which is what kills the composer's 20% at N = 12.64), the explicit **refusal of the uniform leg** with its reason, and the **held-out-CE-loss addition to H3**. See the STATUS box at the top for the two FATAL defects in the rewritten §2.

Written in the spec's voice, scale caveat attached. Assumed slot: after the tier table, before "Real 78% / synthetic 22%" (both now changed in §2).

> **The tier-C factor is a declared epoch cap, not a taste call.** UniMax's Algorithm 1 (ICLR 2023, §3) allocates a fixed budget across sub-corpora uniformly subject to a hard ceiling of **N** epochs per corpus; run on our four pools (A 64.0B, B 44.9B, C 5.0B, D 162.0B) against the 316.0B lane, **N = 5 outputs tier C = 7.91%** — which is why C is 7.91% and not 8%, and why the composer's 20% is refused: at 5.0B unique, 20% **requires N = 12.64**, beyond Two-Phase's 6-epoch HQ ceiling, OpenCoder's ~3.5 and the largest N (10) UniMax ever ran. We adopt UniMax's cap and reject its uniform leg: uniformity across languages is justified by linguistic equity, which has no analogue across *quality* tiers, and applying it here would move 9.30pp from verified native to synthetic. **N = 5 is supported at 5 epochs but not at our scale**: UniMax's own sweep (N ∈ {1,5,10} → TyDi QA 82.2 / 81.5 / 81.8, Table 2) is **Large 1.2B only**, and the paper's central finding is that repetition damage grows with model size — Yoruba at ≈4.7 epochs is harmless at 1.2B and 3.7B but costs **+0.071 nats of held-out loss from 188K steps at 13B**, ending *worse than the 3.7B run* (Fig. 2b). Their smallest corpus is Yoruba at **≈75M tokens, 67× smaller than our tier C**, so the pool-size extrapolation runs in our favour and the scale extrapolation does not; **H3 therefore adds held-out CE loss on the tier-C slice and escalates to 3B if the 1B arm cannot separate.** The same paper is the first in this document to have touched Indic at all, and it sets the reference unit: **both disclosed multilingual builds that publish per-language Indic volumes serve Indic at exactly 1.00 epoch of their real Indic pool** — umT5 48.2B of 48.4B (Table 8, 1× column, 14 languages), and Parmar et al. 6.00B of 6.00B (EMNLP 2024, 8B, 9 languages) — in both cases *because the epoch cap binds, not because the share was chosen*. Measured the same way, our **§5 floor of 5.5% is 0.97 epochs** of the 113.9B real Indic pool and is therefore inside published practice, while **§1's 15.80% is 2.77 epochs** of that same real pool, or 1.15 if Sangraha's 162B synthetic is counted as Indic supply. **We state the 2.77 and defend the synthetic substitution on tier D's own evidence, rather than quoting 1.14× and letting the substitution pass unremarked.**

Two smaller edits it forces elsewhere:
- **§2 hazard 1** — replace "transfers by analogy only" with the real script evidence: Devanagari vocabulary share moves **0.5% (τ=1) → 2.2% (τ=3.33) → 2.6–3.0% (UniMax N=10)** vs **mT5 1.3%** (UniMax Table 4), and raising the epoch cap is one of the three named levers that shifts vocabulary capacity to tail scripts. Add **byte-level fallback on the 256k vocab** (App. C) to the mitigation list. Note it is still not a *fertility* measurement and still has no frozen-embedding condition.
- **§9 "no paper in the evidence base studied Indic"** — no longer true. Amend to: *no paper studies Indic **tiering**; UniMax covers 14 Indic languages as undifferentiated crawl and reports Bengali and Telugu downstream, and is silent on native vs translated vs synthetic (it names parallel data as untested future work).*

---

## 7. Follow-on citations that would further constrain low-resource multilingual mixture design

1. **Hernandez et al. 2022, `2205.10487` "Scaling Laws and Interpretability of Learning from Repeated Data"** — the source of UniMax's own claim that repeating **0.1% of data 100×** can be as harmful as **halving model size**, and the mechanism for repetition damage being a *whole-model* effect rather than a per-language one. **The single most valuable next read**: it is the repetition-scaling-law paper that would let us put a number on tier C's cost at *our* scale instead of borrowing a 1.2B TyDi delta. Coordinate with `ScalingDC` (2305.16264) — different paper, adjacent claim.
2. **Kreutzer et al. 2022, TACL "Quality at a Glance: An Audit of Web-Crawled Multilingual Datasets"** — the audit behind UniMax's Marathi statistic (only **40%** of mC4's Marathi bucket is well-formed Marathi). This is the direct evidence base for **tier B's** reliability and for our §2 hazard 2, and it audits Indic buckets specifically. Highest-value citation for the tier we currently defend with nothing.
3. **Blasi et al. 2022, ACL "Systematic Inequalities in Language Technology Performance Across the World's Languages"** — the "linguistic vs demographic utility" distinction UniMax builds its uniform leg on (App. B, Eq. 3). Relevant because *rejecting* UniMax's uniform leg for our quality tiers is a stronger argument if we can name what the uniformity was actually for.
4. **Chung et al. 2020, EMNLP "Improving Multilingual Models with Language-Clustered Vocabularies"** — same first author; the mismatch UniMax §3.1 warns about between the vocabulary-learning distribution and the training distribution. Directly bears on §2 hazard 1 and on our "Indic tokenizer coverage fixed pre-run" mitigation.
5. **Caswell et al. 2020, COLING "Language ID in the Wild"** — why the 0.95 CLD3 threshold exists, and the failure modes of language ID on low-resource and transliterated text. Bears on separating tier B from tier C, and on `hi-Latn`-style transliteration in our Indic pool.
6. **Wang et al. 2020b (differentiable data selection) and Jean et al. 2019 (bi-level validation-utility scheduling)** — the two learned-weight alternatives UniMax compares against in §2. If OPUS is going to reweight lanes online, these are the multilingual precedents for doing it against validation utility rather than a static share, and UniMax's stated objection (no repetition limit) is the constraint to carry over.
7. **Pfeiffer et al. 2022 "Lifting the Curse of Multilinguality"** — named in UniMax's own future work as the per-language-parameter alternative. Relevant only if we ever consider Indic-specific capacity instead of Indic-specific share.

---

## 8. Agreement and contradiction with the existing evidence base

- **EVIDENCE_MAP §7 "organic repeat bounded"** (Two-Phase 6 HQ / 8 math; OpenCoder ~3.5; survey "a few times"): **agrees and extends**. UniMax's N ∈ {1,5,10} finds no cliff at 5 or 10 downstream (0.7pt spread, non-monotone), and adds the missing variable — harm scales with *model size* and *steps*, not with epoch count alone. It is the first entry in the band that measured a **low-resource, non-English** corpus.
- **EVIDENCE_MAP §2 "all nine papers are silent on Indic"**: **contradicted**. Correct the claim (see §6 above).
- **`synthetic` (Demystifying) rephrase ceiling <50%, textbooks ≤3%**: **orthogonal, no conflict.** UniMax has zero synthetic data and never mentions it; nothing here relaxes or tightens tier D.
- **`midtrain-survey` MAP-Neo Chinese 25% → 8.5%**: **untouched.** UniMax is entirely static and offers no staging evidence in either direction; H5 stands unaided.
- **`pref-curriculum` "a 100M model's PPL on Devanagari is a tokenizer artefact"**: **supported mechanistically.** UniMax Table 4 shows Devanagari vocabulary share swinging 0.5% → 3.0% purely with the sampling strategy, at fixed vocab size — so per-token loss on Devanagari is not comparable across runs whose vocabularies differ. UniMax states the same caveat about its own Fig. 2/3 ("loss values are not directly comparable across sampling strategies due to the difference in vocabulary").
- **`two-phase` "English 5-bucket CC quality classifier is not a verified Indic rule"** (our §2 hazard 2): **supported**. UniMax's only quality gate is language-ID confidence plus bad-word lists, and its Marathi statistic shows crawl language buckets are ~40% reliable for an Indic language. A quality classifier is not the first problem with tier B; language identity is.
- **Error bars**: adds to the tally. **Zero error bars in this paper**, single run per configuration, no seeds reported, plus a **transposition defect in Table 7's Avg column** (§2). Treat sub-0.5pt gaps as noise.
- **`EmnlpPaper` (Parmar et al., EMNLP 2024, `2407.06380`) — external validation plus one same-direction caution.** It is an independent third-party application of Algorithm 1 at **8B / 300B**, reproduced from their published weight figures to ±0.05pp, so UniMax's algorithm is confirmed implementable as written outside Google. Its English N-sweep (19–20 sources, 1219B pool, 300B budget) runs **N=1 / 2 / 4 → LM-Eval 67.14 / 66.50 / 66.61 and MMLU 28.30 / 28.00 / 26.60**: same direction as UniMax's N=1 > N=5 ≈ N=10, but **a larger penalty (−1.70 MMLU at N=4) at 6.7× the model scale**, which is what UniMax's own scale-dependence predicts and a second reason H3 should not be trusted at 1B alone. **Cite it as direction, never as a clean effect size**: that paper offers two different explanations for the same result (§5.2.1 blames repetition, App. E blames the widening uniform leg), so repetition and uniformity are confounded in it, and the sweep is English MMLU rather than a low-resource metric. Their multilingual arm ran **N=1 only**, so it adds no independent evidence on the value of N.

---

## 9. What not to overclaim

- **Do not say UniMax validates 5 epochs at our scale.** The N sweep is **Large 1.2B only**, and the paper's own result is that the harm is invisible at 1.2B and conspicuous at 13B. Quote the 0.7pt as a 1.2B TyDi QA result and attach the scale caveat every time.
- **Do not say UniMax validates repeating a 5B-token pool.** Their largest per-language corpus is English; their *smallest* is ~25–105M tokens. Nothing in the study is at 5.0B. The extrapolation is favourable but it is still an extrapolation.
- **Do not attribute the low-resource gains to the cap.** Fig. 5 (both halves) shows the gains belong to the uniform leg; where the cap binds (te, sw) the gain is −0.3 and +0.4.
- **Do not claim the epoch cap is a large win over temperature sampling.** Over a *tuned* τ=3.33 it is +0.5 TyDi and 0.0–0.6 on XNLI/XQuAD, and on XNLI translate-train it exactly ties at XL and XXL. The large numbers (+3 to +4.4) are all against τ=1, which nobody would choose.
- **Do not port the uniform leg to our quality tiers.** It moves 9.30pp from verified native to synthetic and its equity justification does not transfer.
- **Do not quote Table 7's "Avg" column.** Four of nine cells disagree with the mean of their own row, as two exact transpositions. Use Figure 4.
- **Do not treat this as a decoder-only or a curriculum result.** Encoder-decoder, span corruption, mT5 architecture, static distribution; §7 names decoder-only, parallel data and per-language parameters as untested.
- **Do not mix the two corpora.** Figs. 1–6 and Tables 5/7 use the §4.1 filtered mC4 (Yoruba ≈0.1B chars, 1/8-budget plateau 1.77%); Table 8 and Table 3 use the refreshed 3.1.0 corpus (Yoruba 0.3B chars, 1/8-budget plateau 1.48%). Numbers do not transfer between them.
