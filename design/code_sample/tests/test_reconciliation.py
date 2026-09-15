from pathlib import Path

from extraction.agent import extract_invoice_fields
from extraction.mock_backend import mock_complete
from extraction.reconciliation import reconcile

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def _extract(fixture_name: str):
    text = (FIXTURES_DIR / f"{fixture_name}.txt").read_text()
    return extract_invoice_fields(text, client=object(), complete_fn=mock_complete)


def test_reconcile_clean_match():
    extraction = _extract("invoice_match")
    result = reconcile(extraction)
    assert result.status == "match"
    assert result.discrepancies == []
    assert result.po_total == 1200.00


def test_reconcile_amount_mismatch():
    extraction = _extract("invoice_amount_mismatch")
    result = reconcile(extraction)
    assert result.status == "mismatch"
    assert any("total" in d for d in result.discrepancies)


def test_reconcile_missing_po():
    extraction = _extract("invoice_missing_po")
    result = reconcile(extraction)
    assert result.status == "missing_po"
    assert result.po_total is None
