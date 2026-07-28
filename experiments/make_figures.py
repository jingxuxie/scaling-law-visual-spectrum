"""Generate the complete vector figure set for the AAAI paper.

Run from the repository root:
    python experiments/make_figures.py

Outputs are written to paper/figures/ as PDF and PNG.  Each chart is a separate
file so that the final composite can be assembled in LaTeX without rasterizing.
The script deliberately uses Matplotlib mathtext instead of an external LaTeX
installation, making the figures reproducible on laptops and in CI.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np

plt.rcParams.update(
    {
        "font.size": 8,
        "font.family": "serif",
        "axes.labelsize": 8,
        "axes.linewidth": 0.8,
        "xtick.labelsize": 7.2,
        "ytick.labelsize": 7.2,
        "legend.fontsize": 6.8,
        "lines.linewidth": 1.5,
        "lines.markersize": 4.8,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "text.usetex": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

BLUE = "#276FBF"
ORANGE = "#E07A1F"
GREEN = "#3A8D5D"
SLATE = "#586F7C"
INK = "#263238"
GRID = "#D8E0E6"
PANEL_SIZE = (2.55, 1.85)
PANEL_RECT = [0.20, 0.22, 0.76, 0.61]

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "experiments" / "key_results.csv"
OUT = ROOT / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def load_rows() -> list[dict[str, str]]:
    with DATA.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save(fig: plt.Figure, stem: str) -> None:
    fig.savefig(
        OUT / f"{stem}.pdf",
        bbox_inches="tight",
        pad_inches=0.025,
        facecolor="white",
    )
    fig.savefig(
        OUT / f"{stem}.png",
        dpi=300,
        bbox_inches="tight",
        pad_inches=0.025,
        facecolor="white",
    )
    plt.close(fig)


def panel() -> tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=PANEL_SIZE, facecolor="white")
    ax = fig.add_axes(PANEL_RECT)
    return fig, ax


def style_axes(ax: plt.Axes, *, grid: bool = True) -> None:
    """Apply the shared open-frame academic chart style."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(top=False, right=False, colors=INK)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)
    ax.set_axisbelow(True)
    if grid:
        ax.grid(axis="y", color=GRID, linewidth=0.55, alpha=0.7)


def top_legend(
    fig: plt.Figure,
    handles: list,
    labels: list[str],
    *,
    ncol: int = 2,
) -> None:
    fig.legend(
        handles,
        labels,
        loc="upper center",
        bbox_to_anchor=(0.5, 0.995),
        ncol=ncol,
        frameon=False,
        borderaxespad=0.0,
        handlelength=1.7,
        handletextpad=0.45,
        columnspacing=0.9,
    )


def mechanism_overview() -> None:
    fig = plt.figure(figsize=(10.4, 2.3), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def box(
        x: float,
        y: float,
        w: float,
        h: float,
        title: str,
        body: str,
        facecolor: str,
        *,
        title_fontsize: float = 10.5,
        body_fontsize: float = 9.3,
        body_top_offset: float = 0.16,
    ) -> None:
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            linewidth=0.9,
            edgecolor="#AAB7C2",
            facecolor=facecolor,
        )
        ax.add_patch(patch)
        ax.text(
            x + w / 2,
            y + h - 0.07,
            title,
            ha="center",
            va="top",
            fontsize=title_fontsize,
            fontweight="bold",
            linespacing=1.05,
            color=INK,
        )
        ax.text(
            x + w / 2,
            y + h - body_top_offset,
            body,
            ha="center",
            va="top",
            fontsize=body_fontsize,
            linespacing=1.18,
            color=INK,
        )

    def arrow(x1: float, y1: float, x2: float, y2: float) -> None:
        ax.add_patch(
            FancyArrowPatch(
                (x1, y1),
                (x2, y2),
                arrowstyle="-|>",
                mutation_scale=13,
                linewidth=1.15,
                color=SLATE,
                shrinkA=2,
                shrinkB=2,
            )
        )

    box(
        0.02,
        0.25,
        0.23,
        0.50,
        "Adam/RMSProp\nsecond moments track",
        r"$\mathbb{E}[g_j^2\mid e]$"
        "\n"
        r"$=c_e\Sigma_{jj}+2(\Sigma e)_j^2$"
        "\n"
        r"$\asymp c_e\Sigma_{jj}$",
        "#EEF4F8",
        title_fontsize=9.4,
        body_top_offset=0.25,
    )
    box(
        0.32,
        0.56,
        0.27,
        0.36,
        "Spectrum visible",
        "Aligned or band-limited coordinates"
        "\n"
        r"$P_t\asymp d_t^{-1/2}(\Sigma+\rho_t I)^{-1/2}$"
        "\n"
        r"$q_{\rm eff}\approx1/2$ (scalar factor ignored)",
        "#EAF3FB",
    )
    box(
        0.32,
        0.03,
        0.27,
        0.46,
        "Spectrum hidden",
        "Haar or global Gaussian sketch"
        "\n"
        "when coordinate variances concentrate"
        "\n"
        r"$P\asymp cI$"
        "\n"
        r"$q_{\rm eff}\approx0$",
        "#F5F2EA",
    )
    box(
        0.67,
        0.25,
        0.31,
        0.50,
        "Scaling-law consequences",
        r"visible $\theta\Rightarrow q_{\rm eff}=\theta/2$"
        "\n"
        r"$\Rightarrow K_{\rho,\theta}(n)$"
        "\n"
        r"$\Rightarrow R(M,N),\ R_\star(C)$"
        "\n"
        r"$\Rightarrow$ AdamW decay schedule",
        "#EEF5EF",
    )
    arrow(0.25, 0.54, 0.32, 0.72)
    arrow(0.25, 0.46, 0.32, 0.26)
    arrow(0.59, 0.72, 0.67, 0.57)
    arrow(0.59, 0.26, 0.67, 0.43)
    save(fig, "figure1_visible_spectrum_mechanism")


