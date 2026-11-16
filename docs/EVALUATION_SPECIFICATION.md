# P0.5 — Hypotheses and evaluation

Version: 1.0 — agreed evaluation design, 2026-11-16.
Status: P0.5 complete; P0 design complete. Numeric protocol must be frozen before evaluation.

Builds on the [research scope](RESEARCH_SPECIFICATION.md),
[scenario design](DEGRADATION_SPECIFICATION.md),
[information policy](INFORMATION_ACCESS_SPECIFICATION.md) and
[component contracts](COMPONENT_CONTRACTS.md). These are proposed experiments,
not literature findings or demonstrated improvements.

## Confirmed P0.5 decisions

| ID | Researcher decision | Consequence |
| --- | --- | --- |
| P05-D001 | Primary measure: verified recovery success rate on independently classified recoverable episodes; report violations and overhead separately. | Freeze verification/deadline rules and retain all eligible assigned episodes. Assess infeasible cases separately for conflict handling. |
| P05-D002 | Adopt full system, diagnosis-free LLM replanning, optimizer-only receding-horizon control and rule-based HEMS as core methods. | Use matched scenarios and documented comparable evidence eligibility. Paper-derived diagnostic baselines remain a separate selection. |
| P05-D003 | Include no-SCM, no-hypothetical-Twin-ranking, passive-only and single-action ablations. | Probing comparisons are conditional on an approved bounded policy. Keep the optimizer's predictive model when removing intervention Twin ranking. |
| P05-D004 | Include both adapted Bayesian-network and explicit rule-based diagnostic baselines. | Substitute the diagnostic engine in an otherwise matched workflow; document adaptation fidelity rather than claiming exact paper reproduction. |
| P05-D005 | Establish the hierarchical core first; topology comparisons are supplementary. | Core contribution does not depend on demonstrating superiority across centralized/hierarchical/decentralized architectures. |
| P05-D006 | Separate development and held-out evaluation, including selected generalization cases. | Use non-overlapping windows/controlled seeds, prevent history/forecast leakage, and keep unknown-cause tests separately specified. |
| P05-D007 | Separate matched reactive-recovery and proactive-prevention suites. | Primary recovery starts from common already-violating but recoverable states; prevention evaluates early action separately. Do not select the primary cohort using method-specific outcomes. |
| P05-D008 | Use paired method differences, 95% uncertainty intervals and pilot-based repeat counts, with family/severity breakdowns. | Account for related weather windows/episodes; timesteps are not independent replicates. Select a meaningful target effect in independent pilots. |
| P05-D009 | Require frozen reproducibility manifests and complete run/approval logs. | Record failures, retries and human-response delays. Later tuning creates a new study version; simulated responses require an explicit policy. |
| P05-D010 | Confirm the consolidated hypotheses, endpoint formulas, statistical plan and reproducibility/realization gates; complete P0 design. | P0.5 is complete as a design task. Numerical manifests, source-specific fidelity, schemas and simulator validation remain required before evaluation. Next implementation task: P1.4. |

## Agreed evaluation plan

The primary endpoint is observed verified recovery success on a fixed recoverable
reactive cohort; proactive prevention and infeasible-case handling are separate
suites. Compare four core methods, two adapted diagnostic-engine baselines and
four contribution ablations. Use the hierarchical core first, separated development
and held-out evaluation, paired uncertainty reporting and immutable manifests.
Probing comparisons remain conditional on bounded-policy approval; topology and
Jev experiments are supplementary.

P05-D001–D010 confirm the scope, endpoint formulas, directional hypotheses,
failure treatment and completion gates below. The researcher approved the
consolidated plan on 2026-11-16. No experiment results, numerical effect claims or validated performance
are asserted.

## Primary endpoint and scoring details

Verified recovery success rate among independently labeled recoverable episodes,
using a frozen observation window/cutoff and confirmed EV deadline. Include
every assigned eligible episode, including method failures/timeouts; do not drop
failed runs. Use observed outcomes, not predicted Twin recovery. Unauthorized
requirement changes or physical-safety violations cannot produce a valid success.

