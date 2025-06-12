from typing import List, Any
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
import os


def builtin_slurp(args: List[Any], env: Environment) -> str:
    """Reads the entire contents of a file as a string. (slurp filename)"""
    if len(args) != 1:
        raise EvaluationError(
            "SyntaxError: 'slurp' expects 1 argument (filename), got {}.".format(
                len(args)
            )
        )

    filename_arg = args[0]
    if not isinstance(filename_arg, str):
        raise EvaluationError(
            "TypeError: 'slurp' filename must be a string, got {}.".format(
                type(filename_arg).__name__
            )
        )

    filename = filename_arg

    try:
        # Check if file exists
        if not os.path.exists(filename):
            raise EvaluationError(
                "FileNotFoundError: File '{}' does not exist.".format(filename)
            )

        # Check if it's actually a file (not a directory)
        if not os.path.isfile(filename):
            raise EvaluationError(
                "FileError: '{}' is not a regular file.".format(filename)
            )

        # Read the file contents
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    except PermissionError:
        raise EvaluationError(
            "PermissionError: Permission denied reading file '{}'.".format(filename)
        )
    except UnicodeDecodeError as e:
        raise EvaluationError(
            "UnicodeError: Cannot decode file '{}' as UTF-8: {}.".format(
                filename, str(e)
            )
        )
    except OSError as e:
        raise EvaluationError(
            "OSError: Error reading file '{}': {}.".format(filename, str(e))
        )
    except Exception as e:
        raise EvaluationError(
            "Error: Unexpected error reading file '{}': {}.".format(filename, str(e))
        )


def documentation_slurp() -> str:
    """Returns documentation for the slurp function."""
    return """Function: slurp
Arguments: (slurp filename)
Description: Reads the entire contents of a file as a string.

Examples:
  (slurp "config.txt")                  ; => "file contents as string"
  (slurp "data/input.csv")              ; => "csv,data,here\\nrow2,data2,here"
  (slurp "README.md")                   ; => "# Project Title\\n\\nDescription..."
  
  ; Using with other functions:
  (count (slurp "data.txt"))            ; => character count of file
  (split (slurp "lines.txt") "\\n")     ; => vector of lines
  (println (slurp "message.txt"))       ; => print file contents

Notes:
  - Requires exactly one argument (the filename as a string)
  - Returns the entire file contents as a single string
  - Preserves all whitespace, newlines, and formatting
  - Uses UTF-8 encoding by default
  - Throws descriptive errors for common issues:
    * File not found
    * Permission denied
    * Not a regular file (e.g., directory)
    * Unicode decode errors
  - Relative paths are resolved from current working directory
  - Essential for file processing and configuration reading
  - Pairs well with split function for line-by-line processing
  - Memory usage scales with file size (entire file loaded at once)"""
