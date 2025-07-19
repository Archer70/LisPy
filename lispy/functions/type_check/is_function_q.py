from typing import List, Any, Callable
from ...exceptions import EvaluationError
from ...environment import Environment
from ...closure import Function
from ..decorators import lispy_function, lispy_documentation


@lispy_function("is-function?")
def is_function(args: List[Any], env: Environment) -> bool:
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is-function?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    # Check if it's a Function (user-defined function) or a built-in function (callable)
    return isinstance(arg, Function) or (callable(arg) and not isinstance(arg, type))


@lispy_documentation("is-function?")
def is_function_documentation() -> str:
    return """Function: is-function?
Arguments: (is-function? value)
Description: Tests whether a value is a function (built-in or user-defined).

Examples:
  (is-function? +)              ; => true (built-in function)
  (is-function? (fn [x] x))     ; => true (lambda function)
  (is-function? println)        ; => true (built-in function)
  (define square (fn [x] (* x x)))
  (is-function? square)         ; => true (user-defined function)
  (is-function? 42)             ; => false (number)
  (is-function? "hello")        ; => false (string)
  (is-function? [1 2 3])        ; => false (vector)
  (is-function? nil)            ; => false

Notes:
  - Returns true for both built-in and user-defined functions
  - User-defined functions are created with (fn ...) or (defn ...)
  - Built-in functions include arithmetic, collection operations, etc.
  - Essential for higher-order function programming
  - Useful for validating function arguments
  - Requires exactly one argument"""
