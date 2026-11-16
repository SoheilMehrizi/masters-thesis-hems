# Research specification

Version: 1.0 — agreed P0 design index, 2026-11-16.
Status: P0.1–P0.5 design complete by researcher confirmation; next task P1.4.

This document records the researcher's confirmed decisions separately from
remaining implementation choices. P0.1 scope, P0.2 scenarios, P0.3 access policy,
P0.4 contracts and P0.5 evaluation design are agreed. Their completion records
design agreement, not implemented or validated research components.
The [backlog](PROJECT_BACKLOG.md) defines the task sequence; the
[literature library](literature/index.html) supplies article-based evidence.

## Confirmed decisions

The following decisions were explicitly provided in the 2026-11-16 interview.

| ID | Decision | Consequence for the research scope |
| --- | --- | --- |
| D001 | The main scientific contribution is causal diagnosis and selecting the right corrective intervention. | Agent coordination and computational efficiency support this central contribution. Their independent superiority has not been demonstrated. |
| D002 | Jev is an optional efficiency component, evaluated after the core method works. | The core diagnosis/intervention system must be implementable and evaluable without Jev. Jev integration is not a prerequisite or a confirmed main baseline. |
| D003 | Initial implementation/evaluation uses one home with multiple devices and cooperating agents. | Neighborhood coordination is outside the initial scope. The existing selected CityLearn building remains the initial simulator foundation; later generalization studies are undecided. |
| D004 | Do not constrain the topic by presumed resource limitations; make it as efficient as possible. | No numerical budget or deadline has been specified. Track computational cost and seek efficient execution; do not infer unlimited available resources or sacrifice the agreed scientific objective to minimize calls. |
| D005 | Adopt “Causal Diagnosis and Digital-Twin-Guided Adaptation for Preference-Aware Home Energy Management with LLM Agents.” | Use this English title in the proposal and shared context. Speed and reliability remain evaluation outcomes. |
| D006 | Residents initially supply natural-language requests, translated into confirmed hard constraints and soft priorities. | The interpretation must expose its structured meaning and resolve consequential ambiguities before treating extracted values as binding. Exact preference fields and confirmation rules remain to be specified. |
| D007 | Use a representative request for a 23°C home temperature and a fully charged car battery by tomorrow; the researcher invited a recommended scenario design. | Use the request to develop a coupled HVAC/EV recovery episode. D008–D010 clarify its preference rules; exact departure and charge target are obtained through the agreed clarification procedure. |
| D008 | Target 23°C with a hard 22.5–23.5°C band while the resident is home in the first example. | The occupancy-dependent band is a confirmed example requirement, not a universal comfort standard. Occupancy evidence, transition/initial conditions and the handling of actual violations still require formalization. |
| D009 | Ask for departure time and confirm the charge target when “fully charged by tomorrow” lacks an exact deadline. | Do not silently choose 07:00, midnight or another deadline. A concrete episode receives confirmed values before scheduling. |
| D010 | If requirements are jointly infeasible, report the conflict, offer feasible alternatives and request permission before relaxing a resident's hard requirement. | Do not silently change preference bounds. Physical/equipment safety limits remain enforced in every case; their relaxation is not a negotiation option. |
| D011 | Initial device scope includes HVAC, EV charging, rooftop PV, a stationary battery and fixed household loads. | Each device/input must pass the appropriate simulator validation before experimental claims. Additional flexible appliances and neighborhood coordination are outside this initial device scope. |
| D012 | Automatically adjust HVAC and EV charging schedules within unchanged, confirmed requirements after independent feasibility and safety checks. | Resident approval is not required for every such revised schedule. Changes to resident hard requirements still require permission. This decision does not authorize model recalibration, active probing or other intervention classes. |
| D013 | LLM agents interpret preferences, diagnose and select interventions; a constrained optimizer computes schedules and an independent validator checks them. | Numerical scheduling is not delegated directly to the LLM in the initial core method. Optimizer formulation, horizon, implementation and detailed validator contract remain open. |
| D014 | Retain an explicit Dynamic Structural Causal Model, with LLM agents using diagnostic tools. | Specify time-dependent causal mechanisms, assumptions, evidence access and validation. An explicit SCM does not itself establish identifiability or correct diagnosis. |
| D015 | Use a frozen Reference Twin plus a versioned Operational Twin. | Preserve the reference model and track operational model versions. This architecture does not authorize automatic recalibration or establish either model's fidelity. |
| D016 | Default to minimizing electricity cost after satisfying confirmed hard requirements; report other outcomes separately. | Explicitly confirmed resident soft priorities take precedence over this default. Objective formulation, tariff/export semantics and treatment of infeasibility remain to be formalized. |

