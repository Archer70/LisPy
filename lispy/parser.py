# Parser implementation will go here
from .exceptions import ParseError  # Updated import
from .lexer import TOKEN_RBRACE  # Added LBRACE, RBRACE
from .lexer import TOKEN_RBRACKET  # Added LBRACKET, RBRACKET
from .lexer import (TOKEN_BOOLEAN, TOKEN_LBRACE, TOKEN_LBRACKET, TOKEN_LPAREN,
                    TOKEN_NIL, TOKEN_NUMBER, TOKEN_QUOTE, TOKEN_RPAREN,
                    TOKEN_STRING, TOKEN_SYMBOL)
from .types import (LispyList, LispyMapLiteral,  # Import LispyMapLiteral
                    Symbol, Vector)

# ... import other token types as needed ...


def parse(tokens: list[tuple]):
    """
    Parses a list of tokens into a Lisp expression (AST).
    """
    _tokens = list(tokens)  # Make a mutable copy

    # Forward declaration for _parse_form, as _parse_list will call it.
    # In Python, functions are objects, so actual definition order matters for availability.
    # We will define _parse_form after its helpers, but it needs to be available in _parse_list's scope.
    # This is typically handled by Python's scoping rules for nested functions.

    def _parse_atom(current_token_type, current_token_value):
        """Parses an atomic token and consumes it."""
        _tokens.pop(0)  # Consume the atom token
        if current_token_type == TOKEN_NUMBER:
            try:
                return int(current_token_value)
            except ValueError:
                return float(current_token_value)
        elif current_token_type == TOKEN_STRING:
            return current_token_value  # Already a string
        elif current_token_type == TOKEN_BOOLEAN:
            return current_token_value  # Lexer already returns True/False
        elif current_token_type == TOKEN_NIL:
            # Already None (or a specific Nil object if you have one)
            return current_token_value
        elif current_token_type == TOKEN_SYMBOL:
            # Ensure it's a string (Symbol class might be better later)
            return Symbol(str(current_token_value))
        # Should not be reached if _parse_form calls it correctly
        raise ParseError(
            f"Internal Error: _parse_atom called with unhandled type {current_token_type}"
        )

    def _parse_list():
        """Parses a list form '()' , consuming '(' and ')' and all elements."""
        _tokens.pop(0)  # Consume '('
        expr_list = []
        while _tokens:
            if _tokens[0][0] == TOKEN_RPAREN:
                _tokens.pop(0)  # Consume ')'
                return LispyList(expr_list)  # Changed List to LispyList
            else:
                # Recursively parse inner expression
                expr_list.append(_parse_form())  # Call the main _parse_form
        # If loop finishes without RPAREN, it's an error
        raise ParseError("Unexpected end of input: missing ')' while parsing list")

    def _parse_vector():
        """Parses a vector form '[]', consuming '[' and ']' and all elements."""
        _tokens.pop(0)  # Consume '['
        vector_elements = []
        while _tokens:
            if _tokens[0][0] == TOKEN_RBRACKET:
                _tokens.pop(0)  # Consume ']'
                return Vector(
                    vector_elements
                )  # Successfully parsed vector, return as Vector type
            else:
                # Recursively parse inner expression
                vector_elements.append(_parse_form())  # Call the main _parse_form
        # If loop finishes without RBRACKET, it's an error
        raise ParseError("Unexpected end of input: missing ']' while parsing vector")

    def _parse_map():
        """Parses a map form '{}', consuming '{' and '}' and all key-value pairs."""
        _tokens.pop(0)  # Consume '{'
        map_data = LispyMapLiteral()  # Use LispyMapLiteral instead of dict

        while _tokens:
            if _tokens[0][0] == TOKEN_RBRACE:
                _tokens.pop(0)  # Consume '}'
                return map_data  # Successfully parsed map

            # --- Parse Key ---
            if not _tokens:
                raise ParseError(
                    "Unexpected end of input: missing '}' while parsing map"
                )

            key_token_type, key_token_value = _tokens[0]  # Peek at key token

            # Allow symbols, strings, numbers, booleans, and nil as map keys
            if key_token_type not in (
                TOKEN_SYMBOL,
                TOKEN_STRING,
                TOKEN_NUMBER,
                TOKEN_BOOLEAN,
                TOKEN_NIL,
            ):
                raise ParseError(
                    f"Map key must be a symbol, string, number, boolean, or nil, got {key_token_type}"
                )

            # Parse the key
            key = _parse_form()  # This will consume the key token

            # --- Parse Value ---
            if not _tokens:  # Missing value for the last key
                raise ParseError(
                    f"Unexpected end of input: map literal requires a value for key: {key}"
                )

            if (
                _tokens[0][0] == TOKEN_RBRACE
            ):  # Key without a value before closing brace
                raise ParseError(
                    f"Map literals require an even number of forms (key-value pairs), missing value for key: {key}"
                )

            value = _parse_form()  # Parse the value expression
            map_data[key] = value

        # If loop finishes without RBRACE, it's an unclosed map error
        raise ParseError("Unexpected end of input: missing '}' while parsing map")

    def _parse_form():  # Parses one form/expression
        if not _tokens:
            raise ParseError("Unexpected end of input while parsing form")

        token_type, token_value = _tokens[0]  # Peek, don't pop yet

        if token_type == TOKEN_LPAREN:
            return _parse_list()
        elif token_type == TOKEN_LBRACKET:  # Handle vector literals
            return _parse_vector()
        elif token_type == TOKEN_LBRACE:  # Handle map literals
            return _parse_map()
        elif token_type == TOKEN_QUOTE:  # Handle ' shorthand for quote
            _tokens.pop(0)  # Consume the TOKEN_QUOTE token
            if not _tokens:  # Check if there's an expression to quote
                raise ParseError(
                    "SyntaxError: 'quote' shorthand ' must be followed by an expression."
                )
            quoted_expression = (
                _parse_form()
            )  # Parse the expression that follows the quote
            return LispyList(
                [Symbol("quote"), quoted_expression]
            )  # Changed List to LispyList
        elif token_type in (
            TOKEN_NUMBER,
            TOKEN_STRING,
            TOKEN_BOOLEAN,
            TOKEN_NIL,
            TOKEN_SYMBOL,
        ):
            return _parse_atom(token_type, token_value)
        else:
            # _tokens.pop(0) # Do not consume here, error is about current token
            raise ParseError(
                f"Unexpected token type during parsing: {token_type} ('{token_value}')"
            )

    if not tokens:  # Original token list was empty
        raise ParseError("Unexpected end of input: No tokens to parse.")

    parsed_expression = _parse_form()

    if _tokens:  # If there are unconsumed tokens after parsing one top-level expression
        raise ParseError(f"Unexpected tokens at end of input: {_tokens}")

    return parsed_expression


# For now, assume we parse one top-level form.
# If multiple forms are allowed at top level (e.g. from a file),
# this would need to be a loop that collects results.
