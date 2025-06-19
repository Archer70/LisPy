from typing import List, Any, Callable

# from ..types import Symbol # Not needed here
from ..exceptions import EvaluationError
# from ..environment import Environment # Not needed here


def documentation_quote():
    """Returns documentation for the 'quote' special form."""
    return """Special Form: quote
Arguments: (quote expression)
Description: Returns the expression without evaluating it (prevents evaluation).

Examples:
  (quote 123)                      ; Returns 123 (number)
  (quote "hello")                  ; Returns "hello" (string)
  (quote my-symbol)                ; Returns Symbol(my-symbol) (symbol object)
  (quote (+ 1 2))                  ; Returns [Symbol(+), 1, 2] (list structure)
  (quote ())                       ; Returns [] (empty list)
  (quote (a (b c) d))              ; Returns nested list structure

Notes:
  - Prevents evaluation of the expression
  - Returns symbols as symbol objects
  - Returns lists as their actual structure
  - Useful for creating data structures and metaprogramming
  - Often abbreviated with the ' reader macro

See Also: eval, list"""

def handle_quote_form(expression: List[Any], env: Any, evaluate_fn: Callable) -> Any:
    """Handles the (quote expression) special form."""
    # env and evaluate_fn are not used by quote, but kept for consistent signature
    if len(expression) != 2:
        raise EvaluationError(
            "SyntaxError: 'quote' requires exactly one argument. Usage: (quote your-expression)"
        )

    # Return the expression itself, unevaluated
    return expression[1]
