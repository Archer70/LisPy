import unittest

from lispy.exceptions import ParseError
from lispy.lexer import (TOKEN_BOOLEAN, TOKEN_LBRACE, TOKEN_LBRACKET,
                         TOKEN_LPAREN, TOKEN_NIL, TOKEN_NUMBER, TOKEN_QUOTE,
                         TOKEN_RBRACE, TOKEN_RBRACKET, TOKEN_RPAREN,
                         TOKEN_STRING, TOKEN_SYMBOL)
from lispy.parser import parse
from lispy.types import Symbol


class ParserTest(unittest.TestCase):
    def test_parse_empty(self):
        with self.assertRaisesRegex(
            ParseError, "Unexpected end of input: No tokens to parse."
        ):
            parse([])

    def test_parse_number_integer(self):
        tokens = [(TOKEN_NUMBER, "123")]
        self.assertEqual(parse(tokens), 123)

    def test_parse_number_float(self):
        tokens = [(TOKEN_NUMBER, "3.14")]
        self.assertEqual(parse(tokens), 3.14)

    def test_parse_string(self):
        tokens = [(TOKEN_STRING, "hello world")]
        self.assertEqual(parse(tokens), "hello world")

    def test_parse_boolean_true(self):
        tokens = [(TOKEN_BOOLEAN, True)]
        self.assertEqual(parse(tokens), True)

    def test_parse_boolean_false(self):
        tokens = [(TOKEN_BOOLEAN, False)]
        self.assertEqual(parse(tokens), False)

    def test_parse_nil(self):
        tokens = [(TOKEN_NIL, None)]
        self.assertEqual(parse(tokens), None)

    def test_parse_symbol(self):
        tokens = [(TOKEN_SYMBOL, "my-symbol")]
        self.assertEqual(parse(tokens), Symbol("my-symbol"))

    def test_parse_too_many_tokens_after_atom(self):
        tokens = [(TOKEN_NUMBER, "123"), (TOKEN_NUMBER, "456")]
        with self.assertRaisesRegex(ParseError, "Unexpected tokens at end of input"):
            parse(tokens)

    def test_parse_empty_list(self):
        tokens = [(TOKEN_LPAREN, "("), (TOKEN_RPAREN, ")")]
        self.assertEqual(parse(tokens), [])

    def test_parse_list_with_atoms(self):
        tokens = [
            (TOKEN_LPAREN, "("),
            (TOKEN_SYMBOL, "+"),
            (TOKEN_NUMBER, "1"),
            (TOKEN_NUMBER, "2"),
            (TOKEN_RPAREN, ")"),
        ]
        self.assertEqual(parse(tokens), [Symbol("+"), 1, 2])

    def test_parse_nested_lists(self):
        tokens = [
            (TOKEN_LPAREN, "("),
            (TOKEN_SYMBOL, "+"),
            (TOKEN_NUMBER, "1"),
            (TOKEN_LPAREN, "("),
            (TOKEN_SYMBOL, "*"),
            (TOKEN_NUMBER, "2"),
            (TOKEN_NUMBER, "3"),
            (TOKEN_RPAREN, ")"),
            (TOKEN_RPAREN, ")"),
        ]
        self.assertEqual(parse(tokens), [Symbol("+"), 1, [Symbol("*"), 2, 3]])

    # --- Tests for Quote Shorthand ---
    def test_parse_quote_shorthand_symbol(self):
        tokens = [(TOKEN_QUOTE, "'"), (TOKEN_SYMBOL, "my-symbol")]
        expected_ast = [Symbol("quote"), Symbol("my-symbol")]
        self.assertEqual(parse(tokens), expected_ast)

    def test_parse_quote_shorthand_number(self):
        tokens = [(TOKEN_QUOTE, "'"), (TOKEN_NUMBER, "123")]
        expected_ast = [Symbol("quote"), 123]
        self.assertEqual(parse(tokens), expected_ast)

    def test_parse_quote_shorthand_list(self):
        tokens = [
            (TOKEN_QUOTE, "'"),
            (TOKEN_LPAREN, "("),
            (TOKEN_SYMBOL, "+"),
            (TOKEN_NUMBER, "1"),
            (TOKEN_NUMBER, "2"),
            (TOKEN_RPAREN, ")"),
        ]
        expected_ast = [Symbol("quote"), [Symbol("+"), 1, 2]]
        self.assertEqual(parse(tokens), expected_ast)

    def test_parse_quote_shorthand_empty_list(self):
        tokens = [(TOKEN_QUOTE, "'"), (TOKEN_LPAREN, "("), (TOKEN_RPAREN, ")")]
        expected_ast = [Symbol("quote"), []]
        self.assertEqual(parse(tokens), expected_ast)

    def test_parse_quote_shorthand_nested(self):
        tokens = [
            (TOKEN_QUOTE, "'"),
            (TOKEN_LPAREN, "("),
            (TOKEN_SYMBOL, "a"),
            (TOKEN_QUOTE, "'"),
            (TOKEN_LPAREN, "("),
            (TOKEN_SYMBOL, "b"),
            (TOKEN_SYMBOL, "c"),
            (TOKEN_RPAREN, ")"),
            (TOKEN_RPAREN, ")"),
        ]
        expected_ast = [
            Symbol("quote"),
            [Symbol("a"), [Symbol("quote"), [Symbol("b"), Symbol("c")]]],
        ]
        self.assertEqual(parse(tokens), expected_ast)

    def test_parse_quote_shorthand_eof_error(self):
        tokens = [(TOKEN_QUOTE, "'")]
        with self.assertRaisesRegex(
            ParseError,
            "SyntaxError: 'quote' shorthand ' must be followed by an expression.",
        ):
            parse(tokens)

    # --- Tests for Vector Literals ---
    def test_parse_empty_vector(self):
        tokens = [(TOKEN_LBRACKET, "["), (TOKEN_RBRACKET, "]")]
        self.assertEqual(parse(tokens), [])

    def test_parse_vector_with_atoms(self):
        tokens = [
            (TOKEN_LBRACKET, "["),
            (TOKEN_NUMBER, "1"),
            (TOKEN_STRING, "two"),
            (TOKEN_BOOLEAN, True),
            (TOKEN_SYMBOL, ":three"),
            (TOKEN_RBRACKET, "]"),
        ]
        self.assertEqual(parse(tokens), [1, "two", True, Symbol(":three")])

    def test_parse_vector_with_nested_list(self):
        tokens = [
            (TOKEN_LBRACKET, "["),
            (TOKEN_NUMBER, "1"),
            (TOKEN_LPAREN, "("),
            (TOKEN_SYMBOL, "+"),
            (TOKEN_NUMBER, "2"),
            (TOKEN_NUMBER, "3"),
            (TOKEN_RPAREN, ")"),
            (TOKEN_NUMBER, "4"),
            (TOKEN_RBRACKET, "]"),
        ]
        self.assertEqual(parse(tokens), [1, [Symbol("+"), 2, 3], 4])

    def test_parse_vector_with_nested_vector(self):
        tokens = [
            (TOKEN_LBRACKET, "["),
            (TOKEN_NUMBER, "1"),
            (TOKEN_LBRACKET, "["),
            (TOKEN_NUMBER, "2"),
            (TOKEN_NUMBER, "3"),
            (TOKEN_RBRACKET, "]"),
            (TOKEN_NUMBER, "4"),
            (TOKEN_RBRACKET, "]"),
        ]
        self.assertEqual(parse(tokens), [1, [2, 3], 4])

    def test_parse_unclosed_vector(self):
        tokens = [(TOKEN_LBRACKET, "["), (TOKEN_NUMBER, "1"), (TOKEN_NUMBER, "2")]
        with self.assertRaisesRegex(
            ParseError, "Unexpected end of input: missing ']' while parsing vector"
        ):
            parse(tokens)

    def test_parse_vector_unexpected_token(self):
        tokens = [
            (TOKEN_LBRACKET, "["),
            (TOKEN_NUMBER, "1"),
            (TOKEN_RPAREN, ")"),
            (TOKEN_NUMBER, "2"),
            (TOKEN_RBRACKET, "]"),
        ]
        with self.assertRaisesRegex(
            ParseError, "Unexpected token type during parsing: RPAREN"
        ):
            parse(tokens)

    # --- Tests for Map Literals ---
    def test_parse_empty_map(self):
        tokens = [(TOKEN_LBRACE, "{"), (TOKEN_RBRACE, "}")]
        self.assertEqual(parse(tokens), {})

    def test_parse_map_with_symbol_keys_atom_values(self):
        tokens = [
            (TOKEN_LBRACE, "{"),
            (TOKEN_SYMBOL, ":a"),
            (TOKEN_NUMBER, "1"),
            (TOKEN_SYMBOL, ":b"),
            (TOKEN_STRING, "two"),
            (TOKEN_SYMBOL, ":c"),
            (TOKEN_BOOLEAN, True),
            (TOKEN_RBRACE, "}"),
        ]
        expected_map = {Symbol(":a"): 1, Symbol(":b"): "two", Symbol(":c"): True}
        self.assertEqual(parse(tokens), expected_map)

    def test_parse_map_with_nested_values(self):
        tokens = [
            (TOKEN_LBRACE, "{"),
            (TOKEN_SYMBOL, ":l"),
            (TOKEN_LPAREN, "("),
            (TOKEN_NUMBER, "1"),
            (TOKEN_NUMBER, "2"),
            (TOKEN_RPAREN, ")"),
            (TOKEN_SYMBOL, ":v"),
            (TOKEN_LBRACKET, "["),
            (TOKEN_STRING, "x"),
            (TOKEN_BOOLEAN, False),
            (TOKEN_RBRACKET, "]"),
            (TOKEN_RBRACE, "}"),
        ]
        expected_map = {Symbol(":l"): [1, 2], Symbol(":v"): ["x", False]}
        self.assertEqual(parse(tokens), expected_map)

    def test_parse_unclosed_map(self):
        tokens = [(TOKEN_LBRACE, "{"), (TOKEN_SYMBOL, ":a"), (TOKEN_NUMBER, "1")]
        with self.assertRaisesRegex(
            ParseError, "Unexpected end of input: missing '}' while parsing map"
        ):
            parse(tokens)

    def test_parse_map_odd_number_of_forms(self):
        tokens = [
            (TOKEN_LBRACE, "{"),
            (TOKEN_SYMBOL, ":a"),
            (TOKEN_NUMBER, "1"),
            (TOKEN_SYMBOL, ":b"),
            (TOKEN_RBRACE, "}"),
        ]
        with self.assertRaisesRegex(
            ParseError,
            "Map literals require an even number of forms \\(key-value pairs\\), missing value for key: :b",
        ):
            parse(tokens)

    def test_parse_map_odd_number_of_forms_eof(self):
        tokens = [
            (TOKEN_LBRACE, "{"),
            (TOKEN_SYMBOL, ":a"),
            (TOKEN_NUMBER, "1"),
            (TOKEN_SYMBOL, ":b"),
        ]
        with self.assertRaisesRegex(
            ParseError,
            "Unexpected end of input: map literal requires a value for key: :b",
        ):
            parse(tokens)

    def test_parse_map_number_key(self):
        tokens = [
            (TOKEN_LBRACE, "{"),
            (TOKEN_NUMBER, "123"),
            (TOKEN_STRING, "value"),
            (TOKEN_RBRACE, "}"),
        ]
        ast = parse(tokens)
        expected = {123: "value"}
        self.assertEqual(ast, expected)

    def test_parse_map_string_key(self):
        tokens = [
            (TOKEN_LBRACE, "{"),
            (TOKEN_STRING, "key"),
            (TOKEN_STRING, "value"),
            (TOKEN_RBRACE, "}"),
        ]
        ast = parse(tokens)
        expected = {"key": "value"}
        self.assertEqual(ast, expected)

    def test_parse_map_boolean_key(self):
        tokens = [
            (TOKEN_LBRACE, "{"),
            (TOKEN_BOOLEAN, True),
            (TOKEN_STRING, "value"),
            (TOKEN_RBRACE, "}"),
        ]
        ast = parse(tokens)
        expected = {True: "value"}
        self.assertEqual(ast, expected)

    def test_parse_map_invalid_key_type(self):
        # Test that unsupported key types (like LPAREN) still raise errors
        tokens = [
            (TOKEN_LBRACE, "{"),
            (TOKEN_LPAREN, "("),
            (TOKEN_STRING, "value"),
            (TOKEN_RBRACE, "}"),
        ]
        with self.assertRaisesRegex(
            ParseError,
            "Map key must be a symbol, string, number, boolean, or nil, got LPAREN",
        ):
            parse(tokens)

    # --- Tests for Mismatched Delimiters and Unexpected Tokens ---
    def test_parse_extra_rparen_after_list(self):
        tokens = [(TOKEN_LPAREN, "("), (TOKEN_RPAREN, ")"), (TOKEN_RPAREN, ")")]
        with self.assertRaisesRegex(
            ParseError, r"Unexpected tokens at end of input.*RPAREN"
        ):
            parse(tokens)

    def test_parse_extra_rbracket_after_vector(self):
        tokens = [(TOKEN_LBRACKET, "["), (TOKEN_RBRACKET, "]"), (TOKEN_RBRACKET, "]")]
        expected_msg = "Unexpected tokens at end of input: [('RBRACKET', ']')]"
        with self.assertRaises(ParseError) as cm:
            parse(tokens)
        self.assertEqual(str(cm.exception), expected_msg)

    def test_parse_extra_rbrace_after_map(self):
        tokens = [(TOKEN_LBRACE, "{"), (TOKEN_RBRACE, "}"), (TOKEN_RBRACE, "}")]
        with self.assertRaisesRegex(
            ParseError, r"Unexpected tokens at end of input.*RBRACE"
        ):
            parse(tokens)

    def test_parse_unclosed_inner_list(self):
        tokens = [(TOKEN_LPAREN, "("), (TOKEN_LPAREN, "("), (TOKEN_RPAREN, ")")]
        with self.assertRaisesRegex(
            ParseError, r"Unexpected end of input.*missing.*while parsing list"
        ):
            parse(tokens)

    def test_parse_unexpected_rparen_at_start(self):
        tokens = [(TOKEN_RPAREN, ")")]
        with self.assertRaisesRegex(
            ParseError, "Unexpected token type during parsing: RPAREN \\(\\'\\)\\'\\)"
        ):
            parse(tokens)

    def test_parse_unexpected_rbracket_at_start(self):
        tokens = [(TOKEN_RBRACKET, "]")]
        with self.assertRaisesRegex(
            ParseError, "Unexpected token type during parsing: RBRACKET \\(\\'\\]\\'\\)"
        ):
            parse(tokens)

    def test_parse_unexpected_rbrace_at_start(self):
        tokens = [(TOKEN_RBRACE, "}")]
        with self.assertRaisesRegex(
            ParseError, r"Unexpected token type during parsing: RBRACE \('.*'\)"
        ):
            parse(tokens)

    # --- Integration Tests for Comma Support ---
    def test_parse_vector_with_commas_integration(self):
        """Integration test: lexer + parser with comma-separated vectors."""
        from lispy.lexer import tokenize

        source_code = "[1, 2, 3]"
        tokens = tokenize(source_code)
        result = parse(tokens)
        self.assertEqual(result, [1, 2, 3])

    def test_parse_map_with_commas_integration(self):
        """Integration test: lexer + parser with comma-separated maps."""
        from lispy.lexer import tokenize

        source_code = "{:a 1, :b 2}"
        tokens = tokenize(source_code)
        result = parse(tokens)
        expected_map = {Symbol(":a"): 1, Symbol(":b"): 2}
        self.assertEqual(result, expected_map)

    def test_parse_nested_structures_with_commas_integration(self):
        """Integration test: lexer + parser with comma-separated nested structures."""
        from lispy.lexer import tokenize

        source_code = "{:data [1, 2, 3], :nested {:x 10, :y 20}}"
        tokens = tokenize(source_code)
        result = parse(tokens)
        expected_map = {
            Symbol(":data"): [1, 2, 3],
            Symbol(":nested"): {Symbol(":x"): 10, Symbol(":y"): 20},
        }
        self.assertEqual(result, expected_map)


if __name__ == "__main__":
    unittest.main()
