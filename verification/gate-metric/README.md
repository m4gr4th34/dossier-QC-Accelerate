# Gate-metric instrument (Phase A validation)

Validates the v2 protection-preserving gate metric on a KNOWN, hand-designed
dissipative-cat Z(theta) gate BEFORE any AI search optimizes against it
("establish the measurement on known physics first" — cf. floor-sim).

Three conditions, each measured by a structurally independent operator on a
pure-NumPy/SciPy Lindblad evolution (no quantum libraries):
  (1) logical action  F_logical  — realized vs loss-free (kappa1=0) target
  (2) bias survival   B = pZ/pX   — Pauli error rates from the logical PTM
  (3) convergence     leak_peak (pre-tail, sees non-adiabaticity) + leak_resid

Validated behaviour (run `python gate_metric_validation.py`):
  - bit-flip pX falls ~exponentially in |alpha|^2 (1.0e-5 -> 1.3e-9 over a2=2..5)
  - phase-flip pZ ~ linear in kappa1 * |alpha|^2 * T; bias B spans 3.8..8.0 decades
  - rate frontier degrades through kappa1/kappa2 ~ 5e-3 (F: 0.999 -> 0.835)
  - peak leakage rises monotonically with drive strength (non-adiabaticity)
  - TRUNCATION RAIL: N<=20 rejected as under-resolved (pX underflows); N>=24 converged

Figure: `python make_figure.py` regenerates gate_metric_validation.png
(left: bias by parity; right: the adiabatic tradeoff the search must navigate).

NOTE: this is an INSTRUMENT, not a search. No novelty/physics is claimed here.
