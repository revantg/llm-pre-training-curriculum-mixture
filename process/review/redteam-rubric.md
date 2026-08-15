# Red-team review: `SOLUTION_v3.md` against the assignment rubric

**Reviewer role:** assignment grader + hostile reviewer in the room.
**Target:** `SOLUTION_v3.md` (238 lines, 26,901 bytes).
**Rubric:** `local://rubric.md` (R0–R8 / E1–E11), derived from `assignment.json → descriptionMarkdown` (3,300 chars, verbatim) and `lecture_notes.md §11`. `rubricJson` is empty; the prose **is** the rubric. maxPoints **500**.
**Evidence base:** nine paper briefs in `papers/*/brief.md`, `papers/EVIDENCE_MAP.md`, and the course's own widget source (`widgets/widget_1`, `_6`, `_7`, `_9`).

**Headline:** **≈345 / 500.** The evidence work is genuinely strong — I recomputed every number and most of them are exact to the decimal — but four of the eight named requirements are unaddressed or broken, two table sums do not close, the protected floor is not actually fixed, and ~25% of the document is padding at the same time as two twice-stated requirements are entirely absent. Full table and score reasoning at the end.

---

## 0. Requirement-set correction (read this first)

An earlier version of `local://rubric.md` asserted the assignment text was truncated with `…` in the Axiom source and that R1–R5 was the complete recoverable requirement set. **That was wrong**, and it mattered.

```
json.load(assignment.json)['descriptionMarkdown']  →  len 3300, count('…') == 0
paragraph 2 = 1272 chars on one line, paragraph 5 = 1877 chars on one line
```

The truncation was the `read` tool clipping display lines at 768 chars. The recovered tail carries **two named requirements and three evaluation criteria** that a five-requirement grading would have silently forgiven:

> "…it declares the anneal reserve that will be held back for the cooldown, **and it lays out the difficulty and reasoning-length bands with a concrete example for each. And it commits to justifying these numbers through small proxy runs at the one-billion and three-billion scale** before any of them is trusted at full scale…"

> "…**a plan that quietly hands a large share to a lane that has almost no real data behind it will lose marks** for exactly the wishful accounting this session exists to prevent… and it **lays out the difficulty and reasoning-length bands with a real example at each level**. The thing that separates a good plan from an excellent one is whether it is **written as a testable hypothesis**, so the highest marks go to the person who **specifies a concrete proxy experiment at the one-billion or three-billion scale and names the metric that would confirm or refute their mixture**, and the very highest go to the one that **actually runs that proxy and brings the numbers back**."

Consequence: **R6 is stated twice** (once in each paragraph) and is therefore weighted twice — and `SOLUTION_v3.md` scores zero on it. R8 is also real. This is graded against the corrected R0–R8 / E1–E11.

---

## 1. What is actually right (stated first, because it is load-bearing for the score)

I verified every number the spec attributes to a paper. The following are **exact** against the briefs, and a reviewer pushing on them will lose:

| Claim | Verdict |
|---|---|
| Two-Phase: natural CC is 64.44% Low; zeroing Low lifts MMLU 42.94 → 56.10 (Tables 16–17) | exact |
| Two-Phase: order alone +3.4 avg; GSM8K 30.86→40.33; code 35.55→38.33; MMLU 56.49→56.28 (Table 4) | exact |
| Two-Phase epoch ceilings: 6 HQ crawl (48.3/51.2/55.4/**56.1**/55.7), 8 math, 12 hurts | exact |
| OpenCoder: ~75% exact dupes; file 32.74B (2.4%) vs repo 99.47B (7.5%); 52B hidden; chunk −0.04B | exact |
| OpenCoder: `stars>=5` → lower loss, HumanEval ~0.12 vs 0.18, MBPP ~0.14 vs 0.20 (Figs 10–11) | exact |
| OpenCoder Fig 9: HumanEval stalls ~0.33 vs climbing ~0.47, gap never closes; 84/16; 2.71B unit-tested | exact |
| Dataset-Decomp: MDQA-10 0.8 → **20.8** → 21.2 → 20.4; missing D12/D13 → MDQA-20/30 = 0.0–0.4 | exact |
| Dataset-Decomp: 9.4%→25% at 8192 moves MDQA-avg 21.9→22.1 — and the brief agrees this **is noise** | exact, correctly labelled |
| Dataset-Decomp Table 2: MDQA-30 19.6→24.6, avg 23.0→28.0; Shrink −3.5/−3.4; Grow-P2 1→8 cycles 25.9→28.0, CSR 60.9→62.8 | exact |
| Dataset-Decomp Table 5: +2.9/+3.4, 244 vs 304 ms; DM 51.5→52.4, 27.5→27.1, MDQA-30 20.5→16.0; RoPE +5.4/+4.8 | exact |
| Dataset-Decomp: RefinedWeb 9.4% at 8192, 22.9% ≥4k; Alg 1 empty-bucket quote | exact |
| Spark Joy: 50/100/200/300B sweep; MMLU peak 43.19@100B; Core Avg 39.32@200B; **no point below 50B** | exact |
| Spark Joy: filtered web held at 30% (0.82×) "to prevent a large distribution shift"; bulk 34.35→0 | exact quote |
| Spark Joy: Domain-Specific 0.89 ep / Code 1.12 ep; 30% arm is where the reserve first crosses 1.0 **and** where MMLU/WK/Commonsense/RC/CoreAvg regress | exact, correctly hedged as co-occurrence |
| Spark Joy sans-math: MMLU 29.71 vs 35.69 (−5.98), RC 26.48 vs 37.02 (−10.54), CoreAvg −2.83, from a 100B leg | exact |
| Spark Joy ½·L1 = 41.1%; OpenCoder ≈16% | exact, and the spec's own 19.5% uses the **same** metric — method-consistent |
| Survey Cluster A: 1.96 / 1.48 / 3.85 / 4.00 / 4.76 / 1.96%; Cluster B: 9.03 / 11.11 / 14.08 / 16.67 / 51.28% | all eleven exact |
| Hunyuan-Large "5% of the highest-quality pre-training tokens"; **8×** stricter than 40% | exact quote — and 40/5 = 8 **corrects** the internal brief's "10×" |
| Llama 3 probe: 50%-trained, LR→0 over 40B, 30/70; +24.0% GSM8K / +6.4% MATH at 8B, negligible at 405B | exact quotes |
| OLMo 2 §III-C "not strictly necessary to have a large proportion… just that domain-specific data is present"; 19 probes / 130B | exact |
| CLIMB: 62M 60.11 vs 350M 60.41; 64+32+16 = 112 at 4:2:1; RegMix 59.37 / DoReMi 59.16 / Random 57.93; C20 → 0; top-3 ≈64% vs one cluster at 43%; checklist Q7 = No | all exact |
| Pref-Curriculum: ArXiv 88/12, GitHub 66/34, Wikipedia 14/86; "does not skew" quote; Spearman **0.41**; S-shape `1/(1+exp(10(p−0.5)))`, 43.9% band, Z-shape −1.1; flat for ~35%, worse loss for ~40% | all exact |
| Collapse: a.s. collapse, log-in-real bound, K=1/5/10 → T = 17/95/216, 20/80 ten indistinguishable gens | all exact |
| Demystifying: rephrase <50% converging ~30%; textbooks ≤3% at 50B, ~0% below 10B; App D.2 uncovered-unigram loss spike | exact |
| FLOPs: 6·120e9·40e9 = 2.88e22 vs 6·120e9·2e12 = 1.44e24 = 1/50; a dozen ≈ 24% of one run | exact |
| Agentic inventory: 150+120+90 = 360M long-traj; 80+60+50+30+25+22 = 267M short; total 627M ≈ 0.63B; 4 ep = 2.508B = 0.125% of 2T; 40 + 4.96 = 44.96B; 94.4% generated; 4.96/0.627 = 7.91 ep, 4.96/0.360 = 13.78 ep | every figure closes |
| Indic tiers: 126.4/64 = 1.975; 94.8/44.9 = 2.111; 25.28/5 = 5.056; 69.52/162 = 0.429; 78/22 real/synth; default C 63.2/5 = 12.6× | every figure closes |
| Anneal composition: 60 + 12 + 10 + 8 + 5 + 2 + 3 = 100; tokens 48+9.6+8+6.4+4+1.6+2.4 = 80.0; derived mixture sums to **exactly 100.00** | closes |
| §1 verdict labels (`covered` / `repeat` / `must generate`) | match `widget_1.classify()` (≤1×, ≤4×, >4×) exactly on all seven lanes |
| §8 "what this plan does not have evidence for" | the single best E2 move in the document; all six bullets check out |

