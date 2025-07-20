from typing import Any, Callable, List

from lispy.closure import Function
from lispy.environment import Environment
from lispy.evaluator import evaluate
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import LispyList, Vector


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


@lispy_function("some")
def some(args: List[Any], env: Environment) -> Any:
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


@lispy_documentation("some")
def some_documentation() -> str:
    """Returns documentation for the some function."""
    return """Function: some
Arguments: (some collection predicate)
Description: Returns the first truthy value from applying predicate to collection elements, or nil.

Examples:
  (some [1 2 3] is-number?)             ; => true
  (some ["a" 1 "b"] is-number?)         ; => true
  (some ["a" "b"] is-number?)           ; => nil
  (some [nil false 42] (fn [x] x))      ; => 42 (first truthy value)
  (some [1 2 3] (fn [x] (> x 2)))       ; => true
  (some [] is-number?)                  ; => nil
  (some [-1 0 5] (fn [x] (> x 0)))      ; => true

Notes:
  - Collection must be a list or vector
  - Predicate must be a function that takes 1 argument
  - Returns the actual truthy value returned by predicate, not just true
  - Short-circuits on first truthy result (doesn't evaluate rest)
  - False and nil are considered falsy, everything else is truthy
  - Empty collection returns nil
  - Useful for finding if any element satisfies a condition
  - Can return different types depending on predicate return values"""
