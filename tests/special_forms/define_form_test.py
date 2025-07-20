# lispy_project/tests/special_forms/define_form_test.py
import unittest

from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env
from lispy.utils import run_lispy_string


class DefineFormTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    # --- Tests for 'define' special form ---
    def test_define_simple_value(self):
        # (define x 10)
        result = run_lispy_string("(define x 10)", self.env)
        self.assertEqual(result, 10)  # define returns the value
        self.assertEqual(self.env.lookup("x"), 10)

    def test_define_expression_value(self):
        # (define y (+ 5 5))
        result = run_lispy_string("(define y (+ 5 5))", self.env)
        self.assertEqual(result, 10)
        self.assertEqual(self.env.lookup("y"), 10)

    def test_define_redefinition(self):
        # (define z 1)
        run_lispy_string("(define z 1)", self.env)
        self.assertEqual(self.env.lookup("z"), 1)
        # (define z (+ 10 10))
        result = run_lispy_string("(define z (+ 10 10))", self.env)
        self.assertEqual(result, 20)
        self.assertEqual(self.env.lookup("z"), 20)

    def test_define_incorrect_args_count_too_few(self):
        # (define x)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(define x)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'define' requires a symbol and a value. Usage: (define symbol value)",
        )

    def test_define_incorrect_args_count_too_many(self):
        # (define x 10 20)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(define x 10 20)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'define' requires a symbol and a value. Usage: (define symbol value)",
        )

    def test_define_first_arg_not_symbol(self):
        # (define "not-a-symbol" 10)
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string('(define "not-a-symbol" 10)', self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: First argument to 'define' must be a symbol, got str",
        )

    def test_define_in_empty_env(self):
        # (define new_var "hello_empty")
        empty_env = create_global_env()
        result = run_lispy_string('(define new_var "hello_empty")', empty_env)
        self.assertEqual(result, "hello_empty")
        self.assertEqual(empty_env.lookup("new_var"), "hello_empty")


if __name__ == "__main__":
    unittest.main()
