# Proof audit

This document records the exact scope and dependencies of the paper's claims.

## Theorem stack

### 1. Conditional gradient-second-moment identity

**Status:** complete, exact.

For Gaussian squared loss,

```text
E[g_{t,j}^2 | F_t]
  = (sigma^2 + ||e_t||_Sigma^2) Sigma_jj + 2 (Sigma e_t)_j^2.
```

The two-sided comparison with `Sigma_jj` follows from Cauchy--Schwarz.

### 2. Raw EMA tracking

**Status:** complete under an explicit leverage/effective-window assumption.

The proof uses:

1. degree-four Gaussian-chaos tail control for squared gradients;
2. a leverage bound for exponentially weighted samples;
3. truncation plus conditional Freedman/Bernstein concentration;
4. a union bound over coordinates and times.

The theorem does not claim that every arbitrary Adam trajectory satisfies slow drift. The slow-drift/effective-window condition is stated explicitly.

### 3. Fixed-preconditioner transformation

**Status:** complete, exact.

The change of variables `w = P^{1/2} u` converts fixed preconditioned SGD into ordinary SGD with covariance

```text
Sigma_tilde = P^{1/2} Sigma P^{1/2}.
```

### 4. Visible-spectrum theorem

**Status:** complete, exact under Loewner comparability.

Assumption:

```text
c (Sigma^theta + rho I)^(-1/2)
  <= P <=
C (Sigma^theta + rho I)^(-1/2).
```

Conclusion:

```text
lambda_i(Sigma_tilde)
  ~= lambda_i(Sigma) (lambda_i(Sigma)^theta + rho)^(-1/2).
```

The proof is a congruence argument followed by the min--max principle.

### 5. Learned-mode count and damping knee

**Status:** complete.

For `lambda_i ~= i^{-a}` the active exponent is

```text
alpha = a (1 - theta / 2),
```

and the sample-size knee is

```text
n_rho ~= rho^{-(1/theta - 1/2)}.
```

### 6. Source stability

**Status:** complete in the cases used for the main sharp risk theorem.

- Exact spectral preconditioners preserve each source energy exactly.
- Invariant band decompositions preserve total source mass in each band exactly.
- Globally mixed cases are not claimed to preserve coordinatewise source exponents automatically; they are diagnosed empirically.

### 7. Sharp bias and variance filters

**Status:** complete after reducing to transformed SGD and invoking the one-pass SGD filter bounds of Lin et al. (2024).

The new contribution is the matching spectral-sum evaluation for the two-slope visible spectrum.

Clean source range:

```text
1 < b < alpha + 1.
```

Variance effective-dimension simplification additionally uses `alpha > 1/2`.

### 8. Online adaptive risk law

**Status:** deliberately scoped.

- Sharp risk theorem: fixed/frozen preconditioner.
- Same exponent in aligned online dynamics: follows from commuting coordinatewise sandwich bounds.
- General noncommuting online dynamics: treated as an instantaneous spectral diagnostic and tested empirically; no unrestricted sharp online theorem is claimed.

This distinction must remain visible in the final manuscript.

### 9. Adam first-moment momentum

**Status:** complete for fixed preconditioners.

The slow characteristic root is

```text
1 - gamma mu_i + O((gamma mu_i)^2),
```

so momentum changes constants/stability, not the mode-learning exponent.

### 10. AdamW decay and compute schedule

**Status:** complete.

The exact scalar recursion gives shrinkage floor

```text
delta / (mu_i + delta).
```

For `delta(C) = C^{-s}` the compute-risk exponent is

```text
min((b-1)s/alpha, (b-1)/(max(alpha,b)+1)).
```

### 11. Feature-map cases

**Status:** complete as sufficient conditions.

- Aligned: `theta=1`.
- Band-limited invariant mixing: `theta=1` up to constants.
- Flat coordinate variances or bounded/sub-polynomial diagonal-preconditioner condition number: exponent-level `theta=0`.
- Gaussian sketches: a concentration-based sufficient condition is given; the paper does not claim every Gaussian sketch is uniformly flat in every asymptotic regime.

## Claims intentionally not made

- Adam always beats SGD.
- Better finite-time risk implies a better scaling exponent.
- Every neural-network layer satisfies the visible-spectrum assumption.
- General noncommuting online Adam obeys the same sharp filter law without additional dynamical assumptions.
- Isotropic Gaussian sketches always have a dimension-independent diagonal condition number.

## Remaining author checks

1. Verify that all constants in the main theorem statements are described as independent of scale.
2. Keep critical assumptions in the seven-page main paper; reviewers are not required to read the supplement.
3. Confirm every numerical value against `experiments/key_results.csv`.
4. Replace figure placeholders with outputs from `experiments/make_figures.py`.
5. Compile using the official AAAI-27 author kit and verify that technical content ends by page 7.
