from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import Vector, Symbol
from ..decorators import lispy_function, lispy_documentation


@lispy_function("to-str")
def to_str(args: List[Any], env: Environment) -> str:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'to-str' expects 1 argument, got {len(args)}."
        )

    arg = args[0]

    # Handle different types appropriately
    if arg is None:
        return "nil"
    elif isinstance(arg, bool):
        return "true" if arg else "false"
    elif isinstance(arg, str):
        return arg  # Already a string
    elif isinstance(arg, (int, float)):
        return str(arg)
    elif isinstance(arg, Symbol):
        return arg.name
    elif isinstance(arg, Vector):
        # Convert vector to string representation
        elements = []
        for element in arg:
            if element is None:
                elements.append("nil")
            elif isinstance(element, bool):
                elements.append("true" if element else "false")
            elif isinstance(element, str):
                elements.append(f'"{element}"')  # Quote strings in vector representation
            else:
                elements.append(str(element))
        return f"[{' '.join(elements)}]"
    elif isinstance(arg, list):
        # Convert list to string representation
        elements = []
        for element in arg:
            if element is None:
                elements.append("nil")
            elif isinstance(element, bool):
                elements.append("true" if element else "false")
            elif isinstance(element, str):
                elements.append(f'"{element}"')  # Quote strings in list representation
            else:
                elements.append(str(element))
        return f"({' '.join(elements)})"
    elif isinstance(arg, dict):
        # Convert map to string representation
        pairs = []
        for key, value in arg.items():
            key_str = str(key) if not isinstance(key, str) else f'"{key}"'
            if value is None:
                value_str = "nil"
            elif isinstance(value, bool):
                value_str = "true" if value else "false"
            elif isinstance(value, str):
                value_str = f'"{value}"'
            else:
                value_str = str(value)
            pairs.append(f"{key_str} {value_str}")
        return f"{{{' '.join(pairs)}}}"
    else:
        # Fall back to Python's string representation
        return str(arg)


@lispy_documentation("to-str")
def to_str_documentation() -> str:
    return """Function: to-str
Arguments: (to-str value)
Description: Converts a value to its string representation.

Examples:
  (to-str 42)                   ; => "42"
  (to-str 3.14)                 ; => "3.14"
  (to-str true)                 ; => "true"
  (to-str false)                ; => "false"
  (to-str nil)                  ; => "nil"
  (to-str "hello")              ; => "hello"
  (to-str [1 2 3])             ; => "[1 2 3]"
  (to-str '(a b c))            ; => "(a b c)"
  (to-str {:a 1 :b 2})         ; => "{:a 1 :b 2}"

Notes:
  - Requires exactly one argument
  - nil becomes "nil"
  - Booleans become "true" or "false"
  - Numbers become their string representation
  - Strings are returned unchanged
  - Collections get formatted with appropriate brackets
  - Essential for output formatting and debugging
  - Part of the type conversion function family (to-str, to-int, to-float, to-bool)"""
