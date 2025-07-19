from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import Vector
from ..decorators import lispy_function, lispy_documentation


@lispy_function("concat")
def concat_func(args: List[Any], env: Environment) -> Vector:
    """(concat collection1 collection2 ...)
    Concatenates multiple collections into a single list.
    With no arguments, returns empty list.
    """
    # Handle empty case
    if len(args) == 0:
        return Vector([])

    result = []
    
    for i, collection in enumerate(args):
        # Handle nil case - nil contributes nothing
        if collection is None:
            continue
            
        # Validate collection types
        if isinstance(collection, list):
            result.extend(collection)
        elif isinstance(collection, str):
            result.extend(list(collection))  # Convert string to list of characters
        else:
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to 'concat' must be a list, vector, or string, got {type(collection).__name__}: '{collection}'"
            )

    return Vector(result)


@lispy_documentation("concat")
def concat_documentation() -> str:
    return """Function: concat
Arguments: (concat collection1 collection2 ...)
Description: Concatenates multiple collections into a single list.

Examples:
  (concat [1 2] [3 4])          ; => [1 2 3 4]
  (concat [1 2] [3 4] [5])      ; => [1 2 3 4 5]
  (concat '(a b) '(c d))        ; => [a b c d]
  (concat "hello" "world")      ; => ["h" "e" "l" "l" "o" "w" "o" "r" "l" "d"]
  (concat [] [1 2] [])          ; => [1 2]
  (concat [1] nil [2])          ; => [1 2]
  (concat)                      ; => []

Notes:
  - Accepts any number of arguments (including 0)
  - Collections must be lists, vectors, or strings
  - Strings are converted to lists of characters
  - nil arguments are ignored
  - Always returns a list
  - Empty collections contribute nothing to result
  - Order of elements preserved across all collections
  - Essential for combining multiple data sources"""
