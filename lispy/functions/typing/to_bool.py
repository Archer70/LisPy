from lispy.exceptions import EvaluationError

def to_bool_fn(args, env):
    """Convert a value to a boolean, if possible.

    Usage: (to-bool value)
    """
    if len(args) != 1:
        raise EvaluationError(f"SyntaxError: 'to-bool' expects 1 argument, got {len(args)}.")
    value = args[0]
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    if isinstance(value, float):
        return value != 0.0
    if value is None:
        return False
    if isinstance(value, str):
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        if value.strip() == "":
            return False
        raise EvaluationError(f"TypeError: Cannot convert string '{value}' to bool. Only 'true', 'false', or empty string allowed.")
    if isinstance(value, (list, dict)):
        return len(value) > 0
    raise EvaluationError(f"TypeError: Cannot convert {type(value).__name__} to bool.")

def documentation_to_bool():
    return '''Function: to-bool
Arguments: (to-bool value)
Description: Converts a value to a boolean, if possible. Raises an error if conversion is not possible.

Examples:
  (to-bool true)        ; => true
  (to-bool false)       ; => false
  (to-bool 1)           ; => true
  (to-bool 0)           ; => false
  (to-bool 3.14)        ; => true
  (to-bool 0.0)         ; => false
  (to-bool "true")      ; => true
  (to-bool "false")     ; => false
  (to-bool "")          ; => false
  (to-bool nil)         ; => false
  (to-bool [1 2 3])     ; => true
  (to-bool [])          ; => false
  (to-bool {:a 1})      ; => true
  (to-bool {})          ; => false
''' 