import numpy as np, matplotlib, os
matplotlib.use("Agg"); import matplotlib.pyplot as plt

a2 = np.array([2, 3, 4])
base = np.array([5.17, 3.99, 3.19]) * 1e-3          # hand-designed, T-optimized, converged N
search = np.array([5.38, 3.99, np.nan]) * 1e-3      # two-quad seeded search (a2=4 compute-bound)

fig, ax = plt.subplots(figsize=(7.4, 4.7))
ax.plot(a2, base, "o-", color="#2471a3", lw=2, ms=9,
        label="hand-designed gate (T-optimized)")
ax.plot(a2[:2], search[:2], "s--", color="#c0392b", ms=8,
        label="AI search (2-quadrature, seeded)")
for x, b in zip(a2, base):
    ax.annotate(f"{b*1e3:.2f}e-3", (x, b), textcoords="offset points",
                xytext=(0, 10), ha="center", fontsize=9, color="#2471a3")
ax.annotate("search recovers hand-design\n(gain x1.04; $\\epsilon_y\\!\\to\\!0$)",
            (2, 5.38e-3), textcoords="offset points", xytext=(20, 18),
            fontsize=9, color="#c0392b",
            arrowprops=dict(arrowstyle="->", color="#c0392b"))
ax.annotate("$\\alpha^2{=}4$ search compute-bound\n(needs N$\\geq$24); baseline shown",
            (4, 3.19e-3), textcoords="offset points", xytext=(-150, -34),
            fontsize=8.5, color="#666")
ax.set_xticks([2, 3, 4])
ax.set_xlabel("cat size  $\\alpha^2$  (mean photon number)")
ax.set_ylabel("tolerable noise ratio  $\\kappa_1/\\kappa_2$  (gate-validity frontier)")
ax.set_title("Phase B result: AI search maps the bias-preserving Z($\\pi/2$) frontier\n"
             "but does not push it past hand-design  (kept negative)")
ax.legend(frameon=False, loc="upper right")
ax.grid(alpha=0.3); ax.set_ylim(2.5e-3, 6e-3)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phase_b_frontier_map.png")
fig.savefig(out, dpi=150); print("saved", out)
