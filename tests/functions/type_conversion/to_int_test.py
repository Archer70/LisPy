import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class ToIntFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_to_int_from_int(self):
        self.assertEqual(run_lispy_string("(to-int 42)", self.env), 42)
        self.assertEqual(run_lispy_string("(to-int -7)", self.env), -7)

    def test_to_int_from_float(self):
        self.assertEqual(run_lispy_string("(to-int 3.99)", self.env), 3)
        self.assertEqual(run_lispy_string("(to-int -2.1)", self.env), -2)

    def test_to_int_from_bool(self):
        self.assertEqual(run_lispy_string("(to-int true)", self.env), 1)
        self.assertEqual(run_lispy_string("(to-int false)", self.env), 0)

    def test_to_int_from_string(self):
        self.assertEqual(run_lispy_string('(to-int "42")', self.env), 42)
        self.assertEqual(run_lispy_string('(to-int "3.14")', self.env), 3)
        with self.assertRaises(EvaluationError):
            run_lispy_string('(to-int "notanumber")', self.env)

    def test_to_int_invalid_types(self):
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-int nil)", self.env)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-int [1 2 3])", self.env)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-int {:a 1})", self.env)

    def test_to_int_wrong_arg_count(self):
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-int)", self.env)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-int 1 2)", self.env)


if __name__ == "__main__":
    unittest.main()
