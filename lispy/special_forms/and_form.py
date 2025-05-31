from typing import List, Any, Callable

from ..environment import Environment
# No EvaluationError needed here as argument count is flexible

def handle_and_form(expression: List[Any], env: Environment, evaluate_fn: Callable) -> Any:
    """Handles the (and expr* ) special form.
    Evaluates expressions from left to right.
    If any expression evaluates to false (False or None), its value is returned
    and subsequent expressions are not evaluated (short-circuiting).
    If all expressions evaluate to a truthy value, the value of the last
    expression is returned.
    If there are no expressions, (and) evaluates to true.
    """
    # expression is [Symbol('and'), arg1, arg2, ...]
    args = expression[1:]

    if not args: # No arguments, (and) -> true
        return True

    last_value = True # Default if loop doesn't run (e.g. for (and))
                     # or if all args are truthy, this will be overwritten by the last arg's value.

    for arg_expr in args:
        value = evaluate_fn(arg_expr, env)
        # LisPy truthiness: False and None (nil) are falsy
        is_value_falsy = (value is False or value is None)
        
        if is_value_falsy:
            return value # Short-circuit and return the first falsy value
        
        last_value = value # Keep track of the last evaluated truthy value
    
    return last_value # All were truthy, return the last one's value 