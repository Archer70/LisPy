# tests/functions/vector_q_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class IsVectorQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_vector_q_empty_vector(self):
        """Test (is-vector? []) returns true."""
        self.assertTrue(run_lispy_string("(is-vector? [])", self.env))

    def test_vector_q_vector_with_elements(self):
        """Test (is-vector? [1 2 3]) returns true."""
        self.assertTrue(run_lispy_string("(is-vector? [1 2 3])", self.env))

    def test_vector_q_vector_function_result(self):
        """Test (is-vector? (vector 1 2 3)) returns true."""
        self.assertTrue(run_lispy_string("(is-vector? (vector 1 2 3))", self.env))

    def test_vector_q_nested_vector(self):
        """Test (is-vector? [1 [2 3] 4]) returns true."""
        self.assertTrue(run_lispy_string("(is-vector? [1 [2 3] 4])", self.env))

    def test_vector_q_mixed_types_vector(self):
        """Test (is-vector? [1 \"hello\" true nil]) returns true."""
        self.assertTrue(run_lispy_string('(is-vector? [1 "hello" true nil])', self.env))

    def test_vector_q_vector_with_list(self):
        """Test (is-vector? [1 '(2 3) 4]) returns true."""
        self.assertTrue(run_lispy_string("(is-vector? [1 '(2 3) 4])", self.env))

    def test_vector_q_list(self):
        """Test (is-vector? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is-vector? '(1 2 3))", self.env))

    def test_vector_q_empty_list(self):
        """Test (is-vector? '()) returns false."""
        self.assertFalse(run_lispy_string("(is-vector? '())", self.env))

    def test_vector_q_list_function_result(self):
        """Test (is-vector? (list 1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is-vector? (list 1 2 3))", self.env))

    def test_vector_q_string(self):
        """Test (is-vector? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is-vector? "hello")', self.env))

    def test_vector_q_number(self):
        """Test (is-vector? 42) returns false."""
        self.assertFalse(run_lispy_string("(is-vector? 42)", self.env))

    def test_vector_q_boolean_true(self):
        """Test (is-vector? true) returns false."""
        self.assertFalse(run_lispy_string("(is-vector? true)", self.env))

    def test_vector_q_boolean_false(self):
        """Test (is-vector? false) returns false."""
        self.assertFalse(run_lispy_string("(is-vector? false)", self.env))

    def test_vector_q_nil(self):
        """Test (is-vector? nil) returns false."""
        self.assertFalse(run_lispy_string("(is-vector? nil)", self.env))

    def test_vector_q_map(self):
        """Test (is-vector? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is-vector? {:a 1})", self.env))

    def test_vector_q_symbol(self):
        """Test (is-vector? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is-vector? 'x)", self.env))

    def test_vector_q_no_args(self):
        """Test (is-vector?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-vector?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-vector?' expects 1 argument, got 0."
        )

    def test_vector_q_too_many_args(self):
        """Test (is-vector? [1] [2]) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-vector? [1] [2])", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-vector?' expects 1 argument, got 2."
        )

    def test_vector_q_vs_list_q_distinction(self):
        """Test that is-vector? and is-list? correctly distinguish between vectors and lists."""
        # Test that is-vector? returns true for vectors but false for lists
        self.assertTrue(run_lispy_string("(is-vector? (vector 1 2 3))", self.env))
        self.assertFalse(run_lispy_string("(is-vector? (list 1 2 3))", self.env))

        # Test that is-list? returns true for lists but false for vectors
        self.assertTrue(run_lispy_string("(is-list? (list 1 2 3))", self.env))
        self.assertFalse(run_lispy_string("(is-list? (vector 1 2 3))", self.env))


if __name__ == "__main__":
    unittest.main()
