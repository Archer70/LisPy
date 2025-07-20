# tests/functions/boolean_q_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class IsBooleanQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_boolean_q_true(self):
        """Test (is-boolean? true) returns true."""
        self.assertTrue(run_lispy_string("(is-boolean? true)", self.env))

    def test_boolean_q_false(self):
        """Test (is-boolean? false) returns true."""
        self.assertTrue(run_lispy_string("(is-boolean? false)", self.env))

    def test_boolean_q_function_result_true(self):
        """Test that is-boolean? correctly identifies true returned from functions."""
        run_lispy_string("(define get-true (fn [] true))", self.env)
        self.assertTrue(run_lispy_string("(is-boolean? (get-true))", self.env))

    def test_boolean_q_function_result_false(self):
        """Test that is-boolean? correctly identifies false returned from functions."""
        run_lispy_string("(define get-false (fn [] false))", self.env)
        self.assertTrue(run_lispy_string("(is-boolean? (get-false))", self.env))

    def test_boolean_q_comparison_result_true(self):
        """Test that is-boolean? correctly identifies boolean results from comparisons."""
        self.assertTrue(run_lispy_string("(is-boolean? (= 1 1))", self.env))
        self.assertTrue(run_lispy_string("(is-boolean? (< 1 2))", self.env))

    def test_boolean_q_comparison_result_false(self):
        """Test that is-boolean? correctly identifies boolean results from comparisons."""
        self.assertTrue(run_lispy_string("(is-boolean? (= 1 2))", self.env))
        self.assertTrue(run_lispy_string("(is-boolean? (> 1 2))", self.env))

    def test_boolean_q_logical_operations(self):
        """Test that is-boolean? correctly identifies results from logical operations."""
        self.assertTrue(run_lispy_string("(is-boolean? (not true))", self.env))
        self.assertTrue(run_lispy_string("(is-boolean? (not false))", self.env))

    def test_boolean_q_nil(self):
        """Test (is-boolean? nil) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? nil)", self.env))

    def test_boolean_q_number_zero(self):
        """Test (is-boolean? 0) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? 0)", self.env))

    def test_boolean_q_number_one(self):
        """Test (is-boolean? 1) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? 1)", self.env))

    def test_boolean_q_number_positive(self):
        """Test (is-boolean? 42) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? 42)", self.env))

    def test_boolean_q_number_negative(self):
        """Test (is-boolean? -17) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? -17)", self.env))

    def test_boolean_q_float(self):
        """Test (is-boolean? 3.14) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? 3.14)", self.env))

    def test_boolean_q_string(self):
        """Test (is-boolean? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is-boolean? "hello")', self.env))

    def test_boolean_q_empty_string(self):
        """Test (is-boolean? \"\") returns false."""
        self.assertFalse(run_lispy_string('(is-boolean? "")', self.env))

    def test_boolean_q_empty_list(self):
        """Test (is-boolean? '()) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? '())", self.env))

    def test_boolean_q_list_with_elements(self):
        """Test (is-boolean? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? '(1 2 3))", self.env))

    def test_boolean_q_empty_vector(self):
        """Test (is-boolean? []) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? [])", self.env))

    def test_boolean_q_vector_with_elements(self):
        """Test (is-boolean? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? [1 2 3])", self.env))

    def test_boolean_q_empty_map(self):
        """Test (is-boolean? {}) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? {})", self.env))

    def test_boolean_q_map_with_elements(self):
        """Test (is-boolean? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? {:a 1})", self.env))

    def test_boolean_q_symbol(self):
        """Test (is-boolean? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is-boolean? 'x)", self.env))

    def test_boolean_q_no_args(self):
        """Test (is-boolean?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-boolean?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-boolean?' expects 1 argument, got 0."
        )

    def test_boolean_q_too_many_args(self):
        """Test (is-boolean? true false) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-boolean? true false)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-boolean?' expects 1 argument, got 2."
        )


if __name__ == "__main__":
    unittest.main()
