# Risk Assessment & Exit Criteria

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Model hallucinates or misreads an extracted amount, causing an incorrect match verdict | Medium | High | Golden-dataset accuracy gating before go-live; every match with financial impact requires human approval in Release 1 (no auto-approval yet); structured-output validation via typed schema rejects malformed extractions |
| Vendor/contract data drifts out of date (PO or contract database not kept current) | Medium | Medium | Reconciliation treats "no PO/contract found" as an explicit exception, not a silent pass; ops runbook includes a data-freshness check |
| Compliance/audit pushback on using an LLM for financial control decisions | Low-Medium | High | Compliance officer is a joint approver from Discovery onward; full audit logging designed in from Release 1, not retrofitted |
| Procurement/AP team distrust or low adoption | Medium | Medium | Shadow-mode rollout first (tool runs alongside, doesn't gate anything) before assisted mode; every flag includes a human-readable reason |
| Prompt injection via malicious/malformed invoice content | Low | Medium | Extraction prompt treats invoice content as inert data to extract from, not instructions to follow; output is schema-validated before use |

## Exit Criteria (Pilot Success)
The pilot is considered successful and eligible to move toward productization if, over the final 4 weeks:
- Guardrail metric holds at 0% false-approvals.
- Quality metrics meet or exceed their targets.
- Primary (time-reduction) metric meets or exceeds target.
- Compliance officer signs off that audit logging meets control requirements.

## Exit Criteria (Pilot Kill)
The pilot is halted and reworked (not scaled) if any false-approval occurs, or if extraction accuracy falls
more than 5 points below target for two consecutive weekly measurements.
