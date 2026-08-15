{
  "paper": {
    "arxiv": "2305.13169v2",
    "title": "A Pretrainer's Guide to Training Data: Measuring the Effects of Data Age, Domain Coverage, Quality, & Toxicity",
    "authors": "Longpre, Yauney, Reif, Lee, Roberts, Zoph, Zhou, Wei, Robinson, Mimno, Ippolito (MIT / Cornell / Google Research / OpenAI)",
    "venue": "NONE in arXiv metadata - Comments, Journal-ref and DOI all empty; source builds against iclr2023_conference.sty. Cite as preprint, not a conference paper.",
    "date": "13 Nov 2023, 51pp",
    "slug_corrected_from": "repeat",
    "slug_now": "pretrainers-guide"
  },
  "deliverables": {
    "brief_1": "session_5_era_v5/papers/pretrainers-guide/brief.md",
    "brief_2": "local://pretrainers-guide.md",
    "identical": "yes - diff -q clean, 317 lines / 40616 bytes each",
    "assets": "papers/pretrainers-guide/ - PDF, abs.html, native arXiv HTML, ar5iv.html, TeX tarball, src/, paper.txt, figs/ (18 PNG @200dpi)",
    "fetch_routes_that_worked": "ALL FOUR: /pdf/ 200, /abs/ 200, /html/ 200 (744KB LaTeXML), /e-print/ 200 (17 figure PDFs)"
  },
  "headline": "MISIDENTIFIED IN THE QUEUE. This is not a repetition paper - it has no epoch experiment, no repetition sweep, no multi-pass ablation, and dropout is 0.0. It is SILENT on all seven of our repetition figures and CANNOT replace the borrowed Two-Phase 6/8-epoch ceiling. The paper that does that is 2305.16264 (adjacent number, almost certainly the mix-up), now owned by ScalingDC. But the read was not wasted: the paper is 28 from-scratch pretraining runs at 1.5B - our exact proxy scale - and it is the strongest thing in our evidence base on weakness #8 (validation design), plus it delivers an unasked-for measured caution on our web quality filter.",
  "repetition_audit": {
    "method": "grepped the complete TeX source for epoch|repeat|repetition|duplicat|dedup|multiple times|unique token|data.constrain. Only substantive hits: main.tex:457 (C4+Pile approx-deduplicated per Lee et al. 2022, a preprocessing step) and main.tex:1015 (repeating their OWN experiments).",
    "verdict_all_seven": "SILENT x7",
    "agentic_4ep_0.627B": "SILENT - smallest pool studied is ~10^2x larger; no epoch variable",
    "reasoning_4ep_7.1B": "SILENT",
    "indic_C_5.06x": "SILENT - and English-only per section 8",
    "indic_B_2.11x": "SILENT",
    "indic_A_1.98x": "SILENT",
    "code_1.32x": "SILENT - Code & Math is a leave-one-out bucket, never a repetition arm",
    "opus_6x_effective": "SILENT - no selection-efficiency experiment",
    "latent_multipass_structure_found_but_rejected_as_evidence": "Token budget is FIXED across arms (batch 4096 x seqlen 512 x 88064 steps = 184.68B, Table 5 App C.1) while quality-filter arms shrink the pool to 90.6/83.9/73.3/45.6% (Table 15). So T=0.7 makes 2.193x as many passes as Full Dataset - assumption-free ratio - and still wins (+0.7 mean QA Fig 6, +1.8 toxicity ID Table 15). REJECTED for five reasons: (1) confounded with quality by construction, (2) pool ~71B = ~113x our agentic pool, (3) absolute range only ~1.2-2.6 epochs, below every ceiling we lean on, (4) '% Data' may be documents not tokens, (5) +0.7 is inside the ~+/-0.5pp resolution. Recorded in the brief so nobody re-derives it and over-claims.",
    "can_we_drop_the_borrowed_ceiling": "NO - explicitly no. No directly-measured epoch ceiling at any scale. Our scale-extrapolation weakness stands exactly where it stood.",
    "regularisation_subquestion": "Dropout 0.0 (Table 5) - the paper offers no dropout x repetition interaction at all."
  },
  "weakness_8_primary_value": {
    "seeds_variance_cis": "BLUNT NEGATIVE on the best case: one run per config, no seed replication. Section 8 is literally titled 'Compute Expense & Single Shot Experiments'. Zero error bars / CIs / seed counts on any QA result - verified from the pixels of Figs 6, 7, 8. Only dispersion anywhere is RepBias +/-0.6-0.8 (Tables 3/14/15). Only significance testing is on the TEMPORAL slopes (Pearson r, p<0.05, one-sided Wald). The arm-vs-arm deltas - the results analogous to our mixture comparisons - carry no uncertainty quantification. So it does NOT give us a measured 1.5B noise floor and we must not claim one.",
    "resolution_bound_INFERENCE": "Fig 8's mean-QA column is non-monotone in dose: removing 19.1% (Code) moves mean -0.1; removing 12.9% (Academic) +0.2; removing 6.9% (Books) -2.7. So the column cannot resolve below ~+/-0.5pp. This CORROBORATES our borrowed 0.60/0.86pp Spark Joy band at 1.5B n=1 instead of 7B n=1 - much closer to our probes. Corroboration, not replacement.",
    "single_metric_thresholds_are_fragile": "Arms with null means swing +/-3-7pp per eval family: No Wiki = Web -5.3, ContrastSets +7.2, mean -0.3. H3/H4/H4' are correctly shaped (multi-metric); H1 gates on MDQA-30 ALONE and H7 on a single ratio - those are the two most likely to return an unreadable answer at 1B.",
    "swe_bench_readability_answer": "Two independent findings, same direction. (a) Section 8: they evaluated ONLY after finetuning, 'motivated by finetuning being more applicable for 1.5B parameter models' - a team with 28 runs at 1.5B and Google compute declined prompt-based readout at that size. (b) Table 2: pretraining temporal degradation is 0.41 (r=0.61) at 1.5B but 0.08 (r=0.07, two tasks fail p<0.05) at 20M, while FINETUNING TD is readable at both (2.36 vs 2.84). Pretraining-mixture signal is exactly what collapses as the proxy shrinks. Recommendation: make BFCL AST-match H2's PRIMARY metric and SWE-bench Verified the confirmatory one at 7B, reversing the current order."
  },
  "weakness_10_and_4_floor": {
    "design": "9 domains from 22 Pile sources (Table 8), leave-one-out, 9 models, finetuned on NQ, evaluated on 27 MRQA/UnifiedQA datasets in 7 families.",
    "granularity_verdict": "Shape transfers, taxonomy does not. 9 buckets vs our 7 lanes is comparable granularity, and the smallest (Social 1.2%, Wikipedia 2.1%) bracket our agentic 2.0%. BUT these are provenance buckets inside one English corpus - no agentic, no long-context, no non-English bucket, and Code & Math is ONE bucket merging our code 23.95% and STEM 11.45%.",
    "strongest_datum_unrelated_eval": "Removing Common Crawl costs Academic QA -5.9, while removing the Academic domain itself IMPROVES Academic QA +2.2 - an 8.1pp reversal, and it is the paper's own headline sentence in section 6. Second best and closer to our lanes: removing Code & Math costs Common Sense -5.8 with a mean of only -0.1. Removing PubMed costs Common Sense -5.9. All nine arms lose on Web (-2.5 to -6.3); 8 of 9 lose on Common Sense.",
    "honest_limit_must_be_stated": "TWO of nine arms BEAT the full dataset on mean QA (No Social +0.4, No Academic +0.2) and a third ties (No Code -0.1). The paper hedges to 'all, or NEARLY all, the data' and names Code/Academic as the exceptions. So: SUPPORTED for large/heterogeneous lanes; NULL for small targeted lanes on mean performance; supported for small lanes only as per-eval capability insurance. Our agentic 2.0%'s closest analogues (1.2%, 2.1%) both came in indistinguishable from zero. This cuts slightly AGAINST us and must be cited in the per-eval form or it is an E1 liability.",
    "why_still_additive": "Our two existing floor arguments (CLIMB C20->0, Collapse real-token condition) are both about MECHANISM. This is measured downstream cost of ABSENCE. Different axis, genuinely additive."
  },
  "quality_filter_finding_unasked_for": {
    "concavity": "Mean QA peaks at T=0.975 = only 9% of C4 removed (+2.5), then +1.0 (84% kept), +1.2 (73%), +0.7 (46% kept). Removing 54% returns +0.7 vs +2.5 for removing 9%. Fig 6.",
    "per_lane_damage": "Books QA hurt at EVERY threshold, monotonically: -2.2 / -4.0 / -3.5 / -6.7 - despite Books scoring 1.9x the corpus quality mean (Fig 2). Lowest-quality-scoring domains benefit most (Biomed +6.1, Academic +6.4 at T=0.975).",
    "technical_text_deleted": "Section 3: 'technical domains such as PubMed, Code, and Academic score low on predicted quality, indicating that overly-specific positively-defined filters on web documents may remove substantial amounts of potentially useful specialized text.' App D.2 / Fig 11 confirms: as cutoff rises 0->0.2, Code and PubMed bands collapse while CC, OpenWeb, Wiki, Legal are retained. Read from pixels - no printed values, so do not quote magnitudes.",
    "why_it_matters_to_us": "Two of our seven lanes (code, STEM) ARE the low-predicted-quality technical categories this classifier deletes, and a third (Indic) is non-English. This upgrades our section 2 hazard 2 from assertion to measured cross-domain result AND extends it from Indic to code and STEM. Also challenges section 4's top-5% within-lane reserve quantile: no arm here cuts that hard, and the complementary Inverse T=0.5 arm shows discarding the TOP of the quality distribution costs -3.1 mean QA."
  },
  "verdict": {
    "in_scope": "IN SCOPE - a pretraining-data-composition paper whose independent variable IS the mixture. In scope for a different question than it was queued for.",
    "keep_or_drop": "KEEP, NARROWLY - for two claims and one caveat. Cite in section 7 (proxy design), sections 1/2 (quality-filter concavity + cross-domain filter damage), and ONE clause in section 5 (domain-absence cost, per-eval form). Do NOT cite for repetition, the anneal, or toxicity. Earned footprint is 3-4 sentences plus two table rows. Highest-value contribution is METHODOLOGICAL, which is what E11's top tier rewards, and it lands on the two hypotheses we ourselves flagged as weakest (H1's single metric, H2's unreadable metric).",
    "weaknesses_touched": "#8 YES primary; #10/#4 YES partial; #1 weakly and slightly against us; #2/#3/#5/#6/#7/#9 silent on all six; long-context NO (sequence length fixed at 512)",
    "drafted_insertions": "Three, in spec voice with scale caveats attached: section 7 noise-floor corroboration, section 7 H2 metric reordering, section 2 hazard-2 upgrade."
  },
  "key_implementation_nits": {
    "models": "28 x 1.5B (LM-XL, t5.1.1-XL-like) + 20M (LM-Small) decoder-only, T5X on TPUs",
    "budget": "batch 4096 x seqlen 512 x 88064 steps = 184.68B tokens, identical for both sizes",
    "tokens_per_param": "123 at 1.5B = 6.2x Chinchilla. Ours is 16.7 = 0.83x - OPPOSITE side of Chinchilla, which plausibly flatters their aggressive filter arms",
    "lr": "base 0.5, decay factor 0.5, 1000 warmup, 20000 steps/decay. NO cooldown or anneal leg at all",
    "dropout": "0.0",
    "seq_len": "512 - so nothing on long-context",
    "corpora": "C4 (2019 CC, badwords filter REMOVED) and the Pile (825GB, 22 sources), both approx-deduplicated",
    "code_released": "NONE - no repo, no checkpoints, no data links anywhere"
  },
  "figure_inspection": {
    "tool_status": "inspect_image is NOT MOUNTED. Attempted twice. Exact error both times: 'No such tool device: xd://inspect_image. Mounted: ast_edit, debug, browser, web_search, workflow, mcp__browsermcp_*, mcp__chrome_devtools_*, mcp__cloudflare_*, mcp__langfuse_*, mcp__pencil_*.' No vision device exists in that list.",
    "substitute": "Rasterised all 17 figure PDFs from the TeX source at 200dpi via pdftoppm and inspected each with read, which decodes images inline - genuine pixel inspection, not OCR. Every axis, tick, legend and colorbar in the brief was read from the rendered image.",
    "coverage": "18/18 inspected (17 used + figure-1.pdf, an unused 4-panel leftover in the tarball referenced by no includegraphics).",
    "dispersion_finding": "Of 17 figures, exactly ONE carries any dispersion information (Fig 4 boxplots, and that spread is across datasets, not seeds). Zero carry seed counts or CIs."
  },
  "followon_citations": {
    "highest_value": "2305.16264 Scaling Data-Constrained LMs - owned by ScalingDC, not duplicated",
    "best_route_to_a_measured_small_pool_repetition_number": "Biderman et al. 2023 Pythia - flagged in this paper's section 9 as having 'trained on the Pile, WITH AND WITHOUT DUPLICATION', 70M-12B, PUBLIC CHECKPOINTS. That is a direct duplication ablation we could re-analyse ourselves rather than borrow.",
    "indic_counter_witness": "Dodge et al. 2021 - C4 filtering removes text from communities 'like India or Nigeria' and they recommend AGAINST filtering. A named counter-witness to applying our web filter to the Indic lane.",
    "others": "Lee et al. 2022 (dedup, the method used here); Kreutzer et al. 2022 (multilingual corpora dominated by low-quality text, esp. low-resource); Chung et al. 2023 (multilingual balance, the citation section 8 defers to); Xie et al. 2023a DoReMi; Luu et al. 2021 (TD metric)",
    "still_unsourced_after_this_read": "agentic/tool-use data at pretraining scale, multi-document long-context supply, measured anneal lengths. This paper contributes nothing to any of the three."
  },
  "files_not_touched": "SOLUTION.md, README.md, EVIDENCE_MAP.md, all existing briefs, and everything under review/ are unmodified. git status shows my only addition is papers/pretrainers-guide/."
}