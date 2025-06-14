# tests/functions/list_q_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class IsListQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_list_q_empty_list(self):
        """Test (is_list? '()) returns true."""
        self.assertTrue(run_lispy_string("(is_list? '())", self.env))

    def test_list_q_list_with_elements(self):
        """Test (is_list? '(1 2 3)) returns true."""
        self.assertTrue(run_lispy_string("(is_list? '(1 2 3))", self.env))

    def test_list_q_list_function_result(self):
        """Test (is_list? (list 1 2 3)) returns true."""
        self.assertTrue(run_lispy_string("(is_list? (list 1 2 3))", self.env))

    def test_list_q_nested_list(self):
        """Test (is_list? '(1 (2 3) 4)) returns true."""
        self.assertTrue(run_lispy_string("(is_list? '(1 (2 3) 4))", self.env))

    def test_list_q_mixed_types_list(self):
        """Test (is_list? '(1 \"hello\" true nil)) returns true."""
        self.assertTrue(run_lispy_string('(is_list? \'(1 "hello" true nil))', self.env))

    def test_list_q_vector(self):
        """Test (is_list? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is_list? [1 2 3])", self.env))

    def test_list_q_empty_vector(self):
        """Test (is_list? []) returns false."""
        self.assertFalse(run_lispy_string("(is_list? [])", self.env))

    def test_list_q_vector_function_result(self):
        """Test (is_list? (vector 1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is_list? (vector 1 2 3))", self.env))

    def test_list_q_string(self):
        """Test (is_list? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is_list? "hello")', self.env))

    def test_list_q_number(self):
        """Test (is_list? 42) returns false."""
        self.assertFalse(run_lispy_string("(is_list? 42)", self.env))

    def test_list_q_boolean_true(self):
        """Test (is_list? true) returns false."""
        self.assertFalse(run_lispy_string("(is_list? true)", self.env))

    def test_list_q_boolean_false(self):
        """Test (is_list? false) returns false."""
        self.assertFalse(run_lispy_string("(is_list? false)", self.env))

    def test_list_q_nil(self):
        """Test (is_list? nil) returns false."""
        self.assertFalse(run_lispy_string("(is_list? nil)", self.env))

    def test_list_q_map(self):
        """Test (is_list? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is_list? {:a 1})", self.env))

    def test_list_q_symbol(self):
        """Test (is_list? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is_list? 'x)", self.env))

    def test_list_q_no_args(self):
        """Test (is_list?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is_list?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is_list?' expects 1 argument, got 0."
        )

    def test_list_q_too_many_args(self):
        """Test (is_list? '(1) '(2)) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is_list? '(1) '(2))", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is_list?' expects 1 argument, got 2."
        )

    def test_list_q_vs_is_vector_q_distinction(self):
        """Test that is_list? and is_vector? correctly distinguish between lists and vectors."""
        # Test that is_list? returns true for lists but false for vectors
        self.assertTrue(run_lispy_string("(is_list? (list 1 2 3))", self.env))
        self.assertFalse(run_lispy_string("(is_list? (vector 1 2 3))", self.env))

        # Test that is_vector? returns true for vectors but false for lists
        self.assertTrue(run_lispy_string("(is_vector? (vector 1 2 3))", self.env))
        self.assertFalse(run_lispy_string("(is_vector? (list 1 2 3))", self.env))


if __name__ == "__main__":
    unittest.main()
