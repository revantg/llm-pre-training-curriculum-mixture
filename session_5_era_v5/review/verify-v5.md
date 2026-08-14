# Verification pass — `SOLUTION_v5.md` against the three v3 red-team reviews and the rubric

**Reviewer:** VerifyV5 · graded backwards from `local://rubric.md` (assignment `descriptionMarkdown`, 3300 chars, maxPoints 500, `rubricJson` empty).
**Target:** `session_5_era_v5/SOLUTION_v5.md` — **37,708 bytes / 359 lines** (v3 was 26,901 B).
**Method.** (1) Every FATAL in `redteam-numbers.md` (13), `redteam-citations.md` (14) and `redteam-rubric.md` (15) deduped to **29 distinct findings** and checked line-by-line against v5. (2) Every quantity v5 *newly* claims recomputed from scratch in a fresh kernel — not read off the document. (3) Every widget-derived claim checked against the widget source, including re-running widget 6's tokenizer and accuracy curve and widget 8's spike model. (4) R0–R8 / E1–E11 graded, E11 tier fixed, byte-level E3 audit.

---

## 0. Bottom line

**v5 closes 24 of the 29 deduped FATALs outright, partially closes 3, leaves 2 open, and breaks 3 new things — one of which is a table-sum failure in exactly the failure mode of FATAL-1.**

The arithmetic is now the strongest part of the document. I recomputed **41 independent quantities**; **36 reproduce exactly**, 3 reproduce with a labelling imprecision, and 2 are wrong in a way a reviewer will find. The two headline repairs are real: the §1 share column sums to **100.0000** (not 100.2) and the anneal effective mixture closes to **100.0000** with no residual. The reserve quantiles are no longer computed against a pool the spec says it does not draw from — every one of the five real/derived components divides exactly by the pool it names.

**But the graded artifact is not this file.** The assignment's submission clause is *"link to your Github Repo README.md"*. `README.md` line 7 still reads **"Primary deliverable → `session_5_era_v5/SOLUTION_v3.md`"**, `SOLUTION_v5.md` appears **zero** times in it, and the README's own body still ships `33.9%`, `63.5×`, `+3.4 avg`, `five seams`, and *"8% ... for Indic + agentic + reasoning — real tokens only"* — six of the FATALs v5 fixed, live in the surface the grader reads. **Score for the document as written: ≈438/500. Score for the repository as currently submitted: unchanged at ~310–345.** Fixing that is a two-line edit and it is worth ~100 marks.

---

## 1. FATAL closure table

Every FATAL raised by the three reviewers, deduped. `N`=redteam-numbers, `A`/`§`=redteam-citations, `F`=redteam-rubric. Line numbers are `SOLUTION_v5.md`.

