"""Final deterministic robustness sweep for the AAAI submission.

It checks the central exponent identity over several covariance powers and visible
profiles, rather than only the settings highlighted in the paper.

Run:
    python experiments/robustness_sweep.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent / "results" / "final_robustness.csv"


def fit_slope(x: np.ndarray, y: np.ndarray) -> float:
    mask = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    X = np.vstack([np.ones(mask.sum()), np.log(x[mask])]).T
    coef, *_ = np.linalg.lstsq(X, np.log(y[mask]), rcond=None)
    return float(coef[1])


def run_case(a: float, theta: float, dimension: int, rho: float) -> dict[str, float]:
    ranks = np.arange(1, dimension + 1, dtype=float)
    lam = ranks ** (-a)
    mu = lam / np.sqrt(lam ** theta + rho)

    lo, hi = 100, min(dimension, 50_000)
    spectral_slope = fit_slope(ranks[lo:hi], mu[lo:hi])
    alpha_obs = -spectral_slope
    alpha_pred = a * (1.0 - theta / 2.0)
    q_obs = 1.0 - alpha_obs / a

    n_values = np.geomspace(10.0, 1000.0, 30)
    counts = np.array([np.count_nonzero(mu >= 1.0 / n) for n in n_values], dtype=float)
    active = (counts >= 10) & (counts <= 0.7 * dimension)
    count_slope = fit_slope(n_values[active], counts[active])
    count_pred = 1.0 / alpha_pred

    return {
        "a": a,
        "theta": theta,
        "alpha_obs": alpha_obs,
        "alpha_pred": alpha_pred,
        "alpha_abs_error": abs(alpha_obs - alpha_pred),
        "q_eff_obs": q_obs,
        "q_eff_pred": theta / 2.0,
        "q_eff_abs_error": abs(q_obs - theta / 2.0),
        "count_slope_obs": count_slope,
        "count_slope_pred": count_pred,
        "count_slope_abs_error": abs(count_slope - count_pred),
    }


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    rows = [
        run_case(a, theta, dimension=200_000, rho=1e-16)
        for a in (1.25, 1.5, 2.0, 3.0)
        for theta in (0.0, 0.25, 0.5, 0.75, 1.0)
    ]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    max_q = max(r["q_eff_abs_error"] for r in rows)
    max_alpha = max(r["alpha_abs_error"] for r in rows)
    max_count = max(r["count_slope_abs_error"] for r in rows)
    print(f"Wrote {len(rows)} rows to {OUT}")
    print(f"max alpha error: {max_alpha:.6g}")
    print(f"max q_eff error: {max_q:.6g}")
    print(f"max learned-count slope error: {max_count:.6g}")


if __name__ == "__main__":
    main()
