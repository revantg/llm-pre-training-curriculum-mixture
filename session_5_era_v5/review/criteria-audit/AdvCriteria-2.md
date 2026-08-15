# Adversarial review — AdvCriteria-2 · full clause table C1–C17

**Target:** `session_5_era_v5/SOLUTION.md`, 52,401 B / 346 lines. Read in full (raw, untruncated). Every constant I cite was re-derived from `widgets/` or recomputed; I did not accept a figure because the document asserted it.

**What I recomputed and confirmed correct (stated up front so the criticism below is credible):**
- §6 stage profiles time-average to §1's shares **exactly**, not "within 0.05pp": web 33.85 / code 23.95 / reason 8.50 / long 4.45 / indic 15.80 / STEM 11.45 / agentic 2.00 at stage weights .10/.35/.30/.25. All five stage rows sum to 100; the anneal row sums to **100.000** exactly (21.156+22.969+9.063+2.781+21.875+9.156+7.500+5.500). The v5 rounding FATAL is closed.
- §6b is impeccable and course-derived. I re-ran `widget_6_reasoning_effort.html:212–262`: LEVELS token counts are 32/69/156/341 **plus** `countTokens("The answer is 467.")` = 5 → **37 / 74 / 161 / 346** ✓. τ = 0.18×346 = **62.28** ✓. `acc(L)=0.955−0.615·e^(−L/τ)` → **61.5 / 76.8 / 90.9 / 95.3** ✓. ULTRA−HIGH = **+4.40** at **2.149×** tokens, against `isWasted` threshold `<0.05` ✓. ULTRA is **14** steps ✓.
- `WEIGHTED_MIN=8` with the verbatim comment *"a lane needs at least this share to move its benchmarks"* (widget_1:293) ✓; `floor:2` agentic, `floor:12` indic (widget_1:284/287) ✓; TIERS A40/B25/C20/D15 (widget_1:305–310) ✓; `DIFF[]` B0–B5 definitions verbatim (widget_7:287–294) ✓; widget_7:236 length-band quote verbatim ✓.
- Inventory supply verified against `widget_9`: `SUPPLY_T` code 1.1T / agentic 0.00063T / reason 0.085T / longctx 0.1T / indic 0.276T / stem 0.25T / web 4.5T ✓. **AON 78B is real inventory** — `widget_9:312` `{g:'reason',name:'AON (V4 corpus)',tokens:78e9,tag:'conf'}` ✓. §1.2 arithmetic exact: 28.4/7.1 = 4.00 ep, 141.6/78 = 1.82 ep, 170.0/85.1 = 2.00×, bands 4.26/8.52/9.94/5.68 = 28.40 ✓, ULTRA 5.68/4.6 = 1.23× ✓.

The evidence discipline in this document is genuinely above the field. The clauses I own are the ones it fails.

---

## 1. The C1–C17 table

