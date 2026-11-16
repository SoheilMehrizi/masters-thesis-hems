# P0.4 — Component contracts

Version: 1.0 — agreed component contracts, 2026-11-16.
Status: P0.4 complete as a design task; numerical realization remains a validation gate.

Sources of agreed design: [research scope](RESEARCH_SPECIFICATION.md),
[scenario design](DEGRADATION_SPECIFICATION.md), and
[information access](INFORMATION_ACCESS_SPECIFICATION.md).

## Confirmed P0.4 decisions

| ID | Researcher decision | Consequence |
| --- | --- | --- |
| P04-D001 | Allow automatic independently validated stationary-battery charging/discharging schedules within unchanged operating limits and resident requirements. | Extends routine scheduling authority beyond HVAC/EV. Does not authorize changing limits, true degradation parameters or preference bounds. |
| P04-D002 | Automatically fit/test Operational Twin candidates in isolation; require approval before active promotion initially. | Candidate generation is not deployment. The frozen Reference Twin's parameters remain unchanged; candidate validation and rollback contracts are still required. |
| P04-D003 | Allow active device probes only under an explicitly approved bounded policy. | The policy must define devices, amplitudes, durations and budgets. Every probe still needs independent checks and cannot relax confirmed hard requirements. No numeric probe policy is approved yet. |
| P04-D004 | Use receding-horizon execution with event-triggered replanning. | Execute only the next validated control interval; observe and replan. Select numeric horizons through pilots and explicitly address EV deadlines beyond the immediate horizon. |
| P04-D005 | Use independently validated deterministic fallback with explicit failure reporting. | Earlier plans may be reused only if still valid. Fallback does not guarantee recovery or authorize changing resident hard requirements. |
| P04-D006 | Allow bounded conditional multi-step plans with stepwise validation. | Each step needs preconditions, authority and validation; later steps cannot bypass promotion approval or probe limits. |
| P04-D007 | Use a linear/piecewise-linear scheduling model with LP/MILP as needed and independent validation. | Validate the approximation against Twin predictions and actual outcomes. Preserve CityLearn dynamics; exact coefficients, solver and numerical settings require validation. |
| P04-D008 | Count active-band comfort violations immediately at initialization or occupancy-window start; no implicit grace period. | Report recovery feasibility and plan recovery. Announced occupancy can permit preconditioning; any different allowance requires explicit confirmation. |
| P04-D009 | Run deterministic monitoring each control interval and trigger LLM diagnosis on violations, predicted requirement risks, significant residuals or execution failures. | Routine optimization need not invoke the LLM every interval. Pilot-select and freeze trigger thresholds and call budgets. |

Confirmed decision P04-D010: the researcher approved the consolidated interface
inventory, lifecycle, scheduling requirements and data conventions on 2026-11-16,
and requested progression to P0.5. This completes P0.4 design, not implementation.

## Agreed contract summary

The system uses typed, versioned records and independently validated, stepwise
execution. It schedules HVAC, EV and battery automatically within unchanged
requirements. Operational Twin candidates may be fitted/tested automatically;
active promotion needs approval initially. Device probes require a separately
approved bounded policy. Hard-requirement changes require resident confirmation.

The scheduler is a receding-horizon LP/MILP using a validated linear or piecewise-
linear approximation. Deterministic monitoring runs each interval; LLM diagnosis
is event-triggered. Corrective plans may branch across multiple validated steps.
Failures use a validated deterministic fallback and explicit reporting. Comfort
violations count whenever the confirmed band is active, with no hidden grace.

The interface inventory, lifecycle and unit/time conventions below are confirmed
in P04-D010. Numeric tolerances, probe policies, exact simulator
mapping and executable schemas remain required implementation/validation artifacts,
not claims of completed implementation.

## Already confirmed boundaries

- Natural-language preferences become confirmed hard requirements and soft
  priorities; relaxing resident hard requirements needs permission.
- LLM agents interpret, diagnose and select interventions. A constrained
  optimizer schedules; an independent validator checks candidate actions.
- Validated HVAC/EV scheduling within unchanged requirements may run automatically.
- Physical/equipment safety limits remain enforced. The Reference Twin's model
  parameters stay frozen; its estimated current state may use permitted evidence.