**Nine papers, ~70 attributed numbers, two misquotes and one mis-sourced citation.** That is a high hit rate and it should be said plainly before the attack. The failures below are concentrated in the spec's *own* arithmetic and its *own* structural commitments — not in its reading of the literature.

---

## 2. FATAL findings

Ranked by how fast a grader hits them.

### F1 — The §1 share table does not sum to 100, and the spec says it does
```
33.9 + 24.0 + 15.8 + 11.5 + 8.5 + 4.5 + 2.0 = 100.2
```
Line 24: *"they sum to 100.0%."* False as printed. The underlying exact shares (33.85 / 23.95 / 15.8 / 11.45 / 8.5 / 4.45 / 2.0) do sum to 100.0, and the demand column sums to exactly 2000B — so this is four independent round-half-ups (`.85→.9`, `.95→24.0`, `.45→.5`, `.45→.5`) each adding 0.05pp. **It is still fatal:** R1's entire content is "a share for every capability slot", and the first thing any grader does to a share table is add it up. Fix: print one decimal honestly or state "shares shown to 2 s.f.; exact shares in §6".

### F2 — The §6 anneal row sums to 97 under a header claiming 100
```
20 + 22 + 15 + 3 + 22 + 9 + 6 = 97
```
Line 152: *"Each row sums to 100%."* Seed/General/Reasoning/Long-context all sum to 100 (verified). The anneal row is 3 short, because §4's eighth component — **"Verified synthetic + textbooks 3.0%"** — has no column in the §6 table. So the anneal appears in two places with two different compositions and one of them is missing a bucket. This is the direct answer to *"does §4 match §6?"*: **no.**

### F3 — "The two changes from the course preset" is six changes, and the funding story does not close
Course main preset vs spec, exact:

| | code | agentic | reason | long | indic | stem | web |
|---|---|---|---|---|---|---|---|
| course | 24 | 2 | 6 | 6 | 16 | 12 | 34 |
| spec | 23.95 | 2.0 | 8.5 | 4.45 | 15.8 | 11.45 | 33.85 |
| Δ | −0.05 | 0 | **+2.50** | **−1.55** | −0.20 | −0.55 | −0.15 |

