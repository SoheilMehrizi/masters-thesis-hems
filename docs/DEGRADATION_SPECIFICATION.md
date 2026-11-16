# P0.2 — Degradation scenarios

Version: 1.0 — agreed scenario design, 2026-11-16.
Status: P0.2 complete as a design task; numeric manifest and injector validation remain P2 gates.

Scope follows the [agreed P0.1 specification](RESEARCH_SPECIFICATION.md).
This is an agreed benchmark design, not a set of findings extracted from papers
or an implemented fault injector. Numeric severities, durations and thresholds
are not approved; temporal-profile categories are confirmed below.

## Confirmed P0.2 decisions

| ID | Researcher decision | Consequence |
| --- | --- | --- |
| P02-D001 | Start with explicit, confirmed resident updates; add inferred changes later. | Initial benchmark preference changes have an explicit confirmation event. Do not infer binding preference changes from behavior. |
| P02-D002 | Include HVAC, EV, stationary battery and PV degradation from the start. | The initial equipment family must cover all four device groups. Exact mechanisms and simulator support remain to be specified and validated. |
| P02-D003 | Progress from healthy controls and isolated causes to selected simultaneous and cascading cases. | Cover each family in isolation before evaluating selected combinations; distinguish overlapping root causes from downstream consequences. |
| P02-D004 | Adopt the four proposed device mechanisms and also include stationary-battery energy-capacity and efficiency losses initially. | Initial equipment coverage has six mechanism types; isolate them before combining. Capacity/state and efficiency/energy-balance semantics require explicit validation. |
| P02-D005 | Begin with abrupt persistent cases, then selected gradual and temporary cases. | Stage implementation accordingly; do not omit selected gradual/temporary cases from the intended study merely because abrupt cases come first. |
| P02-D006 | Include recoverable and infeasible cases with matched healthy controls. | Evaluate recovery separately from correct conflict reporting and requests to relax resident requirements. Numerical feasibility checks and labels remain to be defined. |
| P02-D007 | Include PV, outdoor-temperature and fixed-load forecast errors. | Validate each forecast stream and issue-time semantics; isolated cases change forecasts rather than realized conditions. |
| P02-D008 | Include thermal-response and battery-efficiency mismatch in the Operational Twin. | For model-only cases, keep the plant and frozen Reference Twin unchanged. Specific model parameters remain subject to audit. |
| P02-D009 | Include delayed/missing plan delivery and stale preference/plan versions, with the independent validator enabled. | Distinguish rejected-plan containment from unsafe execution; measure any resulting service disruption separately. |
| P02-D010 | Preserve stored kWh for capacity loss at onset states fitting within the reduced capacity; defer above-capacity states. Reduce both charge and discharge efficiencies for initial efficiency-loss cases. | Validate normalized-state mapping and actual simulator efficiency semantics; no undocumented energy clipping or creation. |
| P02-D011 | Adopt the proposed preference-update and combined-scenario shortlist subject to simulator validation. | Use isolated controls for each combination; retain the HVAC-to-EV cascade only if a validated shared electrical constraint supports that causal path. |
| P02-D012 | Select numeric severities and timing through independent simulator pilots using documented physical/feasibility criteria; require a frozen manifest before comparative evaluation. | Numeric values are intentionally deferred to validated benchmark construction. This agreement does not approve any provisional percentage, duration or onset time. |

## Family definitions

| Family | Definition | Example mechanism; numerical realization requires validation |
| --- | --- | --- |
| Preference change | The resident's requirements change; this is a legitimate change, not an equipment fault. Inferred changes require clarification before becoming binding. | A confirmed earlier EV departure invalidates an otherwise valid schedule. |
| Forecast error | Exogenous future inputs differ from the forecast available when scheduling; isolate this from device and Twin-parameter changes. | PV output is lower than forecast while equipment remains healthy. |
| Twin model mismatch | The predictive model is inaccurate relative to an unchanged simulated plant; isolate by changing model assumptions/parameters only. | Operational Twin thermal-response parameters are inaccurate while the plant is unchanged. |
| Equipment degradation | Physical simulated-device behavior changes while the prior model initially remains unchanged. This can produce model residuals without being a model-only injection. | Reduced HVAC capacity or EV charging-power limit. |
| Scheduling/coordination failure | A fault in planning, plan propagation or execution coordination, rather than a changed resident requirement or plant. | Execution receives a stale plan. The independent validator remains enabled. |

