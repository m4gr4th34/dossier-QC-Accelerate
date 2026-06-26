"""Validation figure for the gate-metric instrument."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))  # so 'figure_style' is importable
from figure_style import apply_dossier_style, TITLE_FONT
plt = apply_dossier_style()
from gate_metric_validation import measure_gate

kappa2 = 1.0
eps = 0.05 * kappa2
T = 30.0 / kappa2

# Panel 1: bias scaling vs alpha^2
a2s = [2, 3, 4, 5]
pX, pZ = [], []
for a2 in a2s:
    r = measure_gate(np.sqrt(a2), 1e-3 * kappa2, kappa2, eps, T)
    pX.append(r["pX"]); pZ.append(r["pZ"])
pX, pZ = np.array(pX), np.array(pZ)

# Panel 2: adiabatic tradeoff -- peak leakage vs loss-induced infidelity, across speeds
speeds = [(0.02, 60), (0.05, 30), (0.10, 15), (0.20, 8), (0.40, 4)]
leak_peak, infid = [], []
for epsr, Tr in speeds:
    r = measure_gate(np.sqrt(4.0), 1e-3, kappa2, epsr * kappa2, Tr / kappa2)
    leak_peak.append(r["leak_peak"]); infid.append(1 - r["F"])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

ax1.semilogy(a2s, pX, "o-", label=r"bit-flip $p_X$", color="#cf5d36")
ax1.semilogy(a2s, pZ, "s-", label=r"phase-flip $p_Z$", color="#0c8f86")
ax1.set_xlabel(r"mean photon number $|\alpha|^2$")
ax1.set_ylabel("gate error probability")
ax1.set_title("Condition (2): bias by parity\nbit-flip suppressed, phase-flip linear", fontfamily=TITLE_FONT)
ax1.legend(frameon=False); ax1.grid(which="both")

ax2.loglog(infid, leak_peak, "D-", color="#6b4e9b")
for (epsr, Tr), x, y in zip(speeds, infid, leak_peak):
    ax2.annotate(f"T={Tr}", (x, y), textcoords="offset points",
                 xytext=(6, 4), fontsize=8)
ax2.set_xlabel(r"loss-induced infidelity $1-F$  (slow $\rightarrow$ right)")
ax2.set_ylabel(r"peak non-adiabatic leakage  (fast $\rightarrow$ up)")
ax2.set_title("Conditions (1)+(3): the adiabatic tradeoff\nthe frontier the search must navigate", fontfamily=TITLE_FONT)
ax2.grid(which="both")

fig.tight_layout()
_out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "gate_metric_validation.png")
fig.savefig(_out, dpi=150)
print(f"saved {_out}")
