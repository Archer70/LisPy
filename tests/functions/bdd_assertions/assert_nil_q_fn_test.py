import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.bdd import registry


class TestAssertNilQFn(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()  # Has assert-nil? registered now
        registry.clear_bdd_results()

    def run_in_then_context(self, then_body_code: str):
        registry.start_feature("Test Feature for assert-nil?")
        registry.start_scenario("Test Scenario for assert-nil?")
        run_lispy_string(
            f'(then "a test assertion with assert-nil?" {then_body_code})', self.env
        )
        registry.end_scenario()
        registry.end_feature()

    def test_assert_nil_q_pass(self):
        self.run_in_then_context("(assert-nil? nil)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "passed")
        self.assertNotIn("details", step)

    def test_assert_nil_q_fail_with_true(self):
        self.run_in_then_context("(assert-nil? true)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [nil] but got [True]", step["details"])

    def test_assert_nil_q_fail_with_false(self):
        self.run_in_then_context("(assert-nil? false)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [nil] but got [False]", step["details"])

    def test_assert_nil_q_fail_with_number(self):
        self.run_in_then_context("(assert-nil? 0)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [nil] but got [0]", step["details"])

    def test_assert_nil_q_fail_with_empty_list(self):
        # In LisPy, an empty list is not nil. nil is a distinct value.
        self.run_in_then_context("(assert-nil? (list))")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected [nil] but got [()]", step["details"])

    def test_assert_nil_q_arity_error_no_args(self):
        self.run_in_then_context("(assert-nil?)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn(
            "Step error: SyntaxError: 'assert-nil?' expects 1 argument", step["details"]
        )
        self.assertIn("got 0", step["details"])

    def test_assert_nil_q_arity_error_many_args(self):
        self.run_in_then_context("(assert-nil? nil nil)")
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn(
            "Step error: SyntaxError: 'assert-nil?' expects 1 argument", step["details"]
        )
        self.assertIn("got 2", step["details"])


if __name__ == "__main__":
    unittest.main()
