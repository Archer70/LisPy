from typing import List, Any
from ..exceptions import EvaluationError
from ..environment import Environment
from .doc import doc
from .decorators import lispy_function, lispy_documentation


@lispy_function("print-doc")
def print_doc(args: List[Any], env: Environment) -> None:
    """Prints documentation string to console. (print-doc doc-string-or-function)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'print-doc' expects 1 argument, got {len(args)}."
        )

    arg = args[0]

    # If it's a string, print it directly (original behavior)
    if isinstance(arg, str):
        print(arg)
        return None

    # For anything else, try to get documentation using doc function
    try:
        doc_string = doc([arg], env)
        print(doc_string)
        return None
    except EvaluationError as e:
        # Re-raise with context about print-doc
        raise EvaluationError(f"Error in 'print-doc': {str(e)}")


@lispy_documentation("print-doc")
def print_doc_documentation() -> str:
    """Returns documentation for the print-doc function."""
    return """Function: print-doc
Arguments: (print-doc doc-string-or-function)
Description: Prints documentation to the console. Accepts either a documentation string or a function.

Examples:
  (print-doc +)           ; Prints documentation for + (new!)
  (print-doc abs)         ; Prints documentation for abs (new!)
  (print-doc (doc +))     ; Prints documentation for + (original)
  (print-doc "Hello")     ; Prints "Hello"
  
Usage Patterns:
  (print-doc +)           ; Direct function - most convenient
  (print-doc (doc abs))   ; Chained with doc - still works
  (print-doc "Custom")    ; Custom text
  
Notes:
  - New: Can take functions directly without needing (doc ...)
  - Still accepts strings for custom documentation
  - Returns nil, like other print functions
  - Perfect for scripts and debugging"""
