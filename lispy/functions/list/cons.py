from typing import List, Any
from lispy.exceptions import EvaluationError
from lispy.environment import Environment


def builtin_cons(args: List[Any], env: Environment) -> List[Any]:
    """Prepends an item to a list. (cons item list)"""
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'cons' expects 2 arguments (item list), got {len(args)}."
        )

    item = args[0]
    list_arg = args[1]

    if not isinstance(list_arg, list):
        raise EvaluationError(
            f"TypeError: 'cons' expects its second argument to be a list, got {type(list_arg).__name__}."
        )

    return [item] + list_arg


def documentation_cons() -> str:
    """Returns documentation for the cons function."""
    return """Function: cons
Arguments: (cons item list)
Description: Prepends an item to the front of a list, creating a new list.

Examples:
  (cons 1 (list 2 3))       ; => (1 2 3)
  (cons 1 (list))           ; => (1)
  (cons (list 1 2) (list 3 4))  ; => ((1 2) 3 4)
  (cons "a" (list "b" "c")) ; => ("a" "b" "c")
  (cons 0 [1 2 3])          ; => (0 1 2 3)

Notes:
  - Classic Lisp construct operation
  - Requires exactly two arguments
  - First argument can be any type
  - Second argument must be a list
  - Creates a new list without modifying the original
  - Use with car/cdr for list processing patterns"""
