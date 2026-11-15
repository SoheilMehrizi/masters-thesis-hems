"""Run a saved experiment and print the folder for CityLearn UI."""
import argparse
import json
from hems_sim.experiments import run_experiment

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', type=int, default=0)
    parser.add_argument('--steps', type=int, default=48)
    parser.add_argument('--hvac', type=float, default=0.2)
    parser.add_argument('--seed', type=int, default=2022)
    parser.add_argument('--thermal', action='store_true', help='Use the frozen thermal scenario')
    path = run_experiment(**vars(parser.parse_args()))
    result = json.loads(path.read_text(encoding='utf-8'))
    print(f'Saved experiment: {path}')
    print(f'Choose this folder in CityLearn UI: {result["export_directory"]}')
