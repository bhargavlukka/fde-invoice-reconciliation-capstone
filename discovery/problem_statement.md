# Problem Statement & Constraints

## Problem Statement
Manual three-way invoice reconciliation (invoice vs. purchase order vs. contract) currently takes AP staff an
average of 15-20 minutes per invoice and produces a measurable rate of payment errors (duplicate payments,
overpayments from missed price discrepancies, and late payments from slow discrepancy resolution). This
capstone scopes a pilot to **reduce average manual review time per invoice by at least 60%** and **reduce
mismatch-driven payment errors by at least 40%** within a 2-quarter pilot, for a single invoice category and
vendor segment, without introducing new financial-control risk.

## Constraints / Non-Negotiables
- **Human sign-off required** before any action with direct financial consequence — no autonomous payment
  execution in this release.
- **Full audit trail** — every extraction, match decision, and human approval/denial is logged and
  reconstructable.
- **Data boundary** — invoice, PO, and contract data (which may include vendor banking details and pricing
  considered commercially sensitive) never leaves the approved processing boundary; no data is used to train
  third-party models.
- **No degradation of existing controls** — the pilot must be at least as auditable as today's manual,
  email-based process, not less.
- **Explainability** — every flagged discrepancy must include a human-readable reason, not just a status code.
