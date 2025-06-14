from lispy.exceptions import EvaluationError
from lispy.types import LispyList, Vector, Symbol


def to_str_fn(args, env):
    """Convert a value to its string representation.

    Usage: (to-str value)

    Args:
        value: The value to convert to a string

    Returns:
        A string representation of the input value

    Examples:
        (to-str 42) => "42"
        (to-str 3.14) => "3.14"
        (to-str true) => "true"
        (to-str false) => "false"
        (to-str nil) => "nil"
        (to-str "hello") => "hello"  ; Pass through
        (to-str [1 2 3]) => "[1 2 3]"
        (to-str '(a b c)) => "(a b c)"
        (to-str ':keyword) => ":keyword"
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'to-str' expects 1 argument, got {len(args)}."
        )

    value = args[0]

    # Handle different types
    if value is None:
        return "nil"
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, str):
        return value  # Pass through strings unchanged
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, Symbol):
        return value.name  # Return the symbol name
    elif isinstance(value, Vector):
        # Use the Vector's __repr__ method which gives "[1 2 3]" format
        return repr(value)
    elif isinstance(value, LispyList):
        # Use the LispyList's __repr__ method which gives "(1 2 3)" format
        return repr(value)
    elif isinstance(value, dict):
        # For hash maps, create a simple representation
        items = []
        for k, v in value.items():
            key_str = to_str_fn([k], env) if hasattr(k, "name") else str(k)
            val_str = to_str_fn([v], env)
            items.append(f"{key_str} {val_str}")
        return "{" + " ".join(items) + "}"
    else:
        # Fallback to Python's str() for any other types
        return str(value)


def documentation_str() -> str:
    """Returns documentation for the to-str function."""
    return """Function: to-str
Arguments: (to-str value)
Description: Converts a value to its string representation.

Examples:
  (to-str 42)                              ; => "42"
  (to-str 3.14)                            ; => "3.14"
  (to-str true)                            ; => "true"
  (to-str false)                           ; => "false"
  (to-str nil)                             ; => "nil"
  (to-str "hello")                         ; => "hello" (unchanged)
  (to-str 'symbol)                         ; => "symbol"
  (to-str ':keyword)                       ; => ":keyword"
  (to-str [1 2 3])                         ; => "[1 2 3]"
  (to-str '(a b c))                        ; => "(a b c)"
  (to-str {:a 1 :b 2})                     ; => "{:a 1 :b 2}"

Notes:
  - Requires exactly one argument
  - Strings are returned unchanged (no quotes added)
  - Numbers converted to their decimal representation
  - Booleans become "true"/"false", nil becomes "nil"
  - Symbols return their name without quotes
  - Collections return bracketed representations
  - Useful for string interpolation and building messages
  - Compatible with append function for concatenation"""