Confirmed decision D017: on 2026-11-16 the researcher approved the consolidated
scope, central research question and plain-language recovery definition, and
requested progression to P0.2. This completes P0.1 as a specification task, not
implementation or validation of the proposed method.

## Agreed P0.1 scope

Study whether an explicit Dynamic SCM and Digital-Twin-tested corrective
interventions improve recovery of confirmed household requirements. The initial
study uses one CityLearn home with HVAC, EV charging, PV, stationary storage and
fixed loads. Residents provide natural-language preferences; the system confirms
hard constraints and soft priorities. LLM agents interpret requests, investigate
causes through tools and select interventions. A constrained optimizer computes
schedules, with independent validation before execution. The default soft
objective is electricity cost unless the resident confirms another priority.

A frozen Reference Twin preserves the healthy reference model; a versioned
Operational Twin represents the current model. Exact state synchronization,
calibration rules and rollout contracts remain to be defined. Neither Twin has
been implemented or validated. Their predictions must be checked against actual
post-action observations when assessing recovery.

Validated HVAC/EV rescheduling within unchanged requirements is automatic.
Relaxing resident hard requirements requires permission. Other intervention
permissions remain open. Jev is an optional later efficiency study. Speed,
reliability, causal correctness and agent-topology superiority are outcomes to
test, not established properties or additional confirmed main contributions.

The research question and meaning of recovery below are confirmed in D017.
Detailed decisions remain assigned to later P0 tasks.

## Initial device and control scope

The initial study covers one home with HVAC, EV charging, rooftop PV, stationary
storage and fixed household loads. This is an agreed research scope, not a claim
that every device extension is already validated. Fixed loads are background
inputs rather than newly controllable appliances. PV curtailment or other new
control capabilities are not assumed from its inclusion in scope.

The core responsibilities agreed in D006 and D013 are:

| Responsibility | Assigned mechanism | Specification still needed |
| --- | --- | --- |
| Interpret resident requests | LLM agents, followed by confirmation of extracted hard constraints and soft priorities | Typed preference fields and confirmation procedure |
| Diagnose deviations and select interventions | Explicit Dynamic SCM and LLM agents using diagnostic tools | Mechanisms, uncertainty, causal assumptions and information access |
| Compute device schedules | Constrained numerical optimizer; electricity-cost default unless confirmed priorities override it | Formulation, horizon, solver and feasibility handling |
| Validate candidate actions | Independent validator | Physical constraints, authority checks and failure behavior |
| Execute and verify | Validated scheduling workflow; actual post-action observations | Runtime contract, fallback and outcome criteria |

Automatic HVAC/EV schedule adjustments are authorized within the confirmed
requirements and checks. Permission to relax resident hard requirements is a
separate decision. Stationary-battery dispatch authority, Twin recalibration and
active diagnostic probes still need explicit policies in the later intervention
contracts. These later decisions are now recorded in
[P0.4 contracts](COMPONENT_CONTRACTS.md), P04-D001–D003: battery scheduling is
authorized after validation within unchanged limits; candidate calibration is
automatic but promotion needs approval initially; probes require an approved
bounded policy. Numeric probe limits remain open.

## Adopted topic and title

Previously recorded title:

**Digital-Twin-Guided Diagnostic Adaptation for Fast and Reliable
Preference-Aware Home Energy Management Using LLM-Based Multi-Agent Systems.**

Selected English title, confirmed in the second interview round:

**Causal Diagnosis and Digital-Twin-Guided Adaptation for Preference-Aware
Home Energy Management with LLM Agents.**

Persian rendering:

