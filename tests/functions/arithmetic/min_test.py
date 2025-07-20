# tests/functions/min_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class MinFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_min_single_number(self):
        """Test (min 5) returns 5."""
        result = run_lispy_string("(min 5)", self.env)
        self.assertEqual(result, 5)

    def test_min_two_numbers_integers(self):
        """Test (min 3 7) returns 3."""
        result = run_lispy_string("(min 3 7)", self.env)
        self.assertEqual(result, 3)

    def test_min_two_numbers_equal(self):
        """Test (min 5 5) returns 5."""
        result = run_lispy_string("(min 5 5)", self.env)
        self.assertEqual(result, 5)

    def test_min_three_numbers(self):
        """Test (min 10 3 7) returns 3."""
        result = run_lispy_string("(min 10 3 7)", self.env)
        self.assertEqual(result, 3)

    def test_min_many_numbers(self):
        """Test (min 15 3 8 1 12 6) returns 1."""
        result = run_lispy_string("(min 15 3 8 1 12 6)", self.env)
        self.assertEqual(result, 1)

    def test_min_floats(self):
        """Test (min 3.14 2.71 1.41) returns 1.41."""
        result = run_lispy_string("(min 3.14 2.71 1.41)", self.env)
        self.assertEqual(result, 1.41)

    def test_min_mixed_types(self):
        """Test (min 5 3.2 7) returns 3.2."""
        result = run_lispy_string("(min 5 3.2 7)", self.env)
        self.assertEqual(result, 3.2)

    def test_min_negative_numbers(self):
        """Test (min -5 -2 -8) returns -8."""
        result = run_lispy_string("(min -5 -2 -8)", self.env)
        self.assertEqual(result, -8)

    def test_min_positive_and_negative(self):
        """Test (min 5 -3 2) returns -3."""
        result = run_lispy_string("(min 5 -3 2)", self.env)
        self.assertEqual(result, -3)

    def test_min_with_zero(self):
        """Test (min 0 -1 1) returns -1."""
        result = run_lispy_string("(min 0 -1 1)", self.env)
        self.assertEqual(result, -1)

    def test_min_zeros(self):
        """Test (min 0 0.0 0) returns 0."""
        result = run_lispy_string("(min 0 0.0 0)", self.env)
        self.assertEqual(result, 0)

    def test_min_large_numbers(self):
        """Test (min 1000000 500000 2000000) returns 500000."""
        result = run_lispy_string("(min 1000000 500000 2000000)", self.env)
        self.assertEqual(result, 500000)

    def test_min_very_small_numbers(self):
        """Test (min 0.001 0.0001 0.01) returns 0.0001."""
        result = run_lispy_string("(min 0.001 0.0001 0.01)", self.env)
        self.assertEqual(result, 0.0001)

    def test_min_expression_results(self):
        """Test (min (+ 2 3) (* 2 3) (- 10 3)) returns 5."""
        result = run_lispy_string("(min (+ 2 3) (* 2 3) (- 10 3))", self.env)
        self.assertEqual(result, 5)

    def test_min_no_args(self):
        """Test (min) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(min)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'min' expects at least 1 argument, got 0."
        )

    def test_min_non_number_first(self):
        """Test (min \"hello\" 5) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(min "hello" 5)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 1 to 'min' must be a number, got str: 'hello'",
        )

    def test_min_non_number_middle(self):
        """Test (min 3 \"hello\" 7) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(min 3 "hello" 7)', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to 'min' must be a number, got str: 'hello'",
        )

    def test_min_non_number_last(self):
        """Test (min 3 5 \"hello\") raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(min 3 5 "hello")', self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 3 to 'min' must be a number, got str: 'hello'",
        )

    def test_min_boolean(self):
        """Test (min 5 true) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(min 5 true)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to 'min' must be a number, got bool: 'True'",
        )

    def test_min_nil(self):
        """Test (min 5 nil) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(min 5 nil)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to 'min' must be a number, got NoneType: 'None'",
        )

    def test_min_collection(self):
        """Test (min 5 [1 2]) raises an error."""
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(min 5 [1 2])", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: Argument 2 to 'min' must be a number, got Vector: '[1 2]'",
        )


if __name__ == "__main__":
    unittest.main()