| id | verdict | locator that satisfies (or fails) it | the follow-up a reviewer still asks |
|---|---|---|---|
| **C1** master: holds up on every number | **PARTIAL** | 287 bolded numeric claims across 52.4 KB; most reproduce. But three live contradictions: (a) `SOLUTION.md:157` "**130.7B = 6.28% of 2.080T**" vs `SOLUTION.md:314` "the **116.0B** synthetic total" — and 116.0B sits *inside* the sentence claiming everything is "computed rather than asserted"; (b) `SOLUTION.md:299` prices probes as "a 40B probe on **120B params** … 1/50 of a run, so twelve probes cost ~24%" while every row of the table at `:302–311` is **1B or 3B** — the cost basis prices an experiment the plan never runs, and "twelve" ≠ the 22 arms specified; (c) `BANDS_AND_PROXY.md`, advertised at `README.md:156` as "band definitions + proxy protocol detail", contradicts the deliverable on the length-band budget (25.5/51.0/59.5/34.0B vs 4.26/8.52/9.94/5.68B), on H3 ("survives **5.06×**", arms 8/4/0 vs "survives **2.53×**", arms 4/2/0), on H2's refute action ("**drop agentic to 0.5%**" vs "**the share stays at 2.00%**"), on H4 ("4% anneal beats 2%" vs "80B beats 40B"), and on the shift (19.5% vs 17.64%) | Which of 130.7B and 116.0B is the synthetic total, and why does the sentence asserting computational rigour carry the wrong one? |
| **C2** reasoning + evidence quality | **MET, strongly** | Scale and setting attached to nearly every citation: `:28` Muennighoff `R*_D=15.39` on "182 runs, 7M–9B params"; `:299` "MMLU is not a 1B metric"; `:295` RoPE "Table 4, **1B only**" with the Table-2/Table-4 conflict disclosed; `:341` scale-gap bullet naming nanoGPT/1B/1.5B/≤3B | Nothing structural. This clause is the document's strength. |
| **C3** short + tightly argued; **padding earns nothing** | **FAILED (penalty active)** | 52,401 B. Prose is **40,761 B (77.8%)** against **10,886 B** of tables. `review/redteam-v5-cuts.md:133` handed the author a byte-level plan from 37,708 → **26,258 B**; only one Tier-1 cut (§10, −1,684 B) was taken and the document then **grew 14,693 B (+39%)**. §2 alone is **10,159 B = 19.4%** for one lane. Full accounting in §2 below | Why did the document grow by 39% after a byte-level cut plan? |
| **C4** defended share for all 7 lanes | **MET** | `:18–24` seven rows with share/demand/supply/pre-sel/post-sel/verdict; `:44–50` all six deltas from preset with token cost; every lane has a named sizing driver | STEM 11.45% is sized by "the arithmetic closing" (`:40`) — what defends 11.45 specifically rather than 12.00? |
| **C5** Indic split across all four tiers | **MET** | `:86–91` A **40%** / B **30%** / C **4%** / D **26%** with demand, named supply and repeat per tier; `:93` real 74% / synthetic 26% | Tier D's 4pp gain is placed on a paper that `:113` says "explicitly decline[s] to transfer the result to **synthetic** data" — so what supports D at 26%? |
| **C6** each lane → benchmarks, causally | **PARTIAL** | `:18–24` benchmark column present for all 7. But `:26` concedes: "**The other five shares are supply-and-order constrained; their benchmark column states what they are accountable for, not what sized them.**" **2 of 7 causal.** See §4 below | The course ships `BENCH` + `lit = src.some(k=>vals[IDX[k]]>=WEIGHTED_MIN)` (widget_1:313–321, 489). Under your mixture **6 of 13 benchmark chips go dark**. Why is the widget's own causality test invoked for one lane only? |
| **C7** sized against real inventory supply | **MET with a hole** | `:18–24` supply column matches `widget_9` `SUPPLY_T` exactly; `:32` code re-based to 362B eff.; `:34` Indic re-based to 113.9B real. **Hole:** widget_9 tags every row `conf`\|`approx`\|`synth` (widget_9:241). Only **1,205.0B of 6,401.6B (18.8%)** is `conf`; **78.6% is `approx`**. Per lane confirmed: reason 91.7%, indic 31.9%, code 18.0%, general 17.4%, **long-context 0.0%**, **agentic 0.0%**. The document never mentions the tag | Every agentic row is `approx`. On what basis is `:144` "**74% of this lane is provably not fillable**" — *provably* — when the 0.627B denominator is course-tagged approximate? |
| **C8** says plainly where repeat/generate is required | **MET, exemplary** | `:19–24` `Verdict` column: covered / **repeat** / **generate**; `:133` "**42.1B generated — 91.5%**"; `:34` "A 1.15× lane ratio computed against real+synthetic supply would be precisely the wishful accounting this plan is graded against" | None. Best-discharged clause in the document. |
| **C9** penalty: quiet large share on a data-poor lane | **AVOIDED** | The trap is defused three times: agentic `:24`/`:133`, Indic `:34`, reasoning `:61` ("The trace-shaped pool is **7.1B, not 85.1B**") | Reasoning 8.50% = 170B of which 92% is academic prose, not CoT. Is a lane 92% off-shape still "funded" in `WEIGHTED_MIN`'s sense? |
| **C10** fixes the protected floor | **MET** | `:197` "**Fixed at: Indic 5.5% and agentic 2.0% of trained tokens — per lane, 7.5% together.**" with the derivation at `:209` and feasibility table `:213–216` | The Indic half is **strictly dominated** by the composer's binding `indic ≥ 12` (`:231`), so 5.5% can never fire at lane level. Does your own protected floor have any lane-level effect at all? |
| **C11** declares the anneal reserve | **MET** | `:165` "**62.5% original-distribution ballast + 37.5% reserved (30.0B)**" + 7-row component table `:168–175` with pool, quantile, epochs, real/derived/generated | §4's heading says "Anneal reserve — **80B**" but the body defines the reserve as **30.0B**. Which is the reserve you are holding back? |
| **C12** difficulty bands, real example at **each** of 6 | **MISSING** | `:255–260`. B0 ✓ quoted text, B1 ✓ quoted text, B2 marginal, **B3 ✗, B4 ✗, B5 ✗** — genres, not artifacts. See §3 below | "A **GSM8K-style** multi-step word problem" — which problem? The hedge "-style" concedes it is not an example. |
| **C13** length bands, real example at **each** of 4 | **MISSING** | `:274–277`. LOW/MEDIUM/HIGH quote widget_6's step 1 **verbatim**. **ULTRA `:277` does not**: it prints *"Restate the goal… then verify two independent ways."* — a splice of steps 1 and 2 (widget_6:236–237) under a column headed "First step". One of four levels shows a description, not the step | Three bands are verbatim and the fourth is elided. What is ULTRA's actual first step, and why is it the only one not quoted? |
| **C14** written as a testable hypothesis | **MET** | `:301–311` eight hypotheses, each with scale / arms / metric / numeric confirm / numeric refute / **action on refute**; `:299` pre-commits the between-bounds default ("keep the specified value and re-run at the next scale up") | Eight lane-level falsifiers, **no whole-mixture falsifier**. What single 1B result makes you abandon this mixture rather than adjust one lane? |
| **C15** concrete 1B/3B proxy + named confirm/refute metric | **MET** (highest tier reached) | `:301–311`: H1 MDQA-30+RULER+LongBench ≥90%/<75%; H2 **3B** BFCL AST-match +3.0/+1.0; H3 IndicGenBench chrF+MILU+TyDiQA ±1.0; H4′ GPQA+MATH ≤1.0/>1.5; H6 peak grad-norm <3.0×`RED_T`; H7 length-ratio ≥4×/<2× | **Fatal to the thresholds:** `:299` establishes that single-seed 1B/1.5B work "cannot resolve below **≈±0.5pp**" and `:342` says "Cite curve shapes, not exact optima" — yet H3/H4/H4′/H5 all hinge on **≤1.0 pt** and the document specifies **no seed count** for any of its own probes. At n=1 with ±0.5pp noise a 1.0-pt threshold is unresolvable by the document's own bound. |
| **C16** ran the proxy, brought numbers back | **MISSING — correctly disclaimed** | `:314` "H1–H7 are specified and unrun: this plan claims the **highest** tier … and not 'very highest.'" See §6 below | Neither executed item is a proxy run. Why is ~600 B spent describing a replication whose only output (44.9%) is already at `:293`? |
| **C17** data-gating threshold prerequisite | **MISSING — and it is a prerequisite** | **Zero** occurrences of "licen" in SOLUTION.md. No cleaned-token count, no cumulative target, no documentation artifact, no gate. §8 (`:318–334`) is a *forward-looking* priority list — where to clean **next** — with no threshold and no status. `README.md:26` states R8 and never answers it; `README.md:33–46` decomposes the criteria into **E1–E11 and omits the gating clause entirely**. See §5 below | The criteria say the plan "is looked at only once your team has met the data-gating threshold." What is the threshold, and have you met it? |

