from typing import List, Any, Union
from ...exceptions import EvaluationError
from numbers import Number
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation

Numeric = Union[int, float]


@lispy_function("-")
def subtract(args: List[Any], env: Environment) -> Numeric:
    if not args:
        raise EvaluationError("SyntaxError: '-' requires at least one argument.")

    for i, arg in enumerate(args):
        if not isinstance(arg, Number):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to '-' must be a number, got {type(arg).__name__}: '{arg}'"
            )

    if len(args) == 1:
        return -args[0]
    else:
        result: Numeric = args[0]
        for i in range(1, len(args)):
            result -= args[i]
        return result


@lispy_documentation("-")
def subtract_documentation() -> str:
    return """Function: -
Arguments: (- number1 number2 ...) OR (- number)
Description: Subtracts numbers or negates a single number.

Examples:
  (- 10 4)      ; => 6
  (- 10 2 3)    ; => 5  (10 - 2 - 3)
  (- 7)         ; => -7 (unary minus/negation)
  (- -7)        ; => 7  (negation of negative)
  (- 10.5 0.5)  ; => 10.0
  (- 10 0.5)    ; => 9.5

Notes:
  - With one argument, returns the negation of the number
  - With multiple arguments, subtracts all subsequent numbers from the first
  - Works with both integers and floating-point numbers
  - Requires at least one argument"""
