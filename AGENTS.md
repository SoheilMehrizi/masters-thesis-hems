# HEMS research project — contributor and agent context

Last updated: 2026-11-15. This file provides a portable handoff for collaborators
and coding agents. Read it before changing this repository. It summarizes the
current project; it does not resolve the open P0 research decisions.

## Research objective and status

**Digital-Twin-Guided Diagnostic Adaptation for Fast and Reliable
Preference-Aware Home Energy Management Using LLM-Based Multi-Agent Systems.**

The proposed research investigates whether evidence-grounded diagnosis and
Digital Twin tests can select effective interventions faster and with fewer
constraint violations under changing preferences and operational degradation.
These are research questions, not demonstrated results.

Current focus is **P0: research specification and implementation literature**.
P1.1–P1.3 have saved validation evidence. P1.4 is deferred until the P0 review;
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
  Final baseline selection and reproduction fidelity remain open.
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
- Rebuild generated reports through `scripts/build_literature_site.py`, rather
  than editing generated report HTML. Figure assets/manifest are prepared with
  `scripts/prepare_figure_views.py` when source assets change. Consult
  `docs/literature/README.md` for pipeline details.
- Rebuild the tracker from Markdown with `scripts/build_backlog_page.py`.
  Browser checkboxes/notes do not update Markdown; export progress for handoff.
  Mark tasks complete only with the scoped work, relevant checks, and evidence.

## Working commands

Run from the repository root in PowerShell:

```powershell
# Simulator and UI checks (local recovered artifacts/dependencies required)
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts\validate_setup.py

# Literature rebuild/check (requires pypdf and retained source assets)
.\.venv\Scripts\python.exe scripts\build_literature_site.py
.\.venv\Scripts\python.exe scripts\validate_literature_site.py

# Backlog regeneration
.\.venv\Scripts\python.exe scripts\build_backlog_page.py

# Local documentation server; keep the terminal open
powershell -ExecutionPolicy Bypass -File scripts\serve_literature.ps1

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
next task. **Next research task: P0.1, consolidate the agreed specification and
unresolved choices before proceeding to P1.4.**
