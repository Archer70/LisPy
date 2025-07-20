# lispy_project/lispy/special_forms/or_form.py
from typing import Any, Callable, List

from ..environment import Environment


def documentation_or():
    """Returns documentation for the 'or' special form."""
    return """Special Form: or
Arguments: (or expr1 expr2 ...)
Description: Logical OR with short-circuiting. Returns first truthy value or last falsy value.

Examples:
  (or false nil "hello" "world")   ; Returns "hello" (first truthy value)
  (or false nil)                   ; Returns nil (all falsy)
  (or "first" "never evaluated")   ; Returns "first" (short-circuit)
  (or)                             ; Returns nil (no arguments)
  (or (< 5 3) (> 10 2))            ; Returns true (logical conditions)
  (or user-input "default")        ; Returns "default" if user-input is falsy

Notes:
  - Uses short-circuit evaluation (stops at first truthy value)
  - false and nil are falsy, everything else is truthy
  - Returns actual values, not just true/false
  - Useful for default values and fallback chains

See Also: and, if, when"""


def handle_or_form(
    expression: List[Any], env: Environment, evaluate_fn: Callable
) -> Any:
    """Handles the (or expr* ) special form.
    Evaluates expressions from left to right.
    If any expression evaluates to a truthy value (not False and not None),
    its value is returned and subsequent expressions are not evaluated (short-circuiting).
    If all expressions evaluate to a falsy value (False or None), the value of the last
    expression is returned.
    If there are no expressions, (or) evaluates to nil (which is falsy).
    """
    # expression is [Symbol('or'), arg1, arg2, ...]
    args = expression[1:]

    if not args:  # No arguments, (or) -> nil
        return None

    last_value = None  # Default if loop doesn't run (e.g. for (or))
    # or if all args are falsy, this will be overwritten by the last arg's value.

    for arg_expr in args:
        value = evaluate_fn(arg_expr, env)
        # LisPy truthiness: False and None (nil) are falsy. Everything else is truthy.
        is_value_truthy = not (value is False or value is None)

        if is_value_truthy:
            return value  # Short-circuit and return the first truthy value

        last_value = value  # Keep track of the last evaluated falsy value

    return last_value  # All were falsy, return the last one's value
