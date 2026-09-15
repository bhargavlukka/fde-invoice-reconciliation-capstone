from extraction.schemas import InvoiceExtraction, MatchResult

PO_DATABASE: dict[str, dict] = {
    "PO-1001": {"vendor": "Acme Supplies", "total": 1200.00},
    "PO-1002": {"vendor": "Globex Materials", "total": 875.50},
}

CONTRACT_DATABASE: dict[str, dict] = {
    "Acme Supplies": {"contract_id": "CT-500", "status": "active"},
    "Globex Materials": {"contract_id": "CT-501", "status": "active"},
}


def reconcile(extraction: InvoiceExtraction) -> MatchResult:
    po = PO_DATABASE.get(extraction.po_reference)
    if po is None:
        return MatchResult(
            status="missing_po",
            invoice_total=extraction.total,
            po_total=None,
            discrepancies=[f"No purchase order found matching reference {extraction.po_reference}."],
        )

    discrepancies = []
    if po["vendor"] != extraction.vendor_name:
        discrepancies.append(
            f"Invoice vendor '{extraction.vendor_name}' does not match PO vendor '{po['vendor']}'."
        )
    if abs(po["total"] - extraction.total) > 0.01:
        discrepancies.append(
            f"Invoice total {extraction.total:.2f} does not match PO total {po['total']:.2f}."
        )

    contract = CONTRACT_DATABASE.get(extraction.vendor_name)
    if contract is None or contract["status"] != "active":
        discrepancies.append(f"No active contract on file for vendor '{extraction.vendor_name}'.")

    status = "match" if not discrepancies else "mismatch"
    return MatchResult(
        status=status,
        invoice_total=extraction.total,
        po_total=po["total"],
        discrepancies=discrepancies,
    )
