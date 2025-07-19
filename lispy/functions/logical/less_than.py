from typing import List, Any
from ...exceptions import EvaluationError
from numbers import Number
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("<")
def less_than(args: List[Any], env: Environment) -> bool:
    if len(args) != 2:
        raise EvaluationError("TypeError: < requires exactly two arguments")

    arg1, arg2 = args[0], args[1]

    if not isinstance(arg1, Number):
        raise EvaluationError(
            f"TypeError: Argument 1 to '<' must be a number, got {type(arg1).__name__}: '{arg1}'"
        )
    if not isinstance(arg2, Number):
        raise EvaluationError(
            f"TypeError: Argument 2 to '<' must be a number, got {type(arg2).__name__}: '{arg2}'"
        )

    return arg1 < arg2


@lispy_documentation("<")
def less_than_documentation() -> str:
    return """Function: <
Arguments: (< number1 number2)
Description: Tests if the first number is less than the second.

Examples:
  (< 5 6)           ; => true
  (< -1 0)          ; => true
  (< 5 5.1)         ; => true
  (< 4.9 5)         ; => true
  (< 5 5)           ; => false
  (< 6 5)           ; => false
  (< 0 -1)          ; => false

Notes:
  - Requires exactly two arguments
  - Returns true if first number < second number
  - Works with both integers and floating-point numbers
  - Strict inequality (5 < 5 is false)
  - Use <= for less-than-or-equal comparison"""