**Tally: 9 MET · 4 PARTIAL · 4 MISSING · 1 penalty active.**

---

## 2. C3 — the padding penalty, enforced

### Measured byte budget

| bytes | % | section | lines |
|---|---|---|---|
| 820 | 1.6 | header | 1–11 |
| 5,617 | 10.7 | §1 lane shares | 12–37 |
| 831 | 1.6 | §1.1 deviations | 38–53 |
| 660 | 1.3 | §1.2 reasoning fill | 54–62 |
| 2,200 | 4.2 | §1.3 long-context | 63–81 |
| **10,159** | **19.4** | **§2 Indic** | 82–126 |
| 5,652 | 10.8 | §3 agentic | 127–162 |
| 5,072 | 9.7 | §4 anneal | 163–194 |
| 4,908 | 9.4 | §5 floor | 195–232 |
| 1,369 | 2.6 | §6 curriculum | 233–248 |
| 2,007 | 3.8 | §6a difficulty bands | 249–265 |
| 2,058 | 3.9 | §6b length bands | 266–284 |
| 2,334 | 4.5 | §6c packing/seams | 285–296 |
| 5,299 | 10.1 | §7 proxy protocol | 297–317 |
| 1,285 | 2.5 | §8 cleaning | 318–334 |
| 2,131 | 4.1 | §9 no evidence | 335–346 |

**Byte spend is inversely correlated with clause weight.** C12+C13 are stated **twice** in the assignment (body: "with a concrete example for each"; criteria: "with a real example at each level") and receive **4,065 B = 7.8%**. C17, a **prerequisite**, receives **0 B**. §2 — one lane, one clause — receives **19.4%**.

### Growth against the cut plan the author already had

`review/redteam-v5-cuts.md` targeted v5 (37,708 B) → **26,258 B**, with a clause→sole-carrier map so cuts were provably safe. Section-by-section, against the current file:

| section | v5 | now | Δ |
|---|---|---|---|
| §2 Indic | 2,762 | **10,159** | **+7,397** |
| §1 | 1,981 | 5,617 | +3,636 |
| §3 | 3,476 | 5,652 | +2,176 |
| §5 | 3,621 | 4,908 | +1,287 |
| §7 (both blocks) | 4,443 | 5,299 | +856 |
| §1.3 | 1,422 | 2,200 | +778 |
| §4 | 4,587 | 5,072 | +485 |
| §10 | 1,684 | **0** | −1,684 ✓ |

