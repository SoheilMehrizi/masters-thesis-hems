# Data recovery

Run `python scripts/recover_artifacts.py` from a Python environment to recover
`exports/custom_alameda_complete.zip` into `data/recovered/`.
The script verifies ZIP integrity and all 29 package-manifest entries, refuses
path traversal and modified destination files, and writes a separate inventory
to `reports/dataset_manifest.json`. The two package metadata files are hashed
for the new inventory but are not self-authenticated by the package manifest.

Recovered files are original supplied artifacts, not reconstructed data.
The original audit scripts are retained as evidence and are not automatically
run: some implement later-phase experiments or rewrite the scenarios.
