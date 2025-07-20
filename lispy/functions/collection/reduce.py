from typing import List, Any, Callable
from lispy.types import LispyList, Vector
from lispy.closure import Function  # For user-defined procedures
from lispy.exceptions import EvaluationError, ArityError
from lispy.evaluator import evaluate
from lispy.environment import Environment
from lispy.functions.decorators import lispy_function, lispy_documentation

def _call_reducing_procedure(
    proc: Any, acc: Any, item: Any, env: Environment, evaluate_fn: Callable
) -> Any:
    """Helper to call the reducing procedure (user-defined or built-in)."""
    if isinstance(proc, Function):
        # User-defined function
        if len(proc.params) != 2:
            # This specific check might be redundant if arity is checked before iteration starts,
            # but good for safety if called directly.
            raise ArityError(
                f"Reducing procedure {proc} expects 2 arguments, got different setup."
            )

        call_env = Environment(outer=proc.defining_env)
        call_env.define(proc.params[0].name, acc)
        call_env.define(proc.params[1].name, item)

        result = None
        for expr_in_body in proc.body:
            result = evaluate_fn(expr_in_body, call_env)
        return result
    elif callable(proc):
        # Built-in Python function
        # Built-ins expect a list of args and the env.
        return proc([acc, item], env)  # Pass current env to built-in reducer
    else:
        # Should have been caught by earlier type checks
        raise EvaluationError(
            f"InternalError: Invalid procedure type in _call_reducing_procedure: {type(proc)}"
        )

@lispy_function("reduce")
def reduce(args: List[Any], env: Environment):
    """Implementation of the (reduce collection procedure [initial-value]) LisPy function."""
    num_args = len(args)
    if not (2 <= num_args <= 3):
        raise EvaluationError(
            f"SyntaxError: 'reduce' expects 2 or 3 arguments, got {num_args}."
        )

    collection = args[0]
    procedure = args[1]

    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: First argument to 'reduce' must be a list or vector, got {type(collection)}."
        )

    is_user_defined_fn = isinstance(procedure, Function)
    is_python_callable = callable(procedure) and not is_user_defined_fn

    if not (is_user_defined_fn or is_python_callable):
        raise EvaluationError(
            f"TypeError: Second argument to 'reduce' must be a procedure, got {type(procedure)}."
        )

    # Arity check for the reducing procedure
    expected_arity = 2
    if is_user_defined_fn:
        if len(procedure.params) != expected_arity:
            raise ArityError(
                f"Procedure {procedure} passed to 'reduce' expects {expected_arity} arguments, got {len(procedure.params)}."
            )
    elif is_python_callable:
        # For built-in python callables, they receive (args_list, env).
        # The internal logic of the callable is responsible for checking len(args_list).
        # We can't easily inspect the *effective* arity it expects for its args_list here.
        # The built-in itself should raise an ArityError if it receives an args_list of unexpected length.
        pass  # Trusting the built-in to handle its own arg count from the list it receives.

    if not collection:
        if num_args == 3:  # initial_value is present
            return args[2]  # Return initial_value if collection is empty
        else:
            raise EvaluationError(
                "ValueError: reduce() of empty sequence with no initial value."
            )

    # Determine initial accumulator and iterable sequence
    if num_args == 3:
        accumulator = args[2]
        sequence_to_iterate = list(collection)
    else:  # No initial_value provided
        if len(collection) == 1:
            return collection[
                0
            ]  # Single item in collection, no initial value, return item itself
        accumulator = collection[0]
        sequence_to_iterate = list(collection)[1:]

    # Perform the reduction
    for item in sequence_to_iterate:
        accumulator = _call_reducing_procedure(
            procedure, accumulator, item, env, evaluate
        )

    return accumulator


@lispy_documentation("reduce")
def reduce_documentation() -> str:
    """Returns documentation for the reduce function."""
    return """Function: reduce
Arguments: (reduce collection function [initial-value])
Description: Reduces collection to a single value by applying function cumulatively.

Examples:
  (reduce [1 2 3 4] +)                  ; => 10 (sum without initial)
  (reduce [1 2 3 4] + 0)                ; => 10 (sum with initial)
  (reduce [1 2 3] * 1)                  ; => 6 (product)
  (reduce ["a" "b" "c"] str "")         ; => "abc" (concatenation)
  (reduce [5] + 10)                     ; => 15 (single element)
  (reduce [] + 42)                      ; => 42 (empty with initial)
  (reduce [1 2 3] (fn [acc x] (cons x acc)) '()) ; => (3 2 1) (reverse)

Notes:
  - Collection must be a list or vector
  - Function must take exactly 2 arguments (accumulator, current-element)
  - With initial-value: starts with initial, processes all elements
  - Without initial-value: uses first element as initial, processes rest
  - Empty collection without initial-value raises error
  - Empty collection with initial-value returns initial-value
  - Single element without initial-value returns that element
  - Function is called left-to-right through the collection"""
