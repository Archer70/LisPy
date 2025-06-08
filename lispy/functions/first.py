from lispy.types import LispyList, Vector
from lispy.exceptions import EvaluationError
from ..environment import Environment
from typing import List, Any

EXPECTED_TYPES_MSG = "a list, vector, string, or nil"

def builtin_first(args: List[Any], env: Environment):
    """Implementation of the (first collection) LisPy function.
    Returns the first item of a list, vector, or string. Returns nil for nil or empty collections.
    Usage: (first collection)
    """
    if len(args) != 1:
        raise EvaluationError(f"SyntaxError: 'first' expects 1 argument, got {len(args)}.")

    collection = args[0]

    if collection is None:
        return None
    if isinstance(collection, (LispyList, Vector, str)):
        if not collection: # Empty list, vector, or string
            return None
        return collection[0]
    else:
        raise EvaluationError(f"TypeError: 'first' expects {EXPECTED_TYPES_MSG}, got {type(collection)}.") 