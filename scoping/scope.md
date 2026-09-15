# Scope — Release 1 (Pilot)

## In Scope
- Three-way match (invoice vs. purchase order vs. contract) for **one invoice category** (standard goods
  purchase invoices) and **one vendor segment** (top 10 recurring suppliers by invoice volume).
- Automated field extraction from invoice documents into a structured record.
- Automated match/mismatch verdict against the PO and contract on file.
- Routing of any mismatch, missing-PO case, or above-threshold amount to a human exception queue.
- Full audit logging of every extraction, match decision, and human approval/denial.

## Out of Scope (Release 1)
- Full accounts-payable automation (this pilot covers reconciliation only, not payment scheduling/execution).
- Autonomous payment execution of any kind.
- Multi-currency and multi-language invoices.
- Non-PO-backed spend (e.g. expense reimbursements, one-off purchases without a PO).
- Invoice categories outside the pilot segment (e.g. services/time-and-materials invoices, which have
  fundamentally different matching logic).

## Rationale
Restricting to one invoice category and vendor segment lets the pilot prove the reconciliation pattern and
collect a golden evaluation dataset before generalizing — consistent with the constraint that the pilot must
not introduce new financial-control risk while the model's real-world accuracy is still being measured.
