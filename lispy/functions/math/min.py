from typing import List, Any, Union
from ...exceptions import EvaluationError
from numbers import Number
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation

Numeric = Union[int, float]


@lispy_function("min")
def min_func(args: List[Any], env: Environment) -> Numeric:
    if len(args) == 0:
        raise EvaluationError("SyntaxError: 'min' expects at least 1 argument, got 0.")

    for i, arg in enumerate(args):
        if not isinstance(arg, Number) or isinstance(arg, bool):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to 'min' must be a number, got {type(arg).__name__}: '{arg}'"
            )

    return min(args)


@lispy_documentation("min")
def min_documentation() -> str:
    return """Function: min
Arguments: (min number1 number2 ...)
Description: Returns the smallest number from the given arguments.

Examples:
  (min 5)           ; => 5
  (min 1 5 3)       ; => 1
  (min -1 -5 -3)    ; => -5
  (min 3.14 2.71)   ; => 2.71
  (min 5 4.9)       ; => 4.9

Notes:
  - Requires at least one argument
  - All arguments must be numbers
  - Returns the argument with the lowest numerical value
  - Works with both integers and floating-point numbers
  - Useful for finding minimum values in calculations"""
