from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("spit", web_safe=False, reason="Writes files to filesystem")
def spit_func(args: List[Any], env: Environment) -> None:
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'spit' expects 2 arguments, got {len(args)}."
        )

    filepath, content = args

    # Validate filepath is a string
    if not isinstance(filepath, str):
        raise EvaluationError(
            f"TypeError: First argument to 'spit' must be a string filepath, got {type(filepath).__name__}: '{filepath}'"
        )

    # Convert content to string
    if content is None:
        content_str = "nil"
    elif isinstance(content, bool):
        content_str = "true" if content else "false"
    elif isinstance(content, str):
        content_str = content
    else:
        content_str = str(content)

    # Write to file
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content_str)
        return None
    except PermissionError:
        raise EvaluationError(f"PermissionError: Permission denied writing to '{filepath}'")
    except IsADirectoryError:
        raise EvaluationError(f"IsADirectoryError: '{filepath}' is a directory, not a file")
    except Exception as e:
        raise EvaluationError(f"IOError: Error writing to file '{filepath}': {str(e)}")


@lispy_documentation("spit")
def spit_documentation() -> str:
    return """Function: spit
Arguments: (spit filepath content)
Description: Writes content to a file, creating or overwriting it.

Examples:
  (spit "output.txt" "Hello World")     ; writes "Hello World" to file
  (spit "data.log" "Log entry\\n")      ; writes log entry
  (spit "config.json" "{}")            ; writes empty JSON object
  (spit "numbers.txt" 42)              ; writes "42" to file
  (spit "values.txt" nil)              ; writes "nil" to file

Notes:
  - Requires exactly two arguments (filepath and content)
  - Filepath must be a string
  - Content is converted to string before writing
  - nil becomes "nil", booleans become "true"/"false"
  - Creates file if it doesn't exist
  - Overwrites existing file completely
  - Uses UTF-8 encoding
  - **WEB UNSAFE**: Can write arbitrary files to filesystem
  - Raises error if file can't be written (permissions, etc.)
  - Returns nil (used for side effect)
  - Complement of the 'slurp' function"""
