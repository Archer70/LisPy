from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("nth")
def nth_func(args: List[Any], env: Environment) -> Any:
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'nth' expects 2 arguments, got {len(args)}."
        )

    collection, index = args

    # Validate collection
    if collection is None:
        raise EvaluationError("TypeError: Cannot get nth element of nil")
    
    if not isinstance(collection, (list, str)):
        raise EvaluationError(
            f"TypeError: First argument to 'nth' must be a list, vector, or string, got {type(collection).__name__}: '{collection}'"
        )

    # Validate index
    if not isinstance(index, int):
        raise EvaluationError(
            f"TypeError: Second argument to 'nth' must be an integer, got {type(index).__name__}: '{index}'"
        )

    # Check bounds
    if index < 0 or index >= len(collection):
        raise EvaluationError(
            f"IndexError: Index {index} out of bounds for collection of length {len(collection)}"
        )

    return collection[index]


@lispy_documentation("nth")
def nth_documentation() -> str:
    return """Function: nth
Arguments: (nth collection index)
Description: Returns the element at the specified index in a collection.

Examples:
  (nth [10 20 30] 0)            ; => 10 (first element)
  (nth [10 20 30] 2)            ; => 30 (third element)
  (nth '(a b c d) 1)            ; => b
  (nth "hello" 1)               ; => "e"
  (nth [1 2 3] 5)               ; => Error (index out of bounds)

Notes:
  - Requires exactly two arguments: collection and index
  - Collection must be a list, vector, or string
  - Index must be a non-negative integer
  - Uses zero-based indexing (first element is at index 0)
  - Raises error for out-of-bounds access
  - For strings, returns the character at that position
  - Does not accept negative indices
  - Essential for random access to collection elements"""
