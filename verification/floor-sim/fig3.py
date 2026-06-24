import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from lindblad import fock_ops, dissipator_super
INK="#101d26";PAPER="#f6f8f9";TEAL="#0e7c7b";CORAL="#e4572e";VIOLET="#6b4e9b"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"text.color":INK,
  "xtick.color":INK,"ytick.color":INK,"figure.facecolor":PAPER,"axes.facecolor":PAPER,
  "savefig.facecolor":PAPER,"font.family":"DejaVu Sans"})
N=40;a,I=fock_ops(N);k1=0.05;num=np.diag(np.arange(N)).astype(float)
def coh(z):
    v=np.zeros(N,complex);v[0]=1
    for n in range(1,N):v[n]=v[n-1]*z/np.sqrt(n)
    return v/np.linalg.norm(v)
def ss(J):
    L=dissipator_super(J)+k1*dissipator_super(a)
    ev,vc=np.linalg.eig(L);i=np.argmin(np.abs(ev))
    r=vc[:,i].reshape(N,N,order='F');r=r/np.trace(r);return (r+r.conj().T)/2
ts=np.linspace(0,2.0,17);bal=[];rawbit=[]
for t in ts:
    z1=(-t+np.sqrt(t*t+12))/2;z2=(-t-np.sqrt(t*t+12))/2
    J=a@a-3*I+t*a;rho=ss(J)
    p1=np.real(coh(z1).conj()@rho@coh(z1));p2=np.real(coh(z2).conj()@rho@coh(z2))
    bal.append(min(p1,p2)/max(p1,p2))
    r=np.sort(np.abs(np.linalg.eigvals(dissipator_super(J)+k1*dissipator_super(a)).real))
    rawbit.append(r[1])
fig,ax=plt.subplots(figsize=(7.2,4.5))
ax.plot(ts,bal,"o-",color=VIOLET,lw=2,ms=5,label="code balance  (min/max logical-well population)")
ax.axhline(1.0,color=TEAL,ls=":",lw=1.4)
ax.scatter([0],[1.0],s=170,facecolors="none",edgecolors=TEAL,linewidths=2.4,zorder=5,
           label="symmetric cat (t=0): the only balanced code")
ax2=ax.twinx()
ax2.semilogy(ts,rawbit,"s--",color=CORAL,lw=1.6,ms=4,alpha=0.85,label="naive 'bit-flip' metric (gamed)")
ax.set_xlabel("single-photon admixture  t  in  $J=(a^2-3)+t\\,a$")
ax.set_ylabel("code balance",color=VIOLET);ax.set_ylim(0,1.08)
ax2.set_ylabel("naive bit-flip rate (units $\\kappa_2$)",color=CORAL)
ax.set_title("Reward-hacking, exposed: the metric 'improves' as the qubit dies",
             fontweight="bold",fontsize=12)
ax.text(0.97,0.55,"loss drains the high-photon\nwell -> code collapses to\none state -> 'bit-flip' is\nmeaningless",transform=ax.transAxes,ha="right",va="center",
        fontsize=10,color=INK,bbox=dict(fc=PAPER,ec=VIOLET,alpha=0.85))
l1,la1=ax.get_legend_handles_labels();l2,la2=ax2.get_legend_handles_labels()
ax.legend(l1+l2,la1+la2,loc="lower left",fontsize=9.5,framealpha=0.92)
ax.grid(alpha=0.18)
fig.tight_layout();fig.savefig("/mnt/user-data/outputs/fig3_reward_hacking.png",dpi=150)
fig.savefig("fig3_reward_hacking.png",dpi=150)
print("balance at t=0:",round(bal[0],3)," at t=2:",round(bal[-1],3))
print("saved fig3_reward_hacking.png")
