"""
LisPy doseq special form - Iterate over collections for side effects.

Usage: (doseq [binding collection] body...)

Examples:
  (doseq [x [1 2 3]] (println x))     ; Prints 1, 2, 3 on separate lines
  (doseq [item items] (process item)) ; Process each item for side effects
"""

from typing import List, Any, Callable
from ..types import Vector, LispyList, Symbol
from ..exceptions import EvaluationError
from ..environment import Environment


def documentation_doseq():
    """Returns documentation for the 'doseq' special form."""
    return """Special Form: doseq
Arguments: (doseq [binding collection] body-expr1 body-expr2 ...)
Description: Iterates over a collection, executing body for each element (for side effects).

Examples:
  (doseq [x [1 2 3]] (println x))         ; Prints: 1, 2, 3 (on separate lines)
  (doseq [item items] (process-item item)) ; Process each item
  (doseq [n (range 5)] (print n))         ; Prints: 0 1 2 3 4
  (doseq [line file-lines] 
    (println (str "Line: " line)))        ; Process file lines

Notes:
  - Used for side effects (printing, mutations, etc.)
  - Always returns nil
  - Binding symbol is available in body expressions
  - Creates new scope for binding variable
  - Collection must be a vector or list
  - Binding vector must have exactly 2 elements

See Also: map, for, let, loop"""


def handle_doseq_form(
    expression: List[Any], env: Environment, evaluate_fn: Callable
) -> None:
    """Handles the (doseq [binding collection] body...) special form.

    Iterates over a collection, binding each element to a variable and executing
    the body expressions for their side effects. Returns nil.

    Args:
        expression: List containing the doseq form:
            - expression[0]: 'doseq' symbol (already consumed)
            - expression[1]: Vector [binding collection] where binding is a symbol
            - expression[2:]: Body expressions to execute for each element
        env: The current environment
        evaluate_fn: Function to evaluate expressions

    Returns:
        None: Always returns nil (used for side effects)

    Raises:
        EvaluationError: If incorrect syntax or invalid argument types
    """
    if len(expression) < 3:
        raise EvaluationError(
            f"SyntaxError: 'doseq' expects at least 2 arguments ([binding collection] body...), got {len(expression) - 1}."
        )

    binding_vector = expression[1]
    body_expressions = expression[2:]

    # Validate binding vector
    if not isinstance(binding_vector, (Vector, LispyList, list)):
        raise EvaluationError(
            f"SyntaxError: 'doseq' first argument must be a vector [binding collection], got {type(binding_vector)}."
        )

    if len(binding_vector) != 2:
        raise EvaluationError(
            f"SyntaxError: 'doseq' binding vector must have exactly 2 elements [binding collection], got {len(binding_vector)}."
        )

    binding_symbol, collection_expr = binding_vector[0], binding_vector[1]

    # Validate binding symbol
    if not isinstance(binding_symbol, Symbol):
        raise EvaluationError(
            f"SyntaxError: 'doseq' binding must be a symbol, got {type(binding_symbol)}."
        )

    # Evaluate the collection expression
    collection = evaluate_fn(collection_expr, env)

    # Validate collection
    if not isinstance(collection, (Vector, LispyList)):
        raise EvaluationError(
            f"TypeError: 'doseq' collection must be a vector or list, got {type(collection)}."
        )

    # Create a new environment for the loop
    loop_env = Environment(outer=env)

    # Iterate over collection and execute body for each element
    for item in collection:
        # Bind the current item to the binding symbol
        loop_env.define(binding_symbol.name, item)

        # Execute all body expressions (for side effects)
        for body_expr in body_expressions:
            evaluate_fn(body_expr, loop_env)

    # doseq returns nil
    return None