A prior preference violation is not erased by recovery: report magnitude and
duration separately, including initialization/occupancy transitions. Define
comfort/deadline success, post-deadline observation requirements and verification
windows before evaluation. Report infeasible cases separately for correct conflict
reporting, false feasibility claims and authorized negotiation. Conflict reporting
does not count as restoration success.

## Confirmed core comparisons

| Method | Intended role |
| --- | --- |
| Rule-based HEMS | Simple operational reference with explicit device/priority rules |
| Optimizer-only receding-horizon control | Same scheduling model/validator, routine updates but no LLM diagnostic intervention workflow |
| Diagnosis-free LLM replanning | Comparable LLM/tools/optimizer, with causal diagnosis removed and no hidden cause labels |
| Full system | Explicit Dynamic SCM, permitted Twin-tested interventions and agreed contracts |

Match scenario instances, evidence eligibility, device limits and confirmed
requirements. Record tool, budget and model differences. These references do not
imply reproduction of named papers. Adapted Bayesian/rule diagnostic baselines
are confirmed below; additional paper-derived HEMS reproductions remain candidates.

## Ablation scope and directional hypotheses

| ID | Testable direction, not a claimed result | Controlled comparison |
| --- | --- | --- |
| H1, primary | Full system has higher verified recovery success rate | Full system versus diagnosis-free LLM replanning |
| H2 | Twin-tested selection improves intervention outcomes | Full system versus removal of hypothetical Twin intervention ranking |
| H3 | Selective probing improves recovery/diagnosis, with probe overhead reported as a separate tradeoff | Probing-enabled versus passive-only, after bounded policy approval |
| H4 | Conditional multi-step plans improve recovery | Same controller/evidence with plan restricted to a single action |

Removing Twin intervention ranking does not remove the optimizer's predictive
model or actual outcome measurements. Removing the SCM must not retain its
diagnostic outputs through shared records. Freeze each variant's remaining tools,
prompts, triggers and budgets before experiments.

The no-SCM ablation and diagnosis-free LLM core baseline may coincide only if
their exact evidence, tools, prompts, intervention library and budgets coincide.
Document that equivalence and reuse the condition rather than counting duplicate
labels as independent experiments. A deliberately different implementation must
have its differences specified before results are interpreted.

## Confirmed diagnostic baselines

Add a Bayesian-network diagnostic engine and an explicit rule-based diagnostic
engine, each substituted for the Dynamic SCM within an otherwise matched control
workflow. Use the overlapping observation/cause scope and mark unsupported or
unobservable diagnoses. Separate diagnostic accuracy from downstream recovery;
keep the optimizer, validator and intervention authority comparable.

These are confirmed adaptation directions informed by the library's diagnostic literature,
including the [Bayesian HVAC report](literature/article-03.html) and
[AFDD report](literature/article-05.html). They are not claims of reproducing
published HVAC experiments on a home-energy benchmark. Before implementation,
record source-specific mechanisms retained, changed and omitted, and engineering
extensions for EV/battery/PV. A generic Bayesian network must not be presented as
an exact reproduction of a named article.

## Confirmed topology and split policy

Start with a fixed hierarchical agent workflow to establish the diagnosis/
intervention contribution. Treat centralized-versus-hierarchical-versus-
decentralized topology comparisons as a supplementary study after the core
method works, with comparable evidence/tools and recorded compute budgets.

Separate model fitting/calibration, development pilots and final evaluation using
non-overlapping time windows and controlled scenario seeds. Reserve final cases
before tuning; prevent overlapping history/forecast targets from leaking across
splits. Include heating- and cooling-relevant periods if the validated data allow.
Reserve selected severities/combinations for generalization tests, and introduce
unmodeled mechanisms only under a separately specified unknown-cause protocol.
Do not infer multi-home generalization from this single-home study.

