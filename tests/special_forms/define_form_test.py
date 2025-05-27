# lispy_project/tests/special_forms/define_form_test.py
import unittest

from lispy.evaluator import evaluate
from lispy.functions import global_env
from lispy.exceptions import EvaluationError
from lispy.types import Symbol
from lispy.environment import Environment

class DefineFormTest(unittest.TestCase):

    def setUp(self):
        self.env = Environment(outer=global_env)
        self.empty_env = Environment()

    # --- Tests for 'define' special form ---
    def test_define_simple_value(self):
        # (define x 10)
        expr = [Symbol("define"), Symbol("x"), 10]
        result = evaluate(expr, self.env)
        self.assertEqual(result, 10) # define returns the value
        self.assertEqual(self.env.lookup("x"), 10)

    def test_define_expression_value(self):
        # (define y (+ 5 5))
        expr = [Symbol("define"), Symbol("y"), [Symbol("+"), 5, 5]]
        result = evaluate(expr, self.env)
        self.assertEqual(result, 10)
        self.assertEqual(self.env.lookup("y"), 10)

    def test_define_redefinition(self):
        # (define z 1)
        evaluate([Symbol("define"), Symbol("z"), 1], self.env)
        self.assertEqual(self.env.lookup("z"), 1)
        # (define z (+ 10 10))
        expr_redefine = [Symbol("define"), Symbol("z"), [Symbol("+"), 10, 10]]
        result = evaluate(expr_redefine, self.env)
        self.assertEqual(result, 20)
        self.assertEqual(self.env.lookup("z"), 20)

    def test_define_incorrect_args_count_too_few(self):
        # (define x)
        expr = [Symbol("define"), Symbol("x")]
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: 'define' requires a symbol and a value"):
            evaluate(expr, self.env)
    
    def test_define_incorrect_args_count_too_many(self):
        # (define x 10 20)
        expr = [Symbol("define"), Symbol("x"), 10, 20]
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: 'define' requires a symbol and a value"):
            evaluate(expr, self.env)

    def test_define_first_arg_not_symbol(self):
        # (define "not-a-symbol" 10)
        expr = [Symbol("define"), "not-a-symbol", 10]
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: First argument to 'define' must be a symbol, got str"):
            evaluate(expr, self.env)

    def test_define_in_empty_env(self):
        # (define new_var "hello_empty")
        expr = [Symbol("define"), Symbol("new_var"), "hello_empty"]
        result = evaluate(expr, self.empty_env)
        self.assertEqual(result, "hello_empty")
        self.assertEqual(self.empty_env.lookup("new_var"), "hello_empty")

if __name__ == '__main__':
    unittest.main() 