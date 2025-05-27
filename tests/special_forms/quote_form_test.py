# lispy_project/tests/special_forms/quote_form_test.py
import unittest

from lispy.evaluator import evaluate
from lispy.functions import global_env
from lispy.exceptions import EvaluationError
from lispy.types import Symbol
from lispy.environment import Environment

class QuoteFormTest(unittest.TestCase):

    def setUp(self):
        self.env = Environment(outer=global_env)

    # --- Tests for 'quote' special form ---
    def test_quote_atom_number(self):
        expr = [Symbol("quote"), 123]
        self.assertEqual(evaluate(expr, self.env), 123)

    def test_quote_atom_string(self):
        expr = [Symbol("quote"), "hello"]
        self.assertEqual(evaluate(expr, self.env), "hello")

    def test_quote_atom_symbol(self):
        # (quote my-symbol) -> my-symbol (the Symbol object itself)
        expr = [Symbol("quote"), Symbol("my-symbol")]
        self.assertEqual(evaluate(expr, self.env), Symbol("my-symbol"))

    def test_quote_atom_nil(self):
        expr = [Symbol("quote"), None]
        self.assertIsNone(evaluate(expr, self.env))

    def test_quote_atom_boolean(self):
        expr = [Symbol("quote"), True]
        self.assertTrue(evaluate(expr, self.env))
        expr_false = [Symbol("quote"), False]
        self.assertFalse(evaluate(expr_false, self.env))

    def test_quote_empty_list(self):
        # (quote ()) -> ()
        expr = [Symbol("quote"), []]
        self.assertEqual(evaluate(expr, self.env), [])

    def test_quote_list_of_atoms(self):
        # (quote (1 "two" three))
        inner_list = [1, "two", Symbol("three")]
        expr = [Symbol("quote"), inner_list]
        self.assertEqual(evaluate(expr, self.env), inner_list)

    def test_quote_list_with_sublist_is_not_evaluated(self):
        # (quote (+ 1 2)) -> (+ 1 2) , not 3
        # The inner list represents the S-expression for addition.
        list_to_quote = [Symbol("+"), 1, 2]
        expr = [Symbol("quote"), list_to_quote]
        expected_quoted_list = [Symbol("+"), 1, 2]
        self.assertEqual(evaluate(expr, self.env), expected_quoted_list)

    def test_quote_nested_structure(self):
        # (quote (a (b (quote c)) d))
        # -> (a (b (quote c)) d) where c is Symbol('c')
        structure = [
            Symbol("a"), 
            [Symbol("b"), [Symbol("quote"), Symbol("c")]],
            Symbol("d")
        ]
        expr = [Symbol("quote"), structure]
        self.assertEqual(evaluate(expr, self.env), structure)

    def test_quote_syntax_errors(self):
        # Too few arguments
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: 'quote' requires exactly one argument"):
            evaluate([Symbol("quote")], self.env)
        # Too many arguments
        with self.assertRaisesRegex(EvaluationError, "SyntaxError: 'quote' requires exactly one argument"):
            evaluate([Symbol("quote"), Symbol("a"), Symbol("b")], self.env)

if __name__ == '__main__':
    unittest.main() 