The frozen Reference Twin and baseline models must not be fitted to held-out
truth. Permitted online Operational Twin adaptation uses only past runtime
evidence and the agreed promotion policy; log approval timing and count its
latency consistently across methods. No final outcome may be used to select
thresholds, prompts or scenario severities without declaring a new study version.

## Confirmed scoring and statistical policies

### Recovery versus prevention

Use a predeclared reactive-recovery cohort with common already-violating initial
conditions at method handover, restricted to independently established recoverable
cases. This keeps the primary denominator fixed across methods. Define time zero
and the restoration/verification window in the manifest. Do not classify episodes
for inclusion based on whether a particular method later violates a requirement.

Evaluate proactive prevention in a separate matched suite, allowing controllers
to act before violations. Report sustained requirement satisfaction, prevented/
incurred violations, deadline success and interventions there; do not call a
never-violating episode a measured recovery. Include healthy/benign-disturbance
controls to assess false alarms and unnecessary interventions.

The reactive cohort does not evaluate early detection before handover. The
prevention suite supplies that evidence. Cost-only disturbances with no affected
hard requirement must not inflate the primary recovery denominator. A missed EV
deadline cannot be repaired retroactively by later charging.

### Paired reporting

Use matched scenario/seed instances across methods, report paired effect sizes
with 95% uncertainty intervals, and stratify by family, severity and feasible/
infeasible status. Resampling/inference must account for shared weather windows
or common initial episodes; individual timesteps are not independent replicates.
Freeze the pooling weights and primary comparison before results. Use a separate
development pilot to set repeat counts and a practically meaningful target effect;
do not invent a numerical improvement claim in advance of that design work.

Choose the exact interval/test implementation before final evaluation. Treat H1
as the primary comparison; H2–H4 are secondary contribution tests. Declare
multiplicity handling for confirmatory secondary tests and label exploratory
analyses. Record stochastic LLM settings and repeated-run seeds; determinism of
the simulator does not guarantee identical external-model responses.

### Reproducibility and approvals

Freeze versioned manifests before final runs. Include immutable code/config and
data identifiers, model/provider identifiers and sampling settings, prompts/tools,
SCM/Twin/optimizer/validator versions, initial states and input splits, budgets,
history/retrieval settings, fault scenarios, metric formulas and approval policy.
Retain all failures, timeouts, retries, tool calls and human approvals with costs.
No post-result prompt/threshold tuning is silently folded into the same study.

Operational Twin promotion approvals require a consistent evaluation protocol
across applicable methods. Record pending approvals, response delay and denial;
report operator waiting time separately from compute time and simulated recovery
time. Never fabricate user approval to make an episode finish. A scripted
resident/operator may be used only under a separately explicit frozen policy,
not passed off as observed human responses.

## Supporting metrics

- Comfort violation magnitude/duration; EV target shortfall and deadline success.
- Physical-limit violations and unauthorized actions/requirement changes.
- Time to verified recovery, non-recovery frequency and repeated degradation.
- Root-cause ranking/multi-cause performance, unknown detection and abstention;
  probability calibration only for outputs with defined probabilistic semantics.
- False alarms, missed/late triggers, unnecessary interventions and probe overhead.
- Electricity cost, grid energy, PV utilization and storage throughput, with units.
- End-to-end latency, optimizer runtime, LLM calls/tokens, retrieval and Twin-rollout
  costs; distinguish simulated control time from wall-clock execution time.

Time-to-recovery analysis must retain non-recovery under a predeclared censoring/
failure rule, not average only successful episodes. Define unnecessary interventions
using evaluator-side control/counterfactual criteria, not LLM self-description.
The metric definitions below are agreed in P05-D010; numeric windows,
tolerances and exact inference implementation must be frozen before evaluation.

## Endpoint and supporting metric definitions

- Recovery rate: successful assigned eligible episodes divided by all assigned
  eligible episodes in the fixed reactive cohort. Success requires restoration
  by the frozen cutoff, observed satisfaction over the verification window and
  the confirmed EV target at its deadline, where applicable. Physical-safety
  violations and unauthorized changes invalidate success. A relaxation approved
  after onset is logged as negotiated resolution, not restoration of the original
  requirements. Require sufficient post-restoration observation in the manifest.
