# QC-Accelerate v2 — DRAFT (strategy-room, for framing sign-off)
## AI is already accelerating quantum computing — including learning *where to push*

> **DRAFT STATUS.** Combined Phase A + Phase B writeup for review *before* anything touches
> `paper.html` / `manuscript.tex`. Claim labels in **[brackets]** follow project convention
> (CITE / OPEN-CAVEATED / NEGATIVE-KEPT / FORECAST). Figures: `gate_metric_validation.png`,
> `phase_b_negative.png`, `phase_b_frontier_map.png`.

---

## 1. The receipts: AI is already a co-author of quantum computing

A quantum computer is the most error-prone machine humanity has ever tried to build, and
the thing increasingly keeping it on the rails is AI — not someday, *now*. Walk up the stack
and AI is on every floor.

- **The error-spotter.** When a quantum computer slips, it shows not the mistake but a faint
  pattern of "smoke-alarm" clicks; something must infer, in real time, what broke. Google's
  **AlphaQubit** — a transformer, the architecture under large language models — learned to
  read those patterns and beat the best hand-built surface-code decoders on real Sycamore
  hardware (~6% / ~30% fewer errors; Nature 2024). It is AlphaFold's trick pointed at quantum
  errors. **[CITE]**
- **The code-inventor.** AI isn't just running human blueprints, it's drawing new ones.
  Reinforcement learning, set loose on how to hide a qubit in light, found a genuinely odd
  recipe — store it in "two photons or four photons" — that humans hadn't picked, and it
  surpasses the break-even point; a Nov-2025 successor discovers codes resisting two kinds of
  photon loss at once. **[CITE]**
- **The gate-choreographer.** Deep RL and optimal control design the pulses that flip qubits
  without waking errors (transmon control; the numerically-optimised pulses behind cats' first
  universal control; physics-informed neural-network gate design, 2025). **[CITE]**
- **The hardware's reflexes.** AI reaches into the chip — discovering the engineered
  dissipation that lets a qubit self-heal, while industry builds differentiable digital twins
  of their devices (Alice & Bob, APS March Meeting 2026). **[CITE]**

You can no longer sketch the quantum-computing stack without AI showing up at every layer.
The field crossed, almost without anyone announcing it, from *"can AI help?"* to *"AI is
already helping, everywhere."*

---

## 2. The capability this work adds: AI that *scopes* the frontier

AI contributes to quantum computing in three distinct modes. Two are widely celebrated:
**re-deriving/optimising** what humans designed (faster pulses, better decoders) and
**discovering** what humans didn't think of (the RL codes above). This work demonstrates the
third, less-celebrated mode: **scoping** — using AI to *map a hardware frontier rigorously*,
certify where human design is already optimal, and identify the open ground worth pushing on.

A kept negative, honestly obtained, is not a failure — it is a **map**. It tells the field
which doors are already shut so effort flows to the ones still open. Below, we scope one
stubborn bottleneck (the cat-qubit gate speed limit) end to end, and the negative we report
is the demonstration: AI searched the frontier to its edge, found human design already sitting
on the optimum, **refused a shortcut that would have faked a win**, and handed back a precise
map plus the next target.

---

## 3. The demonstration — scoping the cat-qubit gate frontier

### 3a. Phase A — the map (and an instrument that can't be fooled)

**Central question.** Can an AI search over gate protocols find a bias-preserving logical gate
valid at a *worse* κ₁/κ₂ (engineered-dissipation-to-loss) ratio than hand-designed adiabatic
schemes — or prove cleanly that it cannot?

**The bottleneck is gates, not encodings. [CITE]** Cat encodings and the bias-preserving
universal set exist (Puri et al. 2020), sidestepping magic-state distillation. The wall is a
*rate tradeoff*: protected gates must be slow; slowness exposes single-photon loss as
phase-flips; this sets a brutal κ₁/κ₂ requirement. The gate *set* is not the wall — the *rate*
is (the Eastin–Knill-for-cats boundary).

**Baseline to beat. [CITE]** Below-threshold needs κ₁/κ₂ ≲ 5×10⁻³ at α²=8; hand-designed optima
sit near 10⁻³ (Gautier 2022); the biggest lever is the squeezed cat, ~1–2 orders (Xu 2022;
demonstrated 22 s bit-flip, Rousseau 2025).

**Prior-art. [OPEN-CAVEATED]** AI-for-gates is mature but aimed elsewhere (transmon/Rydberg/
photonic). Eight adversarial passes — incl. the likely industrial occupant's APS MM2026 roster
— did not find the intersection (AI search on cat-qubit bias-preserving gates at the κ₁/κ₂
frontier). Residual blind spot: non-A&B MM2026 talks, unindexed/industrial work.

