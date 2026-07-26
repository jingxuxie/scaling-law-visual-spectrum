# Visible Spectrum: When Adaptive Optimizers Change Scaling Laws

AAAI-27 submission repository for the paper **“Visible Spectrum: When Adaptive Optimizers Change Scaling Laws.”**

The project studies when RMSProp, Adam, and AdamW change scaling exponents rather than only finite-scale constants. The central mechanism is that coordinatewise second moments change spectral scaling only when the optimizer coordinate system exposes the covariance spectrum.

## Repository layout

- `paper/main.tex`: seven-page AAAI-27 main paper source.
- `paper/supplement.tex`: technical supplement with full proofs and extended experimental details.
- `paper/references.bib`: bibliography.
- `paper/FIGURE_PLAN.md`: exact specifications for the final figures.
- `experiments/key_results.csv`: compact table of the results used in the paper.
- `experiments/make_figures.py`: reproduces the paper figures from the compact results table.
- `experiments/validate_claims.py`: checks the numerical claims reported in the manuscript.
- `proofs/PROOF_AUDIT.md`: theorem dependencies, assumptions, and proof status.
- `SUBMISSION_CHECKLIST.md`: AAAI-27 formatting, anonymity, supplement, and reproducibility checklist.

## Build

Download the official AAAI-27 author kit and place `aaai2027.sty` and `aaai2027.bst` in `paper/`. Then run:

```bash
cd paper
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

Build the supplement separately:

```bash
pdflatex supplement
bibtex supplement
pdflatex supplement
pdflatex supplement
```

## Reproduce the compact figures and checks

```bash
python experiments/validate_claims.py
python experiments/make_figures.py
```

The source results were produced in the companion development repository `jingxuxie/scaling-law`; this repository contains the compact, submission-facing artifacts and scripts.

## Submission target

AAAI-27 Main Technical Track. The main manuscript is designed for the seven-page technical-content limit; references occupy pages beyond page seven, and the long proofs are placed in the technical supplement.
