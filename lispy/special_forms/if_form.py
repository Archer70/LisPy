# lispy_project/lispy/special_forms/if_form.py
from typing import List, Any, Callable

# from ..types import Symbol # Not directly needed by if logic itself, but evaluate_fn will handle Symbols
from ..exceptions import EvaluationError
from ..environment import Environment

def handle_if_form(expression: List[Any], env: Environment, evaluate_fn: Callable) -> Any:
    """Handles the (if condition then_expr else_expr) special form."""
    # (if condition then_expr) -> else_expr defaults to None (nil)
    if not (3 <= len(expression) <= 4):
        raise EvaluationError("SyntaxError: 'if' requires a condition, a then-expression, and an optional else-expression. Usage: (if cond then) or (if cond then else)")
    
    condition_expr = expression[1]
    then_expr = expression[2]
    
    # Evaluate the condition
    condition_value = evaluate_fn(condition_expr, env)
    
    # Lisp truthiness: False and None are falsey, everything else is truthy
    is_condition_true = not (condition_value is False or condition_value is None)
    
    if is_condition_true:
        return evaluate_fn(then_expr, env)
    else:
        # Condition is false
        if len(expression) == 4:
            else_expr = expression[3]
            return evaluate_fn(else_expr, env)
        else:
            return None # Default to nil (None) if no else branch 