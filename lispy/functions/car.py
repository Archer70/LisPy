from typing import List, Any
from ..exceptions import EvaluationError
from ..environment import Environment


def builtin_car(args: List[Any], env: Environment) -> Any:
    """Returns the first element of a list. (car list)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'car' expects 1 argument (a list), got {len(args)}."
        )

    list_arg = args[0]

    if not isinstance(list_arg, list):
        raise EvaluationError(
            f"TypeError: 'car' expects its argument to be a list, got {type(list_arg).__name__}."
        )

    if not list_arg:  # Empty list
        raise EvaluationError("RuntimeError: 'car' cannot operate on an empty list.")

    return list_arg[0]


def documentation_car() -> str:
    """Returns documentation for the car function."""
    return """Function: car
Arguments: (car list)
Description: Returns the first element of a list.

Examples:
  (car (list 1 2 3))    ; => 1
  (car '(a b c))        ; => a
  (car (list "x" "y"))  ; => "x"
  (car (list (list 1 2) 3))  ; => (1 2)

Notes:
  - Returns the first element (head) of the list
  - Cannot operate on empty lists - raises an error
  - Classic Lisp function name (Contents of Address Register)
  - Expects exactly one argument which must be a non-empty list
  - Use with 'cdr' to process lists recursively"""
