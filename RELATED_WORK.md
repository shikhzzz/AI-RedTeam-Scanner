# Related Work & Positioning — AI Red Team Scanner

**Purpose:** defend the project honestly against "hasn't this been done?" This project is a **method demonstration and replication-transfer**, not a novel research result. Read this before presenting.

## The one-sentence position (memorize)

> *Gao (2026) audited attack-success judges for jailbreaking; this project applies the same audit methodology to the evaluator layer of prompt-injection scanning — the cheap heuristic matchers real tools ship — where success is behavioral compliance rather than harm.*

## Claims we DO make

- Engineering: a modular, reproducible injection-testing + evaluator-audit harness.
- Experimental (on a tiny demonstration set): keyword vs expected-behavior evaluator, measured against a human gold set via ASR and FPR/FNR/precision/recall/F1.
- A documented, specific failure mode of keyword evaluators in the *injection* setting: a refusal that echoes attack vocabulary (e.g. "I can't reveal my system prompt") scored as a breach.

## Claims we DO NOT make (retired against the literature)

- ❌ "Novel: auditing evaluator reliability for prompt injection." Done for jailbreak judges by Gao 2026, StrongREJECT 2024, RobustJudge 2025, Raina 2024, GuidedBench 2025.
- ❌ "Keyword matching's unreliability is a new finding." Known since GCG (2023); quantified in StrongREJECT (2024).
- ❌ Any generality claim from one model / 10 payloads. This is a demonstration, not a study.

## The field's trajectory (how to narrate it)

*"Does the model refuse?"* (string matching: Perez 2022, GCG 2023) → *"Is harmful content present?"* (intent-based, human-validated: HarmBench, StrongREJECT 2024) → *"Is the judge itself correct?"* (evaluator audits: Gao 2026, RobustJudge 2025). We sit at stage 3, in the injection lane, with cheap evaluators.

## Per-paper delta (what to say when challenged)

| Paper | What it did | Your honest delta |
|---|---|---|
| **Gao 2026** (2606.25487) — your main rival | Audited jailbreak judges (LLM judges + fine-tuned classifier) vs 596 human labels; precision/recall + framing/refusal-prefix evasion | Different **setting** (injection, not jailbreak), different **success definition** (behavioral compliance, not harm), different **evaluator family** (cheap keyword/regex matchers practitioners ship, which Gao never tested). Same method, transferred. Ours is a demonstration; Gao is a full study. |
| **StrongREJECT 2024** | Proved string-matching overstates jailbreak ASR; human-trained judge | We reuse the *insight* (string matching unreliable) as our baseline's known flaw, in the injection setting. |
| **HarmBench 2024** | Intent-based success + fine-tuned judge + human-labeled validation set | We borrow the intent/behavior-based success philosophy; we do not build a trained classifier. |
| **Open-Prompt-Injection / Liu 2024** | Formalized injection; ASV success metric; toolkit | Closest injection formalism; our "success = objective achieved" is a simpler, per-attack version of ASV. Their toolkit is a reuse candidate for future work. |
| **AgentDojo 2024 / InjecAgent 2024** | State/action-based success checks (no text judge) in agent settings | The "right answer" when you control an environment. We don't — we test chat-style app prompts — so we must use a text evaluator, which is exactly why its reliability matters here. Reuse their corpora in future work. |
| **PAIR 2023 / TAP 2023** | Adaptive attacker-LLM loops; judge-based success | Establishes the adaptive adversary our evaluator would need to survive. We do NOT implement an adaptive attack (future work); state this. |
| **GCG 2023** | Optimized suffix; string-match ASR | Our keyword evaluator inherits this exact success function; we audit that inheritance. |
| **RobustJudge 2025** | H1–H8 heuristic attacks on judges + defenses | Source of an evasion test taxonomy to adapt for our evaluator in future work. |
| **Raina 2024** | Universal adversarial phrases inflate judges; comparative > absolute scoring | Evasion-style methodology; non-safety tasks. Informs future evasion experiments. |
| **GuidedBench 2025** | Named the two success philosophies (refusal-based vs harm-based) | Names the axis our keyword vs expected-behavior evaluators straddle. |
| **PyRIT / garak** (tools) | Ship SubStringScorer / model-based detectors; docs concede FP issues | The practitioner reality that makes auditing cheap evaluators legitimate rather than a straw man. |

## The five challenges a professor will raise (and the honest answer)

1. **"Gao 2026 exists — what do you add?"** → Setting + evaluator family transfer; see delta table. Demonstration, not claim of novelty.
2. **"Your ground truth is tiny."** → Agreed; 10 labels is a demonstration of the *method*, not a study. Future work: 600+ inter-annotated labels (Gao-sized).
3. **"Keyword matching is a straw man."** → Yes — and we say so. We audit it only because real tools (PyRIT, garak) still ship it.
4. **"One model isn't a study."** → Correct; single-model result is stated as a limitation, not generalized.
5. **"Where's your threat model?"** → Part 2.4 of the roadmap: direct single-turn injection against an app's user-input channel; indirect/multi-turn explicitly out of scope.

## Reading order (from the review)

Gao 2026 → HarmBench → StrongREJECT → Perez → Open-Prompt-Injection → AgentDojo + InjecAgent → GCG + PAIR → JailbreakBench → Raina → RobustJudge → GuidedBench → PyRIT/garak docs.
