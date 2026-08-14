# ERA V5 · Session 5 — Data Mixture & Curriculum

Design artifact for **TSAI ERA V5, Session 5: Data Mixtures and Curriculum**.

The deliverable is a written specification that decides how a ~120B model's fixed token budget is split across capability lanes, in what order those tokens are served, what is held back for the final anneal, and which of those numbers survive contact with the actual token supply.

**Primary deliverable → [`session_5_era_v5/SOLUTION_v3.md`](session_5_era_v5/SOLUTION_v3.md)**
**Evidence base → [`session_5_era_v5/papers/EVIDENCE_MAP.md`](session_5_era_v5/papers/EVIDENCE_MAP.md)**

---

## 1. The assignment, summarised

Draft the mixture-and-curriculum plan for V5 as a written specification, *specific enough to defend*. The assignment names eight things it must contain:

| # | Requirement |
|---|---|
| R1 | A share of the budget for **every capability slot** |
| R2 | For the Indic slot, the split across **verified / unverified / translated / synthetic** tiers — "rather than hiding behind a single headline number" |
| R3 | Names the **agentic, reasoning and long-context** slots explicitly, and **points each at datasets from the inventory** that will fill it |
| R4 | **Fixes the protected always-on floor** that the selector is not allowed to cross |
| R5 | **Declares the anneal reserve** held back for the cooldown |
| R6 | **Lays out the difficulty and reasoning-length bands, with a concrete example for each** |
| R7 | **Commits to justifying the numbers via small proxy runs at 1B and 3B** before any is trusted at full scale |
| R8 | Alongside the plan, cleaning continues toward the cumulative target, **now aimed at the slots the mixture shows to be starved** |

Submission is a link to a GitHub repo README. 500 points, individual.

> The governing idea, in the course's words: *"a data decision is a hypothesis until a cheap experiment has tested it."*

## 2. Evaluation criteria, summarised

There is no itemised rubric — the prose *is* the rubric. It sets a graded ceiling:

| # | Criterion |
|---|---|
| E1 | Holds up when **"a reviewer sat across from you and pushed on every number"** |
| E2 | Grade rests on reasoning quality **and the evidence behind your choices** |
| E3 | **"A tightly argued short plan will score well while padding earns nothing"** |
| E4 | A **defended** share for every capability lane |
| E5 | Indic tiers stated across all four tiers |
| E6 | Each lane tied to the benchmarks it must win, **"so a reviewer can see why each number is what it is"** |
| E7 | Every lane **sized against real supply from the inventory** |
| E8 | Says **plainly** where a share can only be reached by **repeating or generating** data |
| E9 | **"A plan that quietly hands a large share to a lane that has almost no real data behind it will lose marks for exactly the wishful accounting this session exists to prevent"** |
| E10 | Difficulty and reasoning-length bands **with a real example at each level** |
| E11 | **Tiered ceiling:** good → a plan · excellent → written as a **testable hypothesis** · highest → **specifies a concrete 1B/3B proxy experiment and names the metric that would confirm or refute** the mixture · very highest → **actually runs that proxy and brings the numbers back** |

Two consequences shaped this repo. **E9** means the honest failure mode is over-allocating a supply-poor lane, so every lane carries an explicit supply verdict. **E11** means a plan is not the top band — a named confirm/refute metric is, and an executed proxy is above that.

---

## 3. What we are proposing

**Budget:** ~120B params · main run **2.00T** tokens · anneal **+80B (4.0%)** · total 2.08T.

### Main-run lane shares

| Lane | Share | Demand | Unique supply | Ratio | Verdict |
|---|---|---|---|---|---|
| General web | 33.9% | 677B | 4.50T | 0.15× | covered |
| Code | 24.0% | 479B | 1.10T | 0.44× | covered |
| Indic | 15.8% | 316B | 276B | 1.14× | repeat |
| STEM / math | 11.5% | 229B | 250B | 0.92× | covered |
| Reasoning traces | 8.5% | 170B | 85B | 2.00× | repeat |
| Long-context (curated) | 4.5% | 89B | 100B | 0.89× | covered |
| **Agentic** | **2.0%** | **40B** | **0.63B** | **63.5×** | **must generate** |

### Indic tiers (share of the Indic lane)

| Tier | Share | Demand | Supply | Repeat |
|---|---|---|---|---|
| A verified native | 40% | 126.4B | 64.0B | 1.98× |
| B unverified crawl | 30% | 94.8B | 44.9B | 2.11× |
| C translated / parallel | 8% | 25.3B | 5.0B | 5.06× |
| D synthetic (rephrase) | 22% | 69.5B | 162.0B | 0.43× |

78% real / 22% synthetic.

### Curriculum

