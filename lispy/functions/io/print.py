from typing import List, Any
import sys
from lispy.environment import Environment


def builtin_print(args: List[Any], env: Environment) -> None:
    """Prints values to the console without a newline. (print value1 value2 ...)"""
    if not args:
        # Print nothing if no arguments
        return None

    # Convert each argument to string and print
    output_parts = []
    for arg in args:
        if isinstance(arg, str):
            # Print strings without quotes
            output_parts.append(arg)
        elif arg is None:
            output_parts.append("nil")
        elif isinstance(arg, bool):
            # Print booleans as lowercase
            output_parts.append("true" if arg else "false")
        else:
            # Use string representation for other types
            output_parts.append(str(arg))

    # Join with spaces and print without newline
    output = " ".join(output_parts)
    print(output, end="")
    sys.stdout.flush()  # Ensure immediate output

    return None


def documentation_print() -> str:
    """Returns documentation for the print function."""
    return """Function: print
Arguments: (print value1 value2 ...)
Description: Prints values to console separated by spaces, without a trailing newline.

Examples:
  (print "Hello")                       ; prints: Hello
  (print "Hello" "World")               ; prints: Hello World
  (print "Number:" 42)                  ; prints: Number: 42
  (print true false nil)                ; prints: true false nil
  (print [1 2 3])                       ; prints: [1 2 3]
  (print {:a 1})                        ; prints: {:a 1}
  (print)                               ; prints nothing

Notes:
  - Accepts zero or more arguments
  - Arguments are separated by single spaces
  - No newline is added at the end (use println for newlines)
  - Strings are printed without quotes
  - Booleans printed as "true"/"false", nil as "nil"
  - Always returns nil
  - Output is immediately flushed to console
  - Useful for building output on same line"""
