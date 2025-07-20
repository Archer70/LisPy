# lispy_project/tests/functions/add_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class AddFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_add_integers(self):
        self.assertEqual(run_lispy_string("(+ 1 2 3)", self.env), 6)

    def test_add_floats(self):
        self.assertAlmostEqual(run_lispy_string("(+ 1.5 2.5)", self.env), 4.0)

    def test_add_mixed_types(self):
        self.assertAlmostEqual(run_lispy_string("(+ 1 2.5)", self.env), 3.5)

    def test_add_single_argument(self):
        self.assertEqual(run_lispy_string("(+ 5)", self.env), 5)

    def test_add_no_arguments(self):
        # Standard Lisp behavior: (+) should return 0
        self.assertEqual(run_lispy_string("(+)", self.env), 0)

    def test_add_type_error_non_numeric(self):
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 1 to '\+' must be a number, got str: 'a'",
        ):
            run_lispy_string('(+ "a" 5)', self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 2 to '\+' must be a number, got Vector: '\[.*\]'",
        ):
            run_lispy_string("(+ 5 [])", self.env)

    def test_add_empty_call(self):
        # Standard Lisp behavior: (+) should return 0
        self.assertEqual(run_lispy_string("(+)", self.env), 0)


if __name__ == "__main__":
    unittest.main()
