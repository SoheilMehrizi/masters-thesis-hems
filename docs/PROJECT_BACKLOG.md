# Research implementation backlog

Updated: 2026-11-16

Track completion by changing `- [ ]` to `- [x]`. Complete work task by task, following the researcher's instructions. This checklist records the full research scope; it does not authorize implementation or finalize unresolved methodological choices.

Checked items have saved verification evidence. Unchecked items are pending or not yet verified as complete; some may already have partial work. Architectural agreement alone does not count as implementation completion. Paper-derived baselines remain candidates until their scope and feasibility are agreed.

## Current position and next task

P1.1–P1.3 are complete according to [saved setup validation](../reports/setup_validation.md) and [implementation notes](../reports/implementation_notes.md). These checks were not rerun when this backlog was created. The complete simulator milestone remains open.

**P0 design is complete**, confirmed by the researcher on 2026-11-16. **Next task: P1.4 — reproduce and verify fixed annual equipment sizing.** Numeric experiment manifests and implementation validation gates remain mandatory.

P0.1 is complete following researcher confirmation of the [versioned research specification](RESEARCH_SPECIFICATION.md). Confirmed: causal diagnosis/corrective intervention is central; Jev is optional; the first study uses one home with HVAC, EV charging, PV, stationary battery and fixed loads. LLMs interpret, diagnose using an explicit Dynamic SCM, and select interventions; a constrained optimizer computes schedules with independent validation. Use a frozen Reference Twin and versioned Operational Twin. Default to electricity-cost minimization unless explicitly confirmed resident priorities override it. Validated HVAC/EV rescheduling is automatic within unchanged requirements. The selected title, natural-language input, occupied-home 22.5–23.5°C example band, EV clarification and infeasibility negotiation are recorded. The companion P0.2–P0.5 designs are also complete; exact numerical settings and executable components remain subject to their recorded validation gates.

The [interactive literature library](literature/index.html) now contains analyses of all 29 unique local articles, including six Jev decision-model studies and their [roles in our research and baseline recommendations](literature/research-map.html). This literature deliverable supports P0; it does not finalize specification choices or mark P0 tasks complete.

**Next simulator task: P1.4 — reproduce and verify fixed annual equipment sizing.**

Acceptance: trace the original full-year sizing procedure; reproduce and compare HVAC, PV, and battery ratings against the recovered reference; verify that episode resets and seasonal windows retain the frozen ratings; document discrepancies and evidence. Loading the recorded ratings alone does not complete this task.

## Completion rule

Before checking an implementation task, its scoped behavior must work, relevant checks must pass, and an evidence link must be recorded. For design tasks, record the agreed specification and remaining assumptions. For experiments, retain configuration, seeds, results, and limitations. Mark deferrals explicitly instead of checking them as completed.

## P0 — Research specification

- [x] P0.1 Consolidate agreed research decisions and unresolved choices in a versioned specification.
- [x] P0.2 Formalize all five degradation families, including simultaneous and cascading causes.
- [x] P0.3 Define observed, latent, and evaluator-only variables and access boundaries.
- [x] P0.4 Define component interfaces, data contracts, units, and time semantics.
- [x] P0.5 Define hypotheses, metrics, and model/experiment versioning.

P0.5 completed design decisions P05-D001–D010: verified recovery success rate as primary; four core methods, four ablations and two adapted diagnostic baselines; hierarchical core with supplementary topology studies; separated development/held-out evaluation; separate reactive/prevention suites; paired effects with 95% intervals and pilot-based repeats; frozen manifests and complete run/approval logs. Completion evidence: [agreed evaluation specification v1.0](EVALUATION_SPECIFICATION.md) and final researcher confirmation P05-D010. Endpoint formulas and directional hypotheses are agreed; numeric protocol, statistical implementation and baseline fidelity remain required before evaluation.

