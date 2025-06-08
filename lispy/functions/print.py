from typing import List, Any
import sys
from ..environment import Environment

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