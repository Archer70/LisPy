from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import Vector
from ..decorators import lispy_function, lispy_documentation


@lispy_function("split")
def split_func(args: List[Any], env: Environment) -> Vector:
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'split' expects 2 arguments, got {len(args)}."
        )

    string_arg, separator_arg = args

    # Validate string is a string
    if not isinstance(string_arg, str):
        raise EvaluationError(
            f"TypeError: First argument to 'split' must be a string, got {type(string_arg).__name__}: '{string_arg}'"
        )

    # Validate separator is a string
    if not isinstance(separator_arg, str):
        raise EvaluationError(
            f"TypeError: Second argument to 'split' must be a string, got {type(separator_arg).__name__}: '{separator_arg}'"
        )

    # Handle empty separator case
    if separator_arg == "":
        raise EvaluationError(
            "ValueError: Separator string cannot be empty"
        )

    # Split the string and return as Vector
    try:
        parts = string_arg.split(separator_arg)
        return Vector(parts)
    except Exception as e:
        raise EvaluationError(f"Error in 'split': {str(e)}")


@lispy_documentation("split")
def split_documentation() -> str:
    return """Function: split
Arguments: (split string separator)
Description: Splits a string into a vector of substrings using a separator.

Examples:
  (split "a,b,c" ",")           ; => ["a" "b" "c"]
  (split "1-2-3" "-")           ; => ["1" "2" "3"]
  (split "hello world" " ")     ; => ["hello" "world"]
  (split "no-separators" ",")   ; => ["no-separators"]
  (split "" ",")                ; => [""]
  (split "a,,b" ",")            ; => ["a" "" "b"]
  (split "start,end," ",")      ; => ["start" "end" ""]

Notes:
  - Requires exactly two arguments: string and separator
  - Both arguments must be strings
  - Separator cannot be an empty string
  - Returns a vector of string parts
  - Empty parts are preserved (e.g., "a,,b" splits to ["a" "" "b"])
  - If separator not found, returns vector with original string
  - Trailing separators create empty trailing parts
  - Useful for parsing delimited data and text processing"""
