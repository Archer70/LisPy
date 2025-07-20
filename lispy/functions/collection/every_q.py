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
            f"TypeError: Second argument to 'every?' must be a function, got {type(predicate)}."
        )


@lispy_function("every?")
def every_q(args: List[Any], env: Environment) -> bool:
    """Implementation of the (every? collection predicate) LisPy function.

    Returns true if all elements in the collection satisfy the predicate,
    false if any element fails the predicate.

    Args:
        args: List containing exactly two arguments - collection and predicate function
        env: The current environment

    Returns:
        bool: True if all elements satisfy predicate, False if any element fails

    Raises:
        EvaluationError: If incorrect number of arguments or invalid argument types
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'every?' expects 2 arguments, got {len(args)}."
        )

    collection = args[0]
    predicate = args[1]

    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: First argument to 'every?' must be a list or vector, got {type(collection)}."
        )

    # Check if predicate is callable
    is_user_defined_fn = isinstance(predicate, Function)
    is_python_callable = callable(predicate) and not is_user_defined_fn

    if not (is_user_defined_fn or is_python_callable):
        raise EvaluationError(
            f"TypeError: Second argument to 'every?' must be a function, got {type(predicate)}."
        )

    # Empty collection is vacuously true
    if not collection:
        return True

    # Apply predicate to each element, return False on first falsy result
    for item in collection:
        result = _call_predicate(predicate, item, env, evaluate)
        # In LisPy, False and None are falsy, everything else is truthy
        if result is False or result is None:
            return False

    # All elements satisfied the predicate
    return True


@lispy_documentation("every?")
def every_q_documentation() -> str:
    """Returns documentation for the every? function."""
    return """Function: every?
Arguments: (every? collection predicate)
Description: Returns true if all elements in collection satisfy the predicate, false otherwise.

Examples:
  (every? [1 2 3] is-number?)           ; => true
  (every? [1 "a" 3] is-number?)         ; => false
  (every? [2 4 6] (fn [x] (= (% x 2) 0))) ; => true (all even)
  (every? [1 3 5] (fn [x] (> x 0)))     ; => true (all positive)
  (every? [] is-number?)                ; => true (vacuously true)
  (every? [true true false] (fn [x] x)) ; => false
  (every? [-1 2 3] (fn [x] (> x 0)))    ; => false

Notes:
  - Collection must be a list or vector
  - Predicate must be a function that takes 1 argument
  - Returns true or false (boolean result)
  - Short-circuits on first falsy result (doesn't evaluate rest)
  - False and nil are considered falsy, everything else is truthy
  - Empty collection returns true (vacuous truth)
  - Complement of some: every? tests all, some tests any
  - Useful for validating that all elements meet criteria"""
