# lispy_project/tests/functions/not_fn_test.py
import unittest

from lispy.functions import global_env, create_global_env
from lispy.utils import run_lispy_string
from lispy.exceptions import EvaluationError


class NotFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = global_env
        # For tests that need to define symbols before `not`
        self.test_specific_env = create_global_env()

    def test_not_falsey_values(self):
        self.assertTrue(run_lispy_string("(not false)", self.env))
        self.assertTrue(
            run_lispy_string("(not nil)", self.env)
        )  # Assuming nil is a defined symbol or None is parsed as nil

    def test_not_truthy_values(self):
        self.assertFalse(run_lispy_string("(not true)", self.env))
        self.assertFalse(run_lispy_string("(not 0)", self.env))  # 0 is truthy
        self.assertFalse(run_lispy_string("(not 1)", self.env))
        self.assertFalse(
            run_lispy_string('(not "")', self.env)
        )  # Empty string is truthy
        self.assertFalse(run_lispy_string('(not "hello")', self.env))
        self.assertFalse(
            run_lispy_string("(not (list))", self.env)
        )  # Empty list is truthy, assuming (list) evals to []
        self.assertFalse(
            run_lispy_string("(not (list 1 2))", self.env)
        )  # Non-empty list is truthy

        # Test with a symbol that is defined
        self.test_specific_env.define("my-truthy-var", 123)
        self.assertFalse(
            run_lispy_string("(not my-truthy-var)", self.test_specific_env)
        )

    def test_not_type_error_arg_count(self):
        with self.assertRaisesRegex(
            EvaluationError, "TypeError: not requires exactly one argument"
        ):
            run_lispy_string("(not)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, "TypeError: not requires exactly one argument"
        ):
            run_lispy_string("(not true false)", self.env)

    def test_not_with_unbound_symbol_is_error_before_not(self):
        # This tests that the argument to 'not' is evaluated first.
        # If 'unbound-sym' is not defined, evaluation of it should fail.
        with self.assertRaisesRegex(EvaluationError, "Unbound symbol: unbound-sym"):
            run_lispy_string("(not unbound-sym)", self.env)


if __name__ == "__main__":
    unittest.main()