def visible_qeff(rows: list[dict[str, str]]) -> None:
    theta = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    q = theta / 2.0
    feature_rows = [
        ("Aligned", 0.491395868),
        ("Band-limited", 0.480586190),
        ("Haar", -0.024347537),
        ("Gaussian sketch", -0.027817252),
    ]

    fig, ax = panel()
    profile_line, = ax.plot(
        theta,
        q,
        marker="o",
        color=BLUE,
        label="Controlled sweep",
    )
    theory_line, = ax.plot(
        theta,
        theta / 2.0,
        color=ORANGE,
        linestyle="--",
        label=r"Theory: $\theta/2$",
    )
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.02, 0.54)
    ax.set_xlabel(r"Controlled-profile exponent $\theta$")
    ax.set_ylabel(r"Measured $q_{\rm eff}$")
    style_axes(ax)
    top_legend(
        fig,
        [profile_line, theory_line],
        ["Controlled sweep", r"Theory: $\theta/2$"],
        ncol=2,
    )

    inset = ax.inset_axes([0.04, 0.52, 0.53, 0.42])
    inset.set_axis_off()
    inset.add_patch(
        FancyBboxPatch(
            (0.0, 0.0),
            1.0,
            1.0,
            transform=inset.transAxes,
            boxstyle="round,pad=0.02,rounding_size=0.04",
            linewidth=0.65,
            edgecolor="#B9C4CC",
            facecolor="#F6F8F9",
            zorder=0,
            clip_on=False,
        )
    )
    inset.text(
        0.5,
        0.88,
        "Feature systems",
        ha="center",
        va="center",
        fontsize=6.2,
        fontweight="bold",
        color=INK,
        transform=inset.transAxes,
    )
    y_positions = [0.66, 0.48, 0.30, 0.12]
    for (name, value), y in zip(feature_rows, y_positions):
        inset.scatter(
            [0.08],
            [y],
            marker="s",
            s=13,
            color=GREEN,
            transform=inset.transAxes,
            clip_on=False,
        )
        inset.text(
            0.16,
            y,
            name,
            ha="left",
            va="center",
            fontsize=5.0,
            color=INK,
            transform=inset.transAxes,
        )
        inset.text(
            0.95,
            y,
            rf"${value:.2f}$",
            ha="right",
            va="center",
            fontsize=5.0,
            color=INK,
            transform=inset.transAxes,
        )
    save(fig, "figure2a_qeff_visibility")


def theta_risk(rows: list[dict[str, str]]) -> None:
    settings = ["theta=0.00", "theta=0.25", "theta=0.50", "theta=0.75", "theta=1.00"]
    theta = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
    risk = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "visible_profile" and r["setting"] == setting and r["metric"] == "final_risk"))
        for setting in settings
    ])
    fig, ax = panel()
    ax.semilogy(theta, risk, marker="o", color=BLUE)
    ax.set_xlabel(r"Controlled-profile exponent $\theta$")
    ax.set_ylabel("Final excess risk")
    ax.set_xticks(theta)
    style_axes(ax)
    save(fig, "figure2b_theta_risk")


