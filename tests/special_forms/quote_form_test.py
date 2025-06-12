# lispy_project/tests/special_forms/quote_form_test.py
import unittest

from lispy.functions import create_global_env
from lispy.exceptions import EvaluationError
from lispy.types import Symbol
from lispy.utils import run_lispy_string


class QuoteFormTest(unittest.TestCase):
    def setUp(self):
        self.env = create_global_env()

    # --- Tests for 'quote' special form ---
    def test_quote_atom_number(self):
        result = run_lispy_string("(quote 123)", self.env)
        self.assertEqual(result, 123)

    def test_quote_atom_string(self):
        result = run_lispy_string('(quote "hello")', self.env)
        self.assertEqual(result, "hello")

    def test_quote_atom_symbol(self):
        # (quote my-symbol) -> my-symbol (the Symbol object itself)
        result = run_lispy_string("(quote my-symbol)", self.env)
        self.assertEqual(result, Symbol("my-symbol"))

    def test_quote_atom_nil(self):
        result = run_lispy_string("(quote nil)", self.env)
        self.assertIsNone(result)

    def test_quote_atom_boolean(self):
        result = run_lispy_string("(quote true)", self.env)
        self.assertTrue(result)
        result_false = run_lispy_string("(quote false)", self.env)
        self.assertFalse(result_false)

    def test_quote_empty_list(self):
        # (quote ()) -> ()
        result = run_lispy_string("(quote ())", self.env)
        self.assertEqual(result, [])

    def test_quote_list_of_atoms(self):
        # (quote (1 "two" three))
        result = run_lispy_string('(quote (1 "two" three))', self.env)
        expected = [1, "two", Symbol("three")]
        self.assertEqual(result, expected)

    def test_quote_list_with_sublist_is_not_evaluated(self):
        # (quote (+ 1 2)) -> (+ 1 2) , not 3
        # The inner list represents the S-expression for addition.
        result = run_lispy_string("(quote (+ 1 2))", self.env)
        expected_quoted_list = [Symbol("+"), 1, 2]
        self.assertEqual(result, expected_quoted_list)

    def test_quote_nested_structure(self):
        # (quote (a (b (quote c)) d))
        # -> (a (b (quote c)) d) where c is Symbol('c')
        result = run_lispy_string("(quote (a (b (quote c)) d))", self.env)
        expected = [
            Symbol("a"),
            [Symbol("b"), [Symbol("quote"), Symbol("c")]],
            Symbol("d"),
        ]
        self.assertEqual(result, expected)

    def test_quote_syntax_errors(self):
        # Too few arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(quote)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'quote' requires exactly one argument. Usage: (quote your-expression)",
        )
        # Too many arguments
        with self.assertRaises(EvaluationError) as cm:
            run_lispy_string("(quote a b)", self.env)
        self.assertEqual(
            str(cm.exception),
            "SyntaxError: 'quote' requires exactly one argument. Usage: (quote your-expression)",
        )


if __name__ == "__main__":
    unittest.main()
