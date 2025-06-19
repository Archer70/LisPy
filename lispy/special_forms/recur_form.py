"""
Recur special form for explicit tail call optimization.

The recur form provides explicit tail call optimization, similar to Clojure.
It can only be used in tail position within a function and causes the function
to restart with new argument values.

Usage: (recur arg1 arg2 ...)
"""

from ..exceptions import EvaluationError
from ..tail_call import TailCall


def documentation_recur():
    """Returns documentation for the 'recur' special form."""
    return """Special Form: recur
Arguments: (recur arg1 arg2 ...)
Description: Tail-recursive call to the current function with new arguments.

Examples:
  (fn [n acc] 
    (if (= n 0) acc (recur (- n 1) (+ acc n))))  ; Factorial with accumulator
  (loop [x 0] 
    (if (< x 5) (recur (+ x 1)) x))              ; Count to 5 in loop
  (fn [lst] 
    (if (empty? lst) 
      nil 
      (recur (rest lst))))                       ; Process list recursively

Notes:
  - Can only be used in tail position (last expression) 
  - Must be inside a function or loop form
  - Provides stack-safe recursion (no stack overflow)
  - Number of arguments must match function parameters
  - Jumps back to function start with new argument values
  - More efficient than regular recursive calls

See Also: fn, loop"""


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
