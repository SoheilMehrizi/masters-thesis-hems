"""Persist independent experiments and native CityLearn UI exports."""
from datetime import datetime, timezone
import json
from pathlib import Path
from uuid import uuid4
from threading import Lock
import numpy as np

from hems_sim.environment import ROOT, configuration, rollout

RUNS = ROOT / 'outputs' / 'experiments'
_RUN_LOCK = Lock()


def _json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    raise TypeError(f'Cannot serialize {type(value).__name__}')


def run_experiment(start=0, steps=48, hvac=0.2, seed=2022, thermal=False, root=RUNS):
    if not isinstance(start, int) or not isinstance(steps, int) or not 0 <= start < start + steps < 8760:
        raise ValueError('Choose at least one transition within simulation hours 0–8759.')
    if not -1.0 <= hvac <= 1.0:
        raise ValueError('HVAC action must be between -1 and 1.')
    config = configuration()
    config.update(simulation_start_time_step=start, simulation_end_time_step=start + steps,
                  random_seed=seed, render_mode='end')
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid4().hex[:8]
    directory = Path(root).resolve() / run_id
    directory.mkdir(parents=True, exist_ok=False)
    metadata = {'run_id': run_id, 'configuration': config, 'hvac_action': hvac,
                'scenario': 'frozen' if thermal else 'custom',
                'timestamp_note': 'Use simulation-hour indices; exported calendar dates are not verified.'}
    (directory / 'configuration.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    try:
        # CityLearn/PyTorch use process-wide RNG and thread settings. Serialize
        # browser sessions so simultaneous experiments cannot disturb those.
        with _RUN_LOCK:
            result = rollout(config, hvac, thermal, render_directory=directory, render_session_name='citylearn')
        payload = {**metadata, **result}
        temporary = directory / 'result.tmp'
        temporary.write_text(json.dumps(payload, indent=2, allow_nan=False, default=_json_default), encoding='utf-8')
        temporary.replace(directory / 'result.json')
        return directory / 'result.json'
    except Exception as exc:
        (directory / 'error.txt').write_text(str(exc), encoding='utf-8')
        raise


def saved_runs(root=RUNS):
    return sorted(Path(root).glob('*/result.json'), reverse=True)
