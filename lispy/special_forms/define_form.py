from typing import List, Any, Callable

from ..types import Symbol
from ..exceptions import EvaluationError
from ..environment import Environment


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
