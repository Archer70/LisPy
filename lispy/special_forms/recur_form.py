"""
Recur special form for explicit tail call optimization.

The recur form provides explicit tail call optimization, similar to Clojure.
It can only be used in tail position within a function and causes the function
to restart with new argument values.

Usage: (recur arg1 arg2 ...)
"""

from ..exceptions import EvaluationError
from ..tail_call import TailCall


def handle_recur(expression, env, evaluate_fn):
    """
    Handle the recur special form for explicit tail call optimization.

    Args:
        expression: The recur expression [recur, arg1, arg2, ...]
        env: The current environment
        evaluate_fn: Function to evaluate sub-expressions

    Returns:
        TailCall object indicating a tail recursive call

    Raises:
        EvaluationError: If recur is used incorrectly
    """
    # Get the argument expressions (everything after 'recur')
    arg_exprs = expression[1:]

    # Evaluate all arguments
    evaluated_args = [evaluate_fn(arg, env) for arg in arg_exprs]

    # Look up the current function from the environment
    # The function should be bound to a special variable during execution
    try:
        current_function = env.lookup("__current_function__")
    except EvaluationError:
        raise EvaluationError(
            "SyntaxError: 'recur' can only be used within a function."
        )

    # Check arity
    if len(evaluated_args) != len(current_function.params):
        raise EvaluationError(
            f"ArityError: 'recur' expects {len(current_function.params)} arguments "
            f"to match function parameters, got {len(evaluated_args)}."
        )

    # Return a TailCall object to signal tail recursion
    return TailCall(current_function, evaluated_args)
