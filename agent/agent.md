# HEMS research project — contributor and agent context

Last updated: 2026-11-16. This file provides a portable handoff for collaborators
and coding agents. Read it before changing this repository. It summarizes the
current project; it does not resolve the open P0 research decisions.

All paths below are relative to the repository root. Project-specific workflow
scripts live in `agent/scripts/`; see `agent/README.md` for the tooling map.

## Research objective and status

**Causal Diagnosis and Digital-Twin-Guided Adaptation for Preference-Aware
Home Energy Management with LLM Agents.**

The proposed research investigates whether evidence-grounded diagnosis and
Digital Twin tests can select effective interventions faster and with fewer
constraint violations under changing preferences and operational degradation.
These are research questions, not demonstrated results.

**P0 design is complete**, confirmed on 2026-11-16. **Next task: P1.4,
reproduce and verify fixed annual equipment sizing.**
The [research specification](../docs/RESEARCH_SPECIFICATION.md) records confirmed
decisions separately from open questions. On 2026-11-16, the researcher confirmed
causal diagnosis and corrective intervention as the central contribution, Jev as
an optional later efficiency component, and one multi-device home with cooperating
agents as the initial scope. Efficiency should guide implementation without
presuming resource ceilings. The title above and a natural-language preference
interface were subsequently confirmed. Requests are translated into confirmed
hard constraints and soft priorities. For the first example, 23°C is the target
with a hard 22.5–23.5°C occupied-home band. Ask for a missing EV departure deadline
and confirm the charge target. Report infeasibility and request permission before
relaxing resident hard requirements; physical/equipment safety limits remain
enforced. Initial devices are HVAC, EV charging, PV, stationary battery and fixed
loads. Validated HVAC/EV scheduling may run automatically within unchanged
requirements. LLM agents interpret, diagnose and select interventions; a numerical
constrained optimizer computes schedules and an independent validator checks them.
An explicit Dynamic SCM with diagnostic tools and a frozen Reference Twin plus
versioned Operational Twin are confirmed. The default soft objective is electricity
cost, overridden by explicitly confirmed resident priorities; other outcomes are
reported separately. Battery scheduling within unchanged limits is now authorized
after independent validation (P04-D001). Operational Twin candidate fitting/testing
is automatic; promotion requires approval initially (P04-D002). Active probes need
an explicitly approved bounded policy, not yet numerically specified (P04-D003).
Executable contracts and numerical parameters remain validation artifacts.
P04-D004–D006 confirm receding-horizon/event-triggered execution, independently
validated deterministic fallback with explicit reporting, and bounded conditional
multi-step interventions with stepwise validation. P04-D007–D009 confirm linear/
piecewise-linear LP/MILP scheduling with independent validation, immediate scoring
of active-band violations without implicit grace, and interval monitoring with
event-triggered LLM diagnosis. The consolidated P0.4 interface/lifecycle/unit-time
contract was confirmed in P04-D010; exact schemas and numerical mappings remain
validation gates. P0.5 design is complete in docs/EVALUATION_SPECIFICATION.md.
P05-D001–D003 confirm verified recovery success rate as primary with violations/
overhead reported separately; four core methods (full, diagnosis-free LLM,
optimizer-only, rule-based HEMS); and no-SCM/no-Twin-ranking/passive-only/single-
action ablations. Probing remains conditional on bounded-policy approval.
P05-D004–D006 confirm adapted Bayesian-network and rule diagnostic baselines,
hierarchical core/topology comparisons supplementary, and separated development/
held-out evaluation with selected generalization cases. Detailed scoring,
statistical reporting and experiment manifests were subsequently confirmed in
P05-D007–D009: separate reactive/prevention suites, paired differences with 95%
intervals and pilot-selected repeats, and frozen manifests with complete run/
approval logs. P05-D010 records final endpoint/hypothesis/protocol approval;
P0.1–P0.5 design is complete. Pilot-selected numerical settings, source-specific
baseline fidelity, executable schemas and simulator audits remain mandatory gates.
P0.1 was confirmed complete on 2026-11-16 (D017); P0.2 design is complete in
`docs/DEGRADATION_SPECIFICATION.md`.
The linked P0 companion specifications record agreed design and remaining
implementation/validation gates.
Initial P0.2 decisions: explicit confirmed preference updates (inferred changes
later); degradation coverage for HVAC, EV, stationary battery and PV from the
start; healthy/isolated cases followed by selected simultaneous and cascading
cases. Confirmed mechanisms include HVAC capacity, EV charging-power, battery
discharge-power and PV-output derating, plus battery energy-capacity and efficiency
losses. Begin with abrupt persistent cases, then selected gradual/temporary cases;
include recoverable and infeasible cases with matched controls. Numeric severities
remain deferred to validated pilots. Battery state/efficiency semantics are
confirmed in P02-D010: preserve kWh at
capacity-compatible onset states; derate both charging and discharging efficiency. Confirmed non-equipment coverage:
PV, outdoor-temperature and fixed-load forecast errors; Operational Twin thermal
and battery-efficiency mismatch; delayed/missing plan delivery and stale versions
with independent validation retained. See P02-D007–D012. Selected combinations are confirmed subject to simulator
validation. Pilot-based numeric selection and a frozen manifest remain mandatory
P2 gates. P0.3 design is recorded in docs/INFORMATION_ACCESS_SPECIFICATION.md.
P03-D001–D003 confirm evaluator-only hidden truth/future realizations; the initial
temperature, occupancy, EV/charge, battery-charge, power and execution-log channel
categories subject to validation; and exact approved measurements followed by
selected noise/missing-data/delay tests. P03-D004–D006 confirm a shared timestamped
evidence store with role-specific views, Twin state estimation from permitted
observations/history, and competing hypotheses, unknown outcomes and abstention.
P03-D007–D008 confirm declared future plans with clarification, current observations,
and bounded recent history plus logged bounded retrieval; numeric budgets require
pilots and freezing before comparison. P0.3 and P0.4 designs are complete;
the component contracts are recorded in docs/COMPONENT_CONTRACTS.md. Frozen
Reference Twin parameters are distinct from its observation-based state updates.
P1.1–P1.3 have saved validation evidence. The P0 review is complete; P1.4 is next;
it requires reproducing fixed annual equipment sizing, not just loading ratings.
The literature library covers 29 unique local articles and 293 visual evidence
views. A literature report being available does not complete a P0 decision.

