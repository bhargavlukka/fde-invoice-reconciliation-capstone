from pydantic import BaseModel


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    line_total: float


class InvoiceExtraction(BaseModel):
    vendor_name: str
    invoice_number: str
    po_reference: str
    line_items: list[LineItem]
    subtotal: float
    tax: float
    total: float


class MatchResult(BaseModel):
    status: str  # "match" | "mismatch" | "missing_po"
    invoice_total: float
    po_total: float | None
    discrepancies: list[str]
