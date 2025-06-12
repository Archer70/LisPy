import unittest
from lispy.lexer import (
    tokenize,
    TOKEN_NUMBER,
    TOKEN_STRING,
    TOKEN_BOOLEAN,
    TOKEN_NIL,
    TOKEN_SYMBOL,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LBRACKET,
    TOKEN_RBRACKET,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_QUOTE,
)
from lispy.exceptions import LexerError


# Changed class name to follow Python conventions (PascalCase)
class LexerTest(unittest.TestCase):
    def test_empty_source(self):
        self.assertEqual(tokenize(""), [])

    def test_numbers(self):
        self.assertEqual(tokenize("123"), [(TOKEN_NUMBER, "123")])
        self.assertEqual(tokenize("-456"), [(TOKEN_NUMBER, "-456")])
        self.assertEqual(tokenize("3.14"), [(TOKEN_NUMBER, "3.14")])
        self.assertEqual(tokenize("-0.5"), [(TOKEN_NUMBER, "-0.5")])
        # If we support leading +
        self.assertEqual(tokenize("+7"), [(TOKEN_NUMBER, "+7")])

    def test_strings_simple(self):
        # Value without quotes
        self.assertEqual(tokenize('"hello"'), [(TOKEN_STRING, "hello")])
        self.assertEqual(tokenize('""'), [(TOKEN_STRING, "")])  # Empty string

    def test_strings_with_escapes(self):
        self.assertEqual(tokenize('"hello\\nworld"'), [(TOKEN_STRING, "hello\nworld")])
        self.assertEqual(tokenize('"\\"quote\\""'), [(TOKEN_STRING, '"quote"')])
        self.assertEqual(tokenize('"a\\\\b"'), [(TOKEN_STRING, "a\\b")])

    def test_strings_with_invalid_escapes(self):
        with self.assertRaisesRegex(LexerError, "Invalid escape sequence: \\\\z"):
            tokenize('"hello\\zworld"')
        with self.assertRaisesRegex(LexerError, "Invalid escape sequence: \\\\a"):
            tokenize('"\\a"')
        # Check that valid escapes still work around invalid ones if parsing continued (it shouldn't)
        # but more importantly, that the error is specific.
        with self.assertRaisesRegex(LexerError, "Invalid escape sequence: \\\\q"):
            tokenize('"\\n\\q\\t"')

    def test_string_unterminated_escape(self):
        # For a string like "hello\", the current STRING_REGEX_WITH_ESCAPES fails to match it as a TOKEN_STRING.
        # It falls through to MISMATCH, which raises a ValueError on the initial quote.
        # This test reflects that current behavior.
        # If STRING_REGEX_WITH_ESCAPES is improved to handle content ending in \,
        # then _unescape_string would be called and would raise LexerError("Unterminated...").
        with self.assertRaisesRegex(
            ValueError, r"Lexer error: Unexpected character '\"'"
        ):
            s1 = '"hello\\"'
            tokenize(s1)

        # A string like "\" (content is just one bslash) also fails the regex and raises ValueError.
        with self.assertRaisesRegex(
            ValueError, r"Lexer error: Unexpected character '\"'"
        ):
            s2 = '"\\"'
            tokenize(s2)

    def test_booleans(self):
        self.assertEqual(tokenize("true"), [(TOKEN_BOOLEAN, True)])
        self.assertEqual(tokenize("false"), [(TOKEN_BOOLEAN, False)])
        # Case-insensitivity
        self.assertEqual(tokenize("True"), [(TOKEN_BOOLEAN, True)])
        self.assertEqual(tokenize("FALSE"), [(TOKEN_BOOLEAN, False)])

    def test_nil(self):
        self.assertEqual(tokenize("nil"), [(TOKEN_NIL, None)])

    def test_symbols(self):
        self.assertEqual(tokenize("abc"), [(TOKEN_SYMBOL, "abc")])
        self.assertEqual(tokenize("my-var!"), [(TOKEN_SYMBOL, "my-var!")])
        self.assertEqual(tokenize("+"), [(TOKEN_SYMBOL, "+")])
        self.assertEqual(tokenize("<="), [(TOKEN_SYMBOL, "<=")])
        self.assertEqual(tokenize("key:"), [(TOKEN_SYMBOL, "key:")])
        self.assertEqual(tokenize(":value"), [(TOKEN_SYMBOL, ":value")])

    def test_structural_tokens(self):
        self.assertEqual(tokenize("("), [(TOKEN_LPAREN, "(")])
        self.assertEqual(tokenize(")"), [(TOKEN_RPAREN, ")")])
        self.assertEqual(tokenize("["), [(TOKEN_LBRACKET, "[")])
        self.assertEqual(tokenize("]"), [(TOKEN_RBRACKET, "]")])
        self.assertEqual(tokenize("{"), [(TOKEN_LBRACE, "{")])
        self.assertEqual(tokenize("}"), [(TOKEN_RBRACE, "}")])
        self.assertEqual(tokenize("'"), [(TOKEN_QUOTE, "'")])

    def test_whitespace_and_comments(self):
        self.assertEqual(tokenize("  123  "), [(TOKEN_NUMBER, "123")])
        self.assertEqual(
            tokenize("abc ; this is a comment\n  def"),
            [(TOKEN_SYMBOL, "abc"), (TOKEN_SYMBOL, "def")],
        )
        self.assertEqual(
            tokenize("; entire line comment\n456"), [(TOKEN_NUMBER, "456")]
        )

    def test_combined_expression(self):
        source1 = "(+ 10 20)"
        expected_tokens1 = [
            (TOKEN_LPAREN, "("),
            (TOKEN_SYMBOL, "+"),
            (TOKEN_NUMBER, "10"),
            (TOKEN_NUMBER, "20"),
            (TOKEN_RPAREN, ")"),
        ]
        self.assertEqual(tokenize(source1), expected_tokens1)

        source2 = """
; Define a function
(define my-func (fn [x y]
  ; This is a comment inside
  { :a (+ x 10) ; map with a key
    :b "a string"  ; another entry
    :c [nil false "data"] ; nested vector
  } ))

; Call it
(my-func 123 "ignored")
"""
        expected_tokens2 = [
            (TOKEN_LPAREN, "("),  # define
            (TOKEN_SYMBOL, "define"),
            (TOKEN_SYMBOL, "my-func"),
            (TOKEN_LPAREN, "("),  # fn
            (TOKEN_SYMBOL, "fn"),
            (TOKEN_LBRACKET, "["),
            (TOKEN_SYMBOL, "x"),
            (TOKEN_SYMBOL, "y"),
            (TOKEN_RBRACKET, "]"),
            (TOKEN_LBRACE, "{"),  # map
            (TOKEN_SYMBOL, ":a"),
            (TOKEN_LPAREN, "("),  # +
            (TOKEN_SYMBOL, "+"),
            (TOKEN_SYMBOL, "x"),
            (TOKEN_NUMBER, "10"),
            (TOKEN_RPAREN, ")"),  # end +
            (TOKEN_SYMBOL, ":b"),
            (TOKEN_STRING, "a string"),
            (TOKEN_SYMBOL, ":c"),
            (TOKEN_LBRACKET, "["),  # vector
            (TOKEN_NIL, None),
            (TOKEN_BOOLEAN, False),
            (TOKEN_STRING, "data"),
            (TOKEN_RBRACKET, "]"),  # end vector
            (TOKEN_RBRACE, "}"),  # end map
            (TOKEN_RPAREN, ")"),  # end fn
            (TOKEN_RPAREN, ")"),  # end define
            (TOKEN_LPAREN, "("),  # my-func call
            (TOKEN_SYMBOL, "my-func"),
            (TOKEN_NUMBER, "123"),
            (TOKEN_STRING, "ignored"),
            (TOKEN_RPAREN, ")"),  # end my-func call
        ]
        self.assertEqual(tokenize(source2), expected_tokens2)

    def test_invalid_character(self):
        with self.assertRaisesRegex(ValueError, "Lexer error: Unexpected character"):
            tokenize("123 @ 456")  # @ is not a valid token start

    def test_commas_in_vectors(self):
        """Test that commas are optional and ignored in vectors."""
        # Vector without commas
        self.assertEqual(
            tokenize("[1 2 3]"),
            [
                (TOKEN_LBRACKET, "["),
                (TOKEN_NUMBER, "1"),
                (TOKEN_NUMBER, "2"),
                (TOKEN_NUMBER, "3"),
                (TOKEN_RBRACKET, "]"),
            ],
        )

        # Vector with commas
        self.assertEqual(
            tokenize("[1, 2, 3]"),
            [
                (TOKEN_LBRACKET, "["),
                (TOKEN_NUMBER, "1"),
                (TOKEN_NUMBER, "2"),
                (TOKEN_NUMBER, "3"),
                (TOKEN_RBRACKET, "]"),
            ],
        )

        # Mixed types with commas
        self.assertEqual(
            tokenize('[1, "two", :three]'),
            [
                (TOKEN_LBRACKET, "["),
                (TOKEN_NUMBER, "1"),
                (TOKEN_STRING, "two"),
                (TOKEN_SYMBOL, ":three"),
                (TOKEN_RBRACKET, "]"),
            ],
        )

    def test_commas_in_maps(self):
        """Test that commas are optional and ignored in maps."""
        # Map without commas
        self.assertEqual(
            tokenize("{:a 1 :b 2}"),
            [
                (TOKEN_LBRACE, "{"),
                (TOKEN_SYMBOL, ":a"),
                (TOKEN_NUMBER, "1"),
                (TOKEN_SYMBOL, ":b"),
                (TOKEN_NUMBER, "2"),
                (TOKEN_RBRACE, "}"),
            ],
        )

        # Map with commas
        self.assertEqual(
            tokenize("{:a 1, :b 2}"),
            [
                (TOKEN_LBRACE, "{"),
                (TOKEN_SYMBOL, ":a"),
                (TOKEN_NUMBER, "1"),
                (TOKEN_SYMBOL, ":b"),
                (TOKEN_NUMBER, "2"),
                (TOKEN_RBRACE, "}"),
            ],
        )

        # Complex map with commas
        self.assertEqual(
            tokenize('{key1: "value1", key2: "value2"}'),
            [
                (TOKEN_LBRACE, "{"),
                (TOKEN_SYMBOL, "key1:"),
                (TOKEN_STRING, "value1"),
                (TOKEN_SYMBOL, "key2:"),
                (TOKEN_STRING, "value2"),
                (TOKEN_RBRACE, "}"),
            ],
        )

    def test_commas_in_function_parameters(self):
        """Test that commas are optional and ignored in function parameter lists."""
        # Function params without commas
        self.assertEqual(
            tokenize("(fn [x y z] (+ x y z))"),
            [
                (TOKEN_LPAREN, "("),
                (TOKEN_SYMBOL, "fn"),
                (TOKEN_LBRACKET, "["),
                (TOKEN_SYMBOL, "x"),
                (TOKEN_SYMBOL, "y"),
                (TOKEN_SYMBOL, "z"),
                (TOKEN_RBRACKET, "]"),
                (TOKEN_LPAREN, "("),
                (TOKEN_SYMBOL, "+"),
                (TOKEN_SYMBOL, "x"),
                (TOKEN_SYMBOL, "y"),
                (TOKEN_SYMBOL, "z"),
                (TOKEN_RPAREN, ")"),
                (TOKEN_RPAREN, ")"),
            ],
        )

        # Function params with commas
        self.assertEqual(
            tokenize("(fn [x, y, z] (+ x y z))"),
            [
                (TOKEN_LPAREN, "("),
                (TOKEN_SYMBOL, "fn"),
                (TOKEN_LBRACKET, "["),
                (TOKEN_SYMBOL, "x"),
                (TOKEN_SYMBOL, "y"),
                (TOKEN_SYMBOL, "z"),
                (TOKEN_RBRACKET, "]"),
                (TOKEN_LPAREN, "("),
                (TOKEN_SYMBOL, "+"),
                (TOKEN_SYMBOL, "x"),
                (TOKEN_SYMBOL, "y"),
                (TOKEN_SYMBOL, "z"),
                (TOKEN_RPAREN, ")"),
                (TOKEN_RPAREN, ")"),
            ],
        )

    def test_commas_with_whitespace(self):
        """Test that commas work correctly with surrounding whitespace."""
        # Commas with spaces
        self.assertEqual(
            tokenize("[1 , 2 , 3]"),
            [
                (TOKEN_LBRACKET, "["),
                (TOKEN_NUMBER, "1"),
                (TOKEN_NUMBER, "2"),
                (TOKEN_NUMBER, "3"),
                (TOKEN_RBRACKET, "]"),
            ],
        )

        # Commas without spaces
        self.assertEqual(
            tokenize("[1,2,3]"),
            [
                (TOKEN_LBRACKET, "["),
                (TOKEN_NUMBER, "1"),
                (TOKEN_NUMBER, "2"),
                (TOKEN_NUMBER, "3"),
                (TOKEN_RBRACKET, "]"),
            ],
        )

    def test_commas_in_nested_structures(self):
        """Test that commas work correctly in nested data structures."""
        nested_code = '{:a [1, 2, 3], :b {:c "value", :d true}}'
        expected_tokens = [
            (TOKEN_LBRACE, "{"),
            (TOKEN_SYMBOL, ":a"),
            (TOKEN_LBRACKET, "["),
            (TOKEN_NUMBER, "1"),
            (TOKEN_NUMBER, "2"),
            (TOKEN_NUMBER, "3"),
            (TOKEN_RBRACKET, "]"),
            (TOKEN_SYMBOL, ":b"),
            (TOKEN_LBRACE, "{"),
            (TOKEN_SYMBOL, ":c"),
            (TOKEN_STRING, "value"),
            (TOKEN_SYMBOL, ":d"),
            (TOKEN_BOOLEAN, True),
            (TOKEN_RBRACE, "}"),
            (TOKEN_RBRACE, "}"),
        ]
        self.assertEqual(tokenize(nested_code), expected_tokens)


if __name__ == "__main__":
    unittest.main()
