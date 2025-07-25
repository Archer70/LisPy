from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import Vector


@lispy_function("split")
def split_fn(args, env):
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'split' expects 2 arguments, got {len(args)}."
        )

    string, separator = args

    # Validate string is a string
    if not isinstance(string, str):
        raise EvaluationError(
            f"TypeError: 'split' first argument must be a string, got {type(string)}."
        )

    # Validate separator is a string
    if not isinstance(separator, str):
        raise EvaluationError(
            f"TypeError: 'split' second argument (separator) must be a string, got {type(separator)}."
        )

    # Handle special case of empty separator (split into characters)
    if separator == "":
        return Vector(list(string))

    # Split the string
    parts = string.split(separator)
    return Vector(parts)


@lispy_documentation("split")
def split_documentation() -> str:
    """Returns documentation for the split function."""
    return """Function: split
Arguments: (split string separator)
Description: Splits a string into a vector of substrings using a separator.

Examples:
  (split "a,b,c" ",")           ; => ["a" "b" "c"]
  (split "hello world" " ")     ; => ["hello" "world"]
  (split "one-two-three" "-")   ; => ["one" "two" "three"]
  (split "hello" "")            ; => ["h" "e" "l" "l" "o"] (split into chars)
  (split "" ",")                ; => [""] (empty string gives one empty element)
  (split "no-separator" "x")    ; => ["no-separator"] (separator not found)

Notes:
  - Requires exactly 2 arguments
  - First argument must be a string
  - Second argument must be a string (the separator)
  - Empty separator splits into individual characters
  - Returns vector of string parts
  - Empty string returns vector with one empty string
  - Missing separator returns vector with original string
  - Essential for parsing delimited data
  - Useful for CSV processing, path parsing, etc.
  - Complement of the join function"""
