# physics-project

Course project (수행평가).

## Intermediate Axis Theorem simulation

A simulation of the **intermediate axis theorem** (the *tennis-racquet* /
*Dzhanibekov effect*) — the unstable flipping that occurs when an asymmetric
rigid body is spun about its intermediate principal axis. It reproduces the
physics and key results of Bubbar & Zhu (2025).

- **Python** (`simulation/`): integrates the torque-free Euler rotation
  equations with RK4 → ω-t graphs, a three-axis stable/unstable comparison,
  the sphere–ellipsoid state space (polhode), the inverse period model, and a
  3D flip animation. See [`simulation/README.md`](simulation/README.md) for how
  to run it.
- **Interactive web app** (`web/index.html`): a Three.js simulation that runs
  straight in the browser — sliders for I₁·I₂·I₃ and the initial conditions, a
  live 3D body, the sphere–ellipsoid state space, and an ω(t) plot.

```bash
cd simulation && pip install -r requirements.txt && python run_all.py
```
