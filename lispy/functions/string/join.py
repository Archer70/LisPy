from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("join")
def join_func(args: List[Any], env: Environment) -> str:
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'join' expects 2 arguments, got {len(args)}."
        )

    collection_arg, separator_arg = args

    # Validate separator is a string
    if not isinstance(separator_arg, str):
        raise EvaluationError(
            f"TypeError: Second argument to 'join' must be a string, got {type(separator_arg).__name__}: '{separator_arg}'"
        )

    # Validate collection is a list or vector
    if not isinstance(collection_arg, list):
        raise EvaluationError(
            f"TypeError: First argument to 'join' must be a list or vector, got {type(collection_arg).__name__}: '{collection_arg}'"
        )

    # Convert all elements to strings and join
    try:
        string_elements = []
        for i, element in enumerate(collection_arg):
            if element is None:
                string_elements.append("nil")
            elif isinstance(element, bool):
                string_elements.append("true" if element else "false")
            else:
                string_elements.append(str(element))
        
        return separator_arg.join(string_elements)
    except Exception as e:
        raise EvaluationError(f"Error in 'join': {str(e)}")


@lispy_documentation("join")
def join_documentation() -> str:
    return """Function: join
Arguments: (join collection separator)
Description: Joins elements of a collection into a string using a separator.

Examples:
  (join ["a" "b" "c"] ", ")     ; => "a, b, c"
  (join [1 2 3] "-")            ; => "1-2-3"
  (join ["hello" "world"] " ")  ; => "hello world"
  (join [] ", ")                ; => ""
  (join ["single"] ", ")        ; => "single"
  (join [true false nil] "|")   ; => "true|false|nil"
  (join '(1 2 3) ":")          ; => "1:2:3"

Notes:
  - Requires exactly two arguments: collection and separator
  - Collection must be a list or vector
  - Separator must be a string
  - All elements are converted to strings automatically
  - nil becomes "nil", true becomes "true", false becomes "false"
  - Empty collections return empty string
  - Useful for formatting output and data serialization"""
