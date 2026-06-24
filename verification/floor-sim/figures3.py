import os; OUT=os.path.dirname(os.path.abspath(__file__))
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from kl_proof import analyze, ENC
INK="#101d26";PAPER="#f6f8f9";TEAL="#0e7c7b";CORAL="#e4572e";VIOLET="#6b4e9b";GOLD="#b07d1f"
plt.rcParams.update({"font.size":11,"axes.edgecolor":INK,"axes.labelcolor":INK,"text.color":INK,
  "xtick.color":INK,"ytick.color":INK,"figure.facecolor":PAPER,"axes.facecolor":PAPER,
  "savefig.facecolor":PAPER,"font.family":"DejaVu Sans"})

fig,(axA,axB)=plt.subplots(1,2,figsize=(11,4.4))

# Panel A: KL violation vs nbar
nb=np.linspace(1.5,8,12)
col={2:CORAL,3:GOLD,4:TEAL}
for k in [2,3,4]:
    ys=[analyze(np.sqrt(x),k,ENC[k])[1] for x in nb]
    axA.semilogy(nb,ys,"o-",color=col[k],lw=2,ms=5,label=f"{k}-component cat (Z{k})")
axA.axhline(0.05,color=INK,ls=":",lw=1.2,alpha=.6)
axA.text(7.7,0.058,"correctable",ha="right",va="bottom",fontsize=9,color=INK,alpha=.7)
axA.set_xlabel("cat size  n̄ = α²  (photons)")
axA.set_ylabel("Knill–Laflamme violation  η   (log)")
axA.set_title("Does loss become correctable?",fontweight="bold",fontsize=12)
axA.legend(fontsize=9.5,framealpha=.92,loc="center right")
axA.grid(alpha=.18,which="both")
axA.annotate("4-cat → 0\n(exactly correctable)",xy=(5.62,0.0019),
  xytext=(2.35,0.0026),fontsize=9.5,color=TEAL,ha="left",
  arrowprops=dict(arrowstyle="->",color=TEAL,lw=1.4))
axA.text(5.0,0.42,"2- & 3-cat never reach it\n(loss = logical error)",fontsize=9.5,color=CORAL,va="center",ha="center")

# Panel B: detectable fraction vs k (the ladder selection)
ks=[2,3,4,5,6]
det=[analyze(np.sqrt(4.0),k,ENC[k])[0] for k in ks]
bars=axB.bar([str(k) for k in ks],det,
  color=[CORAL if d<0.99 else TEAL for d in det],edgecolor=INK,lw=1.2,width=.64)
axB.axhline(1.0,color=INK,ls=":",lw=1)
for k,d,b in zip(ks,det,bars):
    axB.text(b.get_x()+b.get_width()/2,d+0.03,f"{d:.2f}",ha="center",fontsize=10,color=INK)
axB.set_ylim(0,1.18)
axB.set_xlabel("number of cat components  k  (Z$_k$ symmetry)")
axB.set_ylabel("fraction of a single loss that is detectable")
axB.set_title("Smallest cat that corrects loss",fontweight="bold",fontsize=12)
axB.annotate("k = 4: minimal\nloss-correcting",xy=(1.66,0.99),xytext=(-0.45,0.84),
  fontsize=10,color=TEAL,fontweight="bold",ha="left",
  arrowprops=dict(arrowstyle="->",color=TEAL,lw=1.6))
axB.text(-0.35,0.06,"k≤3:\nloss hides\nin the code",fontsize=9,color=CORAL,va="bottom")

fig.suptitle("The strong proof: single-photon loss is a correctable Z₄ syndrome — and k=4 is minimal",
  fontsize=12.5,fontweight="bold",y=1.005)
fig.tight_layout()
fig.savefig(os.path.join(OUT,"fig5_kl_correctability.png"),dpi=150)
print("detect(n̄=4):",{k:round(analyze(np.sqrt(4.0),k,ENC[k])[0],3) for k in ks})
print("saved", os.path.join(OUT,"fig5_kl_correctability.png"))
