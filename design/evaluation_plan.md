# Evaluation Plan

## Golden Dataset
A hand-labeled set of at least 30 invoice/PO/contract triples covering: clean matches, amount mismatches,
vendor mismatches, missing-PO cases, and a small number of adversarial/malformed documents (to test
extraction robustness). Each labeled example records the correct extraction (every field) and the correct
match verdict.

## Accuracy Targets
- Field-level extraction accuracy ≥ 98% against the golden dataset (mirrors `scoping/success_metrics.md`).
- Match-verdict accuracy ≥ 95% against the golden dataset.
- Zero tolerance for false-approvals (a mismatch incorrectly verdicted as a match) during the pilot — this is
  the guardrail metric, not the quality metric, and is tracked separately.

## Drift Detection
The golden dataset is re-run against the live extraction agent on a fixed cadence (weekly during pilot,
monthly post-pilot). A drop of more than 2 points in field-level accuracy or any false-approval on the golden
set triggers an immediate review before the system continues processing new invoices.

## Regression Tests
Any change to the extraction prompt, the underlying model, or the reconciliation logic must pass the full
golden-dataset evaluation (at or above the accuracy targets above) before deploying — the same gate the
`eval/run_eval.py` pattern in `multi-agent-support-capstone` uses for its routing/task-success benchmark. The
code sample's `tests/` directory demonstrates the same principle at unit-test scale (deterministic mock
fixtures standing in for the golden dataset).