Six lanes move, not two. And §1 says the long-context cut *funds* reasoning — but long-context releases **1.55pp** while reasoning takes **2.50pp**. The missing **0.95pp = 19B tokens** is taken silently from Indic (−0.20, a *protected* lane), STEM (−0.55, the lane the spec's own confidence table calls "0.92× — almost no headroom"), web and code. This is E9's named failure mode in miniature: a share moved quietly. One sentence fixes it; its absence is a self-inflicted wound on the document's single most-scrutinised paragraph.

### F4 — The 8% floor is not fixed, is non-binding as written, and the two readings differ by 255×
§5: *"8% of every iteration's accepted tokens is reserved for **Indic + agentic + reasoning**"* — i.e. **aggregate**. Never resolved, never split per lane, and never stated whether agentic's 2% share sits inside or outside it.

**Aggregate reading — the floor never binds anywhere:**

| stage | indic + agentic + reason |
|---|---|
| Seed | 20% |
| General | 23% |
| Reasoning | 30% |
| Long-context | 29% |
| Anneal | 43% |
| main-run average | **26.3%** |

The minimum is 20%, i.e. 2.5× the floor. Indic alone (15.8%) satisfies it. So OPUS can drive **agentic and reasoning to zero** and the floor is still met — which is precisely the failure the floor exists to prevent, and precisely CLIMB's C20 → 0 result that §5 cites as the reason the floor must be a hard constraint. **The clause the spec argues hardest for is the one that protects nothing.**

**Per-lane reading — infeasible by 255×:** an 8% real-token floor on agentic over 2T is 160B real tokens against 0.627B unique = **255 epochs**. Impossible.

R4's verb is *"fixes"*. A number that is ambiguous between "vacuous" and "impossible" is not fixed. **This is the single highest-value fix in the document and it costs one table row:** e.g. Indic 5% / reasoning 2.5% / agentic 0.5%, aggregate 8%, all real, and note that agentic's real floor at 0.5% of accepted tokens is itself 10B real from 0.627B unique — so state explicitly that agentic's floor clause is satisfied by *verified generated* trajectories and that only Indic and reasoning carry real-token obligations.

### F5 — §5's "must be real tokens" contradicts §3's "~94% of the lane is generated"
§5 row 4: *"It must be **real tokens**."* §3: total agentic exposure 44.96B of which unique real is 0.627B (**1.4%**), or 2.508B at the 4-epoch ceiling (**5.6%**). The two clauses are jointly satisfiable only under an aggregate floor in which agentic contributes ≈0.03% real and Indic/reasoning carry the rest — a reading the spec never states. As written, §3 and §5 contradict each other about the same lane.

### F6 — §7's kill criterion crosses a floor the spec and the course both declared
§7.5: *"Agentic → **0.5%** if the agentic proxy does not beat a format-only baseline."*

`widget_1_mixture_composer.html` line 284: `{key:"agentic", name:"Agentic / tool-use", color:"#7b61ff", floor:2}` — and `normalize()` refuses to let any lane go below its floor. **2% is a course-given hard floor, not a spec choice.** Dropping to 0.5% crosses it, and also crosses the §5 protected floor the document spent a full section fixing. The spec neither acknowledges the conflict nor states that the kill requires releasing a course constraint. This is the direct answer to *"do the §7 kill criteria contradict an earlier commitment?"*: **yes.**

Note the irony: the *reason* to keep 2% is exactly this hard floor, and §3 buries it as "the composer floor encodes a capability commitment" instead of stating the mechanical fact that the slider cannot go lower.

### F7 — §4's top-5% reserve quantile destroys §4's own sub-1-epoch safety argument
The epoch figures are correct against **whole-lane** supply — I reproduce all four:

| lane | anneal tokens | ÷ whole lane | spec |
|---|---|---|---|
| Indic | 21.48% × 80 = 17.18B | ÷276 = 0.0623 | 0.062 ✓ |
| reasoning | 15.10% × 80 = 12.08B | ÷85 = 0.1421 | 0.142 ✓ |
| long-ctx | 2.67% × 80 = 2.136B | ÷100 = 0.0214 | 0.021 ✓ |
| STEM | 8.87% × 80 = 7.096B | ÷250 = 0.0284 | 0.028 ✓ |

But 16 lines later: *"the reserve is therefore selected by a **top-5% quality quantile within each lane**."* Against a top-5% pool:

| reserved component | tokens | top-5% pool | epochs |
|---|---|---|---|
| Tier-A verified Indic | 9.6B | 5% × 64B = 3.20B | **3.00** |
| Long reasoning traces | 8.0B | 5% × 85B = 4.25B | **1.88** |
| Long agent trajectories | 4.0B | 5% × 0.36B = 0.018B | **222** |
| Algorithmic code | 6.4B | 55.0B | 0.12 |
| HQ STEM | 1.6B | 12.5B | 0.13 |

The two largest reserve components land at **1.9–3.0 epochs** — past the 1.0-epoch line that the *same paragraph* cites Spark Joy to say is where MMLU, World Knowledge, Commonsense, Reading Comprehension and Core Average all regress. The safety argument and the selection rule are computed on different pools.

**Corollary that bites R5 harder:** if the anneal's Indic is priced against the whole 276B lane, it is not *held back* — it is ballast at a higher weight. The epoch table proves the reserve is safe by assuming the reserve is not a reserve.

### F8 — Spark Joy's Language Understanding numbers are attributed to the wrong axis
§4: *"Language Understanding was still negative at every phase length (−0.47 / −1.11 / −1.44 / −1.17 **on LAMBADA / HellaSwag / Winograd / WinoGrande**)"*.

Source (Table 6): those four numbers are the Language Understanding **category** deltas at the four *phase lengths* — 5% / 10% / 20% / 30% (50 / 100 / 200 / 300B). LAMBADA, HellaSwag, Winograd and WinoGrande are the category's four constituent tasks, and Spark Joy publishes **no per-task numbers for them at all**. The spec has fused an x-axis into a task list. The underlying finding (LU negative at every length) survives; the presentation is a misquote a reviewer who has read the paper will catch in one glance.

### F9 — MiniMax-01's weight interpolation is cited as "Published analogue" but is unpublished
§6 seam control: *"**Published analogue**: MiniMax-01 uses linear interpolation of source-specific weights across mixture transitions."*

The mid-training-survey brief flags this exact string as existing **only as commented-out LaTeX in the arXiv source** of the survey, absent from both the rendered PDF and the HTML, with the instruction to cite the primary (2501.08313) instead. The spec cites neither the survey section nor the primary, and calls it "published". Same class of error as `2503.19206` (below): a citation the evidence base cannot support in the form given.

### F10 — "Why 2T" contradicts itself in one sentence
Line 8: *"it is **above** Chinchilla-optimal for 120B (**~2.4T is compute-optimal**; we are deliberately near it rather than 5–10× past it)"*.

120B × 20 tok/param = 2.4T. **2.00T is 0.83× compute-optimal — below, not above.** The overtraining citation (`2503.19206`, "harder downstream tuning") is then load-bearing on a premise the same parenthesis refutes; at 0.83× Chinchilla there is no overtraining to price. Compounding: `2503.19206` is not one of the nine papers — it appears only as a follow-on pointer in the survey brief, its result is at ≤3B / ≤3T, and the brief's own framing of it ("at 2T on a 120B model we are far past Chinchilla") is itself the error the spec inherited.

### F11 — §6 says long-context is cycled; §6's own table end-loads it
§4/§6: *"long-context exposure is **cycled through the whole main run rather than saved for the end**."* The table says otherwise:

| stage | long % | long tokens | share of the 89B lane |
|---|---|---|---|
| Seed (200B) | 1 | 2.0B | 2.2% |
| General (700B) | 2 | 14.0B | 15.7% |
| Reasoning (600B) | 3 | 18.0B | 20.2% |
| Long-context (500B) | 11 | **55.0B** | **61.8%** |

**61.8% of the curated long-context lane is in the final 25% of the run; 18% is in the first 45%.** That is a monotone end-load — the exact shape the quoted Dataset-Decomposition sentence names as the failure mode ("if we only see long sequences toward the end of training, long sequence learning occurs only when the learning rate is too small"), and the shape whose fix (`Grow-P2` ×8) the spec cites approvingly two paragraphs earlier.

Charitable reading: the *length buckets* from packing are cycled while the *curated lane* ramps — those are two different schedules and both are legitimate. But the spec never separates them, so as written §6 contradicts itself and its own citation. One sentence fixes it.

### F12 — §7's long-context floor is defended by a result about a different object
§7.5: *"Long-context stays ≥4% regardless, because **0% is the one setting proven catastrophic**."*

The catastrophic setting in Dataset Decomposition is a length mixture with **no D12/D13 buckets** (MDQA-20/30 = 0.0–0.4, Table 1 rows "≤2k" and "Mid"). It is not a run with a 0% curated multi-document lane. And §6 argues at length that natural packing supplies those buckets for free — 9.4% of a 4.5T web pool ≈ 423B of 8k-contiguous tokens. So **by the spec's own argument the curated lane could go to 0% without entering the catastrophic setting.** The declared floor is defended by a citation about the packing axis, not the lane axis.

### F13 — Tier C is labelled "repeat" where the course's own classifier says "must synthesize"
`widget_1.classify()`: `demand ≤ supply` → covered; `demand ≤ 4×supply` → needs repetition; **else → "supply-limited, must synthesize"**. §1 adopts these three labels exactly and correctly on all seven lanes. §2 then prices tier C at 25.28B against 5.0B = **5.06×** and calls it *"Repeat"*.

By the course's own threshold, 5.06× is **must synthesize**. E8's exact words are *"says plainly where a share can only be reached by repeating data or by generating it"* — and the spec, having imported the classifier, silently departs from it on the one tier it also nominates as its #2 attack surface.

### F14 — The long-context lane's named job is not suppliable by its own inventory, and 60% of it is the packing §1 rejects
`widget_9` long-context group is exactly two entries:
- **Repo-packed code (32K+)** — 60B — "whole repositories packed into 32K+ token sequences"
- **Book-length corpora (packed)** — 40B — "long documents and books packed to fill the context window"

Total 100B = the course's `longctx: 0.1` ✓. But:

1. §6 asserts *"the curated lane's distinct job is **multi-document reasoning**, which web spans do not provide."* **Neither inventory entry is multi-document.** Both are single-repo or single-document packs. The lane's stated reason for existing has no supply behind it, and MDQA — the benchmark §1 assigns it — is a multi-document benchmark.
2. **60% of the lane is repo-level packed code** — while §1 spends a whole subsection arguing, from OpenCoder Table 9 / Fig 8, that repo-level packing "hides 52B character-identical tokens" and loses HumanEval and MBPP to file-level at every matched budget. The spec adopts file-level dedup for code and then builds the majority of its long-context lane out of the packing it just rejected, without reconciling the two.

Neither point is addressed, and both are invisible in the document because **R3's requirement to name the datasets is not met** — the spec never prints "Repo-packed code (32K+)". Naming the inventory would have surfaced the contradiction.

### F15 — Seam count is wrong
§6: *"Every stage boundary and the anneal seam is blended over a 20B-token warmup band (1% of the run per seam, **5 seams**)."* Five stages (Seed / General / Reasoning / Long-context / Anneal) have **four** internal boundaries, and "the anneal seam" *is* the Long-context→Anneal boundary — so it is double-counted. 20B × 4 = 80B (4% of the run), not 100B (5%).

Unremarked consequence: a 20B band at the anneal entry is **25% of the 80B anneal leg**, so the first quarter of the reserve is spent at partially-main proportions. The reserve is materially smaller than 80B and the spec never accounts for it.

---

## 3. WEAK findings

| # | Finding |
|---|---|
| W1 | **FIM is cited at the wrong setting.** The survey sentence ("multiple span-prediction opportunities from a single sample… late-stage training where high-quality data is scarce") is about *code* fill-in-the-middle; DeepSeek-V3 is the only surveyed run using it, on code. Nothing in the survey concerns trajectories. Worse, FIM's suffix-conditioning would let the model see **later tool observations** while generating an earlier plan — which directly contradicts §3.6's own masking rule ("tool observations masked… training on observations teaches the model to invent tool results"). Calling it *"the one published mechanism for stretching a scarce lane"* transplants a code result onto agent traces. |
| W2 | **"measured rephrase ceiling (best ~30%)".** Demystifying's fine grid is exponential and **skips 30%** (points at 20% and 50%); ~30% is interpolated from 20-vs-50 plus a coarse 33% cell. Drop the word "measured". |
| W3 | **Collapse's 50%/80% real figures are a toy.** 8-layer / 256-dim char-level nanoGPT, vocab 65, 2000 steps, one Shakespeare play. Cited twice (§3.4, §5) as floor evidence for a 120B run with no scale statement — and §8's error-bar paragraph does not cover it. The transferable claim is the *shape* (no real ⇒ monotone drift; real every generation ⇒ plateau), which is what the theorem gives anyway. |
| W4 | **"the budget kindest to scarce supply."** Of the composer's four run sizes (1 / 2 / 5 / 10T), **1T is kindest** — the agentic gap would be 20B vs 0.63B. The superlative is refuted by the sentence's own logic. 2T is the composer default (`runSize = 2`), which is the honest defence and is already given. |
| W5 | **"the weighted time-average reproduces §1 within 0.6pp on every lane."** Over the main run it reproduces §1 **exactly** — I get 33.85 / 23.95 / 15.8 / 11.45 / 8.5 / 4.45 / 2.0, deviation **0.00pp on all seven lanes**. The 0.6pp is only true against an unstated 2080B denominator (web −0.58). A hedge that understates the document's cleanest piece of arithmetic and invites a reviewer to look for a 0.6pp error that does not exist. |
| W6 | **Dataset-Decomp Fig 8 is confounded.** The two arms differ in **both** packing and curriculum, at LR 1e-2 with clipping disabled, n=1. "Short-first length ordering suppresses early instability" is one of two entangled variables; the brief says so explicitly. |
| W7 | **CLIMB's proxy transfer is stretched 2000×.** 62M ≈ 350M was measured for a **1B** target, in **continuous** pretraining on a 10T phase-1 foundation, with 40B/400B targets. §7.1 reads it as licensing a 62M ranking pass for a 2T **from-scratch** 120B run. §6 correctly cites CLIMB's own §6 warning against copying continuous behaviour into from-scratch — which makes §7.1's use inconsistent with §6's use of the same paper. |
| W8 | **Selective on the anneal length.** §4 is right that Two-Phase's 40% is Cluster B and a different object. But it never states that **Spark Joy's own recommendation is 10–20% of the run = 200–400B at 2T** (2.5–5× the chosen 80B), nor that OLMo 2's own framing is *"5–10% of training FLOPs"* and includes a **300B (6%)** arm alongside the 50B and 100B ones the spec quotes. Quoting a paper's data while omitting its stated conclusion is the attack, and it is easy to pre-empt in two clauses. |
| W9 | **§1's Indic row counts synthetic as unique supply.** 316B demand ÷ 276B = 1.14× "repeat" — but 162B of that 276B is Sangraha **synthetic**. Real-only: 316 ÷ 113.9 = **2.77×**. §2 makes it recoverable (64 + 44.9 + 5.0 = 113.9B real), but E7's word is *"real supply"* and §1's row is what a grader reads. (Mitigating: 0.276T is the course's own `SUPPLY_T` constant, so the spec is using the number it was given.) |
| W10 | **§4's table has an "Epochs on unique" column containing seven em-dashes.** A header with no data, in the document's most contested table — and the data exists three lines below in prose. |
| W11 | **§4 vs §6 rounding drift on the numbers R5 depends on.** Agentic 6.2% → 4.96B (§4, §3) vs 6% → 4.8B (§6); Indic 21.48% (§4) vs 22% (§6). Small, but the anneal is the one leg where the spec asks to be trusted on tenths of a percent. |
| W12 | **Tier D's provenance claim is asserted, not established.** §2 says tier D is legitimate *"only as rephrased/translated expansion of real Indic text"*. `widget_9` describes the source as *"Sangraha's **synthetic and translated** expansion"* — translation from English is not a same-language rewrite of a real Indic document, which is what Demystifying's ~30% rephrase ceiling was measured on. Translationese has a different failure mode from rephrase, and the spec's own tier taxonomy (C = translated, D = synthetic) collapses if the 162B is largely translated. |

