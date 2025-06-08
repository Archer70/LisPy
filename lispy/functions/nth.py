from lispy.types import Vector, LispyList
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from typing import List, Any


def nth_fn(args: List[Any], env: Environment):
    """Accesses an element from a vector or list by index.

    Usage: (nth collection index [default])
    - collection: The vector or list to access.
    - index: The 0-based index of the element to retrieve.
    - default: (Optional) The value to return if the index is out of bounds.
               If not provided, an error is raised for out-of-bounds access.
    """
    if not 2 <= len(args) <= 3:
        raise EvaluationError(
            f"SyntaxError: 'nth' expects 2 or 3 arguments, got {len(args)}."
        )

    collection, index, *rest = args
    default_value_provided = len(rest) > 0
    default_value = rest[0] if default_value_provided else None

    if not isinstance(collection, (Vector, LispyList)):
        raise EvaluationError(
            f"TypeError: 'nth' first argument must be a vector or list, got {type(collection)}."
        )

    if not isinstance(index, int):
        raise EvaluationError(
            f"TypeError: 'nth' index must be an integer, got {type(index)}."
        )

    if 0 <= index < len(collection):
        return collection[index]
    elif default_value_provided:
        return default_value
    else:
        raise EvaluationError(
            f"IndexError: {index} out of bounds for collection of size {len(collection)}."
        )


def documentation_nth() -> str:
    """Returns documentation for the nth function."""
    return """Function: nth
Arguments: (nth collection index [default])
Description: Retrieves the element at the specified index from a vector or list.

Examples:
  (nth [10 20 30] 0)            ; => 10 (first element)
  (nth [10 20 30] 1)            ; => 20 (second element)
  (nth [10 20 30] 2)            ; => 30 (third element)
  (nth '(a b c) 1)              ; => b (works with lists too)
  (nth [10 20 30] 5)            ; => IndexError (out of bounds)
  (nth [10 20 30] 5 "default")  ; => "default" (with default value)
  (nth [] 0 nil)                ; => nil (empty collection)
  (nth [1 "hi" true] 1)         ; => "hi" (mixed types)

Notes:
  - Collection must be a vector or list
  - Index must be a non-negative integer (0-based)
  - Returns element at index position
  - Throws IndexError if index out of bounds and no default provided
  - Returns default value if index out of bounds and default provided
  - Supports both vectors and lists uniformly
  - Essential for random access to indexed collections
  - Requires 2 or 3 arguments (collection, index, optional default)"""
