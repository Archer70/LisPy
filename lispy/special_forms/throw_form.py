from typing import List, Any, Callable
from lispy.environment import Environment
from lispy.exceptions import EvaluationError, UserThrownError


def handle_throw_form(expression: List[Any], env: Environment, evaluate_fn: Callable) -> Any:
    """
    Handle the 'throw' special form.
    
    Usage: (throw value)
    
    Throws a UserThrownError with the given value.
    """
    if len(expression) != 2:
        raise EvaluationError("SyntaxError: 'throw' expects exactly 1 argument (value), got {}.".format(len(expression) - 1))
    
    value_expr = expression[1]
    value = evaluate_fn(value_expr, env)
    
    # Throw a UserThrownError with the evaluated value
    raise UserThrownError(value) 