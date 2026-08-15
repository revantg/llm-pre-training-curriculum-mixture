# Adversarial audits

Two rounds of independent Opus reviewers, each grading against the verbatim
evaluation criteria (clauses C1-C17) and against the assignment itself.

## Round 1 — on the 52 KB predecessor (`../../iterations/SOLUTION.md`)

| reviewer | mandate | band |
|---|---|---|
| `AdvNumbers-2` | push on every number | 350-395 |
| `AdvEvidence-2` | citation abuse, scale and domain mismatch | 350-395 |
| `AdvWishful-2` | supply ledger, the wishful-accounting penalty | 355-395 |
| `AdvCriteria-2` | full C1-C17, padding penalty, data gate | 385-420 |

Headline: every supply inflation sat in a lane the author had not re-derived, and
the document's own "attack first" list named only audited numbers. 17 FATALs.
Two of these reviewers cross-examined each other mid-run and both withdrew a
finding under peer pressure.

## Round 2 — on `../../../submission/SUBMISSION.md`

Round-2 reports were returned in-session and are recorded in the transcripts
under `../../transcripts/`; their findings are what produced the current
deliverable. Mandates were:

| reviewer | mandate |
|---|---|
| `FreshEyes` | cold read, structure, and the C3 padding penalty |
| `RegressionHunt` | did the claimed fixes land, and what did the rewrite break |
| `VerifierAttack` | is `verify.py` real verification or circular |
| `AssignmentFit` | graded against `course/assignment.json`, not the criteria prose |

Findings that changed the deliverable:

- the declared protected floor **violated** widget 3's own `LANE_FLOOR = 0.08`
- the agentic epoch cap was an unjustified free parameter, and the criterion
  first offered to justify it was retrofitted (efficiency crosses 80% at ~8.9
  epochs, not 8)
- the provenance table omitted 18.4B of distilled traces
- the anneal row printed 99.999, not the claimed 100.000
- a difficulty-band specimen carried a fabricated citation
- assignment requirement R8 (cleaning toward a cumulative target, aimed at the
  starved slots) scored zero
- `verify.py` never opened the document it claimed to verify, so it could not
  detect the document reverting its own flagship correction
