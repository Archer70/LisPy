import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class ToFloatFunctionTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_to_float_from_float(self):
        self.assertEqual(run_lispy_string("(to-float 3.14)", self.env), 3.14)
        self.assertEqual(run_lispy_string("(to-float -2.5)", self.env), -2.5)

    def test_to_float_from_int(self):
        self.assertEqual(run_lispy_string("(to-float 42)", self.env), 42.0)
        self.assertEqual(run_lispy_string("(to-float -7)", self.env), -7.0)

    def test_to_float_from_bool(self):
        self.assertEqual(run_lispy_string("(to-float true)", self.env), 1.0)
        self.assertEqual(run_lispy_string("(to-float false)", self.env), 0.0)

    def test_to_float_from_string(self):
        self.assertEqual(run_lispy_string('(to-float "42")', self.env), 42.0)
        self.assertEqual(run_lispy_string('(to-float "3.14")', self.env), 3.14)
        with self.assertRaises(EvaluationError):
            run_lispy_string('(to-float "notanumber")', self.env)

    def test_to_float_invalid_types(self):
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-float nil)", self.env)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-float [1 2 3])", self.env)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-float {:a 1})", self.env)

    def test_to_float_wrong_arg_count(self):
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-float)", self.env)
        with self.assertRaises(EvaluationError):
            run_lispy_string("(to-float 1 2)", self.env)


if __name__ == "__main__":
    unittest.main()
