# Invoice Extraction + 3-Way Match — Runnable Code Sample

Demonstrates the core agent pattern from `../architecture.md`: extract structured fields from a raw invoice
document via an LLM call, then reconcile them against simulated PO and contract backends.

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env   # only needed for --live
```

## Run (mock mode — default, no API key needed)
```bash
python run_sample.py invoice_match
python run_sample.py invoice_amount_mismatch
python run_sample.py invoice_missing_po
```

## Run (live mode — routes through the real SharedLLM-gateway model)
```bash
python run_sample.py invoice_match --live
```

## Test
```bash
pytest
```

## Files
- `extraction/schemas.py` — typed `LineItem`, `InvoiceExtraction`, `MatchResult` (Pydantic).
- `extraction/llm_client.py` — SharedLLM-gateway-routed Anthropic client wrapper.
- `extraction/agent.py` — `extract_invoice_fields()`, the core LLM agent call.
- `extraction/mock_backend.py` — deterministic regex-based stand-in for the LLM, used by default so the
  sample runs without credentials.
- `extraction/reconciliation.py` — `reconcile()` plus the simulated `PO_DATABASE`/`CONTRACT_DATABASE`.
- `fixtures/` — three sample invoices: a clean match, an amount mismatch, and a missing-PO case.
