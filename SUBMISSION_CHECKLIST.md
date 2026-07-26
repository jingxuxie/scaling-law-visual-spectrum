# AAAI-27 submission checklist

Target: AAAI-27 Main Technical Track.

## Deadlines

All AAAI deadlines are Anywhere on Earth (UTC-12).

- Abstract registration: **July 21, 2026**.
- Full paper: **July 28, 2026**.
- Supplementary material and code: **July 31, 2026**.

The full-paper submission requires a previously registered abstract. Confirm immediately that the abstract exists in OpenReview and that the title/author list are correct.

## Format

- Use the official AAAI-27 author kit (`aaai2027.sty`, `aaai2027.bst`).
- Anonymous, double-blind main-track submission.
- US Letter, AAAI two-column format.
- At most **7 pages of technical content**.
- Maximum total length **9 pages**; pages after page 7 are references only.
- No acknowledgements in the review version.
- Do not modify margins, font sizes, spacing, or style-file settings.
- Use embedded Type 1 or TrueType fonts and a high-resolution PDF.

## Scientific content

- [ ] Keep the exact scope distinction between fixed/frozen sharp risk theorems and general online noncommuting diagnostics.
- [ ] State the transformed-source assumption in the main paper.
- [ ] Keep the EMA effective-window condition in the main paper.
- [ ] Include the two main negative cases: flat/Haar and global Gaussian sketch.
- [ ] Distinguish finite-time risk gains from spectral-exponent gains.
- [ ] Replace all figure placeholders.
- [ ] Verify every number against `experiments/key_results.csv`.
- [ ] Run `python experiments/validate_claims.py`.
- [ ] Run `python experiments/robustness_sweep.py`.

## Supplement

- [ ] Build `paper/supplement.tex` as a separate PDF.
- [ ] Include full raw-EMA, source-stability, risk-filter, compute, momentum, AdamW, and feature-map proofs.
- [ ] Include extended hyperparameter grids and trial details.
- [ ] Include a pointer from the main paper, but keep all critical claims understandable without the supplement.

## Reproducibility

- [ ] Upload code by July 31.
- [ ] Complete the AAAI reproducibility checklist in OpenReview.
- [ ] Record software versions and random seeds.
- [ ] Confirm that the anonymous code archive contains no author names, Git history, usernames, absolute paths, or identifying URLs.
- [ ] Verify that the companion repository or code archive is anonymous during review.

## Final PDF audit

- [ ] Technical content ends by page 7.
- [ ] Pages 8--9 contain references only.
- [ ] No author names or affiliations.
- [ ] No acknowledgements.
- [ ] No broken citations or references.
- [ ] No overfull boxes visible in the PDF.
- [ ] All plots are legible when printed in grayscale.
- [ ] All theorem assumptions are stated before use.
- [ ] Abstract and OpenReview abstract match closely.
