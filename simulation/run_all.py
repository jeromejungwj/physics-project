"""Generate every figure and animation for the project in one go.

    cd simulation
    pip install -r requirements.txt
    python run_all.py
"""

import os

import fig_omega_graphs as omega
import fig_polhode as polhode
import fig_period_model as period
import animate_racquet as racquet

if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    print("[1/4] angular-velocity graphs ...")
    omega.omega_time_series()
    omega.three_axis_comparison()
    print("[2/4] sphere-ellipsoid construction ...")
    polhode.polhode_figure()
    print("[3/4] period vs. initial speed ...")
    period.period_vs_speed()
    print("[4/4] 3D flip animation (this one takes ~a minute) ...")
    racquet.animate()
    print("done -> see the figures/ directory")
