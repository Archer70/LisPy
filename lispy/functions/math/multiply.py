from typing import List, Any, Union
from ...exceptions import EvaluationError
from numbers import Number
from ...environment import Environment
# import math # Not strictly needed for multiply, but good if using math.prod later

Numeric = Union[int, float]


def builtin_multiply(args: List[Any], env: Environment) -> Numeric:
    """Multiplies numbers. (* num1 num2 ...)
    If no arguments, returns 1 (identity for multiplication).
    """
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


def documentation_multiply() -> str:
    """Returns documentation for the * function."""
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
