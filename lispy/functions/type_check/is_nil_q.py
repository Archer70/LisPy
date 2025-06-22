# lispy_project/lispy/functions/type_check/is_nil_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment


def builtin_is_nil_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is nil, false otherwise. (is-nil? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-nil?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return arg is None


def documentation_is_nil_q() -> str:
    """Returns documentation for the is-nil? function."""
    return """Function: is-nil?
Arguments: (is-nil? value)
Description: Tests whether a value is nil (represents absence of value).

Examples:
  (is-nil? nil)             ; => true
  (is-nil? 0)               ; => false
  (is-nil? false)           ; => false
  (is-nil? "")              ; => false (empty string)
  (is-nil? '())             ; => false (empty list)
  (is-nil? [])              ; => false (empty vector)
  (is-nil? {})              ; => false (empty map)
  (is-nil? 42)              ; => false

Notes:
  - Returns true only for the nil value
  - nil represents the absence of a value in LisPy
  - Different from empty collections, zero, or false
  - Essential for null-checking and optional value handling
  - Often used in conditional logic and error handling
  - Requires exactly one argument"""
