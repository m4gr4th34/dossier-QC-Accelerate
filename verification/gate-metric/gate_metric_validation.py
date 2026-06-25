"""
gate_metric_validation.py
=========================
Phase A instrument validation for the QC-Accelerate v2 protection-preserving
gate metric.

Purpose (NOT a search): run a *known*, hand-designed bias-preserving gate
(the dissipative-cat Z(theta) rotation) through the three-condition metric and
confirm the metric reproduces textbook cat physics BEFORE any AI search is
allowed to optimize against it. This is the "establish the measurement on known
physics first" discipline (cf. the v1.0 floor-sim).

Three conditions measured, each by a structurally independent operator on a
pure-NumPy/SciPy Lindblad evolution:
  (1) Logical action  F_logical   -- realized vs loss-free (kappa1=0) target
  (2) Bias survival   B = pZ/pX    -- Pauli error rates from the logical PTM
  (3) Convergence     L (leakage)  -- 1 - Tr(Pi_code rho), after restab tail

Physics:
  drho/dt = -i[H,rho] + kappa2 D[a^2 - alpha^2] rho + kappa1 D[a] rho
  Code space: span{|alpha>, |-alpha>} ~ span{|C+>, |C->}.
  Z(theta) generator: H = eps (a + a^dag)  (opposite energy on |+-alpha>).
  Single-photon loss a -> parity jump -> phase-flip (Z) error; bit-flip (X)
  error is exponentially suppressed in |alpha|^2.

No quantum libraries used. numpy + scipy only.
"""

import numpy as np
from scipy.linalg import expm

# ---------- Fock-space operators ----------

def fock_ops(N):
    a = np.diag(np.sqrt(np.arange(1, N)), 1).astype(complex)
    ad = a.conj().T
    n = ad @ a
    parity = np.diag((-1.0) ** np.arange(N)).astype(complex)
    I = np.eye(N, dtype=complex)
    return a, ad, n, parity, I

def coherent(alpha, N):
    """Coherent state |alpha> in Fock basis, stable recursion."""
    c = np.zeros(N, dtype=complex)
    c[0] = np.exp(-0.5 * abs(alpha) ** 2)
    for k in range(1, N):
        c[k] = c[k - 1] * alpha / np.sqrt(k)
    c /= np.linalg.norm(c)
    return c

def logical_isometry(alpha, N):
    """Orthonormal logical basis from {|alpha>,|-alpha>} via even/odd cats.
    Returns W (N x 2): columns |0_L>,|1_L> with |0_L>~|alpha>, |1_L>~|-alpha>."""
    plus = coherent(alpha, N)
    minus = coherent(-alpha, N)
    # even/odd cats are exactly orthogonal (parity eigenstates)
    cat_e = plus + minus
    cat_o = plus - minus
    cat_e /= np.linalg.norm(cat_e)
    cat_o /= np.linalg.norm(cat_o)
    # computational basis |0_L> = (|C+>+|C->)/sqrt2 ~ |alpha>, |1_L> ~ |-alpha>
    zeroL = (cat_e + cat_o) / np.sqrt(2)
    oneL = (cat_e - cat_o) / np.sqrt(2)
    zeroL /= np.linalg.norm(zeroL)
    oneL /= np.linalg.norm(oneL)
    W = np.column_stack([zeroL, oneL])
    return W

# ---------- Liouvillian (column-stacking vec convention) ----------
# vec(A rho B) = (B^T kron A) vec(rho)

def liouvillian(H, jumps, N):
    I = np.eye(N, dtype=complex)
    L = -1j * (np.kron(I, H) - np.kron(H.T, I))
    for c in jumps:
        cdc = c.conj().T @ c
        L += np.kron(c.conj(), c)
        L += -0.5 * np.kron(I, cdc)
        L += -0.5 * np.kron(cdc.T, I)
    return L

def propagator(L, T):
    return expm(L * T)

def apply_super(P, rho):
    N = rho.shape[0]
    return (P @ rho.reshape(-1, order="F")).reshape(N, N, order="F")

# ---------- Pauli / PTM machinery ----------

PAULI = {
    "I": np.array([[1, 0], [0, 1]], dtype=complex),
    "X": np.array([[0, 1], [1, 0]], dtype=complex),
    "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "Z": np.array([[1, 0], [0, -1]], dtype=complex),
}
PLABELS = ["I", "X", "Y", "Z"]

def logical_channel_ptm(P_evolve, W, restab=None):
    """Pauli transfer matrix (4x4, real) of encode->evolve->(restab)->decode."""
    R = np.zeros((4, 4), dtype=float)
    for j, pj in enumerate(PLABELS):
        rho_phys = W @ PAULI[pj] @ W.conj().T          # lift logical Pauli
        rho_phys = apply_super(P_evolve, rho_phys)     # gate
        if restab is not None:
            rho_phys = apply_super(restab, rho_phys)   # re-stabilization tail
        rho_log = W.conj().T @ rho_phys @ W            # project + decode
        for i, pi in enumerate(PLABELS):
            R[i, j] = np.real(np.trace(PAULI[pi] @ rho_log)) / 2.0
    return R

