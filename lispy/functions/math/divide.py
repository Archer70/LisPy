from typing import List, Any, Union
from ...exceptions import EvaluationError
from numbers import Number
from ...environment import Environment

Numeric = Union[int, float]


def builtin_divide(args: List[Any], env: Environment) -> float:
    """Divides numbers. (/ num1 num2 ...)
    If no arguments or one argument, raises error.
    All results are floats.
    """
    if len(args) < 2:
        raise EvaluationError("SyntaxError: '/' requires at least two arguments.")

    for i, arg in enumerate(args):
        if not isinstance(arg, Number):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to '/' must be a number, got {type(arg).__name__}: '{arg}'"
            )

    # Check for division by zero in subsequent arguments
    for i in range(1, len(args)):
        if args[i] == 0:
            raise EvaluationError(
                f"ZeroDivisionError: Division by zero (argument {i + 1})."
            )

    result: float = float(args[0])  # Start with the first number as a float
    for i in range(1, len(args)):
        result /= float(args[i])
    return result


def documentation_divide() -> str:
    """Returns documentation for the / function."""
    return """Function: /
Arguments: (/ number1 number2 ...)
Description: Divides numbers sequentially, always returning a float.

Examples:
  (/ 10 2)      ; => 5.0
  (/ 100 2 5)   ; => 10.0  (100 / 2 / 5)
  (/ 9 2)       ; => 4.5
  (/ 5.0 2.0)   ; => 2.5
  (/ -10 2)     ; => -5.0
  (/ 10 -2)     ; => -5.0
  (/ -10 -2)    ; => 5.0

Notes:
  - Always returns a float, even when dividing integers
  - Requires at least two arguments
  - Divides the first number by the second, then by the third, etc.
  - Division by zero raises an error
  - Works with both integers and floating-point numbers"""
