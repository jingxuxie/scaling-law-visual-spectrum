# Paper build instructions

This directory contains the anonymous AAAI-27 main manuscript and technical supplement.

## Required author-kit files

Download the official AAAI-27 author kit from the AAAI-27 conference page and copy these files into this directory:

```text
aaai2027.sty
aaai2027.bst
```

Do not use an older style file for the final submission.

## Main paper

```bash
pdflatex main
bibtex main
pdflatex main
pdflatex main
```

The review version should have no author-identifying information or acknowledgements. Technical content must end by page 7; only references may appear on pages 8--9.

## Supplement

```bash
pdflatex supplement
bibtex supplement
pdflatex supplement
pdflatex supplement
```

AAAI reviewers are not required to read supplementary material. All assumptions critical to evaluating the claims are therefore also stated in `main.tex`.

## Figures

Run from the repository root:

```bash
python experiments/make_figures.py
```

Then replace the placeholder boxes in `main.tex` with the generated figure files. See `FIGURE_PLAN.md` for the recommended composite layouts.
