from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import Vector
from ..decorators import lispy_function, lispy_documentation


@lispy_function("conj")
def conj_func(args: List[Any], env: Environment) -> List[Any]:
    if len(args) < 2:
        raise EvaluationError(
            f"SyntaxError: 'conj' expects at least 2 arguments, got {len(args)}."
        )

    collection = args[0]
    elements = args[1:]

    # Handle nil case - treat as empty list
    if collection is None:
        return list(elements)

    # Validate collection type
    if not isinstance(collection, list):
        raise EvaluationError(
            f"TypeError: First argument to 'conj' must be a list or vector, got {type(collection).__name__}: '{collection}'"
        )

    # Create new collection with elements added
    # For lists, add to the front (like Clojure)
    # For vectors, add to the end (like Clojure)
    result = collection.copy()
    
    if isinstance(collection, Vector):
        # Vector - add to end
        result.extend(elements)
    else:
        # List - add to front (in reverse order to maintain proper order)
        for element in reversed(elements):
            result.insert(0, element)

    return result


@lispy_documentation("conj")
def conj_documentation() -> str:
    return """Function: conj
Arguments: (conj collection element1 element2 ...)
Description: Returns a new collection with elements added in the most efficient way.

Examples:
  (conj [1 2 3] 4)              ; => [1 2 3 4] (vector: add to end)
  (conj '(1 2 3) 0)             ; => [0 1 2 3] (list: add to front)
  (conj [1] 2 3 4)              ; => [1 2 3 4] (multiple elements)
  (conj nil 1 2)                ; => [1 2] (nil becomes list)
  (conj [] 1)                   ; => [1]

Notes:
  - Requires at least 2 arguments (collection and one element)
  - For vectors: elements are added to the end
  - For lists: elements are added to the front
  - nil is treated as an empty list
  - Returns a new collection, does not modify original
  - Multiple elements can be added in one call
  - Efficient operation following collection semantics
  - Essential for building collections incrementally"""
