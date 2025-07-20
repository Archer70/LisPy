from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_function, lispy_documentation

@lispy_function("to-int")
def to_int(args, env):
    """Convert a value to an integer, if possible.

    Usage: (to-int value)
    """
    if len(args) != 1:
        raise EvaluationError(f"SyntaxError: 'to-int' expects 1 argument, got {len(args)}.")
    value = args[0]
    if isinstance(value, int):
        return value
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            # Try int first, then float->int
            return int(value) if value.strip().isdigit() else int(float(value))
        except Exception:
            raise EvaluationError(f"TypeError: Cannot convert string '{value}' to int.")
    raise EvaluationError(f"TypeError: Cannot convert {type(value).__name__} to int.")

@lispy_documentation("to-int")
def to_int_documentation():
    return '''Function: to-int
Arguments: (to-int value)
Description: Converts a value to an integer, if possible. Raises an error if conversion is not possible.

Examples:
  (to-int 42)        ; => 42
  (to-int 3.14)      ; => 3
  (to-int "42")      ; => 42
  (to-int "3.14")    ; => 3
  (to-int true)      ; => 1
  (to-int false)     ; => 0
  (to-int nil)       ; => error
  (to-int [1 2 3])   ; => error
''' 