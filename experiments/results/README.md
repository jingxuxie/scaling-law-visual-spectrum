# Compact AAAI experiment results

This directory contains the compact result tables used by the AAAI-27 paper.

## `final_robustness.csv`

A new deterministic robustness sweep over

```text
a ∈ {1.25, 1.5, 2.0, 3.0}
theta ∈ {0, 0.25, 0.5, 0.75, 1.0}
```

checks the identities

```text
alpha_eff = a (1 - theta / 2)
q_eff = theta / 2
learned-count slope = 1 / alpha_eff.
```

Across 20 settings, the maximum fitted errors are approximately:

```text
max alpha error             0.00125
max q_eff error             0.00042
max learned-count error     0.0131
```

The small residual learned-count error comes from integer mode counts and finite fitting windows.

## `../key_results.csv`

A compact table copied from the full development sweeps. It contains the values used in the main paper for:

- controlled visible-profile training;
- hard-source compute-optimal scaling;
- random-feature/sketch wide-learning-rate comparisons;
- compute-dependent AdamW schedules.

The complete raw outputs and training curves remain available in the companion development repository `jingxuxie/scaling-law`.
