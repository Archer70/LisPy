from typing import List, Any, Union
from ...exceptions import EvaluationError
from numbers import Number
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation

Numeric = Union[int, float]


@lispy_function("abs")
def abs_func(args: List[Any], env: Environment) -> Numeric:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'abs' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    if not isinstance(arg, Number) or isinstance(arg, bool):
        raise EvaluationError(
            f"TypeError: Argument to 'abs' must be a number, got {type(arg).__name__}: '{arg}'"
        )

    return abs(arg)


@lispy_documentation("abs")
def abs_documentation() -> str:
    return """Function: abs
Arguments: (abs number)
Description: Returns the absolute value of a number.

Examples:
  (abs 5)       ; => 5
  (abs -5)      ; => 5
  (abs 0)       ; => 0
  (abs 3.14)    ; => 3.14
  (abs -3.14)   ; => 3.14

Notes:
  - Requires exactly one argument
  - Returns the distance from zero on the number line
  - Works with both integers and floating-point numbers
  - Negative numbers become positive, positive numbers stay positive"""
