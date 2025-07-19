from typing import List, Any
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("cdr")
def cdr(args: List[Any], env: Environment) -> List[Any]:
    """Returns all but the first element of a list. (cdr list)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'cdr' expects 1 argument (a list), got {len(args)}."
        )

    list_arg = args[0]

    if not isinstance(list_arg, list):
        raise EvaluationError(
            f"TypeError: 'cdr' expects its argument to be a list, got {type(list_arg).__name__}."
        )

    if not list_arg:  # Empty list
        raise EvaluationError("RuntimeError: 'cdr' cannot operate on an empty list.")

    return list_arg[1:]


@lispy_documentation("cdr")
def cdr_doc() -> str:
    """Returns documentation for the cdr function."""
    return """Function: cdr
Arguments: (cdr list)
Description: Returns all but the first element of a list (the "rest" of the list).

Examples:
  (cdr (list 1 2 3))    ; => (2 3)
  (cdr '(a b c))        ; => (b c)
  (cdr (list "x" "y"))  ; => ("y")
  (cdr (list 1))        ; => ()

Notes:
  - Returns the tail of the list (all elements except the first)
  - Cannot operate on empty lists - raises an error
  - Classic Lisp function name (Contents of Decrement Register)
  - Expects exactly one argument which must be a non-empty list
  - Use with 'car' to process lists recursively
  - Result is always a list (may be empty if input had only one element)"""
