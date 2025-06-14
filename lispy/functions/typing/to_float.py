from lispy.exceptions import EvaluationError

def to_float_fn(args, env):
    """Convert a value to a float, if possible.

    Usage: (to-float value)
    """
    if len(args) != 1:
        raise EvaluationError(f"SyntaxError: 'to-float' expects 1 argument, got {len(args)}.")
    value = args[0]
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return float(value)
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except Exception:
            raise EvaluationError(f"TypeError: Cannot convert string '{value}' to float.")
    raise EvaluationError(f"TypeError: Cannot convert {type(value).__name__} to float.")

def documentation_to_float():
    return '''Function: to-float
Arguments: (to-float value)
Description: Converts a value to a float, if possible. Raises an error if conversion is not possible.

Examples:
  (to-float 42)        ; => 42.0
  (to-float 3.14)      ; => 3.14
  (to-float "42")      ; => 42.0
  (to-float "3.14")    ; => 3.14
  (to-float true)      ; => 1.0
  (to-float false)     ; => 0.0
  (to-float nil)       ; => error
  (to-float [1 2 3])   ; => error
''' 