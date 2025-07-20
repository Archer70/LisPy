# tests/functions/count_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class CountFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()  # This env will need 'count' to be defined

    def test_count_list(self):
        self.assertEqual(run_lispy_string("(count (list 1 2 3))", self.env), 3)
        self.assertEqual(run_lispy_string("(count (list))", self.env), 0)

    def test_count_vector(self):
        self.assertEqual(run_lispy_string("(count [1 2 3])", self.env), 3)
        self.assertEqual(run_lispy_string("(count [])", self.env), 0)

    def test_count_map(self):
        self.assertEqual(run_lispy_string("(count {:a 1 :b 2})", self.env), 2)
        self.assertEqual(run_lispy_string("(count {})", self.env), 0)

    def test_count_string(self):
        self.assertEqual(run_lispy_string('(count "hello")', self.env), 5)
        self.assertEqual(run_lispy_string('(count "")', self.env), 0)

    def test_count_nil(self):
        self.assertEqual(run_lispy_string("(count nil)", self.env), 0)

    def test_count_arg_count_error_none(self):
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(count)", self.env)
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'count' expects 1 argument, got 0."
        )

    def test_count_arg_count_error_many(self):
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(count [] "")', self.env)  # Vector and string as two args
        self.assertEqual(
            str(cm.exception), "SyntaxError: 'count' expects 1 argument, got 2."
        )

    def test_count_type_error_number(self):
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(count 123)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'count' expects a list, vector, map, string, or nil. Got int",
        )

    def test_count_type_error_boolean(self):
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(count true)", self.env)
        self.assertEqual(
            str(cm.exception),
            "TypeError: 'count' expects a list, vector, map, string, or nil. Got bool",
        )


if __name__ == "__main__":
    unittest.main()