**One cut of nine was taken. The document then grew 14,693 B (+39%) against a plan to shrink it 11,450 B.** That is the single most damaging fact about this submission under C3, because it is not an oversight — the author held the map.

### Cuttable without losing a defended number

| bytes | passage | why it is safe |
|---|---|---|
| **−1,150** | `:111` (1,409 B) — "**Tier C was 8% in an earlier draft, defended as 'inside Two-Phase's 6-epoch ceiling.' That defence does not hold and we have withdrawn it.**" + "**One honest correction to why C moved**" | The largest paragraph in the document narrates a **withdrawn position**. It hands a reviewer a discredited number to push on that need not exist. Keep only the NVIDIA cap result (28.30/28.00/26.60 over 18.7B→1.5B sources) that actually sets 4%. |
| **−1,000** | `:299` (1,529 B) cost-basis paragraph | Its headline (1/50, twelve probes, 24%) prices a **120B-parameter** probe; the table below it specifies 1B and 3B. Delete the mispriced basis; keep the MMLU-not-at-1B rule, the ±0.5pp bound and the between-bounds default. |
| **−900** | `:120` (1,306 B) Indic hazard 2 | Decision output is one clause ("no positively-defined quality gate touches tier B, code or STEM without per-lane validation") plus the KenLM substitute. The four Books thresholds and the Fig-11 narration set no number. |
| **−840** | `:36` (1,144 B) "**Filters.**" | Sets **no share in the mixture**. Its two decisions — filtering is web-only; popularity is never a gate — are ~250 B. |
| **−700** | `:34`, `:99`, `:101`, `:209`, `:218` | "One epoch of real Indic = **5.70%**, and umT5 (48.2B/48.4B) + NVIDIA (6.00B/6.00B) both serve exactly 1.00" appears **five times**, spelled out in full twice. State it once. |
| **−690** | `:78` (841 B) file-level-dedup vs repo-packing reconciliation | Defends an internal-consistency charge, not a number. One clause: "file-level dedup selects tokens; repo-packing assembles them — orthogonal." |
| **−600** | `:314` micro-replication block | By the document's own admission it earns no C16 credit, and its sole design output (44.9%) is already stated at `:293`. Keep one clause. |
| **−500** | `:101` (522 B) "The tension is in the assignment's own constraint, not in our choice" + `:109` (393 B) UniMax `normalize()` edge case | The first is meta-defence; the second is an implementation note that sets no share. |
| **−450** | `:139–143` 4×2 agentic compliance table | Eight cells deriving two numbers. One line: "defensible band 0.125–0.376%; we ship 2.00%, 5–16× outside it." |
| **−400** | `:203–207` 5-row proxy-score table | The finding is "reasoning scores 0.818 — third, above web." Three rows are decoration. |
| **−350** | `:264` Fig-9 / Fig-6b numbers in §6a | Duplicates §2 hazard 3 (`:121`). Keep the concession "no paper supports a content-difficulty ladder" — that is C2 gold. |
| **−300** | `:30` "Selector-adjusted supply" | The pre/post columns carry the finding; five sentences → one footnote. |
| **−11,250** | **`BANDS_AND_PROXY.md` in its entirety** | Self-labelled "**Staging file for SOLUTION v4**", advertised at `README.md:156` as current "detail", and contradicts the deliverable on six numbers including the whole length-band budget. Deleting it is a **C1 fix and a C3 fix in one keystroke, at zero cost to any clause** — SOLUTION.md is self-contained for C12/C13/C15. |

In-document cuts: **−7,880 B** → **44,521 B**. Plus proportional compression of §4/§5 (still 9,980 B for two clauses whose sole carriers are two tables): **−4,000 B**. Plus §2's remaining 14 bold-led paragraphs down to the tier table + 6 load-bearing ones: **−3,000 B**. **Landing: ~37,500 B.** Reaching 28,000 requires the full Tier-2 compression pass the earlier review specified and the author declined.

### The decisive question: where does this document stop gaining and start losing?

**Derivation, not a guess.** Tables (10,886 B) are the number carriers and are untouchable. Seventeen clauses at ~700 B of prose defence each = 11,900 B. Headings and rules = 755 B. **Minimum viable = 23,500 B.** Add the genuinely new *defended* material this version has and v5 did not — the Muennighoff law and the 16.39× asymptote (which replaced a borrowed ceiling and re-prices every repeat factor), the post-selector column, code's 32.9%→362B re-basing, Indic's real-supply re-basing, UniMax cap-as-mechanism, the 5.70% floor derivation, H4′, the ±0.5pp resolution bound: **~4,000 B**.

- **Stops gaining at ≈ 28,000 B.**
- **Starts losing at ≈ 32,000 B.**
- **Currently 52,401 B — 20,400 B (64%) past the ceiling.**

