# Final experiment report for AAAI-27

## Central claim validation

All compact claim checks pass:

- visible-profile final risk decreases monotonically with `theta`;
- controlled profiles satisfy `q_eff = theta / 2` to numerical precision;
- hard-source compute-risk exponents match theory with maximum absolute error below `0.009`;
- aligned and band-limited features have `q_eff > 0.48`;
- Haar and global Gaussian-sketch coordinates have `|q_eff| < 0.03`;
- after wide learning-rate tuning, the spectral oracle beats coordinatewise adaptive methods by factors of approximately `5.7x` on Gaussian sketch and `6.8x` on Haar;
- a sufficiently fast AdamW decay schedule recovers the no-decay compute exponent.

Run:

```bash
python experiments/validate_claims.py
```

## New final robustness sweep

The final deterministic sweep covers 20 combinations:

```text
a ∈ {1.25, 1.5, 2.0, 3.0}
theta ∈ {0, 0.25, 0.5, 0.75, 1}
```

It verifies:

```text
alpha_eff = a (1 - theta/2)
q_eff = theta/2
learned-count exponent = 1/alpha_eff.
```

Maximum fitted errors:

```text
alpha_eff       0.00125
q_eff           0.00042
learned count   0.0131
```

Run:

```bash
python experiments/robustness_sweep.py
```

## Evidence hierarchy

1. Exact covariance/second-moment identities.
2. Deterministic spectral-filter and learned-count checks.
3. Actual stochastic RMSProp/Adam/AdamW tracking experiments.
4. Coordinate-alignment and visible-profile interpolation.
5. Optimizer-specific learning-rate grids.
6. Source-condition diagnostics.
7. Compute-optimal and AdamW schedule sweeps.
8. Random-feature and global-sketch wide-LR oracle separation.

## Submission conclusion

No additional large experiment is required for the AAAI submission. The highest-value remaining work is figure production, page-limit compression, independent proofreading, and exact formatting with the official AAAI-27 author kit.
