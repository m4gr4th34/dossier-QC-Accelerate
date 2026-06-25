"""
phase_b_search.py  (hardened, two-quadrature)
Phase B hardened: does richer control (two quadratures + more segments,
baseline-seeded) overturn the single-quadrature negative, or does it survive?
Baseline = T-optimized hand-designed constant-eps_x gate. Verdict = frontier
gain (searched tolerable k1/k2)/(baseline), re-validated at higher truncation.
y-quadrature is the bias-breaking reward-hack vector; condition (2) bit-flip
suppression (pX<=pX_max) catches it. Negative/partial/push all kept.
"""
import time
import numpy as np
from scipy.linalg import expm
from scipy.optimize import differential_evolution, minimize

THR = dict(F_tgt=0.95, pX_max=1e-3, eps_L=1e-3)
PAULI = {"I": np.eye(2, dtype=complex), "X": np.array([[0,1],[1,0]],complex),
         "Y": np.array([[0,-1j],[1j,0]],complex), "Z": np.array([[1,0],[0,-1]],complex)}
PL = ["I","X","Y","Z"]

def build(alpha, N):
    a = np.diag(np.sqrt(np.arange(1,N)),1).astype(complex); ad = a.conj().T
    I = np.eye(N,dtype=complex)
    L2 = a@a - (alpha**2)*I
    def coh(al):
        c=np.zeros(N,complex); c[0]=np.exp(-0.5*abs(al)**2)
        for k in range(1,N): c[k]=c[k-1]*al/np.sqrt(k)
        return c/np.linalg.norm(c)
    p,m = coh(alpha),coh(-alpha); ce,co = p+m,p-m
    ce/=np.linalg.norm(ce); co/=np.linalg.norm(co)
    z=ce+co; z/=np.linalg.norm(z); o=ce-co; o/=np.linalg.norm(o)
    W=np.column_stack([z,o])
    return dict(N=N,a=a,ad=ad,I=I,dx=a+ad,dy=1j*(ad-a),L2=L2,W=W,Pi=W@W.conj().T)

def lind(H,jumps,I):
    L=-1j*(np.kron(I,H)-np.kron(H.T,I))
    for c in jumps:
        cdc=c.conj().T@c
        L+=np.kron(c.conj(),c)-0.5*np.kron(I,cdc)-0.5*np.kron(cdc.T,I)
    return L

def appsup(P,rho):
    n=rho.shape[0]; return (P@rho.reshape(-1,order="F")).reshape(n,n,order="F")

def precompute(alpha,N,kappa2,ratio,K,tail=4.0):
    op=build(alpha,N); I=op["I"]
    jumps=[np.sqrt(kappa2)*op["L2"], np.sqrt(ratio*kappa2)*op["a"]]
    op["L_diss"]=lind(0*I,jumps,I)
    op["Cx"]=-1j*(np.kron(I,op["dx"])-np.kron(op["dx"].T,I))
    op["Cy"]=-1j*(np.kron(I,op["dy"])-np.kron(op["dy"].T,I))
    op["restab"]=expm(op["L_diss"]*(tail/kappa2)); op["K"]=K
    return op

def z_ptm(t):
    R=np.eye(4); c,s=np.cos(t),np.sin(t); R[1,1],R[1,2],R[2,1],R[2,2]=c,-s,s,c; return R

