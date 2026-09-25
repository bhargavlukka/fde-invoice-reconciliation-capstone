# Operations Runbook

## Logging
Every extraction call, reconciliation decision, and human approval/denial is written as a structured log entry
(JSON) including: timestamp, invoice identifier, action, actor (agent or human reviewer id), and — for
extraction — the prompt/model version used. This mirrors the `audit_log` + structured JSON logging pattern
from `multi-agent-support-capstone`.

## Key Alerts
| Alert | Trigger | Response |
|---|---|---|
| Extraction confidence/accuracy drop | Weekly golden-dataset re-run falls below target (see `design/evaluation_plan.md`) | Halt new-invoice processing; page on-call FDE; root-cause before resuming |
| Exception-queue backlog | Open exceptions exceed a defined count or average age threshold | Notify procurement/AP lead; consider temporary staffing reallocation |
| Approval SLA breach | A pending exception is unresolved past the target review window | Escalate to procurement/AP lead, then compliance officer if still unresolved |
| Gateway/API errors | SharedLLM gateway returns elevated error rates | Fail closed (route all in-flight invoices to the exception queue rather than guessing) |

## Incident Playbook
If match accuracy or extraction accuracy drops unexpectedly:
1. Halt auto-processing of new invoices (fail closed to the exception queue).
2. Re-run the golden dataset to confirm and scope the regression.
3. Check for a recent prompt/model version change; roll back if one occurred (see `deployment_ops/deployment_plan.md`).
4. If no recent change, treat as a data-drift incident — check whether the PO/contract database is stale or a
   new document format has appeared.
5. Notify compliance officer if any invoice was auto-approved during the affected window (should be zero per
   the guardrail metric, but the check is mandatory).
6. Resume auto-processing only after the golden-dataset gate passes again.

## Operational Ownership
Once the pilot is handed over, the customer owns day-to-day operations. The FDE team acts as secondary
on-call for 30 days, then moves to escalation-only support.

| Area | Owner (after handover) | Backup | Responsibilities |
|---|---|---|---|
| Service uptime and deploys | IT/Security (platform team) | FDE engineer (first 30 days) | Container health, secrets rotation, applying pinned image/prompt releases, executing rollbacks |
| Model/prompt quality | FDE engineer, moving to a named customer ML/automation owner by day 30 | FDE lead | Weekly golden-dataset re-run, approving prompt/model version changes, drift investigation |
| Exception queue and approval SLA | Procurement/AP Lead | Senior AP clerk | Queue backlog, reviewer assignment, first escalation on SLA breach |
| Audit log and controls | Compliance Officer | Internal audit | Periodic audit-log review, sign-off on any auto-approval threshold change, incident notification review (playbook step 5) |
| PO/contract data freshness | Procurement/AP Lead | IT/Security | Keeping the PO and contract databases current; responding to data-drift incidents (playbook step 4) |
| Business metrics and go/no-go | CFO | FDE lead | Monthly metrics review; decisions to expand scope or halt |

**Alert routing:** golden-dataset regression → model/prompt quality owner. Queue backlog and SLA breach →
Procurement/AP Lead. Gateway/API errors → IT/Security. Any possible false approval → Compliance Officer,
always and immediately.

**Handover criteria:** the FDE team steps back to escalation-only support once each owner above has handled
at least one real alert or scheduled review on their own, and the Compliance Officer has signed off on the
audit log.
