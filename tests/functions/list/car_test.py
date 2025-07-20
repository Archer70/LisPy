# tests/functions/car_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class CarFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()
        run_lispy_string("(define mylist (list 10 20 30))", self.env)
        run_lispy_string("(define nestedlist (list (list 1 2) 3))", self.env)
        run_lispy_string("(define emptylist (list))", self.env)

    def test_car_basic(self):
        self.assertEqual(run_lispy_string("(car mylist)", self.env), 10)
        self.assertEqual(run_lispy_string('(car (list "a" "b"))', self.env), "a")
        self.assertEqual(run_lispy_string("(car nestedlist)", self.env), [1, 2])

    def test_car_on_literal_list(self):
        self.assertEqual(run_lispy_string("(car '(1 2 3))", self.env), 1)
        # Note: (car [1 2 3]) should also work if vectors are treated as lists by car
        # For now, car specifically expects a list, and vectors are distinct type
        # unless we make car more polymorphic or change vector evaluation.
        # According to Requirements.md, vectors are self-evaluating and distinct.
        # Let's assume 'car' works on the list type.

    def test_car_empty_list_error(self):
        with self.assertRaisesRegex(
            EvaluationError, r"RuntimeError: 'car' cannot operate on an empty list."
        ):
            run_lispy_string("(car emptylist)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, r"RuntimeError: 'car' cannot operate on an empty list."
        ):
            run_lispy_string("(car (list))", self.env)
        with self.assertRaisesRegex(
            EvaluationError, r"RuntimeError: 'car' cannot operate on an empty list."
        ):
            run_lispy_string("(car [])", self.env)  # Vector literal, empty

    def test_car_type_error(self):
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: 'car' expects its argument to be a list, got int",
        ):
            run_lispy_string("(car 123)", self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: 'car' expects its argument to be a list, got Symbol",
        ):
            run_lispy_string("(car 'aSymbol)", self.env)
        with self.assertRaisesRegex(
            EvaluationError,
            r"TypeError: 'car' expects its argument to be a list, got NoneType",
        ):
            run_lispy_string("(car nil)", self.env)

    def test_car_argument_count_error(self):
        with self.assertRaisesRegex(
            EvaluationError, r"SyntaxError: 'car' expects 1 argument \(a list\), got 0"
        ):
            run_lispy_string("(car)", self.env)
        with self.assertRaisesRegex(
            EvaluationError, r"SyntaxError: 'car' expects 1 argument \(a list\), got 2"
        ):
            run_lispy_string("(car mylist mylist)", self.env)


if __name__ == "__main__":
    unittest.main()