P0.4 completed design decisions P04-D001–D010: automatic validated battery scheduling within unchanged limits; automatic isolated Operational Twin candidate fitting/testing with approval before active promotion initially; active probes only under an explicitly approved bounded policy; receding-horizon/event-triggered execution; validated deterministic fallback with explicit failure reporting; bounded conditional multi-step plans; linear/piecewise-linear LP/MILP scheduling; immediate scoring of active-band violations without implicit grace; deterministic monitoring with event-triggered LLM diagnosis. Completion evidence: [agreed component contracts v1.0](COMPONENT_CONTRACTS.md) and researcher consolidated confirmation (P04-D010). Executable schemas, audited clock/channel mapping and numerical settings remain later validation gates.

P0.3 completed design decisions P03-D001–D008 are recorded in the [agreed information access policy](INFORMATION_ACCESS_SPECIFICATION.md): evaluator-only hidden truth/future realizations; validated measurement categories; exact observations followed by selected robustness tests; shared timestamped evidence with role-specific views; observation/history-based Twin state estimation; competing hypotheses, unknown outcomes and abstention. Declared future plans with clarification and bounded recent history plus logged bounded retrieval are confirmed. Completion evidence: linked v1.0 policy and researcher answers. Channel mappings, leakage checks and pilot-selected numeric budgets remain mandatory validation gates. P0.5 is also complete; next implementation task is P1.4.

Deliverable: agreed research specification and architecture contracts. Existing conceptual decisions are inputs to this work, not decisions to reopen automatically.

P0.1 completion evidence: [research specification v1.0](RESEARCH_SPECIFICATION.md), D001–D017; researcher confirmed scope, question and recovery definition on 2026-11-16. Companion P0.2–P0.5 designs are now agreed; remaining realization details are explicitly gated. Agreed design: [P0.2 degradation scenarios](DEGRADATION_SPECIFICATION.md).

P0.2 completed design decisions P02-D001–D012: use explicit confirmed preference updates; cover HVAC capacity, EV charging-power, battery discharge-power and PV-output derating plus battery energy-capacity and efficiency losses initially. Progress from healthy/isolated scenarios to selected simultaneous/cascading cases; begin with abrupt persistent changes, then selected gradual/temporary cases. Include recoverable and infeasible cases with matched controls. Forecasts cover PV, outdoor temperature and fixed loads; model mismatch covers thermal response and battery efficiency; coordination covers delayed/missing delivery and stale versions with validation enabled. Battery accounting and selected combinations are confirmed in the linked v1.0 design. Numeric severities and timing require independent pilots and a frozen P2 manifest before evaluation (P02-D012). P0.2 completion records design agreement, not implementation. Access policy: [P0.3](INFORMATION_ACCESS_SPECIFICATION.md), also complete.

## P1 — CityLearn simulator reproduction

- [x] P1.1 Pin and verify CityLearn 3.2.0 and the audited source commit.
- [x] P1.2 Recover and audit the Custom Alameda artifacts; verify all 29 recorded payload hashes.
- [x] P1.3 Load and verify the selected building, schema, and LSTM dynamics.
- [ ] P1.4 Reproduce and verify fixed annual equipment sizing.
- [ ] P1.5 Verify synthetic EV schedules and time-of-use tariffs, including departure-target feasibility and interval boundaries.
- [ ] P1.6 Validate observations, actions, resets, and LSTM warm-up across intended episode windows.
- [ ] P1.7 Reproduce the winter and summer thermal-response reference experiments.
- [ ] P1.8 Validate EV, battery, PV, and energy-balance behavior.
- [ ] P1.9 Validate determinism, logging, and KPI interpretation across the benchmark.

Evidence for P1.1–P1.3: [setup validation](../reports/setup_validation.md). The existing 48-transition winter smoke test does not complete P1.7. Synthetic inputs and unverified forecast issue times/calendar timezone must remain explicitly documented.

Deliverable: reproducible, validated simulation foundation.

