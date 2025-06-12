# lispy_project/tests/functions/less_than_or_equal_test.py
import unittest

from lispy.functions import global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError


class LessThanOrEqualFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = global_env

    def test_less_than_or_equal_true(self):
        self.assertTrue(run_lispy_string("(<= 5 6)", self.env))
        self.assertTrue(run_lispy_string("(<= 5 5)", self.env))
        self.assertTrue(run_lispy_string("(<= -1 0)", self.env))
        self.assertTrue(run_lispy_string("(<= 5 5.0)", self.env))
        self.assertTrue(run_lispy_string("(<= 5.0 5)", self.env))
        self.assertTrue(run_lispy_string("(<= 5 5.1)", self.env))

    def test_less_than_or_equal_false(self):
        self.assertFalse(run_lispy_string("(<= 6 5)", self.env))
        self.assertFalse(run_lispy_string("(<= 0 -1)", self.env))
        self.assertFalse(run_lispy_string("(<= 5.1 5)", self.env))

    def test_less_than_or_equal_type_error_arg_count(self):
        with self.assertRaisesRegex(
            EvaluationError, "TypeError: <= requires exactly two arguments"
        ):
            run_lispy_string("(<= 1)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, "TypeError: <= requires exactly two arguments"
        ):
            run_lispy_string("(<=)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, "TypeError: <= requires exactly two arguments"
        ):
            run_lispy_string("(<= 1 2 3)", self.env)

    def test_less_than_or_equal_type_error_non_numeric(self):
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 1 to '<=' must be a number, got str: 'a'",
        ):
            run_lispy_string('(<= "a" 5)', self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: Argument 2 to '<=' must be a number, got Vector: '\[.*\]'",
        ):
            run_lispy_string("(<= 5 [])", self.env)


if __name__ == "__main__":
    unittest.main()
