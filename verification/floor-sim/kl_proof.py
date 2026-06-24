import numpy as np

def fock_a(N): return np.diag(np.sqrt(np.arange(1,N)),1)
def coherent(beta,N):
    v=np.zeros(N,complex); v[0]=1.0
    for n in range(1,N): v[n]=v[n-1]*beta/np.sqrt(n)
    return v/np.linalg.norm(v)
def kcat_sectors(alpha,k,N):
    w=np.exp(2j*np.pi/k)
    out=[]
    for j in range(k):
        v=sum((w**(-j*m))*coherent(alpha*w**m,N) for m in range(k))
        out.append(v/np.linalg.norm(v))
    return out

def analyze(alpha,k,enc,N=140):
    """Single-photon-loss correctability of the k-component cat.
    Returns (detectable_fraction, knill_laflamme_violation) for error set {I, a}."""
    a=fock_a(N); cs=kcat_sectors(alpha,k,N)
    L0,L1=cs[enc[0]],cs[enc[1]]
    Pc=np.outer(L0,L0.conj())+np.outer(L1,L1.conj())
    fr=[]
    for psi in [L0,L1,(L0+L1)/np.sqrt(2),(L0+1j*L1)/np.sqrt(2)]:
        e=a@psi; e=e/np.linalg.norm(e)
        fr.append(np.real(e.conj()@e - e.conj()@(Pc@e)))
    detect=float(np.mean(fr))
    nbar=np.real(L0.conj()@(a.conj().T@a@L0))
    E=[np.eye(N), a/np.sqrt(max(nbar,1e-9))]; Ls=[L0,L1]; eta=0.0
    for Ea in E:
        for Eb in E:
            B=np.array([[Ls[i].conj()@(Ea.conj().T@Eb@Ls[j]) for j in range(2)] for i in range(2)])
            eta=max(eta, np.linalg.norm(B-(np.trace(B)/2)*np.eye(2)))
    return detect,float(eta)

ENC={2:(0,1),3:(0,1),4:(0,2),5:(0,2),6:(0,3)}

def _report():
    nbars=[2,3,4,6]
    print("DETECTABLE FRACTION of one photon loss   (1.000 = loss is a detectable syndrome)")
    print(f"{'k':>2} {'sym':>4} | " + "  ".join(f"n̄={n:<3.0f}" for n in nbars))
    for k in [2,3,4]:
        print(f"{k:>2} {'Z'+str(k):>4} | " + "   ".join(f"{analyze(np.sqrt(n),k,ENC[k])[0]:5.3f}" for n in nbars))
    print("\nKNILL-LAFLAMME VIOLATION eta   (->0 = exactly correctable; O(1) = uncorrectable)")
    print(f"{'k':>2} {'sym':>4} | " + "  ".join(f"n̄={n:<3.0f}" for n in nbars))
    for k in [2,3,4]:
        print(f"{k:>2} {'Z'+str(k):>4} | " + "  ".join(f"{analyze(np.sqrt(n),k,ENC[k])[1]:6.3f}" for n in nbars))
    print("\nLADDER SELECTION @ n̄=4  (objective told only 'correct one photon loss'):")
    for k in [2,3,4,5,6]:
        d,e=analyze(np.sqrt(4.0),k,ENC[k])
        v="CORRECTS (detectable + KL->0)" if d>0.99 and e<0.25 else ("detects only" if d>0.99 else "FAILS - loss stays in code")
        print(f"   k={k} (Z{k}): detect={d:5.3f}  eta={e:6.3f}  ->  {v}")
    print("\n   => minimal loss-correcting cat the objective selects: k=4.")

if __name__=="__main__":
    _report()
