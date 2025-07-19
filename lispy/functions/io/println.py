from typing import List, Any
from lispy.environment import Environment
from lispy.functions.decorators import lispy_function, lispy_documentation

@lispy_function("println")
def println(args: List[Any], env: Environment) -> None:
    """Prints values to the console with a newline. (println value1 value2 ...)"""
    if not args:
        # Print just a newline if no arguments
        print()
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

    # Join with spaces and print with newline
    output = " ".join(output_parts)
    print(output)

    return None


@lispy_documentation("println")
def println_documentation() -> str:
    """Returns documentation for the println function."""
    return """Function: println
Arguments: (println value1 value2 ...)
Description: Prints values to console separated by spaces, with a trailing newline.

Examples:
  (println "Hello")                     ; prints: Hello\\n
  (println "Hello" "World")             ; prints: Hello World\\n
  (println "Number:" 42)                ; prints: Number: 42\\n
  (println true false nil)              ; prints: true false nil\\n
  (println [1 2 3])                     ; prints: [1 2 3]\\n
  (println {:a 1})                      ; prints: {:a 1}\\n
  (println)                             ; prints: \\n

Notes:
  - Accepts zero or more arguments
  - Arguments are separated by single spaces
  - Always adds a newline at the end
  - Strings are printed without quotes
  - Booleans printed as "true"/"false", nil as "nil"
  - Always returns nil
  - Empty call prints just a newline
  - Most common print function for line-by-line output"""
