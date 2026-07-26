# Reproducibility statement

## Theory

- All assumptions used in the main theorems are stated in `paper/main.tex`.
- Full derivations and proof-scope distinctions are in `paper/supplement.tex` and `proofs/PROOF_AUDIT.md`.
- The sharp risk law relies on the transformed-feature reduction plus the one-pass SGD filter bounds of Lin et al. (2024); the new spectral-sum, visibility, alignment, compute, and AdamW derivations are included.

## Experiments

- Experiments use synthetic Gaussian linear regression and deterministic spectral filters.
- Compact paper values are stored in `experiments/key_results.csv`.
- A final 20-setting exponent robustness sweep is stored in `experiments/results/final_robustness.csv`.
- `experiments/validate_claims.py` verifies all central numerical claims.
- `experiments/make_figures.py` regenerates compact submission figures.
- `experiments/robustness_sweep.py` regenerates the final exponent robustness table.

## Randomness

The companion development experiments use fixed top-level seeds and independent random streams per trial. The submission-facing compact tables report means over the stated number of trials. The wide-LR random-feature comparison uses 10 trials and 16,000 updates.

## Compute

All experiments are laptop-scale. The largest deterministic robustness sweep uses 200,000 synthetic eigenvalues and does not train a model. Stochastic experiments use feature dimensions at most a few thousand, mini-batch Gaussian sampling, and no accelerator-specific code.

## Data and privacy

No external dataset, human subject, sensitive attribute, or personally identifiable information is used.

## Code archive anonymity

Before uploading code to OpenReview, create an anonymous archive without Git history, usernames, absolute local paths, repository remotes, or author-identifying metadata.
