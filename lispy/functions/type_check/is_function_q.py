from typing import List, Any
from ...environment import Environment
from ...exceptions import EvaluationError
from ...closure import Function


def builtin_is_function_q(args: List[Any], env: Environment) -> bool:
    """Implementation of the (is_function? value) LisPy function.

    Returns true if the argument is a function (either user-defined or built-in), false otherwise.

    Args:
        args: List containing exactly one argument to check
        env: The current environment (unused but required by function signature)

    Returns:
        bool: True if the argument is a function, False otherwise

    Raises:
        EvaluationError: If incorrect number of arguments provided
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_function?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]

    # Check if it's a user-defined function (Function instance)
    if isinstance(arg, Function):
        return True

    # Check if it's a built-in function (Python callable)
    # We need to exclude types that are callable but not functions in the LisPy sense
    if callable(arg):
        # Exclude class types and other non-function callables
        if isinstance(arg, type):
            return False
        return True

    return False


def documentation_is_function_q() -> str:
    """Returns documentation for the is_function? function."""
    return """Function: is_function?
Arguments: (is_function? value)
Description: Tests whether a value is a function (user-defined or built-in).

Examples:
  (is_function? +)              ; => true (built-in function)
  (is_function? map)            ; => true (built-in function)
  (is_function? (fn [x] x))     ; => true (lambda function)
  (define my-fn (fn [x] (* x 2)))
  (is_function? my-fn)          ; => true (user-defined function)
  (is_function? 42)             ; => false (number)
  (is_function? "hello")        ; => false (string)
  (is_function? true)           ; => false (boolean)
  (is_function? [1 2 3])        ; => false (vector)
  (is_function? '(1 2 3))       ; => false (list)
  (is_function? nil)            ; => false

Notes:
  - Returns true for both built-in and user-defined functions
  - Works with lambda functions created with 'fn'
  - Works with functions returned from other functions
  - Returns false for all non-function types
  - Essential for higher-order function programming
  - Useful for validating callback arguments
  - Requires exactly one argument"""