Work task by task according to the researcher's instructions. Do not start later
implementation phases merely because they appear in the backlog. Record agreed
decisions, open questions, acceptance criteria, and evidence separately. Preserve
existing work and do not replace the research direction without discussion.

## Proposed research scope

- Preference-aware residential energy management, including cost, comfort, HVAC,
  PV, electrical storage, and the supplied EV extension where validated.
- Five degradation families: preference drift, forecast error, Twin model
  mismatch, equipment degradation, and scheduling/coordination failure. Include
  simultaneous and cascading causes in the intended benchmark.
- A frozen Reference Twin and a versioned Operational Twin, with synchronized
  permitted state/history, isolated hypothetical rollouts, and controlled
  calibration/rollback. Neither subsystem is implemented yet.
- A time-indexed hierarchical structural causal model (Dynamic SCM) for diagnosis,
  dependent cause beliefs, uncertainty, unknown causes, and abstention. Graphs,
  mechanisms, inference choices, priors, and thresholds still need specification.
- Typed, conditional intervention plans with structural validation, independent
  deterministic safety/authority checks, Twin evaluation, bounded diagnostic
  probes, staged execution, outcome verification, and replanning.
- Centralized, hierarchical, and decentralized LLM-agent architectures with
  comparable tool access and computational budgets. LLMs interpret preferences,
  assess evidence, and orchestrate tools; hard constraints require independent
  checks. DRL is a possible comparison, not the proposed primary controller.
- Candidate comparisons include rule-based control, MPC/MILP, direct LLM
  scheduling, adapted LA-UPAHEM and agentic HEMS, Bayesian/rule diagnosis,
  diagnosis-free planning, passive-only diagnosis, and single-action intervention.
  P0.5 confirms the core and adapted diagnostic baselines; additional named-paper
  reproductions remain candidates. Source-specific fidelity records are required.
- Intended evaluation includes diagnosis/calibration/abstention, recovery,
  violations, energy cost, comfort, unnecessary interventions, latency, tokens,
  and computational cost. Freeze splits, seeds, budgets, and protocols before
  final evaluation; distinguish evaluator-only truth from agent observations.

See `docs/PROJECT_BACKLOG.md` for P0–P9 tasks and current acceptance criteria.
Do not invent numerical targets, causal identifiability claims, approved baseline
choices, or finalized scientific specifications that are not recorded there.

## Navigation and sources of truth

| Location | Purpose |
| --- | --- |
| `docs/HEMS_Research_Landing_Final_Title_Updated.html` | Main bilingual research proposal and navigation |
| `docs/PROJECT_BACKLOG.md` | Versioned task scope, verified completion, open decisions |
| `docs/PROJECT_BACKLOG.html` | Interactive tracker; browser progress is local only |
| `docs/literature/index.html` | Categorized article-analysis library |
| `docs/literature/research-map.html` | Proposed research roles and baseline recommendations |
| `reports/literature/analyses/` | Reviewed JSON for article reports and project-role assessments |
| `docs/literature/inventory.json` | Local article inventory and source locations |
| `configs/simulator.json` | Pinned simulator configuration |
| `reports/setup_validation.md` | Saved P1.1–P1.3 evidence and limitations |
| `reports/implementation_notes.md` | Setup provenance and troubleshooting |
| `README.md` | Setup, dashboard, export, and validation instructions |

The proposal includes historical alternatives and illustrative animations. Do
not treat it as proof of implementation or experimental performance. For actual
simulator behavior, inspect the pinned source, configuration, audits, and runs.
`docs/P0_IMPLEMENTATION_LITERATURE.md` contains historical triage; its original
missing-file notes are superseded by the current library inventory.

