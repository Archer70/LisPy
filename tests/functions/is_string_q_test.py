# tests/functions/string_q_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class IsStringQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_string_q_string(self):
        """Test (is_string? \"hello\") returns true."""
        self.assertTrue(run_lispy_string('(is_string? "hello")', self.env))

    def test_string_q_empty_string(self):
        """Test (is_string? \"\") returns true."""
        self.assertTrue(run_lispy_string('(is_string? "")', self.env))

    def test_string_q_multiline_string(self):
        """Test (is_string? \"hello\\nworld\") returns true."""
        self.assertTrue(run_lispy_string('(is_string? "hello\\nworld")', self.env))

    def test_string_q_number_string(self):
        """Test (is_string? \"123\") returns true."""
        self.assertTrue(run_lispy_string('(is_string? "123")', self.env))

    def test_string_q_integer(self):
        """Test (is_string? 42) returns false."""
        self.assertFalse(run_lispy_string("(is_string? 42)", self.env))

    def test_string_q_float(self):
        """Test (is_string? 3.14) returns false."""
        self.assertFalse(run_lispy_string("(is_string? 3.14)", self.env))

    def test_string_q_boolean_true(self):
        """Test (is_string? true) returns false."""
        self.assertFalse(run_lispy_string("(is_string? true)", self.env))

    def test_string_q_boolean_false(self):
        """Test (is_string? false) returns false."""
        self.assertFalse(run_lispy_string("(is_string? false)", self.env))

    def test_string_q_nil(self):
        """Test (is_string? nil) returns false."""
        self.assertFalse(run_lispy_string("(is_string? nil)", self.env))

    def test_string_q_vector(self):
        """Test (is_string? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is_string? [1 2 3])", self.env))

    def test_string_q_list(self):
        """Test (is_string? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is_string? '(1 2 3))", self.env))

    def test_string_q_map(self):
        """Test (is_string? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is_string? {:a 1})", self.env))

    def test_string_q_symbol(self):
        """Test (is_string? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is_string? 'x)", self.env))

    def test_string_q_no_args(self):
        """Test (is_string?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is_string?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is_string?' expects 1 argument, got 0."
        )

    def test_string_q_too_many_args(self):
        """Test (is_string? \"a\" \"b\") raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(is_string? "a" "b")', self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is_string?' expects 1 argument, got 2."
        )


if __name__ == "__main__":
    unittest.main()
