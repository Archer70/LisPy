# lispy_project/tests/functions/subtract_test.py
import unittest

from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class SubtractFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_subtract_simple(self):
        self.assertEqual(run_lispy_string("(- 10 4)", self.env), 6)

    def test_subtract_multiple_args(self):
        self.assertEqual(run_lispy_string("(- 10 2 3)", self.env), 5)

    def test_subtract_unary_minus(self):
        self.assertEqual(run_lispy_string("(- 7)", self.env), -7)
        self.assertEqual(run_lispy_string("(- -7)", self.env), 7)

    def test_subtract_with_floats(self):
        self.assertEqual(run_lispy_string("(- 10.5 0.5)", self.env), 10.0)
        self.assertAlmostEqual(run_lispy_string("(- 10 0.5)", self.env), 9.5)

    def test_subtract_type_error_non_numeric(self):
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 1 to '-' must be a number, got Vector: '\[.*\]'",
        ):
            run_lispy_string("(- [] 5)", self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 2 to '-' must be a number, got str: 'a'",
        ):
            run_lispy_string('(- 5 "a")', self.env)

    def test_subtract_type_error_no_args(self):
        with self.assertRaisesRegex(
            EvaluationError, "SyntaxError: '-' requires at least one argument"
        ):
            run_lispy_string("(-)", self.env)


if __name__ == "__main__":
    unittest.main()
