"""Integration checks regenerate evidence; stale reports cannot make these pass."""
import unittest
from hems_sim.validation import validate

class SetupTests(unittest.TestCase):
    def test_reproducible_setup(self):
        self.assertTrue(validate(), 'See reports/validation_results.json for individual failures')

if __name__ == '__main__':
    unittest.main()
