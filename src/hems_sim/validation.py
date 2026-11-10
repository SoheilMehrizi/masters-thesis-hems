"""Executable evidence for P1.1-P1.3. No prior audit result counts as a test pass."""
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from .environment import ROOT, configuration, load_schema, make_environment, rollout

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def git(source, *args):
    return subprocess.check_output(['git', '-C', str(source), *args], text=True).strip()

def save(name, value):
    path = ROOT / 'reports' / name
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(value, indent=2, default=lambda x: x.item() if hasattr(x, 'item') else str(x), allow_nan=False), encoding='utf-8')

def validate():
    config = configuration()
    checks = []
    def check(name, operation):
        try:
            evidence = operation()
            checks.append({'check': name, 'status': 'PASS', 'evidence': evidence})
            print(f'PASS {name}', flush=True)
        except Exception as error:
            status = 'BLOCKED' if isinstance(error, (FileNotFoundError, ModuleNotFoundError)) else 'FAIL'
            checks.append({'check': name, 'status': status, 'error': str(error), 'traceback': traceback.format_exc()})
            print(f'{status} {name}: {error}', flush=True)

    def provenance():
        import citylearn
        source = (ROOT / config['citylearn_source']).resolve()
        head = git(source, 'rev-parse', 'HEAD')
        assert head == config['expected_commit'] == git(source, 'rev-parse', 'v3.2.0^{commit}')
        assert not git(source, 'status', '--porcelain', '--untracked-files=no'), 'Modified simulator source'
        assert citylearn.__version__ == config['expected_version']
        assert Path(citylearn.__file__).resolve().is_relative_to(source)
        packages = {d.metadata['Name']: d.version for d in importlib.metadata.distributions()}
        for line in (ROOT / 'requirements.lock').read_text().splitlines():
            if line.strip() and not line.startswith('#'):
                name, version = line.split('==')
                assert importlib.metadata.version(name) == version, f'Dependency differs from lock: {name}'
        assert platform.python_version() == '3.11.9'
        assert Path(sys.prefix).resolve() == (ROOT / config['python_environment']).resolve(), 'Wrong Python environment'
        original = json.loads((ROOT / 'data/recovered/manifest.json').read_text())
        for name, digest in original['source_hashes'].items():
            assert sha(source / Path(name)) == digest, name
        manifest = {'actual_commit': head, 'tag': 'v3.2.0', 'origin': git(source, 'remote', 'get-url', 'origin'),
                    'citylearn_version': citylearn.__version__, 'import_path': citylearn.__file__,
                    'python_executable': sys.executable, 'python_version': platform.python_version(),
                    'platform': platform.platform(), 'packages': packages, 'configuration': config,
                    'schema_sha256': sha(ROOT / config['schema_path']),
                    'requirements_sha256': sha(ROOT / 'requirements.lock'),
                    'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
                    'source_acquisition': 'Official GitHub clone of v3.2.0; upstream tag checked with git ls-remote.'}
        save('environment_manifest.json', manifest)
        return {'commit': head, 'source_hashes_verified': len(original['source_hashes']), 'python': platform.python_version()}

    def artifacts():
        archive_manifest = json.loads((ROOT / 'data/recovered/PACKAGE_MANIFEST.json').read_text())
        for name, metadata in archive_manifest['files'].items():
            path = ROOT / 'data/recovered' / name
            assert sha(path) == metadata['sha256'] and path.stat().st_size == metadata['bytes'], name
        return {'verified_files': len(archive_manifest['files'])}

    def dataset():
        source = ROOT / config['citylearn_source']
        original = json.loads((ROOT / 'data/recovered/manifest.json').read_text())
        for name, metadata in original['files'].items():
            assert sha(source / Path(name)) == metadata['sha256'], name
        schema = json.loads((source / 'data/datasets' / config['dataset'] / 'schema.json').read_text())
        assert config['building_id'] in schema['buildings']
        building = schema['buildings'][config['building_id']]
        return {'official_files_verified': len(original['files']), 'building_id': config['building_id'],
                'official_pricing': building.get('pricing'), 'official_carbon_intensity': building.get('carbon_intensity')}

    def schema_and_data():
        import numpy as np
        import pandas as pd
        summaries = {}
        for thermal in (False, True):
            schema = load_schema(config, thermal)
            base = Path(schema['root_directory'])
            b = schema['buildings'][config['building_id']]
            assert b['include'] and schema['seconds_per_time_step'] == 3600
            references = []
            def walk(value, key=''):
                if isinstance(value, dict):
                    for k, v in value.items(): walk(v, k)
                elif isinstance(value, str) and value.endswith(('.csv', '.pth', '.parquet', '.epw')):
                    path = base / value
                    assert path.is_file(), str(path)
                    references.append({'field': key, 'file': value, 'sha256': sha(path)})
            walk(b)
            frame = pd.read_csv(base / b['energy_simulation'])
            required = ['month', 'hour', 'day_type', 'cooling_demand', 'heating_demand', 'indoor_dry_bulb_temperature',
                        'indoor_relative_humidity', 'occupant_count', 'indoor_dry_bulb_temperature_cooling_set_point',
                        'indoor_dry_bulb_temperature_heating_set_point', 'non_shiftable_load', 'solar_generation', 'dhw_demand', 'hvac_mode']
            assert len(frame) == 8760
            assert np.isfinite(frame[required].to_numpy(dtype=float)).all()
            hours = frame['hour'].to_numpy()
            assert np.all(hours[1:] == hours[:-1] % 24 + 1), 'Nonsequential hourly calendar'
            assert frame['month'].between(1, 12).all()
            weather = pd.read_csv(base / b['weather'])
            assert len(weather) == len(frame) and np.isfinite(weather.to_numpy(dtype=float)).all()
            if b.get('pricing'):
                pricing = pd.read_csv(base / b['pricing'])
                assert len(pricing) == len(frame) and np.isfinite(pricing.to_numpy(dtype=float)).all()
            summaries['frozen' if thermal else 'custom'] = {'rows': len(frame), 'columns': list(frame.columns),
                'seconds_per_step': schema['seconds_per_time_step'], 'hvac_modes': frame.hvac_mode.unique().tolist(),
                'references': references, 'building_definition': b,
                'calendar': 'Hourly non-leap 8760-row simulation calendar; no verified civil timezone or measurement timestamps.'}
        save('building_audit.json', summaries)
        return {'custom_rows': 8760, 'frozen_rows': 8760, 'reference_paths_verified': True}

    def model():
        import torch
        from citylearn.dynamics import LSTMDynamics
        schema = load_schema(config)
        attrs = dict(schema['buildings'][config['building_id']]['dynamics']['attributes'])
        path = Path(schema['root_directory']) / attrs.pop('filename')
        state = torch.load(path, map_location='cpu', weights_only=True)
        net = LSTMDynamics(filepath=path, **attrs)
        net.load_state_dict(state.get('model_state_dict', state))
        net.reset()
        assert net.lookback == 13 and not net.training
        result = {'path': str(path.relative_to(ROOT)), 'sha256': sha(path), 'lookback': net.lookback,
                  'input_features': net.input_observation_names, 'input_size': net.input_size,
                  'state_shapes': {k: list(v.shape) for k,v in net.state_dict().items()},
                  'output': 'Min-max normalized indoor temperature, inverse transformed to degrees C.',
                  'warmup': 'History buffer has lookback+1 slots; predictions require a full buffer.',
                  'visibility': 'Predictions overwrite the controlled interval and are held in the next observation slot.'}
        save('model_audit.json', result)
        return {'lookback': 13, 'weights_sha256': sha(path)}

    def initialize():
        env = make_environment(config)
        try:
            env.reset(seed=config['random_seed'])
            b = env.buildings[0]
            result = {'class': type(b).__name__, 'action_names': env.action_names,
                      'observation_names': env.observation_names,
                      'action_bounds': [{'low': s.low.tolist(), 'high': s.high.tolist()} for s in env.action_space],
                      'ratings': {k: {'nominal_power': float(getattr(b,k).nominal_power)}
                                  for k in ('cooling_device','heating_device','pv','electrical_storage')},
                      'battery_capacity_kwh': float(b.electrical_storage.capacity)}
            save('loaded_environment.json', result)
            return {'class': result['class'], 'action_count': len(env.action_names[0]),
                    'observation_count': len(env.observation_names[0]), 'ratings': result['ratings'],
                    'battery_capacity_kwh': result['battery_capacity_kwh']}
        finally: env.close()

    trajectories = {}
    def stepping():
        run = rollout(config)
        assert len(run['rows']) == config['simulation_end_time_step'] - config['simulation_start_time_step']
        assert run['rows'][-1]['terminated'] or run['rows'][-1]['truncated']
        trajectories['custom'] = run
        save('smoke_rollout.json', run)
        return {'transitions': len(run['rows']), 'final_temperature_C': run['rows'][-1]['observed_temperature_C']}

    def determinism():
        first = trajectories.get('custom') or rollout(config)
        second = rollout(config)
        assert first == second, 'Same-process deterministic CPU replay differs'
        return {'comparison': 'Exact equality of all actions, observations, rewards, temperatures and termination flags', 'seed': config['random_seed']}

    def thermal_response():
        import numpy as np
        off, on = rollout(config, hvac=0.0, thermal=True), rollout(config, hvac=0.2, thermal=True)
        a = np.array([r['internal_temperature_C'] for r in off['rows']])
        b = np.array([r['internal_temperature_C'] for r in on['rows']])
        mask = np.array([r['dynamic'] for r in on['rows']])
        assert mask.any()
        threshold = float(32 * np.finfo(np.float32).eps * max(1, np.max(np.abs(a)), np.max(np.abs(b))))
        delta = b-a
        assert np.max(delta[mask]) > threshold, 'No heating response above float32 numerical resolution'
        visible = np.array([r['observed_temperature_C'] for r in on['rows']])
        np.testing.assert_allclose(visible[mask], b[mask], rtol=0, atol=threshold)
        result = {'transitions': len(a), 'first_dynamic_controlled_step': next(r['controlled_global_step'] for r in on['rows'] if r['dynamic']),
                  'maximum_heating_temperature_difference_C': float(delta[mask].max()),
                  'numerical_threshold_C': threshold, 'agent_temperature_matches_internal_prediction': True,
                  'scope': 'Frozen scenario, winter availability smoke test; not the 72-transition reference campaign.'}
        save('thermal_smoke.json', {'summary': result, 'off': off, 'on': on})
        return result

    for name, operation in [('version_and_provenance', provenance), ('artifact_integrity', artifacts),
                            ('official_dataset', dataset), ('schema_and_data', schema_and_data), ('lstm_artifact', model),
                            ('environment_initialization', initialize), ('bounded_rollout', stepping),
                            ('determinism', determinism), ('thermal_response', thermal_response)]:
        check(name, operation)
    checks.append({'check': 'audit_completeness', 'status': 'PASS', 'evidence': 'All nine required checks attempted and individually classified.'})
    save('validation_results.json', checks)
    def status(names):
        values = [c['status'] for c in checks if c['check'] in names]
        return 'FAIL' if 'FAIL' in values else 'BLOCKED' if 'BLOCKED' in values else 'PASS'
    tasks = {'P1.1': status(['version_and_provenance']), 'P1.2': status(['artifact_integrity','official_dataset']),
             'P1.3': status(['schema_and_data','lstm_artifact','environment_initialization','bounded_rollout','determinism','thermal_response'])}
    text = '# Setup validation\n\nGenerated by `python scripts/validate_setup.py`.\n\n| Task | Status |\n|---|---|\n'
    text += ''.join(f'| {k} | {v} |\n' for k,v in tasks.items())
    text += '\n| Check | Status | Evidence |\n|---|---|---|\n'
    text += ''.join(f"| {c['check']} | {c['status']} | {json.dumps(c.get('evidence', c.get('error')), default=str).replace('|','/')} |\n" for c in checks)
    text += '\nSee `environment_manifest.json`, `dataset_manifest.json`, `building_audit.json`, `model_audit.json`, and trajectory JSON files for machine-readable evidence.\n'
    text += '\nLimitations: EV and tariff inputs are synthetic; extensions are preserved but not scientifically validated. No autosizing, source patching, training, fault injection or later-phase work was performed. The frozen scenario is a sizing reference, not an independently calibrated twin. Only a 48-transition winter comparison was planned; the prior 72-transition winter/summer numbers are not claimed reproduced. Forecast channels are pre-existing supplied forecasts, not verified real-time forecasts; no causal or forecasting evaluation is claimed. Calendar timezone is unverified.\n'
    (ROOT / 'reports/setup_validation.md').write_text(text, encoding='utf-8')
    return all(c['status'] == 'PASS' for c in checks)
