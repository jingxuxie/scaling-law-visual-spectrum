"""Generate the three compact figures used by the AAAI paper.

Run from the repository root:
    python experiments/make_figures.py

Outputs are written to paper/figures/ as both PDF and PNG.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "experiments" / "key_results.csv"
OUT = ROOT / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def load_rows() -> list[dict[str, str]]:
    with DATA.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(fig: plt.Figure, stem: str) -> None:
    fig.tight_layout()
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def visible_profile(rows: list[dict[str, str]]) -> None:
    settings = ["theta=0.00", "theta=0.25", "theta=0.50", "theta=0.75", "theta=1.00"]
    theta = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    risk = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "visible_profile" and r["setting"] == s and r["metric"] == "final_risk"))
        for s in settings
    ])
    q = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "visible_profile" and r["setting"] == s and r["metric"] == "q_eff"))
        for s in settings
    ])

    fig = plt.figure(figsize=(6.5, 2.7))
    ax = fig.add_subplot(111)
    ax.semilogy(theta, risk, marker="o", label="Tuned final risk")
    ax.set_xlabel(r"Visible-profile exponent $\theta$")
    ax.set_ylabel("Excess risk")
    ax2 = ax.twinx()
    ax2.plot(theta, q, marker="s", label=r"Measured $q_{\rm eff}$")
    ax2.plot(theta, theta / 2.0, linestyle="--", label=r"Prediction $\theta/2$")
    ax2.set_ylabel(r"$q_{\rm eff}$")
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(handles1 + handles2, labels1 + labels2, loc="best", fontsize=8)
    save(fig, "visible_profile")


def compute_exponents(rows: list[dict[str, str]]) -> None:
    rr = sorted(
        [r for r in rows if r["experiment"] == "compute_hard" and r["metric"] == "risk_exponent"],
        key=lambda r: float(r["setting"].split("=")[1]),
    )
    theta = np.array([float(r["setting"].split("=")[1]) for r in rr])
    obs = np.array([float(r["value"]) for r in rr])
    pred = np.array([float(r["predicted"]) for r in rr])

    fig = plt.figure(figsize=(4.2, 2.8))
    ax = fig.add_subplot(111)
    ax.plot(theta, obs, marker="o", label="Observed")
    ax.plot(theta, pred, marker="x", linestyle="--", label="Predicted")
    ax.set_xlabel(r"Visible-profile exponent $\theta$")
    ax.set_ylabel("Positive compute-risk exponent")
    ax.legend(fontsize=8)
    save(fig, "compute_exponent")


def random_feature(rows: list[dict[str, str]]) -> None:
    cases = ["Gaussian sketch", "Haar"]
    coord_settings = ["gaussian_sketch_adam", "haar_adamw"]
    oracle_settings = ["gaussian_sketch_spectral_oracle", "haar_spectral_oracle"]
    coord_risk = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "random_feature" and r["setting"] == s and r["metric"] == "final_risk"))
        for s in coord_settings
    ])
    oracle_risk = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "random_feature" and r["setting"] == s and r["metric"] == "final_risk"))
        for s in oracle_settings
    ])
    coord_q = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "random_feature" and r["setting"] in {"gaussian_sketch_adam", "haar_adam"} and r["metric"] == "q_eff"))
        for _ in [0]
    ])
    # Explicit values keep the optimizer choice in the risk panel independent of the q diagnostic.
    q_values = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "random_feature" and r["setting"] == "gaussian_sketch_adam" and r["metric"] == "q_eff")),
        float(next(r["value"] for r in rows if r["experiment"] == "random_feature" and r["setting"] == "haar_adam" and r["metric"] == "q_eff")),
    ])

    fig = plt.figure(figsize=(6.6, 2.7))
    ax1 = fig.add_subplot(121)
    x = np.arange(len(cases))
    width = 0.36
    ax1.bar(x - width / 2, coord_risk, width, label="Coordinatewise adaptive")
    ax1.bar(x + width / 2, oracle_risk, width, label="Spectral oracle")
    ax1.set_yscale("log")
    ax1.set_xticks(x, cases)
    ax1.set_ylabel("Tuned final risk")
    ax1.legend(fontsize=7)

    ax2 = fig.add_subplot(122)
    ax2.bar(x - width / 2, q_values, width, label="Coordinatewise")
    ax2.bar(x + width / 2, np.full(2, 0.5), width, label="Spectral oracle")
    ax2.axhline(0.0, linewidth=0.8)
    ax2.set_xticks(x, cases)
    ax2.set_ylabel(r"$q_{\rm eff}$")
    ax2.set_ylim(-0.08, 0.56)
    ax2.legend(fontsize=7)
    save(fig, "random_feature_oracle_separation")


def main() -> None:
    rows = load_rows()
    visible_profile(rows)
    compute_exponents(rows)
    random_feature(rows)
    print(f"Wrote figures to {OUT}")


if __name__ == "__main__":
    main()
