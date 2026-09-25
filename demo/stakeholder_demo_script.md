# Final Stakeholder Demo Script

## Purpose
A 25-minute go/no-go demo for the Release 1 pilot. It shows the three-way reconciliation working on real
scenarios, shows each stakeholder the evidence they care about, and ends with a decision on moving from
assisted mode to limited auto-approval (see `adoption/adoption_strategy.md`).

**Audience:** CFO (sponsor), Compliance Officer (control owner), Procurement/AP Lead (primary user),
IT/Security (gatekeeper). The CFO and Compliance Officer are joint approvers; neither can approve alone.

**Presenter:** FDE lead. **Driver at keyboard:** FDE engineer. **Guest speaker:** one AP clerk from the pilot.

## Pre-Demo Checklist
- [ ] Run all three scenarios in mock mode the morning of the demo and confirm the output matches this script.
- [ ] Keep a terminal already open in `design/code_sample/`. Increase the font size.
- [ ] Have the pilot metrics dashboard ready: final 4 weeks, all metrics from `scoping/success_metrics.md`.
- [ ] Have an audit-log excerpt for one invoice (extraction → match → human decision) ready to show.
- [ ] Fallback: if the terminal fails, use the saved output screenshots. **Do not** switch to `--live` during
      the demo. The mock mode output is deterministic, and the live model is not.

## Agenda (25 min)

| Time | Segment | Primary audience |
|---|---|---|
| 0:00-0:03 | 1. The problem, in their words | All |
| 0:03-0:12 | 2. Live walkthrough: three invoices | AP Lead, Compliance |
| 0:12-0:16 | 3. Control and audit trail | Compliance, IT/Security |
| 0:16-0:21 | 4. Pilot results vs. targets | CFO |
| 0:21-0:23 | 5. Who runs it after we leave | All |
| 0:23-0:25 | 6. The decision | CFO + Compliance |

---

## 1. The Problem, in Their Words (3 min)
> "Six months ago, each invoice took your team 15-20 minutes. A clerk opened the PO, found the contract, and
> compared line items by eye. Mismatches that slipped through turned into overpayments and duplicate
> payments. We agreed on two targets: cut review time by at least 60% and cut mismatch-driven payment errors
> by at least 40%, without weakening a single control. Today we'll show you whether we hit them."

Keep this short. Everyone in the room already knows the problem. The goal is to restate the success
criteria they agreed to, so the results in segment 4 are judged against their targets and not new ones.

## 2. Live Walkthrough: Three Invoices (9 min)
Frame it like this: *"These are the three situations your clerks deal with every day: an invoice that's
clean, one that's wrong, and one we can't match to anything."*

### Invoice 1: clean match
```bash
python run_sample.py invoice_match
```
**Show:** Acme Supplies, INV-9001, which references PO-1001. The extracted total is 1,200.00, the PO total
is 1,200.00, `status: match`, and `discrepancies: []`.

**Say:** *"The agent read the invoice, pulled PO-1001, confirmed that Acme has an active contract, and found
nothing wrong. In assisted mode, the clerk sees this as a suggested approval and makes the decision with
one click instead of spending 15 minutes on lookups."*

### Invoice 2: amount mismatch (the one that matters)
```bash
python run_sample.py invoice_amount_mismatch
```
**Show:** INV-9002 bills Widget B at a quantity of **75**, but the PO covers **50**. The invoice total is
1,300.00 against a PO total of 1,200.00, and `status: mismatch`. The discrepancy reads: *"Invoice total
1300.00 does not match PO total 1200.00."*

**Say:** *"This is the overpayment that used to get through. The agent doesn't just flag it. It says why,
in plain language. It also doesn't reject the invoice or contact the vendor. It routes the invoice to your
exception queue, and a person decides."*

**Hand to the AP clerk (1 min):** they explain how they would have handled this before the pilot and how
they handle it now. A peer's account builds more trust with the AP Lead than anything we can say.

