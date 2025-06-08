from lispy.types import LispyList, Vector
from lispy.exceptions import EvaluationError
from ..environment import Environment
from typing import List, Any

EXPECTED_TYPES_MSG = "a list, vector, string, or nil"


def builtin_first(args: List[Any], env: Environment):
    """Implementation of the (first collection) LisPy function.
    Returns the first item of a list, vector, or string. Returns nil for nil or empty collections.
    Usage: (first collection)
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'first' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    if collection is None:
        return None
    if isinstance(collection, (LispyList, Vector, str)):
        if not collection:  # Empty list, vector, or string
            return None
        return collection[0]
    else:
        raise EvaluationError(
            f"TypeError: 'first' expects {EXPECTED_TYPES_MSG}, got {type(collection)}."
        )


def documentation_first() -> str:
    """Returns documentation for the first function."""
    return """Function: first
Arguments: (first collection)
Description: Returns the first element of a collection, or nil if empty.

Examples:
  (first (list 1 2 3))      ; => 1
  (first [1 2 3])           ; => 1
  (first "hello")           ; => "h"
  (first (list))            ; => nil
  (first [])                ; => nil
  (first "")                ; => nil
  (first nil)               ; => nil
  (first '((1 2) 3))        ; => (1 2)

Notes:
  - Requires exactly one argument
  - Works with lists, vectors, strings, and nil
  - Returns nil for empty collections or nil input
  - Alternative to car function for lists
  - For strings, returns first character as string
  - Safe alternative to indexing (no errors on empty)"""
