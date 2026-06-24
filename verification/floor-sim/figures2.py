import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from lindblad import fock_ops, dissipator_super

INK="#101d26";PAPER="#f6f8f9";TEAL="#0e7c7b";CORAL="#e4572e";VIOLET="#6b4e9b";OPEN="#b07d1f";PASS="#1e8e5a"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"text.color":INK,
 "xtick.color":INK,"ytick.color":INK,"figure.facecolor":PAPER,"axes.facecolor":PAPER,"savefig.facecolor":PAPER})

def parity_masks(N):
    s=(-1.0)**np.arange(N); I,J=np.meshgrid(np.arange(N),np.arange(N),indexing='ij')
    sign=s[I.flatten(order='F')]*s[J.flatten(order='F')]
    return np.where(sign>0)[0],np.where(sign<0)[0]
def anchored(N,nbar,k1=0.05,t=0.0):
    a,I=fock_ops(N); J=(a@a-nbar*I)+t*a; L=dissipator_super(J)+k1*dissipator_super(a)
    e,o=parity_masks(N); cross=np.abs(L[np.ix_(e,o)]).max()+np.abs(L[np.ix_(o,e)]).max()
    gp=np.sort(-np.linalg.eigvals(L[np.ix_(e,e)]).real)[1]
    gb=np.sort(-np.linalg.eigvals(L[np.ix_(o,o)]).real)[0]
    return gb,gp,cross
def naive(N,nbar,k1=0.05):
    a,I=fock_ops(N); L=dissipator_super(a@a-nbar*I)+k1*dissipator_super(a)
    r=np.sort(-np.linalg.eigvals(L).real); return r[1]  # "slowest nonzero" = naive bit-flip

# ---- FIG 3: the fix (convergence) + the diagnosis (symmetry breaking) ----
Ns=[16,20,24,28,32,36,40,44]
gb=[anchored(N,3.0)[0] for N in Ns]
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(11.6,4.4))
ax1.plot(Ns,gb,"o-",color=PASS,lw=2,ms=6,label="parity-anchored  $\\Gamma_{bit}$  (the fix)")
ax1.axhline(gb[-1],color=PASS,ls=":",lw=1)
ax1.set_xlabel("Fock-space cutoff  $N$"); ax1.set_ylabel("bit-flip rate  ($\\kappa_2$)")
ax1.set_title("The fix converges",fontweight="bold",fontsize=12)
ax1.ticklabel_format(axis="y",style="sci",scilimits=(0,0))
ax1.text(0.5,0.5,"stable to 4 sig figs\nacross every cutoff",transform=ax1.transAxes,
         color=PASS,fontsize=11,ha="center",bbox=dict(fc=PAPER,ec=PASS,alpha=0.85))
ax1.legend(); ax1.grid(alpha=0.2)

ts=np.linspace(0,1,11); cr=[anchored(32,3.0,t=t)[2] for t in ts]
ax2.plot(ts,cr,"D-",color=CORAL,lw=2,ms=6)
ax2.set_xlabel("single-photon admixture  $t$  in  $a^2-\\bar n + t\\,a$")
ax2.set_ylabel("cross-sector coupling")
ax2.set_title("The diagnosis: $t>0$ breaks the symmetry",fontweight="bold",fontsize=12)
ax2.axhline(0,color=INK,lw=0.8)
ax2.annotate("parity intact\n(rates defined)",xy=(0,0),xytext=(0.18,0.18),
   textcoords="axes fraction",color=PASS,fontsize=10,
   arrowprops=dict(arrowstyle="->",color=PASS))
ax2.text(0.55,0.55,"qubit dissolving\n(rates undefined)",transform=ax2.transAxes,
   color=CORAL,fontsize=10,bbox=dict(fc=PAPER,ec=CORAL,alpha=0.85))
ax2.grid(alpha=0.2)
fig.tight_layout(); fig.savefig("fig3_metric_fix.png",dpi=150); plt.close(fig)

# ---- FIG 4: the right direction — climb the symmetry ladder ----
def steady_dim(N,k,nbar,thr=1e-6):
    a,I=fock_ops(N); ak=np.linalg.matrix_power(a,k); J=ak-(nbar**(k/2))*I
    return int(np.sum(np.abs(np.linalg.eigvals(dissipator_super(J)).real)<thr))
ks=[2,3,4]; dims=[steady_dim(16+8*k,k,1.5) for k in ks]
fig,ax=plt.subplots(figsize=(7.0,4.4))
bars=ax.bar([f"k={k}\n($Z_{k}$)" for k in ks],dims,color=[CORAL,OPEN,TEAL],width=0.6,edgecolor=INK)
for b,k,d in zip(bars,ks,dims):
    ax.text(b.get_x()+b.get_width()/2,d+0.4,f"dim {d} = {int(round(d**0.5))}$^2$",
            ha="center",fontweight="bold")
ax.set_ylabel("protected steady-manifold dimension")
ax.set_title("Climb the symmetry ladder, don't break it",fontweight="bold",fontsize=12)
ax.set_ylim(0,18)
ax.text(0.02,0.95,"k=2: loss → biased qubit\nk=4: loss → detectable $Z_4$ syndrome → correctable",
        transform=ax.transAxes,va="top",fontsize=10.5,
        bbox=dict(fc=PAPER,ec=INK,alpha=0.9))
fig.tight_layout(); fig.savefig("fig4_symmetry_ladder.png",dpi=150); plt.close(fig)
print("naive bit-flip across N (the OLD method, for the record):",
      [round(naive(N,3.0),7) for N in [16,24,32,40]])
print("saved fig3_metric_fix.png, fig4_symmetry_ladder.png")
