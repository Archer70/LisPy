import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.bdd import registry

class TestAssertTrueQFn(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env() # Has assert-true? registered now
        registry.clear_bdd_results()

    def run_in_then_context(self, then_body_code: str):
        registry.start_feature("Test Feature for assert-true?")
        registry.start_scenario("Test Scenario for assert-true?")
        run_lispy_string(f'(then "a test assertion with assert-true?" {then_body_code})', self.env)
        registry.end_scenario()
        registry.end_feature()

    def test_assert_true_q_pass(self):
        self.run_in_then_context('(assert-true? true)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "passed")
        self.assertNotIn("details", step)

    def test_assert_true_q_fail_with_false(self):
        self.run_in_then_context('(assert-true? false)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [True] but got [False]", step["details"])

    def test_assert_true_q_fail_with_nil(self):
        self.run_in_then_context('(assert-true? nil)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [True] but got [None]", step["details"])

    def test_assert_true_q_fail_with_number(self):
        self.run_in_then_context('(assert-true? 0)') # In many languages 0 is falsey, but not strictly True
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [True] but got [0]", step["details"])

    def test_assert_true_q_fail_with_empty_list(self):
        self.run_in_then_context('(assert-true? (list))') # Empty list is often falsey
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [True] but got [[]]", step["details"])

    def test_assert_true_q_arity_error_no_args(self):
        self.run_in_then_context('(assert-true?)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Step error: SyntaxError: 'assert-true?' expects 1 argument", step["details"])
        self.assertIn("got 0", step["details"])

    def test_assert_true_q_arity_error_many_args(self):
        self.run_in_then_context('(assert-true? true false)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Step error: SyntaxError: 'assert-true?' expects 1 argument", step["details"])
        self.assertIn("got 2", step["details"])

if __name__ == '__main__':
    unittest.main() 