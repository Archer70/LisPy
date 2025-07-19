from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("to-int")
def to_int(args: List[Any], env: Environment) -> int:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'to-int' expects 1 argument, got {len(args)}."
        )

    arg = args[0]

    try:
        if isinstance(arg, bool):
            return 1 if arg else 0
        elif isinstance(arg, int):
            return arg  # Already an int
        elif isinstance(arg, float):
            return int(arg)  # Truncate to integer
        elif isinstance(arg, str):
            # Try to parse as integer
            return int(arg)
        else:
            raise EvaluationError(
                f"TypeError: Cannot convert {type(arg).__name__} to integer: '{arg}'"
            )
    except ValueError:
        raise EvaluationError(
            f"ValueError: Cannot convert string '{arg}' to integer"
        )


@lispy_documentation("to-int")
def to_int_documentation() -> str:
    return """Function: to-int
Arguments: (to-int value)
Description: Converts a value to an integer.

Examples:
  (to-int 3.14)                 ; => 3 (truncated)
  (to-int "42")                 ; => 42
  (to-int "-17")                ; => -17
  (to-int true)                 ; => 1
  (to-int false)                ; => 0
  (to-int 42)                   ; => 42 (already integer)

Notes:
  - Requires exactly one argument
  - Floats are truncated (not rounded) to integers
  - Strings must contain valid integer representation
  - Booleans: true becomes 1, false becomes 0
  - Raises error for invalid conversions
  - Part of the type conversion function family (to-str, to-int, to-float, to-bool)""" 