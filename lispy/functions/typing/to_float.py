from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("to-float")
def to_float(args: List[Any], env: Environment) -> float:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'to-float' expects 1 argument, got {len(args)}."
        )

    arg = args[0]

    try:
        if isinstance(arg, bool):
            return 1.0 if arg else 0.0
        elif isinstance(arg, (int, float)):
            return float(arg)
        elif isinstance(arg, str):
            # Try to parse as float
            return float(arg)
        else:
            raise EvaluationError(
                f"TypeError: Cannot convert {type(arg).__name__} to float: '{arg}'"
            )
    except ValueError:
        raise EvaluationError(
            f"ValueError: Cannot convert string '{arg}' to float"
        )


@lispy_documentation("to-float")
def to_float_documentation() -> str:
    return """Function: to-float
Arguments: (to-float value)
Description: Converts a value to a floating-point number.

Examples:
  (to-float 42)                 ; => 42.0
  (to-float "3.14")             ; => 3.14
  (to-float "-2.5")             ; => -2.5
  (to-float true)               ; => 1.0
  (to-float false)              ; => 0.0
  (to-float 3.14)               ; => 3.14 (already float)

Notes:
  - Requires exactly one argument
  - Integers are converted to equivalent floats
  - Strings must contain valid number representation
  - Booleans: true becomes 1.0, false becomes 0.0
  - Raises error for invalid conversions
  - Part of the type conversion function family (to-str, to-int, to-float, to-bool)""" 