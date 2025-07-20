# tests/functions/is_function_q_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class IsFunctionQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_function_q_builtin_function(self):
        """Test (is-function? +) returns true for built-in functions."""
        self.assertTrue(run_lispy_string("(is-function? +)", self.env))

    def test_function_q_user_defined_function(self):
        """Test that is-function? returns true for user-defined functions."""
        # Define a function first, then test it
        run_lispy_string("(define my-fn (fn [x] (* x 2)))", self.env)
        self.assertTrue(run_lispy_string("(is-function? my-fn)", self.env))

    def test_function_q_lambda_function(self):
        """Test that is-function? returns true for lambda functions."""
        self.assertTrue(run_lispy_string("(is-function? (fn [x] (+ x 1)))", self.env))

    def test_function_q_other_builtin_functions(self):
        """Test that is-function? returns true for various built-in functions."""
        builtin_functions = [
            "+",
            "-",
            "*",
            "/",
            "=",
            "<",
            ">",
            "list",
            "vector",
            "count",
            "first",
            "rest",
            "cons",
            "map",
            "filter",
            "reduce",
        ]

        for func_name in builtin_functions:
            with self.subTest(function=func_name):
                self.assertTrue(
                    run_lispy_string(f"(is-function? {func_name})", self.env)
                )

    def test_function_q_number(self):
        """Test (is-function? 42) returns false."""
        self.assertFalse(run_lispy_string("(is-function? 42)", self.env))

    def test_function_q_string(self):
        """Test (is-function? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is-function? "hello")', self.env))

    def test_function_q_boolean_true(self):
        """Test (is-function? true) returns false."""
        self.assertFalse(run_lispy_string("(is-function? true)", self.env))

    def test_function_q_boolean_false(self):
        """Test (is-function? false) returns false."""
        self.assertFalse(run_lispy_string("(is-function? false)", self.env))

    def test_function_q_nil(self):
        """Test (is-function? nil) returns false."""
        self.assertFalse(run_lispy_string("(is-function? nil)", self.env))

    def test_function_q_list(self):
        """Test (is-function? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is-function? '(1 2 3))", self.env))

    def test_function_q_empty_list(self):
        """Test (is-function? '()) returns false."""
        self.assertFalse(run_lispy_string("(is-function? '())", self.env))

    def test_function_q_vector(self):
        """Test (is-function? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is-function? [1 2 3])", self.env))

    def test_function_q_empty_vector(self):
        """Test (is-function? []) returns false."""
        self.assertFalse(run_lispy_string("(is-function? [])", self.env))

    def test_function_q_map(self):
        """Test (is-function? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is-function? {:a 1})", self.env))

    def test_function_q_empty_map(self):
        """Test (is-function? {}) returns false."""
        self.assertFalse(run_lispy_string("(is-function? {})", self.env))

    def test_function_q_symbol(self):
        """Test (is-function? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is-function? 'x)", self.env))

    def test_function_q_with_partial_application(self):
        """Test that is-function? works with partially applied functions."""
        # Create a partial application and test it
        run_lispy_string("(define add-5 (fn [x] (+ x 5)))", self.env)
        self.assertTrue(run_lispy_string("(is-function? add-5)", self.env))

    def test_function_q_nested_function_definition(self):
        """Test that is-function? works with nested function definitions."""
        # Define a function that returns a function
        run_lispy_string("(define make-adder (fn [n] (fn [x] (+ x n))))", self.env)
        run_lispy_string("(define add-10 (make-adder 10))", self.env)

        self.assertTrue(run_lispy_string("(is-function? make-adder)", self.env))
        self.assertTrue(run_lispy_string("(is-function? add-10)", self.env))

    def test_function_q_function_result(self):
        """Test that is-function? correctly identifies functions returned from other functions."""
        # Test helper functions that return functions or non-functions
        self.env.define(
            "get-function", lambda args, env: lambda x, e: x[0] if x else None
        )
        self.env.define("get-value", lambda args, env: 42)

        self.assertTrue(run_lispy_string("(is-function? (get-function))", self.env))
        self.assertFalse(run_lispy_string("(is-function? (get-value))", self.env))

    def test_function_q_no_args(self):
        """Test (is-function?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-function?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-function?' expects 1 argument, got 0."
        )

    def test_function_q_too_many_args(self):
        """Test (is-function? + -) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-function? + -)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-function?' expects 1 argument, got 2."
        )

    def test_function_q_vs_other_types(self):
        """Test that is-function? correctly distinguishes functions from other callable-like constructs."""
        # Test all other type checking functions to ensure they return false for functions
        run_lispy_string("(define test-fn (fn [x] x))", self.env)

        self.assertFalse(run_lispy_string("(is-number? test-fn)", self.env))
        self.assertFalse(run_lispy_string("(is-string? test-fn)", self.env))
        self.assertFalse(run_lispy_string("(is-list? test-fn)", self.env))
        self.assertFalse(run_lispy_string("(is-vector? test-fn)", self.env))
        self.assertFalse(run_lispy_string("(is-map? test-fn)", self.env))
        self.assertFalse(run_lispy_string("(is-boolean? test-fn)", self.env))
        self.assertFalse(run_lispy_string("(is-nil? test-fn)", self.env))

        # And vice versa - test that is-function? returns false for other types
        self.assertFalse(run_lispy_string("(is-function? 42)", self.env))
        self.assertFalse(run_lispy_string('(is-function? "string")', self.env))
        self.assertFalse(run_lispy_string("(is-function? [1 2 3])", self.env))
        self.assertFalse(run_lispy_string("(is-function? '(1 2 3))", self.env))
        self.assertFalse(run_lispy_string("(is-function? {:a 1})", self.env))
        self.assertFalse(run_lispy_string("(is-function? true)", self.env))
        self.assertFalse(run_lispy_string("(is-function? nil)", self.env))


if __name__ == "__main__":
    unittest.main()
