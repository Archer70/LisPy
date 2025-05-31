import unittest

from lispy.special_forms.and_form import handle_and_form
from lispy.lexer import tokenize
from lispy.parser import parse
from lispy.evaluator import evaluate
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions import create_global_env

class TestAndForm(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    def _run_lispy(self, code_string):
        tokens = tokenize(code_string)
        parsed_expression = parse(tokens)
        # The top-level parsed expression for a special form like (and ...)
        # will be a list, e.g., [Symbol('and'), True, False].
        # We need to pass this list directly to handle_and_form.
        # evaluate() would normally do this decomposition.
        # Here, we simulate that for direct testing of the handler.
        # The first element of the parsed list is the operator, the rest are args.
        # handle_and_form expects expression = [Symbol('and'), arg1, arg2, ...]
        return handle_and_form(parsed_expression, self.env, evaluate)

    def test_and_all_true(self):
        self.assertEqual(self._run_lispy("(and true true)"), True)
        self.assertEqual(self._run_lispy("(and 1 2 3)"), 3) # Returns last value
        self.assertEqual(self._run_lispy("(and true)"), True)
        self.assertEqual(self._run_lispy("(and \"hello\")"), "hello")

    def test_and_one_false(self):
        self.assertEqual(self._run_lispy("(and true false)"), False)
        self.assertEqual(self._run_lispy("(and false true)"), False)
        self.assertEqual(self._run_lispy("(and 1 2 false 4)"), False)
        self.assertEqual(self._run_lispy("(and nil true)"), None) # nil is falsy

    def test_and_short_circuiting(self):
        # (and false (some_error_if_evaluated)) should return false without error
        self.assertEqual(self._run_lispy("(and false (/ 1 0))"), False) 
        # Check with nil
        self.assertEqual(self._run_lispy("(and nil (/ 1 0))"), None)

    def test_and_returns_value_of_first_falsy_expression(self):
        self.assertEqual(self._run_lispy("(and true false \"stop\")"), False)
        self.assertEqual(self._run_lispy("(and true nil \"stop\")"), None)
        self.assertEqual(self._run_lispy("(and 0 1 2)"), 2) # 0 is truthy in LisPy

    def test_and_no_arguments(self):
        # (and) should return true (identity for 'and')
        self.assertEqual(self._run_lispy("(and)"), True)

    def test_and_with_various_truthy_values(self):
        self.assertEqual(self._run_lispy('(and 0 "s" (list 1) (vector 2))'), [2]) # Returns last vector object
        self.assertEqual(self._run_lispy('(and (fn (x) (+ x 1)) 1)'), 1) # Function object is truthy

    def test_and_with_various_falsy_values(self):
        self.assertEqual(self._run_lispy("(and true nil false)"), None) # nil encountered first
        self.assertEqual(self._run_lispy("(and true false nil)"), False) # false encountered first

    def test_and_evaluation_order_and_return_last_truthy(self):
        # Define a var and use it to ensure evaluation happens
        evaluate(parse(tokenize("(define x 10)")), self.env)
        self.assertEqual(self._run_lispy("(and true x)"), 10)
        self.assertEqual(self._run_lispy("(and x true)"), True)


if __name__ == '__main__':
    unittest.main() 