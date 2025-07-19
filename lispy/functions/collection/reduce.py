from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...closure import Function
from ..decorators import lispy_function, lispy_documentation


@lispy_function("reduce")
def reduce_func(args: List[Any], env: Environment) -> Any:
    if len(args) < 2 or len(args) > 3:
        raise EvaluationError(
            f"SyntaxError: 'reduce' expects 2 or 3 arguments, got {len(args)}."
        )

    if len(args) == 2:
        collection, func = args
        initial_value = None
        has_initial = False
    else:
        collection, initial_value, func = args
        has_initial = True

    # Validate collection
    if collection is None:
        return initial_value if has_initial else None
    if not isinstance(collection, list):
        raise EvaluationError(
            f"TypeError: First argument to 'reduce' must be a list or vector, got {type(collection).__name__}: '{collection}'"
        )

    # Validate function
    if not (callable(func) or isinstance(func, Function)):
        raise EvaluationError(
            f"TypeError: Function argument to 'reduce' must be a function, got {type(func).__name__}: '{func}'"
        )

    # Handle empty collection
    if not collection:
        if has_initial:
            return initial_value
        else:
            raise EvaluationError("TypeError: Cannot reduce empty collection without initial value")

    # Start reduction
    if has_initial:
        accumulator = initial_value
        start_index = 0
    else:
        accumulator = collection[0]
        start_index = 1

    # Apply function iteratively
    for i in range(start_index, len(collection)):
        element = collection[i]
        try:
            if isinstance(func, Function):
                # User-defined function
                from ...evaluator import evaluate
                call_expr = [func, accumulator, element]
                accumulator = evaluate(call_expr, env)
            else:
                # Built-in function
                accumulator = func([accumulator, element], env)
        except Exception as e:
            raise EvaluationError(f"Error applying function during reduction at element {i}: {str(e)}")

    return accumulator


@lispy_documentation("reduce")
def reduce_documentation() -> str:
    return """Function: reduce
Arguments: (reduce collection function) or (reduce collection initial-value function)
Description: Reduces a collection to a single value by applying a function cumulatively.

Examples:
  (reduce [1 2 3 4] +)              ; => 10 (1+2+3+4)
  (reduce [1 2 3] 0 +)              ; => 6 (0+1+2+3)
  (reduce [1 2 3 4] *)              ; => 24 (1*2*3*4)
  (reduce ["a" "b" "c"] join)       ; => "abc"
  (reduce [] 0 +)                   ; => 0 (with initial value)
  (reduce [5] +)                    ; => 5 (single element)

Notes:
  - Accepts 2 or 3 arguments
  - Without initial value: uses first element as accumulator, starts with second
  - With initial value: starts with initial value and first element
  - Function must accept 2 arguments (accumulator and current element)
  - Returns accumulator after processing all elements
  - Empty collection without initial value raises error
  - Essential for aggregation and computation patterns"""
