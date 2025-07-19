from lispy.types import Symbol
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from typing import List, Any


def builtin_hash_map(args: List[Any], env: Environment):
    """Implementation of the (hash-map ...) LisPy function.
    Creates a new map from the evaluated arguments, which are treated as key-value pairs.
    Usage: (hash-map key1 val1 key2 val2 ...)
    """
    if len(args) % 2 != 0:
        raise EvaluationError(
            f"SyntaxError: 'hash-map' requires an even number of arguments (key-value pairs), got {len(args)}."
        )

    new_map = {}
    for i in range(0, len(args), 2):
        key = args[i]
        value = args[i + 1]
        # Keys can be symbols, strings, numbers, booleans, or nil
        if not isinstance(key, (Symbol, str, int, float, bool, type(None))):
            raise EvaluationError(
                f"TypeError: 'hash-map' keys must be symbols, strings, numbers, booleans, or nil, got {type(key)}."
            )
        new_map[key] = value
    return new_map


def documentation_hash_map() -> str:
    """Returns documentation for the hash-map function."""
    return """Function: hash-map
Arguments: (hash-map key1 value1 key2 value2 ...)
Description: Creates a hash map from key-value pairs.

Examples:
  (hash-map)                    ; => {}
  (hash-map ':a 1 ':b 2)        ; => {:a 1 :b 2}
  (hash-map ':name "LisPy" ':version 1.0) ; => {:name "LisPy" :version 1.0}
  (hash-map ':x (+ 1 2) ':y (* 3 4))     ; => {:x 3 :y 12}
  
Notes:
  - Requires an even number of arguments (key-value pairs)
  - Keys must be symbols (like ':a, ':name, etc.)
  - Values can be any type
  - Arguments are evaluated before map creation
  - Returns a new mutable hash map
  - Empty call returns empty map {}"""
