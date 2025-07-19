# lispy_project/lispy/functions/type_check/is_boolean_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("is-boolean?")
def is_boolean(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-boolean?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, bool)


@lispy_documentation("is-boolean?")
def is_boolean_documentation() -> str:
    return """Function: is-boolean?
Arguments: (is-boolean? value)
Description: Tests whether a value is a boolean (true or false).

Examples:
  (is-boolean? true)        ; => true
  (is-boolean? false)       ; => true
  (is-boolean? 1)           ; => false (number)
  (is-boolean? 0)           ; => false (number)
  (is-boolean? "true")      ; => false (string)
  (is-boolean? nil)         ; => false
  (is-boolean? [])          ; => false (vector)

Notes:
  - Returns true only for the boolean values true and false
  - Numbers 1 and 0 are not considered booleans
  - String representations like "true" are not booleans
  - Useful for type validation in conditional logic
  - Requires exactly one argument"""