Seed 200B → General 700B → Reasoning 600B → Long-context 500B → **anneal 80B**, with a 20B blended warmup at each of the five seams. The anneal is 60% original-distribution ballast + 40% reserved best data, giving a 19.5% mixture shift.

**Protected floor:** 8% of every iteration's *accepted* tokens for Indic + agentic + reasoning — real tokens only, enforced per length-bucket, per cycle, and inside the anneal mixture as well as the main run.

---

## 4. How we came up with these numbers

The method was **backwards from the benchmarks, then forwards through the supply**. Five steps, in order:

**1. Start from the benchmark, not the corpus.** Each capability was first reduced to a training *shape* via the session's loss-map framing — which tokens carry loss (green), which are context only (grey), which carry a reward with no token loss (violet). SWE-bench means "loss on the patch"; BFCL means "loss on the emitted call". This fixes *what* a lane must contain before any percentage is chosen.

**2. Inventory in tokens, after dedup — never in samples.** The widget-9 inventory is the supply side of every number. Sample counts mislead by orders of magnitude: SWE-Gym is 2.4K samples but 150M tokens, while Glaive is 113K samples and 50M tokens. The code figure was further discounted because ~75% of GitHub files are exact duplicates.

**3. Write shares, then run a coverage check.** Demand = share × 2.00T, compared against unique supply, classified as *covered* (≤1×), *repeat* (≤ the measured organic epoch ceiling), or *must generate*. Any share that fails the check was changed or explicitly flagged — this is the step that produced the two deviations from the course preset, and it is what E7/E8/E9 grade.

**4. Turn repetition into epochs with a real ceiling.** Two-Phase measured organic saturation at 6 epochs for high-quality crawl and ~8 for math, with 12 actively hurting. Everything at or under ~2× repeat is inside that band; anything far past it is a supply problem wearing a repetition costume.

**5. Fill the remainder by type, and name the type.** Synthetic data is not one thing. Rephrasing real documents tops out around 30% of a mixture; inventing content from keywords tops out near 3%. That distinction decides whether a lane's gap is fillable at all.

### The two deviations from the course preset, and what forced them

**Long-context 6% → 4.5%.** Long-context capability is a *threshold*, not a gradient: multi-document QA sits near zero until pretraining sequences exceed the eval context, then jumps and flattens. Raising the 8192-token share from 9.4% to 25% moved the metric by 0.2 points — noise. Meanwhile natural web already supplies ~9.4% of tokens at exactly 8192 if you decompose documents instead of concatenating and chunking them. So most of the capability is a **packing decision**, not a lane purchase. Cutting the curated lane to 4.5% makes it *covered* at 0.89× instead of repeating, and the curated slice keeps its distinct job: multi-document reasoning, which web spans do not provide.

**Reasoning 6% → 8.5%.** A controllable reasoning-effort dial requires a *distribution* of trace lengths, not one slot. 8.5% is 170B against 85B unique — 2.0× repeat, inside the measured ceiling. The budget came from the long-context reduction.

**Anneal 2% → 4.0%.** Published terminal fast-decay legs cluster at 1–5% of a run. The nearest sweep never measured below 50B absolute tokens; our 80B sits inside its measured band, whereas 40B would sit below every point anyone has run.

### The number we did not fix, and why that is deliberate

The agentic lane demands 40B tokens against **0.63B unique** — a 63.5× gap. There is no honest repetition story and no rephrasing story, because rephrasing needs a source document and we do not have 40B tokens of real trajectories to rewrite. The spec therefore states the full arithmetic in the open: **~94% of that lane is generated**, the generation program is environment-grounded and verifier-filtered rather than invented, and a kill criterion drops the lane to 0.5% if a 1B/3B proxy fails to beat a format-data-only baseline. E9 penalises handing a large share to an empty lane *quietly*; the response is to do the opposite of quietly.

---

## 5. How the numbers are backed up

### Nine papers, read in full, figures inspected

Every brief lives in [`session_5_era_v5/papers/<slug>/brief.md`](session_5_era_v5/papers/) and carries the paper's numbers with their setting and location, its assumptions, what it is silent on, and what must not be overclaimed from it.

