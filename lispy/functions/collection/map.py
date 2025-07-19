from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...closure import Function
from ..decorators import lispy_function, lispy_documentation


@lispy_function("map")
def map_func(args: List[Any], env: Environment) -> List[Any]:
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'map' expects 2 arguments, got {len(args)}."
        )

    collection, func = args

    # Validate collection
    if collection is None:
        return []
    if not isinstance(collection, list):
        raise EvaluationError(
            f"TypeError: First argument to 'map' must be a list or vector, got {type(collection).__name__}: '{collection}'"
        )

    # Validate function
    if not (callable(func) or isinstance(func, Function)):
        raise EvaluationError(
            f"TypeError: Second argument to 'map' must be a function, got {type(func).__name__}: '{func}'"
        )

    # Apply function to each element
    result = []
    for i, element in enumerate(collection):
        try:
            if isinstance(func, Function):
                # User-defined function - need to evaluate it properly
                from ...evaluator import evaluate
                # Create function call expression
                call_expr = [func, element]
                mapped_value = evaluate(call_expr, env)
            else:
                # Built-in function
                mapped_value = func([element], env)
            result.append(mapped_value)
        except Exception as e:
            raise EvaluationError(f"Error applying function to element {i}: {str(e)}")

    return result


@lispy_documentation("map")
def map_documentation() -> str:
    return """Function: map
Arguments: (map collection function)
Description: Applies a function to each element of a collection and returns a new list.

Examples:
  (map [1 2 3] (fn [x] (* x 2)))    ; => [2 4 6]
  (map [1 2 3] +)                   ; => [1 2 3] (identity-like)
  (map ["a" "b"] to-str)            ; => ["a" "b"]
  (map [] (fn [x] x))               ; => []
  (map [1 2 3] abs)                 ; => [1 2 3]

Notes:
  - Requires exactly two arguments: collection and function
  - Collection must be a list or vector
  - Function is applied to each element individually
  - Returns a new list with transformed elements
  - nil collection returns empty list
  - Essential for functional programming patterns
  - Does not modify the original collection
  - Function must accept one argument"""
