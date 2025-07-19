from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("=")
def equals(args: List[Any], env: Environment) -> bool:
    if len(args) < 2:
        raise EvaluationError("SyntaxError: '=' requires at least two arguments.")

    # Check if all arguments are numbers and equal to the first one
    first_arg = args[0]
    if not isinstance(first_arg, (int, float)):
        raise EvaluationError(
            f"TypeError: Argument 1 to '=' must be a number for comparison, got {type(first_arg).__name__}: '{first_arg}'"
        )

    for i, arg in enumerate(args[1:], start=2):
        if not isinstance(arg, (int, float)):
            raise EvaluationError(
                f"TypeError: Argument {i} to '=' must be a number for comparison, got {type(arg).__name__}: '{arg}'"
            )
        if arg != first_arg:
            return False

    return True


@lispy_documentation("=")
def equals_documentation() -> str:
    return """Function: =
Arguments: (= number1 number2 ...)
Description: Tests if all numbers are equal.

Examples:
  (= 5 5)           ; => true
  (= 5.0 5)         ; => true
  (= 10 10 10)      ; => true
  (= 5 6)           ; => false
  (= 10 10 6 10)    ; => false
  (= -5 -5.0)       ; => true

Notes:
  - Requires at least two arguments
  - Returns true only if ALL arguments are equal
  - Works with both integers and floating-point numbers
  - 5 and 5.0 are considered equal
  - Currently only supports numeric comparison"""
