from typing import List, Any
from lispy.environment import Environment
from lispy.types import LispyList
from lispy.functions.decorators import lispy_function, lispy_documentation

@lispy_function("list")
def list_fn(args: List[Any], env: Environment) -> LispyList:
    """Constructs a list from its arguments. (list item1 item2 ...)"""
    # args is already the list of evaluated arguments
    return LispyList(args)  # Return a LispyList instead of regular Python list


@lispy_documentation("list")
def list_doc() -> str:
    """Returns documentation for the list function."""
    return """Function: list
Arguments: (list item1 item2 ...)
Description: Creates a list from zero or more arguments.

Examples:
  (list)                ; => ()
  (list 1 2 3)          ; => (1 2 3)
  (list "a" "b" "c")    ; => ("a" "b" "c")
  (list 1 "hello" true) ; => (1 "hello" true)
  (list (+ 1 2) (* 2 3)); => (3 6)
  (list (list 1 2) 3)   ; => ((1 2) 3)

Notes:
  - Accepts zero or more arguments of any type
  - Arguments are evaluated before list creation
  - Creates mutable lists (can be modified with cons, etc.)
  - Use with car/cdr for list processing
  - Empty list is represented as ()"""
