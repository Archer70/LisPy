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


@lispy_function("some")
def some(args: List[Any], env: Environment) -> Any:
    """(some collection predicate)
    Returns the first truthful value returned by the predicate for any element,
    or nil if no element satisfies the predicate.
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'some' expects 2 arguments, got {len(args)}."
        )

    collection = args[0]
    predicate = args[1]

    # Validate collection is iterable
    if not isinstance(collection, (list, tuple, Vector, LispyList)):
        raise EvaluationError(
            f"TypeError: 'some' second argument must be a collection, got {type(collection).__name__}."
        )

    # Handle empty collection
    if len(collection) == 0:
        return None

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
        
        # If any element satisfies the predicate, return the truthful result
        if is_truthful(result):
            return result

    # No element satisfied the predicate
    return None


@lispy_documentation("some")
def some_doc() -> str:
    """Returns documentation for the some function."""
    return """Function: some
Arguments: (some collection predicate)
Description: Returns first truthful value from predicate, or nil if none found.

Examples:
  (some number? ["a" 2 "c"])     ; => true (2 is a number)
  (some even? [1 3 5 7])        ; => nil (no even numbers)
  (some even? [1 3 4 7])        ; => true (4 is even)
  (some string? [1 2 "hello"])   ; => true ("hello" is a string)
  (some identity [nil false 0])  ; => 0 (first truthful value)
  (some identity [nil false])    ; => nil (no truthful values)
  (some positive? [-2 -1 0 3])   ; => true (3 is positive)

Notes:
  - Requires exactly 2 arguments (collection, predicate function)
  - Predicate function should take 1 argument and return a value
  - Returns first truthful result from predicate, not the element
  - Uses LisPy truthiness (nil and false are falsy, everything else truthful)
  - Short-circuits on first truthful result (doesn't check remaining elements)
  - Returns nil if no element satisfies predicate or collection is empty
  - Works with any iterable collection (lists, vectors, etc.)
  - Complement of every?: some tests any, every? tests all"""
