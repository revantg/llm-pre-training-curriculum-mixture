{
  "paper": {
    "arxiv": "2304.09151",
    "title": "UniMax: Fairer and more Effective Language Sampling for Large-Scale Multilingual Pretraining",
    "authors": "Hyung Won Chung*, Noah Constant*, Xavier Garcia*, Adam Roberts, Yi Tay, Sharan Narang, Orhan Firat (* equal contribution), Google Research",
    "venue": "ICLR 2023 — verified from e-print TeX: src/main.tex:4 loads iclr2023_conference.sty, line 63 has \\iclrfinalcopy uncommented (camera-ready)",
    "read_via": "ar5iv HTML (full body, Algorithm 1, Tables 1-8, Appendices A-F) + arXiv e-print TeX (849 lines, venue/Table-2 cells/grep-negatives) + all 17 figure PDFs rasterised at 150dpi and read as pixels, several measured programmatically against their own gridlines"
  },
  "deliverables": {
    "local://unimax.md": "written, 413 lines / 56850 bytes",
    "session_5_era_v5/papers/unimax/brief.md": "written, byte-identical",
    "assets": "papers/unimax/{unimax.pdf (19pp), src/ (TeX + 17 figure PDFs), src.tar.gz, figures/*.png (17)}"
  },
  "verdict": {
    "useful": "YES — the most useful paper in the set for §2 and the only one that touches Indic at all",
    "decision_it_changes": "Stop defending the tier table as four percentages; defend it as one declared per-tier epoch cap plus quality-ordered shares. Set tier C to 7.91% (not 8.00%) and declare N=5. 8.00% is 5.06 epochs so 'N=5' and 'C=8%' cannot both be stated; 7.91% makes the cap exact AND is what Algorithm 1 outputs at N=5 on our real pools.",
    "keep_or_drop": "KEEP"
  },
  "algorithm": {
    "mechanism": "Ascending sort by corpus size; per language b_l = B/(len(L)-i); if b_l > c_l*N then U_l = c_l*N (capped at N epochs) else U_l = b_l (uniform share); B -= U_l each step; p = normalize(U)",
    "capped_unit": "epochs over one language's CHARACTER corpus; N is a single global scalar, no per-language N",
    "residual_redistribution": "no second pass — the ascending sort plus the shrinking denominator len(L)-i does it. Freed budget flows monotonically UP the resource ranking and lands entirely on languages large enough to absorb it, which all converge to one identical uniform value (the plateau in Fig 1b). Head languages are never re-prioritised relative to each other.",
    "unit_conversion": "4 characters per token (following ByT5); a separate SentencePiece vocab is trained per sampling strategy",
    "edge_case_found": "If sum(min(b_l, c_l*N)) < C the loop ends with B>0 and normalize(U) silently rescales, VIOLATING the cap. UniMax never hits this (28.8T corpus vs 4.65T budget). OUR lane does: 275.9B pool vs 316B budget, so 'N=1' would actually deliver 1.145 epochs. Any port to a supply-poor lane must assert sumU == C."
  },
  "smallest_per_language_corpus": {
    "ablation_corpus_§4.1": "Yoruba ~0.105B characters ~= 26M tokens. Derived from §1 (English 9.7T chars, '92,000 times larger than Yoruba'); triple-corroborated because 0.24% (Table 8 tau=3.33 rate) x 4,653B-char 1x budget / 0.105B = 106 epochs, reproducing §1's 'repeated over 100 times' and the pixel-measured ~101 at rank 106 in Fig 1a",
    "refreshed_corpus_Table_8": "Yoruba 0.3B chars ~= 75M tokens (smallest true language); bg-Latn 0.1B chars ~= 25M tokens (smallest row, a Latin transliteration variant)",
    "reach_vs_our_tier_C": "tier C at 5.0B tokens is 67x larger than their Yoruba and 200x larger than their smallest row — applying N=5 there IS extrapolation, but in the SAFE direction (same epoch count over 67x more unique text = less repetition pressure). The unsafe extrapolation is model scale: their N-sweep is Large 1.2B only."
  },
  "key_numbers": {
    "models": "Large 1.2B / XL 3.7B / XXL 13B; encoder-decoder mT5 arch, 256,000-subword vocab with byte-level fallback; umT5 adds Small/Base, umT5-Large DROPPED for pretraining instability",
    "languages": "107 = 101 languages + 6 Latin-script variants",
    "budgets_derived": "1/8 = 145.4B tokens / 581.6B chars (250k steps x 1024 batch x 568 corpus tokens/seq); 1/2 = 581.6B tok / 2.327T chars; 1x = 1.163T tok / 4.653T chars. Independently corroborated twice from Table 8's rate columns (af 1.27%/7.4B -> C=582.7B; da 2.83%/132B -> C=4,664B) and by the uniform-plateau boundaries.",
    "N_values_tested": "N=1 everywhere in the main results. Only sweep = Table 2 right, N in {1,5,10} -> TyDi QA 82.2 / 81.5 / 81.8, Large 1.2B. N=2,3,4 never run. Table 2 right's budget is NOT stated and its N=1 value matches neither the 1/8 nor the 1/2 Large UniMax, so the three N values are internally comparable only.",
    "indic_slice": "14 Indic languages in Table 8 = 193.6B chars = 48.4B tokens (hi 75, bn 34, ta 17, mr 13, ne 11, ur 11, ml 9.4, kn 6.9, te 5.9, gu 3.6, si 3.0, pa 2.2, sd 0.9, hi-Latn 0.7 B chars). 7 of 14 capped at the 1/8 budget; ALL 14 capped at 1x.",
    "umT5_indic_precedent": "Summing Table 8's 1x column over the 14: Indic = 4.14% of 1.163T = 48.2B tokens = EXACTLY 1.00 epoch of the 48.4B pool — supply-limited, not chosen. Directly comparable to our lane-level 316B/276B = 1.14 epochs (not to our 15.80%).",
    "tydi_pixel_exact_Fig4a": "UniMax 82.19/83.97/84.39; tau=3.33 81.69/83.41/83.89; tau=1 80.10/82.04/83.29 (Large/XL/XXL). Delta over tau=3.33 = +0.50/+0.56/+0.50",
    "tydi_bottom4": "UniMax 86.49/87.83/88.50 vs tau=3.33 85.60/87.03/87.49 vs tau=1 82.09/84.19/85.49; bottom-4 verified = id/bn/te/sw",
    "wmt_chrF": "UniMax 41.80/~45.2/48.47 vs tau=3.33 41.19/~44.5/48.16 vs tau=1 37.41/~40.9/44.58; margin over tau=3.33 SHRINKS with scale (+0.61 -> +0.31), as does the per-pair win rate (88% -> 72%)",
    "published_defect_found": "Table 7's 'Avg' column disagrees with the mean of its own 9 per-language cells in 4 of 9 rows, as TWO EXACT TRANSPOSITIONS: Large tau=3.33 prints 82.0 (true 81.69) <-> XL tau=1 prints 81.7 (true 82.04); Large UniMax prints 83.3 (true 82.23) <-> XXL tau=1 prints 82.2 (true 83.32). Figure 4a carries the correct means in all 9 cells. Do not quote Table 7's Avg column."
  },
  "five_questions": {
    "a_degradation_from_over_repetition": "YES, but the channel and threshold are not what H3 assumes. Held-out CE loss (sensitive): Fig 2b, tau=3.33, 1/8 budget, Yoruba at ~4.7 epochs — yo Large 1.768 monotone, yo XL 1.632 monotone, yo XXL min 1.579 at 188K -> 1.650 at 250K = +0.071 nats, AND yo XXL ends WORSE than yo XL (scale inversion). Fig 3e, 1/2 budget, Large only, Yoruba at ~18.6 epochs: min 1.709 at ~571K -> 1.779 at 1M = +0.070, 18 sawtooth teeth from 400K (paper says '300,000 steps' but from pixels the curve is still descending at 300K/500K — 300K is where the sawtooth appears, not where loss turns). Downstream metric (insensitive): N=1/5/10 -> 82.2/81.5/81.8, 0.7pt spread, NON-MONOTONE. So the threshold is not an epoch count — it is epochs x model scale x steps. ~4.7 epochs suffices at 13B but not at 1.2B or 3.7B.",
    "b_cap_vs_temperature": "Yes consistently, but SMALL over a tuned temperature and the cap is NOT where the gain comes from. Over tau=3.33: TyDi +0.50/+0.56/+0.50, TyDi bottom-4 +0.89/+0.80/+1.01, WMT chrF +0.61/+0.68/+0.31, XNLI translate-train +0.4/0.0/0.0 (exact TIES at XL and XXL), XQuAD EM +0.6/+0.3/+0.2. Over tau=1: +1.10 to +4.40. DECISIVE ATTRIBUTION from Fig 5 (both halves, pixel-measured): the two languages where the cap actually binds — te 0.56% vs tau's 0.52%, sw 0.50% vs 0.50% — gain -0.3 and +0.4, while bn (uncapped, on the uniform plateau, 1.78% vs 0.87% = 2.05x exposure) gains +2.9, the largest in the suite. The cap prevents the tau blow-up; the UNIFORM leg produces the wins. Generalised (after EmnlpPaper's refinement): a sub-corpus is capped iff c_l < b/N where b is the uniform residual share; four regimes tabulated. Our tier C is in the CAPPED leg — the leg where no advantage was measured.",
    "c_native_vs_translated_vs_synthetic": "NO — clean negative, and better than silence because the authors name it as out of scope. 'synthetic' appears ZERO times in the source; 'parallel data' appears exactly once, in the Conclusion, as declared future work ('Future work is needed to test if UniMax confers gains in other settings, such as ... (ii) models trained with parallel data'). All training data is one kind: CC web text, CLD3-detected, langid >= 0.95; n_l is a raw character count with no provenance tiering. The only native-vs-translated distinction is in EVAL design (§4.3): TyDi QA chosen because questions are 'written from scratch by native speakers ... the absence of translationese', and they explicitly avoid benchmarks translated post-hoc from English — a strong stated prior that translated text is a distinct, inferior distribution, asserted not measured, and about eval not training. Consequence: our A/B/C/D quality ordering gets NO support here, and UniMax's uniformity principle actively argues against it.",
    "d_when_in_training": "NO — hard negative. grep for curricul|anneal|stag|schedul|mid-train|two-phase|cooldown|'later in training'|'order of' over the full source returns ZERO matches. p_l is computed once, before training, from static character counts, never revisited. Nothing supports or refutes Indic 21.875% in the anneal; MAP-Neo remains the only quantitative precedent and still points the other way. Two adjacent facts concern duration not ordering: (1) the penalty accrues with optimiser steps (Fig 3e turns only in the longer run); (2) §5.3 'the optimal setting of N likely depends on the character budget, as for large enough budgets UniMax-1 will see vanishingly little of the lowest-resource languages' — evidenced by Fig 3f where N=1 leaves yo at 1.92 vs tau=3.33's 1.71. ACTIONABLE CONSEQUENCE: N must be recomputed PER LEG. If the anneal's Indic preserves A40/B30/C8/D22 then anneal tier C = 1.40B, whole-plan tier C = 26.68B = 5.34 epochs and a declared N=5 is broken by our own cooldown; if the anneal Indic is only tier-A's top-15% quantile plus D ballast (as §5's reserve table implies) tier C stays 25.28B. §2 or §5 must say which.",
    "e_tokenizer_fertility": "PARTLY. Vocabulary composition by script and token-length distribution YES (Table 4, App A); per-language FERTILITY (tokens per word/char on text) NO. Devanagari vocabulary share: tau=1 0.5% -> tau=3.33 2.2% -> UM1@4x 1.9% -> UM10@4x 3.0% -> UM1@1x 2.9% -> UM10@1x 2.6%, mT5 1.3%. Devanagari is the paper's own worked example of a tail script. Raising N from 1 to 10 at 4x takes it 1.9% -> 3.0% (+58% relative); UniMax-1@1x gives 2.2x mT5's Devanagari share. Three named levers shift capacity to tail scripts: higher tau, smaller budget, higher N — all also shorten tokens. UniMax vocabs are LONGER than mT5's overall (10+ char 7.5% vs 2.7%), attributed to mT5's whitespace pre-tokeniser. Transferable engineering fact for our §2 hazard 1: 256,000-subword vocab with BYTE-LEVEL FALLBACK (App C) — the standard mitigation for uncovered-unigram loss spikes. Still no frozen-embedding condition anywhere."
  },
  "replacement_question": {
    "answer": "KEEP the four percentages; adopt the cap as the constraint that DERIVES and defends them; explicitly REFUSE Algorithm 1's uniform leg.",
    "algorithm1_on_our_pools": "pools A 64.0 / B 44.9 / C 5.0 / D 162.0 B tokens (total 275.9B), lane budget 316.0B: N=1 -> A 23.20 / B 16.27 / C 1.81 / D 58.72 % but only 275.9B allocated, 40.1B SHORT; N=2 -> 34.21/28.42/3.16/34.21; N=3 -> 31.75/31.75/4.75/31.75; N=4 -> 31.22/31.22/6.33/31.22; N=5 -> 30.70/30.70/7.91/30.70; N=6 -> 30.17/30.17/9.49/30.17; N=10 -> 28.06/28.06/15.82/28.06",
    "finding_1": "N=5 outputs tier C = 7.91% against our hand-chosen 8.00% — a 0.09pp difference. Our weakest number is the output of a published algorithm at a cap value that same paper tested.",
    "finding_2": "But the cap gets A/B/D wrong and we should refuse it: at N=5 Algorithm 1 sets A=B=D=30.70%, taking 9.30pp OUT of verified native and giving +8.70pp to synthetic. Its uniformity is justified by equity across LANGUAGES (linguistic utility, Blasi et al.; demographic utility in App B) — no analogue across quality tiers of one lane. Import the cap, refuse the uniform leg, write down why.",
    "finding_3_inversion": "max tier-C share = N x 5.0B / 316B: N=1 -> 1.58%, N=2 -> 3.16%, N=3 -> 4.75%, N=4 -> 6.33%, N=5 -> 7.91%, N=6 -> 9.49%, N=10 -> 15.82%. Our 8.00% implies N=5.06 (so '8% with cap N=5' is internally inconsistent — use 7.91%). The composer's default C=20% requires N=12.64, which is 2.1x Two-Phase's 6-epoch HQ ceiling and 26% beyond the largest N UniMax ever ran.",
    "finding_4": "The N=1 row exposes the normalisation trap above: our pool (275.9B) < our budget (316B), so Algorithm 1 leaves 40.1B unallocated and normalize() silently delivers 1.145 epochs, not 1.000."
  },
  "figures_inspected": "all 17, rasterised at 150dpi and read as pixels; Figs 1a, 1b, 2b, 3e, 4a/4b/4c, 5-right and 6-left additionally measured programmatically against their own gridlines. NO figure in the paper has error bars; every configuration is a single run with no seeds or variance reported.",
  "solution_md_impact": {
    "§2_tier_C_8pct_5.06x": "REFINE -> 7.91% / 5.00x with declared cap N=5; also CONFIRMS survivable (their N=5 costs 0.7pt at 1.2B)",
    "§2_composer_default_20pct": "CONFIRM and STRENGTHEN — 12.64 epochs on a published cap axis",
    "§2_A40_B30_D22": "CHALLENGES the shape and we should refuse in writing (uniform leg would move 9.30pp native -> synthetic)",
    "§2_no_paper_studied_Indic": "NOW FALSE — 14 Indic languages with char counts; bn and te are 2 of the 4 languages in Fig 4c's lower-resource panel",
    "§2_hazard_1_tokenizer": "REFINE with real script evidence (Devanagari 0.5 -> 3.0%) + name byte-level fallback",
    "§1_Indic_15.80pct_1.14x": "SUPPORTS — 1.14 lane epochs is below umT5's own head-language epoch counts; umT5 ran the whole corpus at N=1",
    "§7_H3": "CHALLENGES THE DESIGN — their N-sweep found the effect absent at exactly H3's 1B scale, and harm grows with scale. Add held-out CE loss on the tier-C slice and pre-commit escalation to 3B. Independently corroborated: an 8B/300B external application loses 1.70 MMLU N=1 -> 4.",
    "§7_H5": "SILENT, no help",
    "§5_Indic_floor": "NEUTRAL — no floor of any kind in this paper",
    "§9_limitations": "amend 'no paper studied Indic' to 'no paper studies Indic TIERING'"
  },
  "draft_insert_for_§2": "Provided in brief §6, in the spec's voice, with the scale caveat attached; requires changing tier C 8% -> 7.91% (demand 25.0B, repeat 5.00x) and +0.09pp elsewhere. Two smaller forced edits also drafted (§2 hazard 1 Devanagari/byte-fallback; §9 'no paper studied Indic').",
  "follow_on_citations": [
    "Hernandez et al. 2022 2205.10487 Scaling Laws and Interpretability of Learning from Repeated Data — UniMax's own source for '0.1% repeated 100x ~= halving model size'; the highest-value next read for pricing tier C at OUR scale (coordinate with ScalingDC 2305.16264)",
    "Kreutzer et al. 2022 TACL Quality at a Glance — the audit behind UniMax's Marathi statistic (only 40% of mC4's Marathi bucket is well-formed Marathi); direct evidence base for tier B and §2 hazard 2, audits Indic buckets specifically",
    "Blasi et al. 2022 ACL Systematic Inequalities — the linguistic-vs-demographic utility distinction the uniform leg rests on; needed to reject that leg cleanly",
    "Chung et al. 2020 EMNLP Language-Clustered Vocabularies — the vocab-vs-training distribution mismatch of §3.1; bears on §2 hazard 1",
    "Caswell et al. 2020 COLING Language ID in the Wild — why the 0.95 CLD3 threshold exists; bears on separating tier B from tier C and on hi-Latn transliteration",
    "Wang et al. 2020b differentiable data selection + Jean et al. 2019 bi-level validation-utility scheduling — multilingual precedents if OPUS reweights online; carry over UniMax's objection that they have no repetition limit",
    "Pfeiffer et al. 2022 Lifting the Curse of Multilinguality — named in UniMax's future work; relevant only for Indic-specific capacity vs share"
  ],
  "coordination": "Claimed scope with EmnlpPaper up front and folded in their refinement: 'which leg binds' is a budget/pool property, not a property of the method. Replaced my regime-specific 'bn is uncapped' with the general condition derived from Algorithm 1 — a sub-corpus is capped iff c_l < b/N, where b is the uniform residual share (at N=1 the threshold is b itself). Their HI 0.867% and BN 0.30% of 300B recover 2.60B and 0.90B, matching their Table 12 pools exactly, independently confirming the rule. Four regimes now tabulated. Their N-sweep is cited as DIRECTION only, with their confound named (§5.2.1 repetition vs App E uniformity, one result), flagged as English MMLU, and noting their multilingual arm was N=1 only. No effect size claimed from their paper; alpha=1.3, their Table 12 analysis and DoReMi -2.31 left entirely to them.",
  "what_not_to_overclaim": [
    "Do not say UniMax validates 5 epochs at our scale — the N sweep is Large 1.2B only and the paper's own finding is that harm is invisible at 1.2B and conspicuous at 13B",
    "Do not say it validates repeating a 5B-token pool — nothing in the study is above ~0.3B chars for a tail language",
    "Do not attribute the low-resource gains to the cap — Fig 5 shows they belong to the uniform leg; where the cap binds the gains are -0.3 and +0.4",
    "Do not call the cap a large win over temperature — over a tuned tau=3.33 it is +0.5 TyDi and exactly 0.0 on XNLI translate-train at XL and XXL",
    "Do not port the uniform leg to our quality tiers",
    "Do not quote Table 7's Avg column — 4 of 9 cells are wrong as two exact transpositions; use Figure 4",
    "Do not treat this as a decoder-only or curriculum result — encoder-decoder, span corruption, static distribution",
    "Do not mix the two corpora — Figs 1-6 and Tables 5/7 use the §4.1 filtered mC4 (Yoruba ~0.1B chars, 1/8 plateau 1.77%); Tables 3/8 use refreshed 3.1.0 (Yoruba 0.3B chars, 1/8 plateau 1.48%)"
  ]
}