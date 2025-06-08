from typing import List, Any
from ..environment import Environment


def builtin_println(args: List[Any], env: Environment) -> None:
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