**To scope honestly, build an instrument that can't be fooled. [CITE — validated]** Three
conditions, holding *simultaneously* (a conjunction, never a weighted sum — the structural
defence against reward-hacking): (1) logical action, (2) bias survival (bit-flip suppression,
measured by parity), (3) convergence (return to the cat manifold). Validated on the *known*
hand-designed dissipative-cat Z gate — it reproduces exponential bit-flip suppression
(pX: 1.0e-5 → 1.3e-9), linear phase-flip growth, the rate-frontier degradation through
κ₁/κ₂ ≈ 5e-3, and a truncation rail that rejects under-resolved runs. *(Fig.
gate_metric_validation.png.)* Shipped: `verification/gate-metric/`.

### 3b. Phase B — searching the frontier to its edge

**Method. [CITE]** A **max-min** objective (maximise the *worst* normalised margin across the
three conditions) — the conjunction-faithful scalarisation that can never trade bias for
fidelity. Bake-off: differential evolution vs finite-difference L-BFGS agreed exactly — DE is
the workhorse; differentiable-Lindblad would buy speed, not capability.

**Hardened comparison.** The search got richer control than any hand design — two quadratures,
more segments, free gate time — and was *seeded with the hand-designed gate itself*. The
baseline was the *T-optimised* hand-designed gate, across α²=2 and 3.

**Result. [NEGATIVE — KEPT].** The search does not beat hand-design: frontier gain ×1.04
(noise), F-binding, stable under truncation refinement. The hand-designed adiabatic gate at
minimal gate time already sits at the control-space optimum. **The instrument proved itself:**
handed a bias-breaking quadrature for free, the search drove its amplitude to *exactly zero*
and recovered the hand-designed gate — cheating was made worthless, by the optimiser's own
choice. *(Figs. phase_b_negative.png, phase_b_frontier_map.png.)*

**Mapped frontier. [CITE]** Hand-designed tolerable κ₁/κ₂ = {5.17, 3.99, 3.19}×10⁻³ at
α²={2,3,4} (converged truncation), monotone — the quantitative output of the scoping.

**Honest scope.** Single-mode Z(π/2); α²∈{2,3} fully searched, α²=4 baseline-only (compute-
bound); two-quadrature shaping; one validity bar. Not CNOT, not dissipation-schedule shaping,
not large α — the untried axes are named, not hidden.

---

## 4. What the scout found: where AI is *not* yet engaged

Genuine white space is *narrow and shrinking* — itself evidence for the thesis. Even
cross-layer co-design is being born (VarEFTQC co-designs encoding+gates, 2026). Verified-thin
gaps: **AI-shaped *time-dependent* dissipation** (everything is static-jumps + shaped-
Hamiltonian); **AI dissipation for *gates*, not codes**; and **AI as adversarial *referee***
(almost all AI optimises; few use AI to *break* protection claims — the mode our instrument
embodies). Candidate (un-cleared): AI discovering *new confinement physics*; end-to-end
biased-noise stack co-design; closed-loop AI on real cat hardware.

---

## 5. Next — the natural v3

The limit is a conjunction (gate must be slow AND slowness exposes loss). Our search broke
neither clause because it only tuned the *drive*. The sharpest, most AI-native move — and the
one the scout's map points straight at — is to change the *object* AI designs: **let AI design
the stabilisation, not the pulse.** AI search over the *gate dissipator* and a learned
*time-dependent squeezing schedule* both run on the instrument we already shipped, by swapping
the search variable from the drive to the jumps. **[FORECAST — v3]**

---

## Honesty ledger (proposed updates)

- **[CITE]** κ₁/κ₂ baselines (Puri 2020; Gautier 2022; Xu 2022; Rousseau 2025); AI-stack
  receipts (AlphaQubit Nature 2024; RL-AQEC Zeng 2022 / arXiv:2511.12482).
- **[OPEN-CAVEATED]** AI-on-cat-gate-κ₁/κ₂ intersection unfound across 8 passes incl. APS
  MM2026; residual = non-A&B MM2026 + unindexed/industrial.
- **[NEGATIVE — KEPT]** Two-quadrature seeded search does not beat T-optimised hand-design for
  single-mode Z(π/2) at α²∈{2,3}; search recovers hand-design and zeros the bias-breaking
  quadrature. *(Replaces the prior FORECAST row.)*
- **[CITE]** Frontier map κ₁/κ₂ = {5.17,3.99,3.19}e-3 at α²={2,3,4}.
- **[FORECAST — v3]** "Design the dissipation, not the pulse" as the next target.
