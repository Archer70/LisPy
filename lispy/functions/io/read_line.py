from typing import List, Any
from lispy.environment import Environment
from lispy.exceptions import EvaluationError


def builtin_read_line(args: List[Any], env: Environment) -> str:
    """Reads a line of input from the console. (read-line [prompt])"""
    if len(args) > 1:
        raise EvaluationError(
            "SyntaxError: 'read-line' expects 0 or 1 arguments (optional prompt), got {}.".format(
                len(args)
            )
        )

    prompt = ""
    if len(args) == 1:
        prompt_arg = args[0]
        if not isinstance(prompt_arg, str):
            raise EvaluationError(
                "TypeError: 'read-line' prompt must be a string, got {}.".format(
                    type(prompt_arg).__name__
                )
            )
        prompt = prompt_arg

    try:
        if prompt:
            return input(prompt)
        else:
            return input()
    except EOFError:
        # Return empty string on EOF (Ctrl+D on Unix, Ctrl+Z on Windows)
        return ""
    except KeyboardInterrupt:
        # Re-raise KeyboardInterrupt to allow graceful shutdown
        raise


def documentation_read_line() -> str:
    """Returns documentation for the read-line function."""
    return """Function: read-line
Arguments: (read-line [prompt])
Description: Reads a line of input from the console, optionally displaying a prompt.

Examples:
  (read-line)                           ; reads input with no prompt
  (read-line "Enter your name: ")       ; reads input with prompt
  (read-line "Age: ")                   ; reads input with custom prompt
  
  ; Interactive examples:
  (println "Hello" (read-line "Name: ")) ; => Hello [user input]
  (let [input (read-line "Command: ")] input) ; => [user input]

Notes:
  - Accepts 0 or 1 arguments
  - Optional first argument is a string prompt to display
  - Returns the input string (without trailing newline)
  - Returns empty string on EOF (Ctrl+D/Ctrl+Z)
  - Allows KeyboardInterrupt (Ctrl+C) to propagate
  - Essential for interactive programs and user input
  - Pairs well with print functions for user interaction
  - Input is returned as-is (no automatic type conversion)"""
