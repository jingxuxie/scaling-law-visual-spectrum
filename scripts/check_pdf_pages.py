"""Audit the compiled AAAI main PDF.

AAAI allows seven pages of technical content and at most nine pages total, with
pages beyond seven reserved for references.  This script checks total length,
locates the References heading, and rejects technical prose preceding it on
page eight.
"""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

PDF = Path(__file__).resolve().parents[1] / "paper" / "main.pdf"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    if not PDF.exists():
        raise SystemExit(f"Missing compiled PDF: {PDF}")
    reader = PdfReader(str(PDF))
    total = len(reader.pages)
    print(f"main.pdf pages: {total}")
    if total > 9:
        raise SystemExit("AAAI main PDF exceeds the nine-page total limit")

    reference_page = None
    reference_offset = None
    for i, page in enumerate(reader.pages, start=1):
        text = normalize(page.extract_text() or "")
        offset = text.find("References")
        if offset >= 0:
            reference_page = i
            reference_offset = offset
            break
    if reference_page is None or reference_offset is None:
        raise SystemExit("Could not find a References heading in the PDF")

    print(f"References begin on page: {reference_page}")
    print(f"Characters before References on that page: {reference_offset}")

    if reference_page > 8:
        raise SystemExit("References begin after page 8; technical content exceeds seven pages")
    if reference_page == 8 and reference_offset > 250:
        raise SystemExit(
            "Technical prose precedes References on page 8; pages after seven must be references only"
        )
    if reference_page < 7:
        print("[WARN] References begin before page 7; the paper may remain substantially under length")
    elif reference_page == 7:
        print("[WARN] References begin on page 7; some technical-page budget remains")
    else:
        print("[PASS] Seven technical pages are followed by references-only pages")


if __name__ == "__main__":
    main()
