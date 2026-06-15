"""Precession period vs. initial angular speed.

Reproduces the key quantitative result of Bubbar & Zhu (2025): the period of
the unstable flipping motion is inversely related to the initial angular speed.
The paper fit a three-parameter inverse model

    T(w0) = a / (w0 + b) + c

to 63 filtered tennis-racquet trials, with best-fit parameters a = 11.85,
b = 2.30 s^-1, c = 0.047 s and a good fit of chi^2 = 1.58.  Here we instead
generate the "data" from the numerical Euler simulation itself: for a range of
initial speeds about (mostly) the intermediate axis we measure the flip period
from the omega_2 zero crossings, then fit the same inverse model.  Our fitted
a, b, c therefore differ from the paper's empirical values -- they come from the
synthetic simulation, not the racquet data -- but the same inverse form holds.
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from physics import simulate, TEXTBOOK_INERTIA


def measure_period(t, w2):
    """Estimate the flip period from the omega_2 series.

    Successive zero crossings of omega_2 are half a precession period apart, so
    we average the zero-to-zero gaps and double them.  (The paper instead labels
    both zeros and local extrema in Fig. 4, where adjacent labelled points are a
    quarter period apart; using zeros alone is sufficient here.)  Returns NaN if
    too few crossings are found.
    """
    sign = np.sign(w2)
    # ignore exact zeros to avoid double counting
    sign[sign == 0] = 1
    crossings = np.where(np.diff(sign) != 0)[0]
    if len(crossings) < 3:
        return np.nan
    # linear interpolation for sub-step crossing times
    times = []
    for i in crossings:
        t0, t1 = t[i], t[i + 1]
        y0, y1 = w2[i], w2[i + 1]
        times.append(t0 - y0 * (t1 - t0) / (y1 - y0))
    times = np.array(times)
    half_periods = np.diff(times)
    return 2.0 * np.mean(half_periods)


def inverse_model(w0, a, b, c):
    return a / (w0 + b) + c


def period_vs_speed(I=TEXTBOOK_INERTIA, outfile="figures/period_vs_speed.png"):
    speeds = np.linspace(2.0, 14.0, 28)
    eps = 0.06  # small perturbation kept fixed -> stay near the intermediate axis
    periods = []
    used = []
    for w0mag in speeds:
        res = simulate(I, [eps, w0mag, eps], t_max=40.0, dt=0.001)
        T = measure_period(res["t"], res["w"][:, 1])
        if np.isfinite(T):
            periods.append(T)
            used.append(w0mag)
    used = np.array(used)
    periods = np.array(periods)

    (a, b, c), _ = curve_fit(inverse_model, used, periods,
                             p0=[10.0, 1.0, 0.0], maxfev=10000)

    # chi-square-like goodness using a nominal 5% spread (illustrative)
    model = inverse_model(used, a, b, c)
    resid = periods - model

    fig, (ax, axr) = plt.subplots(
        2, 1, figsize=(8, 6.5), sharex=True,
        gridspec_kw={"height_ratios": [3, 1]})
    ax.scatter(used, periods, s=28, color="#2ca02c", zorder=3,
               label="numerical Euler simulation")
    fine = np.linspace(used.min(), used.max(), 300)
    fit_label = ("fit  $T = a/(\\omega_0+b)+c$\n"
                 f"$a={a:.2f},\\ b={b:.2f},\\ c={c:.3f}$")
    ax.plot(fine, inverse_model(fine, a, b, c), color="#d62728", lw=2,
            label=fit_label)
    ax.set_ylabel("flip / precession period  $T$  (s)")
    ax.set_title("Precession period is inversely related to initial speed\n"
                 "(reproducing Bubbar & Zhu 2025, Fig. 12)")
    ax.legend(fontsize=9)

    axr.axhline(0, color="grey", lw=0.8)
    axr.scatter(used, resid, s=20, color="#1f77b4")
    axr.set_ylabel("residual (s)")
    axr.set_xlabel(r"initial angular speed  $\omega_0$  (rad s$^{-1}$)")

    fig.tight_layout()
    fig.savefig(outfile, dpi=140)
    plt.close(fig)
    print(f"wrote {outfile}  ->  a={a:.3f}, b={b:.3f}, c={c:.4f}")


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    period_vs_speed()
