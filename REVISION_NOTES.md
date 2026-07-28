# AAAI expansion revision

This package expands the current AAAI manuscript by roughly two to three
two-column pages while strengthening the scientific story rather than adding
padding.

## Main-paper additions

1. **Clearer scope statement.**
   The revised paper distinguishes:
   - exact fixed/frozen-preconditioner risk laws;
   - aligned commuting online RMSProp/Adam corollaries;
   - noncommuting feature systems, for which `q_eff` is a spectral diagnostic
     validated empirically.

2. **More complete proofs in the main paper.**
   Added:
   - the proof of the gradient-second-moment identity;
   - a proof sketch for the matching bias and variance spectral sums;
   - an aligned online RMSProp/Adam corollary;
   - a formal visibility phase transition;
   - the exact AdamW coordinate recursion;
   - a hidden-spectrum oracle-separation proposition;
   - a subpolynomial-mixing proposition;
   - a Gaussian-sketch concentration statement.

3. **More explanatory structure.**
   Added:
   - a table separating the roles of second moments, momentum, and weight decay;
   - a feature-geometry table explaining when spectrum is visible;
   - a new section of testable predictions for block optimizers, damping,
     weight decay, and deep-network diagnostics.

4. **Additional experiment.**
   Added a deterministic damping-knee sweep that verifies both predicted
   regimes:
   - pre-knee learned-count slope `1/[a(1-theta/2)]`;
   - post-knee slope `1/a`.

5. **Expanded experimental protocol and robustness discussion.**
   The main paper now explains dimensions, trials, learning-rate grids,
   checkpoints, source construction, `q_eff` estimation, source diagnostics,
   and the existing 20-setting robustness sweep.

6. **Expanded related work.**
   Added recent work on:
   - optimizer-dependent neural scaling laws;
   - mini-batch/data-reuse scaling laws;
   - matrix-preconditioned optimizer transfer;
   - SOAP and rotated-basis adaptivity;
   - Adam implicit bias;
   - Hanson--Wright concentration for Gaussian sketches.

## Files

- `paper/main.tex`: full replacement for the current main manuscript.
- `paper/references.bib`: full replacement bibliography.
- `experiments/damping_knee_sweep.py`: new experiment.
- `experiments/results/damping_knee_sweep.csv`: generated results.

## Approximate page check

Using a local two-column syntax-check stub with margins close to the AAAI
layout, the revised document placed references on page 8 and produced 9 pages
total. This is only an approximation: the official `aaai2027.sty` compile is
authoritative. After copying the files, compile immediately and trim or restore
small paragraphs so that technical content ends on page 7.

## Apply

From the extracted package directory:

```bash
cp paper/main.tex /path/to/scaling-law-visual-spectrum/paper/main.tex
cp paper/references.bib /path/to/scaling-law-visual-spectrum/paper/references.bib
cp experiments/damping_knee_sweep.py \
   /path/to/scaling-law-visual-spectrum/experiments/damping_knee_sweep.py
mkdir -p /path/to/scaling-law-visual-spectrum/experiments/results
cp experiments/results/damping_knee_sweep.csv \
   /path/to/scaling-law-visual-spectrum/experiments/results/damping_knee_sweep.csv
```

Then:

```bash
cd /path/to/scaling-law-visual-spectrum
python experiments/damping_knee_sweep.py
cd paper
pdflatex main
bibtex main
pdflatex main
pdflatex main
```
