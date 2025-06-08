from typing import List, Any, Callable

# from ..types import Symbol # Not needed here
from ..exceptions import EvaluationError
# from ..environment import Environment # Not needed here


def handle_quote_form(expression: List[Any], env: Any, evaluate_fn: Callable) -> Any:
    """Handles the (quote expression) special form."""
    # env and evaluate_fn are not used by quote, but kept for consistent signature
    if len(expression) != 2:
        raise EvaluationError(
            "SyntaxError: 'quote' requires exactly one argument. Usage: (quote your-expression)"
        )

    # Return the expression itself, unevaluated
    return expression[1]
