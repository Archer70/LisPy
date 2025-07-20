from typing import Any, List

from ...environment import Environment
from ...exceptions import EvaluationError
from ..decorators import lispy_documentation, lispy_function


@lispy_function("=")
def equals(args: List[Any], env: Environment) -> bool:
    if len(args) < 2:
        raise EvaluationError("SyntaxError: '=' requires at least two arguments.")

    first_item = args[0]
    if not isinstance(first_item, (int, float)):
        raise EvaluationError(
            f"TypeError: Argument 1 to '=' must be a number for comparison, got {type(first_item).__name__}: '{first_item}'"
        )

    for i in range(1, len(args)):
        current_item = args[i]
        if not isinstance(current_item, (int, float)):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to '=' must be a number for comparison, got {type(current_item).__name__}: '{current_item}'"
            )
        if first_item != current_item:
            return False
    return True


@lispy_documentation("=")
def equals_documentation() -> str:
    """Returns documentation for the = function."""
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
