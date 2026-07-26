"""Build an anonymous code archive for supplementary submission.

Run from the repository root:
    python scripts/make_anonymous_archive.py

The archive excludes Git metadata, generated PDFs, identifying project metadata,
and this submission-management script itself. Inspect the resulting ZIP before
uploading it to OpenReview.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "anonymous_code_supplement.zip"

EXCLUDE_PARTS = {
    ".git",
    ".github",
    "__pycache__",
    ".venv",
}
EXCLUDE_FILES = {
    "SUBMISSION_CHECKLIST.md",
    "anonymous_code_supplement.zip",
}
TEXT_SUFFIXES = {".py", ".tex", ".bib", ".md", ".txt", ".csv", ".json", ".yml", ".yaml"}
IDENTIFYING_PATTERNS = [
    re.compile(r"jingxuxie", re.I),
    re.compile(r"github\.com/jingxuxie", re.I),
    re.compile(r"Jingxu\s+Xie", re.I),
    re.compile(r"UC\s+Berkeley", re.I),
]


def included(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDE_PARTS for part in rel.parts):
        return False
    if path.name in EXCLUDE_FILES:
        return False
    if path.suffix in {".pdf", ".aux", ".bbl", ".blg", ".log", ".out"}:
        return False
    return path.is_file()


def scan_text(path: Path) -> list[str]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    return [pattern.pattern for pattern in IDENTIFYING_PATTERNS if pattern.search(text)]


def main() -> None:
    files = sorted(path for path in ROOT.rglob("*") if included(path))
    problems: list[str] = []
    for path in files:
        matches = scan_text(path)
        if matches:
            problems.append(f"{path.relative_to(ROOT)}: {matches}")
    if problems:
        print("Identifying strings found; archive was not created:")
        for problem in problems:
            print(f"  {problem}")
        raise SystemExit(1)

    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, path.relative_to(ROOT))
    print(f"Wrote anonymous archive with {len(files)} files: {OUTPUT}")
    print("Manually inspect the ZIP before submission.")


if __name__ == "__main__":
    main()