| # | Original finding (quoted) | v5 | Evidence |
|---|---|---|---|
| 1 | **N1/A1/F1** — *"`33.9 + 24.0 + 15.8 + 11.5 + 8.5 + 4.5 + 2.0 = 100.2`. The sentence directly under the table — 'they sum to 100.0%' — is **false as printed**."* | **CLOSED** | L14 *"Exact time-average of the §6 stage profiles. Sums to 100.00."* Table prints the exact 2-dp shares 33.85 / 23.95 / 15.80 / 11.45 / 8.50 / 4.45 / 2.00. I recompute the sum as **100.0000** exactly (Fraction arithmetic, no float slop) and the time-average deviation from the declared column as **0.0000 pp on all seven lanes**. |
| 2 | **N3/A2/F2** — *"`20+22+15+3+22+9+6 = 97`. Line 152: 'Each row sums to 100%.' ... §4's eighth component has no column in the §6 table."* | **PARTIALLY CLOSED — the column is added, the row still does not sum** | L221 adds the `v-synth` column (**5.5**), and L223 states *"so §4 and §6 agree at 100.00"* — true of the **exact** values (I verify 100.0000). But the **printed** anneal row `21.2 + 23.0 + 9.1 + 2.8 + 21.9 + 9.2 + 7.5 + 5.5 = **100.2**`, under a header at L213 reading *"Every row sums to 100."* Eight round-half-ups of the exact 21.156 / 22.969 / 9.0625 / 2.781 / 21.875 / 9.156 / 7.5 / 5.5 add +0.2. **This is FATAL-1's exact failure mode, moved one table down.** Fix: print 2 dp in this row too, or write "shown to 1 dp; exact values in §4". |
| 3 | **N2/F10** — *"'it is **above** Chinchilla-optimal for 120B (~2.4T is compute-optimal)' ... 2.00T is 0.83× compute-optimal — below, not above."* | **CLOSED** | L8: *"Chinchilla-optimal for 120B is ≈2.4T, so 2.000T is **0.83× compute-optimal on unique tokens** — not an overtrained run."* Direction correct (2.0/2.4 = 0.8333). The 6× effective-token tension is separated as *"a selection-efficiency claim, not a unique-token claim."* `2503.19206` — the out-of-evidence-base citation the FATAL rested on — is deleted (**0** occurrences). |
| 4 | **N5/A8** — *"The §1 supply table ignores OPUS's declared 40% acceptance; three lanes flip covered → repeat."* | **CLOSED** | L16–24 add a **Post-selector** column; L26 states the flip explicitly (*"code, STEM and long-context all move covered → repeat, and reasoning reaches 4.99×"*) **and** makes the steelman the reviewers said was missing (*"a rejected token is not consumed, so it returns to the pool"*). I recompute: 0.376 / 3.307 / 2.862 / 2.290 / 4.994 / 2.225 / 159.49 — all seven match the printed 0.38 / 3.31 / 2.86 / 2.29 / 4.99 / 2.23 / 159.5. Note code's post-selector 3.31 is correctly taken on the **362B effective** pool, not the 1.1T headline. |
| 5 | **N12** — *"§1 says 'Effective code supply is therefore below the 1.10T headline' ... No number is given. Applying OpenCoder's own retention (32.74/99.47 = 32.9%) gives 362B against 479B = 1.32× repeat."* | **CLOSED, at the reviewer's own number** | L19 and L28: `32.74B / 99.47B = 32.9%` → **362B eff.** → **1.32× repeat**. I recompute 0.329144 → 362.06B → 1.3230×. |
| 6 | **N11** — *"The spec's marquee number is 40B/0.63B = 63.5×. The plan's actual agentic exposure is 44.96B, so the whole-plan gap is 71.4×."* | **CLOSED, and the reviewer's arithmetic superseded** | L107: *"40.0B (main) + 6.0B (anneal) = **46.0B**, so the gap to quote is **73.4×**."* I recompute anneal agentic = 7.50% × 80 = 6.000B and 46.0/0.627 = **73.365×**. v5 is right and the reviewers were low: they used the v3 anneal share (6.2% → 4.96B). Residual typo at L107: *"the 63.8**%** main-run figure"* — that is a **multiplier**, not a percent. |
| 7 | **N9/F6** — *"'Agentic → 0.5%' ... `{key:"agentic", floor:2}` and `normalize()` refuses to let any lane go below its floor. Dropping to 0.5% crosses it."* | **CLOSED** | L134: *"An earlier draft dropped agentic to 0.5% on proxy failure — which crosses the `floor:2` clamp invoked to justify it ... Corrected: if H2 refutes, **the share stays at 2.00%** and its composition changes."* H2's refute action (L284) matches: *"keep 2.00% share, swap generated for FIM-multiplied real + format"*. The floor is honoured and the capability claim, not the share, is withdrawn. |
| 8 | **N13/F4/§9** — *"8% ... reserved for Indic + agentic + reasoning — i.e. **aggregate**. Never resolved ... the aggregate reading never binds anywhere ... satisfiable with 8% reasoning and **zero agentic**. Ambiguity here is FATAL."* | **CLOSED** | L172: *"**Fixed at: Indic 5.5% and agentic 2.0% of trained tokens — per lane**, 7.5% together."* L174–184 correct the membership set from widget 3 and give the reason: reasoning scores **0.818, third, above web**, so *"including it would have been wrong twice."* This is the single largest structural repair in the document. One new deduction, item 30 below: 7.5% undershoots the course's own `LANE_FLOOR = 0.08` for the identical two-lane set. |
| 9 | **F5** — *"§5 row 4: 'It must be **real tokens**.' §3: total agentic exposure of which unique real is 1.4% ... §3 and §5 contradict each other about the same lane."* | **CLOSED** | L186–193 scope the clause with a feasibility table and name the contradiction: *"Earlier drafts said 'real tokens only' while also stating the lane is 94% generated — a direct contradiction, now resolved by scoping the clause."* Indic 5.5% = 110.0B vs **113.9B** real (A+B+C) = **0.9658 ep** → clause binds. Agentic 2.0% = 40.0B vs 0.627B = **63.796 ep** → clause cannot bind. Both recomputed exactly. |
| 10 | **N4/F7** — *"'the reserve is selected by a **top-5% quality quantile within each lane**' ... Tier-A Indic 9.6/3.2 = **3.00 epochs**, long reasoning 8.0/4.25 = **1.88** ... The safety argument and the selection rule are computed on different pools."* | **CLOSED** | The blanket top-5% rule is gone; L142–150 give a **per-component pool + quantile + epoch**. Every one divides exactly: Indic 9.6/64 = **0.1500** (top 15%), algorithmic code 6.4/1100 = **0.0058** (top 0.6%), long reasoning 3.0/4.6 = **0.6522** (top 65%), STEM 1.6/97 = **0.0165** (top 1.6%), trajectories 1.4/0.360 = **3.889** (whole pool). L154 names the two that hurt: *"a 3.0B reserve is 65% of it — not a selective quantile, and calling it one would be false"*; *"the long-trajectory reserve runs at 3.89 epochs ... nowhere near 'reweighted, not repeated.'"* |
| 11 | **N81/M10** — *"the 'long reasoning traces 8.0B' component **exceeds the entire long-trace inventory** (≈4.6B)."* | **CLOSED** | Component cut to **3.0B** against the named 4.6B pool (L148), with the 65% figure stated as a liability. |
| 12 | **§3.4** — *"Nothing is actually 'held back'. R5's verb is defeated ... every 'reserved' lane is already over-consumed before the anneal begins."* | **PARTIALLY CLOSED** | Genuine withholding is now named on three axes: L240 *"**B5 is reserve-only**, withheld from the main run and spent in the anneal"*; the §6 stage table holds `v-synth` at `—` for all four main stages and pins agentic at 2 until the anneal; L146–147 label two components *"data that **does not exist yet**"*. **Still unanswered for tier-A Indic:** the main run consumes tier A at 126.4B/64B = **1.98 epochs**, so the 9.6B "top 15%" slice is already trained twice before the anneal opens. v5's honest-notes paragraph covers long-CoT and trajectories but skips this one. One sentence fixes it (cap main-run tier A at 116.8B, or say plainly that the Indic reserve is a **reweight**, not a withholding). |
| 13 | **N6/A4/F8** — *"'−0.47 / −1.11 / −1.44 / −1.17 on LAMBADA / HellaSwag / Winograd / WinoGrande' ... those four numbers are the deltas at the **four phase lengths**. Fabricated axis."* | **CLOSED** | L162: *"−0.47 / −1.11 / −1.44 / −1.17 at 5 / 10 / 20 / 30% — these are the four **phase lengths**; the paper publishes no per-task breakdown within that category."* Axis corrected **and** the absence of per-task data stated. |
| 14 | **A5** — *"'Domain-Specific bucket **peaks at 0.89 epochs** and Code at 1.12' ... the peaks are **1.08 and 1.18** (30% arm) ... and it is a brief-derived table sold as 'Spark Joy's finding'."* | **CLOSED by deletion** | `0.89` and `1.12` no longer occur as epoch claims anywhere (`0.89` survives only as the long-context supply ratio at L23; `1.12` does not occur). The unpublished derived table is not cited. |
| 15 | **A3** — *"`+3.4 average` is a **relative %**; the absolute ordering gain is **+1.74**, printed beside absolute deltas."* | **CLOSED** | L225: *"order alone at identical weights is worth **+1.74 absolute average** (52.86 vs 51.12 — Two-Phase Table 4; the frequently-quoted '+3.4' is that same gain expressed as a *relative* percentage)"*. 52.86 − 51.12 = 1.74 and 52.86/51.12 − 1 = 3.402%. Both verified. The other `+3.4` in the document (L265, DD Table 5 long-context average) is a genuinely absolute figure and is correctly used. |
| 16 | **A6/F9** — *"'**Published analogue**: MiniMax-01 uses linear interpolation' ... commented-out LaTeX absent from the published paper."* | **CLOSED** | `Published` occurs **0** times. L271: *"MiniMax-01 **reportedly** interpolates source weights linearly across transitions (primary **2501.08313**; this detail appears only in the survey's source comments, not its published text)."* Primary named, venue correctly characterised. |
| 17 | **A14/M3** — *"Nemotron-4 *'majority already-seen tokens reweighted'* is an **unsourced quotation** — the only quoted string in the spec not traceable to the evidence base."* | **CLOSED by deletion** | `already-seen` **0**, `Nemotron` **0**. The overlay list at L162 is now the six traceable recipes only (OpenCoder 84/16, Zamba 60/40, Phi-4 70/30, Llama-3 probe 70/30). |
| 18 | **A7** — *"§7.5 declares 'Long-context stays **≥4% regardless**'; the spec's own anneal runs it at 2.7%."* | **CLOSED by deletion of the clause** | No `≥4% regardless` anywhere. H1's refute action (L283) is instead *"raise curated lane to 9.4%, take from web"* — a direction, not a floor, so there is nothing left to violate. The anneal long-context of 2.78% is now stated as a derived residue of the 62.5/37.5 construction (L223). |
| 19 | **F12** — *"§7.5's long-context floor is defended by a result about a different object — DD's catastrophic setting is a length mixture with no D12/D13 buckets, not a 0% curated lane."* | **CLOSED** | The floor is gone (item 18), and L63 now states the threshold result on the **bucket** axis where it belongs (*"multi-doc QA is ≈0 until pretraining sequences exceed the eval context"*), with the lane recast at L72 as *"the top-up guaranteeing non-empty ≥8k buckets."* Object and axis now match. |
| 20 | **F11** — *"'long-context exposure is **cycled through the whole main run**' — the table says otherwise: 61.8% of the lane is in the final 25% of the run."* | **STILL OPEN** | L166 repeats *"cycle long-context exposure through the whole main run"* and the §6 table is unchanged: 1 / 2 / 3 / 11% → **2 / 14 / 18 / 55B**, i.e. **61.8%** of the 89B lane in the final 25% and **18.0%** in the first 45%. v5's own §1.3 supplies the answer and never uses it: with packing, ≥8k exposure per stage is **7.3% / 7.7% / 8.2% / 16.0%** (`0.094 × (web+code tokens) + curated`), so the *buckets* are non-empty in every stage while the *curated lane* ramps. Two schedules, both legitimate; say so in one clause and quote those four numbers. As written, the sentence contradicts the table. |
| 21 | **§3.2/F14** — *"The curated lane's distinct job is **multi-document reasoning**' — the inventory contains **no multi-document data** ... and 60% of it is the repo-level packing the spec cites OpenCoder to reject."* | **CLOSED on half, STILL OPEN on half** | Half 1 **closed, and inverted into a disclosure**: L74 *"the curated inventory is **repo-packed code 60B + packed books 40B**, neither of which is multi-document; so the lane's job is *long single-document* context, and the multi-document capability MDQA measures is **not** funded by any dataset we hold. That gap is real and is H1's actual risk."* It is repeated at §8 item 4, §9 bullet 3, §10, and the closing attack line. Half 2 **open**: v5 rejects repo-level granularity for code at L28 and funds 60% of its long-context lane with repo-packed sequences at L74 without reconciling. The available answer — dedup at file level, then *pack* survivors by repo; granularity of dedup ≠ unit of packing — is one clause and is missing. |
| 22 | **§3.1** — *"The reasoning lane's *actual* trace supply is **7.1B**, not 85B ... The 2.0× repeat headline is only true if V4's own output counts as reasoning-trace supply."* | **CLOSED, exemplarily** | L54–57: trace-shaped pool itemised at **7.1B** (OpenThoughts2 3 + OpenMathReasoning 2 + OpenR1-Math 1.6 + NuminaMath 0.5), AON 78B named separately as *"Academic reasoning text"*, and L57 *"**The trace-shaped pool is 7.1B, not 85B; long-CoT is 4.6B.** The 2.00× lane ratio is comfortable only because 92% of the lane is AON academic prose ... which is **not** chain-of-thought."* Allocation 28.4 + 141.6 = 170.0 ✓; epochs 4.00 and 1.8154 ✓. Listed again in §8 item 3, §10, and the attack line. |
| 23 | **F13** — *"Tier C is labelled 'repeat' where the course's own classifier says 'must synthesize' (5.06× > 4×)."* | **PARTIALLY CLOSED** | The verdict word is gone — L82's column is now a numeric **Repeat** *factor* (`5.06×`), not a classification, and §8 lists tier C as a starved slot with cleaning directed at it. But v5 never states that by `widget_1.classify()` (`demand ≤ 4×supply` → repeat, else must-synthesize) **25.3B against 5.0B is in the must-synthesize band**, while §1 imports those three labels for the seven lanes. A reviewer who opens the composer still lands the point. Also still missing (M12): 5.06× sits *below* Two-Phase's measured 6-epoch organic ceiling, which is the one number that partially defends the tier. |
| 24 | **F3** — *"'The two changes from the course preset' is **six** changes ... long-context releases 1.55pp while reasoning takes 2.50pp. The missing **0.95pp = 19B** is taken silently from Indic, STEM, web and code."* | **CLOSED, best-in-document** | §1.1 (L32–46) tabulates all six deltas with token amounts and L46 states: *"Reasoning's +2.50pp is funded by long-context's −1.55pp plus **0.95pp (19B)** drawn from STEM, Indic, web and code. The 0.95pp is a real cost, and it lands hardest on **STEM, the 0.92× lane with no headroom**."* I verify: deltas +2.50 / −1.55 / −0.55 / −0.20 / −0.15 / −0.05 / 0.00 sum to **exactly 0**, 0.95pp × 20 = **19.0B**, and H4′ (L287) exists to monitor precisely the lane that pays. |
| 25 | **N10/F15** — *"'5 seams' — five stages have **four** internal boundaries; 4×20 = 80B (4%), not 100B (5%)."* | **CLOSED** | L269: *"**Seams: 4 transitions × 20B blended = 80B, 4% of the main run.** Five stages have four boundaries."* |
| 26 | **N7/§3/F-R3** — *"**Reasoning: zero inventory datasets named. Long-context: zero.** Two of the three slots the assignment names by hand are unpointed."* | **CLOSED** | Agentic: nine datasets with token counts (L105). Reasoning: five (L54–55). Long-context: both, with counts (L74). All match widget 9's line items exactly — I re-checked `Repo-packed code (32K+)` 60e9 and `Book-length corpora (packed)` 40e9 in the source. |
| 27 | **N8/§6/M1** — *"R6/E10: bare `B0–B1` labels, no definitions, no examples; no reasoning-length band system at all. **Stated twice, so weighted twice.**"* | **CLOSED** | §6a: six bands, widget 7's `DIFF[]` definitions **verbatim**, plus an original concrete example and lane mapping for each. §6b: four rungs with steps, trace tokens, solve rate, first step of the worked example, share and token allocation. This converts the largest single point loss in v3. |
| 28 | **N-M6/§7/M2** — *"R8: `clean` occurs **0** times."* | **CLOSED** | §8 (L315–328) names starved slots on **two independent definitions** (≥8% funding rule; supply ratio), orders six cleaning targets, quantifies the marginal value of the top one (*"Every 100M real trajectory tokens cuts the generated fraction by ~2 points"*), and states where cleaning is *not* needed (web, at 0.15×). |
| 29 | **§4-citations** — *"**FATAL. The course's own funding rule is never mentioned, and two lanes fail it** (`WEIGHTED_MIN = 8`)."* | **CLOSED** | The rule is now load-bearing in three places: L50 uses it to force reasoning off 6% (*"starved by the course's own rule"*), §1.3 confronts long-context's 4.45% head-on and answers with 17.7% effective ≥4k exposure, and §8 uses it as one of the two definitions of "starved" (agentic 2.00%). |