---

## 4. MISSING — rubric-named gaps and unpre-empted attacks

| # | Missing element |
|---|---|
| **M1** | **R6 / E10 — difficulty bands and reasoning-length bands, with a concrete example for each. Stated twice in the assignment; entirely absent.** The spec has a bare `Difficulty band` column reading `B0–B1 / B1–B2 / B2–B3 / B3–B4 / B4–B5` — no definition of any band, no example at any level — and no reasoning-length band system at all (§6 offers only "short and medium traces in the Reasoning stage; long traces reserved for the anneal": three rungs implied, no ultra, no token lengths, no example). **The course supplies both ladders verbatim.** `widget_7`: `B0 Nursery "simple children's sentences" / B1 Grade-school / B2 High-school / B3 Undergraduate / B4 Graduate / B5 Research–PhD`, plus *"short, medium, long and ultra traces are separate rungs… trace length is scheduled too."* `widget_6`: one worked problem (integers 1–1000 divisible by 3 or 5 → **467**) at LOW 2 steps / MEDIUM 4 / HIGH 6 / ULTRA 13, with per-step token counts. **~1.5KB of writing, zero research, recovers the largest single block of lost marks in the document.** |
| **M2** | **R8 — "the cleaning continues toward the cumulative target, now aimed at the slots the mixture shows to be starved."** The spec *identifies* the starved slots superbly (agentic 63.5×, tier C 5.06×, STEM 0.92×, tier A 1.98×) and then never turns them into a cleaning deliverable. Nothing anywhere about what gets cleaned next or in what order. |
| **M3** | **E11 stops at "excellent."** §7 is a real testable-hypothesis section, but no criterion has a **metric + threshold + seed count**. "Does not beat a format-data-only baseline" names no metric and no margin. "Degrades IndicGenBench" names no delta. The rubric's "highest" tier requires naming *the metric that would confirm or refute the mixture*; the spec names benchmarks, not decision rules. |
| **M4** | **The agentic kill criterion is unmeasurable at the scale it names — and this is the best single question a reviewer has.** §7.5 gates the lane on *"a 1B/3B proxy measured on agentic benchmarks (SWE-bench Verified, τ-bench, BFCL)"*. Spark Joy's own design rationale, quoted in its brief: 7B/1T was chosen *"so that the model performed above the noise floor on key metrics like MMLU."* A 1B/3B **base** model scores ~0 on SWE-bench Verified and τ-bench. The document's highest-stakes decision — whether to keep or kill a 45B-token lane — rests on a measurement its own evidence base says cannot be made at the declared scale. No answer anywhere. |
| **M5** | **Six of seven anneal deviations from the course anneal preset are undefended.** §4 defends web (8 → 20.3) at length and well. It never mentions: indic 28 → 21.5 (**−6.5**), long 8 → 2.7 (−5.3), reason 18 → 15.1 (−2.9), agentic 8 → 6.2 (−1.8), stem 10 → 8.9 (−1.1), code 20 → 22.4 (+2.4). Under grading instruction 9 every one is a maximum-pressure point. The Indic one is the sharpest: §2's "honest precedent statement" bravely defends *raising* Indic into the anneal against MAP-Neo — while never noting that 21.5% is a **6.5pp cut** from what the course's own preset asked for, i.e. the paragraph defends a direction it did not take as far as it was told to. |
| **M6** | **Why 60% ballast and not OpenCoder's 84%.** §4 establishes a 16–40% overlay band from six recipes and then selects **the maximum overlay in the band** while framing the band as a conservatism argument. The available answer — OpenCoder's anneal adds one lane, ours adds five, and 84% ballast leaves 12.8B, less than the Indic overlay alone — is never given. |
| **M7** | **Why 4 sub-cycles.** The measured result is **8** cycles at 1B (`Grow-P2` 1→8: MDQA 25.9→28.0, CSR 60.9→62.8). §8 concedes the inference; no reason for 4 appears anywhere. The mechanical answer (80B ÷ 4 = 20B = exactly the seam width) is available and unstated — and it creates a second unaddressed problem: sub-cycle 1 sits entirely inside the 20B anneal-entry blend band. |
| **M8** | **Why 20B seams.** §8 concedes "an order-of-magnitude choice". But the spec adopts Pref-Curriculum's S-shape and that paper's winning setting blends over **43.9% of the run ≈ 880B at 2T** — 44× wider. Adopting a paper's shape while rejecting its width by 44× with no argument is a prepared attack with no prepared answer. |
| **M9** | **STEM's 250B is not decomposable from the inventory.** The named STEM entries are peS2o 42B + proof-pile-2 55B + D4 STEM (V4) 49B = **146B**. At 146B, demand 229B is **1.57×** — "needs repetition", not "covered". The confidence table hedges ("almost no headroom if inventory is optimistic") without ever doing this arithmetic or naming the datasets. |
| **M10** | **91.7% of the reasoning lane's supply is one already-trained V4 corpus.** Inventory: OpenThoughts2 3B + OpenMathReasoning 2B + NuminaMath 0.5B + OpenR1-Math 1.6B + **AON (V4, confirmed) 78B** = 85.1B. So "170B against 85B unique = 2.0× repeat" is 2× on a corpus the previous cohort already trained, with 7.1B of genuinely new reasoning traces. Worse for R5: the anneal reserves **8.0B of long reasoning traces**, and the only long-trace inventory is OpenThoughts2 + OpenR1-Math = **4.6B → 1.74 epochs on the long-trace bucket**, not the 0.142 the epoch table implies. Invisible because R3's dataset naming is missing. |
| **M11** | **The run's total synthetic fraction is never stated — and it is favourable.** I compute 69.5B (Indic-D main) + 3.8B (Indic-D anneal) + 42.4B (agentic generated) + 2.4B (anneal verified-synthetic) = **118B / 2080B = 5.7%** of the run. Comfortably inside every ceiling the spec cites. The spec leaves its best aggregate number on the table and instead invites the reviewer to assemble it from a "22% of lane" and a "94% of lane". |
| **M12** | **Tier C's available defence is not made.** 5.06× is *below* Two-Phase's measured 6-epoch organic ceiling for high-quality crawl. The spec nominates tier C as its #2 attack surface and never states the one number that partially defends it. |
| **M13** | **"Verified synthetic + textbooks 3.0%" has no source, no supply, no epoch — and contradicts §2.** §2: tier D is legitimate *"never as invented textbooks"*, ceiling ≤3%. §4 then adds a component literally named "textbooks". It is the only anneal line with no provenance statement, and it is the missing 3pp of F2. |
| **M14** | **Tier C and tier D may be the same object.** `widget_9` tags Sangraha synthetic (162B — *all* of tier D) as inventory tier **C**, described as "synthetic **and translated** expansion". The spec's entire case for cutting tier C from 20% to 8% is *"tier C would need 63B against 5.0B unique = 12.6×"* — a supply figure that excludes the translated portion of the 162B. If any material fraction of that 162B is translated, tier C's supply is far larger than 5.0B and the 12-point cut loses its only quantitative justification. |

