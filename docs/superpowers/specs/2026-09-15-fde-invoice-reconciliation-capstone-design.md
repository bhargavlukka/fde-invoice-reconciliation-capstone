# FDE Invoice Reconciliation Capstone — Design Spec

**Assignment:** Medhas Academy Module 14, Capstone Project 2 — Full FDE Engagement Simulation.

**Goal:** Simulate a complete Forward Deployed Engineering engagement, end to end, as a public GitHub
repository of artifacts: discovery, scoping, solution design (with a runnable code sample), deployment/ops,
adoption strategy, and productization recommendations. Submission is the repo URL.

**Customer scenario (fixed by the brief):** A mid-sized financial services company manually reviews
supplier invoices against purchase orders and contracts. The process is slow, error-prone, and hard to
scale. Stakeholders: CFO (cost savings), compliance officer (auditability), procurement users (usability,
trust).

**Repo:** `fde-invoice-reconciliation-capstone`, public, under `bhargavlukka`.

**Depth:** Concise, course-appropriate — each document is complete and specific enough to demonstrate the
underlying FDE skill, not padded to look longer than it needs to be.

**Diagrams:** GitHub-native mermaid code blocks embedded directly in the relevant markdown files (no
separate SVG pipeline, unlike Capstone 1 — brief only requires a diagram, not a specific format, and
mermaid renders natively on GitHub with far less tooling).

**Consistency with Capstone 1 (`multi-agent-support-capstone`):** the code sample reuses the same
SharedLLM-gateway-routed Anthropic client pattern (`ANTHROPIC_BASE_URL` / `ANTHROPIC_API_KEY` env vars,
never `api.anthropic.com` directly), the same mock-mode-by-default / `--live` opt-in pattern so grading
requires no API key, and the same "no Claude/AI attribution in commits" rule.

---

## Repository Structure

```
README.md
discovery/
  stakeholder_map.md
  current_state_workflow.md
  interview_notes.md
  problem_statement.md
scoping/
  scope.md
  success_metrics.md
  risk_assessment.md
design/
  architecture.md
  tech_choices.md
  security_plan.md
  evaluation_plan.md
  code_sample/
    pyproject.toml (or requirements.txt)
    .env.example
    extraction/
      schemas.py
      llm_client.py
      agent.py
      mock_backend.py
    fixtures/
      invoice_match.txt / .json (PO + contract + invoice, clean match)
      invoice_mismatch_amount.txt / .json (amount mismatch)
      invoice_missing_po.txt / .json (no matching PO)
    tests/
      test_agent.py
    README.md
deployment_ops/
  deployment_plan.md
  operations_runbook.md
adoption/
  adoption_strategy.md
productization/
  productization_recommendations.md
```

Each top-level directory maps 1:1 to a brief requirement — no `capstone/`-style nesting is needed here
since there's no Python package spanning multiple top-level dirs (the only code lives entirely under
`design/code_sample/`).

---

## Content Plan Per Section

### `discovery/`
- **stakeholder_map.md** — table: name/role, influence (high/med/low), primary concern, RACI-style
  involvement (CFO = approver/sponsor, compliance officer = approver on control design, procurement
  lead = primary user, IT/security = influencer/gatekeeper).
- **current_state_workflow.md** — narrative of today's manual process (AP clerk receives invoice → manually
  pulls PO and contract → eyeballs line items/totals/terms → flags or approves → routes for payment) plus a
  mermaid flowchart, with explicit call-outs of where errors and delay creep in (manual data entry, no
  single source of truth for contract terms, inconsistent escalation).
- **interview_notes.md** — synthesized notes from 3 personas (CFO, compliance officer, procurement/AP
  lead), each with: role/context, top priorities, top fears, a few representative quotes, and implications
  for design.
- **problem_statement.md** — one measurable problem statement (e.g., cut manual invoice review time and
  mismatch-driven payment errors by target percentages within N months) plus a constraints/non-negotiables
  list (human sign-off required before any payment-affecting action, full audit trail, financial/PII data
  stays inside approved boundary, no fully autonomous payment execution in this release).

