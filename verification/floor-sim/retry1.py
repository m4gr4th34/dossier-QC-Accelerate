import numpy as np
from lindblad import fock_ops, dissipator_super

def logical_metric(J, N, k1=0.05, k2=1.0, gapfactor=8.0):
    """Operational, gap-guarded logical metric.
    Returns dict with validity, bit-flip & phase-flip rates, and the gap ratio.
    A candidate is VALID only if the 4 smallest |Re lambda| (the logical
    operator sector: 1 steady + 3 logical-error modes) sit below a clear
    dissipative gap. Otherwise the 'logical rate' is meaningless and we say so."""
    a,_ = fock_ops(N)
    L = k2*dissipator_super(J) + k1*dissipator_super(a)
    r = np.sort(np.abs(np.linalg.eigvals(L).real))   # |Re lambda| ascending
    logical = r[:4]; leak = r[4]
    gap_ratio = leak / max(logical[3], 1e-15)
    valid = gap_ratio > gapfactor
    return dict(valid=valid, gap_ratio=gap_ratio,
                bitflip=logical[1], phaseflip=logical[2])

# --- (a) the guard ACCEPTS the clean cat and reproduces the bias, cutoff-robustly
print("(a) clean two-photon cat  J = a^2 - nbar  :  cutoff-robustness check")
print(f"{'nbar':>5} {'N=28':>22} {'N=40':>22}")
for nbar in [2.0,3.0,4.0]:
    a28,_=fock_ops(28); a40,_=fock_ops(40)
    m28=logical_metric(a28@a28-nbar*np.eye(28),28)
    m40=logical_metric(a40@a40-nbar*np.eye(40),40)
    s=lambda m:f"valid={m['valid']} bias={m['phaseflip']/m['bitflip']:.2e}"
    print(f"{nbar:5.1f} {s(m28):>22} {s(m40):>22}")

# --- (b) the guard CATCHES my old failure: the modified dissipator J=(a^2-n)+t*a
print("\n(b) the case that fooled me  J = (a^2 - 3) + t*a  :  does a clean qubit even exist?")
print(f"{'t':>6} {'N=20 valid (gap)':>26} {'N=34 valid (gap)':>26}")
for t in [0.0,0.5,1.0,1.5,2.0]:
    a20,_=fock_ops(20); a34,_=fock_ops(34)
    J20=a20@a20-3*np.eye(20)+t*a20; J34=a34@a34-3*np.eye(34)+t*a34
    m20=logical_metric(J20,20); m34=logical_metric(J34,34)
    print(f"{t:6.2f} {str(m20['valid'])+f' ({m20['gap_ratio']:.1f})':>26} "
          f"{str(m34['valid'])+f' ({m34['gap_ratio']:.1f})':>26}")
