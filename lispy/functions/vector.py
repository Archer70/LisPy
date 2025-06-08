from lispy.types import Vector
from ..environment import Environment
from typing import List, Any
# No EvaluationError needed here as (vector ...) doesn't have argument count restrictions
# or specific type restrictions for its elements beyond what the evaluator provides.


def builtin_vector(args: List[Any], env: Environment):
    """Implementation of the (vector ...) LisPy function.
    Creates a new vector containing the evaluated arguments.
    Usage: (vector item1 item2 ...)
    """
    # The arguments in 'args' are already evaluated by the evaluator
    # before being passed to a built-in function.
    return Vector(list(args))  # Convert tuple of args to list, then to Vector


def documentation_vector() -> str:
    """Returns documentation for the vector function."""
    return """Function: vector
Arguments: (vector item1 item2 ...)
Description: Creates a new vector containing the provided arguments as elements.

Examples:
  (vector)                      ; => []
  (vector 1 2 3)                ; => [1 2 3]
  (vector "a" "b" "c")          ; => ["a" "b" "c"]
  (vector 1 "hello" true nil)   ; => [1 "hello" true nil]
  (vector (+ 1 2) (* 3 4))      ; => [3 12] (arguments evaluated)
  (vector [1 2] [3 4])          ; => [[1 2] [3 4]] (nested vectors)
  (vector 'symbol :keyword)     ; => [symbol :keyword]

Notes:
  - Accepts zero or more arguments of any type
  - Arguments are evaluated before being added to vector
  - Creates indexed, ordered collection (unlike lists)
  - Vectors support efficient random access via nth
  - Empty call creates empty vector []
  - Vectors can contain mixed types and nested structures
  - Immutable: once created, cannot be modified directly"""
