import numpy as np

def fock_ops(N):
    """Annihilation a and identity in an N-level Fock space."""
    a = np.diag(np.sqrt(np.arange(1, N)), 1)   # a|n> = sqrt(n)|n-1>
    I = np.eye(N)
    return a, I

def dissipator_super(C):
    """Superoperator for D[C]rho = C rho C^dag - 1/2{C^dag C, rho}.
    Column-stacking convention: vec(A rho B) = (B^T kron A) vec(rho).
    Spectrum is convention-independent."""
    Cd = C.conj().T
    CdC = Cd @ C
    N = C.shape[0]
    I = np.eye(N)
    term1 = np.kron(C.conj(), C)                # C rho C^dag
    term2 = 0.5 * np.kron(I, CdC)               # 1/2 C^dag C rho
    term3 = 0.5 * np.kron(CdC.T, I)             # 1/2 rho C^dag C
    return term1 - term2 - term3

def liouvillian(N, alpha2, k2=1.0, k1=0.0, H=None):
    """L = k2 D[a^2 - alpha2] + k1 D[a]  (+ -i[H,.] if H given)."""
    a, I = fock_ops(N)
    L2 = a @ a - alpha2 * I
    L = k2 * dissipator_super(L2)
    if k1 != 0.0:
        L = L + k1 * dissipator_super(a)
    if H is not None:
        L = L + (-1j) * (np.kron(I, H) - np.kron(H.T, I))
    return L

def spectrum(L):
    ev = np.linalg.eigvals(L)
    # sort by real part descending (closest to 0 first)
    return ev[np.argsort(-ev.real)]

if __name__ == "__main__":
    N = 30
    for alpha2 in [2.0, 3.0, 4.0]:
        L = liouvillian(N, alpha2, k2=1.0, k1=0.0)
        ev = spectrum(L)
        near0 = np.sum(np.abs(ev.real) < 1e-6)
        gap = -ev.real[near0]  # first clearly-nonzero decay rate
        print(f"alpha^2={alpha2}: #(|Re|<1e-6)={near0}, "
              f"top5 Re={np.round(ev.real[:6],8)}, dissipative gap~{gap:.4f}")
