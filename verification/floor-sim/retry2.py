import numpy as np
from lindblad import fock_ops, dissipator_super

N=40; a,I=fock_ops(N); k1=0.05
num=np.diag(np.arange(N)).astype(float)

def coherent(z,N):
    v=np.zeros(N,complex); v[0]=1
    for n in range(1,N): v[n]=v[n-1]*z/np.sqrt(n)
    return v/np.linalg.norm(v)

def steady_state(J):
    L=dissipator_super(J)+k1*dissipator_super(a)
    ev,vecs=np.linalg.eig(L)
    i=np.argmin(np.abs(ev))
    rho=vecs[:,i].reshape(N,N,order='F'); rho=rho/np.trace(rho)
    return (rho+rho.conj().T)/2

print("Is the 'single-photon admixture helps' result real, or is the code collapsing?")
print("J=(a^2-3)+t*a  -> the two stabilized coherent states are the roots of a^2+t*a-3=0.")
print(f"{'t':>5} {'root z1':>8} {'root z2':>8} {'pop|z1>':>9} {'pop|z2>':>9} {'balance':>9} {'n_bar':>7}")
for t in [0.0,0.5,1.0,1.5,2.0]:
    z1=(-t+np.sqrt(t*t+12))/2; z2=(-t-np.sqrt(t*t+12))/2
    J=a@a-3*I+t*a
    rho=steady_state(J)
    c1=coherent(z1,N); c2=coherent(z2,N)
    p1=np.real(c1.conj()@rho@c1); p2=np.real(c2.conj()@rho@c2)
    bal=min(p1,p2)/max(p1,p2)
    nb=np.real(np.trace(rho@num))
    print(f"{t:5.2f} {z1:8.2f} {z2:8.2f} {p1:9.3f} {p2:9.3f} {bal:9.3f} {nb:7.3f}")
print("\n=> as t grows the two logical wells become wildly UNEQUAL: loss drains the")
print("   high-photon well into the low one. The 'bit-flip rate' drops only because")
print("   one logical state is vanishing -- there is nothing left to flip into.")
print("   The metric was being gamed. A real code must be BALANCED.\n")

# Does a richer, BALANCED family do something the cat cannot? 4-component cat.
print("Four-photon dissipation J = a^4 - beta  (the 4-component cat, a known LOSS code):")
for nb_t in [2.0,3.0]:
    beta=nb_t**2
    J4=a@a@a@a - beta*I
    L0=dissipator_super(J4)                      # pristine code space
    r0=np.sort(np.abs(np.linalg.eigvals(L0).real))
    dim=int(np.sum(r0<1e-6))
    # how single-photon loss acts: does 'a' map code space to a DISTINCT subspace?
    # 2-cat: a preserves parity sectors weakly; 4-cat: a steps photon-number mod 4 -> detectable
    print(f"   beta={beta:.0f} (n_bar~{nb_t}):  steady-manifold dim = {dim}  "
          f"(2-photon cat gives 4; >4 here means a larger protected/ syndrome space)")
