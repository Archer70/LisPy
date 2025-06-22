# tests/functions/string_q_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class IsStringQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_string_q_string(self):
        """Test (is-string? \"hello\") returns true."""
        self.assertTrue(run_lispy_string('(is-string? "hello")', self.env))

    def test_string_q_empty_string(self):
        """Test (is-string? \"\") returns true."""
        self.assertTrue(run_lispy_string('(is-string? "")', self.env))

    def test_string_q_multiline_string(self):
        """Test (is-string? \"hello\\nworld\") returns true."""
        self.assertTrue(run_lispy_string('(is-string? "hello\\nworld")', self.env))

    def test_string_q_number_string(self):
        """Test (is-string? \"123\") returns true."""
        self.assertTrue(run_lispy_string('(is-string? "123")', self.env))

    def test_string_q_integer(self):
        """Test (is-string? 42) returns false."""
        self.assertFalse(run_lispy_string("(is-string? 42)", self.env))

    def test_string_q_float(self):
        """Test (is-string? 3.14) returns false."""
        self.assertFalse(run_lispy_string("(is-string? 3.14)", self.env))

    def test_string_q_boolean_true(self):
        """Test (is-string? true) returns false."""
        self.assertFalse(run_lispy_string("(is-string? true)", self.env))

    def test_string_q_boolean_false(self):
        """Test (is-string? false) returns false."""
        self.assertFalse(run_lispy_string("(is-string? false)", self.env))

    def test_string_q_nil(self):
        """Test (is-string? nil) returns false."""
        self.assertFalse(run_lispy_string("(is-string? nil)", self.env))

    def test_string_q_vector(self):
        """Test (is-string? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is-string? [1 2 3])", self.env))

    def test_string_q_list(self):
        """Test (is-string? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is-string? '(1 2 3))", self.env))

    def test_string_q_map(self):
        """Test (is-string? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is-string? {:a 1})", self.env))

    def test_string_q_symbol(self):
        """Test (is-string? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is-string? 'x)", self.env))

    def test_string_q_no_args(self):
        """Test (is-string?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-string?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-string?' expects 1 argument, got 0."
        )

    def test_string_q_too_many_args(self):
        """Test (is-string? \"a\" \"b\") raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(is-string? "a" "b")', self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-string?' expects 1 argument, got 2."
        )


if __name__ == "__main__":
    unittest.main()
