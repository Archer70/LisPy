from lispy.types import Symbol
from lispy.exceptions import EvaluationError
from ..environment import Environment
from typing import List, Any


def builtin_assoc(args: List[Any], env: Environment):
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

        if not isinstance(key, Symbol):
            raise EvaluationError(
                f"TypeError: Map keys in 'assoc' must be symbols, got {type(key)}."
            )

        new_map[key] = value

    return new_map
