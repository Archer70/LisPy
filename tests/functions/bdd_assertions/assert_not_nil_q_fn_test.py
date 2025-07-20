import unittest

from lispy.bdd import registry
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class TestAssertNotNilQFn(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()  # Has assert-not-nil? registered now
        registry.clear_bdd_results()

    def run_in_then_context(self, then_body_code: str):
        registry.start_feature("Test Feature for assert-not-nil?")
        registry.start_scenario("Test Scenario for assert-not-nil?")
        run_lispy_string(
            f'(then "a test assertion with assert-not-nil?" {then_body_code})', self.env
        )
        registry.end_scenario()
        registry.end_feature()

    def test_assert_not_nil_q_pass_with_true(self):
        self.run_in_then_context("(assert-not-nil? true)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "passed")
        self.assertNotIn("details", step)

    def test_assert_not_nil_q_pass_with_false(self):
        self.run_in_then_context("(assert-not-nil? false)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "passed")
        self.assertNotIn("details", step)

    def test_assert_not_nil_q_pass_with_number(self):
        self.run_in_then_context("(assert-not-nil? 0)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "passed")
        self.assertNotIn("details", step)

    def test_assert_not_nil_q_pass_with_empty_list(self):
        self.run_in_then_context("(assert-not-nil? (list))")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "passed")
        self.assertNotIn("details", step)

    def test_assert_not_nil_q_fail_with_nil(self):
        self.run_in_then_context("(assert-not-nil? nil)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn(
            "Assertion Failed: Expected a non-nil value but got [nil].", step["details"]
        )

    def test_assert_not_nil_q_arity_error_no_args(self):
        self.run_in_then_context("(assert-not-nil?)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn(
            "Step error: SyntaxError: 'assert-not-nil?' expects 1 argument",
            step["details"],
        )
        self.assertIn("got 0", step["details"])

    def test_assert_not_nil_q_arity_error_many_args(self):
        self.run_in_then_context("(assert-not-nil? true false)")  # Too many args
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn(
            "Step error: SyntaxError: 'assert-not-nil?' expects 1 argument",
            step["details"],
        )
        self.assertIn("got 2", step["details"])


if __name__ == "__main__":
    unittest.main()
