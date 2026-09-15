from pathlib import Path

from extraction.agent import extract_invoice_fields
from extraction.mock_backend import mock_complete

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def test_extract_clean_match_invoice():
    text = (FIXTURES_DIR / "invoice_match.txt").read_text()
    extraction = extract_invoice_fields(text, client=object(), complete_fn=mock_complete)
    assert extraction.invoice_number == "INV-9001"
    assert extraction.vendor_name == "Acme Supplies"
    assert extraction.po_reference == "PO-1001"
    assert extraction.total == 1200.00
    assert len(extraction.line_items) == 2


def test_extract_amount_mismatch_invoice():
    text = (FIXTURES_DIR / "invoice_amount_mismatch.txt").read_text()
    extraction = extract_invoice_fields(text, client=object(), complete_fn=mock_complete)
    assert extraction.invoice_number == "INV-9002"
    assert extraction.total == 1300.00


def test_extract_missing_po_invoice():
    text = (FIXTURES_DIR / "invoice_missing_po.txt").read_text()
    extraction = extract_invoice_fields(text, client=object(), complete_fn=mock_complete)
    assert extraction.po_reference == "PO-9999"
    assert extraction.vendor_name == "Globex Materials"
