# lispy_project/lispy/functions/type_check/is_list_q.py
from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import LispyList
from ..decorators import lispy_function, lispy_documentation


@lispy_function("is-list?")
def is_list(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-list?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, LispyList)


@lispy_documentation("is-list?")
def is_list_documentation() -> str:
    return """Function: is-list?
Arguments: (is-list? value)
Description: Tests whether a value is a list.

Examples:
  (is-list? '(1 2 3))       ; => true
  (is-list? '())            ; => true (empty list)
  (is-list? (list 1 2 3))   ; => true
  (is-list? [1 2 3])        ; => false (vector)
  (is-list? 42)             ; => false (number)
  (is-list? "hello")        ; => false (string)
  (is-list? nil)            ; => false
  (is-list? {:a 1})         ; => false (map)

Notes:
  - Returns true only for list values (linked lists)
  - Different from vectors, which use square brackets
  - Lists are created with quote syntax '() or (list ...)
  - Useful for distinguishing between list and vector collections
  - Requires exactly one argument"""
