"""Generate the complete vector figure set for the AAAI paper.

Run from the repository root:
    python experiments/make_figures.py

Outputs are written to paper/figures/ as PDF and PNG.  Each chart is a separate
file so that the final composite can be assembled in LaTeX without rasterizing.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

plt.rcParams.update({
    "font.size": 8,
    "font.family": "serif",
    "axes.labelsize": 8,
    "xtick.labelsize": 7.2,
    "ytick.labelsize": 7.2,
    "legend.fontsize": 7.2,
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath,amssymb}",
})

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "experiments" / "key_results.csv"
OUT = ROOT / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def load_rows() -> list[dict[str, str]]:
    with DATA.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=240, bbox_inches="tight")
    plt.close(fig)


def mechanism_overview() -> None:
    fig = plt.figure(figsize=(11.8, 2.7))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def box(x: float, y: float, w: float, h: float, title: str, body: str) -> None:
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.015,rounding_size=0.018",
            linewidth=1.2,
            alpha=0.12,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h * 0.72, title, ha="center", va="center", fontsize=11, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.37, body, ha="center", va="center", fontsize=10, linespacing=1.25)

    def arrow(x1: float, y1: float, x2: float, y2: float) -> None:
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14, linewidth=1.2))

    box(
        0.02, 0.28, 0.22, 0.47,
        "What Adam/RMSProp observes",
        r"$\mathbb{E}[g_j^2\mid e]$" "\n" r"$=c_e\Sigma_{jj}+2(\Sigma e)_j^2$" "\n" r"$\asymp c_e\Sigma_{jj}$",
    )
    box(
        0.31, 0.57, 0.25, 0.31,
        "Spectrum visible",
        "Aligned or band-limited coordinates\n" r"$P\asymp(\Sigma+\rho I)^{-1/2}$" "\n" r"$q_{\rm eff}\approx1/2$",
    )
    box(
        0.31, 0.10, 0.25, 0.31,
        "Spectrum hidden",
        "Haar or global Gaussian sketch\n" r"$P\asymp cI$" "\n" r"$q_{\rm eff}\approx0$",
    )
    box(
        0.65, 0.28, 0.32, 0.47,
        "Scaling-law consequences",
        r"visible $\theta\Rightarrow q_{\rm eff}=\theta/2$" "\n" r"$\Rightarrow K_{\rho,\theta}(n)$" "\n" r"$\Rightarrow R(M,N),\ R_\star(C)$" "\n" r"$\Rightarrow$ AdamW decay schedule",
    )
    arrow(0.24, 0.53, 0.31, 0.70)
    arrow(0.24, 0.48, 0.31, 0.26)
    arrow(0.56, 0.70, 0.65, 0.58)
    arrow(0.56, 0.26, 0.65, 0.43)
    ax.text(0.5, 0.965, "Visible-spectrum mechanism", ha="center", va="top", fontsize=13, fontweight="bold")
    save(fig, "figure1_visible_spectrum_mechanism")


def visible_qeff(rows: list[dict[str, str]]) -> None:
    theta = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    q = theta / 2.0
    feature_names = ["Aligned", "Band", "Haar", "Gaussian\nsketch"]
    feature_q = np.array([0.491395868, 0.480586190, -0.024347537, -0.027817252])
    x_feature = np.array([0.05, 0.25, 0.75, 0.95])

    fig = plt.figure(figsize=(2.3, 1.65))
    ax = fig.add_axes([0.14, 0.18, 0.81, 0.75])
    ax.plot(theta, q, marker="o", label=r"Profiles")
    ax.plot(theta, theta / 2.0, linestyle="--", label=r"Theory: $\theta/2$")
    ax.scatter(x_feature, feature_q, marker="s", s=55, label="Features")
    for i, (x, y, name) in enumerate(zip(x_feature, feature_q, feature_names)):
        x_offset = -4 if i == 0 else 4 if i == 1 else 0
        ax.annotate(name, (x, y), xytext=(x_offset, 4), textcoords="offset points", ha="center", fontsize=7.2)
    ax.axhline(0.0, linewidth=0.8)
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.07, 0.62)
    ax.set_xlabel(r"Visible-profile exponent $\theta$")
    ax.set_ylabel(r"Measured $q_{\rm eff}$")
    ax.legend(
        fontsize=7.2,
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=3,
        borderaxespad=0.0,
        columnspacing=0.7,
        handlelength=1.4,
    )
    save(fig, "figure2a_qeff_visibility")


def theta_risk(rows: list[dict[str, str]]) -> None:
    settings = ["theta=0.00", "theta=0.25", "theta=0.50", "theta=0.75", "theta=1.00"]
    theta = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    risk = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "visible_profile" and r["setting"] == setting and r["metric"] == "final_risk"))
        for setting in settings
    ])
    fig = plt.figure(figsize=(2.1, 1.65))
    ax = fig.add_axes([0.16, 0.18, 0.79, 0.75])
    ax.semilogy(theta, risk, marker="o")
    ax.set_xlabel(r"Visible-profile exponent $\theta$")
    ax.set_ylabel("Tuned final excess risk")
    ax.set_xticks(theta)
    save(fig, "figure2b_theta_risk")


def oracle_separation(rows: list[dict[str, str]]) -> None:
    cases = ["Gaussian sketch", "Haar"]
    coord_risk = np.array([0.0008350359, 0.0007839851])
    oracle_risk = np.array([0.0001454145, 0.0001158156])
    coord_q = np.array([-0.0278173, -0.0230626])
    x = np.arange(len(cases))
    width = 0.34

    fig = plt.figure(figsize=(2.3, 1.65))
    ax = fig.add_axes([0.15, 0.20, 0.80, 0.72])
    b1 = ax.bar(x - width / 2, coord_risk, width, label="Coordinatewise adaptive")
    b2 = ax.bar(x + width / 2, oracle_risk, width, label="Spectral oracle")
    ax.set_yscale("log")
    ax.set_xticks(x, cases)
    ax.set_ylabel("Tuned final excess risk")
    ax.legend(fontsize=7.2)
    for i, bar in enumerate(b1):
        ax.annotate(rf"$q_{{\rm eff}}={coord_q[i]:.3f}$", (bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=7.2)
    for bar in b2:
        ax.annotate(r"$q_{\rm eff}=0.5$", (bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=7.2)
    save(fig, "figure2c_hidden_spectrum_oracle")


def compute_phase(rows: list[dict[str, str]]) -> None:
    theta_dense = np.linspace(0, 1, 201)

    def beta(a: float, b: float, theta: np.ndarray) -> np.ndarray:
        alpha = a * (1.0 - theta / 2.0)
        return (b - 1.0) / (np.maximum(alpha, b) + 1.0)

    rr = sorted(
        [r for r in rows if r["experiment"] == "compute_hard" and r["metric"] == "risk_exponent"],
        key=lambda r: float(r["setting"].split("=")[1]),
    )
    theta_obs = np.array([float(r["setting"].split("=")[1]) for r in rr])
    obs = np.array([float(r["value"]) for r in rr])

    fig = plt.figure(figsize=(2.3, 1.65))
    ax = fig.add_axes([0.16, 0.18, 0.79, 0.75])
    ax.plot(theta_dense, beta(3.0, 1.4, theta_dense), label=r"Theory: $(a,b)=(3,1.4)$")
    ax.scatter(theta_obs, obs, marker="o", label="Observed hard-source sweep")
    ax.plot(theta_dense, beta(1.5, 1.4, theta_dense), linestyle="--", label=r"Theory: $(a,b)=(1.5,1.4)$")
    ax.set_xlabel(r"Visible-profile exponent $\theta$")
    ax.set_ylabel("Positive compute-risk exponent")
    ax.set_xlim(0, 1)
    ax.legend(fontsize=7.2)
    save(fig, "figure3a_compute_phase_transition")


def allocation_exponents() -> None:
    theta = np.linspace(0, 1, 201)
    alpha = 3.0 * (1.0 - theta / 2.0)
    m = np.maximum(alpha, 1.4)
    m_exp = 1.0 / (m + 1.0)
    n_exp = m / (m + 1.0)
    fig = plt.figure(figsize=(2.3, 1.65))
    ax = fig.add_axes([0.16, 0.18, 0.79, 0.75])
    ax.plot(theta, m_exp, label=r"$M_\star$ exponent")
    ax.plot(theta, n_exp, label=r"$N_\star$ exponent")
    ax.plot(theta, m_exp, linestyle="--", label=r"$K_\star$ exponent")
    ax.set_xlabel(r"Visible-profile exponent $\theta$")
    ax.set_ylabel("Compute allocation exponent")
    ax.set_xlim(0, 1)
    ax.legend(fontsize=7.2)
    save(fig, "figure3b_allocation_exponents")


def adamw_schedule(rows: list[dict[str, str]]) -> None:
    settings = ["theta=1_s=0.00", "theta=1_s=0.05", "theta=1_s=0.10", "theta=1_s=0.20", "theta=1_s=0.40", "theta=1_s=0.80"]
    s = np.array([0.0, 0.05, 0.10, 0.20, 0.40, 0.80])
    obs = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "weight_decay" and r["setting"] == setting and r["metric"] == "risk_exponent"))
        for setting in settings
    ])
    pred = np.array([
        float(next(r["predicted"] for r in rows if r["experiment"] == "weight_decay" and r["setting"] == setting and r["metric"] == "risk_exponent"))
        for setting in settings
    ])
    fig = plt.figure(figsize=(2.3, 1.65))
    ax = fig.add_axes([0.16, 0.18, 0.79, 0.75])
    ax.plot(s, obs, marker="o", label="Observed")
    ax.plot(s, pred, marker="x", linestyle="--", label="Predicted")
    ax.axvline(0.6, linestyle=":", label=r"Threshold $s_\star=0.6$")
    ax.set_xlabel(r"Weight-decay schedule exponent $s$")
    ax.set_ylabel("Positive compute-risk exponent")
    ax.legend(fontsize=7.2)
    save(fig, "figure3c_adamw_schedule")


def main() -> None:
    rows = load_rows()
    mechanism_overview()
    visible_qeff(rows)
    theta_risk(rows)
    oracle_separation(rows)
    compute_phase(rows)
    allocation_exponents()
    adamw_schedule(rows)
    print(f"Wrote figure PDFs and PNGs to {OUT}")


if __name__ == "__main__":
    main()
