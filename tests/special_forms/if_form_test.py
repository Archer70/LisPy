# lispy_project/tests/special_forms/if_form_test.py
import unittest

from lispy.evaluator import evaluate
from lispy.functions import global_env
from lispy.exceptions import EvaluationError
from lispy.types import Symbol
from lispy.environment import Environment

class IfFormTest(unittest.TestCase):

    def setUp(self):
        self.env = Environment(outer=global_env)

    # --- Tests for 'if' special form ---
    def test_if_true_condition(self):
        # (if true 10 20) -> 10
        expr = [Symbol("if"), True, 10, 20]
        self.assertEqual(evaluate(expr, self.env), 10)

    def test_if_false_condition(self):
        # (if false 10 20) -> 20
        expr = [Symbol("if"), False, 10, 20]
        self.assertEqual(evaluate(expr, self.env), 20)

    def test_if_nil_condition_is_falsey(self):
        # (if nil 10 20) -> 20 (nil is falsey)
        expr = [Symbol("if"), None, 10, 20]
        self.assertEqual(evaluate(expr, self.env), 20)

    def test_if_truthy_condition_number(self):
        # (if 0 10 20) -> 10 (0 is truthy)
        expr = [Symbol("if"), 0, 10, 20]
        self.assertEqual(evaluate(expr, self.env), 10)

    def test_if_truthy_condition_string(self):
        # (if "hello" 10 20) -> 10 ("hello" is truthy)
        expr = [Symbol("if"), "hello", 10, 20]
        self.assertEqual(evaluate(expr, self.env), 10)
    
    def test_if_truthy_condition_empty_list(self):
        # (if '() 10 20) -> Previously 10 (empty list is truthy)
        # Now, evaluating '() (which is []) as a condition is an error.
        expr = [Symbol("if"), [], 10, 20]
        with self.assertRaisesRegex(EvaluationError, "Cannot evaluate an empty list as a function call or special form"):
            evaluate(expr, self.env)

    def test_if_false_condition_no_else(self):
        # (if false 10) -> nil (None)
        expr = [Symbol("if"), False, 10]
        self.assertIsNone(evaluate(expr, self.env))

    def test_if_true_condition_no_else(self):
        # (if true 10) -> 10
        expr = [Symbol("if"), True, 10]
        self.assertEqual(evaluate(expr, self.env), 10)

    def test_if_condition_is_expression(self):
        # (if (= 5 5) (+ 1 2) (+ 3 4)) -> 3
        expr = [Symbol("if"), [Symbol("="), 5, 5], [Symbol("+"), 1, 2], [Symbol("+"), 3, 4]]
        self.assertEqual(evaluate(expr, self.env), 3)

    def test_if_only_correct_branch_is_evaluated(self):
        # Define x, then (if true (define x 100) (define x 200)), x should be 100
        self.env.define("x", 1)
        true_branch_defines_x_100 = [Symbol("define"), Symbol("x"), 100]
        false_branch_defines_x_200 = [Symbol("define"), Symbol("x"), 200]
        
        expr_if_true = [Symbol("if"), True, true_branch_defines_x_100, false_branch_defines_x_200]
        evaluate(expr_if_true, self.env)
        self.assertEqual(self.env.lookup("x"), 100, "True branch should have been evaluated")

        # Reset x, then (if false (define x 300) (define x 400)), x should be 400
        self.env.define("x", 1) # Reset x
        false_branch_defines_x_300 = [Symbol("define"), Symbol("x"), 300]
        true_branch_defines_x_400 = [Symbol("define"), Symbol("x"), 400] # Swapped for clarity in this test part
        
        expr_if_false = [Symbol("if"), False, false_branch_defines_x_300, true_branch_defines_x_400]
        evaluate(expr_if_false, self.env)
        self.assertEqual(self.env.lookup("x"), 400, "False branch should have been evaluated")

    def test_if_syntax_errors(self):
        # Too few arguments
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: 'if' requires a condition, a then-expression, and an optional else-expression"):
            evaluate([Symbol("if"), True], self.env)
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: 'if' requires a condition, a then-expression, and an optional else-expression"):
            evaluate([Symbol("if")], self.env)
        # Too many arguments
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: 'if' requires a condition, a then-expression, and an optional else-expression"):
            evaluate([Symbol("if"), True, 1, 2, 3], self.env)

if __name__ == '__main__':
    unittest.main() 