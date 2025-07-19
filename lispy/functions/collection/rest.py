from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import Vector
from ..decorators import lispy_function, lispy_documentation


@lispy_function("rest")
def rest_func(args: List[Any], env: Environment) -> List[Any]:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'rest' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Handle nil case
    if collection is None:
        return []

    # Handle different collection types
    if isinstance(collection, list):
        return collection[1:] if len(collection) > 1 else []
    elif isinstance(collection, str):
        # For strings, return the rest as a list of characters
        return list(collection[1:]) if len(collection) > 1 else []
    else:
        raise EvaluationError(
            f"TypeError: 'rest' expects a list, vector, or string, got {type(collection).__name__}: '{collection}'"
        )


@lispy_documentation("rest")
def rest_documentation() -> str:
    return """Function: rest
Arguments: (rest collection)
Description: Returns all elements except the first from a collection.

Examples:
  (rest [1 2 3 4])              ; => [2 3 4]
  (rest '(a b c))               ; => [b c]
  (rest "hello")                ; => ["e" "l" "l" "o"]
  (rest [1])                    ; => []
  (rest [])                     ; => []
  (rest nil)                    ; => []

Notes:
  - Requires exactly one argument
  - Works with lists, vectors, and strings
  - Returns empty list for single-element or empty collections
  - For strings, returns list of remaining characters
  - Always returns a list (not the original collection type)
  - Essential for list processing and recursion
  - Complement of the 'first' function"""
