from lispy.types import LispyList
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from typing import List, Any

def builtin_vals(args: List[Any], env: Environment):
    """Implementation of the (vals map) LisPy function.
    Returns a list of the values in a map.
    Usage: (vals map)
    """
    if len(args) != 1:
        raise EvaluationError(f"SyntaxError: 'vals' expects 1 argument (a map), got {len(args)}.")

    target_map = args[0]

    if target_map is None:
        return LispyList([])  # Vals of nil is an empty list
    elif not isinstance(target_map, dict):
        raise EvaluationError(f"TypeError: 'vals' expects a map or nil, got {type(target_map)}.")
    
    # dict.values() returns a view object, convert it to a list for Lispy
    return LispyList(list(target_map.values())) 