The *mechanism* by which extra bytes lose marks, not merely fail to gain: **287 bolded numeric claims.** The criteria's operative test is a reviewer pushing on **every number**. Every paragraph that discloses a superseded position (`:111`), prices a non-existent experiment (`:299`), or restates a settled fact for the fifth time (`:218`) adds numbers to defend without adding a clause to discharge. The document then compounds it at `:345` by handing the reviewer a pre-ranked "**Attack first:**" list. Honesty is a C2 asset; a longer attack surface is a C1 liability. Past ~32 KB the second dominates.

### Was ~26,000 right?

**Essentially yes, and it is now ~2,000 B too tight.** It was derived bottom-up from a clause→sole-carrier map — the correct method — but against v5's content set, which lacked the repetition law, the selector-adjusted column and the real-supply Indic re-basing. Those are marks-earning and cost bytes. **Revised target: 28,000 B (band 26,000–30,000).** The earlier recommendation was sound; the author's response was to add 14,693 B.

**Cut, in order:** delete `BANDS_AND_PROXY.md` (−11,250) → §2 to ≤4,500 B (−5,650) → `:299` cost basis (−1,000) → `:111` draft history (−1,150) → `:36` Filters (−840) → the 5.70% quintuplication (−700) → §4+§5 compression (−4,000) → the remaining table above.

---

## 3. C12/C13 — a real example at each of ten levels

### Difficulty bands, `:255–260`

| band | what is printed | ruling |
|---|---|---|
| B0 | *"The cat sat on the mat. The mat was red."* | **REAL** — quoted artifact |
| B1 | *"Water boils at 100 °C at sea level."* | **REAL** — quoted artifact |
| B2 | "A Wikipedia article on photosynthesis; a 30-line Python script with one loop" | **MARGINAL** — first half names one identifiable document; second half is a genre |
| B3 | "A **GSM8K-style** multi-step word problem; a single-file module with tests; an IndicGenBench summarisation pair" | **NOT REAL** — "-style" is an explicit concession that no item is given |
| B4 | "An AIME problem with a worked solution; a SWE-Gym task with a repo checkout; a peS2o paper section" | **NOT REAL** — dataset + item-type, no item |
| B5 | "A GPQA-Diamond physics item; a proof-pile-2 formal proof; a full SWE-smith trajectory with recovery" | **NOT REAL** — dataset + item-type, no item |

**Verdict: MISSING.** Three bands fail outright and one is marginal. The pattern is the worst possible one: **the examples get vaguer exactly as the band gets harder.** B0–B1, which any reader could exemplify unaided, are quoted; B3–B5, which carry the entire difficulty claim, are dataset names with a difficulty adjective. That is a *description of what an example would look like*, which is precisely the failure the clause names. **Fix: three quoted stems (one GSM8K item, one AIME stem, one GPQA-Diamond stem), ~450 B → MET.**

### Reasoning-length bands, `:274–277`

| band | printed "first step" | widget_6 ground truth | ruling |
|---|---|---|---|
| LOW | *"Inclusion-exclusion: floor(1000/3) + floor(1000/5) − floor(1000/15)."* | verbatim, step 1 (`:215`) | **REAL** |
| MEDIUM | *"Count multiples of 3 up to 1000: floor(1000/3) = 333."* | verbatim (`:221`) | **REAL** |
| HIGH | *"Let A = multiples of 3 and B = multiples of 5 inside [1, 1000]."* | verbatim (`:228`) | **REAL** |
| ULTRA | *"Restate the goal… then verify two independent ways."* | steps 1 and 2 are *"Restate the goal: count n with 1 at most n at most 1000 such that 3 divides n or 5 divides n."* and *"Plan: apply inclusion-exclusion…, then verify two independent ways."* (widget_6:236–237) | **NOT REAL** — a splice of two steps behind an ellipsis, under a column headed "First step" |

**Verdict: MISSING.** Three of four are verbatim; the fourth is the only cell in the document that elides its source, and it is the band whose distinctiveness (346 tokens, 14 steps) most needs exhibiting. **Fix: paste ULTRA's verbatim step 1 (+60 B) and print LOW's full two-step trace (+130 B, it is 37 tokens) → MET at ~190 B.** Highest marks-per-byte in this review.

Secondary C13 point: the column shows a *first step*, never a trace. For a length band the distinguishing artifact **is** the trace, and step 1 is the least distinguishing part of it — LOW's and HIGH's first steps are both one line.

### Does `BANDS_AND_PROXY.md` rescue C12/C13?

**No — it damages the submission.** It carries the same six B0–B5 cells (slightly richer at B5: adds FrontierMath) and the same four length cells with the **same spliced ULTRA**, so it fixes nothing. It is self-labelled "**Staging file for SOLUTION v4**" yet `README.md:156` presents it as current "band definitions + proxy protocol detail" — so a reviewer following the author's own map lands on a table where the length bands partition **170.0B** (25.5/51.0/59.5/34.0) instead of **28.4B**, a 6× divergence from the deliverable, plus a contradictory H2 refute action, H3 threshold, H4 hypothesis and mixture-shift figure. **Ruling: it does not satisfy the criteria, it does not split the answer — it contradicts it.** SOLUTION.md is self-contained; the companion should be deleted.

