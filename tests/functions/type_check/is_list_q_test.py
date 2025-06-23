# tests/functions/list_q_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class IsListQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_list_q_empty_list(self):
        """Test (is-list? '()) returns true."""
        self.assertTrue(run_lispy_string("(is-list? '())", self.env))

    def test_list_q_list_with_elements(self):
        """Test (is-list? '(1 2 3)) returns true."""
        self.assertTrue(run_lispy_string("(is-list? '(1 2 3))", self.env))

    def test_list_q_list_function_result(self):
        """Test (is-list? (list 1 2 3)) returns true."""
        self.assertTrue(run_lispy_string("(is-list? (list 1 2 3))", self.env))

    def test_list_q_nested_list(self):
        """Test (is-list? '(1 (2 3) 4)) returns true."""
        self.assertTrue(run_lispy_string("(is-list? '(1 (2 3) 4))", self.env))

    def test_list_q_mixed_types_list(self):
        """Test (is-list? '(1 \"hello\" true nil)) returns true."""
        self.assertTrue(run_lispy_string('(is-list? \'(1 "hello" true nil))', self.env))

    def test_list_q_vector(self):
        """Test (is-list? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is-list? [1 2 3])", self.env))

    def test_list_q_empty_vector(self):
        """Test (is-list? []) returns false."""
        self.assertFalse(run_lispy_string("(is-list? [])", self.env))

    def test_list_q_vector_function_result(self):
        """Test (is-list? (vector 1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is-list? (vector 1 2 3))", self.env))

    def test_list_q_string(self):
        """Test (is-list? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is-list? "hello")', self.env))

    def test_list_q_number(self):
        """Test (is-list? 42) returns false."""
        self.assertFalse(run_lispy_string("(is-list? 42)", self.env))

    def test_list_q_boolean_true(self):
        """Test (is-list? true) returns false."""
        self.assertFalse(run_lispy_string("(is-list? true)", self.env))

    def test_list_q_boolean_false(self):
        """Test (is-list? false) returns false."""
        self.assertFalse(run_lispy_string("(is-list? false)", self.env))

    def test_list_q_nil(self):
        """Test (is-list? nil) returns false."""
        self.assertFalse(run_lispy_string("(is-list? nil)", self.env))

    def test_list_q_map(self):
        """Test (is-list? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is-list? {:a 1})", self.env))

    def test_list_q_symbol(self):
        """Test (is-list? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is-list? 'x)", self.env))

    def test_list_q_no_args(self):
        """Test (is-list?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-list?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-list?' expects 1 argument, got 0."
        )

    def test_list_q_too_many_args(self):
        """Test (is-list? '(1) '(2)) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-list? '(1) '(2))", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-list?' expects 1 argument, got 2."
        )

    def test_list_q_vs_is_vector_q_distinction(self):
        """Test that is-list? and is-vector? correctly distinguish between lists and vectors."""
        # Test that is-list? returns true for lists but false for vectors
        self.assertTrue(run_lispy_string("(is-list? (list 1 2 3))", self.env))
        self.assertFalse(run_lispy_string("(is-list? (vector 1 2 3))", self.env))

        # Test that is-vector? returns true for vectors but false for lists
        self.assertTrue(run_lispy_string("(is-vector? (vector 1 2 3))", self.env))
        self.assertFalse(run_lispy_string("(is-vector? (list 1 2 3))", self.env))


if __name__ == "__main__":
    unittest.main()
