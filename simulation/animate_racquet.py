"""3D animation of the tumbling asymmetric top (the visible flip itself).

Integrates the free rigid-body motion and renders a racquet-shaped object whose
orientation follows the integrated quaternion.  When launched near the
intermediate axis the object performs the periodic 180-degree flips that define
the tennis-racquet / Dzhanibekov effect.  The conserved angular-momentum vector
L is drawn in the world frame to show that the *body* flips while L stays fixed.

Saves an animated GIF (no ffmpeg required).
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from physics import simulate, quat_to_matrix, TEXTBOOK_INERTIA


def racquet_geometry():
    """Return (vertices, faces) of a simple racquet: a flat head + a handle.

    Body axes are arranged so that:
      x = r1 (primary,  largest I) -- across the head, in the face plane
      y = r2 (intermediate)        -- perpendicular to the face (flip axis)
      z = r3 (tertiary, smallest I)-- along the handle
    """
    hw, hl, ht = 0.9, 1.2, 0.06   # head half-width, half-length, half-thickness
    handle_w, handle_t = 0.18, 0.10
    handle_len = 1.3

    def box(cx, cy, cz, sx, sy, sz):
        v = np.array([
            [cx - sx, cy - sy, cz - sz], [cx + sx, cy - sy, cz - sz],
            [cx + sx, cy + sy, cz - sz], [cx - sx, cy + sy, cz - sz],
            [cx - sx, cy - sy, cz + sz], [cx + sx, cy - sy, cz + sz],
            [cx + sx, cy + sy, cz + sz], [cx - sx, cy + sy, cz + sz],
        ])
        f = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
             [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4]]
        return v, f

    # head centred a bit up the +z axis, handle below it
    hv, hf = box(0, 0, ht + handle_len, hw, ht, hl)   # head: wide in x, thin in y
    gv, gf = box(0, 0, 0.0, handle_w, handle_t, handle_len)  # handle along z

    verts = np.vstack([hv, gv])
    faces = hf + [[i + len(hv) for i in face] for face in gf]
    return verts, faces


def animate(I=TEXTBOOK_INERTIA, w0=(0.06, 6.0, 0.0), t_max=12.0,
            outfile="figures/racquet_flip.gif", n_frames=180):
    res = simulate(I, w0, t_max=t_max, dt=0.002)
    q = res["q"]
    # world-frame L (constant): R(0) @ L_body(0)
    L0_world = quat_to_matrix(q[0]) @ res["L"][0]
    L0_world = L0_world / np.linalg.norm(L0_world) * 2.6

    step = max(1, len(q) // n_frames)
    frames = range(0, len(q), step)

    verts, faces = racquet_geometry()

    fig = plt.figure(figsize=(6.5, 6.5))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_box_aspect((1, 1, 1))
    lim = 2.6

    def draw(idx):
        ax.clear()
        R = quat_to_matrix(q[idx])
        vw = verts @ R.T
        polys = [[vw[i] for i in face] for face in faces]
        head = Poly3DCollection(polys[:6], facecolor="#2ca02c",
                                edgecolor="k", alpha=0.9, linewidths=0.5)
        handle = Poly3DCollection(polys[6:], facecolor="#8c564b",
                                  edgecolor="k", alpha=0.95, linewidths=0.5)
        ax.add_collection3d(head)
        ax.add_collection3d(handle)
        # fixed angular-momentum vector in the world frame
        ax.quiver(0, 0, 0, *L0_world, color="#d62728", lw=2.5,
                  arrow_length_ratio=0.12)
        ax.text(*L0_world * 1.05, "L (conserved)", color="#d62728", fontsize=9)
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
        ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z")
        ax.set_title(f"Dzhanibekov flip about the intermediate axis\n"
                     f"t = {res['t'][idx]:5.2f} s", fontsize=11)
        return ax,

    anim = FuncAnimation(fig, draw, frames=frames, interval=50, blit=False)
    writer = PillowWriter(fps=20)
    anim.save(outfile, writer=writer)
    plt.close(fig)
    print(f"wrote {outfile}")


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    animate()
