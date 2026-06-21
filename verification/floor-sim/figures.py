import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lindblad import fock_ops, dissipator_super, liouvillian, spectrum

INK="#101d26"; PAPER="#f6f8f9"; TEAL="#0e7c7b"; CORAL="#e4572e"; VIOLET="#6b4e9b"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,
    "text.color":INK,"xtick.color":INK,"ytick.color":INK,"figure.facecolor":PAPER,
    "axes.facecolor":PAPER,"savefig.facecolor":PAPER,"font.family":"DejaVu Sans"})

# ---------- FIG 1: the steady state IS a qubit ----------
N=24; nbar=2.0
L=liouvillian(N,nbar,k2=1.0,k1=0.0)
ev=np.linalg.eigvals(L)
fig,ax=plt.subplots(figsize=(6.6,4.4))
ax.scatter(ev.real,ev.imag,s=26,color=INK,alpha=0.55,zorder=2)
zero=ev[np.abs(ev.real)<1e-6]
ax.scatter(zero.real,zero.imag,s=170,facecolors="none",edgecolors=CORAL,
           linewidths=2.4,zorder=3,label=f"{len(zero)} zero modes = one logical qubit")
gap=np.sort(-ev.real)[np.sum(np.abs(ev.real)<1e-6)]
ax.axvspan(-gap,0.15,color=TEAL,alpha=0.08,zorder=0)
ax.axvline(-gap,color=TEAL,ls="--",lw=1.6,label=f"dissipative gap  $\\kappa_2$-scale = {gap:.2f}")
ax.set_xlabel("Re $\\lambda$  (decay rate, units of $\\kappa_2$)")
ax.set_ylabel("Im $\\lambda$")
ax.set_title("The steady state of two-photon dissipation is one logical qubit",
             fontweight="bold",fontsize=12)
ax.legend(loc="upper left",framealpha=0.9); ax.grid(alpha=0.18)
fig.tight_layout(); fig.savefig("fig1_qubit_manifold.png",dpi=150); plt.close(fig)

# ---------- FIG 2: autonomous protection + exponential bias ----------
N=40; k1=0.05
nbars=np.arange(1.0,6.01,0.25)
gbit=[]; gphase=[]
for nb in nbars:
    L=liouvillian(N,nb,k2=1.0,k1=k1)
    r=np.sort(-np.linalg.eigvals(L).real)
    gbit.append(r[1]); gphase.append(r[2])
gbit=np.array(gbit); gphase=np.array(gphase); bias=gphase/gbit

fig,(ax1,ax2)=plt.subplots(1,2,figsize=(11.6,4.5))
ax1.semilogy(nbars,gbit,"o-",color=CORAL,lw=2,ms=5,label="bit-flip  $\\Gamma_X$  (exponential $\\downarrow$)")
ax1.semilogy(nbars,gphase,"s-",color=TEAL,lw=2,ms=5,label="phase-flip  $\\Gamma_Z$  (linear $\\uparrow$)")
ax1.set_xlabel("cat size  $\\bar n=\\alpha^2$  (mean photons)")
ax1.set_ylabel("logical error rate  (units of $\\kappa_2$)")
ax1.set_title("Autonomous protection — no code, no decoder",fontweight="bold",fontsize=12)
ax1.legend(); ax1.grid(alpha=0.2,which="both")
# fit exponent for annotation
slope=np.polyfit(nbars,np.log(gbit),1)[0]
ax1.text(0.05,0.06,f"$\\Gamma_X\\propto e^{{{slope:.2f}\\,\\bar n}}$",transform=ax1.transAxes,
         color=CORAL,fontsize=12,bbox=dict(fc=PAPER,ec=CORAL,alpha=0.8))

ax2.semilogy(nbars,bias,"D-",color=VIOLET,lw=2,ms=5)
ax2.set_xlabel("cat size  $\\bar n=\\alpha^2$")
ax2.set_ylabel("noise bias  $\\Gamma_Z/\\Gamma_X$")
ax2.set_title("The bias the qubit is engineered to have",fontweight="bold",fontsize=12)
ax2.grid(alpha=0.2,which="both")
ax2.text(0.05,0.86,f"bias grows from {bias[0]:.0f}\nto {bias[-1]:.1e}",transform=ax2.transAxes,
         color=VIOLET,fontsize=11,va="top",bbox=dict(fc=PAPER,ec=VIOLET,alpha=0.8))
fig.tight_layout(); fig.savefig("fig2_autonomous_protection.png",dpi=150); plt.close(fig)

# save the data table
import csv
with open("floor_sim_data.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["n_bar","Gamma_bitflip","Gamma_phaseflip","bias"])
    for nb,b,p,bi in zip(nbars,gbit,gphase,bias): w.writerow([f"{nb:.3f}",f"{b:.6e}",f"{p:.6e}",f"{bi:.6e}"])

print("exponent slope (Gamma_X ~ exp(slope * n_bar)):",round(slope,3))
print("bias range:",f"{bias[0]:.1f}","->",f"{bias[-1]:.3e}")
print("phase-flip / (k1*n_bar) check:",np.round(gphase/(k1*nbars),3)[:5],"(should be ~2, i.e. 2*k1*n_bar)")
print("saved: fig1_qubit_manifold.png, fig2_autonomous_protection.png, floor_sim_data.csv")
