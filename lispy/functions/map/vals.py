from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import LispyList


@lispy_function("vals")
def vals(args: List[Any], env: Environment):
    """Implementation of the (vals map) LisPy function.
    Returns a list of the values in a map.
    Usage: (vals map)
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'vals' expects 1 argument (a map), got {len(args)}."
        )

    target_map = args[0]

    if target_map is None:
        return LispyList([])  # Vals of nil is an empty list
    elif not isinstance(target_map, dict):
        raise EvaluationError(
            f"TypeError: 'vals' expects a map or nil, got {type(target_map)}."
        )

    # dict.values() returns a view object, convert it to a list for Lispy
    return LispyList(list(target_map.values()))


@lispy_documentation("vals")
def vals_doc() -> str:
    """Returns documentation for the vals function."""
    return """Function: vals
Arguments: (vals map)
Description: Returns a list of all values in a map.

Examples:
  (vals {:a 1 :b 2 :c 3})       ; => (1 2 3) (order may vary)
  (vals {})                     ; => ()
  (vals nil)                    ; => ()
  (vals {:name "LisPy" :version 1.0}) ; => ("LisPy" 1.0)

Notes:
  - Requires exactly one argument
  - Argument must be a map or nil
  - nil is treated as empty map, returns empty list
  - Returns a LisPy list of values
  - Value order in result is not guaranteed
  - For empty maps, returns empty list ()
  - Values can be any type (numbers, strings, lists, etc.)"""
