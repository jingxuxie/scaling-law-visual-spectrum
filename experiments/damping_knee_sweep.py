"""Verify the two-slope damping transition in the visible-spectrum theorem.

This is a deterministic experiment on the exact effective spectrum

    mu(i) = lambda(i) / sqrt(lambda(i)^theta + rho),
    lambda(i) = i^{-a}.

Rather than truncating to a finite dimension, we solve n * mu(i) = 1 by
log-space bisection.  This allows clean fits far below and far above the
predicted knee

    n_rho = rho^{-(1/theta - 1/2)}.

Run from the repository root:

    python experiments/damping_knee_sweep.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent / "results" / "damping_knee_sweep.csv"


def fit_slope(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    X = np.vstack([np.ones(mask.sum()), np.log(x[mask])]).T
    coef, *_ = np.linalg.lstsq(X, np.log(y[mask]), rcond=None)
    return float(coef[1])


def learned_count_continuous(a: float, theta: float, rho: float, n: float) -> float:
    """Solve n * mu(i) = 1 for continuous rank i >= 1."""

    def log_margin(log_i: float) -> float:
        i = math.exp(log_i)
        lam = i ** (-a)
        mu = lam / math.sqrt(lam**theta + rho)
        return math.log(n * mu)

    if log_margin(0.0) < 0:
        return 0.0

    lo, hi = 0.0, 1.0
    while log_margin(hi) > 0:
        hi *= 2.0
        if hi > 128.0:
            raise RuntimeError("failed to bracket learned-mode cutoff")

    for _ in range(120):
        mid = (lo + hi) / 2.0
        if log_margin(mid) > 0:
            lo = mid
        else:
            hi = mid
    return math.exp((lo + hi) / 2.0)


def run_case(a: float, theta: float, rho: float) -> dict[str, float]:
    n_knee = rho ** (-(1.0 / theta - 0.5))
    pre_n = np.geomspace(n_knee / 1e4, n_knee / 20.0, 50)
    post_n = np.geomspace(n_knee * 20.0, n_knee * 1e4, 50)

    pre_k = np.array(
        [learned_count_continuous(a, theta, rho, n) for n in pre_n]
    )
    post_k = np.array(
        [learned_count_continuous(a, theta, rho, n) for n in post_n]
    )

    pre_pred = 1.0 / (a * (1.0 - theta / 2.0))
    post_pred = 1.0 / a
    pre_obs = fit_slope(pre_n, pre_k)
    post_obs = fit_slope(post_n, post_k)

    return {
        "a": a,
        "theta": theta,
        "rho": rho,
        "n_knee_pred": n_knee,
        "pre_slope_obs": pre_obs,
        "pre_slope_pred": pre_pred,
        "pre_abs_error": abs(pre_obs - pre_pred),
        "post_slope_obs": post_obs,
        "post_slope_pred": post_pred,
        "post_abs_error": abs(post_obs - post_pred),
    }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cases = [
        (1.5, 1.0, 1e-8),
        (1.5, 0.75, 1e-6),
        (1.5, 0.5, 1e-3),
    ]
    rows = [run_case(*case) for case in cases]

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(rows[0].keys()),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(
            f"theta={row['theta']:.2f}, rho={row['rho']:.1e}, "
            f"n_knee={row['n_knee_pred']:.3g}, "
            f"pre={row['pre_slope_obs']:.4f}/{row['pre_slope_pred']:.4f}, "
            f"post={row['post_slope_obs']:.4f}/{row['post_slope_pred']:.4f}"
        )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
