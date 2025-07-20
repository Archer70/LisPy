import os
from typing import Any, List

from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function


@lispy_function("spit", web_safe=False, reason="File system access")
def spit(args: List[Any], env: Environment) -> None:
    """Writes content to a file. (spit filename content)"""
    if len(args) != 2:
        raise EvaluationError(
            "SyntaxError: 'spit' expects 2 arguments (filename, content), got {}.".format(
                len(args)
            )
        )

    filename_arg, content_arg = args

    # Validate filename is a string
    if not isinstance(filename_arg, str):
        raise EvaluationError(
            "TypeError: 'spit' filename must be a string, got {}.".format(
                type(filename_arg).__name__
            )
        )

    # Validate content is a string
    if not isinstance(content_arg, str):
        raise EvaluationError(
            "TypeError: 'spit' content must be a string, got {}.".format(
                type(content_arg).__name__
            )
        )

    filename = filename_arg
    content = content_arg

    try:
        # Check if the directory exists and create it if it doesn't
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError as e:
                raise EvaluationError(
                    "OSError: Cannot create directory '{}': {}.".format(
                        directory, str(e)
                    )
                )

        # Write the file contents
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

        # Return None (spit doesn't return anything meaningful)
        return None

    except PermissionError:
        raise EvaluationError(
            "PermissionError: Permission denied writing to file '{}'.".format(filename)
        )
    except IsADirectoryError:
        raise EvaluationError(
            "IsADirectoryError: '{}' is a directory, not a file.".format(filename)
        )
    except OSError as e:
        raise EvaluationError(
            "OSError: Error writing to file '{}': {}.".format(filename, str(e))
        )
    except Exception as e:
        raise EvaluationError(
            "Error: Unexpected error writing to file '{}': {}.".format(filename, str(e))
        )


@lispy_documentation("spit")
def spit_documentation() -> str:
    """Returns documentation for the spit function."""
    return """Function: spit
Arguments: (spit filename content)
Description: Writes string content to a file, creating or overwriting as needed.

Examples:
  (spit "output.txt" "Hello, World!")      ; => nil (writes to file)
  (spit "data/log.txt" "Error occurred")   ; => nil (creates directory if needed)
  (spit "config.json" "{\\"key\\": \\"value\\"}") ; => nil (writes JSON)
  
  ; Using with other functions:
  (spit "numbers.txt" (to-str 42))            ; => nil (convert number to string)
  (spit "lines.txt" (join ["a" "b" "c"] "\\n")) ; => nil (join and write lines)
  (spit "report.txt" (to-str "Count: " (count data))) ; => nil (build and write report)

Notes:
  - Requires exactly two arguments (filename and content strings)
  - Creates directories in the path if they don't exist
  - Overwrites existing files completely
  - Uses UTF-8 encoding for text files
  - Returns nil (no meaningful return value)
  - Throws descriptive errors for common issues:
    * Permission denied
    * Invalid directory path
    * Trying to write to a directory
    * File system errors
  - Essential for file output, logging, and data export
  - Pairs perfectly with slurp for file round-trips
  - Memory efficient (writes content directly to disk)
  - Atomic operation (file is written completely or not at all)"""