def realized_ptm(ex,ey,T,op):
    K=op["K"]; dt=T/K
    P=np.eye(op["L_diss"].shape[0],dtype=complex)
    for k in range(K):
        P=expm((op["L_diss"]+ex[k]*op["Cx"]+ey[k]*op["Cy"])*dt)@P
    Pt=op["restab"]@P
    R=np.zeros((4,4))
    for j,pj in enumerate(PL):
        lg=op["W"].conj().T@appsup(Pt,op["W"]@PAULI[pj]@op["W"].conj().T)@op["W"]
        for i,pi in enumerate(PL): R[i,j]=np.real(np.trace(PAULI[pi]@lg))/2
    dens=[np.array([[1,0],[0,0]],complex),np.array([[0,0],[0,1]],complex),
          0.5*np.array([[1,1],[1,1]],complex),0.5*np.array([[1,-1j],[1j,1]],complex)]
    lp=[1-np.real(np.trace(op["Pi"]@appsup(P,op["W"]@d@op["W"].conj().T))) for d in dens]
    lr=[1-np.real(np.trace(op["Pi"]@appsup(Pt,op["W"]@d@op["W"].conj().T))) for d in dens]
    return R,float(np.mean(lp)),float(np.mean(lr))

def conditions(ex,ey,T,op,target=z_ptm(np.pi/2)):
    R,lp,lr=realized_ptm(ex,ey,T,op)
    F=float(np.clip(np.real((np.trace(target.T@R)+2)/6),0,1))
    d=np.clip(np.real(np.diag(R@target.T)),-1,1); rI,rX,rY,rZ=d
    pX=max(0.25*(rI+rX-rY-rZ),0.0); pZ=max(0.25*(rI-rX-rY+rZ),0.0)
    return dict(F=F,pX=pX,pZ=pZ,leak_peak=lp,leak_resid=lr)

def margins(c,thr=THR):
    return ((c["F"]-thr["F_tgt"])/(1-thr["F_tgt"]),
            (thr["pX_max"]-c["pX"])/thr["pX_max"],
            (thr["eps_L"]-c["leak_resid"])/thr["eps_L"])

def min_margin(ex,ey,T,op):
    c=conditions(ex,ey,T,op); return min(margins(c)),c

def calibrate_constant(alpha,N,kappa2,T,K,target=np.pi/2):
    op0=precompute(alpha,N,kappa2,0.0,K); er=0.01
    R,_,_=realized_ptm(np.full(K,er),np.zeros(K),T,op0)
    th=np.arctan2(R[2,1],R[1,1]);  th+= (2*np.pi if th<=0 else 0)
    return target/(th/er)

def frontier_fixed(ex,ey,T,alpha,N,kappa2,K,r_lo=1e-4,r_hi=3e-2,iters=16):
    def valid(r):
        m,_=min_margin(ex,ey,T,precompute(alpha,N,kappa2,r,K)); return m>=0
    if not valid(r_lo): return None
    lo,hi=r_lo,r_hi
    if valid(hi): return hi
    for _ in range(iters):
        mid=np.sqrt(lo*hi)
        if valid(mid): lo=mid
        else: hi=mid
    return lo

def baseline_best(alpha,N,kappa2,K,T_grid):
    best=dict(T=None,r=-1,e=None)
    for T in T_grid:
        e=calibrate_constant(alpha,N,kappa2,T,K)
        r=frontier_fixed(np.full(K,e),np.zeros(K),T,alpha,N,kappa2,K) or 0.0
        if r>best["r"]: best=dict(T=T,r=r,e=e)
    return best

def run_DE(op,K,x0,eps_b,T_b,budget):
    bounds=[eps_b]*(2*K)+[T_b]; n={"c":0}
    def neg(x):
        n["c"]+=1; m,_=min_margin(x[:K],x[K:2*K],x[2*K],op); return -m
    t0=time.time()
    res=differential_evolution(neg,bounds,x0=x0,maxiter=budget["maxiter"],
        popsize=budget["popsize"],tol=1e-4,seed=0,polish=True,init="sobol",
        mutation=(0.5,1.5))
    return dict(x=res.x,m=-res.fun,nfev=n["c"],t=time.time()-t0)

