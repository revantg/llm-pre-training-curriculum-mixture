# ERA V5 · Session 5 — Pretraining Mixture and Curriculum

> ### The submission is **[`session_5_era_v5/SUBMISSION.md`](session_5_era_v5/SUBMISSION.md)**
>
> Self-contained. Nothing else in this repo is graded.

A written specification deciding how a ~120B model's fixed token budget is split across capability lanes, in what order those tokens are served, what is held back for the final anneal, and which of those numbers survive contact with the actual token supply.

---

## Verify it

Every published number is re-derived from the raw dataset inventory rather than taken on trust:

```bash
python3 session_5_era_v5/verify.py
```

Zero dependencies. Checks are reported in two classes — **independent** (re-derived from the primary inventory) and **structural** (internal consistency only) — because a verifier that grades its own hardcoded constants proves nothing. The script prints its own limitations.

## Where each requirement is answered

| The assignment asks for | Section |
|---|---|
| A defended share for every capability slot | §0, §2 |
| Indic split across verified / unverified / translated / synthetic | §5 |
| Agentic, reasoning and long-context named, each pointed at inventory datasets | §3, §6 |
| Every lane sized against real supply; repeat-or-generate stated plainly | §3 |
| The protected always-on floor | §7 |
| The anneal reserve held back for cooldown | §8 |
| Difficulty and reasoning-length bands, with a real example at each level | §10, §11 |
| Cleaning and token documentation as a gate | §12 |
| Proxy runs at 1B / 3B with named confirm-or-refute metrics | §13 |
| Lane-to-benchmark causal ties | §4 |
| Known weaknesses, ranked | §14 |

## Layout

```
session_5_era_v5/
├── SUBMISSION.md          # >>> THE DELIVERABLE <<<
├── verify.py              # re-derives the published numbers; zero deps
├── widgets/               # the 9 course widgets — source of truth for preset constants
├── papers/
│   ├── EVIDENCE_MAP.md    # cross-paper synthesis against the assignment's asks
│   └── <slug>/brief.md    # 14 per-paper briefs, numbers with their measurement scale
├── review/criteria-audit/ # adversarial audit reports on an earlier draft
├── iterations/            # superseded drafts, audit trail only — see its README
├── lecture_notes.md       # course source
├── assignment.json        # assignment text and submission format
└── transcript_google.txt  # official session transcript

READING_GUIDE.md           # which papers to read, in what order, and which to skip
transcripts/               # the full working session that produced this (Git LFS)
```

## Also here

**[`READING_GUIDE.md`](READING_GUIDE.md)** — the 14 papers tiered by marks-per-hour, with a skip list and a requirement-to-paper map. Read this before the briefs.

**[`session_5_era_v5/papers/EVIDENCE_MAP.md`](session_5_era_v5/papers/EVIDENCE_MAP.md)** — what each paper does and does not support, cross-referenced against the assignment.

**[`session_5_era_v5/review/criteria-audit/`](session_5_era_v5/review/criteria-audit/)** — reports from independent adversarial reviewers commissioned to break an earlier draft. Kept because the corrections they forced are visible in the current one.

**[`transcripts/`](transcripts/)** — the complete working session, including every paper read and every revision, as Git LFS objects. See [`transcripts/README.md`](transcripts/README.md). Clone without the payload:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone <repo>
```
