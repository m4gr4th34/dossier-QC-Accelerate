import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import os

T = np.array([2,3,4,5,6,8,10,12,16,20,25,30])
fr = np.array([5.172,4.821,4.406,4.021,3.683,3.136,2.723,2.402,1.939,1.624,1.348,1.151])*1e-3
r_base = 5.172e-3; r_star = 7.757e-3

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.plot(T, fr, "o-", color="#2471a3", label="hand-designed constant-$\\epsilon$ baseline")
ax.scatter([2],[r_base], s=120, facecolor="none", edgecolor="#2471a3", linewidth=2,
           zorder=5, label=f"best baseline = {r_base:.2e} (T=2)")
ax.axhline(r_star, ls="--", color="#c0392b", lw=1.5,
           label=f"search target (1.5x) = {r_star:.2e}")
ax.scatter([1.5],[r_star], marker="x", s=120, color="#c0392b", zorder=5)
ax.annotate("shaped-pulse search:\nbest reachable < baseline\n(margin -0.29, NOT valid here)",
            (1.5, r_star), textcoords="offset points", xytext=(28, -6),
            fontsize=9, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.set_xlabel("gate time  $T \\cdot \\kappa_2$")
ax.set_ylabel("tolerable noise ratio  $\\kappa_1/\\kappa_2$  (frontier)")
ax.set_title("Phase B (preliminary): shaped single-quadrature pulse does NOT\n"
             "beat the T-optimized hand-designed gate  ($\\alpha^2=2$, K=5)")
ax.legend(frameon=False, fontsize=9, loc="upper right")
ax.grid(alpha=0.3)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "phase_b_negative.png")
fig.savefig(out, dpi=150); print("saved", out)
