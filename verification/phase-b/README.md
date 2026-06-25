# Phase B — AI search over cat-qubit gate protocols (kept negative)

Searches gate protocols on the Phase-A-validated three-condition metric, asking whether
AI can find a bias-preserving Z(pi/2) gate valid at a worse kappa1/kappa2 than the
T-optimized hand-designed gate. Objective is MAX-MIN over the three conditions (conjunction-
faithful; cannot trade bias for fidelity). Arms: differential evolution (workhorse) and
finite-difference L-BFGS (agreed exactly).

RESULT (kept negative): with two-quadrature control, more segments, and seeded with the
hand-designed gate, the search does NOT beat hand-design (frontier gain x1.04, F-binding,
truncation-stable at alpha^2 in {2,3}). Handed a bias-breaking quadrature for free, the
search drove it to exactly zero and recovered hand-design -- the un-gameable metric made
cheating worthless. Frontier map: tolerable kappa1/kappa2 = {5.17, 3.99, 3.19}e-3 at
alpha^2 = {2,3,4} (converged truncation).

Scope: single-mode Z(pi/2); alpha^2 in {2,3} fully searched, alpha^2=4 baseline-only
(compute-bound at honest N); two-quadrature shaping; one validity bar. Not CNOT, not
dissipation-schedule shaping, not large alpha.

Run: `python phase_b_search.py "[(2,12,18,15,8)]"` reproduces the alpha^2=2 verdict.
Figures (regenerated, not committed -- same convention as floor-sim/gate-metric):
`python make_figure_phaseb.py` and `python make_frontier_map.py`.
NOTE: the two figure scripts plot recorded run values; phase_b_search.py reproduces them.
