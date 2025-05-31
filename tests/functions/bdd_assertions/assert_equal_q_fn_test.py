# tests/functions/bdd_assertions/assert_equal_q_fn_test.py
import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError, AssertionFailure
from lispy.bdd import registry

class TestAssertEqualQFn(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env() # Has assert-equal? registered now
        registry.clear_bdd_results()

    def run_in_then_context(self, then_body_code: str) -> None:
        registry.start_feature("Test Feature")
        registry.start_scenario("Test Scenario")
        # The `then` handler will call add_step for us.
        # It will also catch AssertionFailure and update the step.
        run_lispy_string(f'(then "a test assertion" {then_body_code})', self.env)
        registry.end_scenario()
        registry.end_feature()

    def test_assert_equal_q_pass(self):
        self.run_in_then_context('(assert-equal? 5 5)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "passed")
        self.assertNotIn("details", step)

    def test_assert_equal_q_fail(self):
        self.run_in_then_context('(assert-equal? 5 6)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [5]", step["details"])
        self.assertIn("but got [6]", step["details"])

    def test_assert_equal_q_different_types(self):
        self.run_in_then_context('(assert-equal? "5" 5)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [5] (type: str)", step["details"])
        self.assertIn("but got [5] (type: int)", step["details"])

    def test_assert_equal_q_arity_error_few_args(self):
        # This error should be caught by the `then` handler if it causes an exception
        # before `assert-equal?` even runs its own arity check.
        # The `assert-equal?` arity check is an EvaluationError, not AssertionFailure.
        self.run_in_then_context('(assert-equal? 5)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        # Check for the wrapped error message from then_form_handler
        self.assertIn("Step error: SyntaxError: 'assert-equal?' expects 2 arguments", step["details"])
        self.assertIn("got 1", step["details"])

    def test_assert_equal_q_arity_error_many_args(self):
        self.run_in_then_context('(assert-equal? 5 5 5)')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Step error: SyntaxError: 'assert-equal?' expects 2 arguments", step["details"])
        self.assertIn("got 3", step["details"])

    def test_assertion_failure_does_not_halt_later_scenarios(self):
        lispy_code = """
        (describe "Feature with multiple scenarios"
            (it "Scenario 1 - fails"
                (given "g1")
                (when "w1")
                (then "t1 fails" (assert-equal? 1 0)))
            (it "Scenario 2 - passes"
                (given "g2")
                (when "w2")
                (then "t2 passes" (assert-equal? 1 1))))
        """
        run_lispy_string(lispy_code, self.env)
        
        self.assertEqual(len(registry.BDD_RESULTS), 1)
        feature = registry.BDD_RESULTS[0]
        self.assertEqual(len(feature["scenarios"]), 2)
        
        scenario1 = feature["scenarios"][0]
        self.assertEqual(scenario1["description"], "Scenario 1 - fails")
        self.assertEqual(scenario1["steps"][2]["status"], "failed") # The 'then' step

        scenario2 = feature["scenarios"][1]
        self.assertEqual(scenario2["description"], "Scenario 2 - passes")
        self.assertEqual(scenario2["steps"][2]["status"], "passed") # The 'then' step

if __name__ == '__main__':
    unittest.main() 