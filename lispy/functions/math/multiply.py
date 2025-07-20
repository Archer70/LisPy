from numbers import Number
from typing import Any, List, Union

from ...environment import Environment
from ...exceptions import EvaluationError
from ..decorators import lispy_documentation, lispy_function

Numeric = Union[int, float]


@lispy_function("*")
def multiply(args: List[Any], env: Environment) -> Numeric:
    if not args:
        return 1  # Identity for multiplication

    product: Numeric = 1
    for i, arg in enumerate(args):
        if not isinstance(arg, Number):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to '*' must be a number, got {type(arg).__name__}: '{arg}'"
            )
        product *= arg
    return product


@lispy_documentation("*")
def multiply_documentation() -> str:
    return """Function: *
Arguments: (* number1 number2 ...)
Description: Multiplies zero or more numbers together.

Examples:
  (*)           ; => 1
  (* 5)         ; => 5
  (* 2 3)       ; => 6
  (* 2 3 4)     ; => 24
  (* 5 0)       ; => 0
  (* 5 1)       ; => 5
  (* 5 0.5)     ; => 2.5
  (* 2.5 2.0)   ; => 5.0

Notes:
  - With no arguments, returns 1 (multiplicative identity)
  - With one argument, returns that number
  - Works with both integers and floating-point numbers
  - All arguments must be numbers"""
