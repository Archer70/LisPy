# lispy_project/lispy/functions/count.py
from typing import List, Any
from ..types import Vector  # For type checking
from ..exceptions import EvaluationError
from ..environment import Environment  # Added Environment import


def builtin_count(args: List[Any], env: Environment) -> int:  # Added env parameter
    """Returns the number of items in a collection (list, vector, map, string) or 0 for nil. (count collection)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'count' expects 1 argument, got {len(args)}."
        )

    arg = args[0]

    if arg is None:  # nil
        return 0
    elif isinstance(arg, (list, Vector, str, dict)):
        return len(arg)
    else:
        type_name = type(arg).__name__
        # Special handling for Function type name for clarity in error
        if hasattr(arg, "__class__") and arg.__class__.__name__ == "Function":
            type_name = "Function"  # Though count shouldn't be called on functions
        raise EvaluationError(
            f"TypeError: 'count' expects a list, vector, map, string, or nil. Got {type_name}"
        )


def documentation_count() -> str:
    """Returns documentation for the count function."""
    return """Function: count
Arguments: (count collection)
Description: Returns the number of items in a collection.

Examples:
  (count (list 1 2 3))      ; => 3
  (count [1 2 3])           ; => 3
  (count {:a 1 :b 2})       ; => 2
  (count "hello")           ; => 5
  (count "")                ; => 0
  (count (list))            ; => 0
  (count [])                ; => 0
  (count nil)               ; => 0

Notes:
  - Requires exactly one argument
  - Works with lists, vectors, maps, strings, and nil
  - For maps, counts key-value pairs
  - For strings, counts characters
  - nil always returns 0
  - Empty collections return 0"""
