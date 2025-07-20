# tests/functions/max_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class MaxFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_max_single_number(self):
        """Test (max 5) returns 5."""
        result = run_lispy_string("(max 5)", self.env)
        self.assertEqual(result, 5)

    def test_max_two_numbers_integers(self):
        """Test (max 3 7) returns 7."""
        result = run_lispy_string("(max 3 7)", self.env)
        self.assertEqual(result, 7)

    def test_max_two_numbers_equal(self):
        """Test (max 5 5) returns 5."""
        result = run_lispy_string("(max 5 5)", self.env)
        self.assertEqual(result, 5)

    def test_max_three_numbers(self):
        """Test (max 10 3 7) returns 10."""
        result = run_lispy_string("(max 10 3 7)", self.env)
        self.assertEqual(result, 10)

    def test_max_many_numbers(self):
        """Test (max 15 3 8 1 12 6) returns 15."""
        result = run_lispy_string("(max 15 3 8 1 12 6)", self.env)
        self.assertEqual(result, 15)

    def test_max_floats(self):
        """Test (max 3.14 2.71 1.41) returns 3.14."""
        result = run_lispy_string("(max 3.14 2.71 1.41)", self.env)
        self.assertEqual(result, 3.14)

    def test_max_mixed_types(self):
        """Test (max 5 3.2 7) returns 7."""
        result = run_lispy_string("(max 5 3.2 7)", self.env)
        self.assertEqual(result, 7)

    def test_max_negative_numbers(self):
        """Test (max -5 -2 -8) returns -2."""
        result = run_lispy_string("(max -5 -2 -8)", self.env)
        self.assertEqual(result, -2)

    def test_max_positive_and_negative(self):
        """Test (max 5 -3 2) returns 5."""
        result = run_lispy_string("(max 5 -3 2)", self.env)
        self.assertEqual(result, 5)

    def test_max_with_zero(self):
        """Test (max 0 -1 1) returns 1."""
        result = run_lispy_string("(max 0 -1 1)", self.env)
        self.assertEqual(result, 1)

    def test_max_zeros(self):
        """Test (max 0 0.0 0) returns 0."""
        result = run_lispy_string("(max 0 0.0 0)", self.env)
        self.assertEqual(result, 0)

    def test_max_large_numbers(self):
        """Test (max 1000000 500000 2000000) returns 2000000."""
        result = run_lispy_string("(max 1000000 500000 2000000)", self.env)
        self.assertEqual(result, 2000000)

    def test_max_very_small_numbers(self):
        """Test (max 0.001 0.0001 0.01) returns 0.01."""
        result = run_lispy_string("(max 0.001 0.0001 0.01)", self.env)
        self.assertEqual(result, 0.01)

    def test_max_expression_results(self):
        """Test (max (+ 2 3) (* 2 3) (- 10 3)) returns 7."""
        result = run_lispy_string("(max (+ 2 3) (* 2 3) (- 10 3))", self.env)
        self.assertEqual(result, 7)

    def test_max_no_args(self):
        """Test (max) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(max)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'max' expects at least 1 argument, got 0."
        )

    def test_max_non_number_first(self):
        """Test (max \"hello\" 5) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(max "hello" 5)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 1 to 'max' must be a number, got str: 'hello'",
        )

    def test_max_non_number_middle(self):
        """Test (max 3 \"hello\" 7) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(max 3 "hello" 7)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to 'max' must be a number, got str: 'hello'",
        )

    def test_max_non_number_last(self):
        """Test (max 3 5 \"hello\") raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(max 3 5 "hello")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 3 to 'max' must be a number, got str: 'hello'",
        )

    def test_max_boolean(self):
        """Test (max 5 true) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(max 5 true)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to 'max' must be a number, got bool: 'True'",
        )

    def test_max_nil(self):
        """Test (max 5 nil) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(max 5 nil)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to 'max' must be a number, got NoneType: 'None'",
        )

    def test_max_collection(self):
        """Test (max 5 [1 2]) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(max 5 [1 2])", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to 'max' must be a number, got Vector: '[1 2]'",
        )


if __name__ == "__main__":
    unittest.main()
