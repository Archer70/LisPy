# tests/special_forms/bdd/given_form_test.py
import unittest

from lispy.functions import create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError
from lispy.bdd import registry # Import registry


class TestGivenForm(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        registry.clear_bdd_results()

    def helper_run_in_scenario_context(self, code_string):
        registry.start_feature("Test Feature for 'given'")
        registry.start_scenario("Test Scenario for 'given'")
        try:
            result = run_lispy_string(code_string, self.env)
        finally:
            registry.end_scenario()
            registry.end_feature()
        return result

    def test_given_basic_structure_with_body(self):
        # (given "a precondition" (define x 10))
        # `define` returns the assigned value.
        result = self.helper_run_in_scenario_context(
            '(given "a precondition" (define x 10))'
        )
        self.assertEqual(result, 10)
        # We can also check the side effect if define adds to env
        self.assertEqual(self.env.lookup('x'), 10)


    def test_given_body_evaluates_and_returns_last_expression(self):
        result = self.helper_run_in_scenario_context(
            '(given "a precondition" (define x 10) (+ x 5))'
        )
        self.assertEqual(result, 15)

    def test_given_no_body(self):
        # (given "a precondition without actions")
        result = self.helper_run_in_scenario_context('(given "a precondition without actions")')
        self.assertIsNone(result)

    def test_given_arity_error_no_args(self):
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_scenario_context('(given)')
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'given' expects at least a description string, got 0 arguments."
        )

    def test_given_arity_error_no_description_string(self):
        # (given (define x 10))
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_scenario_context('(given (define x 10))')
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'given' expects a description string as its first argument."
        )

    def test_given_description_not_a_string(self):
        # (given 123 (define x 10))
        with self.assertRaises(EvaluationError) as cm:
            self.helper_run_in_scenario_context('(given 123 (define x 10))')
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'given' expects a description string as its first argument."
        )

    def test_given_outside_it_block(self):
        # `given` should only be valid inside an `it` block.
        registry.start_feature("Dummy Feature for Context Test")
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(given "a condition" (print "test"))', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'given' form can only be used inside an 'it' block."
        )
        registry.end_feature() # Clean up

if __name__ == '__main__':
    unittest.main() 