from lispy.types import LispyList, Symbol # Changed List to LispyList
from lispy.exceptions import EvaluationError
from lispy.environment import Environment # Added Environment import
from typing import List, Any # Added typing imports

def builtin_keys(args: List[Any], env: Environment): # Added env parameter and type hint for args
    """Implementation of the (keys map) LisPy function.
    Returns a list of the keys in a map.
    Usage: (keys map)
    """
    if len(args) != 1:
        raise EvaluationError(f"SyntaxError: 'keys' expects 1 argument (a map), got {len(args)}.")

    target_map = args[0]

    if target_map is None:
        return LispyList([]) # Changed List to LispyList
    elif not isinstance(target_map, dict):
        raise EvaluationError(f"TypeError: 'keys' expects a map or nil, got {type(target_map)}.")
    
    # dict.keys() returns a view object, convert it to a list for Lispy
    # The elements are already Symbols as stored in our maps.
    return LispyList(list(target_map.keys())) # Changed List to LispyList 