# lispy_project/tests/functions/divide_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class DivideFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_divide_simple(self):
        self.assertEqual(run_lispy_string("(/ 10 2)", self.env), 5.0)

    def test_divide_multiple_args(self):
        self.assertEqual(run_lispy_string("(/ 100 2 5)", self.env), 10.0)

    def test_divide_produces_float(self):
        self.assertEqual(run_lispy_string("(/ 9 2)", self.env), 4.5)

    def test_divide_with_floats_input(self):
        self.assertEqual(run_lispy_string("(/ 5.0 2.0)", self.env), 2.5)
        self.assertAlmostEqual(run_lispy_string("(/ 10.0 2.5 2.0)", self.env), 2.0)

    def test_divide_negative_numbers(self):
        self.assertEqual(run_lispy_string("(/ -10 2)", self.env), -5.0)
        self.assertEqual(run_lispy_string("(/ 10 -2)", self.env), -5.0)
        self.assertEqual(run_lispy_string("(/ -10 -2)", self.env), 5.0)

    def test_divide_by_zero(self):
        with self.assertRaisesRegex(
            EvaluationError, r"ZeroDivisionError: Division by zero \(argument 2\)\."
        ):
            run_lispy_string("(/ 10 0)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, r"ZeroDivisionError: Division by zero \(argument 3\)\."
        ):
            run_lispy_string("(/ 10 2 0 5)", self.env)

    def test_divide_type_error_non_numeric(self):
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 1 to '/' must be a number, got str: 'a'",
        ):
            run_lispy_string('(/ "a" 5)', self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 2 to '/' must be a number, got Vector: '\[.*\]'",
        ):
            run_lispy_string("(/ 5 [])", self.env)

    def test_divide_syntax_error_arg_count(self):
        with self.assertRaisesRegex(
            EvaluationError, "SyntaxError: '/' requires at least two arguments."
        ):
            run_lispy_string("(/)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, "SyntaxError: '/' requires at least two arguments."
        ):
            run_lispy_string("(/ 10)", self.env)


if __name__ == "__main__":
    unittest.main()
