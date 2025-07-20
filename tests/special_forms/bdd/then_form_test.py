# tests/special_forms/bdd/then_form_test.py
import unittest

from lispy.bdd import registry
from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class TestThenForm(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        registry.clear_bdd_results()

    def helper_run_in_scenario_context(self, code_string):
        run_lispy_string("(define result-value 42)", self.env)
        registry.start_feature("Test Feature for 'then'")
        registry.start_scenario("Test Scenario for 'then'")
        try:
            result = run_lispy_string(code_string, self.env)
        finally:
            registry.end_scenario()
            registry.end_feature()
        return result

    def test_then_basic_structure_with_body(self):
        result = self.helper_run_in_scenario_context(
            '(then "an outcome is expected" nil)'
        )
        self.assertIsNone(result)

    def test_then_body_evaluates_and_returns_last_expression(self):
        result = self.helper_run_in_scenario_context(
            '(then "an outcome is validated" (= result-value 42))'
        )
        self.assertTrue(result)

    def test_then_no_body(self):
        result = self.helper_run_in_scenario_context(
            '(then "an outcome without specific checks")'
        )
        self.assertIsNone(result)

    def test_then_arity_error_no_args(self):
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_scenario_context("(then)")
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'then' expects at least a description string, got 0 arguments.",
        )

    def test_then_arity_error_no_description_string(self):
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_scenario_context("(then (= result-value 42))")
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'then' expects a description string as its first argument.",
        )

    def test_then_description_not_a_string(self):
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_scenario_context("(then 123 (= result-value 42))")
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'then' expects a description string as its first argument.",
        )

    def test_then_outside_it_block(self):
        registry.start_feature("Dummy Feature for Context Test")
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(then "an outcome" (print "test"))', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'then' form can only be used inside an 'it' block.",
        )
        registry.end_feature()


if __name__ == "__main__":
    unittest.main()
