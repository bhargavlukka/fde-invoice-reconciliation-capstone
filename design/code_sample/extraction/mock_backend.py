import json
import re

from extraction.llm_client import LLMResponse

_FIELD_PATTERNS = {
    "invoice_number": re.compile(r"^Invoice Number:\s*(\S+)", re.MULTILINE),
    "vendor_name": re.compile(r"^Vendor:\s*(.+)$", re.MULTILINE),
    "po_reference": re.compile(r"^PO Reference:\s*(\S+)", re.MULTILINE),
    "subtotal": re.compile(r"^Subtotal:\s*([\d.]+)", re.MULTILINE),
    "tax": re.compile(r"^Tax:\s*([\d.]+)", re.MULTILINE),
    "total": re.compile(r"^Total:\s*([\d.]+)", re.MULTILINE),
}
_LINE_ITEM_PATTERN = re.compile(
    r"^-\s*(.+?)\s*\|\s*Qty:\s*([\d.]+)\s*\|\s*Unit Price:\s*([\d.]+)\s*\|\s*Line Total:\s*([\d.]+)\s*$",
    re.MULTILINE,
)


def mock_complete(client, system: str, messages: list[dict], tools: list[dict] | None = None, model: str | None = None) -> LLMResponse:
    """Deterministically 'extracts' fields from a structured invoice document via regex,
    standing in for the real LLM call so the sample is runnable without an API key."""
    invoice_text = messages[-1]["content"]

    fields = {}
    for name, pattern in _FIELD_PATTERNS.items():
        match = pattern.search(invoice_text)
        fields[name] = match.group(1).strip() if match else None

    line_items = [
        {
            "description": desc.strip(),
            "quantity": float(qty),
            "unit_price": float(price),
            "line_total": float(total),
        }
        for desc, qty, price, total in _LINE_ITEM_PATTERN.findall(invoice_text)
    ]

    payload = {
        "vendor_name": fields["vendor_name"],
        "invoice_number": fields["invoice_number"],
        "po_reference": fields["po_reference"],
        "line_items": line_items,
        "subtotal": float(fields["subtotal"]),
        "tax": float(fields["tax"]),
        "total": float(fields["total"]),
    }

    return LLMResponse(text=json.dumps(payload), tool_calls=[], stop_reason="end_turn")
