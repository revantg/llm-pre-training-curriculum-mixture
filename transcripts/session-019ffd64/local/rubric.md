# THE ASSIGNMENT — verbatim, full text

Source: `session_5_era_v5/assignment.json` → `descriptionMarkdown` (3300 chars, **zero** ellipsis characters — an earlier apparent truncation was a display artefact of two single lines of 1272 and 1877 chars).
Metadata: "Session 5 - Assignment QnA" · **maxPoints 500** · individual · one part "Github README.md Link" (`link`, 500 pts) · `rubricJson` **empty** — the prose below IS the rubric · allowResubmission true.

---

## Verbatim: the assignment paragraph

> From here the work is yours, and it is the most consequential design artifact the course has asked for so far. Each one of you will draft the mixture-and-curriculum plan for V5 as a written specification, and it has to be specific enough to defend. It states a share of the budget for every capability slot, and for the Indic slot it states the split across the verified, unverified, translated, and synthetic tiers rather than hiding behind a single headline number. It names the agentic and reasoning and long-context slots explicitly and points each one at the datasets from the inventory that will fill it. It fixes the protected always-on floor that the selector is not allowed to cross, it declares the anneal reserve that will be held back for the cooldown, and it lays out the difficulty and reasoning-length bands with a concrete example for each. And it commits to justifying these numbers through small proxy runs at the one-billion and three-billion scale before any of them is trusted at full scale, because the lesson that runs through this whole arc is that a data decision is a hypothesis until a cheap experiment has tested it. Alongside the plan the cleaning continues toward the cumulative target, now aimed at the slots the mixture shows to be starved.

## Verbatim: the Evaluation Strategy paragraph

> You will be evaluated on how well your plan would hold up if a reviewer sat across from you and pushed on every number, so the grade rests on the quality of your reasoning and the evidence behind your choices, and a tightly argued short plan will score well while padding earns nothing. A strong submission gives a defended share of the budget to every capability lane and states the Indic split across its verified, unverified, translated, and synthetic tiers, and it ties each lane back to the benchmarks it is meant to win so that a reviewer can see why each number is what it is. It sizes every lane against the real supply from the inventory and says plainly where a share can only be reached by repeating data or by generating it, and a plan that quietly hands a large share to a lane that has almost no real data behind it will lose marks for exactly the wishful accounting this session exists to prevent. It fixes the protected floor and declares the reserve it is holding back for the anneal, and it lays out the difficulty and reasoning-length bands with a real example at each level. The thing that separates a good plan from an excellent one is whether it is written as a testable hypothesis, so the highest marks go to the person who specifies a concrete proxy experiment at the one-billion or three-billion scale and name the metric that would confirm or refute their mixture, and the very highest go to the one that actually run that proxy and bring the numbers back. Your plan is reviewed the way a technique candidate is reviewed, in the open and against these criteria, and it is looked at only once your team has met the data-gating threshold, because a mixture is only as trustworthy as the cleaned and documented tokens standing behind it, and the plans that survive this review are the ones that will shape the mixture the whole cohort actually trains on.

## Verbatim: submission

> You're submitting link to your Github Repo README.md where we can see evaluate your work.

---

## Gradeable requirements — R0–R8

- **R0** written specification, "specific enough to defend"
- **R1** share of the budget for **every capability slot**
- **R2** Indic split across **verified / unverified / translated / synthetic**, "rather than hiding behind a single headline number"
- **R3** names **agentic + reasoning + long-context** explicitly and **points each at the datasets from the inventory**
- **R4** **fixes** the protected always-on floor the **selector is not allowed to cross**
- **R5** **declares the anneal reserve** held back for the cooldown
- **R6** **lays out the difficulty AND reasoning-length bands with a concrete example for each** — stated **twice** (assignment: "a concrete example for each"; evaluation: "a real example at each level"), therefore weighted twice. Two distinct band systems. Bare labels are not bands; a band needs a definition **and** an example.
- **R7** **commits to justifying these numbers through small proxy runs at 1B and 3B** before any is trusted at full scale
- **R8** "Alongside the plan **the cleaning continues toward the cumulative target, now aimed at the slots the mixture shows to be starved**"

## Gradeable evaluation criteria — E1–E11

- **E1** holds up when "a reviewer sat across from you and **pushed on every number**"
- **E2** grade rests on reasoning quality **and the evidence behind your choices**
- **E3** "a tightly argued short plan will score well while **padding earns nothing**"
- **E4** a **defended** share for every capability lane
- **E5** Indic tiers stated across all four
- **E6** each lane tied to the benchmarks it must win "so that a reviewer can see **why each number is what it is**"
- **E7** sizes every lane against the **real supply from the inventory**
- **E8** says **plainly** where a share can only be reached by **repeating or generating**
- **E9** "a plan that **quietly hands a large share to a lane that has almost no real data behind it will lose marks** for exactly the **wishful accounting** this session exists to prevent"
- **E10** difficulty and reasoning-length bands **with a real example at each level** (restates R6)
- **E11** **tiered ceiling**, explicit in the text:
  - good → a plan
  - **excellent → "written as a testable hypothesis"**
  - **highest → "specifies a concrete proxy experiment at the one-billion or three-billion scale AND name the metric that would confirm or refute their mixture"**
  - **very highest → "actually run that proxy and bring the numbers back"**

Context clause, not directly gradeable: the plan "is looked at only once your team has met the **data-gating threshold**."

---

## How to grade — work backwards from this text

1. **E1 is the whole grade.** For every number: is there a stated defence traceable to a paper, the widget inventory, the lecture, or explicit arithmetic? Correct-but-undefended still loses.
2. **E3 must be enforced hard.** Length is not merit. Name anything not serving R1–R8 / E4–E11 and say what to cut.
3. **E7/E8 are a matched pair, and E9 is their teeth.** Over-allocating a supply-poor lane is the named failure mode of the whole session.
4. **E6 requires magnitude justification**, not decorative benchmark labels.
5. **R3 requires named inventory datasets with token counts** — verify against `session_5_era_v5/widgets/widget_9_dataset_inventory.html`. "Long trajectories" is not a dataset.
6. **R6/E10 needs two band systems, each with an example.** Sources: `widgets/widget_7_curriculum_stages.html` (`DIFF[]`, B0 Nursery → B5 Research/PhD, plus "trace length is scheduled too") and `widgets/widget_6_reasoning_effort.html` (LOW 2 / MEDIUM 4 / HIGH 6 / **ULTRA 14** steps on one shared problem — integers in [1,1000] divisible by 3 or 5 → **467**).
7. **R4's verb is "fixes."** Resolve per-lane vs aggregate; ambiguity here is FATAL.
8. **R5's object is "held back."** Name what is withheld during the main run, not only what the anneal contains.
9. **Every deviation from the course preset needs the strongest defence.** Taste-only deviations are WEAK at minimum.
10. **R7 + E11 are the ceiling.** Named metric + numeric threshold + scale, and ideally executed numbers.

## Severity labels

- **FATAL** — wrong number, arithmetic that does not close, fabricated or reversed citation, internal contradiction, or an unaddressed R1–R8 requirement.
- **WEAK** — defensible but oversold; right finding at the wrong scale; deviation justified only by taste; decorative benchmark link.
- **MISSING** — a requirement or criterion with no prepared answer; an obvious reviewer attack not pre-empted.
- **PADDING** — correct but irrelevant to R1–R8 / E4–E11. Per E3 this costs marks. Name it and say what to cut.
