# lispy_project/tests/functions/multiply_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class MultiplyFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_multiply_simple(self):
        self.assertEqual(run_lispy_string("(* 2 3)", self.env), 6)

    def test_multiply_multiple_args(self):
        self.assertEqual(run_lispy_string("(* 2 3 4)", self.env), 24)

    def test_multiply_with_zero(self):
        self.assertEqual(run_lispy_string("(* 5 0)", self.env), 0)
        self.assertEqual(run_lispy_string("(* 5 1 0 10)", self.env), 0)

    def test_multiply_with_one(self):
        self.assertEqual(run_lispy_string("(* 5 1)", self.env), 5)

    def test_multiply_no_args(self):
        self.assertEqual(
            run_lispy_string("(*)", self.env), 1
        )  # Identity for multiplication

    def test_multiply_one_arg(self):
        self.assertEqual(run_lispy_string("(* 7)", self.env), 7)

    def test_multiply_with_floats(self):
        self.assertEqual(run_lispy_string("(* 5 0.5)", self.env), 2.5)
        self.assertAlmostEqual(run_lispy_string("(* 2.5 2.0 1.5)", self.env), 7.5)

    def test_multiply_type_error_non_numeric(self):
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 1 to '\*' must be a number, got str: 'a'",
        ):
            run_lispy_string('(* "a" 5)', self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 2 to '\*' must be a number, got Vector: '\[.*\]'",
        ):
            run_lispy_string("(* 5 [])", self.env)

    def test_multiply_empty_call(self):
        self.assertEqual(
            run_lispy_string("(*)", self.env), 1
        )  # Identity for multiplication


if __name__ == "__main__":
    unittest.main()
