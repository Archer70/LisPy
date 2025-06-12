from typing import List, Any, Union
from ...exceptions import EvaluationError
from numbers import Number
from ...environment import Environment

Numeric = Union[int, float]


def builtin_min(args: List[Any], env: Environment) -> Numeric:
    """Returns the minimum of the given numbers. (min num1 num2 ...)"""
    if len(args) == 0:
        raise EvaluationError("SyntaxError: 'min' expects at least 1 argument, got 0.")

    # Validate all arguments are numbers and find minimum
    minimum = None
    for i, arg in enumerate(args):
        if not isinstance(arg, Number) or isinstance(arg, bool):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to 'min' must be a number, got {type(arg).__name__}: '{arg}'"
            )

        if minimum is None or arg < minimum:
            minimum = arg

    return minimum


def documentation_min() -> str:
    """Returns documentation for the min function."""
    return """Function: min
Arguments: (min number1 number2 ...)
Description: Returns the smallest of the given numbers.

Examples:
  (min 5)           ; => 5
  (min 3 7)         ; => 3
  (min 10 3 7 1 9)  ; => 1
  (min -5 -2 -8)    ; => -8
  (min 5 -3 2)      ; => -3
  (min 3.14 2.71)   ; => 2.71

Notes:
  - Requires at least one argument
  - Works with both integers and floating-point numbers
  - All arguments must be numbers"""
