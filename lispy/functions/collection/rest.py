from lispy.types import LispyList, Vector
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from typing import List, Any
from lispy.functions.decorators import lispy_function, lispy_documentation

@lispy_function("rest")
def rest(args: List[Any], env: Environment):
    """Implementation of the (rest coll) LisPy function.
    Returns a new list or vector containing all but the first item.
    Returns an empty collection of the same type if the input is empty or has one element.
    Usage: (rest collection)
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'rest' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    if isinstance(collection, LispyList):
        if len(collection) <= 1:
            return LispyList([])
        else:
            return LispyList(collection[1:])
    elif isinstance(collection, Vector):
        if len(collection) <= 1:
            return Vector([])
        else:
            return Vector(collection[1:])
    elif collection is None:  # (rest nil) should probably return nil or an empty list
        return LispyList(
            []
        )  # Consistent with (first nil) behavior, (rest nil) is '() for Clojure
    else:
        raise EvaluationError(
            f"TypeError: 'rest' expects a list, vector, or nil, got {type(collection)}."
        )  # Updated error message


@lispy_documentation("rest")
def rest_documentation() -> str:
    """Returns documentation for the rest function."""
    return """Function: rest
Arguments: (rest collection)
Description: Returns all elements of a collection except the first.

Examples:
  (rest (list 1 2 3))       ; => (2 3)
  (rest [10 20 30])         ; => [20 30]
  (rest (list 1))           ; => ()
  (rest [77])               ; => []
  (rest (list))             ; => ()
  (rest [])                 ; => []
  (rest nil)                ; => ()

Notes:
  - Requires exactly one argument
  - Works with lists, vectors, and nil (but not strings)
  - Returns same collection type as input
  - Returns empty collection for single-element or empty inputs
  - Alternative to cdr function for lists
  - For nil input, returns empty list
  - Preserves original collection type (list vs vector)"""
