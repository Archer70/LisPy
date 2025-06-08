from typing import List, Any, Union
from ..exceptions import EvaluationError
from numbers import Number
from ..environment import Environment

Numeric = Union[int, float]


def builtin_abs(args: List[Any], env: Environment) -> Numeric:
    """Returns the absolute value of a number. (abs num)"""
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


def documentation_abs() -> str:
    """Returns documentation for the abs function."""
    return """Function: abs
Arguments: (abs number)
Description: Returns the absolute value of a number.

Examples:
  (abs 5)       ; => 5
  (abs -5)      ; => 5
  (abs 0)       ; => 0
  (abs -3.14)   ; => 3.14
  (abs (- 2 7)) ; => 5

Notes:
  - Always returns a non-negative number
  - Preserves the type (int or float) of the input""" 