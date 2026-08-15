{
  "reviewer": "AdvWishful-2",
  "clauses_owned": [
    "C7",
    "C8",
    "C9"
  ],
  "score_band": "355-395 / 500",
  "to_move_up_one_band": "Rebuild the §1 'Unique supply' column from widget 9's line items instead of widget 1's SUPPLY_T constant — which corrects STEM 250B→146B (0.92×→1.57×), nets the 60B repo-packed double count out of long-context (0.89×→1.53×), strips the 135M synthetic-origin sets from the agentic 'real' pool (73.4×→93.5×), and reclassifies the 4.6B distilled long-CoT as generated — then restate the Verdict column and the corpus-wide synthetic total accordingly.",
  "master_finding": "Every one of the 7 'Unique supply' values in SOLUTION.md:18-24 is lifted verbatim from the constant vector at widget_1_mixture_composer.html:302 (SUPPLY_T). The author de-rates exactly two (code by 32.9% file-level retention at :32, Indic by stripping synthetic at :34) and accepts the other five as given. C7 asks for sizing against the inventory (widget 9), which sums to 6401.6B vs SUPPLY_T's 6311.6B — and the divergence is concentrated in the one lane never checked (STEM). Consequence: the four loudly-conceded weaknesses are all in de-rated lanes; the four silent inflations are all in lanes where the constant was accepted. §9's 'Attack first' list (:345) nominates four audited numbers and zero of the four unaudited ones.",
  "independent_ledger": [
    {
      "lane": "web",
      "spec_supply_B": 4500,
      "spec_ratio": "0.15x",
      "my_supply_B": 4691,
      "my_ratio_wholeplan": "0.148x",
      "must_generate_B": 0,
      "disagreement": "spec conservative by 191B",
      "severity": "none"
    },
    {
      "lane": "code",
      "spec_supply_B": "1100 -> 362 eff",
      "spec_ratio": "1.32x",
      "my_supply_B": 362.9,
      "my_ratio_wholeplan": "1.52x",
      "must_generate_B": 0,
      "disagreement": "spec ratio is main-run-only; ignores 18.4B anneal and ~53.4B drawn by long-context from the same pool",
      "severity": "WEAK"
    },
    {
      "lane": "indic",
      "spec_supply_B": "275.9 -> 113.9 real",
      "spec_ratio": "2.77x",
      "my_supply_B": 113.9,
      "my_ratio_wholeplan": "2.93x",
      "must_generate_B": 84.3,
      "disagreement": "agrees in substance; mine is whole-plan incl. 17.5B anneal",
      "severity": "none"
    },
    {
      "lane": "stem",
      "spec_supply_B": 250,
      "spec_ratio": "0.92x covered",
      "my_supply_B": 146,
      "my_ratio_wholeplan": "1.62x (1.57x main, 3.92x post-selector)",
      "must_generate_B": 0,
      "disagreement": "104B phantom supply (+71%); verdict flips covered -> repeat",
      "severity": "FATAL"
    },
    {
      "lane": "reasoning",
      "spec_supply_B": 85.1,
      "spec_ratio": "2.00x",
      "my_supply_B": "85.1 (78.5 real / 6.6 distilled)",
      "my_ratio_wholeplan": "2.08x lane; 4.42x on traces; 9.09x on short-trace pool",
      "must_generate_B": "21.4 distilled booked as real",
      "disagreement": "internal epoch ledger self-contradictory three ways",
      "severity": "FATAL"
    },
    {
      "lane": "long_context",
      "spec_supply_B": 100,
      "spec_ratio": "0.89x",
      "my_supply_B": 59.7,
      "my_ratio_wholeplan": "1.53x",
      "must_generate_B": 0,
      "disagreement": "60B repo-packed code is derived from the code pool (widget9:318 src='packed from code corpora'); double-counted across two lanes",
      "severity": "FATAL"
    },
    {
      "lane": "agentic",
      "spec_supply_B": 0.627,
      "spec_ratio": "63.8x main / 73.4x whole-plan",
      "my_supply_B": "0.492 organic (0.360 trajectories)",
      "my_ratio_wholeplan": "93.5x (127.8x trajectory-only)",
      "must_generate_B": "42.6 = 92.7%",
      "disagreement": "21.5% of the stated 'real' pool is synthetic by widget 9's own descriptions",
      "severity": "FATAL"
    }
  ],
  "verified_credits": "All 7 shares, all 4 stage rows (each summing 100), the time-average to declared shares, the anneal 62.5/37.5 construction (21.156+22.969+21.875+9.156+9.063+7.500+5.500+2.781=100.000), the 30.0B reserve components, all four Indic tier factors (1.975/2.111/2.528/0.507), every pre- and post-selector ratio, the 16.39x asymptote (0.627*16.39=10.28B=25.7% of 40B), 91.5% generated, 73.4x, and the 17.64% vs 32.0% shift comparison all reproduce exactly. The arithmetic is not where this plan is weak.",
  "findings": [
    {
      "id": "F1",
      "severity": "FATAL",
      "locator": "SOLUTION.md:21, :52, :328 vs widget_9:362-381, widget_1:302",
      "claim": "STEM booked at 250.0B / 0.92x 'covered'. Widget 9's STEM datasets total 146B (peS2o 42 + proof-pile-2 55 + D4 STEM 49). Correct ratio 1.57x main / 1.62x whole-plan / 3.92x post-selector. Aggravated by :52 calling it 'the 0.92x lane with no headroom' while taking 0.55pp out of it, and :174 which sizes the anneal reserve against a 97B pool, proving the author knows the real numbers. Mitigation: stem:0.25 is a course constant, but its own comment claims it derives 'from Dataset Inventory' and it does not; the author de-rated code and Indic for exactly this class of gap."
    },
    {
      "id": "F2",
      "severity": "FATAL",
      "locator": "SOLUTION.md:23, :78 vs widget_9:318",
      "claim": "60B repo-packed code counted as independent long-context supply though widget 9 gives src='packed from code corpora' and SOLUTION.md:78 states 'the lane is assembled from the file-level-deduplicated pool'. Either the 60B sits inside the 362.9B code pool (code's true draw 532.4B = 1.47x) or it de-rates by 32.9% to 19.7B (long-context supply 59.7B = 1.49x main / 1.53x whole-plan). The spec takes the favourable branch on both lanes simultaneously."
    },
    {
      "id": "F3",
      "severity": "FATAL",
      "locator": "SOLUTION.md:58 vs :279 vs :129",
      "claim": "Reasoning epoch ledger contradicts itself: :58 books trace-shaped 7.1B -> 28.4B at 4.00x while :279 books ULTRA 5.68B against 4.6B long-CoT at 1.23x. If ULTRA consumes long-CoT, the other three bands' 22.72B falls on 2.5B (OpenMathReasoning 2 + NuminaMath 0.5) = 9.09x, 2.3x the plan's own declared safe ceiling, stated nowhere. Whole-plan traces run 4.42x and long-CoT 1.89x. Also NuminaMath is 'problems with answers' per widget_9:304-306, not traces, making the trace pool 6.6B and the main run 4.30x."
    },
    {
      "id": "F4",
      "severity": "FATAL",
      "locator": "SOLUTION.md:173 vs widget_9:296, :308",
      "claim": "Anneal reserve row labels 3.0B drawn from OpenThoughts2 + OpenR1-Math as Kind='real' in the one column whose purpose is separating real from generated. Widget 9 tags OpenR1-Math tier D 'R1-distilled' and OpenThoughts2 'distilled at scale'. The 4.6B long-CoT pool is 100% model-generated; 21.4B of distilled tokens are served whole-plan as real supply."
    },
    {
      "id": "F5",
      "severity": "FATAL",
      "locator": "SOLUTION.md:157 vs :314",
      "claim": "Two different corpus-wide synthetic totals: :157 computes 130.7B = 6.28% of 2.080T; :314 claims 'the 116.0B synthetic total [is] computed rather than asserted'. Neither cross-references the other. Both understate: adding F4's distilled mass gives >=152.1B = 7.31%."
    },
    {
      "id": "F6",
      "severity": "FATAL",
      "locator": "SOLUTION.md:131, :133 vs widget_9:258-259, :262-263, :266-267",
      "claim": "The agentic 'real' 0.627B pool includes 135M (21.5%) synthetic-origin data by the inventory's own words: Glaive 'Synthetic single- and multi-turn function-calling dialogues', xLAM 'APIGen-generated', ToolACE 'Self-evolving synthesis'. The spec calls all 267M 'short function-call format data' and never flags it. Organic pool 0.492B; honest gap 93.5x not 73.4x; generated fraction 92.7% not 91.5%. This is the exact named C9 move, inside the lane the plan holds up as its model of honesty."
    },
    {
      "id": "F7",
      "severity": "FATAL",
      "locator": "SOLUTION.md:131, :175, :177 vs :129 and :107",
      "claim": "Whole-plan the 360M trajectory pool runs at (4*0.360 + 1.400)/0.360 = 7.89 epochs, 1.97x the 4-epoch ceiling :129 declares measured-safe. :177 reports 3.89 epochs by scoping to the anneal leg alone. The plan performs precisely this whole-plan check for Indic and acts on it at :107 (tier C excluded from the anneal to protect the declared cap). Same structure, opposite treatment, no explanation."
    },
    {
      "id": "F8",
      "severity": "FATAL",
      "locator": "SOLUTION.md:59, :61 vs widget_9:312-315; grep of lecture_notes.md, all 9 widgets, BANDS_AND_PROXY.md",
      "claim": "The reasoning lane's largest component is named 'AON / D5 Academic-Reasoning-Overflow (V4 corpus)' and characterised as 'academic prose... not chain-of-thought'. Widget 9 has only 'AON (V4 corpus)', described as 'The reasoning-heavy slot as trained in the V4 run'. 'D5' and 'Academic-Reasoning-Overflow' appear in no course source; widget 9 has D1-D4 only. 141.6B served = 7.08% of the run rests on an invented identifier and an unsourced content type."
    },
    {
      "id": "F9",
      "severity": "FATAL",
      "locator": "SOLUTION.md:26 vs :283",
      "claim": ":26 sets reasoning at 8.50% because WEIGHTED_MIN=8 makes 6% 'an unfunded lane that cannot move AIME, GPQA, HLE or BBH'. :283 cites Two-Phase moving GSM8K 30.86->40.33 'with reasoning-shaped data at 1.3% of its second phase, so a small well-placed slice suffices'. Trace-shaped tokens served = 28.4B = 1.42% of the run. The plan's own citation says its trace component alone is sufficient; the 141.6B that lifts 1.42% to 8.50% is supported by no benchmark argument in the document."
    },
    {
      "id": "F10",
      "severity": "FATAL (argument)",
      "locator": "SOLUTION.md:144 vs :150, :153",
      "claim": "The 16.39xU asymptote is used to prove 0.627B can never exceed 10.28B effective, 74% of the lane 'provably not fillable'. It is never applied to the 42.1B generated fill, which is rolled out from the same 360M seed with tool observations masked, so its loss-bearing tokens are frozen-8B-teacher output conditioned on that seed. The law invoked to condemn the alternative is never tested against the substitute. Sharpest unanswered attack on §3."
    },
    {
      "id": "W1",
      "severity": "WEAK",
      "locator": "SOLUTION.md:101, :103 vs widget_1:287",
      "claim": "'The tension is in the assignment's own constraint, not in our choice' is 76% true. The verified indic>=12 floor forces 240B = 2.11x; the plan chose 15.80% = 2.77x. The extra 3.80pp / 76B is discretionary and defended by one word, 'the differentiator'. Web sits at 0.148x with unlimited headroom; returning the 3.80pp there is never considered."
    },
    {
      "id": "W2",
      "severity": "WEAK",
      "locator": "SOLUTION.md:20 vs :34, :99",
      "claim": "The §1 summary table bolds Indic 2.05x (tiers A+B+C demand vs real). The like-for-like lane figure (316B vs 113.9B real) is 2.77x and appears only in prose. A reviewer scans the table."
    },
    {
      "id": "W3",
      "severity": "WEAK->FATAL",
      "locator": "SOLUTION.md:93, :157 vs widget_9:337 and :111",
      "claim": "Tier D's 82.2B is classified rephrase-class (band <50%) rather than invented-textbook (ceiling <=3%) because widget 9 calls Sangraha synthetic a 'synthetic and translated expansion'. Translation is not rephrasing, and :111 concedes 'the unmeasured translated-corpus gap' in the same document. Reclassified, invented-class synthetic = 86.6B = 4.16%, breaching the <=3% ceiling and falsifying :157's 'compliant corpus-wide' claim. A load-bearing compliance verdict hangs on one adjective in a widget tooltip."
    },
    {
      "id": "W4",
      "severity": "WEAK->FATAL framing",
      "locator": "SOLUTION.md:146 vs :172-175, :243",
      "claim": "'2% is not ours to lower' is verified for the main run, but nothing forces the anneal's 7.50% agentic. Of that 6.0B, 3.6B is freshly generated agentic and 1.4B is trajectory repetition — both discretionary. Dropping the 3.6B cuts whole-plan generated agentic 42.1B->38.5B and the anneal share to 3.0%. The plan books the whole 46.0B / 73.4% / 91.5% under the floor excuse. The plan's own worst number was made worse by a free choice."
    },
    {
      "id": "W5",
      "severity": "WEAK",
      "locator": "lecture_notes.md:157, :221 vs SOLUTION.md:199-209",
      "claim": "The course extends protection to 'Indic, agentic and reasoning' and names 'long reasoning traces' as requiring protected floors. §5 excludes reasoning on a lane-level selector score of 0.818 while §1.2 concedes the lane is 92% not-the-capability. The genuinely scarce sub-pool (4.6B long-CoT, 100% distilled, 1.89x whole-plan) receives no floor."
    },
    {
      "id": "OVER1",
      "severity": "over-concession, credit-neutral",
      "locator": "SOLUTION.md:339, :78, :327 vs :67, :287",
      "claim": "The concession that 'nothing we hold is multi-document while MDQA is the metric' is analytically wrong in the plan's own disfavour: DD's decomposition yields single-document sequences (:287) and it is those buckets that move MDQA-10 0.8->20.8 and rescue MDQA-20/30 (:67). MDQA responds to sequence length, not multi-document composition, so the packing argument genuinely rescues the capability claim. The concession misdirects: long-context's real defect is F2's 60B double count, which §9 never mentions. Cleaning priority 4 is spent on a non-problem."
    }
  ],
  "synthetic_as_supply_tally": {
    "disclosed_and_repudiated": [
      "Indic 1.15x shown beside 2.05x (:20), repudiated verbatim at :34 as 'precisely the wishful accounting this plan is graded against'",
      "tier C's freed 4pp absorbed by tier D's 0.51x synthetic headroom (:111), placement conceded 'unsupported' at :113"
    ],
    "silent_and_flattering": [
      "agentic 0.627B 'real' includes 135M synthetic-origin (F6): 73.4x -> 93.5x",
      "4.6B distilled long-CoT booked real, 21.4B served (F4)",
      "60B derived repo-packed pool as independent supply (F2): 0.89x -> 1.53x and code 1.32x -> 1.47x",
      "STEM 250B vs 146B (F1): 0.92x -> 1.57x"
    ],
    "verdict": "Two disclosed and repudiated; four silent, all in the flattering direction. That ratio is the review."
  },
  "ruling_agentic_C9": "The confession EARNS marks on the share and LOSES marks on the ledger behind it. CREDIT: 2.00% is not the author's number to choose. widget_1_mixture_composer.html:284 hard-codes {key:'agentic', floor:2}; normalize() at :337 clamps any lower value and :355/:359 pin it when other sliders move — I read the function and 2% is genuinely unreachable from below. lecture_notes.md:157 and :221 independently require agentic above a protected floor, so zero is forbidden by a second, non-widget source. And the course's own supply readout at widget_1:442 states verbatim: 'agentic is the binding constraint, it must be synthesized; the scarce lanes need repetition and synthetic generation to fill even these small shares.' A plan that allocates the floor and fills it by declared generation is executing the course's instruction, not evading it. C9 penalises a plan that QUIETLY hands a LARGE share to an empty lane; agentic is the smallest lane in the plan (2.00%, 0.030% of trained tokens in unique terms) and the loudest number in the document — §3 is titled 'the one non-compliant number', quotes 91.5% generated and 73.4x, and derives a 25.7%-of-lane asymptotic fill ceiling that makes the impossibility worse than a reviewer would have found unaided. Neither trigger of C9 fires. 'Cut the lane' is not an available honest move: I checked both counterfactuals, and a reviewer demanding the cut is demanding a non-compliant plan. DEBIT, and it is real: the confession is not audited to the standard of the number it confesses. (i) The excuse covers 40.0B of 46.0B — nothing forces the anneal's 7.50% agentic, of which 3.6B is freshly generated and discretionary, yet the whole 46.0B / 73.4x is booked under 'not ours to lower'. (ii) The 0.627B 'real' pool is >=21.5% synthetic by widget 9's own descriptions; the honest gap is 93.5x. (iii) Whole-plan the trajectory pool runs at 7.89 epochs against a self-declared 4-epoch ceiling — the same whole-plan check the plan performs and acts on for Indic tier C at :107. (iv) The asymptote proves real data cannot fill the lane and is never applied to the seed-derived substitute. NET: score the agentic SHARE as compliant and well-defended; score the agentic LEDGER as three undeclared inflations. A confession is not a substitute for a fix — but here no fix existed. What did exist was an audit of the confession, and it was not performed.",
  "reasoning_vs_agentic_resolved": "Reasoning is the bigger marks problem, but it belongs under C7's sizing limb and C6, not under C9's 'almost no real data' limb. C9 has three triggers: quiet, large, almost-no-real-data. Agentic fires the third and only the third. Reasoning fires the second (170B, +50B, the plan's largest reallocation, funded by 0.55pp taken from the tightest lane) and fires the third only if 'real data' is scoped to the capability rather than the lane — the lane holds 85.1B of genuinely real supply at 2.08x, so on supply alone reasoning is a funded lane. Neither is quiet. The tiebreaker is fixability: agentic is loud and unfixable (floor verified hard in two independent course sources); reasoning is loud and fixable-and-unfixed (reverting to the course's 6.00%, or splitting into 'reasoning traces 1.5% + academic 7.0%', is refuted by no constraint anywhere in the repo and costs nothing). A reviewer penalises fixable-and-unfixed harder, and reasoning carries 4.25x the tokens. The decisive charge is not the conceded 7.1B/170B mismatch — a conceded mismatch is cheap. It is F9: the sizing rule at :26 is refuted by the plan's own citation at :283 (1.3% sufficed; the plan serves 1.42% trace-shaped). Stack F8 on it and the remaining 141.6B has an invented identifier and an unsourced content type. Agentic is a small, forced, over-declared number whose ledger needs an audit; reasoning is a large, free, self-refuted number whose justification collapses under one follow-up. Reasoning costs materially more.",
  "long_context_verdict": "Split verdict. The SUPPLY number fails (F2: 60B double count, 0.89x -> 1.53x, undisclosed). The CAPABILITY claim survives: the packing argument rescues it rather than evading it, because DD's own decomposition buckets are single-document (:287) and it is sequence length, not multi-document composition, that moves MDQA-10 from 0.8 to 20.8 and rescues MDQA-20/30 from 0.0-0.4 (:67). §9's concession at :339 is therefore an over-concession that its own §1.3 evidence refutes, and it misdirects attention from the actual 60B defect. Cleaning priority 4 (:327) is spent on a non-problem.",
  "lane_ranking_worst_first": [
    {
      "rank": 1,
      "lane": "STEM",
      "why": "104B phantom, verdict flips covered 0.92x -> repeat 1.57x, zero disclosure, and the plan raids this lane while mispricing it. One question destroys the row and cascades into H4'."
    },
    {
      "rank": 2,
      "lane": "Long-context",
      "why": "0.89x -> 1.53x; 60B double-counted across two lanes; the plan's own :78 supplies the proof; zero disclosure."
    },
    {
      "rank": 3,
      "lane": "Reasoning",
      "why": "Supply exists but the internal ledger contradicts itself three ways (F3), 91.7% of the pool is unsourced (F8), the distilled core is booked real (F4), the share is self-refuted (F9)."
    },
    {
      "rank": 4,
      "lane": "Agentic",
      "why": "Indefensible on supply and the plan says so more thoroughly than a reviewer would manage unaided. Ranked 4th not 1st because the share is course-forced and the disclosure is genuine; the ledger behind it (F6, F7, F10, W4) is what fails."
    },
    {
      "rank": 5,
      "lane": "Indic",
      "why": "Largest real-supply stretch by tokens (2.77x/2.93x against a verified 1.00-epoch published convention), but every component is disclosed, the tier split is exact, the floor is verified at widget_1:287, and the whole-plan cap is genuinely enforced. One deduction: 76B of the stretch is discretionary (W1)."
    },
    {
      "rank": 6,
      "lane": "Code",
      "why": "1.32x understates to 1.52x once the anneal and the long-context draw are charged, but the 32.9% file-level de-rating is the plan's best piece of independent supply work."
    },
    {
      "rank": 7,
      "lane": "Web",
      "why": "Clean at 0.148x, conservative by 191B. Nothing to attack."
    }
  ],
  "section_9_concession_adequacy": "The four loud concessions (agentic 73.4x, Indic tier C, reasoning's 7.1B trace pool, MDQA multi-document) are all in lanes where the author had already de-rated supply — they are receipts for completed work, not exposures. The four material inflations (STEM 104B, long-context 60B double count, agentic's 21.5%-synthetic 'real' pool, distilled long-CoT booked real) appear in no concession and in no 'Attack first' entry. The MDQA concession is additionally wrong in the plan's own disfavour. Judgment: the concessions are individually honest and collectively misdirecting — a reviewer who accepts :345 as the attack surface will audit only the numbers that already survive."
}