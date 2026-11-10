# Implementation and reproduction record

## Completed scope

P1.1–P1.3 only. See `setup_validation.md` for the latest executable status.
The original package is recovered unchanged; new code and reports are separate.
No CityLearn source patches were made. Original audit scripts were inspected,
not executed to recreate their later-phase experiments.

## Discovery and provenance

- Initial project: README, LICENSE, .gitignore, report_landing.html, and exports.
  Exports were untracked; no user changes were overwritten.
- Supplied archive: `exports/custom_alameda_complete.zip` (1,329,479 bytes).
  SHA-256: `615825f4527dc9ebf06bf304d7b145ed24e7e5283889ba2cdac4949a8ee452e1`.
- All 29 listed payload files matched package SHA-256 hashes and sizes.
  Two package metadata files were also preserved and separately inventoried.
- The original audit folder was located under the user's Documents/ChatGPT
  directory. Its embedded Python 3.11.9 reported torch 2.15.0+cpu but lacked
  the venv module. It was inspected, not modified or reused as the environment.
- GitHub `ls-remote` returned annotated tag object
  `35e09244b89178acc422969bc59c44e14458ff86`, peeling to the expected commit
  `fd86484b8b438f03eb40c3ec06dc90caa349842d`.
- A clean local audit source clone was briefly prepared while the network clone
  was downloading. The installed source is the direct official GitHub clone at
  `vendor/CityLearn`, not that fallback.
- The validator compares the installed source tree against the original audit's
  source hashes and the selected official dataset files against its recorded
  hashes. Package self-consistency alone is not proof of independent authorship.

## Commands executed during setup

PowerShell, from the project root (routine directory listings and source reads
omitted). These commands describe actual work; `scripts/setup.ps1` is the
repeatable entry point with exit-code checks and pinned dependencies.

```powershell
git status --short
py -0p
python -c "import sys; print(sys.executable); print(sys.version)"
git ls-remote https://github.com/citylearn-project/CityLearn.git refs/tags/v3.2.0 'refs/tags/v3.2.0^{}'
git clone --depth 1 --branch v3.2.0 https://github.com/citylearn-project/CityLearn.git vendor/CityLearn
python -m pip install --target .tools uv
$env:UV_PYTHON_INSTALL_DIR = Join-Path $PWD '.python'
$env:UV_CACHE_DIR = Join-Path $PWD '.uv-cache'
.\.tools\bin\uv.exe python install 3.11.9
.\.tools\bin\uv.exe venv --python .python/cpython-3.11.9-windows-x86_64-none/python.exe .venv
.\.tools\bin\uv.exe pip install --python .venv/Scripts/python.exe 'numpy==1.26.4' 'pandas==3.0.6' 'torch==2.15.0' 'gymnasium==1.4.0' 'scikit-learn==1.2.2' platformdirs pyyaml requests simplejson setuptools wheel
New-Item -ItemType Directory -Force .build-tmp
$env:TEMP = Join-Path $PWD '.build-tmp'
$env:TMP = $env:TEMP
.\.tools\bin\uv.exe pip install --python .venv/Scripts/python.exe --no-build-isolation --no-deps -e vendor/CityLearn -e .
.\.tools\bin\uv.exe pip check --python .venv/Scripts/python.exe
python scripts/recover_artifacts.py
.\.venv\Scripts\python.exe scripts/validate_setup.py
powershell -ExecutionPolicy Bypass -File scripts/setup.ps1
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts/smoke_test.py
git diff --check
```

The resolved versions were read from installed package metadata and written to
`requirements.lock`. Subsequent setup uses that exact lock. uv resolved to
0.13.7 and the setup script pins that bootstrap version.

Final verification: all 10 validation checks PASS, no FAIL/BLOCKED/NOT RUN.
The unittest runner executed one integration test containing the validation
suite and returned OK (19.473 seconds). The standalone example completed 48
transitions with final observed temperature 18.47085189819336 C. The setup
script completed end-to-end against the prepared environment. Dependency
checking reported all 33 installed packages compatible. `git diff --check`
reported no whitespace errors; the simulator checkout remained clean.

## Issues resolved and dependency differences

1. Sandbox DNS prevented the first GitHub query. Network-enabled execution
   successfully verified and downloaded the official release.
2. Default `python` was 3.13.17 and the launcher reported no registered runtimes.
   Installed project-local Python 3.11.9, matching the audit's Python version.
3. Editable installation initially failed with a setuptools `invalid variable`
   exception caused by braces in the sandbox temporary-directory name. Rebased
   TEMP and TMP to `.build-tmp`; both editable installations then succeeded.
4. A uv command using its default sandbox cache reported access warnings.
   All repeatable commands set UV_CACHE_DIR to the writable `.uv-cache`.
5. The prior audit's torch version was confirmed by actual import; the new
   environment also reports 2.15.0+cpu. NumPy 1.26.4 and pandas 3.0.6 match.
   Runtime package metadata is in `environment_manifest.json`.
6. NREL-PySAM is omitted because this setup never invokes PV autosizing.
   Setuptools and wheel are included for traceable editable installation.

## Interpretation and next-stage readiness

The 48-transition winter smoke comparison produced a maximum heating versus
off difference of 5.706839561462402 C. Predictions became active at controlled
step 14. Predicted internal and returned observed temperatures agreed within a
float32-derived tolerance of 0.0000862184097059071 C. Exact same-seed replay of
all recorded observations, rewards, actions and temperatures passed.

These are new bounded observations, not the prior 72-transition winter result
of approximately 6.25387 C or summer result of approximately 8.73389 C. Those
campaigns were not rerun. No physical calibration accuracy is established.

The original LSTM has 13 inputs, 13-step lookback, two recurrent layers with
8 hidden units, and one normalized temperature output. The loader preserves
the pretrained weights. It does not train or substitute a model. History is
initialized empty; historical temperatures are used during warm-up. Later
temperatures are model-generated and held into the next observation slot.

Forecast columns already exist in the recovered schema. Their real-time issue
availability is not established. EV/tariff schedules are synthetic. The hourly
calendar has no independently verified timezone. These limitations must be
resolved as appropriate before causal or forecasting research claims.

The setup is ready for separately authorized P1.4–P1.9 work if the current
validation report remains PASS. No such later-phase implementation is included.