- Hidden evaluator truth remains outside runtime tools. Unknown diagnoses and
  abstention are permitted; model predictions alone do not establish recovery.

## Scheduling model contract

Use eligible initial-state estimates, forecasts, confirmed preferences and
versioned model coefficients to construct a finite-horizon constrained schedule.
The default objective is net electricity cost using declared import/export
tariffs and actual interval durations; confirmed resident priorities override
that default. Do not invent export remuneration when the tariff does not define it.

The formulation must represent household power balance; device availability,
power and energy bounds; battery/EV state transitions and conversion losses;
thermal-response approximation; occupied comfort bounds; and the confirmed EV
charge target at its deadline. Use linear or piecewise-linear dynamics, introducing
integer variables only where the chosen device/mode formulation requires them.
Exact coefficients, device-mode rules and approximation error require audits and
validation. This does not replace the plant's original LSTM or authorize model
fitting from hidden fault labels/true degraded parameters.

For horizons ending before an EV deadline, either extend the horizon with explicitly
available forecast/assumption provenance or include a documented terminal
reachability constraint. Never assume perfect future inputs to establish
reachability. A feasible schedule means feasibility under stated model assumptions,
not guaranteed real-plant compliance. The independent validator checks candidate
constraints/authority using permitted information; it cannot rely on hidden plant
truth. Observe actual outcomes and score violations separately.

Do not silently soften hard bounds with optimization penalties. When the present
state already violates a bound, retain that violation in the log and report
whether future restoration is feasible. Distinguish a modeled recovery trajectory
from an approved revision of the resident's requirements; a recovery plan does
not erase violations along that trajectory. Emergency/degraded-mode behavior
must preserve physical limits without labeling unmet requirements as satisfied.

## Comfort activation and diagnosis triggers

The confirmed temperature band is evaluated from the start of its active window,
including episode initialization. No unconfirmed transition allowance or grace
period is introduced. Use declared occupancy plans for preconditioning where
feasible; unforeseen occupancy can make immediate compliance impossible. Log
that condition and apply the confirmed conflict/recovery procedure.

Monitor approved observations, execution status, residuals and predicted risks
each control interval. Invoke diagnosis on the agreed event categories, with
thresholds, persistence/debounce rules and call budgets selected through pilots
and frozen before comparison. Log trigger inputs, reasons and suppression events
so that efficiency measurements include missed/late detection and not only saved
LLM calls. Preference interpretation remains an LLM role when a new natural-
language request arrives; event-triggered diagnosis does not remove that role.

## Agreed interface inventory

| Contract | Proposed essential content |
| --- | --- |
| Preference contract | Version, confirmation event, active windows, hard bounds, soft priorities, provenance and superseded version |
| Observation record | Channel, value, unit, measurement time, arrival time, source, quality and measured/estimated status |
| Forecast record | Issue/arrival times, target interval, variable, values, units and provenance |
| Diagnosis report | Competing causes, evidence references, uncertainty semantics, unknown/abstention status and model version |
| Intervention proposal | Typed action, target, parameters, preconditions, required authority, expected effect, risks and verification/rollback conditions |
| Twin evaluation | Initial estimated state and uncertainty, model/state versions, hypothetical action sequence, forecast version and predicted outcomes |
| Optimizer request/result | Preference/model/forecast versions, initial state, horizon, constraints/objective, solution or failure status and solver metadata |
| Validation decision | Candidate hash/version, checked constraints and authority, validity window, rejection reasons and validator version |
| Execution/verification log | Actual accepted commands, acknowledgement/status, timestamps, measured outcomes and whether recovery was verified |

These fields define the agreed interface inventory. Executable JSON schemas,
complete enumerations and numeric tolerances remain implementation artifacts.

## Authority contract

Routine battery scheduling is authorized by P04-D001 under the same independent
validation and unchanged-requirement boundary as HVAC/EV scheduling. Isolated
Operational Twin candidate fitting/testing is authorized, using only permitted
runtime evidence; promotion waits for approval tied to the specific candidate
version and validation report. Do not treat an expired or different candidate's
approval as transferable. No promotion is implied merely by a favorable fit.

