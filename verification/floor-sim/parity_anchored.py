import numpy as np
from lindblad import fock_ops, dissipator_super

def parity_masks(N):
    s=(-1.0)**np.arange(N)
    I,J=np.meshgrid(np.arange(N),np.arange(N),indexing='ij')
    sign=s[I.flatten(order='F')]*s[J.flatten(order='F')]
    return np.where(sign>0)[0],np.where(sign<0)[0]

def anchored_rates(N,nbar,k1=0.05,t=0.0):
    a,I=fock_ops(N)
    J=(a@a - nbar*I) + t*a          # t!=0 adds parity-ODD single-photon term
    L=dissipator_super(J)+k1*dissipator_super(a)
    even,odd=parity_masks(N)
    cross=np.abs(L[np.ix_(even,odd)]).max()+np.abs(L[np.ix_(odd,even)]).max()
    g_phase=np.sort(-np.linalg.eigvals(L[np.ix_(even,even)]).real)[1]  # even: steady + phase
    g_bit  =np.sort(-np.linalg.eigvals(L[np.ix_(odd,odd)]).real)[0]    # odd: bit-flip
    return g_bit,g_phase,cross

print("CORRECTED LABELS  (even sector = phase-flip, odd sector = bit-flip):")
print(f"{'n_bar':>6}{'Gamma_bit(odd)':>16}{'Gamma_phase(even)':>18}{'check 2*k1*n':>14}")
for nb in [2.0,3.0,4.0]:
    b,p,c=anchored_rates(40,nb)
    print(f"{nb:6.1f}{b:16.3e}{p:18.3e}{0.05*2*nb:14.3f}")

print("\nDIAGNOSIS: does the +t*a direction break the parity symmetry the anchor needs?")
print(f"{'t':>6}{'cross-sector coupling':>24}{'  parity symmetry':>18}")
for t in [0.0,0.1,0.25,0.5,1.0]:
    b,p,c=anchored_rates(36,3.0,t=t)
    status = "INTACT (anchor valid)" if c<1e-9 else "BROKEN (rates undefined)"
    print(f"{t:6.2f}{c:24.3e}   {status}")
print("\n=> t=0: parity intact, rates well-defined. t>0: my old 'enrichment' breaks")
print("   the symmetry that DEFINES the cat logical operators. The non-convergence")
print("   I saw before was the qubit dissolving, not a numerical artifact.")