| Paper | Scale actually tested | What it backs |
|---|---|---|
| CLIMB `2504.13161` | ≤1B, 40B–400B, English | Mixture *search* beats hand-set weights; cheap proxies rank mixtures; searched mixes are sparse and will zero any lane absent from the objective |
| Two-Phase `2412.15285` | 8B/25B, 1T–15T | Order alone is worth +3.4 avg at identical weights; organic epoch ceilings (6 / 8); web quality gating (64% Low → zeroing lifts MMLU 42.94→56.10) |
| OpenCoder `2411.04905` | 1.5B/8B, 2.5T + 100B anneal | File-level > repo-level dedup; a ~4% high-quality anneal with 84% distribution continuity; popularity filters hurt |
| Demystifying Synthetic `2510.01631` | 100M–3B, ≤200B | Safe synthetic ratios *by type*: rephrase ~30%, invented ≤3%; an 8B generator beats a 70B one |
| Model Collapse `2404.05090` | theory + small GPT-2 | Closed self-training loops collapse almost surely; a real-data floor in every generation bounds the drift |
| Mid-Training Survey `2510.06826` | 17-run ledger | Resolves "anneal" into two distinct objects: 1–5% terminal decay vs 9–51% second stage; the 10–40% new-data overlay pattern |
| Spark Joy `2406.03476` | 7B, 1T, 50–300B sweep | The end-of-training phase-length sweep; and the sans-math ablation showing a final phase can drive a starved lane *below* baseline |
| Preference Curriculum `2501.13126` | 1.3B/3B, 100B/1T | Ordering is a domain re-timer with no floor of its own; blended transitions beat hard switches |
| Dataset Decomposition `2405.13226` | 1B–7B, ≤1.1T, 64–8192 ctx | Long-context is a threshold; packing and RoPE base buy more than lane share does; short→long ordering also suppresses gradient spikes |

### Four evidence disciplines

**Every number is traceable to one of four sources** — a paper (with setting and table), the widget inventory, the lecture / V4 run history, or arithmetic shown in the document. A number with no traceable defence is treated as a defect, because E1 grades numbers individually.

**Scale mismatches are declared, not hidden.** Most of this literature is 1B–8B and English-only; we are specifying 120B and multilingual. Where a finding is cited outside its measured range it is marked as such, and the one frontier-scale anneal measurement in the literature is a *null* result at 405B — which is stated rather than omitted.

**Silence is reported as silence.** No paper in the set studied Indic, none trains agentic trajectories at pretraining scale, and none trains beyond 8192 context. The Indic tier split is therefore arithmetic against our own inventory plus a synthetic ceiling borrowed from English experiments, and it is labelled that way. The one quantitative low-resource precedent available cuts its non-English share entering mid-training — the opposite of our proposal — and the spec says so.

**Confidence is graded per number.** The spec closes with a confidence table naming the weakest link behind each figure, and it names the three numbers a reviewer should attack first. Nothing is presented as more certain than its evidence.

### Adversarial review

The specification was put through a red-team pass whose only job was to break it: recomputing every share, ratio, epoch count and mixture-shift figure independently; checking every citation against the paper brief for misquotes, wrong-scale claims and cases where the paper is silent or says the opposite; and grading against the assignment's own requirements with findings labelled *fatal / weak / missing / padding*. That review is what recovered the assignment's full requirement set — the difficulty-and-reasoning-band and proxy-run clauses had been lost to a display truncation, and the correction is why R6, R7, R8, E9, E10 and E11 appear above.

---

## 6. Repo layout

```
session_5_era_v5/
├── SOLUTION_v3.md              # primary deliverable: the V5 mixture + curriculum spec
├── PRETRAINING_SOLUTION_v2.md  # prior iteration, kept for the audit trail
├── papers/
│   ├── EVIDENCE_MAP.md         # cross-paper synthesis against the 7 assignment items
│   └── <slug>/brief.md         # per-paper teaching brief with citable numbers
├── lecture_notes.md            # course source (Session 5)
├── transcript_google.txt       # official session transcript
├── widgets/                    # the 9 interactive widgets; the data models behind every course number
├── transcripts/                # session video captions (VTT) + metadata
├── assignment.json             # assignment text, rubric metadata, submission format
├── session_5.json              # session payload
└── manifest.json               # export inventory with SHA-256 checksums

transcripts/                    # working-session transcripts (Git LFS)
├── session-019ffd64.jsonl
└── session-019ffd64.html
```

## 7. Transcripts are Git LFS objects

The full working session — every tool call, paper read and revision that produced this spec — is exported to [`transcripts/`](transcripts/) in both machine-readable and human-readable form:

| File | Size | Format |
|---|---|---|
| `session-019ffd64.jsonl` | ~5 MB | raw session log, one JSON object per event |
| `session-019ffd64.html` | ~44 MB | rendered, browsable conversation |

Both are tracked through **Git LFS**, configured in [`.gitattributes`](.gitattributes) *before* the files were first staged. Only a pointer — object id and size — is versioned in git; the conversation text itself never enters git objects. Diffs, `git log -p` and `git grep` therefore stay clean and the repo stays clonable without pulling 47 MB of transcript.

Generated with:

```bash
# rendered HTML
omp --export ~/.omp/agent/sessions/<project>/<session>.jsonl

# raw JSONL is the session file itself
cp ~/.omp/agent/sessions/<project>/<session>.jsonl transcripts/
```

To clone without transcript payloads:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone <repo>
```

To fetch them later:

```bash
git lfs pull
```
