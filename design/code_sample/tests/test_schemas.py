# design/code_sample/tests/test_schemas.py
from extraction.schemas import InvoiceExtraction, LineItem, MatchResult


def test_line_item_holds_amount_fields():
    item = LineItem(description="Widget", quantity=10, unit_price=5.0, line_total=50.0)
    assert item.line_total == 50.0


def test_invoice_extraction_requires_line_items_list():
    extraction = InvoiceExtraction(
        vendor_name="Acme Supplies",
        invoice_number="INV-9001",
        po_reference="PO-1001",
        line_items=[LineItem(description="Widget", quantity=10, unit_price=5.0, line_total=50.0)],
        subtotal=50.0,
        tax=0.0,
        total=50.0,
    )
    assert extraction.total == 50.0
    assert len(extraction.line_items) == 1


def test_match_result_status_and_discrepancies():
    result = MatchResult(status="match", invoice_total=50.0, po_total=50.0, discrepancies=[])
    assert result.status == "match"
    assert result.discrepancies == []
