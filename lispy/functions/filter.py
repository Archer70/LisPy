from typing import List, Any, Callable
from lispy.types import LispyList, Vector, Symbol
from lispy.closure import Function  # For user-defined procedures
from lispy.exceptions import EvaluationError, ArityError
from lispy.evaluator import evaluate # For evaluating user-defined function bodies
from lispy.environment import Environment

def _call_predicate(
    predicate: Any, 
    item: Any, 
    env: Environment, 
    evaluate_fn: Callable
) -> Any:
    """Helper to call the predicate (user-defined or built-in)."""
    if isinstance(predicate, Function):
        # User-defined function
        if len(predicate.params) != 1:
            # This specific check might be redundant if arity is checked before iteration starts,
            # but good for safety if called directly.
            raise ArityError(f"Predicate {predicate} expects 1 argument, got different setup.")
        
        call_env = Environment(outer=predicate.defining_env)
        call_env.define(predicate.params[0].name, item)
        
        result = None
        for expr_in_body in predicate.body:
            result = evaluate_fn(expr_in_body, call_env)
        return result
    elif callable(predicate):
        # Built-in Python function
        # Built-ins expect a list of args and the env.
        return predicate([item], env) # Pass current env to built-in predicate
    else:
        # Should have been caught by earlier type checks
        raise EvaluationError(f"InternalError: Invalid predicate type in _call_predicate: {type(predicate)}")

def builtin_filter(args: List[Any], env: Environment):
    """Implementation of the (filter collection predicate) LisPy function."""
    if len(args) != 2:
        raise EvaluationError(f"SyntaxError: 'filter' expects 2 arguments, got {len(args)}.")

    collection = args[0]
    predicate = args[1]

    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(f"TypeError: First argument to 'filter' must be a list or vector, got {type(collection)}.")
    
    is_user_defined_fn = isinstance(predicate, Function)
    is_python_callable = callable(predicate) and not is_user_defined_fn

    if not (is_user_defined_fn or is_python_callable):
        raise EvaluationError(f"TypeError: Second argument to 'filter' must be a procedure, got {type(predicate)}.")

    # Arity check for the predicate
    expected_arity = 1
    if is_user_defined_fn:
        if len(predicate.params) != expected_arity:
            raise ArityError(f"Procedure {predicate} passed to 'filter' expects {expected_arity} argument, got {len(predicate.params)}.")
    elif is_python_callable:
        # For built-in python callables, they receive (args_list, env).
        # The internal logic of the callable is responsible for checking len(args_list).
        # We can't easily inspect the *effective* arity it expects for its args_list here.
        # The built-in itself should raise an ArityError if it receives an args_list of unexpected length.
        pass # Trusting the built-in to handle its own arg count from the list it receives.

    filtered_items = []
    for item in collection:
        # In LisPy, False and None are falsy, everything else is truthy.
        predicate_result = _call_predicate(predicate, item, env, evaluate)
        if predicate_result is not False and predicate_result is not None:
            filtered_items.append(item)

    if isinstance(collection, Vector):
        return Vector(filtered_items)
    else: # LispyList
        return LispyList(filtered_items) 