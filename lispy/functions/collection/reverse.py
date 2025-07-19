from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("reverse")
def reverse_func(args: List[Any], env: Environment) -> List[Any]:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'reverse' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Handle nil case
    if collection is None:
        return []

    # Validate and reverse collection
    if isinstance(collection, list):
        return list(reversed(collection))
    elif isinstance(collection, str):
        return list(reversed(collection))
    else:
        raise EvaluationError(
            f"TypeError: 'reverse' expects a list, vector, or string, got {type(collection).__name__}: '{collection}'"
        )


@lispy_documentation("reverse")
def reverse_documentation() -> str:
    return """Function: reverse
Arguments: (reverse collection)
Description: Returns a new list with elements in reverse order.

Examples:
  (reverse [1 2 3 4])           ; => [4 3 2 1]
  (reverse '(a b c))            ; => [c b a]
  (reverse "hello")             ; => ["o" "l" "l" "e" "h"]
  (reverse [])                  ; => []
  (reverse nil)                 ; => []

Notes:
  - Requires exactly one argument
  - Works with lists, vectors, and strings
  - For strings, returns list of characters in reverse order
  - nil returns empty list
  - Always returns a list (not original collection type)
  - Does not modify the original collection
  - Useful for processing in reverse order
  - Essential for many algorithms and data transformations"""