Changing the plant can make the Twin inaccurate as a consequence. Record the
injected root cause separately from downstream model mismatch and symptoms;
do not label every residual as an independent equipment and model fault.
Identical symptoms need not uniquely identify a cause. Ambiguity and unknown
causes need an explicit policy in the diagnostic/evaluation contracts.

## Confirmed scenario progression

1. Healthy controls and legitimate preference updates.
2. Isolated cases for each family with matched healthy reference conditions.
3. Selected simultaneous causes with independently specified onsets.
4. Selected cascades with explicit causal links, distinguished from coincident faults.

The progression is confirmed in P02-D003. The conditionally selected
cascade is reduced HVAC capacity causing longer operation, followed by an EV
deadline risk under a shared electrical limit. That case requires a validated
shared-limit model; deadline risk is a consequence, not automatically a second fault.

## Confirmed initial equipment mechanisms

These are controlled benchmark interventions, not claims about the frequency or
physical mechanisms of real device failures. Preserve healthy source artifacts;
use separately versioned experiment configurations or wrappers.

| Device | Confirmed mechanism category | Isolation requirement |
| --- | --- | --- |
| HVAC | Reduce available heating/cooling capacity | Keep weather, resident requirements and initial predictive model unchanged in the isolated case; select season-appropriate operation. |
| EV charger | Reduce maximum delivered charging power | Preserve EV availability and charge target; distinguish the actual device limit from a revised schedule or forecast. |
| Stationary battery | Reduce maximum available discharge power | Keep usable energy capacity and initial stored energy unchanged; preserve physical state continuity. This does not authorize automatic battery interventions. |
| Rooftop PV | Derate plant-side available PV power under otherwise matched irradiance/weather | Keep weather and initial forecast unchanged in the isolated case; distinguish plant derating from forecast-only error. |
| Stationary battery | Reduce usable energy capacity | Preserve discharge-power and efficiency settings in the isolated case. Define stored-energy/state-of-charge mapping and account explicitly for energy made unavailable at the change. |
| Stationary battery | Reduce energy conversion efficiency | Preserve usable capacity and power limits in the isolated case. Specify charge/discharge efficiency allocation and verify energy losses explicitly. |

The six mechanism categories are confirmed in P02-D004. Battery capacity loss
must not silently rescale stored energy to preserve a normalized state-of-charge
value, or silently discard energy through undocumented clipping. The initial
state, newly accessible capacity and treatment of any inaccessible stored energy
need a documented rule. A normalized observation alone is not an energy ledger.
Initial efficiency-loss cases affect both charge and discharge, per P02-D010;
their numerical mapping follows the audited simulator semantics.
Injection interfaces, units and supported physical responses require simulator
audits. No device degradation is implemented by changing an observation alone.

## Temporal and feasibility coverage

- Start with abrupt, persistent changes at controlled onset times; add selected
  gradual and temporary cases after the isolated mechanisms are validated.
- Include cases recoverable under unchanged confirmed requirements and cases
  made infeasible by the change, alongside matched healthy controls.

The two coverage choices above are confirmed in P02-D005–D006. The following
implementation/evaluation procedures are proposed and still require specification:

- Establish feasibility with an evaluator-side numerical check using the defined
  plant and information assumptions. Do not infer infeasibility from a single
  controller's failure, and do not expose evaluator-only truth to agents.
- Select numeric deratings and episode durations after checking device response
  and achievable recovery. Do not claim arbitrary percentages represent realistic
  field failure severities. Numeric levels must be frozen before final evaluation.

## Non-equipment scenario scope

| Family | Initial cases and approval status | Isolation boundary |
| --- | --- | --- |
| Preference update | Confirmed: temperature-target/band update; EV departure or charge-target update. | Version the preference contract at confirmation; keep equipment healthy in isolated cases. |
| Forecast error | Confirmed: errors in PV, outdoor-temperature and fixed-load forecasts | Modify only the forecast stream available to scheduling; preserve the realized plant/input trajectory in the matched comparison. Validate forecast issue times first. |
| Twin model mismatch | Confirmed: thermal-response mismatch and battery-efficiency mismatch in the Operational Twin | Keep plant behavior and frozen Reference Twin unchanged; version the inaccurate Operational Twin configuration. Specific model parameters require an audit. |
| Scheduling/coordination failure | Confirmed: delayed/missing plan update and stale preference/plan version | Inject at a defined plan-delivery interface; keep validator enabled. Count rejection as containment, not as execution of an unsafe plan. |

These are project-design choices, not article-derived findings. A
Reference Twin may already have ordinary approximation error; model-only injected
mismatch must be distinguished from that baseline error. The forecast cases do
not assume that all three forecast streams currently exist or are leakage-free.

