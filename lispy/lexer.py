# Lexer implementation will go here

import re  # Import the regex module
from .exceptions import LexerError # Import LexerError

# Token Types (constants)
TOKEN_NUMBER = "NUMBER"
TOKEN_STRING = "STRING"
TOKEN_BOOLEAN = "BOOLEAN"
TOKEN_NIL = "NIL"
TOKEN_SYMBOL = "SYMBOL"
TOKEN_LPAREN = "LPAREN"  # (
TOKEN_RPAREN = "RPAREN"  # )
TOKEN_LBRACKET = "LBRACKET"  # [
TOKEN_RBRACKET = "RBRACKET"  # ]
TOKEN_LBRACE = "LBRACE"  # {
TOKEN_RBRACE = "RBRACE"  # }
TOKEN_QUOTE = "QUOTE"  # '

# Regex definitions (used by TOKEN_SPECIFICATION)
NUMBER_REGEX = r"[+-]?\d*\.?\d+"
STRING_REGEX_WITH_ESCAPES = r'"((?:\\.|[^"\\])*)"'
BOOLEAN_TRUE_REGEX = r"(?i)\btrue\b"
BOOLEAN_FALSE_REGEX = r"(?i)\bfalse\b"
NIL_REGEX = r"\bnil\b"
SYMBOL_REGEX = r"[a-zA-Z_+\-*/<=>?!.:][a-zA-Z0-9_+\-*/<=>?!.:]*"
LPAREN_REGEX = r"\("
RPAREN_REGEX = r"\)"
LBRACKET_REGEX = r"\["
RBRACKET_REGEX = r"\]"
LBRACE_REGEX = r"\{"
RBRACE_REGEX = r"\}"
QUOTE_REGEX = r"'"
COMMENT_REGEX = r";.*"
COMMA_REGEX = r","

# Token Specification: (token_type, original_pattern_str, compiled_regex_object)
# Order matters for some of these.
_raw_token_specification = [
    (TOKEN_NUMBER, NUMBER_REGEX),
    (TOKEN_STRING, STRING_REGEX_WITH_ESCAPES),
    (TOKEN_BOOLEAN, BOOLEAN_TRUE_REGEX),
    (TOKEN_BOOLEAN, BOOLEAN_FALSE_REGEX),
    (TOKEN_NIL, NIL_REGEX),
    (TOKEN_LPAREN, LPAREN_REGEX),
    (TOKEN_RPAREN, RPAREN_REGEX),
    (TOKEN_LBRACKET, LBRACKET_REGEX),
    (TOKEN_RBRACKET, RBRACKET_REGEX),
    (TOKEN_LBRACE, LBRACE_REGEX),
    (TOKEN_RBRACE, RBRACE_REGEX),
    (TOKEN_QUOTE, QUOTE_REGEX),
    (TOKEN_SYMBOL, SYMBOL_REGEX),
    ('SKIP', r'\s+'),
    ('SKIP', COMMA_REGEX),  # Skip commas like whitespace
    ('SKIP', COMMENT_REGEX),
    ('MISMATCH', r'.')
]

TOKEN_SPECIFICATION = [
    (ttype, p_str, re.compile(p_str))
    for ttype, p_str in _raw_token_specification
]


def _unescape_string(s: str) -> str:
    # Converts defined escape sequences (e.g., \\n, \\t, \\", \\\\)
    # in a raw string segment. Assumes s is the content of a
    # string literal, with outer quotes already stripped.
    # as per Requirements.md.

    result = []
    i = 0
    n = len(s)
    while i < n:
        char = s[i]
        if char == '\\':
            i += 1
            if i >= n:
                raise LexerError("Unterminated escape sequence at end of string")
            escaped_char = s[i]
            if escaped_char == 'n':
                result.append('\n')
            elif escaped_char == 't':
                result.append('\t')
            elif escaped_char == '"':
                result.append('"')
            elif escaped_char == '\\':
                result.append('\\')
            else:
                raise LexerError(f"Invalid escape sequence: \\{escaped_char}")
        else:
            result.append(char)
        i += 1
    return "".join(result)


def _match_next_token(source_code: str, position: int):
    """Tries to match a token from TOKEN_SPECIFICATION at the given position."""
    # Iterate through (token_type, original_pattern_str, compiled_regex)
    for token_type, pattern_str, compiled_regex in TOKEN_SPECIFICATION:
        match = compiled_regex.match(source_code, position)
        if match:
            # Return original pattern_str for _get_token_value
            return token_type, pattern_str, match
    return None, None, None


def _get_token_value(token_type: str, pattern_str: str, matched_string: str):
    """Converts the raw matched string to its final token value based
    on type and original pattern."""
    # pattern_str is used here to distinguish between boolean true/false and nil
    if pattern_str == NIL_REGEX:
        return None
    elif pattern_str == BOOLEAN_TRUE_REGEX:
        return True
    elif pattern_str == BOOLEAN_FALSE_REGEX:
        return False
    elif token_type == TOKEN_STRING:
        raw_content = matched_string[1:-1]
        return _unescape_string(raw_content)
    else:
        return matched_string


def tokenize(source_code: str) -> list[tuple]:
    tokens = []
    position = 0
    source_len = len(source_code)

    while position < source_len:
        token_details = _match_next_token(source_code, position)
        token_type, pattern_str, match = token_details

        if not match:
            err_msg = (
                f"Lexer error: No token matched at position {position} "
                f"for \'{source_code[position:]}\'"
            )
            raise RuntimeError(err_msg)

        matched_string = match.group(0)

        if token_type == 'SKIP':
            position = match.end(0)
            continue
        elif token_type == 'MISMATCH':
            err_msg = (
                f"Lexer error: Unexpected character \'{matched_string}\' "
                f"at position {position}"
            )
            raise ValueError(err_msg)

        actual_value = _get_token_value(
            token_type, pattern_str, matched_string
        )
        tokens.append((token_type, actual_value))
        position = match.end(0)

    return tokens