### `scoping/`
- **scope.md** — Release 1 in-scope: 3-way match (invoice vs. PO vs. contract) for one invoice
  category/vendor segment, automated extraction + match/mismatch verdict, human review queue for
  exceptions and all auto-approvals above a threshold. Out of scope: full AP automation, auto-payment
  execution, multi-currency/multi-language, non-PO spend.
- **success_metrics.md** — SMART metrics under the 5 required categories: primary (e.g., % reduction in
  manual review time), guardrail (e.g., false-approval rate ceiling), quality (extraction field accuracy),
  adoption (% of eligible invoices routed through the tool), business (dollar value of error/rework
  avoided).
- **risk_assessment.md** — risk table (model hallucination on extracted amounts, vendor/contract data
  drift, compliance/audit pushback, procurement trust/adoption risk) each with likelihood, impact,
  mitigation; plus explicit exit/kill criteria for the pilot.

### `design/`
- **architecture.md** — mermaid component diagram: document ingestion → extraction agent → reconciliation
  (3-way match) agent → exception queue → human approval → audit log / downstream AP system; component
  list with one-line responsibility each; data flow narrative.
- **tech_choices.md** — stack choices (Anthropic SDK via SharedLLM gateway for extraction/reasoning,
  Pydantic for typed I/O, a document store + audit log, containerized deployment) each with a short
  rationale and at least one alternative considered and rejected.
- **security_plan.md** — IAM (least-privilege service accounts, role separation between reviewers and
  approvers), data handling (retention, PII/financial data minimization), encryption (at rest/in transit),
  approval workflows (who can approve what, mirroring Capstone 1's human-approval-gate pattern).
- **evaluation_plan.md** — golden dataset description (labeled invoice/PO/contract triples with known
  correct extraction + match verdict), accuracy targets for field extraction and match decisions, drift
  detection approach (periodic re-scoring against the golden set, alert on degradation), regression tests
  gating prompt/model changes before deploy.
- **code_sample/** — runnable core agent pattern: given invoice text + PO text + contract terms, extract
  structured fields via the LLM into a Pydantic schema, then produce a match/mismatch verdict with
  discrepancy detail. Mock mode is default (deterministic canned responses keyed by fixture name, zero
  network calls, zero API key needed); `--live` flag routes through the real SharedLLM-gateway client.
  Ships 3 fixtures (clean match, amount mismatch, missing PO) and pytest tests covering both.

### `deployment_ops/`
- **deployment_plan.md** — Docker Compose for the pilot deployment, secrets via environment variables
  (`.env`, gitignored, `.env.example` documents every var), scaling path (single-tenant pilot container →
  queue-backed horizontal workers as invoice volume grows), rollback plan (versioned/pinned prompts and
  model version, ability to revert to prior container image).
- **operations_runbook.md** — structured logging of every extraction/match/approval decision, key alerts
  (extraction confidence drop, exception-queue backlog, approval SLA breach), and a short incident
  playbook (what to do if the model starts mis-extracting or match accuracy drops).

### `adoption/`
- **adoption_strategy.md** — phased rollout (shadow mode alongside existing manual process → assisted mode
  where the tool suggests and humans confirm → limited auto-approval below a risk threshold), training
  plan for procurement/AP users, change-management/communication plan addressing the 3 personas' concerns,
  feedback loop for continuous improvement.

### `productization/`
- **productization_recommendations.md** — path from single-customer pilot to reusable product: generalizing
  beyond invoices to other document-reconciliation use cases, packaging/deployment model for new customers,
  a cost/pricing model, and a 2-3 quarter roadmap.

### `README.md`
Engagement overview/problem statement, how to navigate the repo (linking every section above), and how to
run the code sample (mock mode, then `--live`).

---

## Out of Scope
- Building a full production system (Capstone 1 already demonstrates that muscle) — this capstone's code
  deliverable is deliberately a single runnable sample of the core agent pattern, not a full multi-agent
  package.
- Real customer data, real API integrations, or an actual deployed pilot — everything is simulated per the
  brief.

## Open Questions
None — all decisions were resolved during brainstorming (repo name, doc depth, diagram format, deployment/
adoption/productization content since the pasted brief didn't detail those sections).
