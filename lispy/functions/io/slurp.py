from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("slurp", web_safe=False)
def slurp_func(args: List[Any], env: Environment) -> str:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'slurp' expects 1 argument, got {len(args)}."
        )

    filepath = args[0]

    # Validate filepath is a string
    if not isinstance(filepath, str):
        raise EvaluationError(
            f"TypeError: 'slurp' expects a string filepath, got {type(filepath).__name__}: '{filepath}'"
        )

    # Read the file
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise EvaluationError(f"FileNotFoundError: File '{filepath}' not found")
    except PermissionError:
        raise EvaluationError(f"PermissionError: Permission denied accessing '{filepath}'")
    except UnicodeDecodeError:
        raise EvaluationError(f"UnicodeDecodeError: Could not decode '{filepath}' as UTF-8")
    except Exception as e:
        raise EvaluationError(f"IOError: Error reading file '{filepath}': {str(e)}")


@lispy_documentation("slurp")
def slurp_documentation() -> str:
    return """Function: slurp
Arguments: (slurp filepath)
Description: Reads the entire contents of a file as a string.

Examples:
  (slurp "config.txt")          ; => "contents of config.txt"
  (slurp "/path/to/file.log")   ; => contents as string
  (slurp "data.json")           ; => JSON file contents
  (slurp "nonexistent.txt")     ; => Error (file not found)

Notes:
  - Requires exactly one argument (filepath as string)
  - Reads entire file into memory as a single string
  - Uses UTF-8 encoding by default
  - Raises error if file doesn't exist or can't be read
  - File path can be relative or absolute
  - **WEB UNSAFE**: Can access arbitrary files on filesystem
  - Useful for configuration files and data loading
  - Complement of the 'spit' function"""
