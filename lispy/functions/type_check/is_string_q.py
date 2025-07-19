# lispy_project/lispy/functions/type_check/is_string_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("is-string?")
def is_string(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-string?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, str)


@lispy_documentation("is-string?")
def is_string_documentation() -> str:
    return """Function: is-string?
Arguments: (is-string? value)
Description: Tests whether a value is a string.

Examples:
  (is-string? "hello")      ; => true
  (is-string? "")           ; => true (empty string)
  (is-string? 'world)       ; => false (symbol)
  (is-string? 42)           ; => false (number)
  (is-string? true)         ; => false (boolean)
  (is-string? nil)          ; => false
  (is-string? [1 2 3])      ; => false (vector)

Notes:
  - Returns true only for string values
  - Empty strings are still strings
  - Symbols are not strings
  - Useful for type validation before string operations
  - Requires exactly one argument"""
