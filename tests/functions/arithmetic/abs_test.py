# tests/functions/abs_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class AbsFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_abs_positive_integer(self):
        """Test (abs 5) returns 5."""
        result = run_lispy_string("(abs 5)", self.env)
        self.assertEqual(result, 5)

    def test_abs_negative_integer(self):
        """Test (abs -5) returns 5."""
        result = run_lispy_string("(abs -5)", self.env)
        self.assertEqual(result, 5)

    def test_abs_zero(self):
        """Test (abs 0) returns 0."""
        result = run_lispy_string("(abs 0)", self.env)
        self.assertEqual(result, 0)

    def test_abs_positive_float(self):
        """Test (abs 3.14) returns 3.14."""
        result = run_lispy_string("(abs 3.14)", self.env)
        self.assertEqual(result, 3.14)

    def test_abs_negative_float(self):
        """Test (abs -3.14) returns 3.14."""
        result = run_lispy_string("(abs -3.14)", self.env)
        self.assertEqual(result, 3.14)

    def test_abs_very_small_positive(self):
        """Test (abs 0.001) returns 0.001."""
        result = run_lispy_string("(abs 0.001)", self.env)
        self.assertEqual(result, 0.001)

    def test_abs_very_small_negative(self):
        """Test (abs -0.001) returns 0.001."""
        result = run_lispy_string("(abs -0.001)", self.env)
        self.assertEqual(result, 0.001)

    def test_abs_large_positive(self):
        """Test (abs 1000000) returns 1000000."""
        result = run_lispy_string("(abs 1000000)", self.env)
        self.assertEqual(result, 1000000)

    def test_abs_large_negative(self):
        """Test (abs -1000000) returns 1000000."""
        result = run_lispy_string("(abs -1000000)", self.env)
        self.assertEqual(result, 1000000)

    def test_abs_expression_result(self):
        """Test (abs (- 3 8)) returns 5."""
        result = run_lispy_string("(abs (- 3 8))", self.env)
        self.assertEqual(result, 5)

    def test_abs_no_args(self):
        """Test (abs) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(abs)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'abs' expects 1 argument, got 0."
        )

    def test_abs_too_many_args(self):
        """Test (abs 1 2) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(abs 1 2)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'abs' expects 1 argument, got 2."
        )

    def test_abs_non_number(self):
        """Test (abs \"hello\") raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(abs "hello")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument to 'abs' must be a number, got str: 'hello'",
        )

    def test_abs_boolean(self):
        """Test (abs true) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(abs true)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument to 'abs' must be a number, got bool: 'True'",
        )

    def test_abs_nil(self):
        """Test (abs nil) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(abs nil)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument to 'abs' must be a number, got NoneType: 'None'",
        )

    def test_abs_list(self):
        """Test (abs [1 2 3]) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(abs [1 2 3])", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument to 'abs' must be a number, got Vector: '[1 2 3]'",
        )


if __name__ == "__main__":
    unittest.main()
