"""Exercise native exports, run isolation, and dashboard controls."""
import json
import importlib.util
import csv
from pathlib import Path
import tempfile
import unittest

from hems_sim.environment import ROOT, configuration, rollout
from hems_sim.experiments import run_experiment


class ExportTests(unittest.TestCase):
    def test_export_preserves_trajectory_and_isolates_runs(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.build-tmp') as directory:
            first = run_experiment(steps=16, root=directory)
            second = run_experiment(steps=16, root=directory)
            self.assertNotEqual(first, second)
            result = json.loads(first.read_text())
            config = configuration()
            config['simulation_end_time_step'] = 16
            expected = rollout(config)
            self.assertEqual(result['rows'], expected['rows'])
            self.assertEqual(result['rows'], json.loads(second.read_text())['rows'])
            exports = Path(result['export_directory'])
            self.assertTrue((exports / 'exported_kpis.csv').is_file())
            self.assertTrue(list(exports.glob('exported_data_*_ep0.csv')))
            with (exports / 'exported_data_community_ep0.csv').open() as file:
                self.assertEqual(len(list(csv.DictReader(file))), 16)
            self.assertTrue(result['rows'][-1]['terminated'])

    def test_invalid_window_rejected_before_creating_run(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.build-tmp') as directory:
            with self.assertRaises(ValueError):
                run_experiment(start=8750, steps=48, root=directory)
            self.assertEqual(list(Path(directory).iterdir()), [])


@unittest.skipUnless(importlib.util.find_spec('streamlit'), 'Install requirements-ui.lock for UI checks')
class DashboardTests(unittest.TestCase):
    def test_saved_run_and_signal_selection(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(ROOT / 'scripts/dashboard.py')).run(timeout=60)
        self.assertFalse(app.exception)
        if app.metric:
            app.selectbox(key='signal').select('electrical_storage_soc').run(timeout=60)
            self.assertFalse(app.exception)
            choices = app.selectbox(key='comparison').options
            if len(choices) > 1:
                from hems_sim.experiments import saved_runs
                other = next(str(p) for p in saved_runs() if str(p) != app.session_state['selected_run'])
                app.selectbox(key='comparison').select(other).run(timeout=60)
                self.assertFalse(app.exception)
            app.number_input[0].set_value(8758)
            app.number_input[1].set_value(48)
            app.button[0].click().run(timeout=60)
            self.assertFalse(app.exception)
            self.assertTrue(app.error)


if __name__ == '__main__':
    unittest.main()