def pauli_error_rates(R_real, R_ideal):
    """Error channel = realized o ideal^{-1}; return Pauli-twirled p_I,pX,pY,pZ."""
    R_err = R_real @ np.linalg.inv(R_ideal)
    # Pauli-twirl: diagonal of error PTM gives Pauli channel fidelities
    d = np.clip(np.real(np.diag(R_err)), -1.0, 1.0)  # [rII, rXX, rYY, rZZ]
    rI, rX, rY, rZ = d
    pI = 0.25 * (rI + rX + rY + rZ)
    pX = 0.25 * (rI + rX - rY - rZ)
    pY = 0.25 * (rI - rX + rY - rZ)
    pZ = 0.25 * (rI - rX - rY + rZ)
    return pI, pX, pY, pZ

# ---------- The three-condition metric ----------

def measure_gate(alpha, kappa1, kappa2, eps, T, N=None, tail_factor=4.0):
    if N is None:
        N = int(np.ceil(abs(alpha) ** 2 + 8 * abs(alpha) + 12))
    a, ad, n, parity, I = fock_ops(N)
    W = logical_isometry(alpha, N)
    Pi_code = W @ W.conj().T

    H_gate = eps * (a + ad)                  # Z(theta) generator
    L2 = np.sqrt(kappa2) * (a @ a - (alpha ** 2) * I)

    # realized gate (with loss) and loss-free target (kappa1 = 0)
    jumps_real = [L2, np.sqrt(kappa1) * a]
    jumps_ideal = [L2]
    P_real = propagator(liouvillian(H_gate, jumps_real, N), T)
    P_ideal = propagator(liouvillian(H_gate, jumps_ideal, N), T)

    # re-stabilization tail: dissipation only, gate off
    restab_real = propagator(liouvillian(0 * H_gate, jumps_real, N), tail_factor / kappa2)
    restab_ideal = propagator(liouvillian(0 * H_gate, jumps_ideal, N), tail_factor / kappa2)

    R_real = logical_channel_ptm(P_real, W, restab_real)
    R_ideal = logical_channel_ptm(P_ideal, W, restab_ideal)

    pI, pX, pY, pZ = pauli_error_rates(R_real, R_ideal)
    # guard tiny negatives from numerical noise
    pX, pY, pZ = max(pX, 0.0), max(pY, 0.0), max(pZ, 0.0)

    # F_logical: average logical-state fidelity realized vs ideal over 6 cardinals
    F = avg_logical_fidelity(P_real, P_ideal, W, restab_real, restab_ideal)

    # Leakage: peak (pre-tail, sees non-adiabaticity) and residual (post-tail)
    leak_peak, leak_resid = leakage(P_real, W, Pi_code, restab_real)

    bias = pZ / pX if pX > 0 else np.inf
    # theta read from the clean loss-free channel, not the damped lossy one
    return dict(N=N, F=F, pX=pX, pY=pY, pZ=pZ, bias=bias,
                leak_peak=leak_peak, leak_resid=leak_resid,
                theta=realized_theta(R_ideal))

def realized_theta(R):
    """Recover the realized Z-rotation angle from the PTM action on X,Y block."""
    # Z(theta): X->cosX - sinY ; Y-> sinX + cosY
    c = R[1, 1]; s = R[2, 1]
    return np.degrees(np.arctan2(s, c))

def cardinal_states():
    s = {}
    s["0"] = np.array([[1, 0], [0, 0]], dtype=complex)
    s["1"] = np.array([[0, 0], [0, 1]], dtype=complex)
    s["+"] = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)
    s["-"] = 0.5 * np.array([[1, -1], [-1, 1]], dtype=complex)
    s["+i"] = 0.5 * np.array([[1, -1j], [1j, 1]], dtype=complex)
    s["-i"] = 0.5 * np.array([[1, 1j], [-1j, 1]], dtype=complex)
    return s

def _decode(P, rho_phys, W, restab):
    rho_phys = apply_super(P, rho_phys)
    if restab is not None:
        rho_phys = apply_super(restab, rho_phys)
    rho_log = W.conj().T @ rho_phys @ W
    tr = np.real(np.trace(rho_log))
    return rho_log / tr if tr > 0 else rho_log

def avg_logical_fidelity(P_real, P_ideal, W, restab_real, restab_ideal):
    fids = []
    for rho_L in cardinal_states().values():
        rho_phys = W @ rho_L @ W.conj().T
        r = _decode(P_real, rho_phys, W, restab_real)
        i = _decode(P_ideal, rho_phys, W, restab_ideal)
        # state fidelity for qubit density matrices
        fids.append(state_fidelity(r, i))
    return float(np.mean(fids))

