# Paper build instructions

This directory contains the anonymous AAAI-27 main manuscript and technical supplement.

## Source layout

`main.tex` now imports three modular expansion files:

```text
additional_analysis.tex       formal feature-map guarantees and exponent consequences
experiment_addendum.tex       protocol, robustness, source diagnostics, and practical use
related_work_addendum.tex     recent scaling, optimizer-transfer, and random-feature work
```

The bibliography is split across `references.bib` and `additional_references.bib`.

## AAAI-27 author kit

The repository includes the official author kit in `../AAAI_AuthorKit27`.
The manuscript uses its `aaai2027.sty` and `aaai2027.bst` files directly; do
not substitute an older style.

## Figures

From the repository root, generate the seven vector figure panels:

```bash
python experiments/make_figures.py
```

This writes PDF and PNG versions under `paper/figures/`. The main manuscript
embeds the vector PDF versions as three numbered figures. PDF figures are no
longer ignored by Git so that the final submission sources can be self-contained.

## Main paper

From `paper/`, build with the bundled style and bibliography search paths:

```bash
TEXINPUTS=../AAAI_AuthorKit27: \
BSTINPUTS=../AAAI_AuthorKit27: \
BIBINPUTS=.: \
latexmk -pdf main.tex
```

The review version should have no author-identifying information or acknowledgements. Technical content must end by page 7; only references may appear on pages 8--9.

## Supplement

```bash
TEXINPUTS=../AAAI_AuthorKit27: \
BSTINPUTS=../AAAI_AuthorKit27: \
BIBINPUTS=.: \
latexmk -pdf supplement.tex
```

AAAI reviewers are not required to read supplementary material. All assumptions critical to evaluating the claims are therefore also stated in `main.tex`.

## Checks

From the repository root:

```bash
python scripts/check_submission.py
python experiments/validate_claims.py
python experiments/robustness_sweep.py
```