- Primary effect: full-system recovery rate minus diagnosis-free LLM recovery
  rate on matched episodes, in percentage points. H1 proposes a positive effect;
  no minimum numerical gain is claimed. Pilot-select the practically meaningful
  target effect and sample size before final evaluation, with no final-data tuning.
- Comfort burden: integrate max(lower bound minus temperature, zero) plus
  max(temperature minus upper bound, zero) over active occupied intervals, using
  timestep hours, yielding degree-hours. Also report violating duration, maxima
  and recovery-phase burden. Never remove onset/arrival violations retrospectively.
- EV outcome: observed energy shortfall at the confirmed deadline, in kWh, plus
  deadline success under the frozen tolerance and declared usable-capacity
  semantics. Later charging cannot repair a missed deadline.
- Recovery timing: elapsed simulated time from common handover to the beginning
  of a subsequently verified restoration interval; also record when verification
  completes. Use a frozen failure/censoring rule for non-recovery and report its
  frequency. Do not compare successful-only means as the sole timing result.
- Cost/energy: integrate measured interval power with duration and declared tariffs;
  distinguish imports, exports and conversion losses. Fix export remuneration,
  PV-utilization denominator and storage-throughput convention in the manifest.
- Diagnostic outcomes: compare cause sets/rankings to evaluator truth, separating
  injected roots from consequences, legitimate preference changes, unknown causes
  and abstention. Fix cause ontology, multi-cause scoring and observable-scope
  restrictions. Assess probabilistic calibration only for defined probability
  outputs; LLM confidence prose is not automatically a probability.
- Intervention burden: count and type executed interventions/probes, failed
  attempts and repeated actions. Label an action avoidable only under a frozen
  evaluator-side omission/replay rule that preserves the relevant goals and
  safety conditions; report unassessable cases rather than inventing labels.
- Overhead: report LLM calls/tokens, retrieval, Twin rollouts, solver time, retries,
  wall-clock latency, simulated recovery time and operator waiting separately.
  Record actual spending only with applicable provider/tariff provenance.

For pooled comparisons, freeze family/severity weights; also show stratified
results. H1 is the primary confirmatory contrast; H2–H4 are secondary. Fix the
interval estimator, dependence grouping and multiplicity rule before final runs.

## Mandatory realization gates after design approval

Before comparative evaluation, require a reviewed manifest with exact episode
windows/splits, supported channels, initial states, injection parameters, numeric
verification windows/cutoffs, thresholds, budgets, tolerances, repeat counts,
seeds, pooling weights and statistical implementation. Include source-specific
baseline fidelity records and exact unknown-cause/abstention protocols. An unknown-
cause test must state which mechanism is withheld from the diagnostic ontology,
training/rules/prompts, and how tuning access is prevented.

Holdout cases that fail the independent feasibility check must be classified
consistently for every method before their outcomes are inspected. Keep method
timeouts/failures in their assigned cohort; mark genuine infrastructure-invalid
runs separately and apply a frozen rerun policy to all methods. Never replace an
unfavorable valid run selectively. Record model/API version changes that prevent
exact reruns as a reproducibility limitation.

The experiment manifest must link code/config/data hashes, simulator version,
SCM/Twin/optimizer/validator versions, model identifiers/settings, prompts/tools,
retrieval parameters, authority policies and raw logs. Approved model promotions
are versioned events; rollback must retain the previous version and reason.
Active probes and scripted operator policies require their separate approvals.

Jev remains optional after the core method works. Its absence cannot block the
core study. P0.5 is complete with P05-D001–D010 and researcher confirmation.
Completing P0 does not mean the numeric manifest or simulator is validated.
The next simulator task after approval is P1.4: reproduce and verify fixed annual
equipment sizing, with the existing source artifacts preserved.
