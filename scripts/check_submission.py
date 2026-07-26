"""Static checks for the anonymous AAAI submission.

Run from the repository root:
    python scripts/check_submission.py

This script does not replace compiling with the official AAAI-27 author kit.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
MAIN = PAPER / "main.tex"
SUPP = PAPER / "supplement.tex"
MAIN_INPUTS = [
    PAPER / "additional_analysis.tex",
    PAPER / "experiment_addendum.tex",
    PAPER / "discussion_addendum.tex",
    PAPER / "related_work_addendum.tex",
]
BIBS = [PAPER / "references.bib", PAPER / "additional_references.bib"]

# The current official template explicitly protects these packages in main.tex.
REQUIRED_MAIN_PACKAGES = {"url", "graphicx", "natbib", "caption"}
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


def identifying_errors(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    for pattern in IDENTIFYING_PATTERNS:
        if re.search(pattern, text, re.I):
            errors.append(f"{path}: identifying pattern: {pattern}")
    return errors


def check_main() -> list[str]:
    text = MAIN.read_text(encoding="utf-8")
    errors: list[str] = []
    used = packages(text)
    bad = sorted(used & PROHIBITED_PACKAGES)
    if bad:
        errors.append(f"{MAIN}: prohibited or format-risk packages: {bad}")
    missing_required = sorted(REQUIRED_MAIN_PACKAGES - used)
    if missing_required:
        errors.append(f"{MAIN}: missing protected template packages: {missing_required}")
    if "\\usepackage[submission]{aaai2027}" not in text:
        errors.append(f"{MAIN}: missing AAAI-27 submission style")
    if "\\bibliographystyle" in text:
        errors.append(f"{MAIN}: remove manual bibliographystyle; AAAI style sets it")
    if "Anonymous Submission" not in text:
        errors.append("main paper is not explicitly anonymous")
    if re.search(r"\\section\*?\{Acknowledg", text, re.I):
        errors.append("main paper contains acknowledgements")
    errors.extend(identifying_errors(MAIN, text))
    return errors


def main() -> None:
    required = [MAIN, SUPP, *MAIN_INPUTS, *BIBS]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit(f"Missing required files: {missing}")

    errors = check_main()

    source_paths = [MAIN, SUPP, *MAIN_INPUTS]
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in source_paths)
    bib_text = "\n".join(path.read_text(encoding="utf-8") for path in BIBS)
    missing_cites = sorted(cite_keys(source_text) - bib_keys(bib_text))
    if missing_cites:
        errors.append(f"Missing bibliography keys: {missing_cites}")

    for path in MAIN_INPUTS:
        errors.extend(identifying_errors(path, path.read_text(encoding="utf-8")))

    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        raise SystemExit(1)

    print("[PASS] AAAI package and modular-source checks")
    print("[PASS] bibliography keys resolve across both BibTeX files")
    print("[PASS] anonymous main-paper source checks")
    print("[NOTE] Compile with the official author kit to verify page count and PDF compliance")


if __name__ == "__main__":
    main()