**تشخیص علّی و سازگاری هدایت‌شده با دوقلوی دیجیتال برای مدیریت انرژی خانگی
مبتنی بر ترجیحات با عامل‌های مدل زبانی بزرگ**

The title puts the confirmed diagnostic contribution first. Speed and reliability
remain outcomes to evaluate, rather than demonstrated properties. Selecting the
title does not establish causal identifiability or complete the methodology.

## Representative episode — recommended draft, not a finalized benchmark

Resident request: “I want the temperature at 23 degrees Celsius and my car's
battery fully charged by tomorrow.”

### Request interpretation

| Element | Confirmed interpretation | Still requires clarification |
| --- | --- | --- |
| Temperature | Target 23°C; hard 22.5–23.5°C band while the resident is home, for this example. | Occupancy inputs, initial state and occupancy-transition treatment. |
| EV | Ask for the departure deadline and confirm the intended charge target. | The actual departure/target values, connection/availability, current charge and usable charge-limit semantics. |
| Infeasibility | Explain the conflict, propose feasible alternatives and ask before relaxing a resident's hard requirement. Routine HVAC/EV rescheduling is automatic after checks within unchanged requirements. | Soft-objective ranking and authority for other intervention classes. |

The hard comfort requirement constrains planning and defines a violation if the
observed temperature leaves the band during its active window. It is not a claim
that disturbances or thermal inertia can never cause a violation. P04-D008 now
confirms immediate scoring at initialization/occupancy activation with no implicit
grace interval. Recovery is planned and logged without erasing those violations;
exact recovery deadlines and verification metrics remain for P0.5.

“Tomorrow” must be resolved against the eventual scenario clock and verified time
semantics. Do not silently substitute the chat date, midnight, or a departure
time. Exact calendar/time alignment remains a simulator verification task.

### Recommended system behavior

1. Translate the request into a proposed structured preference contract, clarify
   missing consequential details, and obtain confirmation of hard bounds.
2. Check whether the confirmed temperature and EV goals are jointly feasible
   under device, availability and electrical constraints. Report conflicts and
   feasible alternatives; obtain permission before relaxing a resident's hard
   requirement. Keep physical/equipment safety limits enforced in every case.
3. Use the constrained optimizer to produce a schedule; apply the independent
   validator before execution. Monitor actual temperature, EV charge progress
   and the other permitted observations.
4. When a confirmed bound is violated or a goal is at risk, assess competing
   causes. Candidate explanations might include forecast error, equipment
   degradation, Twin mismatch or scheduling/coordination failure. Similar symptoms
   must not automatically be labeled as one known fault.
5. Compare permitted corrective interventions through diagnosis and isolated Twin
   rollouts; check physical constraints and authority independently of LLM output.
6. Execute validated HVAC/EV schedule adjustments automatically within unchanged
   requirements. Apply the separately specified authority policy to other
   interventions. Observe outcomes and verify recovery; a favorable Twin
   prediction alone does not count as recovery.

The companion P0.2–P0.5 specifications now define scenario categories, information
access, intervention authority and evaluation rules. Numeric settings, simulator
channel mappings and executable action interfaces remain mandatory implementation/
validation artifacts. These steps describe intended behavior, not an implemented
or experimentally validated controller.

### Confirmed central research question

Does causal diagnosis combined with Digital-Twin-tested intervention selection
improve verified recovery of confirmed household requirements, relative to
diagnosis-free replanning, while respecting hard constraints and avoiding
unnecessary interventions?

This question is confirmed in D017. The agreed P0.5 evaluation plan defines the
baselines, directional hypotheses and metric formulas; pilot-selected numeric
settings must be frozen before evaluation.

Confirmed meaning of verified recovery: actual observations show that affected
requirements are restored and remain satisfied over a specified verification
window; the EV target is checked at its confirmed deadline. Log the preceding
violations and intervention costs even if recovery succeeds. If restoration is
infeasible, reporting that conflict is appropriate behavior but does not count as
successful restoration of the original requirements. Verification windows,
thresholds and numeric cutoffs must be realized under the agreed P0.5 pilot and
manifest policy before evaluation.

## Architecture and comparison scope after P0

