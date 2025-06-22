# lispy_project/lispy/functions/type_check/is_boolean_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment


def builtin_is_boolean_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a boolean, false otherwise. (is-boolean? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-boolean?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, bool)


def documentation_is_boolean_q() -> str:
    """Returns documentation for the is-boolean? function."""
    return """Function: is-boolean?
Arguments: (is-boolean? value)
Description: Tests whether a value is a boolean (true or false).

Examples:
  (is-boolean? true)            ; => true
  (is-boolean? false)           ; => true
  (is-boolean? (= 1 1))         ; => true (comparison result)
  (is-boolean? (< 1 2))         ; => true (comparison result)
  (is-boolean? (not true))      ; => true (logical operation result)
  (is-boolean? nil)             ; => false
  (is-boolean? 0)               ; => false
  (is-boolean? 1)               ; => false
  (is-boolean? "true")          ; => false (string)
  (is-boolean? [])              ; => false (vector)
  (is-boolean? '())             ; => false (list)

Notes:
  - Returns true only for actual boolean values (true/false)
  - Works with boolean results from comparisons and logical operations
  - Returns false for "truthy" or "falsy" values that aren't booleans
  - Returns false for nil, numbers, strings, collections
  - Essential for strict boolean validation
  - Requires exactly one argument"""
