# Security Plan

## IAM
- Service credentials (the SharedLLM gateway API key) are scoped to this application only, stored as an
  environment variable, never checked into source control (`.env` is gitignored; `.env.example` documents the
  variable names only).
- Role separation: the system that executes extraction/reconciliation runs under a service identity with
  read-only access to PO/contract data; only the human-approval step (a distinct, audited action) can move an
  invoice toward payment.
- Reviewers (procurement/AP staff) and approvers (anyone authorized to resolve an exception) are logically
  distinct roles in the audit log, even if the same person holds both in the pilot.

## Data Handling
- Invoice, PO, and contract data are processed only for the duration of the extraction/reconciliation request;
  no invoice content is persisted by the LLM provider (per the SharedLLM gateway's no-training-on-input terms).
- Data retention for audit purposes follows the org's existing financial-records retention policy — the audit
  log stores decisions and metadata, not full raw documents, beyond what's needed to reconstruct a decision.
- PII/financial data (vendor banking details, pricing) is never logged in plaintext outside the audit log's
  access-controlled store.

## Encryption
- All data in transit (to the SharedLLM gateway, to internal services) uses TLS.
- Data at rest (audit log, PO/contract databases) is encrypted using the deployment environment's standard
  disk/volume encryption.

## Approval Workflows
- Mirrors the human-approval-gate pattern from `multi-agent-support-capstone`: any invoice reconciliation
  result that is not a clean, below-threshold match is written to a pending-exceptions store and requires an
  explicit approve/deny action from an authorized human before it can proceed downstream.
- An approval is bound to the exact extraction/match payload it was granted for — a payload change (e.g. a
  corrected amount) requires a fresh approval, never reuses a prior grant.