def state_fidelity(rho, sigma):
    # qubit fidelity F = Tr[rho sigma] + 2 sqrt(det rho det sigma)
    rho = (rho + rho.conj().T) / 2
    sigma = (sigma + sigma.conj().T) / 2
    val = np.real(np.trace(rho @ sigma) +
                  2 * np.sqrt(max(np.real(np.linalg.det(rho)), 0) *
                              max(np.real(np.linalg.det(sigma)), 0)))
    return float(np.clip(val, 0.0, 1.0))

def leakage(P_real, W, Pi_code, restab):
    """Return (peak pre-tail leakage, residual post-tail leakage)."""
    peak, resid = [], []
    for rho_L in cardinal_states().values():
        rho_phys = W @ rho_L @ W.conj().T
        rho_gate = apply_super(P_real, rho_phys)             # right after gate
        peak.append(1 - np.real(np.trace(Pi_code @ rho_gate)))
        rho_tail = apply_super(restab, rho_gate)             # after restab tail
        resid.append(1 - np.real(np.trace(Pi_code @ rho_tail)))
    return float(np.mean(peak)), float(np.mean(resid))


if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True)
    kappa2 = 1.0
    eps = 0.05 * kappa2         # weak drive -> Zeno/adiabatic Z gate
    T = 30.0 / kappa2           # slow gate (adiabatic regime)

    print("=" * 74)
    print("INSTRUMENT VALIDATION  -- dissipative cat Z-gate through 3-cond metric")
    print("=" * 74)

    print("\n[A] BIAS SCALING: bit-flip suppression & bias growth vs alpha^2")
    print("    (known physics: pX falls ~exp in alpha^2; bias B = pZ/pX rises)")
    print(f"    {'alpha^2':>8} {'N':>4} {'pX':>12} {'pZ':>12} {'log10(B)':>9} {'leak_res':>10}")
    for a2 in [2, 3, 4, 5]:
        r = measure_gate(np.sqrt(a2), kappa1=1e-3 * kappa2,
                         kappa2=kappa2, eps=eps, T=T)
        logB = np.log10(r["bias"]) if np.isfinite(r["bias"]) else np.inf
        print(f"    {a2:>8} {r['N']:>4} {r['pX']:>12.3e} {r['pZ']:>12.3e}"
              f" {logB:>9.2f} {r['leak_resid']:>10.2e}")

    print("\n[B] RATE FRONTIER: phase-flip vs noise ratio kappa1/kappa2")
    print("    (known physics: pZ ~ linear in kappa1; validity degrades as ratio worsens)")
    print(f"    {'k1/k2':>10} {'F_logical':>10} {'pZ':>12} {'log10(B)':>9} {'leak_res':>10}")
    for ratio in [1e-4, 1e-3, 5e-3, 1e-2, 3e-2]:
        r = measure_gate(np.sqrt(4.0), kappa1=ratio * kappa2,
                         kappa2=kappa2, eps=eps, T=T)
        logB = np.log10(r["bias"]) if np.isfinite(r["bias"]) else np.inf
        print(f"    {ratio:>10.0e} {r['F']:>10.5f} {r['pZ']:>12.3e}"
              f" {logB:>9.2f} {r['leak_resid']:>10.2e}")

    print("\n[C] NON-ADIABATIC LEAKAGE: gate speed vs convergence")
    print("    (known physics: faster gate / stronger drive -> more PEAK leakage)")
    print(f"    {'eps/k2':>8} {'T*k2':>6} {'F_logical':>10} {'leak_peak':>11} {'leak_res':>10}")
    for epsr, Tr in [(0.02, 60), (0.05, 30), (0.10, 15), (0.20, 8), (0.40, 4)]:
        r = measure_gate(np.sqrt(4.0), kappa1=1e-3, kappa2=kappa2,
                         eps=epsr * kappa2, T=Tr / kappa2)
        print(f"    {epsr:>8.2f} {Tr:>6} {r['F']:>10.5f}"
              f" {r['leak_peak']:>11.2e} {r['leak_resid']:>10.2e}")

    print("\n[D] TRUNCATION ROBUSTNESS RAIL: B, leak vs Fock cutoff N")
    print("    (rail: reported rates must converge across truncations)")
    print(f"    {'N':>4} {'pX':>12} {'pZ':>12} {'log10(B)':>9} {'leak_res':>10}")
    for Nfix in [16, 20, 24, 30]:
        r = measure_gate(np.sqrt(4.0), kappa1=1e-3, kappa2=kappa2,
                         eps=eps, T=T, N=Nfix)
        logB = np.log10(r["bias"]) if np.isfinite(r["bias"]) else np.inf
        print(f"    {Nfix:>4} {r['pX']:>12.3e} {r['pZ']:>12.3e}"
              f" {logB:>9.2f} {r['leak_resid']:>10.2e}")
    print("\nDONE.")
