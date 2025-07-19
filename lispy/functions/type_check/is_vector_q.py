# lispy_project/lispy/functions/type_check/is_vector_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import Vector
from ..decorators import lispy_function, lispy_documentation


@lispy_function("is-vector?")
def is_vector(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-vector?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, Vector)


@lispy_documentation("is-vector?")
def is_vector_documentation() -> str:
    return """Function: is-vector?
Arguments: (is-vector? value)
Description: Tests whether a value is a vector.

Examples:
  (is-vector? [1 2 3])      ; => true
  (is-vector? [])           ; => true (empty vector)
  (is-vector? (vector 1 2)) ; => true
  (is-vector? '(1 2 3))     ; => false (list)
  (is-vector? 42)           ; => false (number)
  (is-vector? "hello")      ; => false (string)
  (is-vector? nil)          ; => false
  (is-vector? {:a 1})       ; => false (map)

Notes:
  - Returns true only for vector values (indexed arrays)
  - Different from lists, which use parentheses with quote
  - Vectors are created with square brackets [] or (vector ...)
  - Useful for distinguishing between vector and list collections
  - Requires exactly one argument"""