---

## 5. PADDING — E3 enforced hard

E3 is explicit: *"a tightly argued short plan will score well while **padding earns nothing**."* Applied without mercy. "Padding" = correct, well-cited, and serving no R1–R8 / E4–E11 clause.

| Block | Lines | ~Bytes | Why it is padding | Cut to |
|---|---|---|---|---|
| **Confidence summary** (22 rows) | 213–237 | ~2,400 | Pure restatement — every row's content already appears in §§1–8, and §8 already does the honesty work in prose. It also **actively costs marks on E1/E4**: labelling six lanes "Medium"/"Medium-high" hands a reviewer a ranked target list and reads as "undefended". | Fold the 3 rows carrying new information (STEM 0.92× headroom; DD's speed half shrinks at 120B; cycle count inferred from an 8-cycle result) into §8. **Cut ~2,000** |
| **"Packing and positional encoding are part of the mixture"** | 171–175 | ~1,900 | Binary decomposition, document-masking deltas, RoPE θ=100k, ABF θ≈10⁶, YaRN α(s)=0.1·ln s+1, 244 vs 304 ms. None of it is a share, a tier, a floor, a reserve, a band, a benchmark tie or a supply statement. By the lecture's own division this is Session 6 ("Session 6 builds the system that can execute that recipe"). | Keep **one** sentence — the 9.4% × 4.5T ≈ 423B natural 8k-contiguous supply, because that one changes a lane number. **Cut ~1,600** |
| **§5's eight-row evidence table** | 135–144 | ~1,700 | Eight clauses × eight citations defending the *existence* of a floor nobody disputes, for a floor that (F4) never binds. The most-cited object in the document spends its space on the least contested proposition while R4's actual question — the number, and per-lane vs aggregate — goes unanswered. | Keep 3 rows (hard constraint / real tokens / per-bucket-per-cycle); spend the space on the per-lane split. **Cut ~1,200** |
| **"Code lane is file-level deduped"** | 37–39 | ~700 | A cleaning decision, not a share. Its only load-bearing sentence is the conclusion ("effective code supply is below the headline; 479B stays covered"). Keeping the dedup ladder while the long-context lane is 60% repo-packed code (F14) is actively harmful. | One clause. **Cut ~500** |
| **Cluster-A/B 11-run ledger** | 107 | ~600 | Eleven percentages to defend one number. Two bracketing runs (OpenCoder 3.85%, Hunyuan-Large 4.76%) plus the taxonomy sentence do identical work. | Two runs + the taxonomy sentence. **Cut ~450** |
| **"Never gate on popularity"** | 35 | ~400 | Correct and well-cited, but it sets no number in this spec. | One clause inside the Indic hazard list. **Cut ~300** |
| **§6 bullet 4 (sequence-length ordering)** | 169 | ~450 | Duplicates the packing section's argument with the same citations. | Merge. **Cut ~300** |
| **"Why 2T" (Chinchilla clause)** | 8 | ~350 | The clause is self-contradicting (F10) and 2T is the composer default, i.e. given. | Two clauses: "composer default; the budget most forgiving of scarce supply among the presets offered." **Cut ~250** |
| **§3 point 5 (FIM)** | 78 | ~400 | Worse than padding — a wrong-setting citation that contradicts §3.6 (W1). | Cut entirely or restate as an untested proposal. **Cut ~400** |

