from typing import List, Any
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.closure import Function
from lispy.functions.decorators import lispy_function, lispy_documentation

@lispy_function("is-function?")
def is_function_q(args: List[Any], env: Environment) -> bool:
    """Implementation of the (is-function? value) LisPy function.

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
            f"SyntaxError: 'is-function?' expects 1 argument, got {len(args)}."
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


@lispy_documentation("is-function?")
def is_function_q_documentation() -> str:
    """Returns documentation for the is-function? function."""
    return """Function: is-function?
Arguments: (is-function? value)
Description: Tests whether a value is a function (user-defined or built-in).

Examples:
  (is-function? +)              ; => true (built-in function)
  (is-function? map)            ; => true (built-in function)
  (is-function? (fn [x] x))     ; => true (lambda function)
  (define my-fn (fn [x] (* x 2)))
  (is-function? my-fn)          ; => true (user-defined function)
  (is-function? 42)             ; => false (number)
  (is-function? "hello")        ; => false (string)
  (is-function? true)           ; => false (boolean)
  (is-function? [1 2 3])        ; => false (vector)
  (is-function? '(1 2 3))       ; => false (list)
  (is-function? nil)            ; => false

Notes:
  - Returns true for both built-in and user-defined functions
  - Works with lambda functions created with 'fn'
  - Works with functions returned from other functions
  - Returns false for all non-function types
  - Essential for higher-order function programming
  - Useful for validating callback arguments
  - Requires exactly one argument"""