## Simulator contract and scientific boundaries

- CityLearn **3.2.0**, commit `fd86484b8b438f03eb40c3ec06dc90caa349842d`.
- Building `resstock-amy2018-2021-release-1-102040`, Alameda dataset; seed 2022.
- Python 3.11, local `.venv`; use its executable directly on Windows.
- Preserve recovered source files, model weights, original schemas, and hashes.
  Do not silently autosize, patch vendor source, or modify baseline parameters.
  Use explicit, separately recorded configurations for experiments.
- Original Alameda data, the recovered custom scenario, and frozen sizing
  scenario are distinct. The frozen scenario is not a calibrated Digital Twin.
- EV schedules and tariffs are synthetic. Calendar timezone and forecast
  issue-time availability remain unverified; do not claim leakage-free causal
  forecasting from the current setup.
- The LSTM history requires warm-up: steps 0–13 precede dynamic control at 14.
  Positive combined HVAC actions request heating; negative actions cooling.
  Use loaded action/observation names and units, not assumed positional mappings.
- A 48-transition winter smoke test is not seasonal reference reproduction or
  physical-model validation. No fault benchmark, optimized controller, Twin
  service, causal engine, or LLM-agent system is implemented yet.
- Dashboard/export tools execute bounded fixed-action runs. Save configurations,
  seeds, provenance, outputs, and limitations; never relabel supplied historical
  results as newly executed tests.

## Literature and website editing rules

- Keep the selected Technical Dashboard style and English/Persian toggle with
  one language visible by default. Maintain Persian direction and mobile layout.
- Base article claims on the supplied papers, with page citations and full
  bibliographies. Explicitly label reviewer analysis and project recommendations.
  Mark unstated hypotheses/questions as unstated instead of inventing them.
- Use original figures with captions and explanations. Report explicitly printed
  values only; do not estimate curves or error bars. Retain full-page source
  context when a reliable crop cannot be established. Do not claim unavailable
  supplements or cited papers were independently reviewed.
- Additional reports use canonical reviewed `article-*.json` files. The first
  two use their builders and `existing-roles.json`. Historical `author_group_*`,
  `author_twins_preferences_reports.py`, and `author_jev_reports.py` scripts can overwrite manual review
  corrections: do not rerun them without comparing and preserving those fixes.
- Rebuild generated reports through `agent/scripts/build_literature_site.py`, rather
  than editing generated report HTML. Figure assets/manifest are prepared with
  `agent/scripts/prepare_figure_views.py` when source assets change. Consult
  `docs/literature/README.md` for pipeline details.
- Rebuild the tracker from Markdown with `agent/scripts/build_backlog_page.py`.
  Browser checkboxes/notes do not update Markdown; export progress for handoff.
  Mark tasks complete only with the scoped work, relevant checks, and evidence.

## Working commands

Run from the repository root in PowerShell:

```powershell
# Simulator and UI checks (local recovered artifacts/dependencies required)
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts\validate_setup.py

# Literature rebuild/check (requires pypdf and retained source assets)
.\.venv\Scripts\python.exe agent\scripts\build_literature_site.py
.\.venv\Scripts\python.exe agent\scripts\validate_literature_site.py

# Backlog regeneration
.\.venv\Scripts\python.exe agent\scripts\build_backlog_page.py

# Local documentation server; keep the terminal open
powershell -ExecutionPolicy Bypass -File agent\scripts\serve_literature.ps1

# Optional simulator dashboard (requires requirements-ui.lock)
powershell -ExecutionPolicy Bypass -File scripts\start_dashboard.ps1
```

The documentation server binds to loopback port 8768. Main landing:
`http://127.0.0.1:8768/HEMS_Research_Landing_Final_Title_Updated.html`.
Run checks appropriate to the change and report actual outcomes and blockers.
Do not install or upgrade dependencies silently just to make a check pass.

## Sharing and reproducibility

Commit source, configuration, documentation, reviewed analysis, and required
local website assets. Do not commit environments, credentials, vendor clones,
recovered binary datasets, original ZIP packages, or experiment output folders.
These are excluded by `.gitignore`. Do not push or publish unless requested.

The source literature folder was supplied at
`A:\University\Master\3rd Semester\LLM Course\Working\Literature review`.
This is machine-specific; collaborators must supply their own authorized source
PDFs and update paths when regenerating assets. Website figure/page reproductions
are for local research; a local Git commit is not authorization to publish them.
Simulator recreation also needs the original archive under `exports/`; consult
`README.md`. A checkout alone does not include the recovered simulation data.

On handoff, report completed work, checks/evidence, unresolved decisions, and the
next task. **P0 design is complete. Next task: P1.4, reproduce and verify fixed
annual equipment sizing.** Preserve source artifacts and document comparison
against recovered reference ratings; loading the ratings alone is insufficient.
