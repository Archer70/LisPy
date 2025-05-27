# tests/functions/cons_test.py
import unittest
from lispy.utils import run_lispy_string
from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.types import Symbol

class ConsFnTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def test_cons_basic(self):
        self.assertEqual(run_lispy_string("(cons 1 (list 2 3))", self.env), [1, 2, 3])
        self.assertEqual(run_lispy_string("(cons (list 1 2) (list 3 4))", self.env), [[1, 2], 3, 4])

    def test_cons_to_empty_list(self):
        self.assertEqual(run_lispy_string("(cons 1 (list))", self.env), [1])
        self.assertEqual(run_lispy_string("(cons 1 [])", self.env), [1]) # Vector literal should also work if it evaluates to list

    def test_cons_symbols(self):
        run_lispy_string("(define a 1)", self.env)
        run_lispy_string("(define b (list 2 3))", self.env)
        self.assertEqual(run_lispy_string("(cons a b)", self.env), [1, 2, 3])

    def test_cons_type_error_second_arg(self):
        with self.assertRaisesRegex(EvaluationError, r"TypeError: 'cons' expects its second argument to be a list, got int"):
            run_lispy_string("(cons 1 2)", self.env)
        with self.assertRaisesRegex(EvaluationError, r"TypeError: 'cons' expects its second argument to be a list, got Symbol"):
            run_lispy_string("(cons 1 'a)", self.env)
        with self.assertRaisesRegex(EvaluationError, r"TypeError: 'cons' expects its second argument to be a list, got NoneType"):
            run_lispy_string("(cons 1 nil)", self.env)

    def test_cons_argument_count_error(self):
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: 'cons' expects 2 arguments \(item list\), got 1"):
            run_lispy_string("(cons 1)", self.env)
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: 'cons' expects 2 arguments \(item list\), got 3"):
            run_lispy_string("(cons 1 (list 2) 3)", self.env)
        with self.assertRaisesRegex(EvaluationError, r"SyntaxError: 'cons' expects 2 arguments \(item list\), got 0"):
            run_lispy_string("(cons)", self.env)

if __name__ == '__main__':
    unittest.main() 