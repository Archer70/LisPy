from lispy.types import Vector, Symbol
from lispy.exceptions import EvaluationError
from lispy.environment import Environment
from lispy.closure import Function
from typing import List, Any, Callable

def _call_comparison_function(
    compare_fn: Any, 
    a: Any, 
    b: Any, 
    env: Environment, 
    evaluate_fn: Callable
) -> int:
    """Helper to call a user-defined comparison function."""
    if isinstance(compare_fn, Function):
        # User-defined function
        if len(compare_fn.params) != 2:
            raise EvaluationError(f"Comparison function {compare_fn} expects 2 arguments, got {len(compare_fn.params)}.")
        
        call_env = Environment(outer=compare_fn.defining_env)
        call_env.define(compare_fn.params[0].name, a)
        call_env.define(compare_fn.params[1].name, b)
        
        result = None
        for expr_in_body in compare_fn.body:
            result = evaluate_fn(expr_in_body, call_env)
        
        # Convert boolean or numeric result to comparison format
        if isinstance(result, bool):
            return -1 if result else 1  # true means a < b
        elif isinstance(result, (int, float)):
            if result < 0:
                return -1
            elif result > 0:
                return 1
            else:
                return 0
        else:
            raise EvaluationError(f"Comparison function must return a number or boolean, got {type(result)}.")
    
    elif callable(compare_fn):
        # Built-in Python function
        result = compare_fn([a, b], env)
        if isinstance(result, bool):
            return -1 if result else 1
        elif isinstance(result, (int, float)):
            if result < 0:
                return -1
            elif result > 0:
                return 1
            else:
                return 0
        else:
            raise EvaluationError(f"Comparison function must return a number or boolean, got {type(result)}.")
    else:
        raise EvaluationError(f"Invalid comparison function type: {type(compare_fn)}")


def sort_fn(args: List[Any], env: Environment):
    """Sorts a vector and returns a new sorted vector.

    Usage: (sort vector [compare-fn])
    - vector: The vector to sort.
    - compare-fn: (Optional) A function that takes two arguments and returns:
                  - A negative number if first < second
                  - Zero if first == second  
                  - A positive number if first > second
                  - Or a boolean where true means first < second
                  
    If no comparison function is provided, uses default ordering.
    """
    if not 1 <= len(args) <= 2:
        raise EvaluationError(f"SyntaxError: 'sort' expects 1 or 2 arguments, got {len(args)}.")

    vector = args[0]
    compare_fn = args[1] if len(args) == 2 else None

    if not isinstance(vector, Vector):
        raise EvaluationError(f"TypeError: 'sort' first argument must be a vector, got {type(vector)}.")

    # Create a copy of the vector elements to avoid mutating the original
    elements = list(vector)
    
    if compare_fn is None:
        # Use Python's default sorting - it handles mixed types well
        try:
            elements.sort()
        except TypeError:
            # If direct comparison fails, sort by string representation
            elements.sort(key=str)
    else:
        # Validate comparison function
        is_user_defined_fn = isinstance(compare_fn, Function)
        is_python_callable = callable(compare_fn) and not is_user_defined_fn

        if not (is_user_defined_fn or is_python_callable):
            raise EvaluationError(f"TypeError: Second argument to 'sort' must be a procedure, got {type(compare_fn)}.")

        # Check arity for user-defined functions
        if is_user_defined_fn and len(compare_fn.params) != 2:
            raise EvaluationError(f"Comparison function {compare_fn} passed to 'sort' expects 2 arguments, got {len(compare_fn.params)}.")

        # Import evaluate function for comparison calls
        from lispy.evaluator import evaluate
        
        # Sort using the custom comparison function
        def compare_wrapper(a, b):
            return _call_comparison_function(compare_fn, a, b, env, evaluate)
        
        # Use functools.cmp_to_key for Python 3 compatibility
        from functools import cmp_to_key
        elements.sort(key=cmp_to_key(compare_wrapper))

    return Vector(elements) 