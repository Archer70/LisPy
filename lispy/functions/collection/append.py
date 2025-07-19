from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import Vector
from ..decorators import lispy_function, lispy_documentation


@lispy_function("append")
def append_func(args: List[Any], env: Environment) -> List[Any]:
    if len(args) < 2:
        raise EvaluationError(
            f"SyntaxError: 'append' expects at least 2 arguments, got {len(args)}."
        )

    result = []
    
    for i, arg in enumerate(args):
        if isinstance(arg, list):
            result.extend(arg)
        elif isinstance(arg, str):
            # Treat strings as sequences of characters
            result.extend(list(arg))
        elif arg is None:
            # nil contributes nothing
            continue
        else:
            # Individual elements are appended as-is
            result.append(arg)

    return result


@lispy_documentation("append")
def append_documentation() -> str:
    return """Function: append
Arguments: (append collection1 collection2 ...)
Description: Concatenates multiple collections into a single list.

Examples:
  (append [1 2] [3 4])          ; => [1 2 3 4]
  (append '(a b) '(c d))        ; => [a b c d]
  (append [1] [2] [3])          ; => [1 2 3]
  (append [1 2] 3 [4 5])        ; => [1 2 3 4 5]
  (append "hello" " " "world")  ; => ["h" "e" "l" "l" "o" " " "w" "o" "r" "l" "d"]
  (append [] [1 2])             ; => [1 2]
  (append [1 2] nil [3])        ; => [1 2 3]

Notes:
  - Requires at least two arguments
  - Collections are flattened into the result
  - Individual elements are added as single items
  - Strings are treated as sequences of characters
  - nil arguments are ignored
  - Always returns a list
  - Useful for building larger collections from smaller ones"""
