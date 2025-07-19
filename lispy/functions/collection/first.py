from typing import List, Any, Optional
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("first")
def first_func(args: List[Any], env: Environment) -> Any:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'first' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Handle nil case
    if collection is None:
        return None

    # Handle different collection types
    if isinstance(collection, list):
        return collection[0] if collection else None
    elif isinstance(collection, str):
        return collection[0] if collection else None
    else:
        raise EvaluationError(
            f"TypeError: 'first' expects a list, vector, or string, got {type(collection).__name__}: '{collection}'"
        )


@lispy_documentation("first")
def first_documentation() -> str:
    return """Function: first
Arguments: (first collection)
Description: Returns the first element of a collection.

Examples:
  (first [1 2 3])               ; => 1
  (first '(a b c))              ; => a
  (first "hello")               ; => "h"
  (first [])                    ; => nil
  (first nil)                   ; => nil

Notes:
  - Requires exactly one argument
  - Works with lists, vectors, and strings
  - Returns nil for empty collections or nil input
  - For strings, returns the first character as a string
  - Essential for list processing and iteration
  - Complement of the 'rest' function"""
