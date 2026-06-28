An Open Dossier · **QC-Accelerate** · working draft · June 2026

# Accelerating Quantum Computing Research Using AI and Robotics

*Irfan Ali-Khan — Independent Researcher*

AI has quietly become a co-author of quantum-computing research — it spots the errors, invents the codes, and choreographs the gates. Chapter 1 of this dossier established the *floor*: a cat qubit the physics protects on its own, with bit-flip errors crushed exponentially as the cat grows. This chapter asks the next question — can you *operate* on that protected qubit, running a logic gate, without breaking the protection? We use it to demonstrate a third thing AI can do, past re-deriving and discovering: **scoping** a hardware frontier honestly. We build a gate scorecard that cannot be reward-hacked, validate it against known physics, then turn an AI search loose with more freedom than any human design — and seeded from the best human gate. It returns a clean, rigorous negative: the hand-designed bias-preserving gate already sits at the optimum of this control space, and handed a bias-breaking shortcut, the search drove it to zero on its own. A kept “no” is a map — it marks which doors are shut and points to the open ground: letting AI shape the engineered dissipation itself, in time.

## Avenues

| Avenue | Thesis | Status | Forecast | Sources |
|---|---|---|---|---|
| Engineering layer — make today's machine better | AI decoders and below-threshold surface codes improve the qubits we already have, without changing what they're made of. | ESTABLISHED | — | AQ, BT |
| Designed qubits — search the hardware space | Let AI design the qubit's circuit or screen new materials and molecules: a different qubit, not a better-tuned one. An optimiser rediscovered fluxonium from a blank circuit. | REPORTED | — | SQ, DEF, MOL |
| Self-correcting matter — passive storage | Store a qubit in a material whose global structure resists noise on its own. A 3D self-correcting memory is claimed, but key stability and fabrication questions stay open. | OPEN-UNVERIFIED | — | SCM |
| The floor — a qubit that heals itself | Engineer the equation of motion so the qubit is a self-healing steady state. A from-first-principles cat-qubit simulation shows exponential noise bias; a Knill-Laflamme proof shows the four-component cat makes single-photon loss a correctable Z4 syndrome (k=4 minimal). Whether a search can discover such codes unaided is open. | FORECAST | ~55% by first automated discovery of a loss-correcting bosonic code beyond the cat family, peer-reviewed and reproduced, by 2031 | AQEC, MIR, RLQEC, RLBOS |

## Consistency checks

Results from `verification/verify_numbers.py` — the same checks the in-page console runs; CI reruns them on every commit.

- [PASS] Consistency: at least one avenue in the landscape
- [PASS] Consistency: every FORECAST has a dated signpost
- [PASS] Consistency: all forecast probabilities lie in [0,100]

**TOTAL: 3 checks · 3 pass · 0 fail** — All checks pass — the survey is internally consistent.

## 1 AI is already a co-author of quantum computing research

A qubit (The quantum version of a bit. A normal bit is 0 or 1; a qubit can be a blend of both at once — and that blend is so delicate that almost anything can destroy it.) is the most error-prone object humanity has ever tried to compute with — and increasingly, the thing keeping it on the rails is AI. Not someday. Now. Walk up the stack and AI is on every floor.

**It spots the errors.** When a quantum computer slips, it doesn't show you the mistake — it shows a faint pattern of smoke-alarm clicks (The cross-check measurements an error-correcting code spits out. They don't reveal the stored information (that would destroy it) — they reveal a shadow of what went wrong, which a 'decoder' must then interpret.), and something has to infer, in real time, what actually broke. Google trained a transformer (The neural-network architecture behind today's large language models. It turns out the same machinery that predicts the next word is good at reading the correlated pattern of error signals off a quantum chip.) to read those patterns; their AlphaQubit decoder beat the best hand-built methods on real hardware [Nature '24]. It is, almost exactly, AlphaFold's trick pointed at quantum errors.

