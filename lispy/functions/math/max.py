from typing import List, Any, Union
from ...exceptions import EvaluationError
from numbers import Number
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation

Numeric = Union[int, float]


@lispy_function("max")
def max_func(args: List[Any], env: Environment) -> Numeric:
    if len(args) == 0:
        raise EvaluationError("SyntaxError: 'max' expects at least 1 argument, got 0.")

    for i, arg in enumerate(args):
        if not isinstance(arg, Number) or isinstance(arg, bool):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to 'max' must be a number, got {type(arg).__name__}: '{arg}'"
            )

    return max(args)


@lispy_documentation("max")
def max_documentation() -> str:
    return """Function: max
Arguments: (max number1 number2 ...)
Description: Returns the largest number from the given arguments.

Examples:
  (max 5)           ; => 5
  (max 1 5 3)       ; => 5
  (max -1 -5 -3)    ; => -1
  (max 3.14 2.71)   ; => 3.14
  (max 5 5.1)       ; => 5.1

Notes:
  - Requires at least one argument
  - All arguments must be numbers
  - Returns the argument with the highest numerical value
  - Works with both integers and floating-point numbers
  - Useful for finding maximum values in calculations"""
