# P0.3 — Information access

Version: 1.0 — agreed access-policy design, 2026-11-16.
Status: P0.3 complete as a design task; channel mappings and leakage checks remain validation gates.

This task follows the [agreed scope](RESEARCH_SPECIFICATION.md) and
[degradation design](DEGRADATION_SPECIFICATION.md). It defines information
boundaries before choosing exact observation names from the audited simulator.

## Confirmed decisions

| ID | Researcher decision | Consequence |
| --- | --- | --- |
| P03-D001 | Keep injected fault labels, true degraded parameters, injection onset/severity, future realized trajectories and privileged feasibility results evaluator-only. | Runtime agents use legitimate observations, confirmed preferences, issued forecasts and model tools. Any hidden-truth oracle must be separately labeled. |
| P03-D002 | Adopt indoor/outdoor temperature, occupancy, EV connection/reported charge, battery reported charge, available device/grid/PV power measurements, and command/acknowledgement/version logs, subject to channel validation. | Map each channel to validated support. Document missing channels instead of assuming availability. |
| P03-D003 | Start with exact approved measurements, then add selected noise, missing-data and delay tests. | Exact measurements do not authorize reading arbitrary hidden simulator state. Robustness cases are part of the intended study, staged after the clean observation baseline. |
| P03-D004 | Use a shared timestamped evidence store with role-specific tool views. | Apply the same hidden-truth boundary to every role; document comparable evidence eligibility for controller comparisons and retain provenance/tool-access logs. |
| P03-D005 | Initialize and synchronize both Twins from approved observations and permitted history; estimate unobserved states. | No copying hidden plant states or injected degraded parameters. Privileged initialization, if studied, is a separately labeled oracle. |
| P03-D006 | Allow competing causes, unknown outcomes and abstention when evidence is insufficient. | Do not force one known-fault label. Confidence thresholds and response/evaluation contracts remain P0.4–P0.5 decisions. |
| P03-D007 | Use resident-declared future occupancy/EV plans with current observations and clarification of consequential missing details. | Label plans as intentions; never substitute hidden future realized schedules. |
| P03-D008 | Use a bounded recent history window with bounded, logged retrieval of older eligible evidence. | Select window lengths and retrieval budgets through independent pilots, freeze before comparison, and document equivalent retrieval opportunities. |

## Access matrix

The hidden-truth boundary, evidence routing and observation-based Twin state
initialization are confirmed in P03-D001 and P03-D004–D005. History policy is
confirmed in P03-D008; numeric limits and exact fields require pilot selection
and validation before comparison.

| Information | Runtime access policy | Boundary |
| --- | --- | --- |
| Confirmed preference contract and updates | Relevant agents, optimizer and validator | Expose confirmed versions and timestamps; a resident update is not a hidden fault label. |
| Current/past measurements and command/acknowledgement logs | Via explicit observation and tool interfaces | Only channels available by the decision time; distinguish measured values from model estimates. Exact channel list remains open. |
| Forecasts and published tariff schedules | Issued forecasts and schedules available by decision time | Preserve issue time, target time and provenance. Future realized weather, PV and loads are not forecasts. |
| Reference/Operational Twin configuration and predictions | Via model tools and versioned metadata | Model assumptions are visible as assumptions; injected true plant parameters are not silently copied into the model. |
| Fault labels, injection mechanism/severity/onset and scenario selection | Evaluator only | Do not expose labels through prompts, tool payloads, filenames or scenario identifiers. Genuine device alarms, if modeled, are separate observations. |
| Future realized trajectories and privileged feasibility checks | Evaluator only | Never feed evaluator truth into ordinary diagnosis or schedule selection. Any oracle comparison must be separately labeled. |

The plant's true degraded parameters may be latent while the controller's nominal
ratings remain known. Actual measurements can reveal evidence of degradation;
the policy should hide injected answers, not remove legitimate diagnostic evidence.

## Initial measurement contract

P03-D002 confirms the channel categories, not a claim that every simulator field
is already available. For each mapped channel, record source, units, sampling and
arrival times, measurement/estimate status and missing-value behavior. Reported
charge must have an explicit denominator: do not silently provide true degraded
capacity through a normalized charge reading. If a modeled battery-management
measurement reveals capacity, identify that as a deliberate observation channel.

Current occupancy and EV connection observations do not automatically provide
perfect future occupancy/arrival schedules. A confirmed resident departure plan
can be available as a declared plan, with provenance; it is not future realized
truth. P03-D007 confirms declared plans, current observations and clarification
as the future-availability information policy.

## Confirmed evidence and diagnosis policies

- Use a shared, timestamped evidence store with role-specific tool views. All
  agents and controller variants obey the same runtime eligibility boundary;
  role specialization does not grant evaluator-truth access. Record tool calls
  and evidence provenance so information differences are auditable.
- Initialize and synchronize Twin states from approved observations and permitted
  history. Estimate unobserved states; do not copy hidden plant states or injected
  degraded parameters into either Twin. Any privileged state-initialization study
  is a separate oracle experiment, not the main result.
- Permit multiple competing cause hypotheses, an unknown/unmodeled-cause outcome
  and abstention when evidence is insufficient. A posterior ranking or tool output
  is not ground truth. Thresholds, scoring and responses follow in P0.4–P0.5.

The Reference Twin's model parameters remain frozen; updating its estimated
current state from permitted observations is distinct from recalibrating its
parameters. P03-D005 authorizes the information basis for state estimation, not
automatic model recalibration. Unknown cause and abstention are also distinct:
unknown expresses that modeled causes do not adequately explain evidence;
abstention withholds a sufficiently confident diagnosis. Neither is a physical
fault label, and both need explicit scoring rules.

## Confirmed future-information and history policies

- Use current measured occupancy/EV connection and resident-declared future plans.
  Treat future plans as declared intentions, not perfect realizations. When a
  consequential future availability window is unspecified, ask for clarification
  or expose the assumption before confirmation; never read future simulator rows
  to fill it in silently.
- Use a bounded recent history window plus logged retrieval of older eligible
  evidence through tools. Select window lengths and retrieval budgets through
  independent pilots, then freeze them before comparison. Apply the same eligibility
  rules and document equivalent retrieval opportunities across compared methods;
  a shared store does not imply unlimited context or free information processing.
  Warm-up uses only permitted past data and must be documented separately from
  scored control intervals.

## Validation requirements — not executed

Before comparative runs, audit the observation/tool adapters for future-row access,
scenario filenames/IDs, hidden fault metadata and accidental plant-state copying.
Check measurement time versus arrival time when delays are introduced. Keep
evaluator labels in a separate logging path unavailable to ordinary runtime tools.
Verify that Twin hypothetical rollouts cannot mutate the real plant or expose
future realized exogenous inputs. Record missing channels and resulting scope
limitations before freezing experiments.

## Deferred implementation details and completion

- Map exact simulator channels and define units, timestamps and tool schemas in
  P0.4 and simulator validation; unsupported measurements remain explicit limitations.
- Select numeric history windows and retrieval budgets through pilots and record
  them in the frozen experiment configuration before comparative evaluation.
- Implement and execute leakage checks before reporting runtime results.
- Define unknown-cause/abstention thresholds and evaluation in P0.4–P0.5.

P0.3 is complete with P03-D001–D008 and the recorded researcher answers. This
records access-policy agreement, not validated adapters or proven absence of
leakage. Next: [P0.4 component contracts](COMPONENT_CONTRACTS.md).
