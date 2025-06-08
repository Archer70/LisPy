# lispy_project/lispy/functions/type_check/is_boolean_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment


def builtin_is_boolean_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a boolean, false otherwise. (is_boolean? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_boolean?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, bool)


def documentation_is_boolean_q() -> str:
    """Returns documentation for the is_boolean? function."""
    return """Function: is_boolean?
Arguments: (is_boolean? value)
Description: Tests whether a value is a boolean (true or false).

Examples:
  (is_boolean? true)            ; => true
  (is_boolean? false)           ; => true
  (is_boolean? (= 1 1))         ; => true (comparison result)
  (is_boolean? (< 1 2))         ; => true (comparison result)
  (is_boolean? (not true))      ; => true (logical operation result)
  (is_boolean? nil)             ; => false
  (is_boolean? 0)               ; => false
  (is_boolean? 1)               ; => false
  (is_boolean? "true")          ; => false (string)
  (is_boolean? [])              ; => false (vector)
  (is_boolean? '())             ; => false (list)

Notes:
  - Returns true only for actual boolean values (true/false)
  - Works with boolean results from comparisons and logical operations
  - Returns false for "truthy" or "falsy" values that aren't booleans
  - Returns false for nil, numbers, strings, collections
  - Essential for strict boolean validation
  - Requires exactly one argument""" 