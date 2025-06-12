# tests/special_forms/bdd/action_form_test.py
import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.bdd import registry


class TestActionForm(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        registry.clear_bdd_results()
        # For tests that might need pre-conditions, set them up in the test method or helper

    def helper_run_in_scenario_context(self, code_string):
        # Define initial-value within this helper if tests need it fresh
        run_lispy_string("(define initial-value 100)", self.env)
        registry.start_feature("Test Feature for 'action'")
        registry.start_scenario("Test Scenario for 'action'")
        try:
            result = run_lispy_string(code_string, self.env)
        finally:
            registry.end_scenario()
            registry.end_feature()
        return result

    def test_action_basic_structure_with_body(self):
        result = self.helper_run_in_scenario_context('(action "an action occurs" nil)')
        self.assertIsNone(result)

    def test_action_body_evaluates_and_returns_last_expression(self):
        result = self.helper_run_in_scenario_context(
            '(action "an action occurs" (define new-value (+ initial-value 5)) new-value)'
        )
        self.assertEqual(result, 105)
        self.assertEqual(self.env.lookup("new-value"), 105)

    def test_action_no_body(self):
        result = self.helper_run_in_scenario_context(
            '(action "an action without specific steps")'
        )
        self.assertIsNone(result)

    def test_action_arity_error_no_args(self):
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_scenario_context("(action)")
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'action' expects at least a description string, got 0 arguments.",
        )

    def test_action_arity_error_no_description_string(self):
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_scenario_context("(action 42)")
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'action' expects a description string as its first argument.",
        )

    def test_action_description_not_a_string(self):
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_scenario_context("(action 123 nil)")
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'action' expects a description string as its first argument.",
        )

    def test_action_outside_it_block(self):
        # registry.clear_bdd_results() in setUp
        registry.start_feature("Dummy Feature for Context Test")
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(action "an action" nil)', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'action' form can only be used inside an 'it' block.",
        )
        registry.end_feature()


if __name__ == "__main__":
    unittest.main()