def run_LBFGS(op,K,x0,eps_b,T_b):
    bounds=[eps_b]*(2*K)+[T_b]; n={"c":0}
    def neg(x):
        n["c"]+=1; m,_=min_margin(x[:K],x[K:2*K],x[2*K],op); return -m
    t0=time.time()
    res=minimize(neg,x0,method="L-BFGS-B",bounds=bounds,options=dict(maxiter=300,eps=1e-3))
    return dict(x=res.x,m=-res.fun,nfev=n["c"],t=time.time()-t0)

def hardened_bakeoff(a2,N,N_hi,K,kappa2=1.0,push=1.5,budget=dict(maxiter=15,popsize=8)):
    alpha=np.sqrt(a2); T_grid=[2,3,4,6,8,12,20]
    print(f"\n{'='*68}\nalpha^2={a2}  N={N} (reval N={N_hi})  K={K}  2-quadrature\n{'='*68}")
    bb=baseline_best(alpha,N,kappa2,K,T_grid); r_base=bb["r"]
    print(f"[baseline] T={bb['T']} eps={bb['e']:.4f} frontier k1/k2={r_base:.3e}")
    r_star=r_base*push; op=precompute(alpha,N,kappa2,r_star,K)
    eps_b,T_b=(-0.5,0.5),(1.2,40.0)
    x0=np.concatenate([np.full(K,bb["e"]),np.zeros(K),[np.clip(float(bb["T"]),*T_b)]])
    de=run_DE(op,K,x0,eps_b,T_b,budget); lb=run_LBFGS(op,K,de["x"],eps_b,T_b)
    best=max([de,lb],key=lambda d:d["m"])
    print(f"[search]   DE m={de['m']:+.3f} ({de['nfev']}ev {de['t']:.0f}s) | "
          f"LBFGS m={lb['m']:+.3f} | best m={best['m']:+.3f}")
    ex,ey,T=best["x"][:K],best["x"][K:2*K],best["x"][2*K]
    _,cb=min_margin(ex,ey,T,op)
    print(f"           winner T={T:.2f} F={cb['F']:.4f} pX={cb['pX']:.2e} "
          f"leak={cb['leak_resid']:.2e} |eps_y|max={np.max(np.abs(ey)):.3f}")
    fr=frontier_fixed(ex,ey,T,alpha,N,kappa2,K) or 0.0
    print(f"[frontier] N={N}: searched {fr:.3e} vs baseline {r_base:.3e} -> x{fr/r_base:.2f}")
    bb_hi=baseline_best(alpha,N_hi,kappa2,K,[bb["T"],bb["T"]+2,max(2,bb["T"]-1)])
    fr_hi=frontier_fixed(ex,ey,T,alpha,N_hi,kappa2,K) or 0.0
    gh=fr_hi/bb_hi["r"] if bb_hi["r"] else float("inf")
    print(f"[frontier] N={N_hi}: searched {fr_hi:.3e} vs baseline {bb_hi['r']:.3e} -> x{gh:.2f}")
    verdict=("PUSH" if gh>=push else "PARTIAL" if gh>1.05 else "NEGATIVE (kept)")
    print(f"[VERDICT]  alpha^2={a2}: {verdict} (gain x{gh:.2f} at N={N_hi})")
    return dict(a2=a2,r_base=bb_hi["r"],fr=fr_hi,gain=gh,verdict=verdict)

if __name__=="__main__":
    np.set_printoptions(precision=4,suppress=True)
    print("HARDENED PHASE B — two-quadrature, baseline-seeded"); print("bar:",THR)
    res=[]
    import sys
    configs=eval(sys.argv[1]) if len(sys.argv)>1 else [(2,12,18,15,8)]
    for cfg in configs:
        a2,N,N_hi,mi,ps=cfg
        res.append(hardened_bakeoff(a2,N,N_hi,K=6,budget=dict(maxiter=mi,popsize=ps)))
    print("\nSUMMARY")
    for r in res:
        print(f"  a^2={r['a2']}: base={r['r_base']:.3e} search={r['fr']:.3e} "
              f"x{r['gain']:.2f} -> {r['verdict']}")
    print("DONE.")
