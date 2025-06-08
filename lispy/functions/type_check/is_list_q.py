# lispy_project/lispy/functions/type_check/is_list_q.py
from typing import List, Any
from ...types import LispyList
from ...exceptions import EvaluationError
from ...environment import Environment


def builtin_is_list_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a list, false otherwise. (is_list? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_list?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, LispyList)


def documentation_is_list_q() -> str:
    """Returns documentation for the is_list? function."""
    return """Function: is_list?
Arguments: (is_list? value)
Description: Tests whether a value is a list (distinct from vectors).

Examples:
  (is_list? '())            ; => true
  (is_list? '(1 2 3))       ; => true
  (is_list? (list 1 2 3))   ; => true
  (is_list? '(1 (2 3) 4))   ; => true
  (is_list? [1 2 3])        ; => false (vector)
  (is_list? (vector 1 2 3)) ; => false (vector)
  (is_list? "hello")        ; => false
  (is_list? 42)             ; => false
  (is_list? nil)            ; => false

Notes:
  - Returns true only for LisPy lists, not vectors
  - Lists and vectors are distinct types in LisPy
  - Empty list '() returns true
  - Use is_vector? to test for vectors specifically
  - Essential for distinguishing collection types
  - Requires exactly one argument""" 