"""Sphere-ellipsoid construction in angular-momentum state space.

Reproduces the geometric "phenomenal explanation" of Figures 1-3 in Bubbar &
Zhu (2025).  In (L1, L2, L3) state space:

  * conservation of |L|  -> a SPHERE of radius L           (eq. 3)
  * conservation of energy -> an ELLIPSOID  L_i^2/I_i ...   (eq. 2)

The motion is confined to the intersection of the two surfaces (the polhode).
Spinning about the largest or smallest axis gives tiny closed loops near a pole
(stable).  Spinning about the intermediate axis gives separatrix curves that
wrap the entire sphere (unstable) -- this is the intermediate axis theorem.
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt

from physics import simulate, TEXTBOOK_INERTIA


def _sphere(radius, n=60):
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(0, np.pi, n)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones_like(u), np.cos(v))
    return x, y, z


def polhode_figure(I=TEXTBOOK_INERTIA, outfile="figures/sphere_ellipsoid.png"):
    I1, I2, I3 = I
    spin = 6.0
    eps = 0.25

    # Three representative initial conditions -> three polhodes.
    starts = {
        "primary $r_1$ (stable)":      ([spin, eps, eps],  "#d62728"),
        "intermediate $r_2$ (unstable)": ([eps, spin, eps], "#2ca02c"),
        "tertiary $r_3$ (stable)":     ([eps, eps, spin],  "#1f77b4"),
    }

    fig = plt.figure(figsize=(13, 6))

    # ---- Left: the construction for the intermediate-axis case ----------
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    res = simulate(I, [eps, spin, eps], t_max=10.0, dt=0.001)
    L = res["L"]
    Lmag = res["Lmag"][0]

    # |L| sphere (eq. 3)
    sx, sy, sz = _sphere(Lmag)
    ax.plot_surface(sx, sy, sz, color="#9ecae1", alpha=0.18, linewidth=0,
                    shade=True)
    # energy ellipsoid (eq. 2): semi-axes a_i = sqrt(2 K I_i)
    K = res["energy"][0]
    a = np.sqrt(2 * K * np.array(I))
    ex, ey, ez = _sphere(1.0)
    ax.plot_surface(a[0] * ex, a[1] * ey, a[2] * ez, color="#fdae6b",
                    alpha=0.20, linewidth=0)
    # the polhode (intersection traced by the actual motion)
    ax.plot(L[:, 0], L[:, 1], L[:, 2], color="#2ca02c", lw=2.5,
            label="polhode (intersection)")
    ax.set_title("Intermediate axis: intersection wraps the sphere\n"
                 "(blue = $|L|$ sphere, orange = energy ellipsoid)", fontsize=10)
    ax.set_xlabel("$L_1$"); ax.set_ylabel("$L_2$"); ax.set_zlabel("$L_3$")
    ax.legend(fontsize=8, loc="upper left")
    _equal_3d(ax, a.max())

    # ---- Right: all three polhodes on one sphere ------------------------
    # Larger perturbation so the *stable* loops are visible small ellipses
    # (not just dots) next to the unstable wrap-around curve.
    eps_vis = 1.4
    starts_vis = {
        "primary $r_1$ (stable)":        ([spin, eps_vis, eps_vis], "#d62728"),
        "intermediate $r_2$ (unstable)": ([eps_vis, spin, eps_vis], "#2ca02c"),
        "tertiary $r_3$ (stable)":       ([eps_vis, eps_vis, spin], "#1f77b4"),
    }
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    Lref = 0.0
    for label, (w0, color) in starts_vis.items():
        res = simulate(I, w0, t_max=10.0, dt=0.001)
        L = res["L"]
        Lref = max(Lref, res["Lmag"][0])
        ax2.plot(L[:, 0], L[:, 1], L[:, 2], color=color, lw=2.2, label=label)
    # faint reference sphere
    sx, sy, sz = _sphere(Lref)
    ax2.plot_surface(sx, sy, sz, color="grey", alpha=0.12, linewidth=0)
    Lmag = Lref
    ax2.set_title("Stable poles vs. unstable wrap-around polhode", fontsize=10)
    ax2.set_xlabel("$L_1$"); ax2.set_ylabel("$L_2$"); ax2.set_zlabel("$L_3$")
    ax2.legend(fontsize=8, loc="upper left")
    _equal_3d(ax2, Lmag)

    fig.suptitle("State-space construction of the Intermediate Axis Theorem "
                 "(after Bubbar & Zhu 2025, Figs. 1-3)", fontsize=12)
    fig.tight_layout()
    fig.savefig(outfile, dpi=140)
    plt.close(fig)
    print(f"wrote {outfile}")


def _equal_3d(ax, r):
    ax.set_xlim(-r, r); ax.set_ylim(-r, r); ax.set_zlim(-r, r)
    try:
        ax.set_box_aspect((1, 1, 1))
    except Exception:
        pass


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    polhode_figure()