**Total identified cut ≈ 7,000 bytes of 26,901 ≈ 26%.**

**The E3 verdict, stated as a grader would:** the document spends ~26% of its length on material the rubric never asks for, while **two twice-stated named requirements (R6/E10) and one named requirement (R8) are entirely absent** — and adding all three costs ~1.8KB. The padding is not paying for the gap; it is displacing it. The defensible version of this spec is **~20–21KB and strictly more complete than the 26.9KB version.**

---

## 6. Internal-consistency audit (the three cross-checks, answered directly)

**(a) Does §4's anneal mixture match §6's curriculum row? — NO. FATAL.**

| | web | code | reason | long | indic | stem | agentic | v-synth | sum |
|---|---|---|---|---|---|---|---|---|---|
| §4 printed | 20.3 | 22.4 | 15.1 | 2.7 | 21.5 | 8.9 | 6.2 | 3.0 | **100.1** |
| §4 exact (derived) | 20.31 | 22.37 | 15.10 | 2.67 | 21.48 | 8.87 | 6.20 | 3.00 | **100.00** ✓ |
| §6 row | 20 | 22 | 15 | 3 | 22 | 9 | 6 | — | **97** ✗ |

§4's derivation is *exactly* right — 60% ballast at the exact main proportions plus the six overlays closes to 100.00 with no residual, which is the best piece of arithmetic in the document. §6 then drops the eighth bucket, and the row sums to 97 under a header claiming 100. Agentic also drifts (4.96B vs 4.8B), and §3's 44.96B total uses the §4 figure.

**(b) Does §5's floor contradict any §1 share? — Not numerically, and that is the problem. FATAL on R4.**
8% aggregate sits below every stage's lane-triple total (min 20% at Seed; 26.3% main average; 43% anneal), so it never binds and constrains the selector nowhere. The real contradiction is **§5's "must be real tokens" against §3's "~94% of the lane is generated"** (F5), plus the unresolved per-lane/aggregate ambiguity whose two readings differ by 255× (F4).

**(c) Do §7's kill criteria contradict earlier commitments? — YES, twice. FATAL.**
1. **agentic → 0.5%** crosses the course's hard `floor: 2` for agentic *and* the §5 protected floor the spec spent a section fixing (F6).
2. **"Long-context stays ≥4% regardless, because 0% is the one setting proven catastrophic"** is defended by a result about missing *length buckets*, which §6 argues natural packing supplies for free — so by the spec's own reasoning the curated lane's floor is not what that citation protects (F12).
3. Non-contradiction, for the record: **tier C → 4%** is coherent — 12.64B ÷ 5.0B = 2.53×, and synthetic rises to 26% of the lane, still inside the <30% rephrase ceiling. The spec should say so; silence invites the reader to assume it breaks the ceiling.

---

## 7. The twelve hardest questions, with answer-quality verdicts

**Q1. Why deviate from the course preset at all? You say "two changes" — I count six, and your funding does not close.**
Long-context releases 1.55pp; reasoning takes 2.50pp; 0.95pp (19B tokens) comes silently out of Indic, STEM, web and code — including the lane you yourself call "0.92×, almost no headroom".
→ **NO ANSWER.** F3. The two deviations that *are* argued (long-ctx, reasoning) are argued well; the four that are not are the ones a grader will price. Worst-positioned failure in the document, because it sits in the paragraph titled "and why".

**Q2. Long-context 6% → 4.5%. Dataset Decomposition shows 9.4% already saturates. It says nothing about 4.5%. Which direction does your evidence actually run?**
The paper bounds the share from *above* (≥9.4% saturates; 25% adds noise). It is silent below 9.4% — the brief is explicit that "the one number we most want… is not measured". The spec's real argument is better than the one it leads with: packing supplies the length exposure, so the curated lane's job is content, not length.
→ **ANSWERED WEAKLY, and pre-empted honestly.** §8 concedes "the 2–9% region is unmeasured" and the confidence table says "threshold proven; the 2–9% region is unmeasured". But the *content* half of the argument then collapses on Q3.

**Q3. Your curated long-context lane exists to do multi-document reasoning. Name the datasets.**
`widget_9` has exactly two: Repo-packed code (32K+) 60B and Book-length corpora 40B. **Neither is multi-document.** And 60% of the lane is the repo-level packing your own §1 rejects on OpenCoder Table 9 / Fig 8.
→ **NO ANSWER.** F14 + R3 failure. This is the question I would open with. It converts the long-context section from "well-argued deviation" to "lane sized against supply that cannot do the job named for it", and it is only invisible because the datasets are never printed.

**Q4. Reasoning 6% → 8.5% at 2.0× repeat. What is the 85B?**
78B of the 85B (91.7%) is AON — the V4 run's own reasoning slot. New open traces total 7.1B. And your anneal reserves 8.0B of *long* traces against ≤4.6B of genuinely long-trace inventory = 1.74 epochs, not the 0.142 your table shows.
→ **NO ANSWER.** M10 + R3 failure.

**Q5. Why 2% agentic when your own arithmetic says 0.2%?**
The complete answer exists and is one line: **2% is the course composer's hard floor** (`{key:"agentic", floor:2}`), which `normalize()` will not let any slider cross. It is not the spec's choice. The spec instead writes "the composer floor encodes a capability commitment (Codex-class agentic is a stated V5 goal)" — taste-flavoured phrasing for a mechanical constraint.
→ **ANSWERED, BUT UNDERSOLD.** The disclosure is exemplary (63.5×, 94% generated, the literature-compliant 0.2–0.25% named explicitly, kill criterion declared). What is missing is the sentence that makes it unattackable: *"0.2% is the literature-compliant number and we would take it; the composer floor forbids it; here is the gating that makes 2% survivable."* And then F6 undoes it: the kill criterion drops **below** that same floor.

**Q6. Is the 8% floor per-lane or aggregate? If aggregate across Indic + agentic + reasoning, is agentic's 2% inside or outside it?**
Unresolved. Aggregate reading: it never binds (minimum lane-triple total 20% at Seed; 26.3% average; 43% anneal), Indic alone satisfies it, and OPUS can still zero agentic and reasoning — the exact CLIMB C20 → 0 failure §5 cites as the reason it must be a hard constraint. Per-lane reading: 8% real agentic = 160B from 0.627B unique = **255 epochs**, impossible.
→ **NO ANSWER, and FATAL under R4's verb "fixes".** Cheapest high-value fix in the document: one table row splitting the 8% (e.g. Indic 5 / reasoning 2.5 / agentic 0.5), stating which lanes carry real-token obligations, and stating that agentic's clause is met by verified-generated trajectories with a real-token seed in every batch.

