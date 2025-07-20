# lispy_project/tests/functions/equals_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class EqualsFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_equals_numbers_true(self):
        self.assertTrue(run_lispy_string("(= 5 5)", self.env))
        self.assertTrue(run_lispy_string("(= 5.0 5)", self.env))

    def test_equals_multiple_numbers_true(self):
        self.assertTrue(run_lispy_string("(= 10 10 10 10)", self.env))

    def test_equals_numbers_false(self):
        self.assertFalse(run_lispy_string("(= 5 6)", self.env))
        self.assertFalse(run_lispy_string("(= 5.0 6)", self.env))

    def test_equals_multiple_numbers_false(self):
        self.assertFalse(run_lispy_string("(= 10 10 6 10)", self.env))

    def test_equals_syntax_error_arg_count(self):
        with self.assertRaisesRegex(
            EvaluationError, "SyntaxError: '=' requires at least two arguments."
        ):
            run_lispy_string("(=)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, "SyntaxError: '=' requires at least two arguments."
        ):
            run_lispy_string("(= 5)", self.env)

    def test_equals_type_error_non_numeric(self):
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 1 to '=' must be a number for comparison, got str: 'a'",
        ):
            run_lispy_string('(= "a" 5)', self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 2 to '=' must be a number for comparison, got Vector: '\[.*\]'",
        ):
            run_lispy_string("(= 5 [])", self.env)


if __name__ == "__main__":
    unittest.main()
