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
        raise EvaluationError(f"SyntaxError: 'hash-map' requires an even number of arguments (key-value pairs), got {len(args)}.")

    new_map = {}
    for i in range(0, len(args), 2):
        key = args[i]
        value = args[i+1]
        if not isinstance(key, Symbol):
            raise EvaluationError(f"TypeError: 'hash-map' keys must be symbols, got {type(key)}.")
        new_map[key] = value
    return new_map 