**Q7. Why is the Indic anneal RAISED when MAP-Neo cut Chinese 25% → 8.5%?**
→ **ANSWERED WELL — the best paragraph in the document.** §2's "honest precedent statement" names the counter-precedent, names its magnitude, names the only supporting precedent (Yi-Lightning), states that Yi-Lightning discloses no percentages, and concludes "We are writing this number first, not following the field." That is exactly what E2 rewards.
**But the follow-up lands:** 21.5% is a **6.5pp cut** from the course's own anneal preset of 28%. So the paragraph defends a direction it did not take as far as it was asked to, and never says so (M5).

**Q8. Why 60% ballast and not OpenCoder's 84%?**
§4 assembles a 16–40% overlay band from six recipes and then picks the band maximum while framing the band as conservatism. The available answer (OpenCoder's anneal adds one lane; ours adds five; 84% ballast leaves 12.8B, less than the Indic overlay alone) is absent.
→ **ANSWERED WEAKLY.** The 19.5% mixture-shift comparison is genuinely good and method-consistent (I reproduce ½·L1 = 19.48% against Spark Joy 41.05% and OpenCoder 16%), but it defends the *shift*, not the *ballast fraction*. Different question, and the reviewer will ask the one that is not answered.

**Q9. Why 20B seams? And why five?**
§8 concedes 20B is "an order-of-magnitude choice". Meanwhile the spec adopts Pref-Curriculum's S-shape whose winning setting blends over **43.9% of the run ≈ 880B** — 44× wider. And five stages have four boundaries; 20B × 4 = 80B (4%), not the stated 5 seams / 100B / 5%.
→ **NO ANSWER on the width (M8, pre-empted but undefended); FATAL on the count (F15).** Unremarked: 20B on an 80B anneal is 25% of the reserve leg spent ramping in.

**Q10. Why 4 sub-cycles when the measured result is 8?**
→ **NO ANSWER.** §8 and the confidence table both concede the inference; neither gives a reason. The mechanical answer (80B ÷ 4 = 20B = the seam width) is available, unstated, and would immediately raise the follow-up that sub-cycle 1 lies entirely inside the anneal-entry blend band (M7).

**Q11. Your anneal epochs are all far below 1.0. Recompute them against your own top-5% quantile.**
Tier-A Indic 9.6B ÷ 3.2B = **3.00 epochs**. Long reasoning 8.0B ÷ 4.25B = **1.88 epochs**. Both past the 1.0-epoch line the same paragraph cites Spark Joy to say is where five categories regress. And if the anneal Indic is really drawn from the whole 276B lane, it was never held back.
→ **NO ANSWER.** F7. This is the question that breaks R5, because it turns the reserve's safety proof into a proof that the reserve is not a reserve.

**Q12. Your agentic kill criterion is a 1B/3B proxy on SWE-bench Verified and τ-bench. What score do you expect a 1B base model to get?**
Zero. Spark Joy's stated reason for choosing 7B/1T is that it is the smallest scale where MMLU clears the noise floor; SWE-bench Verified on a 1B base model is not a measurement. The document's highest-stakes decision — keep or kill 45B tokens — is gated on a metric that cannot be read at the declared scale.
→ **NO ANSWER, and it is the best question in the room.** M4. It attacks R7 and E11 simultaneously and cannot be waved off, because the spec itself cites the paper that establishes the noise-floor problem.

*Runners-up a reviewer will also reach:* your tier D is Sangraha "synthetic **and translated**" — is tier C a subset of tier D, and what is the ceiling for machine-translated English→Indic as opposed to same-language rephrase (M14/W12)? What is the run's total synthetic fraction (M11 — the answer, 5.7%, helps you)? Which datasets make up 250B of STEM (M9 — the answer, 146B, hurts you)? And how does FIM apply to a trajectory without letting the model see later tool observations, given your own masking rule (W1)?

---

## 8. Per-requirement grading

| Req | Verdict | Specific missing element |
|---|---|---|
| **R0** written spec, "specific enough to defend" | **PARTIAL** | Reads as a defensible spec and would survive most of a viva, but 15 internal-arithmetic/consistency failures and 4 unaddressed named requirements. Also reads as internal notes in places ("the three numbers a reviewer should attack first", em-dash-only table column) for a submission that is a public GitHub README. |
| **R1** share for every capability slot | **PARTIAL** | All 7 slots present with demand/supply/ratio/verdict/benchmarks — genuinely good. But the printed table **sums to 100.2** while asserting 100.0 (F1), and "two changes from the course preset" is six changes whose funding is 0.95pp short (F3). |
| **R2** Indic split A/B/C/D, not a headline number | **PASS** | Strongest requirement in the document: four tiers with share, demand, unique supply, repeat factor, named sources, plus real-78/synth-22 and the synthetic-type ceiling. Deductions: tier C labelled "repeat" where the course's own >4× rule says "must synthesize" (F13); tier D's provenance asserted (W12); tier C's supply may exclude the translated part of the 162B (M14). |
| **R3** agentic + reasoning + long-ctx pointed at inventory datasets | **FAIL** | Agentic is exemplary — 9 of 9 datasets with token counts, split long-trajectory vs format. **Reasoning: zero datasets named** (OpenThoughts2 / OpenMathReasoning / NuminaMath / OpenR1-Math / AON all absent). **Long-context: zero datasets named**, and the two that exist cannot do the multi-doc job the spec assigns the lane (F14). Two of three slots unpointed. |
| **R4** *fixes* the protected always-on floor the selector cannot cross | **FAIL** | A number is stated (8%) but not **fixed**: per-lane vs aggregate unresolved, the two readings differ by 255×, the aggregate reading never binds anywhere (min 20% vs 8%), and "must be real tokens" contradicts §3's 94%-generated agentic lane (F4, F5). |
| **R5** declares the anneal reserve **held back** for the cooldown | **PARTIAL** | Reserve declared with components, %, tokens; §6 correctly shows agentic pinned at 2% until the anneal, which is the "held back" mechanic the assignment wants. But the epoch-safety argument is priced against the **un-reserved whole-lane** pools, and the stated top-5% quantile pushes the two largest components to 1.88 and 3.00 epochs (F7). "Verified synthetic + textbooks 3.0%" has no source, supply or epoch and contradicts §2 (M13). |
| **R6** difficulty **and** reasoning-length bands, concrete example for each | **FAIL** | Bare labels `B0–B1 … B4–B5` in one table column. No band definitions, no example at any level, no reasoning-length band system. Both ladders and both worked examples are sitting in `widget_7` and `widget_6`. **Stated twice in the assignment, so weighted twice.** (M1) |
| **R7** commits to 1B and 3B proxy validation | **PASS** | §7.4 explicit ("Confirm on 1B then 3B before the mixture and architecture are frozen"), backed by a concrete CLIMB search protocol, the Llama-3 anneal-probe protocol, and correct FLOPs pricing (1/50 of a run per probe, a dozen ≈ 24%). Deduction: the agentic criterion is unmeasurable at that scale (M4) and CLIMB's 62M→1B transfer is stretched toward 120B (W7). |
| **R8** cleaning continues, aimed at the starved slots | **FAIL** | Starved slots are identified precisely; no cleaning deliverable, target or ordering anywhere. (M2) |
| **E1** holds up when pushed on every number | **PARTIAL** | Most attributed numbers survive verification exactly (§1 credit list). The document loses on its **own** numbers: two table sums, the preset-change accounting, the epoch/quantile mismatch, the seam count, the Chinchilla clause. Of my 12 hostile questions, **7 have no answer**. |
| **E2** reasoning quality and evidence behind the choices | **PASS-minus** | The best axis in the document. Nine papers used at the right settings, ceilings distinguished by synthetic *type*, Cluster A vs Cluster B correctly separated, and §8 is a real differentiator. Deductions: one misquote (F8), one unpublished citation presented as published (F9), one out-of-corpus citation on a broken premise (F10), FIM at the wrong setting (W1), "measured" for an interpolated 30% (W2). |
| **E3** tightly argued and short; padding earns nothing | **FAIL** | ~26% padding (~7.0KB of 26.9KB) — confidence summary, packing/RoPE section, 8-row floor table, dedup ladder, 11-run ledger — while R6, R8 and R3's reasoning/long-ctx datasets are absent for ~1.8KB of writing. The padding actively costs marks: the confidence table hands a reviewer a ranked list of six lanes labelled "Medium". |
| **E4** *defended* share for every lane | **PARTIAL** | Long-context, reasoning, agentic and the anneal are genuinely defended. Web 33.9%, code 24.0%, STEM 11.5% and Indic 15.8% are **asserted**: their magnitudes have no argument beyond the course preset, and the spec's own confidence table admits "no published code-share sweep inside a general mixture". |
| **E5** Indic tiers stated | **PASS** | See R2. |
| **E6** lane → benchmark, so a reviewer sees **why each number is what it is** | **PARTIAL** | The benchmark column is well-sourced (course `BENCH` map + survey Table VI + Dataset-Decomp's MDQA/TOEFL/QuALITY). But it is **decorative for 5 of 7 lanes** — no benchmark justifies a *magnitude* except long-context (via MDQA thresholds) and reasoning (via the effort dial). And the course's own rule `WEIGHTED_MIN = 8 // a lane needs at least this share to move its benchmarks` means **agentic at 2.0% and long-context at 4.45% claim benchmarks they do not fund by the course's own threshold** — never addressed. |
| **E7** sizes every lane against **real** supply from the inventory | **PARTIAL** | Demand/supply/ratio computed for all 7 lanes and all 4 tiers, arithmetic exact, and the verdict labels match the course classifier. But §1's Indic row counts 162B synthetic as unique supply (real-only 2.77×, W9); STEM's 250B is not decomposable from the inventory (146B nameable, M9); long-context's 100B cannot do the job named for it (F14); reasoning's 85B is 92% one already-trained corpus (M10). |
| **E8** says **plainly** where a share needs repeating or generating | **PASS-minus** | Genuinely plain and in the right places: "must generate", "~94% of the lane is generated", "we are writing this number first", per-tier repeat factors in the table. Single deduction: tier C at 5.06× is called "repeat" where the course's own classifier says "must synthesize" (F13). |
| **E9** no quiet over-allocation to a supply-poor lane | **PARTIAL** | **Verdict on the parent's question: loud disclosure IS sufficient to escape E9, and the 2% should stay.** E9's operative word is *"quietly"*; v3 is the loudest possible disclosure — it computes 63.5×, states 94% generated, names the literature-compliant 0.2–0.25% alternative, and declares a kill criterion. Moreover 2% is the **course's own hard floor**, so lowering it is not the spec's option. The "wishful accounting" charge does not stick. Two things stop this being a full PASS: the 0.95pp silently reallocated from Indic/STEM/web/code (F3) is precisely a quiet over-allocation in miniature; and the kill criterion that makes 2% survivable is itself void because 0.5% breaches the floor (F6). |
| **E10** bands with a real example at each level | **FAIL** | Same as R6. A requirement stated twice, failed once, costs twice. |
| **E11** tiered ceiling | **Reaches tier 2 of 4 — "excellent", not "highest".** | ✔ tier 1 (plan). ✔ tier 2: written as a testable hypothesis — §7.1–7.6 and §8 are exactly that, and "every number above is a hypothesis" is the right framing. ✘ tier 3 ("highest"): no criterion has a **named metric + threshold**; "does not beat a format-data-only baseline" states no metric and no margin; "degrades IndicGenBench" states no delta; and the one metric that *is* named is unreadable at the declared 1B/3B scale (M4). ✘ tier 4 ("very highest"): nothing run, no numbers brought back. |

*Context clause, noted not graded:* the plan "is looked at only once your team has met the data-gating threshold". R8's cleaning deliverable is the only place the spec could have connected to it, and R8 is a FAIL.

---

## 9. Score

**Estimated: 345 / 500 (69%). Defensible band 330–360.**

Reasoning, in the rubric's own weighting:

- **The R-checklist gates the score.** Of eight named requirements: **2 PASS** (R2, R7), **2 PARTIAL** (R1, R5), **4 FAIL** (R3, R4, R6, R8). Half the explicitly named requirements are unaddressed or broken. No amount of evidence quality recovers a requirement that was never attempted — and R6 was stated twice.
- **E2 and E8 are where the marks are earned.** Nine papers read at the right settings, ~70 attributed numbers of which 67 verify exactly, ceilings correctly separated by synthetic *type*, Cluster A vs Cluster B correctly distinguished (a real insight the survey supports and most submissions will get wrong), the 8× quantile arithmetic corrected against the internal brief, and a §8 that volunteers six disqualifying limitations. That is upper-second-class work on the criterion the rubric says the grade "rests on".
- **E1 caps it.** 7 of my 12 hardest questions have no prepared answer, and the failures are in the spec's *own* arithmetic — two table sums, a funding story 0.95pp short, an epoch table computed on the wrong pool, a seam miscount, a self-contradicting Chinchilla clause. A grader who adds up the first table and gets 100.2 reads the rest more harshly.
- **E3 costs real marks and is the most self-inflicted loss.** ~26% padding while three named requirements sit unwritten for ~1.8KB. "Padding earns nothing" is explicit; here padding also *displaces*.
- **E11 caps the ceiling.** "Excellent" not "highest", so the top band is unreachable regardless of the rest.
- **E9, judged in the spec's favour.** The agentic disclosure is the single best-executed thing in the document and should not be penalised. It is the reason this is a 345 and not a 300.

**Four fixes, no new research, ~2KB net after cuts, move this to ~430–445:**

1. **Write R6/E10** — the six difficulty bands with the course's own example strings (B0 nursery "simple children's sentences" → B5 research/PhD), and the four reasoning-length rungs with the course's worked problem (1–1000 divisible by 3 or 5 → 467) at 2/4/6/13 steps, tied to the stage table's existing band column. **~1.5KB. Largest single recovery available.**
2. **Split the 8% floor per lane** and state which lanes carry real-token obligations. **~0.3KB. Converts R4 FAIL → PASS.**
3. **Name the reasoning and long-context datasets** with token counts, as the agentic section already does. **~0.3KB. Converts R3 FAIL → PASS** — and forces the honest sentence about repo-packed code and the 78B V4 reasoning corpus, which is E2 credit rather than a liability.
4. **Fix the two table sums, the "two changes" accounting, the seam count, and the Chinchilla clause; recompute the anneal epochs against the top-5% pool.** **~5 lines. Removes six of the twelve FATALs.**

Then spend the ~7KB of cuts on R8 (name the cleaning targets: tier-A Indic verification, agentic trajectory generation, STEM inventory audit) and on a named confirm/refute metric with a threshold at a scale where it can actually be read — which is what E11's "highest" tier asks for.
