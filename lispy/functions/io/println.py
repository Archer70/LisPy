from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("println")
def println_func(args: List[Any], env: Environment) -> None:
    if len(args) == 0:
        print()
        return None

    # Convert all arguments to strings and print them
    output_parts = []
    for arg in args:
        if arg is None:
            output_parts.append("nil")
        elif isinstance(arg, bool):
            output_parts.append("true" if arg else "false")
        elif isinstance(arg, str):
            output_parts.append(arg)
        else:
            output_parts.append(str(arg))
    
    # Print with trailing newline
    print(" ".join(output_parts))
    return None


@lispy_documentation("println")
def println_documentation() -> str:
    return """Function: println
Arguments: (println value1 value2 ...)
Description: Prints values to standard output with a trailing newline.

Examples:
  (println "Hello")             ; prints "Hello" then newline
  (println "Hello" "World")     ; prints "Hello World" then newline
  (println 42)                  ; prints "42" then newline
  (println true false nil)      ; prints "true false nil" then newline
  (println)                     ; prints just a newline

Notes:
  - Accepts zero or more arguments
  - Values are separated by spaces when printed
  - Always adds a trailing newline (use print to avoid newline)
  - nil becomes "nil", booleans become "true"/"false"
  - All other values converted to strings
  - Returns nil (used for side effect)
  - Essential for output and debugging
  - Safe for web environments (output only)"""
