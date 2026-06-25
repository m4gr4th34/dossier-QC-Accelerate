# QC-Accelerate v2 — AI Is Already Accelerating Quantum Computing
### (and where the next contribution points)

*The thrust of this project is that AI and large-scale computation are accelerating
the road to real quantum hardware. Our own result this round is one honest brick in
that wall. This document first shows how much AI is ALREADY doing across the field —
then couches each next-step avenue as "AI is already here; here is the next move."
Every "open" item names its residual blind spot. Nothing here is a novelty claim.*

---

## Part 1 — The receipts: AI is already a co-author of quantum computing

A quantum computer is the most error-prone machine humanity has tried to build. The
thing increasingly keeping it on the rails is AI — not someday, now. Across every
layer of the stack, AI has gone from "could it help?" to "it already did."

**The error-spotter — AlphaQubit.** When a quantum computer makes a mistake, it doesn't
show you the mistake; it shows you a faint pattern of "smoke-alarm" clicks, and someone
has to infer what actually went wrong, fast. Google DeepMind + Google Quantum AI trained
a transformer (the same architecture under large language models) to read those patterns.
It beat the best hand-built decoders — ~6% fewer errors than the slow-but-accurate method,
~30% fewer than the practical one — on real hardware (Nature, 2024). It is, almost exactly,
AlphaFold's trick pointed at quantum errors.

**The code-inventor.** Even more striking: AI isn't just running human blueprints, it's
drawing new ones. Turned loose on how to store a qubit in light, reinforcement learning
found a genuinely odd recipe — encode the information in "two photons or four photons" —
that humans hadn't picked, and it beats the break-even point for error correction
(Zeng et al., 2022/2023). Three weeks before this writing, a deeper version discovered
codes that survive *two* kinds of photon loss at once (arXiv:2511.12482, Nov 2025).

**The gate-choreographer.** Flipping a qubit without waking its errors is a control
problem, and AI has been solving it for years — deep reinforcement learning designing
control pulses for superconducting qubits (Niu et al. 2019; Baum et al. 2021; Porotti
et al. 2023), and the numerically-optimized pulses that gave cat qubits their first
universal control. Newer work even uses physics-informed neural networks to design
gates directly from the equations of open-system dynamics (arXiv:2511.09463, 2025).

**The hardware's reflexes.** AI is reaching into the chip itself — discovering the
"engineered dissipation" that lets a qubit quietly self-heal (the same RL-for-codes
work above), while industry builds differentiable digital twins of their devices to
extract parameters automatically (Alice & Bob, APS March Meeting 2026).

**Our brick.** And us: we pointed an AI search at one stubborn knob — the speed limit
on cat-qubit logical gates — gave it richer controls than any human design, let it
search hard, and it honestly came back: *the humans already nailed this one.* It even
declined a tempting shortcut that would have cheated the metric. That's not a failure;
that's the system working. We came away with a precise map of where the wall actually
is, and a validated instrument to test the next idea. Real acceleration includes the
honest "no" — it tells you which doors are already shut so you stop pushing on them.

**The punchline for a general reader:** you can no longer sketch the quantum-computing
stack without AI showing up at every floor — spotting errors, inventing codes,
choreographing gates, designing the hardware's reflexes. The field quietly crossed from
"can AI help build a quantum computer?" to "AI is already helping, everywhere."

---

## Part 2 — Where the next AI contribution points (avenues, couched as "already here → next")

The limit our search hit is a *conjunction*: a cat-qubit gate must be slow, **and**
slowness exposes photon loss as error. You don't beat a conjunction by tuning the drive
(we tried — that box is solved). You change the *object* AI designs. Conveniently, AI is
already moving on each of these objects; the open part is pointing it at the gate-speed
frontier specifically.

### Tier 1 — open, AI-native, buildable on the instrument we already validated

**A2 — Let AI design the dissipation, not the pulse.**
*Already here:* AI designs engineered dissipation to discover error-correction codes
(Zeng et al.; arXiv:2511.12482); hand-designed dissipation (the "squeezed cat") is the
single biggest known lever, ~1–2 orders of magnitude on the κ₁/κ₂ ratio (arXiv:2210.13406;
demonstrated, 22 s bit-flip time, arXiv:2502.07892).
*Next move (OPEN-CAVEATED):* AI search over the *gate* dissipation for fast, bias-preserving
operations — the codes are taken, the gates are not. Drops straight onto our metric (swap
the search variable from the drive to the jump operators).

**A7 — Let AI choreograph *time-dependent* squeezing, synced to the gate.**
*Already here:* static squeezing is demonstrated and a big win (above).
*Next move (OPEN-CAVEATED):* a learned schedule s(t) that squeezes the vulnerable quadrature
exactly when the gate is exposed — static squeezing is occupied, the schedule is not.
Buildable on our metric.

### Tier 2 — open, higher novelty, higher risk

