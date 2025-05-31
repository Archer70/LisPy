import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.bdd import registry

class TestAssertFalseQFn(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env() # Has assert-false? registered now
        registry.clear_bdd_results()

    def run_in_then_context(self, then_body_code: str):
        registry.start_feature("Test Feature for assert-false?")
        registry.start_scenario("Test Scenario for assert-false?")
        run_lispy_string(f'(then "a test assertion with assert-false?" {then_body_code})', self.env)
        registry.end_scenario()
        registry.end_feature()

    def test_assert_false_q_pass(self):
        self.run_in_then_context('(assert-false? false)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "passed")
        self.assertNotIn("details", step)

    def test_assert_false_q_fail_with_true(self):
        self.run_in_then_context('(assert-false? true)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [False] but got [True]", step["details"])

    def test_assert_false_q_fail_with_nil(self):
        self.run_in_then_context('(assert-false? nil)') # nil is not strictly False
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [False] but got [None]", step["details"])

    def test_assert_false_q_fail_with_number(self):
        self.run_in_then_context('(assert-false? 1)') # Numbers are not strictly False
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [False] but got [1]", step["details"])

    def test_assert_false_q_arity_error_no_args(self):
        self.run_in_then_context('(assert-false?)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Step error: SyntaxError: 'assert-false?' expects 1 argument", step["details"])
        self.assertIn("got 0", step["details"])

    def test_assert_false_q_arity_error_many_args(self):
        self.run_in_then_context('(assert-false? false true)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Step error: SyntaxError: 'assert-false?' expects 1 argument", step["details"])
        self.assertIn("got 2", step["details"])

if __name__ == '__main__':
    unittest.main() 