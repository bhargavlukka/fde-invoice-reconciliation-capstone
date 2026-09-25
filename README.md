# FDE Invoice Reconciliation — Full Engagement Simulation

## About This Repository
This repository simulates a complete Forward Deployed Engineering (FDE) engagement, from discovery through
productization, for a fictional customer. It was built for Medhas Academy Module 14, Capstone Project 2: Full
FDE Engagement Simulation.

## Customer Scenario
A mid-sized financial services company manually reviews supplier invoices against purchase orders and
contracts. The process is slow, error-prone, and hard to scale. Stakeholders: the CFO (cost savings), the
compliance officer (auditability), and procurement users (usability and trust). See
`discovery/problem_statement.md` for the full, measurable problem statement.

## How to Navigate This Repository
- [`discovery/`](discovery/) — stakeholder map, current-state workflow, synthesized interview notes, problem statement and constraints.
- [`scoping/`](scoping/) — Release 1 scope, SMART success metrics, risk assessment and exit criteria.
- [`design/`](design/) — architecture, technology choices, security plan, evaluation plan, and a runnable code sample.
- [`deployment_ops/`](deployment_ops/) — deployment plan and operations runbook (including operational ownership).
- [`demo/`](demo/) — final stakeholder demo script for the go/no-go review.
- [`adoption/`](adoption/) — phased adoption strategy.
- [`productization/`](productization/) — path from pilot to reusable product.

## Running the Code Sample
```bash
cd design/code_sample
pip install -r requirements.txt
cp .env.example .env   # only needed for --live; mock mode needs no credentials

# Mock mode (default, no API key required)
python run_sample.py invoice_match
python run_sample.py invoice_amount_mismatch
python run_sample.py invoice_missing_po

# Live mode (routes through the real SharedLLM-gateway model)
python run_sample.py invoice_match --live

# Run tests
pytest
```

See [`design/code_sample/README.md`](design/code_sample/README.md) for details on what each file does.