**Tally: 24 CLOSED · 3 PARTIALLY CLOSED (#2, #12, #23) · 2 STILL OPEN (#20, #21-half) · plus #21 half-closed.**

### Newly broken or newly weak in v5

| # | Finding | Severity |
|---|---|---|
| 30 | **The protected floor undershoots the course constant it replaces.** `widget_3` line 365: `const LANE_FLOOR=0.08;   // 8% of trained tokens reserved for Indic + agentic` — the course's 8% is **already** Indic+agentic only, and the widget's UI text confirms it (*"a fixed 8% of every iteration is forced to be Indic + agentic"*). v5 ships **7.5%** for that identical membership set and justifies the reduction by *excluding reasoning* (L184: *"hence 7.5% rather than V4's 8%"*) — a reason that cannot apply, because reasoning was never in the course's 8%. The defence v5 needs is sitting in its own feasibility table: at 6.0% Indic the real-token requirement is 120B against 113.9B = **1.05 epochs**, so **5.5% is the largest Indic floor that stays under one epoch of real Indic**, and the course's 8% is therefore unreachable *with real tokens*. Say that and the deviation becomes forced instead of arbitrary. | **WEAK (deviation from a course constant, defended by a non sequitur)** |
| 31 | **§6's printed anneal row sums to 100.2** under a header claiming 100 — see closure item #2. Same round-half-up mechanism as FATAL-1. | **FATAL (recurrence)** |
| 32 | **"62% ballast + 38% reserved" does not reproduce its own table.** The reserve components sum to **30.0B** (9.6+6.4+4.4+3.6+3.0+1.6+1.4) and the ballast that produces the printed effective mixture is **50.0B** — i.e. **62.5 / 37.5**, not 62/38. At a literal 62/38 the ballast is 49.6B and web comes out at 20.97%, not the printed 21.16%. The mixture is internally exact at 62.5/37.5 (I reproduce all eight lanes to 4 dp and the sum to 100.0000); only the *label* is 0.5pp off, in a section whose whole argument is a ballast fraction. Print 62.5/37.5. | **WEAK** |
| 33 | **The corpus-wide synthetic total is understated by ~1.0B and is internally inconsistent about 1.4B.** L132 uses *"agentic generated 42.5B"*. Consistently with §5's own statement that the real component is the entire 627M pool at 4 epochs (2.508B), generated agentic is 46.0 − 2.508 = **43.49B**, and the 42.5B figure only appears if the 1.4B component §4 labels **real** is counted as generated while the 1.0B agentic ballast is excluded. Corrected total 117.4B = **5.64%** of 2.080T; v5 prints 116.4B = 5.60%. Additionally the Indic-D mass in the *anneal* (~1.7B, from 22% of the 7.9B Indic ballast) is omitted, giving ~119.1B = **5.73%** — which is the 5.7% the rubric reviewer independently computed. Conclusion (compliant corpus-wide) is unaffected; the direction of the error is self-favouring, which is the direction E9 punishes. | **WEAK** |
| 34 | **"8.5% is the smallest share clearing that line" (L50) is false.** `SLOTS.forEach((s,i)=>{ (vals[i]>=WEIGHTED_MIN?funded:starved)...})` — the test is `>= 8`, so **8.0%** clears it. The extra 0.5pp = 10B is a choice, not arithmetic forcing, and it is part of the 0.95pp taken from lanes with no headroom. This slightly undercuts both *"Arithmetic forcing, not preference"* (L50) and *"Only two are choices"* (L34). | **WEAK** |
| 35 | **"every threshold is set outside that band" (L279) is false for H4′,** whose *confirm* side is *"STEM loses ≤ **0.5 pt**"* against a stated noise floor of **0.60pp / 0.86pp**. More generally, all eight hypotheses have an **undefined middle band** (H1 75–90%, H2 +1.0 to +3.0, H4 0 to +1.0, H4′ 0.5 to 1.0, H5, H6, H7) and no default action is stated for landing in it. Numeric thresholds exist, which is what E11's "highest" tier asks for; the dead zone is a quality deduction, not a tier blocker. | **WEAK** |
| 36 | **STEM's supply figure now contradicts v5's own reserve table.** §1 prices STEM against **250.0B** (the course's `SUPPLY_T`), while §4 prices the STEM reserve against *"peS2o 42B + proof-pile-2 55B"* = **97B**. Widget 9's only STEM-shaped line items are peS2o 42 + proof-pile-2 55 + `D4 STEM (V4)` 49 = **146B**. At 146B, demand 229B is **1.57×** pre-selector and **3.92×** post-selector — not the printed 0.92×/2.29× — and §1.1 removes a further 0.55pp from this lane. This was WEAK-12/M9 in v3; v5 makes it sharper by naming a 97B pool for the same lane. It is now the strongest remaining E7 attack. | **WEAK, escalating** |
| 37 | **§1's Indic row still counts 162B of synthetic as unique supply** (316/276 = 1.14×). v5 *does* publish the real-only pool (113.9B) in §5's feasibility table but never re-prices the §1 row, where real-only is **316/113.9 = 2.77×**. E7's word is "real supply". One extra cell closes it. | **WEAK (carried over)** |
| 38 | **The submission surface was not updated.** `README.md` L7/L154 name `SOLUTION_v3.md` as the primary deliverable; `SOLUTION_v5.md` occurs **0** times. README L61/67/82/84/112/125 still ship `33.9%`, `63.5×` (twice), *"five seams"*, *"8% ... Indic + agentic + reasoning — real tokens only"*, *"+3.4 avg"*, and the retracted *"multi-document reasoning, which web spans do not provide"*. | **FATAL for the grade, trivial to fix** |
| 39 | **"reproducible from this repository" (L298) has no artifact.** §7(b)'s micro-replication is internally coherent — I verified every figure below — but no script exists in the repo (`session_5_era_v5/` contains no analysis code for it). Either commit the ~30 lines or drop the word "reproducible". | **WEAK** |

---

## 2. Independent re-verification of v5's new arithmetic

Recomputed from source values in a clean kernel; nothing read off the document. **36 of 41 exact.**

**Lane shares and demand.** Stage weights 200/700/600/500 on the §6 profiles: rows sum to 100 / 100 / 100 / 100, budgets sum to **2000**. Time-average → web 33.85, code 23.95, reason 8.50, long 4.45, indic 15.80, STEM 11.45, agentic 2.00; **Σ = 100.0000**; deviation from the declared column **0.0000 pp** (v5's L300 claims "within 0.05pp" — it understates its own precision by an infinite factor; say 0.00). Demands 677.0 / 479.0 / 170.0 / 89.0 / 316.0 / 229.0 / 40.0, **Σ = 2000.0**. ✅

**Supply ratios.** Pre-selector 0.1504 / 0.4355 / 1.1449 / 0.9160 / 1.9977 / 0.8900 / **63.796**; post-selector (÷0.40) 0.376 / **3.307** (on 362B) / 2.862 / 2.290 / 4.994 / 2.225 / **159.49**. All match. ✅ Code effective pool 1100 × 0.329144 = **362.06B**, ratio **1.3230×**. ✅

**Funding table.** ✅ Closes to zero exactly: `+2.50 = 1.55 + 0.95`; deltas −0.55 / −0.20 / −0.15 / −0.05 on STEM / Indic / web / code; token column −11 / −4 / −3 / −1 and +50 / −31; 0.95pp × 20 = **19.0B**.

**Floor feasibility.** ✅ Indic 5.5% × 2000 = **110.0B**; real A+B+C = 64 + 24 + 20.9 + 3 + 2 = **113.9B** ("114B"); 110/113.9 = **0.9658** → 0.96 ep. Agentic 2.0% × 2000 = **40.0B**; 40/0.627 = **63.796** → 63.8 ep.

**Agentic band table.** ✅ All eight cells. Real 4 ep = 2.508B = **0.1254%**; 6 ep = 3.762B = **0.1881%**. Ceilings: 80/20 → 0.157 / 0.235; rephrase ≤30% → 0.179 / 0.269; 50/50 → 0.251 / 0.376. Band **0.125–0.376%**; 2.00/0.376 = 5.3× and 2.00/0.125 = 16.0× → *"5–16× outside it"* ✅. Whole-plan 46.0B / 0.627 = **73.365×** ✅. Generated fraction 43.49/46.0 = **94.5%** → *"6/94"* ✅ (see #33 for the 42.5B component).

**Reserve.** ✅ Components sum to **30.0B**; real/derived 22.0B and generated 8.0B; 8/30 = **26.7%** → "27% of the reserve". Every quantile ↔ epoch pair divides exactly against the pool it names (table in closure item #10).

**Anneal effective mixture.** ✅ At ballast 50.0B: web 21.1562 / code 22.9688 / indic 21.8750 / STEM 9.1562 / reason 9.0625 / agentic 7.5000 / v-synth 5.5000 / long 2.7812 — **Σ = 100.0000**, and every printed 2-dp value matches. Agentic 6.0B confirms §3's 46.0B total. Label caveat #32.

**Mixture shift.** ✅ ½·L1(main → anneal, 8 lanes) = **17.6375%** → 17.64. Course preset pair (`pretrain` → `anneal` in `widget_1.PRESETS`) = **32.0%**. 1 − 17.6375/32.0 = **44.88%** → *"45% gentler"*. Spark Joy ½·L1 = **41.05%** ✅.

**Anneal size.** ✅ 80/2080 = **3.8462%** → 3.85%, matching OpenCoder's 100B/2.6T = 3.846%.

**Corpus-wide synthetic.** 69.5 + 42.5 + 4.4 = 116.4B = **5.596%** of 2.080T → "5.6%" ✅ *as printed*; **43.49B** is the consistent agentic figure → 117.39B = **5.644%**, and with anneal Indic-D ≈ 5.73% (#33). Invented-textbook class 4.4/2080 = **0.2115%** ✅ under ≤3%.

**Trace budget.** ✅ 4 × 7.1 = **28.4B**; 15/30/35/20 → **4.26 / 8.52 / 9.94 / 5.68**, Σ = 28.4; academic 141.6/78 = **1.8154** → 1.82; 28.4 + 141.6 = 170.0 = the lane demand. **ULTRA 5.68 / 4.6 = 1.2348× → 1.23×** ✅.

**Long-context packing table.** ✅ Web ≥4k 0.229 × 677 = **155.0**, ≥8k 0.094 × 677 = **63.6** → "64B"; code ≥4k 0.229 × 479 = **109.7** → "110B", ≥8k = **45.0**; curated 89 at both; totals **354B = 17.7%** and **198B = 9.9%**. *New caveat:* applying **RefinedWeb's** length distribution to the **code** lane (110B / 45B) is an unsourced transfer — DD measured web, not repositories. It is 31% of the ≥4k total; flag it or drop the code row (which still leaves 244B = 12.2%, clearing 8% by 1.5×).

**Seams and spike.** ✅ 4 × 20B = **80B = 4.0%** of 2000B.

**FLOPs.** ✅ 6 × 1.2e11 × 4.0e10 = **2.880e22**; 6 × 1.2e11 × 2.0e12 = **1.440e24**; ratio **0.0200 = 1/50** exactly; 12 × 2% = **24%**.

**§7(b) micro-replication** (claimed as executed). Internally coherent: 342 documents + 38 chunk-boundary splits = **380** fragments ✅ (and 38/342 = **11.1%** ✅); 78,581/342 = **229.8** ✅, /380 = **206.8** ✅, /1375 = **57.1** ✅; 3452.5/421.1 = **8.199×** → "8.20×" ✅; published comparator 1344/930 = **1.445×** → "1.45×" ✅; 59 × 733.3 / 78,581 = 55.06% kept → **44.9% discarded** ✅ (the same 44.9% reused in §5 and §6c). Only gap: no committed script (#39).

---

## 3. Widget verification

Every widget-derived claim in v5 checked against the source file.

| v5 claim | Widget source | Verdict |
|---|---|---|
| `{key:"agentic", name:"Agentic / tool-use", floor:2}` and *"`normalize()` will not let any slider below it"* (L120) | `widget_1` L284 — quoted **verbatim including the `name` field**. `normalize()` clamps to `floor`. | ✅ exact |
| `WEIGHTED_MIN = 8` — *"a lane needs at least this share to move its benchmarks"* (L50) | `widget_1` L293, comment verbatim; used at L481 to build `funded`/`starved` | ✅ exact (but the test is `>= 8`, not `> 8` — see #34) |
| Per-lane composer floors `indic ≥ 12`, `agentic ≥ 2` (L205) | `widget_1` L287/L284 | ✅ exact |
| Course preset pair used for the 32.0% comparator | `widget_1.PRESETS.pretrain = [24,2,6,6,16,12,34]`, `.anneal = [20,8,18,8,28,10,8]` | ✅ exact |
| Composer default Indic tiers A40/B25/C20/D15 (L80) | `widget_1.TIERS` = 40 / 25 / 20 / 15 | ✅ exact |
| Verdict labels covered / repeat / must-generate | `widget_1.classify()` thresholds `≤ supply`, `≤ 4×supply`, else | ✅ used correctly on the seven lanes; **not** applied to tier C (closure #23) |
| *"Widget 3 marks `indic: scarce:true`, `agentic: scarce:true`, `reasoning: scarce:false`"* (L174) | `widget_3` L350–354: `agentic {scarce:true}`, `indic {scarce:true}`, `reasoning {scarce:false}`, `web`/`code` false | ✅ exact |
| English proxy `[0.70, 0.53, 0.33]` (L174) | `widget_3.PROXY.english.vec` | ✅ exact |
| Proxy scores **code 0.841 / reasoning 0.818 / web 0.776 / agentic 0.602 / indic 0.567** (L176–182) | recomputed `dot(domain.vec, proxy)`: 0.84140 / 0.81760 / 0.77640 / 0.60200 / 0.56740 | ✅ **all five exact**, and the ordering claim *"Reasoning scores third, above web"* holds |
| `keepFrac = 0.40` (L6, L184) | `widget_3` L373; `effMult()` gives 6.0× at 0.40 | ✅ exact |
| Widget 7 `DIFF[]` definitions (L231–238) | `widget_7` L287–294: B0 Nursery *"simple children's sentences"* → B5 Research/PhD *"research and PhD-grade papers"* | ✅ **all six verbatim** |
| *"alongside difficulty: short, medium, long and ultra traces are separate rungs. A hard problem with a short trace and an easy one with an ultra trace are not interchangeable, so trace length is scheduled too."* (L246) | `widget_7` L236 — verbatim from *"alongside difficulty"* onward | ✅ exact |
| Widget 6 step counts **2 / 4 / 6 / 14** (L252–255) | `widget_6.LEVELS[].steps.length` = **2 / 4 / 6 / 14** (ULTRA is L236–249, fourteen elements) | ✅ exact. **ULTRA = 14 steps** — note this corrects `redteam-rubric.md` L392, which says "13 steps" |
| Trace tokens **37 / 74 / 161 / 346** | re-ran `TOKRE=/[A-Za-z]+|\d+|[^\sA-Za-z0-9]/g` plus the `"The answer is 467."` tail: **37 / 74 / 161 / 346** | ✅ exact |
| Solve rates **61.5 / 76.8 / 90.9 / 95.3%**, curve `acc(L) = 0.955 − 0.615·exp(−L/τ)`, `τ = 0.18·ultra` | `BASE=0.34, PLATEAU=0.955`, `TAU=ULTRA_TOK*0.18 = 62.28`: **61.55 / 76.76 / 90.86 / 95.26** | ✅ exact; `0.955 − 0.615` = the widget's `PLATEAU − (PLATEAU − BASE)` |
| *"ULTRA **+4.40 points** over HIGH for **2.15×** the tokens, tripping the widget's 'wasted effort' flag at +5.0"* (L259) | recomputed gain **4.399 pp**, ratio **2.1491×**; `isWasted()` fires when `ULTRA_GAIN < 0.05` | ✅ exact, including the threshold semantics |
| **Answer 467** at every band (L248) | `widget_6.ANSWER = "467"`, one shared problem | ✅ exact |
| First-step examples per band | LOW/MEDIUM/HIGH quote `steps[0]` verbatim. **ULTRA's** *"Restate the goal… then verify two independent ways."* elides **two** steps (`steps[0]` + `steps[1]`) into one ellipsis | ✅ / ⚠ minor: it reads as one step; use `steps[0]` alone |
| Widget 8 `peakFactor = 1 + effSharp·A·effFrozen`, `RED_T = 3.0` (L270) | `widget_8` L239 `RED_T=3.0`; L244 `A=7, F=21.4, C_W=1.5, C_F=2.0`; L259–261 the three formulas | ✅ exact |
| *"at a 20B band, **1.34×** with frozen embeddings and **1.23×** unfrozen"* | at sharpness 1.0: frozen **1.3382**, unfrozen **1.2258** | ✅ exact |
| *"~**6B** already clears it frozen"* | `peakFactor(1, b, frozen)` crosses 3.0 at **b = 5.58B**; 6B → 2.798 | ✅ correct and conservative |
| *"V4's ~150× corresponds to sharpness 1.0, frozen embeddings, zero band"* | `1 + 1.0 × 7 × 21.4 = **150.8**`; widget headline *"~150x"* | ✅ exact |
| Widget 9 inventory: reasoning 3 / 2 / 1.6 / 0.5 / AON 78; long-ctx 60 + 40; Indic 64 / 24 / 162 / 20.9 / 3 / 2; agentic nine items = 627M; STEM peS2o 42 + proof-pile-2 55 | all line items match `widget_9` `tokens:` fields | ✅ exact. Two residuals: widget 9 tags `Sangraha (synthetic)` as **`tier:'C'`** (v5 discloses the translated-component premise but never quotes the tag), and widget 9's STEM itemisation totals **146B**, not 250B (#36) |

One extrapolation to flag: widget 8's band slider is `min=0 max=5` **B tokens**. v5 evaluates the model at a **20B** band, 4× beyond the interactive range. The formula is monotone and well-behaved there, and the direction is conservative (a wider band can only lower the peak), but the number is an extrapolation of a course model, not a reading of it — worth one parenthesis.

---

## 4. R0–R8 / E1–E11

| ID | Requirement / criterion | v5 | Specific remaining element |
|---|---|---|---|
| **R0** | Written spec, "specific enough to defend" | **PASS** | Reads as a defensible spec throughout. Deduct: the `63.8%`-for-`63.8×` typo (L107), the 62/38 label (#32), and — outside the file — the README still names v3 (#38). |
| **R1** | Share for every capability slot | **PASS** | Seven lanes with share / demand / unique supply / pre- and post-selector ratio / verdict; exact shares sum to 100.0000. Deduct: §6's printed anneal row sums to 100.2 under a header claiming 100 (#31). |
| **R2** | Indic split verified / unverified / translated / synthetic | **PASS** | Four tiers with share, demand, named supply, repeat factor; composer default shown non-fundable at 12.6×; real 78 / synth 22 checked against a ceiling whose *type* is argued (rephrase-class, not textbook-class); weakest premise volunteered and routed to cleaning. |
| **R3** | Agentic + reasoning + long-context → inventory datasets | **PASS** | 3-for-3, with token counts, all matching widget 9. The naming surfaced two honest liabilities (7.1B trace pool; no multi-document data) and v5 published both. |
| **R4** | **Fixes** the floor the selector cannot cross | **PASS** | Per-lane 5.5% / 2.0%, membership derived from `widget_3.scarce`, real-token clause scoped by a feasibility table, binding analysis given ("never binds under this mixture ... claiming otherwise would oversell it"). Deduct: 7.5% < the course's 8% for the same two lanes, with a reason that does not apply (#30). |
| **R5** | Declares the anneal reserve **held back** | **PASS-minus** | Seven components with pool, quantile, epochs and real/derived/generated label; two labelled as not-yet-existing; withholding named on the difficulty axis (B5 reserve-only), the lane axis (v-synth absent from all four main stages) and the share axis (agentic pinned at 2). Deduct: tier-A Indic's 9.6B is not withheld — the main run already runs tier A at 1.98 epochs (closure #12). |
| **R6** | Difficulty **and** reasoning-length bands, concrete example each | **PASS** | Both systems; six difficulty bands with widget-verbatim definitions plus original examples and lane mapping; four length rungs with steps / tokens / solve rate / example / share / token allocation. Deduct: ULTRA's example fuses two steps. |
| **R7** | Commits to 1B **and** 3B proxy runs before trust | **PASS** | Eight hypotheses across 1B and 3B, FLOP-priced at 1/50 of a run, Llama-3 branch protocol (30/70, LR→0), and an escalation path when 3B cannot separate. |
| **R8** | Cleaning aimed at the starved slots | **PASS** | Two independent definitions of "starved", six ordered targets, marginal value of the top target quantified, and an explicit non-target. |
| **E1** | Holds up when pushed on every number | **PASS-minus** | 36 of 41 recomputed quantities exact, and the five load-bearing v3 accounting holes are closed. Against it: #31 (a printed row that does not sum under a header claiming it does), #32, #33, #34, #35, #36. A grader who adds the anneal row reads the rest harder — same dynamic that capped v3. |
| **E2** | Reasoning quality **and the evidence behind the choices** | **PASS** | Every previously-flagged misattribution corrected at the source, not papered over: relative-vs-absolute, phase-lengths-vs-tasks, published-vs-commented, plus new scale caveats (Collapse's nanoGPT, DD's 1B-only RoPE and its Table 2/Table 4 conflict, Demystifying's interpolated 30%, Spark Joy's cruising LR). §9 volunteers six disqualifying limitations. The strongest E2 move in the document is citing Preference Curriculum **against** its own difficulty ladder (L242). |
| **E3** | Tightly argued; **padding earns nothing** | **PARTIAL** | **12.3% cuttable (4,654 B)** — down from v3's 26% — but the ratio still costs marks, and §7's "reproducible from this repository" has no artifact behind it. Full byte-level plan in §6 below. |
| **E4** | **Defended** share for every lane | **PASS-minus** | §1.1 converts the four previously-undefended main-run deviations into *derived* quantities with a stated cost and a monitoring hypothesis, and §4 states plainly that the anneal's code/reason/STEM/agentic values are *derived* from the 62/38 construction rather than chosen — which is the honest answer to v3's four undefended anneal lanes. Deduct: STEM 11.45% still rests on a supply figure that contradicts the reserve table (#36). |
| **E5** | Indic tiers stated | **PASS** | Fully, and used downstream (reserve, H3, cleaning target 2). |
| **E6** | Benchmarks show **why each number is what it is** | **PASS-minus** | The course's own funding rule now drives a magnitude (reasoning ≥ 8), and the two lanes that fail it are confronted rather than decorated: long-context with a 17.7% effective-exposure answer, agentic by being named starved and routed to cleaning. Deduct: the 0.5pp above 8.0 is undefended (#34), and web / code / STEM magnitudes are still preset-inherited. |
| **E7** | Sized against **real supply from the inventory** | **PASS-minus** | Post-selector column, code's 362B effective pool, the 7.1B trace disclosure, per-tier Indic supply, and a real-only Indic pool in the floor table. Deduct: STEM 250B vs 97B vs 146B (#36); §1's Indic row still counts 162B of synthetic as unique (#37). |
| **E8** | Says **plainly** where repeating or generating is needed | **PASS (strong)** | "repeat" / "must generate" in the headline table, `73.4×`, the defensible band with *"We ship 2.00%, which is 5–16× outside it. Stated here, not buried"*, every reserve row labelled real / derived / **generated**, and *"FIM ... creates **zero new tokens**"* — the v3 category error retired in one clause. |
| **E9** | No quiet over-allocation to a supply-poor lane | **PARTIAL** | Disclosure is now maximal and *quantified against v5's own ceilings*, the 2% is shown to be a course clamp rather than a choice, and the fallback no longer breaks the floor it invokes. Per E9's own grammar the penalty attaches to the **allocation** and only the adverb attaches to the disclosure, so this cannot reach PASS while the share is 5–16× outside the band the document itself computes. It is, however, the best-executed thing in the file, and #33's self-favouring 1B slip is the only place the "quiet" charge gets any purchase. |
| **E10** | Bands with a real example at each level | **PASS** | See R6. Stated twice, so this is the largest single recovery from v3. |
| **E11** | Tiered ceiling | **Tier 3 of 4 — "highest"** | See §5. |

**Requirement axis** (R0–R8): 0.90 + 0.90 + 0.95 + 0.95 + 0.90 + 0.80 + 0.95 + 0.95 + 0.90 = 8.20/9 = **0.911**
**Criterion axis** (E1–E11): 0.85 + 0.92 + 0.75 + 0.85 + 0.95 + 0.75 + 0.80 + 0.95 + 0.70 + 0.95 + 0.78 = 9.25/11 = **0.841**

---

## 5. E11 — tier reached, and what blocks the next one

**Tier reached: 3 of 4 — "highest".** The rubric's test is *"specifies a concrete proxy experiment at 1B or 3B **AND** names the metric that would confirm or refute their mixture"*, and the parent's gloss is *"named metric + threshold + scale"*. All eight hypotheses satisfy all four elements:

| | Scale | Metric | Confirm | Refute | Action |
|---|---|---|---|---|---|
| H1 | 1B, 100B, 4 arms | MDQA-30 | ≥90% of the 9.4% arm | <75% | raise lane to 9.4% |
| H2 | **3B**, 40B branch | SWE-bench Verified pass@1, BFCL AST-match | ≥ +3.0 pts | < +1.0 pt | keep 2.00%, swap composition |
| H3 | 1B, 100B | IndicGenBench chrF, MILU | within 1.0 pt | > 1.0 pt below | C → 4% |
| H4 | 1B, branch 96/98% | MMLU+GSM8K+HumanEval avg | ≥ +1.0 pt | ≤ 0 | revert to 40B |
| H4′ | 1B, 100B | GPQA + MATH | ≤ 0.5 pt loss | > 1.0 pt | return 0.55pp |
| H5 | 1B | MILU + Flores-101 chrF; MMLU | ≥ +1.5 / ≤ 1.0 loss | > 1.0 loss | flatten Indic |
| H6 | 1B | peak gradient-norm multiplier | < 3.0× (`RED_T`) | > 3.0× | widen band |
| H7 | 1B, 100B | LOW:ULTRA length ratio + accuracy | ratio ≥ 4× | < 2× | widen spread |

Thresholds are anchored to a stated single-seed noise floor (0.60pp / 0.86pp), which is what makes them gradeable rather than decorative — and H2's *"threshold caveat we must own"* pre-empts M4, the question all three reviewers called the best in the room, by naming the escalation (7B) and the metric that survives at small scale (BFCL AST-match). This clears the bar all three prior reviews said was missed.

**What blocks "very highest": nothing but execution.** The tier requires *"actually run that proxy and bring the numbers back"*. v5 correctly declines to claim it (L296) and instead reports two things that *were* executed — the mixture arithmetic and a micro-replication of DD's `Σl(l−1)/2Σl` on a 342-document corpus. Both are real and I reproduced both, but neither is a **mixture proxy at 1B/3B**, so the tier is unreachable as submitted. The cheapest genuine crossing is **H7 at reduced scale**: it needs no benchmark harness, only a trace-length ratio and per-band accuracy, and it is the one hypothesis whose confirm criterion is already implied by the design (346/37 = 9.35× against a ≥4× bar). Second cheapest is **H6** — a gradient-norm trace at 1B across bands 0 / 5 / 20B, which is a single-metric run against a course-given threshold. Either one, with numbers in a table, moves E11 from 0.78 to ~0.95 and the total by roughly +8 marks; more importantly it is the only remaining path to the assignment's top band.

Secondary deduction inside "highest": every hypothesis has an undefined band between confirm and refute, with no stated default (#35), and L279's *"every threshold is set outside that band"* is false for H4′'s 0.5pt confirm.

---

## 6. E3 — byte-level padding audit

**Measured: 37,708 bytes / 359 lines. Section budget:**

| Bytes | Lines | Section |
|---|---|---|
| 756 | 1–11 | header / budget / selector / Chinchilla |
| 1,982 | 12–31 | §1 lane shares |
| 907 | 32–47 | §1.1 deviations and funding |
| 980 | 48–58 | §1.2 reasoning |
| 1,423 | 59–77 | §1.3 long-context |
| 2,763 | 78–102 | §2 Indic tiers |
| 3,477 | 103–137 | §3 agentic |
| 4,588 | 138–169 | §4 anneal reserve |
| 3,622 | 170–210 | §5 floor |
| 1,383 | 211–226 | §6 curriculum |
| 2,083 | 227–243 | §6a difficulty bands |
| 2,114 | 244–262 | §6b length bands |
| 2,391 | 263–274 | §6c packing / seams |
| 2,708 | 275–293 | §7 proxy protocol |
| 1,737 | 294–314 | §7 what we ran |
| 1,531 | 315–331 | §8 cleaning |
| 1,579 | 332–341 | §9 no evidence |
| 1,685 | 344–359 | §10 confidence table |

**Every block I would cut, with the byte saving:**

| # | Block | Lines | Bytes | Why it earns nothing | Save |
|---|---|---|---|---|---|
| C1 | **§10 "The numbers most likely to be wrong"** — the whole 9-row table | 344–357 | 1,534 | Pure restatement: every row's content is already in §§1–5 and §9 does the honesty work in prose, better. It also **actively costs marks** — it hands a reviewer a ranked target list with three lanes pre-labelled "Low". Keep the closing *"Attack first"* line (L358, 190 B), which is the only part that earns; fold the two rows carrying anything new (`Decomposition + RoPE 100k` measured-at-1B; `62% ballast` vs Spark Joy's 0.82×) into §9 as clauses. | **1,285** |
| C2 | **§3 items 1, 2 and 4** — the Collapse-family rebuttals | 124–127 | 1,074 | Items 2 and 4 state in their own text that they do not support the plan (*"Outside a theorem is not proof of safety"*; *"This citation marks how far outside the measured region we are; it does not support us"*). Four numbers to refute a self-consuming loop the plan does not propose. Merge 1+2+4 into one item: environment-grounded + verifier-biased + real tokens in every batch, all three declared unmeasured. Keep item 3 (sets the teacher budget) and item 5 (matches widget 5). | **650** |
| C3 | **§6c "Ramp, not step"** | 271 | 468 | After its own two hedges (*"blends two halves of one corpus, not two mixtures"*, *"44× wider than our band"*) and the MiniMax-01 sentence's correct demotion to *"appears only in the survey's source comments"*, the bullet defends no number. Keep one clause: "we take PrefCurriculum's S-shape, not its 43.9% width." | **360** |
| C4 | **§4 "Cyclic, not a tail block"** | 166 | 567 | Concludes that cycling *"interacts with ramp aggressiveness and is not universally good"* and that DD's mechanism *"concerns the main run's LR decay, not the interior of a leg"* — i.e. it argues neither for nor against 4 sub-cycles. Compress to the decision plus the concession. | **340** |
| C5 | **§7(b) prose tail** — the "first attempt used mean span length" lab note | 311 | 635 (partial) | Revision history of the analyst, not of the plan. The overshoot explanation (short-document corpus, 44.9% discarded) is load-bearing and stays; the failed-first-attempt sentence is a notebook entry. | **230** |
| C6 | **§6c seam bullet, DD Fig 8 corroboration** | 270 (partial) | 522 (partial) | *"~8 loss spikes to 7.5–8.1"* immediately followed by *"those arms differ in both packing and curriculum, so it is not attributable to ordering alone"* — a corroboration cancelled in the same sentence. The widget-8 pricing before it does all the work. | **200** |
| C7 | **§2 hazard 1, the Demystifying App. D.2 sentence** | 95 (partial) | 533 (partial) | Two clauses of citation ending in *"so it transfers by analogy only"*, immediately superseded by *"The real evidence is V4: gradient norm ~150×"*. Lead with V4 and the mitigation. | **220** |
| C8 | **§4 "Why 80B" Cluster-A ledger** | 158 (partial) | 533 (partial) | Five Cluster A percentages and two Cluster B to defend one number. The taxonomy sentence plus the two bracketing runs (OpenCoder 3.85%, Hunyuan-Large 4.76%) do identical work. | **200** |
| C9 | **§1 "Filters", the popularity clause** | 30 (partial) | 342 (partial) | `stars>=5` sets no number in this plan. The Low-bucket zeroing does (web-only filtering policy) and stays. | **150** |
| C10 | **§5 closing paragraph** (OPUS/curriculum orthogonality; PrefCurriculum has no floor) | 207 | 249 | True, and it constrains nothing: no share, tier, floor, reserve, band or benchmark depends on it. | **249** |
| C11 | **"Earlier drafts…" framing** at 5 sites | 74, 134, 154, 174, 193 | ~600 | A first-time reader has no access to the earlier drafts, so *"Earlier drafts said X"* is dead weight in a public README; the corrected position is what earns. Keep the corrections verbatim, drop the litigation. (Exception: keep the one at L154, where the *reasoning error* — proving a reserve safe by assuming it is not a reserve — is itself the insight.) | **250** |
| C12 | **§5 evidence rows 1–2** | 199–200 | 268 | *"any lane absent from the objective dies"* and *"different objectives, different winners"* are the same CLIMB point twice. Merge. | **120** |
| C13 | **§0 Chinchilla paragraph** | 8 | 343 | Now correct (closure #3) but the budget is a course given (`runSize = 2`). One sentence: below compute-optimal on unique tokens, and 2T is the presets' kindest setting for scarce supply. | **150** |
| C14 | **§1 code-dedup justification** | 28 (partial) | 345 (partial) | The 32.9% → 362B → 1.32× derivation is load-bearing and stays; *"it wins HumanEval and MBPP at every matched budget"* + the 52B char-identical figure defend a **cleaning** choice, not a share. One clause. | **130** |
| C15 | **§6b "Why all four must exist", Two-Phase sentence** | 261 (partial) | 463 (partial) | Two-Phase's 1.3%-of-phase-2 reasoning share is a different object from a trace-length split; the behavioural argument before it is the real defence. | **120** |
| C16 | **§8 re-derived ratios** | 317 (partial) | 1,531 (partial) | 73.4× / 5.06× / 1.32× / 0.92× are all three sections old by this point. R8 needs the *ordering* and the *directive*, not the re-derivation. | **200** |
| | **Total** | | | | **4,654** |

Plus **C17**, size-neutral and not counted in the total: commit the ~30-line micro-replication script, or delete the words *"reproducible from this repository"* (L298). An unbacked reproducibility claim is worse than no claim.

**Measured padding: 4,654 B = 12.3%** of 37,708 — against v3's measured 26%. **Byte target I would ship: 33,050 B (33.0 KB), −12.3%.**

**Why not ~24 KB.** I disagree with the more aggressive target, and the disagreement is arithmetic rather than taste. Reaching 24 KB means cutting a further **~9.0 KB** *after* the 4.65 KB above, and there is no 9 KB of non-earning prose left. The only blocks that size are: §9 (1,579 B — all three reviewers called it the highest-value section in the document under E1/E2), the honest-notes paragraphs that close FATALs #9/#10/#12/#21/#22 (~1,600 B — deleting them re-opens five closed FATALs), the example columns in §6a/§6b (~1,900 B — that is R6/E10, weighted twice), §7's threshold table (~1,300 B — that is E11's "highest" tier), §5's feasibility table (~600 B — that is R4), and §1.1 (907 B — that is F3). Each of those *is the requirement*. v3 was 26.9 KB **with R3, R4, R6 and R8 absent**; those four repairs cost ~8.7 KB of unavoidable gradeable content, which is why the honest defensible size went **up**. E3 penalises padding, not length — *"a tightly argued short plan will score well"*, and tightness is the operative word. At 12.3% cuttable this document is tight; cutting it to 24 KB would trade ~13 marks of E3 for ~60 marks of R3/R4/R6/R8/E11.

---

## 7. Score

**≈ 438 / 500 (87.6%). Defensible band 425–450.**

Mean of the two axes: (0.911 + 0.841) / 2 = 0.876.

| Prior | Score | Delta |
|---|---|---|
| RedTeamNumbers | 307 | **+131** |
| RedTeamCitations | 310 | **+128** |
| RedTeamRubric | 345 | **+93** |
| mean 320.7 | | **+117** |

**Where the +117 comes from.** Four requirements moved FAIL → PASS (R3, R4, R6, R8), and R6/E10 counts twice — that alone is worth ~70 marks on the requirement axis, which the rubric says *gates* the score. E11 moved from tier 2 to tier 3, worth ~15. The five accounting holes that capped E1 (share sum, OPUS ratios, reserve epochs, seam count, Chinchilla) are all closed, and the three citation FATALs (relative-vs-absolute, phase-length axis, unpublished MiniMax) are corrected at the source rather than hedged — worth ~20 across E1/E2. E3 improved from 26% to 12.3% padding, worth ~5.

**What still caps it below ~470.** In descending marks-per-fix:

1. **Update `README.md`** (#38). Two lines. Until then a grader following the submission link reads v3, and the honest score for the *submission* is ~310–345, not 438. This is worth more than everything else on this list combined.
2. **Print the §6 anneal row at 2 dp** (#31) — one row; removes a FATAL that is a literal repeat of the finding all three reviewers opened with.
3. **Fix 62/38 → 62.5/37.5** and the agentic-generated component to 43.5B (#32, #33) — two numbers.
4. **Reconcile STEM** (#36): state that widget 9 itemises 146B and your own reserve prices 97B, and give the ratio at each; then take the 0.55pp from web instead. This is the attack a reviewer with the inventory open will actually run.
5. **Two clauses** for the open items: separate the length-bucket schedule from the curated-lane ramp with the per-stage ≥8k figures 7.3 / 7.7 / 8.2 / 16.0% (#20), and distinguish dedup granularity from packing unit for the long-context lane (#21).
6. **One sentence** turning the 7.5% floor from arbitrary into forced: 6.0% Indic = 120B > 113.9B real = 1.05 epochs, so 8% is unreachable in real tokens (#30).
7. **Run H6 or H7 at 1B** and bring the numbers back. That is the only route to E11's fourth tier and the assignment's top band.

Items 1–6 are ~15 lines of editing and no new research; they would put this at **~465–475**. Item 7 is the ceiling.

**Attack surfaces I would open with, in order:** the README pointing at v3; the anneal row that sums to 100.2; STEM's three different supply figures (250 / 146 / 97); "cycled" long-context against a table that end-loads 61.8% of the lane; and agentic 2.00% against a self-computed defensible ceiling of 0.376%.