## P2 — Degradation-injection benchmark

- [ ] P2.1 Define and validate healthy reference scenarios.
- [ ] P2.2 Implement and validate preference-drift scenarios.
- [ ] P2.3 Implement and validate forecast-error scenarios without future-data leakage.
- [ ] P2.4 Implement and validate Digital Twin model-mismatch scenarios.
- [ ] P2.5 Implement and validate equipment-degradation scenarios.
- [ ] P2.6 Implement and validate scheduling/coordination-failure scenarios.
- [ ] P2.7 Implement simultaneous and cascading degradation scenarios.
- [ ] P2.8 Define and enforce limited-observability conditions.
- [ ] P2.9 Isolate hidden ground truth and establish paired counterfactual evaluation.

Deliverable: versioned benchmark with documented onset times, severities, mechanisms, and information boundaries.

## P3 — Controllers and baseline reproduction

- [ ] P3.1 Implement a rule-based HEMS baseline.
- [ ] P3.2 Agree and implement an MPC/MILP formulation.
- [ ] P3.3 Implement constrained direct LLM scheduling.
- [ ] P3.4 Resolve scope and implement the selected LA-UPAHEM comparison, documenting adaptations.
- [ ] P3.5 Resolve scope and implement the selected El Makroum agentic scheduling comparison.
- [ ] P3.6 Evaluate healthy-operation performance under matched conditions.
- [ ] P3.7 Document baseline fidelity, budgets, shared tasks, and reproduction limitations.

Deliverable: comparable controller interfaces and reproducible reference results. DRL remains a possible comparison, not the proposed core controller.

## P4 — Digital Twin infrastructure

- [ ] P4.1 Implement the Reference Twin with frozen reference parameters.
- [ ] P4.2 Implement the versioned Operational Twin.
- [ ] P4.3 Implement state/history synchronization using permitted evidence.
- [ ] P4.4 Generate evidence and residuals with provenance.
- [ ] P4.5 Implement isolated hypothetical rollouts from consistent snapshots.
- [ ] P4.6 Implement calibration authorization, validation, and rollback.
- [ ] P4.7 Test separation of equipment degradation, model mismatch, and evaluator state.

Deliverable: isolated, versioned dual-Twin subsystem.

## P5 — Dynamic SCM and diagnosis

- [ ] P5.1 Specify the time-indexed hierarchical causal graph.
- [ ] P5.2 Specify structural mechanisms, hidden states, and causal assumptions.
- [ ] P5.3 Agree and implement the probabilistic inference representation.
- [ ] P5.4 Define evidence likelihoods, priors, and calibration procedure.
- [ ] P5.5 Implement dependent, simultaneous-cause belief inference.
- [ ] P5.6 Implement unknown-cause and abstention behavior with justified thresholds.
- [ ] P5.7 Evaluate identifiability and confounded cause pairs.
- [ ] P5.8 Implement the agreed diagnostic baselines.
- [ ] P5.9 Evaluate selective safe tests using decision value, cost, and risk.
- [ ] P5.10 Validate causal/interventional predictions and uncertainty calibration.

Deliverable: probabilistic causal diagnosis engine with a structured diagnosis-to-planner contract.

## P6 — Intervention planning and execution

- [ ] P6.1 Define the typed operation library, preconditions, permissions, and side effects.
- [ ] P6.2 Define conditional multi-step plan schemas and termination rules.
- [ ] P6.3 Implement structural plan validation.
- [ ] P6.4 Implement deterministic safety and authority checks, including fallback constraints.
- [ ] P6.5 Evaluate candidate plans using Twin rollouts and causal hypotheses.
- [ ] P6.6 Agree and implement expected-loss and robust-loss planning objectives.
- [ ] P6.7 Implement bounded active diagnostic probes and independent safety checks.
- [ ] P6.8 Implement staged execution, delivery uncertainty, idempotency, outcome verification, and replanning.
- [ ] P6.9 Implement agreed intervention baselines and component ablations.

