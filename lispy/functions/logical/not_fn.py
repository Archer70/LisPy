from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("not")
def not_func(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError("TypeError: not requires exactly one argument")

    arg = args[0]
    
    # Handle nil and false as falsy
    if arg is None or arg is False:
        return True
    
    # Everything else is truthy
    return False


@lispy_documentation("not")
def not_documentation() -> str:
    return """Function: not
Arguments: (not value)
Description: Returns the logical negation of a value.

Examples:
  (not true)        ; => false
  (not false)       ; => true
  (not nil)         ; => true
  (not 0)           ; => false (0 is truthy)
  (not "")          ; => false (empty string is truthy)
  (not [])          ; => false (empty vector is truthy)
  (not 42)          ; => false (numbers are truthy)

Notes:
  - Only nil and false are considered falsy
  - All other values (including 0, empty strings, empty collections) are truthy
  - This follows Lisp conventions rather than many other languages
  - Useful for conditional logic and boolean operations
  - Requires exactly one argument"""
