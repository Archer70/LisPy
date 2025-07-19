from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...closure import Function
from ..decorators import lispy_function, lispy_documentation


@lispy_function("filter")
def filter_func(args: List[Any], env: Environment) -> List[Any]:
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'filter' expects 2 arguments, got {len(args)}."
        )

    collection, predicate = args

    # Validate collection
    if collection is None:
        return []
    if not isinstance(collection, list):
        raise EvaluationError(
            f"TypeError: First argument to 'filter' must be a list or vector, got {type(collection).__name__}: '{collection}'"
        )

    # Validate predicate
    if not (callable(predicate) or isinstance(predicate, Function)):
        raise EvaluationError(
            f"TypeError: Second argument to 'filter' must be a function, got {type(predicate).__name__}: '{predicate}'"
        )

    # Filter elements based on predicate
    result = []
    for i, element in enumerate(collection):
        try:
            if isinstance(predicate, Function):
                # User-defined function
                from ...evaluator import evaluate
                call_expr = [predicate, element]
                test_result = evaluate(call_expr, env)
            else:
                # Built-in function
                test_result = predicate([element], env)
            
            # Apply LisPy truthiness: only nil and false are falsy
            if test_result is not None and test_result is not False:
                result.append(element)
        except Exception as e:
            raise EvaluationError(f"Error applying predicate to element {i}: {str(e)}")

    return result


@lispy_documentation("filter")
def filter_documentation() -> str:
    return """Function: filter
Arguments: (filter collection predicate)
Description: Returns a new list containing only elements that satisfy the predicate.

Examples:
  (filter [1 2 3 4] (fn [x] (> x 2)))   ; => [3 4]
  (filter [1 2 3 4] (fn [x] (= x 3)))   ; => [3]
  (filter [] (fn [x] true))             ; => []
  (filter [1 nil 3] (fn [x] x))         ; => [1 3] (nil is falsy)
  (filter [true false nil 42] (fn [x] x)) ; => [true 42]

Notes:
  - Requires exactly two arguments: collection and predicate
  - Collection must be a list or vector
  - Predicate is applied to each element
  - Only elements where predicate returns truthy value are included
  - In LisPy, only nil and false are falsy
  - Returns a new list, does not modify original
  - Empty collection returns empty list
  - Essential for data processing and selection"""
