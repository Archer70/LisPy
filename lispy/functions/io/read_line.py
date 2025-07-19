from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ..decorators import lispy_function, lispy_documentation


@lispy_function("read-line", web_safe=False)
def read_line_func(args: List[Any], env: Environment) -> str:
    if len(args) > 1:
        raise EvaluationError(
            f"SyntaxError: 'read-line' expects 0 or 1 arguments, got {len(args)}."
        )

    # Optional prompt
    if len(args) == 1:
        prompt = args[0]
        if not isinstance(prompt, str):
            raise EvaluationError(
                f"TypeError: 'read-line' prompt must be a string, got {type(prompt).__name__}: '{prompt}'"
            )
        
        # Print prompt without newline
        print(prompt, end="")
    
    # Read line from stdin
    try:
        line = input()
        return line
    except EOFError:
        # Return empty string on EOF (Ctrl+D / end of input)
        return ""
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        raise EvaluationError("KeyboardInterrupt: User interrupted input")
    except Exception as e:
        raise EvaluationError(f"IOError: Error reading input: {str(e)}")


@lispy_documentation("read-line")
def read_line_documentation() -> str:
    return """Function: read-line
Arguments: (read-line) or (read-line prompt)
Description: Reads a line of text from standard input.

Examples:
  (read-line)                   ; waits for user input, returns line
  (read-line "Enter name: ")    ; shows prompt, returns input
  (read-line "Password: ")      ; prompts for password input
  
  ; Example interactive program:
  (let [name (read-line "What's your name? ")]
    (println "Hello," name))

Notes:
  - Accepts 0 or 1 arguments (optional prompt)
  - Prompt must be a string if provided
  - Waits for user to press Enter
  - Returns the input line as a string (without newline)
  - Returns empty string on EOF (end of input)
  - **WEB UNSAFE**: Reads from standard input
  - Essential for interactive programs and user input
  - Blocks execution until input is received
  - Can be interrupted with Ctrl+C (raises error)
  - Useful for command-line interfaces and prompts"""
