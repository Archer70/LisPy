from numbers import Number
from typing import Any, List, Union

from ...environment import Environment
from ...exceptions import EvaluationError
from ..decorators import lispy_documentation, lispy_function

Numeric = Union[int, float]


@lispy_function("+")
def add(args: List[Any], env: Environment) -> Numeric:
    if not args:  # Handles (+)
        return 0  # Standard Lisp behavior for (+) is 0

    total: Numeric = 0
    # Check types and sum
    for i, arg in enumerate(args):
        if not isinstance(arg, Number):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to '+' must be a number, got {type(arg).__name__}: '{arg}'"
            )
        total += arg
    return total


@lispy_documentation("+")
def add_documentation() -> str:
    return """Function: +
Arguments: (+ number1 number2 ...)
Description: Adds zero or more numbers together.

Examples:
  (+)           ; => 0
  (+ 5)         ; => 5
  (+ 2 3)       ; => 5
  (+ 1 2 3 4)   ; => 10
  (+ 2.5 1.5)   ; => 4.0
  (+ -3 7)      ; => 4

Notes:
  - With no arguments, returns 0
  - Accepts both integers and floating-point numbers
  - All arguments must be numbers"""
