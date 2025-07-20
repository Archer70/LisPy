"""
Loop special form for efficient local iteration with recur.

The loop form creates a lexical binding context and establishes a recursion point
that can be targeted by recur for efficient iteration without stack growth.

Usage: (loop [binding1 init1 binding2 init2 ...] body...)

Examples:
    (loop [n 10]
      (if (<= n 0)
        "done"
        (recur (- n 1))))

    (loop [items [1 2 3] result []]
      (if (empty? items)
        result
        (recur (rest items) (conj result (first items)))))
"""


def documentation_loop():
    """Returns documentation for the 'loop' special form."""
    return """Special Form: loop
Arguments: (loop [var1 init1 var2 init2 ...] body-expr1 body-expr2 ...)
Description: Creates a recursion point with local bindings. Use 'recur' to loop back with new values.

Examples:
  (loop [x 0] (if (< x 5) (recur (+ x 1)) x))  ; Returns 5 (counts to 5)
  (loop [acc 0 n 10] 
    (if (= n 0) acc (recur (+ acc n) (- n 1)))) ; Returns 55 (sum 1-10)
  (loop [items [1 2 3] result []]
    (if (empty? items) 
      result 
      (recur (rest items) (conj result (first items)))))  ; Copy list

Notes:
  - Creates local bindings like 'let'
  - Establishes a recursion point for 'recur'
  - 'recur' jumps back to loop with new binding values
  - Provides efficient tail-call optimization
  - Binding vector must have even number of elements
  - At least one body expression is required

See Also: recur, let, fn"""


from typing import Any, Callable, List

from ..environment import Environment
from ..exceptions import EvaluationError
from ..tail_call import TailCall
from ..types import Symbol


class LoopFunction:
    """
    A special function-like object that represents a loop context.
    This allows recur to target the loop instead of a regular function.
    """

    def __init__(self, binding_symbols: List[Symbol], body: List[Any]):
        self.params = binding_symbols  # Match Function interface for recur
        self.body = body
        self.defining_env = None  # Will be set during execution

    def __repr__(self) -> str:
        param_names = [p.name for p in self.params]
        return f"<LoopFunction bindings:({', '.join(param_names)})>"


def handle_loop_form(
    expression: List[Any], env: Environment, evaluate_fn: Callable
) -> Any:
    """
    Handle the loop special form for efficient local iteration.

    Syntax: (loop [binding1 init1 binding2 init2 ...] body...)

    Args:
        expression: The loop expression [loop, bindings, body...]
        env: The current environment
        evaluate_fn: Function to evaluate sub-expressions

    Returns:
        The result of the loop execution

    Raises:
        EvaluationError: If loop is used incorrectly
    """
    if len(expression) < 3:
        raise EvaluationError(
            "SyntaxError: 'loop' requires a bindings vector and at least one body expression. "
            "Usage: (loop [var val ...] body...)"
        )

    bindings_form = expression[1]
    if not isinstance(bindings_form, list):
        raise EvaluationError(
            f"SyntaxError: Bindings for 'loop' must be a vector/list, got {type(bindings_form).__name__}. "
            "Usage: (loop [var val ...] body...)"
        )

    if len(bindings_form) % 2 != 0:
        # Format the bindings list for better error messages
        formatted_bindings = [str(item) for item in bindings_form]
        raise EvaluationError(
            f"SyntaxError: Bindings in 'loop' must be in symbol-value pairs. "
            f"Found an odd number of elements in bindings vector: [{', '.join(formatted_bindings)}]. "
            "Usage: (loop [var val ...] body...)"
        )

    body_expressions = expression[2:]
    if not body_expressions:
        raise EvaluationError(
            "SyntaxError: 'loop' must have at least one expression in its body."
        )

    # Extract binding symbols and initial values
    binding_symbols = []
    init_expressions = []

    for i in range(0, len(bindings_form), 2):
        symbol_node = bindings_form[i]
        if not isinstance(symbol_node, Symbol):
            raise EvaluationError(
                f"SyntaxError: Variable in 'loop' binding must be a symbol, "
                f"got {type(symbol_node).__name__}: '{symbol_node}' at index {i} in bindings vector."
            )

        init_expr = bindings_form[i + 1]
        binding_symbols.append(symbol_node)
        init_expressions.append(init_expr)

    # Evaluate initial values in the outer environment
    initial_values = [evaluate_fn(init_expr, env) for init_expr in init_expressions]

    # Create the loop function object
    loop_function = LoopFunction(binding_symbols, body_expressions)
    loop_function.defining_env = env  # Set the outer environment

    # Execute the loop with trampoline (similar to function execution)
    return _execute_loop(loop_function, initial_values, evaluate_fn)


def _execute_loop(
    loop_function: LoopFunction, initial_values: List[Any], evaluate_fn: Callable
) -> Any:
    """
    Execute a loop with trampoline support for recur.

    This is similar to _execute_user_defined_function but for loops.
    """
    current_values = initial_values

    # Trampoline loop for explicit tail call optimization via recur
    while True:
        # Create a new environment for the loop iteration
        loop_env = Environment(outer=loop_function.defining_env)

        # Bind the loop function to a special variable for recur
        loop_env.define("__current_function__", loop_function)

        # Bind current values to loop variables
        for param_symbol, value in zip(loop_function.params, current_values):
            loop_env.define(param_symbol.name, value)

        # Evaluate body expressions sequentially in the loop environment
        result = None
        for body_expr in loop_function.body:
            result = evaluate_fn(body_expr, loop_env)

            # Check if the result is a TailCall (from recur)
            if isinstance(result, TailCall):
                # Tail call detected - continue loop with new values
                current_values = result.args
                break  # Break out of body evaluation loop, continue trampoline

        # If we get here without a TailCall, return the result
        if not isinstance(result, TailCall):
            return result
