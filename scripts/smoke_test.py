"""Run a bounded fixed-action example, not an energy controller."""
import argparse
from hems_sim.environment import configuration, rollout
from hems_sim.validation import save

parser = argparse.ArgumentParser()
parser.add_argument('--steps', type=int, default=48)
parser.add_argument('--start', type=int, default=0)
parser.add_argument('--hvac', type=float, default=0.2)
args = parser.parse_args()
config = configuration()
config['simulation_start_time_step'] = args.start
config['simulation_end_time_step'] = args.start + args.steps
result = rollout(config, hvac=args.hvac)
save('example_rollout.json', {'configuration': config, 'hvac_action': args.hvac, **result})
print(f"Completed {len(result['rows'])} transitions. Final observed temperature: {result['rows'][-1]['observed_temperature_C']:.4f} C")
print('Saved reports/example_rollout.json')
