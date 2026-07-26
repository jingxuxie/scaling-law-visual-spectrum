# AAAI figure plan

The main paper is limited to seven pages of technical content, so the figures should carry the empirical story efficiently.

## Figure 1 — Visible-spectrum mechanism

**Format:** one full-width schematic with three panels.

### Panel A: what the optimizer observes

Show a covariance ellipse/eigenspectrum on the left and coordinatewise gradient second moments on the right.

Equation callout:

```text
E[g_j^2 | e] = c_e Sigma_jj + 2 (Sigma e)_j^2 ~= c_e Sigma_jj.
```

Message: Adam/RMSProp sees coordinate variances, not eigenvalues directly.

### Panel B: aligned versus globally mixed coordinates

Two columns:

- aligned/band-limited: diagonal second moments follow the spectrum, `q_eff ~= 1/2`;
- Haar/global Gaussian sketch: diagonal second moments are nearly scalar, `q_eff ~= 0`.

### Panel C: downstream scaling law

Flow diagram:

```text
visible theta
 -> q_eff = theta/2
 -> K(n)
 -> risk R(M,N)
 -> compute allocation and AdamW schedule.
```

## Figure 2 — Empirical visibility and stochastic training

**Format:** full-width, three panels, generated from existing results.

### Panel A: `q_eff` by feature system

Plot aligned, band-limited, synthetic theta profiles, Haar, and Gaussian sketch.
Overlay the theoretical line `q_eff = theta/2` for controlled profiles.

### Panel B: tuned final risk versus theta

Use a logarithmic y-axis. Data are in `experiments/key_results.csv`.

### Panel C: hidden-spectrum oracle separation

For Haar and Gaussian sketch, show:

- tuned final risk of coordinatewise adaptive method versus spectral oracle;
- measured `q_eff` next to the bars or in an inset.

The key visual point is that global mixing leaves a useful spectrum, but hides it from coordinatewise adaptivity.

## Figure 3 — Compute and AdamW phase diagrams

**Format:** full-width, three panels.

### Panel A: compute-risk exponent versus theta

Show two theory curves:

- a saturating case `(a,b)=(1.5,1.4)`;
- a hard-source full-range case `(a,b)=(3.0,1.4)`.

Overlay deterministic sweep points.

### Panel B: optimal allocation exponents

Plot exponents of `M_*`, `N_*`, and `K_*` versus theta.

### Panel C: AdamW schedule

Plot compute-risk exponent versus decay-schedule exponent `s` for several theta values. Mark the threshold

```text
s_* = alpha / (max(alpha,b)+1).
```

## Generation

Run:

```bash
python experiments/make_figures.py
```

This creates compact versions of Figures 2 and 3 under `paper/figures/`. Figure 1 is conceptual and should be drawn manually or in a vector-graphics editor.
