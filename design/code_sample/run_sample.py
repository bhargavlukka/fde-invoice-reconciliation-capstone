import argparse
import json
from pathlib import Path

from extraction.agent import extract_invoice_fields
from extraction.llm_client import complete, get_anthropic_client
from extraction.mock_backend import mock_complete
from extraction.reconciliation import reconcile

FIXTURES_DIR = Path(__file__).parent / "fixtures"
FIXTURE_NAMES = ["invoice_match", "invoice_amount_mismatch", "invoice_missing_po"]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the invoice extraction + 3-way match agent on a sample fixture."
    )
    parser.add_argument("fixture", choices=FIXTURE_NAMES)
    parser.add_argument(
        "--live",
        action="store_true",
        help="Call the real SharedLLM-gateway-routed model instead of the mock backend.",
    )
    args = parser.parse_args()

    invoice_text = (FIXTURES_DIR / f"{args.fixture}.txt").read_text()

    if args.live:
        client = get_anthropic_client()
        complete_fn = complete
    else:
        client = object()
        complete_fn = mock_complete

    extraction = extract_invoice_fields(invoice_text, client=client, complete_fn=complete_fn)
    result = reconcile(extraction)

    print(json.dumps(
        {"extraction": extraction.model_dump(), "match_result": result.model_dump()},
        indent=2,
    ))


if __name__ == "__main__":
    main()
