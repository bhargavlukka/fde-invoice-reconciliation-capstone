# Productization Recommendations

## Beyond Invoices
The extraction-plus-reconciliation pattern generalizes to other document-matching problems the same
organization (or future customers) face: expense report vs. receipt matching, contract renewal vs. current
pricing audits, or shipment vs. bill-of-lading reconciliation. The `InvoiceExtraction`/`MatchResult` schema
pair is a specific instance of a general "extract structured fields, reconcile against a system of record"
pattern — the productized version should expose that pattern with pluggable schemas rather than a
hardcoded invoice shape.

## Packaging for New Customers
- Ship as a deployable service (Docker image) with a documented extension point for: (a) the extraction
  schema, (b) the reconciliation rules, (c) the system-of-record connector (PO/contract database today,
  configurable data source later).
- A new customer's onboarding path is: define their document schema → provide a golden dataset → run the
  evaluation gate from `design/evaluation_plan.md` → shadow mode → assisted mode → limited auto-approval,
  exactly the phased rollout used in `adoption/adoption_strategy.md`.

## Cost/Pricing Model
- Primary cost driver is LLM extraction calls (metered via the SharedLLM gateway), which scales with invoice
  volume, not headcount — pricing to the customer should follow the same shape (per-document or tiered
  monthly volume), not a flat seat license.
- Track cost-per-invoice-processed alongside the business success metric (dollar value of errors avoided) so
  the ROI story stays quantifiable as volume grows.

## Roadmap (2-3 Quarters)
1. **Q1:** Complete the pilot, hit exit criteria, expand from one vendor segment to all recurring PO-backed
   vendors.
2. **Q2:** Move from single-tenant Docker Compose to the queue-backed scaling path in
   `deployment_ops/deployment_plan.md`; add a second document-matching use case (e.g. expense/receipt
   matching) to validate the pattern generalizes.
3. **Q3:** Package as a reusable internal platform capability (or, if applicable, an external-facing product)
   with self-serve schema/rule configuration for new use cases, building on the extension points defined
   above.
