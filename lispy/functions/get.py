from lispy.types import Vector, Symbol
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from typing import List, Any


def get_fn(args: List[Any], env: Environment):
    """Accesses an element from a vector or a map.

    Usage: (get collection key [default])
    - collection: The vector or map to access.
    - key: The index (for vectors) or key (for maps).
    - default: (Optional) The value to return if the key/index is not found.
               If not provided, an error is raised for out-of-bounds vector access,
               and nil is returned for a missing map key.
    """
    if not 2 <= len(args) <= 3:
        raise EvaluationError(
            f"SyntaxError: 'get' expects 2 or 3 arguments, got {len(args)}."
        )

    collection, key, *rest = args
    default_value_provided = len(rest) > 0
    default_value = rest[0] if default_value_provided else None

    if isinstance(collection, Vector):
        if not isinstance(key, int):
            raise EvaluationError(
                f"TypeError: Vector index must be an integer, got {type(key)}."
            )
        if 0 <= key < len(collection):
            return collection[key]
        elif default_value_provided:
            return default_value
        else:
            raise EvaluationError(
                f"IndexError: {key} out of bounds for vector of size {len(collection)}."
            )
    elif isinstance(collection, dict):  # Assuming maps are Python dicts
        if not isinstance(key, Symbol):
            raise EvaluationError(
                f"TypeError: Map key must be a symbol, got {type(key)}."
            )

        if key in collection:
            return collection[key]
        elif default_value_provided:
            return default_value
        else:
            return None  # Return nil for missing key if no default
    else:
        raise EvaluationError(
            f"TypeError: 'get' first argument must be a vector or map, got {type(collection)}."
        )


def documentation_get() -> str:
    """Returns documentation for the get function."""
    return """Function: get
Arguments: (get collection key [default])
Description: Retrieves a value from a vector or map by key/index.

Examples:
  (get [10 20 30] 1)           ; => 20
  (get {:a 1 :b 2} ':a)        ; => 1
  (get {:a 1 :b 2} ':c)        ; => nil
  (get {:a 1 :b 2} ':c "not found") ; => "not found"
  (get [10 20] 5)              ; => IndexError (no default)
  (get [10 20] 5 "out of bounds") ; => "out of bounds"

Notes:
  - For vectors: key must be integer index (0-based)
  - For maps: key must be a symbol
  - Returns nil for missing map keys (if no default provided)
  - Throws IndexError for out-of-bounds vector access (if no default)
  - Optional third argument provides default value
  - Works with vectors, maps, and requires 2-3 arguments"""
