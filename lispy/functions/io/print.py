from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("print")
def print_func(args: List[Any], env: Environment) -> None:
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
    
    # Print without trailing newline
    print(" ".join(output_parts), end="")
    return None


@lispy_documentation("print")
def print_documentation() -> str:
    return """Function: print
Arguments: (print value1 value2 ...)
Description: Prints values to standard output without a trailing newline.

Examples:
  (print "Hello")               ; prints "Hello" (no newline)
  (print "Hello" "World")       ; prints "Hello World"
  (print 42)                    ; prints "42"
  (print true false nil)        ; prints "true false nil"
  (print)                       ; prints nothing (empty line)

Notes:
  - Accepts zero or more arguments
  - Values are separated by spaces when printed
  - No trailing newline is added (use println for newline)
  - nil becomes "nil", booleans become "true"/"false"
  - All other values converted to strings
  - Returns nil (used for side effect)
  - Essential for output and debugging
  - Safe for web environments (output only)"""
