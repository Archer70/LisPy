# lispy_project/lispy/functions/type_check/is_vector_q.py
from typing import List, Any
from ...types import Vector
from ...exceptions import EvaluationError
from ...environment import Environment


def builtin_is_vector_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a vector, false otherwise. (is_vector? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_vector?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, Vector)


def documentation_is_vector_q() -> str:
    """Returns documentation for the is_vector? function."""
    return """Function: is_vector?
Arguments: (is_vector? value)
Description: Tests whether a value is a vector (distinct from lists).

Examples:
  (is_vector? [])           ; => true
  (is_vector? [1 2 3])      ; => true
  (is_vector? (vector 1 2 3)) ; => true
  (is_vector? [1 [2 3] 4])  ; => true
  (is_vector? '(1 2 3))     ; => false (list)
  (is_vector? (list 1 2 3)) ; => false (list)
  (is_vector? "hello")      ; => false
  (is_vector? 42)           ; => false
  (is_vector? nil)          ; => false

Notes:
  - Returns true only for LisPy vectors, not lists
  - Vectors and lists are distinct types in LisPy
  - Empty vector [] returns true
  - Use is_list? to test for lists specifically
  - Vectors provide indexed access and are often more efficient
  - Essential for distinguishing collection types
  - Requires exactly one argument"""
