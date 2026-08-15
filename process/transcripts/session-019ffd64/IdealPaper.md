{
  "paper": "IDEAL: Data Equilibrium Adaptation for Multi-Capability Language Model Alignment — arXiv 2505.12762v1 [cs.AI], 19 May 2025, v1 only",
  "slug": "ideal",
  "verdict_headline": "DROP — do not cite in the submission",
  "deliverables": {
    "local_ideal_md": "written, 23,012 bytes / 154 lines, byte-identical to brief.md",
    "brief_md": "research/papers/ideal/brief.md — same content",
    "assets": "papers/ideal/ holds paper.pdf (copied from ~/Downloads), paper.html, paper_clean.txt (MathML-stripped full text), paper_nomath.html, figs/ with all 5 extracted figures"
  },
  "path_correction": "The assignment's paths did not exist on this machine. local://rubric.md was initially missing (parent later confirmed it was a resume artefact and republished it; I read it and re-checked the verdict against E3 and the E11 tiers). /home/rev/... does not exist; the repo is at /Users/revant.gupta/timepass/curriculum-creation/. I also recovered the verbatim 3,300-char assignment text from assignment.json -> descriptionMarkdown.",
  "verdict": {
    "a_in_or_out_of_scope": "OUT OF SCOPE. Post-training (SFT) paper: LLaMA-3.1-8B, full fine-tuning, 23.8k-66k instruction samples, 1 or 3 epochs, batch 256, LR 2e-5 cosine, 8xA100, OpenCompass. No pretraining run, no token budget, no anneal, no LR decay leg, no curriculum ordering, no packing, no multilingual, no long-context, no agentic trajectories. Its five domains (math/code/reasoning/instruction/TrustAI) are not our seven lanes. SOLUTION.md line 3 already excludes SFT by name.",
    "b_weaknesses_touched": "One, weakly: #8 validation design — and only as a caution, not a number. Touches none of #1 agentic supply, #2 Indic tier C, #3 reasoning trace shape, #4 long-context/multi-doc, #5 anneal size, #6 difficulty ladder, #7 reasoning-length split, #9 seam width, #10 OPUS floor.",
    "c_confirm_challenge_refine": "None. Zero numbers moved. The 4-epoch ceiling used in SOLUTION.md §1.2/§3/§4/§5 is only RE-CITED by IDEAL from Muennighoff with no measurement of its own, so it is a citation of a citation, not confirmation. The 7.01%->2.17% attenuation is at most a WEAK challenge to §7 threshold design, and Spark Joy's n=1 0.60pp/0.86pp band already does that job in-domain. DoReMi/DOGE instability adds nothing over CLIMB Table 1 at pretraining scale.",
    "d_keep_or_drop": "DROP. Per E3 (padding earns nothing) and the PADDING severity label, a tenth paper defending no number is a net loss. It cannot lift E11 — that ceiling wants a 1B/3B pretraining proxy with a named confirm/refute metric, and IDEAL is an 8B SFT influence method whose own metric it shows to be basket-sensitive. Citing it hands a reviewer the cheapest hit on an E1-graded document: 'your own line 3 says SFT is out of scope.'"
  },
  "figures_all_inspected": {
    "method": "xd://inspect_image is NOT mounted in this session. Exact error, quoted in the brief after one retry: 'No such tool device: xd://inspect_image. Mounted: ast_edit, debug, browser, web_search, workflow, mcp__browsermcp_*, mcp__chrome_devtools_*, mcp__cloudflare_*, mcp__langfuse_*, mcp__pencil_*.' All five figures were instead decoded inline as images through read — native vision, not OCR.",
    "fig1": "data_distribution.png — schematic only, contains NO data. 3-D 'Data-proportion Space' loss surface, axis labelled loss from origin O, two unlabelled proportion axes, no tick values, no units, no error bars. Blue triangle 'Random Initial Situation' above purple star 'Optimized Situation' in a dashed ellipse marked Case1. Two boxed D1-D4 bar charts joined by an arrow labelled IDEAL. A cartoon, not evidence.",
    "fig2": "Four bar panels (m-sensitivity, D1(IDEAL), 1 epoch), y-axis 'Metric', x ticks 0/1/2/3 = bar index only, shared legend Joint SFT / IDEAL(m=0.3) / IDEAL(m=0.15) / IDEAL(m=0.1), values printed above bars, NO error bars in any panel despite 5 averaged runs, every y-axis truncated above zero. (a) Mathematics 63-70 step 1: 66.62 / 67.58 / 68.01 / 65.50. (b) Reasoning 71.0-75.0 step 0.5: 72.92 / 73.07 / 72.82 / 72.97. (c) Instruction ~35.5-41.5 step 1: 38.36 / 38.35 / 39.78 / 37.71. (d) Coding ~39-47 step 2: 41.26 / 42.68 / 44.51 / 41.68."
  },
  "verified_arithmetic": {
    "headline_7pct_is_relative": "Table 1 epoch=3 Joint 55.35 -> IDEAL D2 59.23 = +3.88 absolute = +7.01% relative. Epoch=1 is +3.08 = +5.62%.",
    "basket_attenuation": "4 benchmarks +7.01% rel / +3.88 abs -> 8 benchmarks +2.17% rel / +1.17 abs = 3.24x relative, 3.32x absolute attenuation. The paper concedes this itself.",
    "volume_matters_little": "Table 2: 2.8x more data (25k -> 66k samples) moved the average -0.09.",
    "fig2_reconstructs_table1": "Panel averages are exactly 54.79 (Joint) and 56.28 (m=0.15), matching Table 1's epoch=1 rows to the decimal.",
    "m_0_1_regresses": "m=0.1 averages 54.47 vs Joint 54.79 = -0.33 — an under-aggressive reweighting step is worse than not reweighting; the paper calls this only 'marginal gains'.",
    "recommended_setting_loses_a_domain": "On panel (b) Reasoning, the recommended m=0.15 (72.82) is the LOWEST of the four bars, below Joint 72.92.",
    "six_of_twelve_below_baseline": "6 of 12 non-IDEAL mixture-perturbation cells land below the un-tuned Joint blend (Random2 and DoReMi-D1 at both epochs, DOGE-D1 and DOGE-D2 at epoch=1); all 4 IDEAL cells are above.",
    "table4_reconstructed": "Applying gamma = 0.15/max|alpha| gives beta_D2 = [0.0087, 0.15, 0.0275, 0.0322, -0.0085]; D1 x (1+beta) predicts D2 as [4.94, 6.33, 5.04, 5.06, 4.66]k vs reported [4.9, 6.3, 5.0, 5.1, 4.7]k — max error 0.043k across all five domains.",
    "scale_gap": "[INFERENCE] paper reports sample counts only, never tokens; at a generous 1k tok/sample the §4.2 set is ~24M tokens, ~87,000x below our 2.080T."
  },
  "internal_inconsistencies_found": [
    "Table 4's column labelled 'beta (x1e-5)' cannot be the applied beta — Eq. 9 forces max|beta| = m = 0.15 and the observed Code move is +14.5%; the tabulated values are the pre-scaling gradient alpha. Mislabelled, and no code is released.",
    "Three different volume conventions: D1->D2 applies (1+beta) with no renormalisation; D0->D1 only reconstructs if renormalised to ~25k; §5.2 says the §4.2 total grew 23.8k -> 25.3k.",
    "The epoch/HumanEval claim is contradicted by its own Table 1: Specific/Coding HumanEval goes 37.20 (ep=1) -> 41.46 (ep=3), an increase, not the claimed decrease. Only the cross-method maximum falls."
  ],
  "two_traps_flagged": [
    "Do NOT cite the 0.00 HumanEval / 2.99 BBH single-domain collapses as §5 floor evidence — that is SFT catastrophic forgetting on 5.3k samples, not pretraining lane starvation. Spark Joy's sans-math arm (MMLU 29.71 vs 35.69, RC 26.48 vs 37.02, 100B final phase at 7B) is the right object at the right scale and is already cited.",
    "Do NOT cite IDEAL for the 4-epoch repetition ceiling — it is a bare re-citation of Muennighoff with no measurement attached."
  ],
  "follow_on_pointers": [
    {
      "ref": "Muennighoff et al., Scaling Data-Constrained Language Models, NeurIPS 36:50358-50376, 2023 (arXiv 2305.16264)",
      "why": "IDEAL's ref [43]. The PRIMARY behind the 4-epoch ceiling SOLUTION.md reuses in four places (§1.2 4.00 ep, §3 the defensible-band table and 2.508B = 0.125% of 2T, §4 3.89 ep, §5 627M at >=4 ep) and behind widget 1's <=4x classifier threshold. Cited by nothing in the nine.",
      "status": "ALREADY IN FLIGHT — a sibling holds papers/scaling-dc/ with 2305.16264v5. Flagged in the brief and messaged to Main so it is not double-dispatched."
    },
    {
      "ref": "Chung et al., UniMax (arXiv 2304.09151)",
      "why": "Low-resource MULTILINGUAL PRETRAINING mixture built on an explicit per-language EPOCH CAP. The missing precedent for the Indic tier table — §2 concedes 'no paper here studied Indic' while pricing tier C at 5.06x on 5.0B (weakness #2), A at 1.98x, B at 2.11x.",
      "status": "UNCOVERED — the one slot worth spending."
    },
    {
      "ref": "Chen et al., Take the Bull by the Horns (arXiv 2402.14270)",
      "why": "Continual-pretraining hard-sample reweighting — closest published object to the unsupported B0-B5 difficulty ladder (weakness #6). If its hardness signal is loss/perplexity-based it REINFORCES Preference Curriculum's objection rather than rescuing the ladder; either way §6a's claim changes.",
      "status": "Named from bibliography only, NOT read — logged as a lead, not evidence."
    }
  ],
  "gaps_confirmed_absent": "Nothing in IDEAL's bibliography concerns agentic/tool-use trajectory data at pretraining scale, multi-document long-context data, or measured anneal lengths — the three areas of greatest need. No code released for IDEAL itself.",
  "if_overruled": "One optional §7 clause is drafted in the brief in the spec's voice, with the scale caveat attached, citing only the 3.2x basket attenuation as a hazard to our own threshold design — never as a defence of any share. The brief's closing line states that if §7 does not need it, cite nothing from this paper.",
  "protected_files_untouched": "SOLUTION.md, README.md, EVIDENCE_MAP.md, every existing brief and everything under review/ are unmodified; git status shows papers/ideal/ as a new untracked directory only."
}