from lispy.types import Symbol
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from ..decorators import lispy_function, lispy_documentation
from typing import List, Any


@lispy_function("assoc")
def assoc(args: List[Any], env: Environment):
    """Implementation of the (assoc map key val ...) LisPy function.
    Associates key-value pairs with a map, returning a new map.
    Usage: (assoc map key1 value1 [key2 value2 ...])
    """
    if len(args) < 3:
        raise EvaluationError(
            f"SyntaxError: 'assoc' expects at least 3 arguments (map, key, value), got {len(args)}."
        )

    original_map = args[0]
    kv_pairs = args[1:]

    if len(kv_pairs) % 2 != 0:
        raise EvaluationError(
            f"SyntaxError: 'assoc' requires an even number of key/value arguments after the map, got {len(kv_pairs)}."
        )

    if not (isinstance(original_map, dict) or original_map is None):
        raise EvaluationError(
            f"TypeError: First argument to 'assoc' must be a map or nil, got {type(original_map)}."
        )

    # Create a new map based on the original, or an empty map if original_map is None
    new_map = dict(original_map) if original_map is not None else {}

    for i in range(0, len(kv_pairs), 2):
        key = kv_pairs[i]
        value = kv_pairs[i + 1]

        # Keys can be symbols, strings, numbers, booleans, or nil
        if not isinstance(key, (Symbol, str, int, float, bool, type(None))):
            raise EvaluationError(
                f"TypeError: Map keys in 'assoc' must be symbols, strings, numbers, booleans, or nil, got {type(key)}."
            )

        new_map[key] = value

    return new_map


@lispy_documentation("assoc")
def assoc_doc() -> str:
    """Returns documentation for the assoc function."""
    return """Function: assoc
Arguments: (assoc map key1 value1 [key2 value2 ...])
Description: Associates key-value pairs with a map, returning a new map.

Examples:
  (assoc {} ':a 1)              ; => {:a 1}
  (assoc {:a 1} ':b 2)          ; => {:a 1 :b 2}
  (assoc {:a 1} ':a 10)         ; => {:a 10} (updates existing)
  (assoc {} ':x 1 ':y 2 ':z 3)  ; => {:x 1 :y 2 :z 3}
  (assoc nil ':a 1)             ; => {:a 1} (nil treated as empty map)

Notes:
  - First argument must be a map or nil
  - Requires at least 3 arguments (map, key, value)
  - Additional key-value pairs can be provided
  - Keys must be symbols (like ':a, ':name, etc.)
  - Values can be any type
  - Returns a new map, does not modify original
  - Later keys override earlier keys in same call"""
