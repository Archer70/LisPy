from numbers import Number
from typing import Any, List, Union

from ...environment import Environment
from ...exceptions import EvaluationError
from ..decorators import lispy_documentation, lispy_function

Numeric = Union[int, float]


@lispy_function("max")
def max_fn(args: List[Any], env: Environment) -> Numeric:
    """Returns the maximum of the given numbers. (max num1 num2 ...)"""
    if len(args) == 0:
        raise EvaluationError("SyntaxError: 'max' expects at least 1 argument, got 0.")

    # Validate all arguments are numbers and find maximum
    maximum = None
    for i, arg in enumerate(args):
        if not isinstance(arg, Number) or isinstance(arg, bool):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to 'max' must be a number, got {type(arg).__name__}: '{arg}'"
            )

        if maximum is None or arg > maximum:
            maximum = arg

    return maximum


@lispy_documentation("max")
def max_documentation() -> str:
    """Returns documentation for the max function."""
    return """Function: max
Arguments: (max number1 number2 ...)
Description: Returns the largest of the given numbers.

Examples:
  (max 5)           ; => 5
  (max 3 7)         ; => 7
  (max 10 3 7 1 9)  ; => 10
  (max -5 -2 -8)    ; => -2
  (max 5 -3 2)      ; => 5
  (max 3.14 2.71)   ; => 3.14

Notes:
  - Requires at least one argument
  - Works with both integers and floating-point numbers
  - All arguments must be numbers"""