### Invoice 3: missing PO
```bash
python run_sample.py invoice_missing_po
```
**Show:** Globex Materials, INV-9003, which references PO-9999. `status: missing_po`, `po_total: null`, and
the discrepancy reads: *"No purchase order found matching reference PO-9999."*

**Say:** *"When the agent can't find what it needs, it doesn't guess. A missing PO is an explicit
exception, never a silent pass. That same rule is why a stale PO database shows up as more exceptions
rather than as bad approvals."*

## 3. Control and Audit Trail (4 min)
Speak to the Compliance Officer and IT/Security directly.

- **Show the audit-log excerpt** for INV-9002. It records the extraction with its prompt and model version,
  the mismatch verdict, and the clerk's decision with reviewer ID and timestamp. *"Every decision can be
  reconstructed, including which model version made it."*
- **Human sign-off:** no payment-affecting action happens without a person. Release 1 does not execute
  payments at all.
- **Fail closed:** if the SharedLLM gateway errors, all in-flight invoices go to the exception queue
  (`deployment_ops/operations_runbook.md`).
- **Data boundary:** invoice data stays within the approved boundary and is not used to train third-party
  models (`design/security_plan.md`).
- **Prompt injection:** invoice text is treated as data to extract, not as instructions to follow, and all
  output is schema-validated before it's used.

## 4. Pilot Results vs. Targets (5 min)
Show the dashboard. Present every metric, including any that fell short. Hiding a miss in this room costs
more trust than the miss itself.

| Metric | Target | Result (final 4 weeks) |
|---|---|---|
| Review time reduction | ≥ 60% | *[from dashboard]* |
| Payment error reduction | ≥ 40% | *[from dashboard]* |
| False-approval rate (guardrail) | 0% | *[from dashboard]* |
| Field extraction accuracy | ≥ 98% | *[from dashboard]* |
| Verdict accuracy | ≥ 95% | *[from dashboard]* |
| Eligible invoices routed through tool | ≥ 80% | *[from dashboard]* |
| Errors avoided vs. operating cost | ≥ 3x | *[from dashboard]* |

**Say to the CFO:** *"The number to watch is the guardrail. If it isn't zero, we don't ask for
auto-approval today, no matter how good the rest looks."*

## 5. Who Runs It After We Leave (2 min)
Walk through the ownership table in `deployment_ops/operations_runbook.md#operational-ownership`. The main
point: *"After handover, every alert has a named owner on your side. We stay on call as backup for 30 days,
not as the primary."*

## 6. The Decision (2 min)
Ask for one explicit decision. Don't leave it open-ended.

> "We're asking the CFO and Compliance Officer to jointly approve moving to **limited auto-approval** for
> clean matches below the risk threshold, in the pilot segment only. Everything else keeps going to a
> human. Any false approval automatically suspends auto-approval."

**Possible outcomes:**
- **Approve:** schedule the Compliance sign-off on the threshold value and set the handover date.
- **Approve with conditions:** record each condition with an owner and a date before leaving the room.
- **Not yet:** stay in assisted mode, agree on which metric has to move, and set the date for the next review.

## Likely Questions

| Question | From | Answer |
|---|---|---|
| "What if the model reads an amount wrong?" | CFO | Output is schema-validated. A wrong amount produces a mismatch, which goes to a person. The guardrail stops auto-approval on the first false approval. |
| "Can an auditor see why something was approved?" | Compliance | Yes. Every step is logged with its actor and the prompt/model version (segment 3). |
| "What happens if the model provider changes the model?" | IT/Security | The model and prompt are pinned. Upgrades must pass the golden-dataset gate before release, and rollback means reverting the pinned image. |
| "Is this replacing my team?" | AP Lead | No. It removes the lookup work, and the judgment on real exceptions stays with your team. |
| "When can we add services invoices?" | CFO | Not in Release 1. Their matching logic is different. See `productization/productization_recommendations.md`. |
