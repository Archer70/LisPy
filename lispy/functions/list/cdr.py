from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function


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
Description: Returns all elements of a list except the first (the tail).

Examples:
  (cdr (list 1 2 3))    ; => (2 3)
  (cdr '(a b c))        ; => (b c)
  (cdr (list "x" "y"))  ; => ("y")
  (cdr (list 10))       ; => ()
  (cdr '(1 2 3 4))      ; => (2 3 4)

Notes:
  - Returns the tail of the list (everything except the first element)
  - Cannot operate on empty lists - raises an error
  - Classic Lisp function name (Contents of Decrement Register)
  - For a single-element list, returns an empty list
  - Use with 'car' to process lists recursively
  - Expects exactly one argument which must be a non-empty list"""
