from typing import List, Any, Callable
from ..types import LispyList, Vector
from ..closure import Function
from ..exceptions import EvaluationError
from ..evaluator import evaluate
from ..environment import Environment


def _call_predicate(
    predicate: Any, item: Any, env: Environment, evaluate_fn: Callable
) -> Any:
    """Helper to call the predicate (user-defined or built-in) on an item."""
    if isinstance(predicate, Function):
        # User-defined function
        if len(predicate.params) != 1:
            raise EvaluationError(
                f"TypeError: Predicate function expects 1 argument, got {len(predicate.params)}."
            )

        call_env = Environment(outer=predicate.defining_env)
        call_env.define(predicate.params[0].name, item)

        result = None
        for expr_in_body in predicate.body:
            result = evaluate_fn(expr_in_body, call_env)
        return result
    elif callable(predicate):
        # Built-in Python function
        return predicate([item], env)
    else:
        raise EvaluationError(
            f"TypeError: First argument to 'some' must be a function, got {type(predicate)}."
        )


def builtin_some(args: List[Any], env: Environment) -> Any:
    """Implementation of the (some collection predicate) LisPy function.
    
    Returns the first logical true value of applying the predicate to each element
    in the collection, or nil if no element satisfies the predicate.
    
    Args:
        args: List containing exactly two arguments - collection and predicate function
        env: The current environment
        
    Returns:
        The first truthy result of applying predicate to collection elements, or None
        
    Raises:
        EvaluationError: If incorrect number of arguments or invalid argument types
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'some' expects 2 arguments, got {len(args)}."
        )

    collection = args[0]
    predicate = args[1]

    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: First argument to 'some' must be a list or vector, got {type(collection)}."
        )

    # Check if predicate is callable
    is_user_defined_fn = isinstance(predicate, Function)
    is_python_callable = callable(predicate) and not is_user_defined_fn

    if not (is_user_defined_fn or is_python_callable):
        raise EvaluationError(
            f"TypeError: Second argument to 'some' must be a function, got {type(predicate)}."
        )

    # Apply predicate to each element, return first truthy result
    for item in collection:
        result = _call_predicate(predicate, item, env, evaluate)
        # In LisPy, False and None are falsy, everything else is truthy
        if result is not False and result is not None:
            return result
    
    # No element satisfied the predicate
    return None 