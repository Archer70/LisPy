from typing import Any, Callable, List

from lispy.closure import Function
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import Vector


def _call_comparison_function(
    compare_fn: Any, a: Any, b: Any, env: Environment, evaluate_fn: Callable
) -> int:
    """Helper to call a user-defined comparison function."""
    if isinstance(compare_fn, Function):
        # User-defined function
        if len(compare_fn.params) != 2:
            raise EvaluationError(
                f"Comparison function {compare_fn} expects 2 arguments, got {len(compare_fn.params)}."
            )

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
            raise EvaluationError(
                f"Comparison function must return a number or boolean, got {type(result)}."
            )

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
            raise EvaluationError(
                f"Comparison function must return a number or boolean, got {type(result)}."
            )
    else:
        raise EvaluationError(f"Invalid comparison function type: {type(compare_fn)}")


@lispy_function("sort")
def sort(args: List[Any], env: Environment):
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
        raise EvaluationError(
            f"SyntaxError: 'sort' expects 1 or 2 arguments, got {len(args)}."
        )

    vector = args[0]
    compare_fn = args[1] if len(args) == 2 else None

    if not isinstance(vector, Vector):
        raise EvaluationError(
            f"TypeError: 'sort' first argument must be a vector, got {type(vector)}."
        )

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
            raise EvaluationError(
                f"TypeError: Second argument to 'sort' must be a procedure, got {type(compare_fn)}."
            )

        # Check arity for user-defined functions
        if is_user_defined_fn and len(compare_fn.params) != 2:
            raise EvaluationError(
                f"Comparison function {compare_fn} passed to 'sort' expects 2 arguments, got {len(compare_fn.params)}."
            )

        # Import evaluate function for comparison calls
        from lispy.evaluator import evaluate

        # Sort using the custom comparison function
        def compare_wrapper(a, b):
            return _call_comparison_function(compare_fn, a, b, env, evaluate)

        # Use functools.cmp_to_key for Python 3 compatibility
        from functools import cmp_to_key

        elements.sort(key=cmp_to_key(compare_wrapper))

    return Vector(elements)


@lispy_documentation("sort")
def sort_documentation() -> str:
    """Returns documentation for the sort function."""
    return """Function: sort
Arguments: (sort vector [compare-fn])
Description: Returns a new sorted vector. Optionally accepts a comparison function.

Examples:
  (sort [3 1 4 1 5])            ; => [1 1 3 4 5] (ascending default)
  (sort [])                     ; => []
  (sort ["zebra" "apple"])      ; => ["apple" "zebra"] (alphabetical)
  (sort [3.14 2 1.5 4])         ; => [1.5 2 3.14 4] (mixed numbers)
  
  ; Custom comparison functions:
  (sort [1 3 2 5] (fn [a b] (> a b)))     ; => [5 3 2 1] (descending)
  (sort [1 3 2 5] (fn [a b] (- b a)))     ; => [5 3 2 1] (numeric comparison)
  (sort [-3 1 -2] (fn [a b] (< (abs a) (abs b))))  ; => [1 -2 -3] (by absolute)

Notes:
  - First argument must be a vector (not lists)
  - Optional second argument must be a comparison function
  - Returns new vector, original is not modified
  - Default sort is ascending order for numbers, alphabetical for strings
  - Comparison function takes 2 arguments, returns:
    * Negative number if first < second
    * Zero if first == second  
    * Positive number if first > second
    * Boolean where true means first < second
  - Comparison function must have exactly 2 parameters
  - Handles mixed numeric types (int/float) gracefully
  - Uses string representation fallback for incomparable types"""
