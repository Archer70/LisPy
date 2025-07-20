from typing import Any, Callable, List

from lispy.environment import Environment
from lispy.exceptions import EvaluationError, UserThrownError


def documentation_throw():
    """Returns documentation for the 'throw' special form."""
    return """Special Form: throw
Arguments: (throw value)
Description: Throws an exception with the given value, which can be caught by try/catch.

Examples:
  (throw "Error message")          ; Throws string as exception
  (throw 404)                      ; Throws number as exception
  (throw {:type "custom" :msg "Failed"})  ; Throws map as exception
  (try (throw "oops") (catch e e)) ; Returns "oops" (caught exception)

Notes:
  - Immediately stops execution and propagates exception
  - Exception value can be any type
  - Must be caught by a try/catch block or program terminates
  - Useful for error handling and control flow

See Also: try"""


def handle_throw_form(
    expression: List[Any], env: Environment, evaluate_fn: Callable
) -> Any:
    """
    Handle the 'throw' special form.

    Usage: (throw value)

    Throws a UserThrownError with the given value.
    """
    if len(expression) != 2:
        raise EvaluationError(
            "SyntaxError: 'throw' expects exactly 1 argument (value), got {}.".format(
                len(expression) - 1
            )
        )

    value_expr = expression[1]
    value = evaluate_fn(value_expr, env)

    # Throw a UserThrownError with the evaluated value
    raise UserThrownError(value)
