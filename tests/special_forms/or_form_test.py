import unittest

from lispy.evaluator import evaluate
from lispy.functions import create_global_env  # Added
from lispy.lexer import tokenize  # Added
from lispy.parser import parse
from lispy.special_forms.or_form import handle_or_form  # To be created


class TestOrForm(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()  # Use global env

    def _run_lispy(self, code_string):
        tokens = tokenize(code_string)  # Tokenize the input string first
        parsed_expression = parse(tokens)  # Pass tokens to parse
        # Similar to TestAndForm, directly pass the parsed list to the handler.
        return handle_or_form(parsed_expression, self.env, evaluate)

    def test_or_all_false(self):
        self.assertEqual(self._run_lispy("(or false false)"), False)
        self.assertEqual(
            self._run_lispy("(or nil nil nil)"), None
        )  # Returns last value (nil)
        self.assertEqual(self._run_lispy("(or false)"), False)
        self.assertEqual(self._run_lispy("(or nil)"), None)

    def test_or_one_true(self):
        self.assertEqual(self._run_lispy("(or false true)"), True)
        self.assertEqual(self._run_lispy("(or true false)"), True)
        self.assertEqual(self._run_lispy('(or nil "hello" false)'), "hello")
        self.assertEqual(self._run_lispy("(or 0 false)"), 0)  # 0 is truthy

    def test_or_short_circuiting(self):
        # (or true (some_error_if_evaluated)) should return true without error
        self.assertEqual(self._run_lispy("(or true (/ 1 0))"), True)
        self.assertEqual(self._run_lispy('(or "text" (/ 1 0))'), "text")

    def test_or_returns_value_of_first_truthy_expression(self):
        self.assertEqual(self._run_lispy('(or false "yay" true)'), "yay")
        self.assertEqual(self._run_lispy("(or nil 123 true)"), 123)

    def test_or_no_arguments(self):
        # (or) should return false (identity for 'or', or nil based on common Lisp)
        # Let's go with nil as it's a falsy value, consistent with Clojure's (or) -> nil
        self.assertEqual(self._run_lispy("(or)"), None)

    def test_or_with_various_falsy_values(self):
        self.assertEqual(self._run_lispy("(or nil false)"), False)
        self.assertEqual(self._run_lispy("(or false nil)"), None)

    def test_or_with_various_truthy_values(self):
        self.assertEqual(self._run_lispy('(or false 0 "hello")'), 0)
        self.assertEqual(self._run_lispy("(or nil (list 1) false)"), [1])  # List object

    def test_or_evaluation_order_and_return_last_falsy(self):
        # Define a var and use it to ensure evaluation happens
        evaluate(parse(tokenize("(define x nil)")), self.env)  # Tokenize before parsing
        evaluate(
            parse(tokenize("(define y false)")), self.env
        )  # Tokenize before parsing
        self.assertEqual(
            self._run_lispy("(or x y)"), False
        )  # x (nil) then y (false), returns false
        self.assertEqual(
            self._run_lispy("(or y x)"), None
        )  # y (false) then x (nil), returns nil


if __name__ == "__main__":
    unittest.main()
