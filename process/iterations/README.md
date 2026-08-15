# Superseded iterations — audit trail only

**None of these files is the deliverable.** That is [`../SOLUTION.md`](../SOLUTION.md).

They are kept so the revision history is inspectable: what was claimed, what a reviewer broke, and what replaced it.

| File | Score | Why it was replaced |
|---|---|---|
| `PRETRAINING_SOLUTION_v2.md` | not reviewed | First full draft. Superseded before adversarial review. |
| `SOLUTION_v3.md` | **307 / 310 / 345** | Three independent red-team passes found 29 deduped FATALs. Also the version the README wrongly pointed at for a while, which capped the repo's effective score regardless of later work. |
| `SOLUTION_v4.md` | not scored | Closed the v3 FATALs. Retains the retracted `0.83x` figure. |
| `SOLUTION_v5.md` | **438 / 500** | Best-scoring iteration. Retains the retracted `0.83x` figure. |

## The corrections that only exist in the deliverable

| Change | v4 / v5 said | `SOLUTION.md` says |
|---|---|---|
| Compute-optimal ratio | `0.83x`, from the remembered ~20-tokens-per-parameter heuristic — **unsourced folklore** | `0.85x`, from Muennighoff's fitted `U_N = 0.051 * U_D` giving 2.353T |
| Agentic scarcity | stated as a 73.4x ratio | restated as an **impossibility**: the 0.627B pool yields at most 10.28B effective tokens ever, so >=78% of the lane must be generated at any epoch count |
| Corpus synthetic mass | stale | 130.7B = 6.28% of 2.080T |
| Multilingual probes | MMLU at 1B | MMLU moved to 3B+; XCOPA and TyDiQA-GoldP added at 1B |
| Indic tier C | defended as "inside the 6-epoch ceiling" | that defence **withdrawn**; cut to 4% after NVIDIA found N=1 > N=2 > N=4 |

Read these only to check that the revision history is honest. Grade `../SOLUTION.md`.
