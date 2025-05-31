# lispy_project/lispy/special_forms/or_form.py
from typing import List, Any, Callable

from ..environment import Environment

def handle_or_form(expression: List[Any], env: Environment, evaluate_fn: Callable) -> Any:
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

    if not args: # No arguments, (or) -> nil
        return None 

    last_value = None # Default if loop doesn't run (e.g. for (or))
                      # or if all args are falsy, this will be overwritten by the last arg's value.

    for arg_expr in args:
        value = evaluate_fn(arg_expr, env)
        # LisPy truthiness: False and None (nil) are falsy. Everything else is truthy.
        is_value_truthy = not (value is False or value is None)
        
        if is_value_truthy:
            return value # Short-circuit and return the first truthy value
        
        last_value = value # Keep track of the last evaluated falsy value
    
    return last_value # All were falsy, return the last one's value 