The Dynamic SCM and two-Twin arrangement are now confirmed in D014–D015.
Typed conditional intervention planning and information boundaries are agreed in
P0.3–P0.4. The hierarchical agent workflow is the core; topology comparisons are
supplementary. P0.5 confirms four core methods, adapted Bayesian/rule diagnostic
baselines and four ablations. DRL and additional paper-derived HEMS reproductions
remain optional candidates. No exact paper reproduction is approved merely by
appearing in the literature library.
See [shared project context](../agent/agent.md) for the current boundaries.

## Agreed design documents and implementation gates

P0.1–P0.5 are complete as design tasks. The
[P0.2 degradation specification](DEGRADATION_SPECIFICATION.md) records the agreed scenario design. The [P0.3 access policy](INFORMATION_ACCESS_SPECIFICATION.md) is agreed.
The [P0.4 contracts](COMPONENT_CONTRACTS.md) are agreed (P04-D010).
The [P0.5 evaluation plan](EVALUATION_SPECIFICATION.md) is agreed (P05-D010).
Next implementation task: P1.4, reproduce and verify fixed annual equipment sizing.

| Completed design task | Agreed scope; detailed realization follows validation |
| --- | --- |
| P0.2 | Five degradation families, overlap, simultaneous/cascading causes, episode initial conditions and feasible/infeasible cases |
| P0.3 | Observations, latent/evaluator-only truth, forecast availability, occupancy evidence and diagnostic information access |
| P0.4 | Preference schema and confirmation, device/control interfaces, optimizer formulation/horizon, Twin state/version contracts, battery/calibration/probing authority, fallback, units and clock semantics |
| P0.5 | Quantitative hypotheses, recovery windows, metrics, baselines, topology-comparison scope, data splits and versioning |

Concrete EV deadlines and charge targets are scenario inputs obtained through the
agreed clarification policy. Submission deliverable/date remain unspecified;
presumed resource limitations should not drive topic selection.

## P0 sequence and completion gate

1. P0.1: finish the topic interview and consolidate an agreed specification,
   recording remaining choices explicitly.
2. P0.2: formalize the five degradation families, simultaneous and cascading cases.
3. P0.3: define observable, latent and evaluator-only information boundaries.
4. P0.4: define interfaces, contracts, units and time semantics.
5. P0.5: formalize hypotheses, metrics and experiment/model versioning.

P0.1 is complete, supported by D001–D017 and the researcher's consolidated confirmation.
P0.2–P0.5 completion evidence is in the linked version 1.0 companion documents and
their decision tables. The P0 review gate is now satisfied. Work continues task by
task; later phases are not automatically authorized by their appearance here.

Still required: simulator audits; exact channel/schema/time mappings; validated
Twin, SCM, optimizer, validator and fallback implementations; source-specific
baseline fidelity records; independent severity/threshold/horizon pilots; and
frozen numeric experiment manifests. Device probes remain disabled until their
bounded policy is explicitly approved. Operational Twin promotion still needs
approval initially. These are implementation/evaluation gates, not unrecorded
exceptions to the completed design.

## Revision history

| Version | Date | Change |
| --- | --- | --- |
| 0.1 | 2026-11-16 | Recorded D001–D004 from the first topic interview; retained title and architecture questions as open. |
| 0.2 | 2026-11-16 | Recorded selected title, natural-language interface and resident example (D005–D007); drafted the recovery episode with unresolved parameters explicit. |
| 0.3 | 2026-11-16 | Recorded the occupied-home temperature band, deadline clarification and infeasibility negotiation rules (D008–D010). |
| 0.4 | 2026-11-16 | Recorded initial device scope, automatic validated HVAC/EV scheduling, and the LLM/optimizer/validator responsibility split (D011–D013). |
| 0.5 | 2026-11-16 | Recorded explicit Dynamic SCM, two-Twin arrangement and electricity-cost default (D014–D016); consolidated scope for review and assigned detailed open decisions to P0.2–P0.5. |
| 0.6 | 2026-11-16 | Confirmed scope, question and recovery definition (D017); completed P0.1 and opened P0.2. |
| 1.0 | 2026-11-16 | Indexed agreed P0.2–P0.5 companion specifications and final P05-D010 confirmation; completed P0 design with numeric/implementation gates preserved. |