---

## 4. C6 — causal or decorative, lane by lane

| lane | share | what actually sized it | benchmark tie |
|---|---|---|---|
| Reasoning | 8.50 | `WEIGHTED_MIN = 8` + 0.5pp margin (`:26`) | **CAUSAL** |
| Long-context | 4.45 | threshold-not-gradient; funded by 17.7% ≥4k packing exposure (`:65–76`) | **CAUSAL** (inverted, and argued) |
| Web | 33.85 | arithmetic closing, −0.15 from preset (`:48`) | decorative |
| Code | 23.95 | arithmetic closing, −0.05 (`:49`) | decorative |
| Indic | 15.80 | composer `floor:12` + strategic bet; the doc says one epoch of real Indic would be **5.70%** (`:99`) | decorative — arguably **anti-causal** |
| STEM | 11.45 | arithmetic closing, −0.55 (`:46`) | decorative |
| Agentic | 2.00 | widget_1 `floor:2`, "**not ours to lower**" (`:146`) | decorative |

**2 of 7 causal**, and `:26` concedes it in the document's own words. The criteria require the tie to explain "**why each number is what it is**"; for five lanes the document states it does not.

**The fix is course-native, true, and ~250 B.** Widget 1 ships `BENCH` (widget_1:313–321) — an explicit lane→benchmark map — and lights each chip via `lit = src.some(k => vals[IDX[k]] >= WEIGHTED_MIN)` (widget_1:489), applied across `SLOTS.forEach` (widget_1:481). That is the course's own per-lane benchmark-causality test, and this mixture's result is computable:

- **Lit:** code 23.95, reasoning 8.50, STEM 11.45, indic 15.80, web 33.85 → LiveCodeBench, Aider, AIME, GPQA, HLE, MILU, IndicGenBench, MMLU.
- **Dark:** agentic 2.00 → SWE-bench, τ-bench, BFCL, GAIA, BrowseComp; long-context 4.45 → long-eval. **6 of 13 chips dark.**

One sentence — "five of seven lanes clear `WEIGHTED_MIN=8` and light every chip they feed; the two that do not are agentic (on `floor:2`, funded by §3's generation program) and long-context (funded by 17.7% packing exposure, not lane share)" — converts the benchmark column from accountability to threshold-causality **for all seven lanes at once**, and it is the widget's own logic rather than an invented argument.

---

## 5. C17 — the gate, and it is unaddressed

The criteria: the plan "is looked at **only once your team has met the data-gating threshold**, because a mixture is only as trustworthy as the **cleaned and documented** tokens standing behind it." The assignment body reinforces it: "Alongside the plan the cleaning continues toward the **cumulative target**."

**Findings:**

1. **No gate is stated.** No threshold, no cumulative target, no cleaned-token count, no "we have met it." `grep -c licen SOLUTION.md` = **0**. Nothing in the repo (no session 1–4 artifact, no cleaning log) supplies it either.
2. **§8 is tactical, not a gate.** `:318–334` is a 6-row table of where cleaning would *next* be most valuable, keyed to starved slots. That discharges the assignment's second half ("now aimed at the slots the mixture shows to be starved") and is genuinely well done — priority 1 even quantifies the return ("every 100M real trajectory tokens cuts the generated fraction ~2 points"). But it is entirely **forward-looking**: no status, no threshold, no gate to pass.
3. **The omission is in the author's own reading of the rubric, not just the writing.** `README.md:33–46` decomposes the criteria into **E1–E11** and the gating clause is **not among them**. `README.md:26` states R8 as a requirement and no section of the README answers it.
4. **The instrument for the gate is sitting in the course's own inventory, unused.** `widget_9` tags every row `conf`\|`approx`\|`synth` (widget_9:241) and carries `lic:` on all 32 rows. Recomputed: **1,205.0B of 6,401.6B (18.8%) is `conf`; 5,034.6B (78.6%) is `approx`.** Per lane confirmed: reason 91.7% (AON), indic 31.9%, code 18.0%, general 17.4%, **long-context 0.0%, agentic 0.0%**. Licence values include `task licenses` (SWE-Gym, SWE-smith) and `mixed` (OpenHands) — exactly the rows the 91.5%-generated agentic lane seeds from.

**Consequences beyond C17.** Because the document never states the tag, every coverage ratio inherits an undisclosed uncertainty in its denominator: 0.92× STEM, 1.32× code, 2.05× Indic real, 0.89× long-context and **63.8×/73.4× agentic** are all computed against `approx` counts. And `:144`'s "**74% of this lane is provably not fillable from the organic pool**" says *provably* on top of a 0.627B figure the course tags approximate. That is the one place the document's otherwise exemplary evidence discipline lapses.

