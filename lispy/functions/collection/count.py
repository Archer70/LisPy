# lispy_project/lispy/functions/count.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("count")
def count_func(args: List[Any], env: Environment) -> int:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'count' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Handle different collection types
    if collection is None:
        return 0
    elif isinstance(collection, (list, str, dict)):
        return len(collection)
    else:
        raise EvaluationError(
            f"TypeError: 'count' expects a collection (list, vector, map, or string), got {type(collection).__name__}: '{collection}'"
        )


@lispy_documentation("count")
def count_documentation() -> str:
    return """Function: count
Arguments: (count collection)
Description: Returns the number of elements in a collection.

Examples:
  (count [1 2 3 4])             ; => 4
  (count '(a b c))              ; => 3
  (count {:a 1 :b 2})           ; => 2
  (count "hello")               ; => 5
  (count [])                    ; => 0
  (count nil)                   ; => 0

Notes:
  - Requires exactly one argument
  - Works with vectors, lists, maps, and strings
  - nil counts as 0 (empty collection)
  - For maps, counts the number of key-value pairs
  - For strings, counts the number of characters
  - Essential for iteration and bounds checking"""
