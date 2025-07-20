import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class ToBoolFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_to_bool_from_bool(self):
        self.assertTrue(run_lispy_string("(to-bool true)", self.env))
        self.assertFalse(run_lispy_string("(to-bool false)", self.env))

    def test_to_bool_from_int(self):
        self.assertTrue(run_lispy_string("(to-bool 1)", self.env))
        self.assertFalse(run_lispy_string("(to-bool 0)", self.env))
        self.assertTrue(run_lispy_string("(to-bool -1)", self.env))

    def test_to_bool_from_float(self):
        self.assertTrue(run_lispy_string("(to-bool 3.14)", self.env))
        self.assertFalse(run_lispy_string("(to-bool 0.0)", self.env))
        self.assertTrue(run_lispy_string("(to-bool -2.5)", self.env))

    def test_to_bool_from_string(self):
        self.assertTrue(run_lispy_string('(to-bool "true")', self.env))
        self.assertFalse(run_lispy_string('(to-bool "false")', self.env))
        self.assertFalse(run_lispy_string('(to-bool "")', self.env))
        with self.assertRaises(EvaluationError):
            run_lispy_string('(to-bool "notabool")', self.env)

    def test_to_bool_from_nil(self):
        self.assertFalse(run_lispy_string("(to-bool nil)", self.env))

    def test_to_bool_from_collections(self):
        self.assertTrue(run_lispy_string("(to-bool [1 2 3])", self.env))
        self.assertFalse(run_lispy_string("(to-bool [])", self.env))
        self.assertTrue(run_lispy_string("(to-bool {:a 1})", self.env))
        self.assertFalse(run_lispy_string("(to-bool {})", self.env))

    def test_to_bool_wrong_arg_count(self):
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-bool)", self.env)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-bool 1 2)", self.env)


if __name__ == "__main__":
    unittest.main()
