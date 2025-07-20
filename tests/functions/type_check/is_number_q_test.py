# tests/functions/number_q_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class IsNumberQFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_number_q_integer(self):
        """Test (is-number? 42) returns true."""
        self.assertTrue(run_lispy_string("(is-number? 42)", self.env))

    def test_number_q_negative_integer(self):
        """Test (is-number? -17) returns true."""
        self.assertTrue(run_lispy_string("(is-number? -17)", self.env))

    def test_number_q_zero(self):
        """Test (is-number? 0) returns true."""
        self.assertTrue(run_lispy_string("(is-number? 0)", self.env))

    def test_number_q_float(self):
        """Test (is-number? 3.14) returns true."""
        self.assertTrue(run_lispy_string("(is-number? 3.14)", self.env))

    def test_number_q_negative_float(self):
        """Test (is-number? -2.5) returns true."""
        self.assertTrue(run_lispy_string("(is-number? -2.5)", self.env))

    def test_number_q_string(self):
        """Test (is-number? \"hello\") returns false."""
        self.assertFalse(run_lispy_string('(is-number? "hello")', self.env))

    def test_number_q_boolean_true(self):
        """Test (is-number? true) returns false."""
        self.assertFalse(run_lispy_string("(is-number? true)", self.env))

    def test_number_q_boolean_false(self):
        """Test (is-number? false) returns false."""
        self.assertFalse(run_lispy_string("(is-number? false)", self.env))

    def test_number_q_nil(self):
        """Test (is-number? nil) returns false."""
        self.assertFalse(run_lispy_string("(is-number? nil)", self.env))

    def test_number_q_vector(self):
        """Test (is-number? [1 2 3]) returns false."""
        self.assertFalse(run_lispy_string("(is-number? [1 2 3])", self.env))

    def test_number_q_list(self):
        """Test (is-number? '(1 2 3)) returns false."""
        self.assertFalse(run_lispy_string("(is-number? '(1 2 3))", self.env))

    def test_number_q_map(self):
        """Test (is-number? {:a 1}) returns false."""
        self.assertFalse(run_lispy_string("(is-number? {:a 1})", self.env))

    def test_number_q_symbol(self):
        """Test (is-number? 'x) returns false."""
        self.assertFalse(run_lispy_string("(is-number? 'x)", self.env))

    def test_number_q_no_args(self):
        """Test (is-number?) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-number?)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-number?' expects 1 argument, got 0."
        )

    def test_number_q_too_many_args(self):
        """Test (is-number? 1 2) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(is-number? 1 2)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'is-number?' expects 1 argument, got 2."
        )


if __name__ == "__main__":
    unittest.main()
