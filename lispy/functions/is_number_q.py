# lispy_project/lispy/functions/number_q.py
from typing import List, Any
from numbers import Number
from ..exceptions import EvaluationError
from ..environment import Environment


def builtin_is_number_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a number, false otherwise. (is_number? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_number?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    # Check for Number but exclude booleans (since bool is a subclass of int in Python)
    return isinstance(arg, Number) and not isinstance(arg, bool)


def documentation_is_number_q() -> str:
    """Returns documentation for the is_number? function."""
    return """Function: is_number?
Arguments: (is_number? value)
Description: Tests whether a value is a number (integer or float).

Examples:
  (is_number? 42)       ; => true
  (is_number? -17)      ; => true
  (is_number? 0)        ; => true
  (is_number? 3.14)     ; => true
  (is_number? -2.5)     ; => true
  (is_number? "123")    ; => false
  (is_number? true)     ; => false
  (is_number? nil)      ; => false
  (is_number? [1 2 3])  ; => false

Notes:
  - Returns true for both integers and floating-point numbers
  - Returns false for booleans (even though they're numeric in Python)
  - Returns false for numeric strings like "123"
  - Essential for type validation in dynamic code
  - Requires exactly one argument""" 