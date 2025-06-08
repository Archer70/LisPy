# lispy_project/lispy/functions/nil_q.py
from typing import List, Any
from ..exceptions import EvaluationError
from ..environment import Environment


def builtin_is_nil_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is nil, false otherwise. (is_nil? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_nil?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return arg is None


def documentation_is_nil_q() -> str:
    """Returns documentation for the is_nil? function."""
    return """Function: is_nil?
Arguments: (is_nil? value)
Description: Tests whether a value is nil (represents absence of value).

Examples:
  (is_nil? nil)             ; => true
  (is_nil? 0)               ; => false
  (is_nil? false)           ; => false
  (is_nil? "")              ; => false (empty string)
  (is_nil? '())             ; => false (empty list)
  (is_nil? [])              ; => false (empty vector)
  (is_nil? {})              ; => false (empty map)
  (is_nil? 42)              ; => false

Notes:
  - Returns true only for the nil value
  - nil represents the absence of a value in LisPy
  - Different from empty collections, zero, or false
  - Essential for null-checking and optional value handling
  - Often used in conditional logic and error handling
  - Requires exactly one argument""" 