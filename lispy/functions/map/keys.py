from typing import Any, List  # Added typing imports

from lispy.environment import Environment  # Added Environment import
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import LispyList  # Changed List to LispyList


@lispy_function("keys")
def keys(
    args: List[Any], env: Environment
):  # Added env parameter and type hint for args
    """Implementation of the (keys map) LisPy function.
    Returns a list of the keys in a map.
    Usage: (keys map)
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'keys' expects 1 argument (a map), got {len(args)}."
        )

    target_map = args[0]

    if target_map is None:
        return LispyList([])  # Changed List to LispyList
    elif not isinstance(target_map, dict):
        raise EvaluationError(
            f"TypeError: 'keys' expects a map or nil, got {type(target_map)}."
        )

    # dict.keys() returns a view object, convert it to a list for Lispy
    # The elements are already Symbols as stored in our maps.
    return LispyList(list(target_map.keys()))  # Changed List to LispyList


@lispy_documentation("keys")
def keys_doc() -> str:
    """Returns documentation for the keys function."""
    return """Function: keys
Arguments: (keys map)
Description: Returns a list of all keys in a map.

Examples:
  (keys {:a 1 :b 2 :c 3})       ; => (:a :b :c) (order may vary)
  (keys {})                     ; => ()
  (keys nil)                    ; => ()
  (keys {:name "LisPy" :version 1.0}) ; => (:name :version)

Notes:
  - Requires exactly one argument
  - Argument must be a map or nil
  - nil is treated as empty map, returns empty list
  - Returns a LisPy list of symbol keys
  - Key order in result is not guaranteed
  - For empty maps, returns empty list ()
  - Keys are always symbols in LisPy maps"""
