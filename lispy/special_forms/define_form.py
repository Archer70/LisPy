from typing import Any, Callable, List

from ..environment import Environment
from ..exceptions import EvaluationError
from ..types import Symbol


def documentation_define():
    """Returns documentation for the 'define' special form."""
    return """Special Form: define
Arguments: (define symbol value)
Description: Creates a global variable binding by evaluating value and binding it to symbol.

Examples:
  (define x 42)                    ; Returns 42 (define a number)
  (define greeting "Hello")        ; Returns "Hello" (define a string)
  (define sum (+ 10 20))           ; Returns 30 (define with expression)
  (define pi 3.14159)              ; Returns 3.14159 (define a constant)
  (define square (fn [x] (* x x))) ; Returns function (define a function)
  (define items [1 2 3])           ; Returns [1 2 3] (define a collection)

Notes:
  - Creates global bindings that persist
  - Value expression is evaluated before binding
  - Returns the evaluated value
  - Redefining overwrites the previous value

See Also: let, fn"""


def handle_define_form(
    expression: List[Any], env: Environment, evaluate_fn: Callable
) -> Any:
    """Handles the (define symbol value) special form."""
    if len(expression) != 3:
        raise EvaluationError(
            "SyntaxError: 'define' requires a symbol and a value. Usage: (define symbol value)"
        )

    symbol_to_define = expression[1]
    if not isinstance(symbol_to_define, Symbol):
        raise EvaluationError(
            f"SyntaxError: First argument to 'define' must be a symbol, got {type(symbol_to_define).__name__}"
        )

    value_expr = expression[2]
    evaluated_value = evaluate_fn(value_expr, env)  # Use the passed-in evaluate_fn

    env.define(symbol_to_define.name, evaluated_value)
    return evaluated_value  # 'define' typically returns the value assigned
