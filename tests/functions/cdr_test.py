# tests/functions/cdr_test.py
import unittest
from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError


class CdrFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        run_lispy_string("(define mylist (list 10 20 30))", self.env)
        run_lispy_string("(define singlelist (list 10))", self.env)
        run_lispy_string("(define emptylist (list))", self.env)

    def test_cdr_basic(self):
        self.assertEqual(run_lispy_string("(cdr mylist)", self.env), [20, 30])
        self.assertEqual(
            run_lispy_string('(cdr (list "a" "b" "c"))', self.env), ["b", "c"]
        )

    def test_cdr_on_single_element_list(self):
        self.assertEqual(run_lispy_string("(cdr singlelist)", self.env), [])
        self.assertEqual(run_lispy_string("(cdr (list 1))", self.env), [])

    def test_cdr_on_literal_list(self):
        self.assertEqual(run_lispy_string("(cdr '(1 2 3))", self.env), [2, 3])
        # Similar to car, cdr is assumed to work on the list type.

    def test_cdr_empty_list_error(self):
        with self.assertRaisesRegex(
            EvaluationError, r"RuntimeError: 'cdr' cannot operate on an empty list."
        ):
            run_lispy_string("(cdr emptylist)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, r"RuntimeError: 'cdr' cannot operate on an empty list."
        ):
            run_lispy_string("(cdr (list))", self.env)
        with self.assertRaisesRegex(
            EvaluationError, r"RuntimeError: 'cdr' cannot operate on an empty list."
        ):
            run_lispy_string("(cdr [])", self.env)  # Vector literal, empty

    def test_cdr_type_error(self):
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: 'cdr' expects its argument to be a list, got int",
        ):
            run_lispy_string("(cdr 123)", self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: 'cdr' expects its argument to be a list, got Symbol",
        ):
            run_lispy_string("(cdr 'aSymbol)", self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: 'cdr' expects its argument to be a list, got NoneType",
        ):
            run_lispy_string("(cdr nil)", self.env)

    def test_cdr_argument_count_error(self):
        with self.assertRaisesRegex(
            EvaluationError, r"SyntaxError: 'cdr' expects 1 argument \(a list\), got 0"
        ):
            run_lispy_string("(cdr)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, r"SyntaxError: 'cdr' expects 1 argument \(a list\), got 2"
        ):
            run_lispy_string("(cdr mylist mylist)", self.env)


if __name__ == "__main__":
    unittest.main()