Forecast/model-only changes do not by themselves change physical feasibility
when the plant, realized inputs and confirmed requirements are fixed. Separate
true infeasibility from a controller's mistaken belief that a feasible task is
infeasible, or its failure to find a schedule. Not every family must have a
physically infeasible isolated variant.

## Confirmed accounting, combinations and selection rules

### Battery accounting

For initial capacity-loss cases, preserve stored energy in kWh and select onset
states whose stored energy fits within the reduced usable capacity; update the
normalized state-of-charge consistently. Do not silently clip or create energy.
Document excluded state/severity combinations. Cases with stored energy above
the new capacity need a separate explicit physical/accounting rule and are deferred
under P02-D010. For efficiency loss, initially derate both charging and
discharging conversion efficiencies, respecting the simulator's actual parameter
semantics rather than assuming a round-trip value is a one-way efficiency.

### Selected combinations

Confirmed simultaneous shortlist: HVAC capacity loss plus PV forecast error; battery
capacity loss plus battery-efficiency model mismatch; a confirmed earlier EV
departure plus delayed schedule delivery. Each requires its isolated controls
and a joint case. The preference update remains a legitimate change, not a fault.

Conditionally selected cascade: HVAC capacity loss changes operation, producing EV charging
shortfall risk through shared electrical constraints. Validate that causal path
before retaining this case; do not inject a second fault merely to force a
cascade. A reduced plant capability does not imply that a software action can
repair the equipment. Evaluate permissible mitigation and honest infeasibility
reporting; repairs require an explicitly modeled intervention.

### Severity and timing selection

Confirmed rule: choose numeric settings using independent simulator pilots and
predefined physical/feasibility criteria, then freeze the scenario manifest
before comparative evaluation. Do not tune cases to favor the proposed method.
Use multiple severity levels where meaningful, record units and denominators,
and retain cases where degradation is contained without a service violation.
Exact levels, onset/duration profiles, resets and reproducible episode windows
must be recorded during validated benchmark construction; they are not finalized
by agreeing a scope or selection rule.

## Required numeric manifest and validation gate — P2

- Family and exact mechanism; injected root cause versus downstream consequences.
- Plant, model, forecast, preference or coordination component being changed.
- Onset, duration, severity, persistence and reset behavior.
- Healthy counterpart and checks that only intended mechanisms changed.
- Expected symptoms and alternative explanations; information access finalized in P0.3.
- Initial feasibility, post-change feasibility and achievable corrective responses.
- Simultaneous/cascade composition and dependency graph where applicable.
- Simulator support and validation needed; evaluator-only injection truth kept separate.

The researcher approved deferring numeric realization through P02-D012. The
fields above are mandatory before final evaluation; completing P0.2 does not
waive them or claim the injectors work.

## Mechanism checks and episode lifecycle

For every isolated mechanism, retain a matched no-injection run and compare
configuration changes, trajectories and energy accounting. Expected symptoms
are test expectations, not guaranteed observations: HVAC loss may impair thermal
tracking; EV power loss may slow charging; battery losses may reduce available
support or increase energy losses; PV derating may reduce generation. Forecast
and Twin errors may produce prediction residuals; delivery/version faults may
produce missing acknowledgements or validator rejections. Each symptom can have
other explanations, so symptom presence alone is not a diagnostic label.

Every scenario manifest must specify onset, persistence, release/repair behavior
and reset. A new matched episode restores the healthy configuration and defined
initial state; never carry an injected fault or modified Twin into another run
unintentionally. A temporary fault's release is not evidence that the controller
repaired it. Gradual/temporary capacity cases must obey the confirmed accounting
restriction throughout the trajectory. The Reference Twin remains frozen in
model-only mismatch cases; hypothetical rollouts must not mutate the plant.

For simultaneous cases, retain healthy, each isolated component, and combined
conditions. For cascades, validate intermediate links and the shared constraint;
do not count a downstream symptom as a separately injected root cause. If the
selected cascade is unsupported, record that limitation and seek a revised case
rather than silently claiming cascade coverage.

## Completion and next task

P0.2 design is complete with P02-D001–D012 and the recorded researcher answers.
Open implementation dependencies are simulator/device validation, numeric pilot
manifests, feasibility checks and injector tests in P1/P2. Detailed information
access, interfaces and metrics remain P0.3–P0.5. No simulator changes were made.

Next: [P0.3 — information access](INFORMATION_ACCESS_SPECIFICATION.md).
