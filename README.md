# Reproducible CityLearn HEMS research setup

Project navigation: [research proposal](docs/HEMS_Research_Landing_Final_Title_Updated.html),
[literature library](docs/literature/index.html), and
[interactive backlog](docs/PROJECT_BACKLOG.html).
Read [agent/agent.md](agent/agent.md) for shared research context, implementation
status, scientific boundaries, contributor rules, and handoff instructions.
[Agent tooling](agent/README.md) contains the library/backlog workflow and scripts;
the root [AGENTS.md](AGENTS.md) provides the discovery entry point.

This project implements P1.1–P1.3: CityLearn 3.2.0 at commit
`fd86484b8b438f03eb40c3ec06dc90caa349842d`, recovery of the supplied Custom
Alameda package, and bounded validation of building
`resstock-amy2018-2021-release-1-102040` and its LSTM thermal model.

## Start using the installed environment

Open PowerShell and run:

```powershell
cd A:\projects\masters-thesis-hems
.\.venv\Scripts\python.exe scripts\smoke_test.py
```

This runs 48 hourly transitions with a fixed HVAC action of 0.2 and all other
actions zero, prints the final observed indoor temperature, and saves the full
trajectory to `reports/example_rollout.json`. It is a smoke-test input, not an
optimized controller. It does not train a model or modify the recovered data.
Using the full Python executable avoids PowerShell activation-policy issues.

Run the complete validation suite:

```powershell
.\.venv\Scripts\python.exe scripts\validate_setup.py
```

Each check prints PASS, FAIL, or BLOCKED. The command exits nonzero if any check
does not pass. Read `reports/setup_validation.md` for the status of P1.1–P1.3,
and `reports/validation_results.json` for evidence and error tracebacks.
The same integration checks can be run through Python's test runner:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Change a bounded example's window and HVAC input:

```powershell
.\.venv\Scripts\python.exe scripts\smoke_test.py --start 0 --steps 48 --hvac 0.2
```

Inspect `reports/loaded_environment.json` for the actual action names and bounds.
For this combined HVAC action, positive values request heating and negative
values request cooling; 0.2 requests 20% of rated heating electrical power once
dynamic control is active. The validation
suite checks a winter heating comparison using the recovered frozen scenario.
Steps 0–13 are history warm-up; a lack of action response there is expected.
Each example run replaces `reports/example_rollout.json`; copy it if you need
to retain multiple runs. Indices are zero-based simulation hours, not verified
civil timestamps.

## Local simulator dashboard and CityLearn UI

Install the optional UI dependencies into the existing environment:

```powershell
$env:UV_CACHE_DIR = Join-Path $PWD '.uv-cache'
.\.tools\bin\uv.exe pip install --python .venv/Scripts/python.exe -r requirements-ui.lock
```

Start the dashboard:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_dashboard.ps1
```

Open http://127.0.0.1:8501 in your browser. Use the sidebar to select the
custom or frozen scenario, start hour, number of transitions, seed, and fixed
HVAC action. Run experiments, inspect signals and temperature set points,
compare saved runs, and download observations, complete JSON, or an interactive
chart. Runs execute synchronously; wait for completion before starting another.
Battery and EV actions remain zero. This is an experiment UI, not an optimized
controller or a live step/pause interface.

Every run gets a unique folder under `outputs/experiments/` (excluded from Git).
Successful runs include `result.json`, configuration, and native CityLearn CSV
exports. Failed runs retain their configuration and error message but do not
appear in the successful-run selector. Dashboard controls do not modify the
baseline configuration or recovered data. Download or back up important runs.

To export without the dashboard:

```powershell
.\.venv\Scripts\python.exe scripts/export_ui.py --start 0 --steps 48 --hvac 0.2
```

Open [CityLearn UI](https://citylearnui.netlify.app/), click **Choose folders**,
and select the exact export directory printed by the command or dashboard.
Native CSV exports include time series and KPIs. Their calendar timestamps are
not verified civil dates; the custom dashboard uses simulation-hour indices.
Observation charts show the next observation step, while each saved JSON row
also records the controlled interval and internal temperature. The first 14
transitions build thermal history. Interpret short-run KPIs with that warm-up
and the synthetic tariff/EV inputs in mind.

Verify exports and the dashboard (after installing the UI dependencies):

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_ui.py -v
```

## Python API

Use `.venv/Scripts/python.exe` as your editor's Python interpreter. For example:

```python
from hems_sim.environment import configuration, make_environment

config = configuration()
env = make_environment(config)
try:
    observations, info = env.reset(seed=config['random_seed'])
    print(env.action_names)
    print(env.observation_names)
    actions = [[0.2 if name == 'cooling_or_heating_device' else 0.0
                for name in names] for names in env.action_names]
    observations, rewards, terminated, truncated, info = env.step(actions)
finally:
    env.close()
```

The central-agent flat interface returns nested observations and actions. Match
values to the names from the loaded environment. The loader rebases only the
in-memory `root_directory`, selects the target building, explicitly sets seed
2022 and the simulation window, and rejects autosizing. Original JSON files
remain byte-for-byte intact. Strict artifact checking is enabled by default.

## Configuration and evidence

`configs/simulator.json` holds relative source/schema paths, the building ID,
seed, interface, time window, Python environment, rendering mode, thread count,
and artifact-checking policy. Keep the default configuration for the baseline
audit. Use the example command's options for exploratory bounded runs.

| Location | Purpose |
|---|---|
| `exports/custom_alameda_complete.zip` | User-supplied original package; retain separately from Git |
| `data/recovered/` | Original package contents, excluded from Git |
| `vendor/CityLearn/` | Official source, editable installation, excluded from Git |
| `.python/`, `.venv/`, `.tools/` | Local Python runtime, environment and setup utility |
| `src/hems_sim/environment.py` | Portable loader and bounded rollout |
| `src/hems_sim/validation.py` | Executable data/source/model/rollout checks |
| `requirements.lock` | Exact installed runtime and build dependency versions |
| `reports/environment_manifest.json` | Python, packages, source commit and run settings |
| `reports/dataset_manifest.json` | Recovered file sizes, hashes and package provenance |
| `reports/building_audit.json` | Actual data columns, schema references and device definitions |
| `reports/model_audit.json` | Weight hash, input features, tensor shapes and history length |
| `reports/loaded_environment.json` | Loaded action/observation interface and equipment ratings |
| `reports/smoke_rollout.json`, `reports/thermal_smoke.json` | Executed trajectories and thermal comparison |
| `reports/setup_validation.md` | Current status and scientific limitations |
| `reports/implementation_notes.md` | Installation commands, deviations and troubleshooting |

## Recreate the setup on Windows

Prerequisites: Git, internet access, a working bootstrap Python with pip, and
the supplied archive at `exports/custom_alameda_complete.zip`.

```powershell
cd A:\projects\masters-thesis-hems
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

This installs pinned uv 0.13.7 into `.tools`, obtains Python 3.11.9 into
`.python`, creates `.venv`, clones and checks the official release, installs
`requirements.lock`, installs both local packages in editable mode, checks
dependencies, verifies/extracts the archive, and runs validation. It stops on
errors and refuses a mismatching existing CityLearn checkout. It does not reset
repositories or overwrite modified recovered artifacts. Network access is
needed for first-time downloads. Existing valid environments are reused.

No NREL-PySAM installation is needed: the recovered scenarios contain fixed
device ratings and the previously sized PV profile. PySAM would be required
for relevant future autosizing work, which is outside this setup.

## Scientific boundaries

The original Alameda dataset, recovered custom scenario and frozen sizing
scenario are distinct artifacts. EV schedules and tariff inputs are synthetic;
they are preserved and inspected, not validated as measured household data.
The frozen scenario is not an independently calibrated digital twin.

The supplied `verification.json` reports earlier experiments. New results are
written separately under `reports/`; prior results are never counted as current
test passes. The short heating comparison establishes dynamic response and
observation visibility, not physical model accuracy or reproduction of the
72-transition seasonal reference campaigns. Exact repeatability is checked on
this CPU/runtime, not promised across hardware or dependency versions.

The LSTM starts with an empty history, uses previous temperatures and current
interval loads/weather, and writes a simulated temperature into the controlled
interval and the next observation slot. Supplied forecast channels remain
enabled by the original schema. Their issue-time availability and absence of
look-ahead leakage have not been independently established; do not use this
setup result as evidence of a causal forecasting evaluation.

No fault framework, controller, digital twin service, causal model or LLM agent
is implemented. Later P1 tasks require separate authorization.

## References

- [Official release](https://github.com/citylearn-project/CityLearn/releases/tag/v3.2.0)
- [Schema reference](https://www.citylearn.net/guides/schema_reference.html)
- [Simulation instructions](https://www.citylearn.net/guides/running_simulations.html)
- [Alameda schema at the pinned commit](https://github.com/citylearn-project/CityLearn/blob/fd86484b8b438f03eb40c3ec06dc90caa349842d/data/datasets/ca_alameda_county_neighborhood/schema.json)
