# lispy_project/lispy/functions/type_check/is_string_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment


def builtin_is_string_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a string, false otherwise. (is-string? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-string?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, str)


def documentation_is_string_q() -> str:
    """Returns documentation for the is-string? function."""
    return """Function: is-string?
Arguments: (is-string? value)
Description: Tests whether a value is a string.

Examples:
  (is-string? "hello")      ; => true
  (is-string? "")           ; => true
  (is-string? "123")        ; => true
  (is-string? "hello\\nworld") ; => true
  (is-string? 42)           ; => false
  (is-string? true)         ; => false
  (is-string? nil)          ; => false
  (is-string? [1 2 3])      ; => false
  (is-string? '(a b c))     ; => false

Notes:
  - Returns true for any string, including empty strings
  - Returns true for strings containing numbers like "123"
  - Returns false for all non-string types
  - Essential for type validation and string processing
  - Requires exactly one argument"""
