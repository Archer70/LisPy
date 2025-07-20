# lispy_project/lispy/functions/type_check/is_vector_q.py
from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import Vector


@lispy_function("is-vector?")
def is_vector_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a vector, false otherwise. (is-vector? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-vector?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, Vector)


@lispy_documentation("is-vector?")
def is_vector_q_documentation() -> str:
    """Returns documentation for the is-vector? function."""
    return """Function: is-vector?
Arguments: (is-vector? value)
Description: Tests whether a value is a vector (distinct from lists).

Examples:
  (is-vector? [])           ; => true
  (is-vector? [1 2 3])      ; => true
  (is-vector? (vector 1 2 3)) ; => true
  (is-vector? [1 [2 3] 4])  ; => true
  (is-vector? '(1 2 3))     ; => false (list)
  (is-vector? (list 1 2 3)) ; => false (list)
  (is-vector? "hello")      ; => false
  (is-vector? 42)           ; => false
  (is-vector? nil)          ; => false

Notes:
  - Returns true only for LisPy vectors, not lists
  - Vectors and lists are distinct types in LisPy
  - Empty vector [] returns true
  - Use is-list? to test for lists specifically
  - Vectors provide indexed access and are often more efficient
  - Essential for distinguishing collection types
  - Requires exactly one argument"""
