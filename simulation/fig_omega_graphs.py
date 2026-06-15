"""Angular-velocity time series and three-axis stability comparison.

The first figure plots the body-frame angular-velocity components over time, in
the style of the omega-t gyroscope data in Bubbar & Zhu (2025) (their Fig. 5;
the periodic sign reversal of the off-axis components is the "reversed axes"
behaviour they note around Fig. 7).  Rotation started near the intermediate
axis shows the characteristic periodic flipping: omega_2 holds roughly steady
while omega_1 and omega_3 spike and reverse sign.

The second figure is an additional pedagogical comparison (not a specific paper
figure) contrasting rotation started about each of the three principal axes --
only the intermediate axis is unstable.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from physics import simulate, TEXTBOOK_INERTIA


def omega_time_series(I=TEXTBOOK_INERTIA, outfile="figures/omega_intermediate.png"):
    """Unstable flipping when spun about the intermediate axis (Fig. 5 style)."""
    w0 = [0.08, 6.0, 0.0]  # mostly about r2 with a tiny perturbation
    res = simulate(I, w0, t_max=12.0, dt=0.001)
    t, w = res["t"], res["w"]

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.plot(t, w[:, 0], label=r"$\omega_1$ (primary, $I_1$)", color="#d62728")
    ax.plot(t, w[:, 1], label=r"$\omega_2$ (intermediate, $I_2$)", color="#2ca02c", lw=2.2)
    ax.plot(t, w[:, 2], label=r"$\omega_3$ (tertiary, $I_3$)", color="#1f77b4")
    ax.plot(t, np.linalg.norm(w, axis=1), label=r"$|\boldsymbol{\omega}|$",
            color="black", lw=1, ls="--", alpha=0.7)
    ax.axhline(0, color="grey", lw=0.6)
    ax.set_xlabel("time  $t$  (s)")
    ax.set_ylabel(r"angular velocity  (rad s$^{-1}$)")
    ax.set_title("Intermediate-axis rotation: the unstable flip "
                 "(tennis-racquet / Dzhanibekov effect)")
    ax.legend(loc="upper right", ncol=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(outfile, dpi=140)
    plt.close(fig)
    print(f"wrote {outfile}")


def three_axis_comparison(I=TEXTBOOK_INERTIA, outfile="figures/three_axis_comparison.png"):
    """Stable about r1 and r3, unstable about r2 (the heart of the theorem)."""
    eps = 0.08          # small perturbation onto the other two axes
    spin = 6.0
    cases = [
        ("Primary axis $r_1$ (largest $I$)  -- STABLE",
         [spin, eps, eps]),
        ("Intermediate axis $r_2$  -- UNSTABLE",
         [eps, spin, eps]),
        ("Tertiary axis $r_3$ (smallest $I$)  -- STABLE",
         [eps, eps, spin]),
    ]

    fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
    colors = ["#d62728", "#2ca02c", "#1f77b4"]
    labels = [r"$\omega_1$", r"$\omega_2$", r"$\omega_3$"]
    for ax, (title, w0) in zip(axes, cases):
        res = simulate(I, w0, t_max=14.0, dt=0.001)
        for j in range(3):
            ax.plot(res["t"], res["w"][:, j], color=colors[j], label=labels[j],
                    lw=2.0 if "UNSTABLE" in title else 1.6)
        ax.axhline(0, color="grey", lw=0.6)
        ax.set_title(title, fontsize=11)
        ax.set_ylabel(r"$\omega$ (rad/s)")
        ax.legend(loc="upper right", ncol=3, fontsize=9)
    axes[-1].set_xlabel("time  $t$  (s)")
    fig.suptitle("Only the intermediate axis is unstable "
                 r"($I_1 > I_2 > I_3$)", y=1.0, fontsize=13)
    fig.tight_layout()
    fig.savefig(outfile, dpi=140)
    plt.close(fig)
    print(f"wrote {outfile}")


if __name__ == "__main__":
    import os
    os.makedirs("figures", exist_ok=True)
    omega_time_series()
    three_axis_comparison()
