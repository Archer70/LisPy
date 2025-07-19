# lispy_project/lispy/functions/type_check/is_number_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from numbers import Number
from ..decorators import lispy_function, lispy_documentation


@lispy_function("is-number?")
def is_number(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-number?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, Number) and not isinstance(arg, bool)


@lispy_documentation("is-number?")
def is_number_documentation() -> str:
    return """Function: is-number?
Arguments: (is-number? value)
Description: Tests whether a value is a number (integer or float).

Examples:
  (is-number? 42)           ; => true
  (is-number? 3.14)         ; => true
  (is-number? -5)           ; => true
  (is-number? 0)            ; => true
  (is-number? "42")         ; => false (string)
  (is-number? true)         ; => false (boolean)
  (is-number? nil)          ; => false
  (is-number? [1 2 3])      ; => false (vector)

Notes:
  - Returns true for both integers and floating-point numbers
  - Returns false for booleans (even though they're technically numbers in Python)
  - Useful for type validation before arithmetic operations
  - Requires exactly one argument"""
