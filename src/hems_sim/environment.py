"""Load the recovered scenarios without altering the original artifact files."""
from pathlib import Path
import json
import os
import hashlib

ROOT = Path(__file__).resolve().parents[2]

def configuration(path=None):
    return json.loads(Path(path or ROOT / 'configs/simulator.json').read_text(encoding='utf-8'))

def load_schema(config, thermal=False):
    path = ROOT / config['thermal_schema_path' if thermal else 'schema_path']
    if config.get('strict_artifact_validation', True):
        recovered = ROOT / 'data/recovered'
        manifest = json.loads((recovered / 'PACKAGE_MANIFEST.json').read_text())
        for name, expected in manifest['files'].items():
            artifact = recovered / name
            if hashlib.sha256(artifact.read_bytes()).hexdigest() != expected['sha256']:
                raise ValueError(f'Recovered artifact changed: {name}')
    schema = json.loads(path.read_text(encoding='utf-8'))
    schema['root_directory'] = str(path.parent.resolve())
    # Never autosize against a short smoke-test window.
    def check(value):
        if isinstance(value, dict):
            if value.get('autosize'):
                raise ValueError('Autosizing is forbidden in the bounded validation setup')
            for child in value.values():
                check(child)
        elif isinstance(value, list):
            for child in value:
                check(child)
    check(schema)
    return schema

def make_environment(config=None, thermal=False):
    config = config or configuration()
    os.environ['CITYLEARN_OFFLINE'] = '1'
    import torch
    from citylearn.citylearn import CityLearnEnv
    torch.set_num_threads(config['torch_threads'])
    torch.use_deterministic_algorithms(True)
    start, end = config['simulation_start_time_step'], config['simulation_end_time_step']
    if not 0 <= start < end < 8760:
        raise ValueError('Expected 0 <= start < end < 8760')
    return CityLearnEnv(load_schema(config, thermal), buildings=[config['building_id']],
                        random_seed=config['random_seed'], simulation_start_time_step=start,
                        simulation_end_time_step=end, episode_time_steps=end-start+1,
                        interface=config['interface'], render_mode=config['render_mode'])

def rollout(config=None, hvac=0.2, thermal=False):
    import numpy as np
    config = config or configuration()
    env = make_environment(config, thermal)
    try:
        observations, _ = env.reset(seed=config['random_seed'])
        rows = []
        for _ in range(config['simulation_end_time_step'] - config['simulation_start_time_step']):
            actions = [[hvac if name == 'cooling_or_heating_device' else 0.0 for name in names]
                       for names in env.action_names]
            for action, space in zip(actions, env.action_space):
                if not space.contains(np.asarray(action, dtype=space.dtype)):
                    raise ValueError(f'Invalid action: {action}')
            building = env.buildings[0]
            local_step = building.time_step
            dynamic = bool(building.simulate_dynamics)
            observations, reward, terminated, truncated, _ = env.step(actions)
            if not np.isfinite(np.asarray(observations)).all() or not np.isfinite(reward).all():
                raise ValueError('Nonfinite observation/reward')
            ti = env.observation_names[0].index('indoor_dry_bulb_temperature')
            rows.append({'controlled_global_step': config['simulation_start_time_step'] + local_step,
                         'dynamic': dynamic, 'actions': actions, 'observations': observations,
                         'reward': reward, 'terminated': bool(terminated), 'truncated': bool(truncated),
                         'internal_temperature_C': float(building.energy_simulation.indoor_dry_bulb_temperature[local_step]),
                         'observed_temperature_C': float(observations[0][ti])})
            if terminated or truncated:
                break
        return {'rows': rows, 'action_names': env.action_names, 'observation_names': env.observation_names}
    finally:
        env.close()
