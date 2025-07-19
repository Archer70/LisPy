from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("to-bool")
def to_bool(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'to-bool' expects 1 argument, got {len(args)}."
        )

    arg = args[0]

    # Follow LisPy truthiness rules: only nil and false are falsy
    if arg is None or arg is False:
        return False
    else:
        return True


@lispy_documentation("to-bool")
def to_bool_documentation() -> str:
    return """Function: to-bool
Arguments: (to-bool value)
Description: Converts a value to a boolean using LisPy truthiness rules.

Examples:
  (to-bool true)                ; => true
  (to-bool false)               ; => false
  (to-bool nil)                 ; => false
  (to-bool 0)                   ; => true (0 is truthy in LisPy)
  (to-bool "")                  ; => true (empty string is truthy)
  (to-bool [])                  ; => true (empty vector is truthy)
  (to-bool 42)                  ; => true
  (to-bool "hello")             ; => true

Notes:
  - Requires exactly one argument
  - Follows LisPy truthiness: only nil and false are falsy
  - All other values (including 0, empty strings, empty collections) are truthy
  - Different from many languages where 0 and empty values are falsy
  - Part of the type conversion function family (to-str, to-int, to-float, to-bool)""" 