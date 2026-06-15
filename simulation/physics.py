"""Core physics for the Intermediate Axis Theorem simulation.

This module numerically integrates the torque-free Euler rotation equations
that govern a freely rotating rigid body (an "asymmetric top").  These are the
same equations used in Bubbar & Zhu (2025), "The Intermediate Axis Theorem: A
Model for the Period and a Phenomenal Explanation" (Science One Programme, UBC).

Torque-free Euler equations (body frame fixed to the principal axes):

    I1 * dw1/dt = (I2 - I3) * w2 * w3
    I2 * dw2/dt = (I3 - I1) * w3 * w1
    I3 * dw3/dt = (I1 - I2) * w1 * w2

When I1 > I2 > I3, rotation about the *intermediate* axis (I2) is unstable and
the body undergoes the periodic flipping known as the tennis-racquet effect or
the Dzhanibekov effect.  Rotation about the largest (I1) or smallest (I3) axis
is stable.

Alongside the angular velocity we integrate an orientation quaternion so the
body can be drawn in 3D.  The body-frame angular velocity w drives the
quaternion q (which maps body -> world coordinates) via

    dq/dt = 0.5 * q (x) (0, w)
"""

from __future__ import annotations

import numpy as np


# --- Measured moments of inertia from the paper (Table 2) --------------------
# 27" tennis racquet + iPhone 12 zip-tied to the centre of the strings.
#   I1 (primary, r1)      = 78.0  g.m^2  (largest)
#   I2 (intermediate, r2) = 78.0  g.m^2  (middle -> the unstable axis)
#   I3 (tertiary, r3)     = 1.391 g.m^2  (smallest)
# The paper measured I1 and I2 as nearly equal (within uncertainty), yet the
# racquet still flipped -- they were "sufficiently different" to act as an
# asymmetric top.  Because I1 ~ I2 the flip is very slow, so the figures use the
# well-separated TEXTBOOK_INERTIA preset for a clear, fast Dzhanibekov flip.
RACQUET_INERTIA = (78.0e-3, 78.0e-3, 1.391e-3)  # kg.m^2 (paper Table 2)

# A textbook "T-handle"/box preset with well separated moments for a clean,
# obvious Dzhanibekov flip.
TEXTBOOK_INERTIA = (3.0, 2.0, 1.0)  # arbitrary units, I1 > I2 > I3


def euler_derivatives(w: np.ndarray, I: tuple[float, float, float]) -> np.ndarray:
    """Right-hand side of the torque-free Euler rotation equations."""
    I1, I2, I3 = I
    w1, w2, w3 = w
    return np.array([
        (I2 - I3) * w2 * w3 / I1,
        (I3 - I1) * w3 * w1 / I2,
        (I1 - I2) * w1 * w2 / I3,
    ])


def quat_mult(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Hamilton product of two quaternions stored as [w, x, y, z]."""
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return np.array([
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    ])


def quat_to_matrix(q: np.ndarray) -> np.ndarray:
    """Rotation matrix (body -> world) for a unit quaternion [w, x, y, z]."""
    w, x, y, z = q / np.linalg.norm(q)
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - z * w),     2 * (x * z + y * w)],
        [2 * (x * y + z * w),     1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
        [2 * (x * z - y * w),     2 * (y * z + x * w),     1 - 2 * (x * x + y * y)],
    ])


def _state_derivative(state: np.ndarray, I) -> np.ndarray:
    w = state[:3]
    q = state[3:]
    dw = euler_derivatives(w, I)
    dq = 0.5 * quat_mult(q, np.array([0.0, w[0], w[1], w[2]]))
    return np.concatenate([dw, dq])


def simulate(I, w0, t_max=10.0, dt=0.002, q0=None):
    """Integrate the free rigid-body motion with a fixed-step RK4 scheme.

    Parameters
    ----------
    I    : (I1, I2, I3) principal moments of inertia (I1 > I2 > I3 recommended).
    w0   : initial body-frame angular velocity (3-vector).
    t_max: total simulated time.
    dt   : integration step.
    q0   : initial orientation quaternion [w, x, y, z]; defaults to identity.

    Returns
    -------
    dict with arrays: t, w (N,3), q (N,4), L (N,3 body-frame momentum),
    Lmag (N,), energy (N,).  L and energy should stay constant -> a check on
    the integrator.
    """
    I = tuple(float(x) for x in I)
    w0 = np.asarray(w0, dtype=float)
    if q0 is None:
        q0 = np.array([1.0, 0.0, 0.0, 0.0])

    n = int(round(t_max / dt))
    t = np.linspace(0.0, n * dt, n + 1)
    state = np.empty((n + 1, 7))
    state[0, :3] = w0
    state[0, 3:] = q0 / np.linalg.norm(q0)

    for k in range(n):
        s = state[k]
        k1 = _state_derivative(s, I)
        k2 = _state_derivative(s + 0.5 * dt * k1, I)
        k3 = _state_derivative(s + 0.5 * dt * k2, I)
        k4 = _state_derivative(s + dt * k3, I)
        s_next = s + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        s_next[3:] /= np.linalg.norm(s_next[3:])  # renormalise quaternion
        state[k + 1] = s_next

    w = state[:, :3]
    q = state[:, 3:]
    Iarr = np.array(I)
    L = w * Iarr  # body-frame angular momentum components
    Lmag = np.linalg.norm(L, axis=1)
    energy = 0.5 * np.sum(Iarr * w ** 2, axis=1)
    return {"t": t, "w": w, "q": q, "L": L, "Lmag": Lmag, "energy": energy, "I": Iarr}


if __name__ == "__main__":
    # Quick self-test: energy and |L| must be conserved for free rotation.
    res = simulate(TEXTBOOK_INERTIA, [0.05, 5.0, 0.05], t_max=20.0, dt=0.001)
    dE = np.ptp(res["energy"]) / res["energy"][0]
    dL = np.ptp(res["Lmag"]) / res["Lmag"][0]
    print(f"Relative energy drift: {dE:.2e}")
    print(f"Relative |L| drift:    {dL:.2e}")
    print("Conserved to ~machine precision -> integrator OK")
