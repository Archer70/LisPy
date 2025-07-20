from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from lispy.functions.decorators import lispy_function, lispy_documentation
from typing import List, Any

@lispy_function("not")
def not_fn(args_list: List[Any], env: Environment) -> bool:
    if len(args_list) != 1:
        raise EvaluationError("TypeError: not requires exactly one argument")
    val = args_list[0]
    # Lisp truthiness: False and None (nil) are false, everything else is true.
    # The not function returns True if the value is falsy, False otherwise.
    is_falsy = val is False or val is None
    return is_falsy  # This was the bug: it should be True if falsy.


@lispy_documentation("not")
def not_documentation() -> str:
    """Returns documentation for the not function."""
    return """Function: not
Arguments: (not value)
Description: Returns the logical negation of a value using LisPy truthiness rules.

Examples:
  (not true)                    ; => false
  (not false)                   ; => true
  (not nil)                     ; => true
  (not 0)                       ; => false (0 is truthy in LisPy)
  (not 1)                       ; => false
  (not "")                      ; => false (empty string is truthy)
  (not [])                      ; => false (empty vector is truthy)
  (not '())                     ; => false (empty list is truthy)

Notes:
  - Requires exactly one argument
  - In LisPy: only false and nil are falsy, everything else is truthy
  - Returns true if argument is false or nil
  - Returns false for all other values (numbers, strings, collections, etc.)
  - Different from many languages where 0, "", [] are falsy
  - Essential for conditional logic and boolean operations
  - Useful for inverting test conditions
  - Follows Lisp/Clojure truthiness conventions"""
