"""Validate the compact numerical claims used in the AAAI manuscript.

Run from the repository root:
    python experiments/validate_claims.py
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "key_results.csv"


def load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get(rows: list[dict[str, str]], experiment: str, setting: str, metric: str) -> float:
    matches = [
        r for r in rows
        if r["experiment"] == experiment
        and r["setting"] == setting
        and r["metric"] == metric
    ]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one row for {(experiment, setting, metric)}, got {len(matches)}")
    return float(matches[0]["value"])


def main() -> None:
    rows = load_rows()
    checks: list[tuple[str, bool, str]] = []

    # Controlled theta interpolation.
    theta_settings = ["theta=0.00", "theta=0.25", "theta=0.50", "theta=0.75", "theta=1.00"]
    risks = [get(rows, "visible_profile", s, "final_risk") for s in theta_settings]
    checks.append((
        "visible-profile final risk decreases monotonically",
        all(risks[i + 1] < risks[i] for i in range(len(risks) - 1)),
        str(risks),
    ))
    q_errors = []
    for s in theta_settings:
        row = next(r for r in rows if r["experiment"] == "visible_profile" and r["setting"] == s and r["metric"] == "q_eff")
        q_errors.append(abs(float(row["value"]) - float(row["predicted"])))
    checks.append(("q_eff = theta/2 in controlled profiles", max(q_errors) < 1e-8, f"max error={max(q_errors):.3g}"))

    # Compute-optimal theorem.
    compute_rows = [r for r in rows if r["experiment"] == "compute_hard" and r["metric"] == "risk_exponent"]
    compute_errors = [abs(float(r["value"]) - float(r["predicted"])) for r in compute_rows]
    checks.append(("hard-source compute exponents match theory", max(compute_errors) < 0.01, f"max error={max(compute_errors):.4f}"))

    # Visibility split in random features.
    aligned = get(rows, "random_feature", "aligned_adam", "q_eff")
    band = get(rows, "random_feature", "band_adam", "q_eff")
    sketch = get(rows, "random_feature", "gaussian_sketch_adam", "q_eff")
    haar = get(rows, "random_feature", "haar_adam", "q_eff")
    checks.append(("aligned and band-limited features have q_eff near 1/2", min(aligned, band) > 0.45, f"aligned={aligned:.3f}, band={band:.3f}"))
    checks.append(("global mixing has q_eff near zero", max(abs(sketch), abs(haar)) < 0.06, f"sketch={sketch:.3f}, haar={haar:.3f}"))

    # Wide-LR oracle separation.
    g_adam = get(rows, "random_feature", "gaussian_sketch_adam", "final_risk")
    g_oracle = get(rows, "random_feature", "gaussian_sketch_spectral_oracle", "final_risk")
    h_adamw = get(rows, "random_feature", "haar_adamw", "final_risk")
    h_oracle = get(rows, "random_feature", "haar_spectral_oracle", "final_risk")
    checks.append(("spectral oracle wins after wide LR tuning", g_oracle < g_adam and h_oracle < h_adamw, f"sketch ratio={g_adam/g_oracle:.2f}, haar ratio={h_adamw/h_oracle:.2f}"))

    # AdamW schedule recovers the no-decay law.
    wd_fast = next(r for r in rows if r["experiment"] == "weight_decay" and r["setting"] == "theta=1_s=0.80")
    wd_error = abs(float(wd_fast["value"]) - float(wd_fast["predicted"]))
    checks.append(("fast AdamW decay schedule recovers no-decay exponent", wd_error < 0.01, f"error={wd_error:.4f}"))

    failed = False
    for name, passed, detail in checks:
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {name}: {detail}")
        failed |= not passed

    print(f"\n{len(checks) - int(failed) if failed else len(checks)}/{len(checks)} claim groups passed")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
