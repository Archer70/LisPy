# lispy_project/lispy/functions/type_check/is_list_q.py
from typing import List, Any
from ...types import LispyList
from ...exceptions import EvaluationError
from ...environment import Environment


def builtin_is_list_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a list, false otherwise. (is-list? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-list?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, LispyList)


def documentation_is_list_q() -> str:
    """Returns documentation for the is-list? function."""
    return """Function: is-list?
Arguments: (is-list? value)
Description: Tests whether a value is a list (distinct from vectors).

Examples:
  (is-list? '())            ; => true
  (is-list? '(1 2 3))       ; => true
  (is-list? (list 1 2 3))   ; => true
  (is-list? '(1 (2 3) 4))   ; => true
  (is-list? [1 2 3])        ; => false (vector)
  (is-list? (vector 1 2 3)) ; => false (vector)
  (is-list? "hello")        ; => false
  (is-list? 42)             ; => false
  (is-list? nil)            ; => false

Notes:
  - Returns true only for LisPy lists, not vectors
  - Lists and vectors are distinct types in LisPy
  - Empty list '() returns true
  - Use is-vector? to test for vectors specifically
  - Essential for distinguishing collection types
  - Requires exactly one argument"""
