"""Static checks for the anonymous AAAI submission.

Run from the repository root:
    python scripts/check_submission.py

This script does not replace compiling with the official AAAI-27 author kit.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "paper" / "main.tex"
SUPP = ROOT / "paper" / "supplement.tex"
BIB = ROOT / "paper" / "references.bib"

# AAAI's official LaTeX sample loads times/helvet/courier explicitly.  These are
# therefore required rather than prohibited.  The packages below are common
# sources of unauthorized margin, spacing, or hyperlink changes.
REQUIRED_PACKAGES = {"times", "helvet", "courier", "url", "graphicx", "natbib", "caption"}
PROHIBITED_PACKAGES = {
    "hyperref",
    "fullpage",
    "geometry",
    "titlesec",
    "enumitem",
    "wrapfig",
    "multicol",
}

IDENTIFYING_PATTERNS = [
    r"Jingxu",
    r"jingxuxie",
    r"UC Berkeley",
    r"Voleon",
    r"github\.com/jingxuxie",
]


def packages(tex: str) -> set[str]:
    found: set[str] = set()
    for match in re.finditer(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", tex):
        found.update(x.strip() for x in match.group(1).split(","))
    return found


def cite_keys(tex: str) -> set[str]:
    out: set[str] = set()
    for match in re.finditer(r"\\cite\w*\{([^}]*)\}", tex):
        out.update(x.strip() for x in match.group(1).split(","))
    return out


def bib_keys(bib: str) -> set[str]:
    return set(re.findall(r"@\w+\{\s*([^,\s]+)", bib))


def check_file(path: Path, is_main: bool) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    used = packages(text)
    bad = sorted(used & PROHIBITED_PACKAGES)
    if bad:
        errors.append(f"{path}: prohibited or format-risk packages: {bad}")
    missing_required = sorted(REQUIRED_PACKAGES - used)
    if missing_required:
        errors.append(f"{path}: missing official-template packages: {missing_required}")
    if "\\usepackage[submission]{aaai2027}" not in text:
        errors.append(f"{path}: missing AAAI-27 submission style")
    if "\\setlength{\\pdfpagewidth}{8.5in}" not in text or "\\setlength{\\pdfpageheight}{11in}" not in text:
        errors.append(f"{path}: missing official US-Letter PDF dimensions")
    if "\\bibliographystyle" in text:
        errors.append(f"{path}: remove manual bibliographystyle; AAAI style sets it")
    if is_main:
        if "Anonymous AAAI-27 Submission" not in text:
            errors.append("main paper is not explicitly anonymous")
        if re.search(r"\\section\*?\{Acknowledg", text, re.I):
            errors.append("main paper contains acknowledgements")
        for pattern in IDENTIFYING_PATTERNS:
            if re.search(pattern, text, re.I):
                errors.append(f"main paper contains identifying pattern: {pattern}")
    return errors


def main() -> None:
    missing = [str(p) for p in (MAIN, SUPP, BIB) if not p.exists()]
    if missing:
        raise SystemExit(f"Missing required files: {missing}")

    errors = check_file(MAIN, is_main=True) + check_file(SUPP, is_main=False)
    main_text = MAIN.read_text(encoding="utf-8")
    supp_text = SUPP.read_text(encoding="utf-8")
    bib_text = BIB.read_text(encoding="utf-8")
    missing_cites = sorted((cite_keys(main_text) | cite_keys(supp_text)) - bib_keys(bib_text))
    if missing_cites:
        errors.append(f"Missing bibliography keys: {missing_cites}")

    placeholder_count = main_text.count("Replace this rule box")
    if placeholder_count:
        print(f"[WARN] {placeholder_count} figure placeholder(s) remain in main.tex")
    else:
        print("[PASS] no figure placeholders remain")

    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        raise SystemExit(1)

    print("[PASS] AAAI package and bibliography checks")
    print("[PASS] anonymous main-paper source checks")
    print("[NOTE] Compile with the official author kit to verify page count and PDF compliance")


if __name__ == "__main__":
    main()