**It invents the error-correction codes.** More striking: AI isn't only running human blueprints, it's drawing new ones. Set loose on how to hide a qubit inside light, reinforcement learning found a genuinely odd recipe — store the information in "two photons or four photons" — that humans hadn't picked, and it beats the break-even point for error correction [RL-code '23]. A 2025 successor discovered codes that survive two kinds of photon loss at once [bosonic-RL '25].

**It choreographs the gates.** Flipping a qubit without waking its errors is a control problem, and AI has been quietly solving it for years — deep reinforcement learning designing the control pulses for superconducting qubits, and the numerically-optimized pulses behind early universal control of cat qubits.

**It designs the hardware's reflexes.** AI now reaches into the chip itself — discovering the engineered dissipation (Deliberately sculpted energy leaks that, instead of causing errors, constantly pump a qubit back into its correct state. The usual enemy, decoherence, turned into the janitor.) that lets a qubit self-heal — while industry builds differentiable digital twins of their devices to read out chip parameters automatically.

*You can no longer sketch the quantum-computing stack without AI on every layer. The field crossed, almost without anyone announcing it, from "can AI help build a quantum computer?" to "AI is already helping, everywhere."*

## 2 Three ways AI helps — and the one this dossier adds

AI helps quantum computing in three distinct ways. Two are famous: **re-deriving** what humans designed (faster pulses, better decoders) and **discovering** what humans didn't (the codes above). This dossier demonstrates the third, quieter one: **scoping** — using AI to map a hardware frontier rigorously, certify where human design is already optimal, and point to the open ground worth pushing on.

The idea runs against intuition: a careful *"no"* is one of the most useful things a search can produce. An honestly-obtained negative is a **map** — it tells the field which doors are already shut, so effort flows to the ones still open.

*We re-derive and we discover. This is the third thing: we scope — and a kept "no" is a map of where to push.*

## 3 The bottleneck we scoped: operating a protected qubit

Chapter 1 of this dossier [v1.0] established the *floor*: a cat qubit (A qubit encoded in two mirror-image states of a microwave oscillator, named after Schrödinger's cat. Make the 'cat' bigger and one whole type of error (the bit-flip) vanishes exponentially — so its noise is extremely lopsided, or 'biased'.) the physics protects on its own, with bit-flip errors crushed exponentially as the cat grows [Mirrahimi '14]. That gives you a superb place to *store* a qubit. This edition asks the next question: can you *operate* on it — run a logic gate — without breaking the protection?

The trouble is a rate. A bias-preserving gate (A gate that does its job without spoiling the qubit's lopsided (biased) noise — bit-flips must stay rare even mid-operation, or the whole hardware-efficiency advantage collapses.) has to be run adiabatically (Slowly and smoothly, so the qubit is gently guided and never knocked out of its protected manifold. The price of gentleness is time — and time is exactly when ordinary photon loss accumulates.) to stay protected; but slowness gives ordinary photon loss time to pile up as phase errors. The result is a brutal requirement on one ratio: the engineered, protective dissipation versus the unavoidable loss — written κ₁/κ₂ (κ₂ is the rate of the 'good' engineered two-photon dissipation that protects the cat; κ₁ is the rate of 'bad' single-photon loss. The whole question is how large a κ₁/κ₂ (how much bad relative to good) a working gate can tolerate. Smaller is easier; the frontier is how far up you can push it.). Hand-designed gates have fought this ratio for years; the natural question for an AI is whether a smarter search can tolerate a *worse* ratio than the best human design — or prove cleanly that it can't.

*The wall isn't whether the gate exists. It's the rate it must run at to stay protected — and that rate is the thing to beat.*

## 4 An instrument that can't be fooled

v1.0's sharpest lesson was a failure: a naive search once reward-hacked (When an optimiser satisfies the letter of your scoring rule while violating its intent. In v1.0 the search 'improved' a protection score by quietly destroying the qubit it was meant to protect.) its own metric, scoring well by destroying the qubit. So before asking "can AI beat the human gate?", we built a scorecard that *cannot* be gamed — and validated it against gates whose behaviour is already known.

A gate counts only if it passes three checks *at once* — never a weighted average, where a search could trade one away for another: it must (1) actually perform the intended logic, (2) keep the bit-flip protection intact — measured directly by parity (Whether the field holds an even or odd number of photons. A lost photon flips parity, so reading parity is how you catch the error that matters — and it can't be faked by a search the way a lumped error-rate can.), not by a lumpable score — and (3) stay converged inside the protected manifold. We ran the known hand-designed gate through it: the scorecard reproduces textbook cat physics — bit-flips falling off a cliff, phase-flips rising gently, the frontier degrading right where theory says it should — and a built-in resolution check rejects any run whose numbers haven't converged.

*(figure: Validation of the three-condition gate metric: exponential bit-flip suppression on the left, the adiabatic speed-vs-loss tradeoff on the right — The scorecard, validated on a known gate. Left: bit-flip error falls exponentially with cat size while phase-flip stays flat — the protection, measured by parity. Right: the tradeoff the search must navigate — fast gates leak, slow gates accumulate loss.)*

**Verified · in-repo · gate-metric.** The three-condition metric reproduces the known dissipative-cat gate's behaviour from first principles (exponential bit-flip suppression, linear phase-flip, frontier near κ₁/κ₂ ≈ 5×10⁻³), and its truncation rail rejects under-resolved runs. This validates the *measurement* against known physics before any search is allowed to optimise against it. Code: `verification/gate-metric/`.

*You cannot honestly search a frontier with a scorecard that can be cheated. So first we built one that can't — and proved it on physics we already understood.*

## 5 The search, and the result it honestly returned

Then we let an AI search loose with *more* freedom than any human design — two control knobs instead of one, finer pulse shaping, free timing — and, to make the test as hard as possible on ourselves, we *seeded it with the best human gate*, so it started from the human answer and could only try to improve.

It couldn't. Across cat sizes, the search recovered the hand-designed gate and could not push the tolerable κ₁/κ₂ past it (a 4% wobble — noise). The hand-designed adiabatic gate, run as fast as it can go, already sits at the optimum of this control space.

*(figure: Frontier map: tolerable noise ratio versus cat size, with the AI search sitting on top of the hand-designed baseline — The mapped frontier: how bad a noise ratio a working gate tolerates, versus cat size. The AI search (coral) lands on top of the hand-designed baseline (teal) — at α²=2 it recovers the hand-designed result (gain ×1.04, with the bias-breaking quadrature ε_y driven to zero), and at α²=3 it matches it exactly. At α²=4 the search is compute-bound (it needs N≥24 Fock states), so only the baseline is shown. It scopes the wall precisely, but does not move it.)*

The telling part is *how* it failed. We had handed the search a tempting shortcut — a second control knob that could speed the gate up by quietly breaking the bias. A reward-hack would have seized it. Instead, because the scorecard makes bias-breaking worthless, the search drove that knob to *exactly zero* on its own and returned to the honest human gate. The instrument worked: cheating wasn't punished after the fact, it was made pointless, and the optimiser saw that.

*(figure: The hand-designed baseline frontier rising as gate time shortens, with the AI search target above it unreached — The kept negative, in one picture. The hand-designed gate's reachable frontier (teal) rises as the gate runs faster; the dashed line marks the 1.5× target the search would need to clear. The shaped single-quadrature pulse cannot reach it — its best reachable frontier falls below the baseline (margin −0.29), producing no valid gate that beats hand-design at this operating point. A clean “no” — and a precise map of where the wall sits.)*

> **Negative · kept · in-repo · phase-b** — With two-quadrature control, finer shaping, and seeded from the hand-designed gate, an AI search does *not* beat the best hand-designed bias-preserving gate on κ₁/κ₂ (gain ≈ ×1.04; independently reproduced). Handed a bias-breaking degree of freedom, the search set it to exactly zero — the un-gameable scorecard made the shortcut worthless. Scope: single-mode Z(π/2), cat sizes n̄ = 2–3 fully searched, two-quadrature shaping, one validity bar; not yet CNOT, large cats, or dissipation-schedule shaping. A rigorous map and a kept negative — the project's guaranteed floor — not a defeat. Code: `verification/phase-b/`.

*Given more freedom than any human gate, and the human gate as its starting point, the AI's honest answer was: you already have the best one here. That "no" is the result.*

## 6 Where AI has *not* yet been engaged

Having mapped this wall, the natural next move is to ask what the map leaves open — and the honest headline is that genuine white space is *narrow, and shrinking*. We went looking for big AI-untouched fields and mostly found AI already arriving; even joint cross-layer co-design (Designing several layers of the quantum computer together — the code, the gates, the hardware — instead of one at a time. Long an obvious gap; now being filled by AI too.) is being born [co-design '26]. The verified-thin gaps are specific: AI that shapes the engineered dissipation *in time* (everything today is static dissipation with a shaped drive); AI that designs dissipation for *gates* rather than for memory; and AI used as an adversarial *referee* — to certify protection and hunt cheats — rather than only as an optimiser. The last one is the mode this dossier's scorecard embodies, and it is rare.

*AI saturated the stack so fast that honest white space now takes effort to find — and the cleanest open ground is letting AI shape the dissipation itself, in time.*

## 7 What this says about AI

v1.0's most important moment wasn't a result — it was a failure caught: a search reward-hacking its own metric, reported rather than hidden. This edition is the same virtue one level up. There, AI caught itself cheating on a *metric*. Here, given a real frontier and a tempting shortcut, AI *declined* the cheat unprompted, mapped the wall, certified the human design optimal, and pointed at where to push next. Re-deriving and discovering get the headlines; scoping — knowing where the wall is, and saying so — is the quieter capability that makes a search trustworthy.

*The striking part isn't that AI went deep. It's that it knew where to stop — and said so.*

## 8 Next: design the dissipation, not the pulse

The limit we hit is a conjunction: a protected gate must be slow, *and* slowness exposes loss. Our search broke neither clause because it only tuned the *drive*. The sharpest, most AI-native move the map points at is to change the *object* AI designs — the protective dissipation itself, made time-dependent — rather than the pulse on top of it. It runs on the very instrument we just built and shipped, by swapping the search variable from the drive to the engineered leaks.

> **Forecast · v3** — Letting AI search the *gate dissipator* — and a learned, time-dependent squeezing schedule synchronised to the gate [squeezed-cat '23–'25] — is the indicated next attack on the κ₁/κ₂ frontier, and the natural v3. Posted as the challenge, with named credit for whoever closes it. Robotics — automating the build-measure-learn loop on real hardware — is the program's other arm, named in the title and reserved for a later chapter of this lineage (“robotics in QC research, today and ahead”); it enters when the work moves from simulation onto real devices.

## References

- **Nature '24** — Bausch et al., Google DeepMind & Google Quantum AI, 2024.. A transformer neural network learned to decode the surface code and beat the standard matching decoder on real Sycamore-processor data — state-of-the-art error decoding, learned rather than hand-written. *Nature 635, 834–840 (2024).*

- **RL-code '23** — Zeng et al., 2023.. A reinforcement-learning agent searching bosonic codes found, surprisingly, a code built from the Fock states |2⟩ and |4⟩ that suppresses single-photon loss past the break-even point — a recipe humans had not picked. *Phys. Rev. Lett. (2023); arXiv:2212.11651.*

- **bosonic-RL '25** — Deep-RL bosonic-code discovery, 2025.. Curriculum-learning deep reinforcement learning used to discover bosonic autonomous-QEC codes that resist single- and double-photon loss, working directly against the Knill–Laflamme conditions. *Phys. Rev. A (2025); arXiv:2511.12482.*

- **v1.0** — Ali-Khan, this dossier, Chapter 1 (v1.0, 2026).. The first chapter of the lineage: a self-explaining descent to the 'floor', with a minimal cat-qubit simulation reproducing exponential noise bias and a Knill–Laflamme proof that the four-component cat makes photon loss a correctable syndrome. *DOI 10.5281/zenodo.20838233.*

- **Mirrahimi '14** — Mirrahimi et al., 2014.. Introduced dynamically-protected cat qubits: two-photon dissipation stabilises two coherent states and exponentially biases noise toward phase errors, the basis for hardware-efficient bias-preserving computation. *New J. Phys. 16, 045014 (2014); arXiv:1312.2017.*

- **co-design '26** — Variational early-fault-tolerant co-design, 2026.. Jointly learns noise-tailored encodings and their logical gate sets in a single framework — evidence that even cross-layer co-design, long thought wide open, is now being engaged by AI. *arXiv:2605.28162 (2026).*

- **squeezed-cat '23–'25** — Squeezed-cat qubits, 2023–2025.. Engineering the dissipator itself — adding squeezing — is the single biggest known lever on the κ₁/κ₂ threshold (~1–2 orders of magnitude). Recently demonstrated in hardware: 22 s bit-flip time and improved Z-gate fidelity. *arXiv:2210.13406 (npj QI 2023); arXiv:2502.07892 (2025).*