Deliverable: safe intervention workflow covering structural, safety, sandbox, and runtime validation gates.

## P7 — Agentic architectures

- [ ] P7.1 Define shared prompts, tool permissions, model configuration, and contracts.
- [ ] P7.2 Implement the centralized architecture.
- [ ] P7.3 Implement the hierarchical architecture.
- [ ] P7.4 Implement the decentralized architecture with disagreement and timeout handling.
- [ ] P7.5 Integrate common SCM and Twin interfaces across architectures.
- [ ] P7.6 Test failure handling, fallback, and authority boundaries.
- [ ] P7.7 Instrument matched computational budgets, tokens, latency, and cost.

Deliverable: three comparable agent architectures. Their implementation order can be chosen task by task.

## P8 — Experiments

- [ ] P8.1 Freeze scenario definitions, seeds, train/validation/test splits, and evaluation protocol.
- [ ] P8.2 Evaluate diagnostic performance, uncertainty calibration, and abstention.
- [ ] P8.3 Evaluate single, simultaneous, and cascading causes.
- [ ] P8.4 Compare passive diagnosis with selective active diagnosis.
- [ ] P8.5 Measure observed recovery, safety, cost, comfort, and unnecessary interventions.
- [ ] P8.6 Compare the three agent topologies under matched conditions.
- [ ] P8.7 Compare direct LLM scheduling and LLM-orchestrated optimization.
- [ ] P8.8 Run agreed ablations that test the contribution claims.
- [ ] P8.9 Run robustness, model-mismatch, missing-data, and out-of-distribution tests.
- [ ] P8.10 Complete statistical analysis, confidence intervals, and failure/negative-result analysis.

Deliverable: reproducible experimental evidence. Freeze the protocol before final evaluation; do not tune on the test set.

## P9 — Paper and reproducibility release

- [ ] P9.1 Verify primary literature and complete the novelty-collision audit.
- [ ] P9.2 Finalize precise, evidence-supported contribution statements.
- [ ] P9.3 Document simulator, dataset, model, and synthetic-extension provenance.
- [ ] P9.4 Write the mathematical methodology and explicit assumptions.
- [ ] P9.5 Report baselines, adaptations, experimental results, and computational costs.
- [ ] P9.6 Document threats to validity and simulation-only limitations.
- [ ] P9.7 Prepare and verify the reproducibility repository and execution instructions.
- [ ] P9.8 Prepare the manuscript and submission package for the agreed venue.

Deliverable: reviewable publication and reproducibility package. Submission/publication is a separate instructed action.

## Milestone checklist

- [ ] M1 — Complete simulation foundation verified (P1).
- [ ] M2 — Degradation benchmark validated (P2).
- [ ] M3 — Control baselines established (P3).
- [ ] M4 — Twins and causal diagnosis validated (P4–P5).
- [ ] M5 — Safe intervention workflow operational (P6).
- [ ] M6 — Agent architectures implemented and compared (P7 and P8.6).
- [ ] M7 — Experimental results finalized (P8).
- [ ] M8 — Publication and reproducibility package ready (P9).

## Evidence and decision log

Add a row whenever a task is completed, deferred, blocked, or materially re-scoped. Preserve task IDs when refining the plan.

| Task | Status | Evidence / decision | Recorded date |
|---|---|---|---|
| P1.1 | Complete | [Saved validation](../reports/setup_validation.md): version and source provenance | 2026-11-13 |
| P1.2 | Complete | [Saved validation](../reports/setup_validation.md): recovered payload integrity | 2026-11-13 |
| P1.3 | Complete | [Saved validation](../reports/setup_validation.md): model, initialization, rollout, replay, thermal response | 2026-11-13 |

Dates above record backlog reconciliation, not new test execution dates. The initial-paper subset, final venue, detailed inference method, loss weights, thresholds, and experiment counts remain open until agreed.