Active physical/simulated-device probes wait for a separately approved bounded
policy. A hypothetical rollout remains isolated computation, not a device probe.
Scheduling that deliberately changes operation to obtain diagnostic information
must be labeled as probing rather than bypassing probe policy as routine control.
Numeric probe limits and approval scope remain explicit open gates.

Including a degraded device in the benchmark is not authorization to alter its
model, actively probe it or claim a software command physically repairs it.

## Confirmed execution policies

- Receding-horizon scheduling: plan ahead, execute only the next validated control
  interval, observe actual outcomes and replan. Confirmed preference updates,
  material new evidence and invalid/stale plans can trigger replanning sooner
  than the ordinary cycle. Select numerical horizons and triggers through pilots;
  retain EV deadline reachability through horizon coverage or an explicit terminal
  feasibility condition, without reading future realized inputs.
- If the LLM/planner fails or a candidate is rejected, use a deterministic fallback
  controller whose actions are also independently validated. Reuse an earlier plan
  only when it remains current and valid under current evidence and authority.
  If no action can satisfy all requirements, report the conflict, preserve physical
  limits and seek approval before relaxing resident hard requirements. Log actual
  violations; fallback is not a guarantee of comfort or deadline satisfaction.
- Permit bounded conditional multi-step intervention plans: each step has typed
  parameters, evidence-based preconditions, authority, a validation gate and an
  observed-outcome check before the next branch. Future steps do not inherit a
  blanket approval to relax requirements, promote models or exceed probe limits.

## Execution lifecycle and failure statuses

1. Capture a versioned snapshot of eligible evidence, confirmed preferences and
   current model/authority versions. Produce a typed candidate plan.
2. Validate its structure, numerical constraints, version compatibility and
   authority. Twin evaluations retain their own input/model versions; favorable
   predictions do not override a rejected authority or physical-limit check.
3. Immediately before dispatch, check freshness and versions again. A plan whose
   preference/model/authority dependencies changed needs revalidation or replanning.
4. Dispatch only the next approved interval/step. Record acceptance, acknowledgement
   and observed effect separately; a sent command is not proof it executed.
5. Verify the measured outcome before branching. Stop or replan when preconditions
   fail; log fallback activation and its reason.

Distinguish optimizer infeasibility, timeout, numerical error and feasible-but-not-
proven-optimal results. A timeout without a solution is not proof of infeasibility.
A feasible incumbent may be considered only after the same independent checks.
Keep validator rejection, stale evidence, missing acknowledgement, diagnostic
abstention and observed requirement violation as separate statuses. Neither
abstention nor a missing LLM response is itself a fault diagnosis.

If no action passes all checks, report that condition rather than inventing a
universally safe zero action or executing a rejected command. The simulator-
specific degraded-mode/fallback behavior must be validated and its unresolved
requirements logged; nominal feasibility is not a physical guarantee.

## Data conventions

Use degrees Celsius for temperature, kW for power, kWh for energy and explicit
currency units for costs. Represent normalized charge with a declared denominator
and range. Separate nonnegative charge/discharge and import/export fields in
contracts; record adapters to native simulator signs instead of changing vendor
semantics. Distinguish instantaneous/state samples from interval-average power
and integrated energy; conversions use the actual timestep duration.

Every record needs an episode identifier, scenario-relative step, relevant event
and availability times, provenance and version references. Absolute timestamps
must preserve the audited scenario calendar/timezone; never substitute the chat
clock. Use explicit start-inclusive/end-exclusive interval boundaries, subject
to tested adapters at simulator boundaries. Unknown timezone/alignment is an
unresolved validation issue, not a guessed UTC offset.

## Completion evidence and deferred artifacts

P04-D001–D010 and the researcher's consolidated confirmation complete P0.4 as a
design task. This does not claim implemented or validated components.

Required later artifacts include executable schemas/adapters; audited calendar,
timezone and timestep mapping; validated scheduler/validator/fallback behavior;
model-candidate validation/promotion/rollback implementation; and pilot-selected
horizons, thresholds, tolerances and probe-policy bounds. Probes remain disabled
until a bounded policy is explicitly approved. Unsupported simulator capabilities
must be recorded and resolved rather than assumed available.

No simulator behavior was altered during this contract interview. After contract
review, [P0.5](EVALUATION_SPECIFICATION.md) defines hypotheses, comparisons,
metrics and experiment versioning.
