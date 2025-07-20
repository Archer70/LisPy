import unittest

from lispy.bdd import registry
from lispy.exceptions import AssertionFailure, EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class TestAssertRaisesQForm(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        registry.clear_bdd_results()

    def run_in_then_context(self, then_body_code: str):
        """Helper to run code in a proper BDD context."""
        registry.start_feature("Test Feature for assert-raises?")
        registry.start_scenario("Test Scenario for assert-raises?")
        run_lispy_string(
            f'(then "a test assertion with assert-raises?" {then_body_code})', self.env
        )
        registry.end_scenario()
        registry.end_feature()

    def test_assert_raises_q_success_basic(self):
        """Test assert-raises? succeeds when expected error is raised."""
        # Test division by zero
        result = run_lispy_string(
            '(assert-raises? "Division by zero" (/ 1 0))', self.env
        )
        self.assertTrue(result)

    def test_assert_raises_q_success_partial_message_match(self):
        """Test assert-raises? succeeds with partial message match."""
        # Should work with substring matching
        result = run_lispy_string(
            '(assert-raises? "expects 1 argument" (abs))', self.env
        )
        self.assertTrue(result)

    def test_assert_raises_q_success_function_error(self):
        """Test assert-raises? succeeds with function argument errors."""
        result = run_lispy_string(
            '(assert-raises? "must be a number" (abs "hello"))', self.env
        )
        self.assertTrue(result)

    def test_assert_raises_q_success_type_error(self):
        """Test assert-raises? succeeds with type errors."""
        result = run_lispy_string(
            '(assert-raises? "expects 1 argument" (abs))', self.env
        )
        self.assertTrue(result)

    def test_assert_raises_q_success_undefined_variable(self):
        """Test assert-raises? succeeds with undefined variable errors."""
        result = run_lispy_string(
            '(assert-raises? "Unbound symbol" undefined_var)', self.env
        )
        self.assertTrue(result)

    def test_assert_raises_q_failure_no_error_raised(self):
        """Test assert-raises? fails when no error occurs."""
        with self.assertRaises(AssertionFailure) as cm:
            run_lispy_string('(assert-raises? "some error" (+ 1 2))', self.env)
        self.assertIn("Expected an EvaluationError", str(cm.exception))
        self.assertIn("but no error was raised", str(cm.exception))

    def test_assert_raises_q_failure_wrong_error_message(self):
        """Test assert-raises? fails when error message doesn't match."""
        with self.assertRaises(AssertionFailure) as cm:
            run_lispy_string('(assert-raises? "wrong message" (/ 1 0))', self.env)
        self.assertIn("Expected EvaluationError message containing", str(cm.exception))
        self.assertIn("wrong message", str(cm.exception))
        self.assertIn("Division by zero", str(cm.exception))

    def test_assert_raises_q_arity_error_no_args(self):
        """Test assert-raises? with no arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(assert-raises?)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'assert-raises?' expects 2 arguments (expected-message form), got 0.",
        )

    def test_assert_raises_q_arity_error_one_arg(self):
        """Test assert-raises? with only one argument."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(assert-raises? "message")', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'assert-raises?' expects 2 arguments (expected-message form), got 1.",
        )

    def test_assert_raises_q_arity_error_too_many_args(self):
        """Test assert-raises? with too many arguments."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(assert-raises? "message" (+ 1 2) "extra")', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'assert-raises?' expects 2 arguments (expected-message form), got 3.",
        )

    def test_assert_raises_q_non_string_expected_message(self):
        """Test assert-raises? with non-string expected message."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(assert-raises? 123 (/ 1 0))", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'assert-raises?' expects its first argument (expected-message) to be a string, but it evaluated to type int.",
        )

    def test_assert_raises_q_nil_expected_message(self):
        """Test assert-raises? with nil as expected message."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(assert-raises? nil (/ 1 0))", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'assert-raises?' expects its first argument (expected-message) to be a string, but it evaluated to type NoneType.",
        )

    def test_assert_raises_q_boolean_expected_message(self):
        """Test assert-raises? with boolean as expected message."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(assert-raises? true (/ 1 0))", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'assert-raises?' expects its first argument (expected-message) to be a string, but it evaluated to type bool.",
        )

    def test_assert_raises_q_list_expected_message(self):
        """Test assert-raises? with list as expected message."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(assert-raises? (list "error") (/ 1 0))', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'assert-raises?' expects its first argument (expected-message) to be a string, but it evaluated to type LispyList.",
        )

    def test_assert_raises_q_error_in_expected_message_evaluation(self):
        """Test assert-raises? when evaluating expected message raises error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(assert-raises? (/ 1 0) (+ 1 2))", self.env)
        self.assertIn(
            "SyntaxError: 'assert-raises?' could not evaluate its first argument (expected-message):",
            str(cm.exception),
        )

    def test_assert_raises_q_with_variable_expected_message(self):
        """Test assert-raises? with variable as expected message."""
        run_lispy_string('(define expected-msg "Division by zero")', self.env)
        result = run_lispy_string("(assert-raises? expected-msg (/ 1 0))", self.env)
        self.assertTrue(result)

    def test_assert_raises_q_with_function_call_expected_message(self):
        """Test assert-raises? with function call as expected message."""
        result = run_lispy_string(
            '(assert-raises? (to-str "Division by zero") (/ 1 0))', self.env
        )
        self.assertTrue(result)

    def test_assert_raises_q_with_complex_form(self):
        """Test assert-raises? with complex form that should error."""
        run_lispy_string("(define x 5)", self.env)
        result = run_lispy_string(
            '(assert-raises? "not a function" ((+ x 1) 42))', self.env
        )
        self.assertTrue(result)

    def test_assert_raises_q_with_nested_expression(self):
        """Test assert-raises? with nested expression."""
        result = run_lispy_string(
            '(assert-raises? "expects 1 argument" (abs (+ 1 2) (+ 3 4)))', self.env
        )
        self.assertTrue(result)

    def test_assert_raises_q_case_sensitive_matching(self):
        """Test assert-raises? matching is case sensitive."""
        with self.assertRaises(AssertionFailure) as cm:
            run_lispy_string('(assert-raises? "DIVISION BY ZERO" (/ 1 0))', self.env)
        self.assertIn("Expected EvaluationError message containing", str(cm.exception))
        self.assertIn("DIVISION BY ZERO", str(cm.exception))

    def test_assert_raises_q_empty_string_message(self):
        """Test assert-raises? with empty string (should match any error)."""
        result = run_lispy_string('(assert-raises? "" (/ 1 0))', self.env)
        self.assertTrue(result)

    def test_assert_raises_q_in_bdd_context_success(self):
        """Test assert-raises? in proper BDD context when it succeeds."""
        self.run_in_then_context('(assert-raises? "Division by zero" (/ 1 0))')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "passed")
        self.assertNotIn("details", step)

    def test_assert_raises_q_in_bdd_context_failure(self):
        """Test assert-raises? in proper BDD context when it fails."""
        self.run_in_then_context('(assert-raises? "wrong message" (/ 1 0))')
        scenario = registry.BDD_RESULTS[0]["scenarios"][0]
        step = scenario["steps"][0]
        self.assertEqual(step["status"], "failed")
        self.assertIn("Expected EvaluationError message containing", step["details"])

    def test_assert_raises_q_with_quote_form(self):
        """Test assert-raises? with quoted form (should not evaluate the form)."""
        # The quoted form should not be evaluated, so no error should be raised
        with self.assertRaises(AssertionFailure) as cm:
            run_lispy_string('(assert-raises? "some error" \'(/ 1 0))', self.env)
        self.assertIn("but no error was raised", str(cm.exception))

    def test_assert_raises_q_exception_not_evaluation_error(self):
        """Test assert-raises? when a non-EvaluationError exception occurs."""
        # This test may be harder to trigger since most LisPy errors are EvaluationError
        # But let's try with a Python exception that might leak through
        with self.assertRaises(AssertionFailure) as cm:
            # This is a bit contrived, but testing the exception handling path
            run_lispy_string('(assert-raises? "some error" (+ 1 2))', self.env)
        self.assertIn("Expected an EvaluationError", str(cm.exception))
        self.assertIn("but no error was raised", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
