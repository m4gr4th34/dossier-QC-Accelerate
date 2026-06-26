import numpy as np, matplotlib, os
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))  # so 'figure_style' is importable
from figure_style import apply_dossier_style, TITLE_FONT
plt = apply_dossier_style()

a2 = np.array([2, 3, 4])
base = np.array([5.17, 3.99, 3.19]) * 1e-3          # hand-designed, T-optimized, converged N
search = np.array([5.38, 3.99, np.nan]) * 1e-3      # two-quad seeded search (a2=4 compute-bound)

fig, ax = plt.subplots(figsize=(7.4, 4.7))
ax.plot(a2, base, "o-", color="#0c8f86", lw=2, ms=9,
        label="hand-designed gate (T-optimized)")
ax.plot(a2[:2], search[:2], "s--", color="#cf5d36", ms=8,
        label="AI search (2-quadrature, seeded)")
for x, b in zip(a2, base):
    ax.annotate(f"{b*1e3:.2f}e-3", (x, b), textcoords="offset points",
                xytext=(0, -16), ha="center", fontsize=9, color="#0c8f86")
ax.set_xticks([2, 3, 4])
ax.set_xlabel("cat size  $\\alpha^2$  (mean photon number)")
ax.set_ylabel("tolerable noise ratio  $\\kappa_1/\\kappa_2$  (gate-validity frontier)")
ax.set_title("Phase B result: AI search maps the bias-preserving Z($\\pi/2$) frontier\n"
             "but does not push it past hand-design  (kept negative)", fontfamily=TITLE_FONT)
ax.legend(frameon=False, loc="upper right")
ax.grid(); ax.set_ylim(2.5e-3, 6e-3)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phase_b_frontier_map.png")
fig.savefig(out, dpi=150); print("saved", out)