**Ruling: MISSING, and weighted as a prerequisite.** The criteria make review *conditional* on this clause; a plan silent on it invites the reviewer to ask whether it should be being read at all. **Fix, ~350 B:** one paragraph stating (a) the cumulative cleaned-token target and the team's position against it, (b) that 18.8% of the inventory mass this plan draws on is course-`conf`irmed and 78.6% `approx`, so ratios carry that uncertainty, and (c) the licence posture for the `mixed`/`task licenses` rows the agentic generation program seeds from. That single paragraph moves C17 off zero **and** hardens C7.

---

## 6. C16 — ruling on the two executed items

**Neither is a proxy run, and the document is right to say so.**

1. **"The mixture is executable arithmetic" (`:314`).** I verified it and it holds — the stage time-average is exact (not "within 0.05pp"), every row sums to 100.000, §6b's four solve rates and token counts reproduce from widget 6's own curve, §1.2's epochs are exact. This is real and it defends C2/C14. It is **not** a proxy: no model, no metric from H1–H7, no confirm/refute evaluated. It is the arithmetic being self-consistent — a precondition for the plan, not a test of it.
2. **The 342-document packing micro-replication (`:314`).** It measures a **corpus statistic** (DD's `Σl(l−1)/2Σl`) on **78,581 tokens of the author's own briefs and lecture notes** — roughly $3.8\times10^{-8}$ of the 2.08T mixture — using no model, no training, and no benchmark. Its 8.20× overshoot against DD's published 1.45× is honestly explained. Its one design output (the ≥256 bucket policy, 44.9%) is already stated at `:293`.

**Ruling: C16 MISSING; claiming it would be overreach, and the document does not claim it.** `:314` states plainly "H1–H7 are specified and unrun: this plan claims the **highest** tier … and not 'very highest.'" **That concession is adequate and it is the right call** — the alternative would have been fatal under C1.

Two residual charges, both mine:
- **Reproducibility is asserted, not provided.** "reproducible from this repository" — there is **no script, no corpus manifest, no output artifact**. `papers_workspace.py` is a marimo notebook of paper notes; it computes neither item. Either commit the ~30 lines that produce the four-row table, or drop "reproducible."
- **The block contains a number contradicted elsewhere.** The sentence claiming "every ratio, tier factor, reserve quantile, epoch count, the 17.64% shift and the **116.0B** synthetic total are computed rather than asserted" cites 116.0B where `:157` computes **130.7B** (84.2 + 42.1 + 4.4, and 130.7/2080 = 6.284% ✓). The rigour claim carries the one stale number in the paragraph.

---

## 7. §9's concessions — adequate, or a small admission covering a larger problem?

| concession `:337–344` | ruling |
|---|---|
| "Indic is now partly evidenced, and the evidence is thin" — neither paper compares native vs translated vs synthetic | **Adequate and load-bearing.** It concedes the exact axis the A/B/C/D split turns on. |
| "No paper trains agentic trajectories at pretraining scale… 2.00% is 5–16× outside the band our own citations support" | **Adequate, and unusually brave.** Names the magnitude of its own violation. |
| "Long-context evidence stops at 8192, and nothing we hold is multi-document while MDQA is the metric" | **Adequate**, stated three times (`:78`, `:329`, `:339`) — which is itself a C3 finding. |
| "Almost nothing has error bars… single-seed. Cite curve shapes, not exact optima" | **Inadequate — this is the one concession that distracts.** It is offered about the *papers* and then not applied to the plan's **own** probes: `:299` fixes the resolution floor at ≈±0.5pp and H3/H4/H4′/H5 set **≤1.0 pt** thresholds with **no seed count specified**. Conceding that others are single-seed while leaving your own arms unspecified is a small admission standing in for the larger one. |
| "Eleven claims reach us through the mid-training survey rather than a primary" | **Adequate**, but it is process narration; the three primaries are already cited in place. ~350 B of C3 exposure. |
| "**Attack first:** agentic 2.00%; Indic tier C; the reasoning lane's 7.1B trace pool; the absence of multi-document data" (`:345`) | **Adequate as honesty, net-negative as tactics.** Under C1 this pre-loads the reviewer's four hardest questions. Keep it only if all four have a stated answer within the document — three do (`:159` fallback, `:115` separability, `:61` disclosure); the MDQA gap does not, and `:331` says so. |

**Nothing material is conceded in §9 that is contradicted elsewhere.** The concessions are real, not decorative. The single inadequacy is the seed-count silence.

---

## 8. Prioritised by marks moved per byte — deletions included

| # | change | Δ bytes | clause | why this rank |
|---|---|---|---|---|
| 1 | **Delete `BANDS_AND_PROXY.md`** | **−11,250** | C1, C3 | Removes six live contradictions with the deliverable *and* 21% of the reviewed byte count. Zero clause cost — SOLUTION.md is self-contained. Best ratio in the review by an order of magnitude. |
| 2 | Paste ULTRA's verbatim first step; print LOW's full 37-token trace | **+190** | **C13 → MET** | Twice-stated clause off MISSING for the price of two sentences. |
| 3 | Quote three real stems at B3/B4/B5 (one GSM8K item, one AIME stem, one GPQA-Diamond stem) | **+450** | **C12 → MET** | Same clause, same leverage; fixes the three bands that carry the difficulty claim. |
| 4 | Add the data-gating paragraph: cumulative target + status; 18.8% `conf` / 78.6% `approx` of inventory mass; licence posture on `mixed`/`task licenses` rows | **+350** | **C17 off zero**, hardens C7 | A prerequisite currently worth nothing. Also removes the *"provably"* overclaim at `:144`. |
| 5 | State seeds per probe arm (or widen the ≤1.0 pt thresholds) | **+120** | C15, C1 | Closes the sharpest follow-up on the highest-scoring section, using the document's own ±0.5pp bound. |
| 6 | Add the `WEIGHTED_MIN`/`BENCH` sentence: 5 of 7 lanes light their chips; the 2 dark ones are agentic (`floor:2`) and long-context (packing-funded) | **+250** | **C6 PARTIAL → MET** | Converts five decorative ties to threshold-causal using the course's own widget logic. |
| 7 | Add H0: a whole-mixture falsifier vs the course preset at 1B/100B | **+200** | C14, C15 | Answers "what would make you abandon the mixture, not just a lane?" |
| 8 | **Delete `:111`** (draft history + withdrawn tier-C defence), keeping only the NVIDIA cap result | **−1,150** | C1, C3 | Largest paragraph in the document; narrates a retracted number. |
| 9 | **Delete/repair `:299`'s cost basis** — it prices a 120B probe for a 1B/3B table | **−1,000** | C1, C3, C15 | Removes a contradiction and 1 KB in one edit. |
| 10 | Reconcile 130.7B / 116.0B at `:314`; drop "reproducible from this repository" or commit the script | **±0** | C1, C16 | Free. The rigour sentence currently carries the stale figure. |
| 11 | **Delete `:36` "Filters"** to its two decisions | **−840** | C3 | Sets no share in the mixture. |
| 12 | **Collapse the 5.70%/umT5/NVIDIA fact from five statements to one** (`:34`, `:99`, `:101`, `:209`, `:218`) | **−700** | C3 | Pure restatement. |
| 13 | **§2 → ≤4,500 B**; **§4+§5 → ≤6,000 B combined** | **−8,650** | C3 | 19.4% of the document for one lane, and 19.1% for two clauses carried by two tables. |
| 14 | Add one clause: Indic's 5.5% floor is dominated by `indic ≥ 12` at lane level and binds only per-bucket/per-cycle | **+120** | C10 | Pre-empts "then it can never fire." |
| 15 | Retitle §4 "Anneal — 80B leg, 30.0B reserve" | **+20** | C11 | Removes a heading/body mismatch on the declared reserve. |

**Net: +1,700 B added, −23,590 B removed → ~30,500 B, all four MISSING clauses closed and C6 lifted to MET.**

---

## 9. The single highest-leverage fix

**Cut the reviewed surface to ≤30,000 bytes by executing items 1, 8, 9, 11, 12 and 13 — starting with the deletion of `BANDS_AND_PROXY.md`.**

It is the highest-leverage change because it is the only one that moves the clause the criteria state as an explicit **penalty**, and it moves three others for free: C1 improves (six contradictions with the stale companion vanish; 287 bolded numbers shrink toward a defensible count), C2 is untouched (not one defended number is lost — the cut list is drawn from restatement, draft history, a mispriced cost basis, and a paragraph that sets no share), and the ~1,700 B needed for C12/C13/C17/C6/C15 becomes affordable inside a document that is *shorter* than it is today. The author already holds a byte-level map to this outcome at `review/redteam-v5-cuts.md:133`; the file has since grown 39%. Executing the plan the author already commissioned is worth more than any sentence that could be added.

---

```
SCORE: 385-420 / 500
TO MOVE UP ONE BAND: Cut the reviewed surface from 52,401 B to <=30,000 B — delete BANDS_AND_PROXY.md (-11,250 B, six contradictions with the deliverable), :111 draft history (-1,150), :299's 120B-scale cost basis (-1,000), :36 Filters (-840), the 5.70%/umT5 quintuplication (-700), and §2 down to <=4,500 B — then spend 1,700 B of the recovered budget on ULTRA's verbatim first step, three real B3/B4/B5 stems, the data-gating paragraph, and the WEIGHTED_MIN/BENCH lit-chip sentence.
```