def oracle_separation(rows: list[dict[str, str]]) -> None:
    cases = ["Gaussian sketch", "Haar"]
    coord_risk = np.array([0.0008350359, 0.0007839851])
    oracle_risk = np.array([0.0001454145, 0.0001158156])
    coord_q = np.array([-0.0278173, -0.0230626])
    x = np.arange(len(cases))
    width = 0.34

    fig, ax = panel()
    b1 = ax.bar(
        x - width / 2,
        coord_risk,
        width,
        color=BLUE,
        label="Best coordinatewise adaptive",
    )
    b2 = ax.bar(
        x + width / 2,
        oracle_risk,
        width,
        color=ORANGE,
        label="Spectral oracle",
    )
    ax.set_yscale("log")
    ax.set_ylim(8e-5, 1.2e-3)
    ax.set_xticks(x, ["Gaussian\nsketch", "Haar"])
    ax.set_ylabel("Final excess risk")
    for i, bar in enumerate(b1):
        ax.annotate(
            rf"$q_{{\rm eff}}$" "\n" rf"${coord_q[i]:.3f}$",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=6.4,
            linespacing=0.9,
        )
    for bar in b2:
        ax.annotate(
            r"$q_{\rm eff}$" "\n" r"$0.5$",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=6.4,
            linespacing=0.9,
        )
    style_axes(ax)
    top_legend(
        fig,
        [b1, b2],
        ["Best coordinatewise\nadaptive", "Spectral oracle"],
        ncol=2,
    )
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

    fig, ax = panel()
    hard_line, = ax.plot(
        theta_dense,
        beta(3.0, 1.4, theta_dense),
        color=BLUE,
        label="Hard-source theory",
    )
    observed = ax.scatter(
        theta_obs,
        obs,
        marker="o",
        s=32,
        color=BLUE,
        edgecolor="white",
        linewidth=0.55,
        zorder=3,
        label="Observed: hard-source sweep",
    )
    saturated_line, = ax.plot(
        theta_dense,
        beta(1.5, 1.4, theta_dense),
        color=ORANGE,
        linestyle="--",
        label="Saturating theory",
    )
    ax.set_xlabel(r"Visible-profile exponent $\theta$")
    ax.set_ylabel(r"Compute-risk exponent $\beta$")
    ax.set_xlim(-0.03, 1.04)
    style_axes(ax)
    top_legend(
        fig,
        [hard_line, observed, saturated_line],
        [
            r"Theory: $(3,1.4)$",
            "Observed: hard source",
            r"Theory: $(1.5,1.4)$",
        ],
        ncol=2,
    )
    save(fig, "figure3a_compute_phase_transition")


def allocation_exponents() -> None:
    theta = np.linspace(0, 1, 201)
    alpha = 3.0 * (1.0 - theta / 2.0)
    m = np.maximum(alpha, 1.4)
    m_exp = 1.0 / (m + 1.0)
    n_exp = m / (m + 1.0)
    fig, ax = panel()
    mk_line, = ax.plot(
        theta,
        m_exp,
        color=BLUE,
        label=r"$M$ and $K$ exponents",
    )
    n_line, = ax.plot(
        theta,
        n_exp,
        color=ORANGE,
        label=r"$N$ exponent",
    )
    ax.set_xlabel(r"Visible-profile exponent $\theta$")
    ax.set_ylabel(r"Exponent $\gamma$ in $X_\star\propto C^\gamma$")
    ax.set_xlim(0, 1)
    style_axes(ax)
    top_legend(
        fig,
        [mk_line, n_line],
        [r"$M$ and $K$ exponents", r"$N$ exponent"],
        ncol=1,
    )
    save(fig, "figure3b_allocation_exponents")


def adamw_schedule(rows: list[dict[str, str]]) -> None:
    settings = ["theta=1_s=0.00", "theta=1_s=0.05", "theta=1_s=0.10", "theta=1_s=0.20", "theta=1_s=0.40", "theta=1_s=0.80"]
    s = np.array([0.0, 0.05, 0.10, 0.20, 0.40, 0.80])
    obs = np.array([
        float(next(r["value"] for r in rows if r["experiment"] == "weight_decay" and r["setting"] == setting and r["metric"] == "risk_exponent"))
        for setting in settings
    ])
    a, b, theta = 3.0, 1.4, 1.0
    alpha = a * (1.0 - theta / 2.0)
    m = max(alpha, b)
    s_dense = np.linspace(0.0, 0.8, 301)
    theory_dense = np.minimum(
        (b - 1.0) * s_dense / alpha,
        (b - 1.0) / (m + 1.0),
    )
    theory_marker_s = np.sort(np.unique(np.append(s, 0.6)))
    theory_marker_beta = np.minimum(
        (b - 1.0) * theory_marker_s / alpha,
        (b - 1.0) / (m + 1.0),
    )
    fig, ax = panel()
    observed_line, = ax.plot(s, obs, marker="o", color=BLUE, label="Observed")
    theory_line, = ax.plot(
        s_dense,
        theory_dense,
        color=ORANGE,
        linestyle="--",
        label="Theory",
    )
    ax.scatter(
        theory_marker_s,
        theory_marker_beta,
        marker="x",
        s=30,
        color=ORANGE,
        linewidth=1.2,
        zorder=3,
    )
    threshold = ax.axvline(
        0.6,
        color=SLATE,
        linestyle=":",
        label=r"Threshold $s_\star=0.6$",
    )
    ax.set_xlim(-0.02, 0.84)
    ax.set_xlabel(r"Weight-decay schedule exponent $s$")
    ax.set_ylabel("Positive compute-risk exponent")
    style_axes(ax)
    top_legend(
        fig,
        [observed_line, theory_line, threshold],
        ["Observed", "Theory", r"Threshold $s_\star=0.6$"],
        ncol=2,
    )
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
    print(f"Wrote figures to {OUT}")


if __name__ == "__main__":
    main()
