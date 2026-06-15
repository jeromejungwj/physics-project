# Intermediate Axis Theorem — Simulation

A numerical simulation of the **intermediate axis theorem** (a.k.a. the
*tennis-racquet effect* or *Dzhanibekov effect*), reproducing the physics and
key results of:

> Bubbar, F. & Zhu, L. (2025). *The Intermediate Axis Theorem: A Model for the
> Period and a Phenomenal Explanation.* Science One Programme, UBC.

When a rigid body with three distinct principal moments of inertia
(I₁ > I₂ > I₃) is spun about its **intermediate** axis, the motion is unstable
and the body periodically flips. Spinning about the largest or smallest axis is
stable. The simulation integrates the **torque-free Euler rotation equations**

```
I₁ ω̇₁ = (I₂ − I₃) ω₂ ω₃
I₂ ω̇₂ = (I₃ − I₁) ω₃ ω₁
I₃ ω̇₃ = (I₁ − I₂) ω₁ ω₂
```

with a 4th-order Runge–Kutta scheme, alongside an orientation quaternion so the
body can be drawn in 3D. Energy and |L| are conserved to ~machine precision,
which validates the integrator.

## What's here

| File | What it produces |
|------|------------------|
| `physics.py` | Core RK4 integrator (ω + orientation quaternion), conserved quantities. Run it for a conservation self-test. |
| `fig_omega_graphs.py` | ω(t) time series of the flip + a 3-panel **stable/unstable comparison** of the three axes (paper Figs. 5–7). |
| `fig_polhode.py` | The **sphere ∩ ellipsoid** state-space construction and the polhode curves (paper Figs. 1–3). |
| `fig_period_model.py` | **Precession period vs. initial speed**, fitting the inverse model `T = a/(ω₀+b)+c` to simulated data (paper Fig. 12). |
| `animate_racquet.py` | A 3D GIF of the racquet **flipping** about the intermediate axis, with the conserved L vector. |
| `run_all.py` | Generates every figure and the animation. |

The companion **interactive web version** lives in `../web/index.html`
(open it in any browser — sliders for I₁, I₂, I₃ and the initial conditions,
live 3D body, the sphere/ellipsoid state space, and a scrolling ω(t) plot).

## Run it

```bash
cd simulation
pip install -r requirements.txt
python run_all.py          # everything -> figures/
# or individually:
python physics.py          # integrator conservation self-test
python fig_omega_graphs.py
python fig_polhode.py
python fig_period_model.py
python animate_racquet.py
```

Outputs are written to `simulation/figures/`.

## Reproduced results

- **Unstable flip about r₂ only.** ω₂ periodically reverses sign while ω₁ and ω₃
  spike during each flip; rotation about r₁ and r₃ stays steady.
- **State-space geometry.** The motion follows the intersection of the |L|
  sphere and the energy ellipsoid; about the intermediate axis this curve wraps
  the whole sphere (the source of the instability).
- **Period ∝ 1/ω₀.** The flip period follows the inverse relation the paper
  fitted to racquet data, here recovered directly from the simulation.
