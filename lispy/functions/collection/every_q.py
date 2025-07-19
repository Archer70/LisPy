from typing import List, Any
from ...exceptions import EvaluationError
from ...environment import Environment
from ...types import Vector, LispyList
from ...closure import Function
from ..decorators import lispy_function, lispy_documentation


def is_truthful(value: Any) -> bool:
    """
    Determine if a value is truthful according to LisPy semantics.
    In LisPy, only `None` (nil) and `False` are falsy.
    Everything else is truthful.
    """
    return value is not None and value is not False


@lispy_function("every?")
def every_q(args: List[Any], env: Environment) -> bool:
    """(every? collection predicate)
    Returns true if the predicate returns a truthful value for every element in the collection.
    Returns true for an empty collection.
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'every?' expects 2 arguments, got {len(args)}."
        )

    collection = args[0]
    predicate = args[1]

    # Validate collection is iterable
    if not isinstance(collection, (list, tuple, Vector, LispyList)):
        raise EvaluationError(
            f"TypeError: 'every?' second argument must be a collection, got {type(collection).__name__}."
        )

    # Handle empty collection
    if len(collection) == 0:
        return True

    # Check each element
    for element in collection:
        # Apply predicate to element
        if isinstance(predicate, Function):
            # User-defined function
            from ...evaluator import evaluate
            call_expr = [predicate, element]
            result = evaluate(call_expr, env)
        else:
            # Built-in function
            result = predicate([element], env)
        
        # If any element fails the predicate, return False
        if not is_truthful(result):
            return False

    return True


@lispy_documentation("every?")
def every_q_doc() -> str:
    """Returns documentation for the every? function."""
    return """Function: every?
Arguments: (every? collection predicate)
Description: Returns true if predicate returns truthful value for every element.

Examples:
  (every? number? [1 2 3 4])     ; => true (all are numbers)
  (every? even? [2 4 6 8])       ; => true (all are even)
  (every? positive? [1 2 3])     ; => true (all are positive)
  (every? string? [1 "a" 3])     ; => false (not all are strings)
  (every? identity [true 1 "a"]) ; => true (all are truthful)
  (every? identity [true nil])   ; => false (nil is falsy)
  (every? even? [])              ; => true (empty collection)

Notes:
  - Requires exactly 2 arguments (collection, predicate function)
  - Predicate function should take 1 argument and return a value
  - Uses LisPy truthiness (nil and false are falsy, everything else truthful)
  - Short-circuits on first falsy result (doesn't check remaining elements)
  - Returns true for empty collections (vacuous truth)
  - Works with any iterable collection (lists, vectors, etc.)"""