**A5 — Exceptional-point gates.** *Already here:* AI/real-time control drives systems to
non-Hermitian "exceptional points" for robust, one-way state transfer (arXiv:2111.04754;
PRL 128.160401) — on transmons. *Next move (OPEN-CAVEATED):* use it as a bias-preserving
cat logical gate. Testable in our sim; may break bias (that's the experiment).

**A1 — Loss-transparent gates for the dissipative cat.** *Already here:* "error-transparent"
gates are demonstrated for phase gates and just extended toward universal (arXiv:2603.15356,
Apr 2026). *Next move (OCCUPIED — thin sliver):* the cat-specific, bias-preserving, AI-found
version. Easy add to our metric (a fourth condition), but mostly taken.

### Tier 3 — partly occupied, or needs a bigger simulation than our sandbox

**A3 — Native/passive instruction set** (logical gates as free phase-space symmetries;
beam-splitter logical gates in multimode cats). PARTIALLY OCCUPIED — entangling beam-splitter
gates exist (arXiv:2010.08699); a passive bias-preserving *universal* set is open. Needs a
two-mode sim.

**A6 — Critical-point gates** (operate near a dissipative phase transition so a tiny drive
gives a big protected rotation). OCCUPIED as an encoding — the "critical cat code" exists
(arXiv:2208.04928); as a *gate* resource it is open-ish. Add detuning to test.

**A4 — Correct loss *during* the gate** (4-leg cat, Z₄ syndrome — our own C13). OCCUPIED-
CAVEATED — concurrent-correction concepts exist (PReSPA, arXiv:2004.09322) and there is a
known hard wall (parity checks fight continuous stabilisation). Needs a 4-component sim.

**A8 — Floquet-built gate generators** (fast in the rotating frame, stabilised in the lab
frame). OPEN-CAVEATED — Floquet methods already analyse cat stabilisation; gate generators
are the open part; heating is the risk. Needs time-dependent stabilisation.

---

## Bottom line for the DOI update

Two messages, both honest and both on-thesis. **One:** AI is already accelerating quantum
computing at every layer of the stack — decoders, codes, gates, hardware — and we can show
the receipts. **Two:** we added a rigorous brick (a kept negative + a validated instrument),
and it points at the sharpest remaining AI-native target: *let AI design the stabilisation,
not the pulse* (A2 + A7, fused). That is the natural v3, and it runs on the instrument we
already built and shipped.

---

## Part 3 — Where AI has NOT yet been engaged

**The honest headline: genuine white space is *narrow*, and it keeps shrinking — which
is itself the strongest evidence for this project's thesis.** We went looking for big
AI-untouched fields and mostly found AI already arriving. Even cross-layer co-design,
which we expected to be wide open, is being born right now: VarEFTQC jointly learns
encodings *and* logical gate sets in one framework (arXiv:2605.28162, ~1 month old), and
decoder–hardware co-design is active (arXiv:2606.11076). So the real white space is
*specific*, not broad.

**Verified thin (cleared in this sweep):**
- **AI-shaped *time-dependent* dissipation.** Everything AI touches in the bosonic stack
  shapes the *Hamiltonian* over *static* engineered dissipation, or discovers *static*
  codes. A learned, time-varying jump-operator schedule — AI choreographing the
  dissipation itself, moment to moment — is essentially unengaged. Sharpest gap, and
  exactly where our negative points.
- **AI designing dissipation for *gates*, not codes.** AI discovers dissipative
  codes/memory; AI search over the *gate* dissipator at the κ₁/κ₂ frontier is open.
- **AI as adversarial *referee*, not optimizer.** Almost all AI here optimizes (find the
  best gate/code/pulse). Using AI/computation as a *skeptic* — to certify a claimed
  protected operation really keeps its protection under realistic noise, and to actively
  hunt reward-hacks — is rare. Our un-gameable metric is a small instance; the general
  mode (AI that tries to *break* protection claims) is under-used, and it is the mode
  honesty most needs.

**Candidate white space (NOT yet adversarially cleared — flagged honestly):**
- **AI discovering new confinement *physics*.** AI picks *what* to encode, but works
  *within* the three known stabilisation mechanisms (dissipative / Kerr / squeezed). Can
  AI discover a *qualitatively new* confining Lindbladian? To our knowledge untested.
- **End-to-end co-design of the *biased-noise* stack.** Generic encoding+gate co-design
  is emerging; the cat-specific chain (bosonic confinement → bias-preserving gates →
  outer repetition/LDPC code → decoder) co-optimised end-to-end is thinner.
- **Closed-loop AI on the *real* cat device.** Most cat AI lives in simulation;
  hardware-in-the-loop tuning of the actual dissipative-cat chip is rare.

**Takeaway (pairs with Part 1):** AI has saturated the quantum-computing stack so fast
that finding honest white space now takes real effort — and the cleanest open ground is
"let AI shape the dissipation, *in time*," which is exactly where our result sends us.
