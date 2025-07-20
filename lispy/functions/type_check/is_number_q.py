# lispy_project/lispy/functions/type_check/is_number_q.py
from numbers import Number
from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function


@lispy_function("is-number?")
def is_number_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a number, false otherwise. (is-number? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-number?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    # Check for Number but exclude booleans (since bool is a subclass of int in Python)
    return isinstance(arg, Number) and not isinstance(arg, bool)


@lispy_documentation("is-number?")
def is_number_q_documentation() -> str:
    """Returns documentation for the is-number? function."""
    return """Function: is-number?
Arguments: (is-number? value)
Description: Tests whether a value is a number (integer or float).

Examples:
  (is-number? 42)       ; => true
  (is-number? -17)      ; => true
  (is-number? 0)        ; => true
  (is-number? 3.14)     ; => true
  (is-number? -2.5)     ; => true
  (is-number? "123")    ; => false
  (is-number? true)     ; => false
  (is-number? nil)      ; => false
  (is-number? [1 2 3])  ; => false

Notes:
  - Returns true for both integers and floating-point numbers
  - Returns false for booleans (even though they're numeric in Python)
  - Returns false for numeric strings like "123"
  - Essential for type validation in dynamic code
  - Requires exactly one argument"""
