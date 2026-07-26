"""Audit the compiled AAAI main PDF.

The AAAI main track allows seven pages of technical content and at most nine
pages total, with pages beyond seven reserved for references.  This script
checks total length and reports the first page containing the References heading.
"""

from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

PDF = Path(__file__).resolve().parents[1] / "paper" / "main.pdf"


def main() -> None:
    if not PDF.exists():
        raise SystemExit(f"Missing compiled PDF: {PDF}")
    reader = PdfReader(str(PDF))
    total = len(reader.pages)
    print(f"main.pdf pages: {total}")
    if total > 9:
        raise SystemExit("AAAI main PDF exceeds the nine-page total limit")

    reference_page = None
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if "References" in text:
            reference_page = i
            break
    if reference_page is None:
        raise SystemExit("Could not find a References heading in the PDF")
    print(f"References begin on page: {reference_page}")
    if reference_page > 8:
        raise SystemExit("References begin after page 8; technical content likely exceeds seven pages")
    if reference_page < 6:
        print("[WARN] References begin before page 6; the paper may still be substantially under length")
    elif reference_page == 8:
        print("[PASS] Technical content fills seven pages before references")
    else:
        print("[PASS] References begin within the allowed range")


if __name__ == "__main__":
    main()
