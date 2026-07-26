# Visible Spectrum: When Adaptive Optimizers Change Scaling Laws

AAAI-27 submission repository for the paper **“Visible Spectrum: When Adaptive Optimizers Change Scaling Laws.”**

The project studies when RMSProp, Adam, and AdamW change scaling exponents rather than only finite-scale constants. The central mechanism is that coordinatewise second moments change spectral scaling only when the optimizer coordinate system exposes the covariance spectrum.

## Current status

The submission-facing theorem stack, technical supplement, compact experiment tables, robustness sweep, claim checks, figure scripts, proof audit, and reproducibility materials are in place. The remaining manual gates are:

1. confirm that an AAAI-27 abstract was registered by the July 21 deadline;
2. download the official AAAI-27 author kit;
3. generate/insert the final figures;
4. compile and compress the main technical content to seven pages;
5. upload the anonymous supplement and code archive by July 31.

## Repository layout

- `paper/main.tex`: anonymous AAAI-27 main paper source.
- `paper/supplement.tex`: technical supplement with full proofs and extended experimental details.
- `paper/references.bib`: bibliography.
- `paper/abstract.txt` and `paper/keywords.txt`: OpenReview submission text.
- `paper/FIGURE_PLAN.md`: exact specifications for the final figures.
- `experiments/key_results.csv`: compact table of the results used in the paper.
- `experiments/make_figures.py`: reproduces compact paper figures.
- `experiments/validate_claims.py`: checks the numerical claims reported in the manuscript.
- `experiments/robustness_sweep.py`: regenerates the final 20-setting exponent robustness sweep.
- `proofs/PROOF_AUDIT.md`: theorem dependencies, assumptions, and proof status.
- `scripts/check_submission.py`: static anonymity, package, and bibliography checks.
- `scripts/make_anonymous_archive.py`: builds an anonymous code ZIP after scanning identifying strings.
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

## Reproduce figures and checks

```bash
pip install -r requirements.txt
python scripts/check_submission.py
python experiments/validate_claims.py
python experiments/robustness_sweep.py
python experiments/make_figures.py
```

Build the anonymous code archive only after all checks pass:

```bash
python scripts/make_anonymous_archive.py
```

The full raw experimental outputs were produced in the companion development repository `jingxuxie/scaling-law`; this repository contains the compact, submission-facing artifacts and scripts.

## Submission target

AAAI-27 Main Technical Track. The main manuscript is designed for the seven-page technical-content limit; references occupy pages beyond page seven, and long proofs are placed in the technical supplement.
