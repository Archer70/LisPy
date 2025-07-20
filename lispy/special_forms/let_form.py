# lispy_project/lispy/special_forms/let_form.py
from typing import Any, Callable, List

from ..environment import Environment
from ..exceptions import EvaluationError
from ..types import Symbol


def documentation_let():
    """Returns documentation for the 'let' special form."""
    return """Special Form: let
Arguments: (let [var1 val1 var2 val2 ...] body-expr1 body-expr2 ...)
Description: Creates local variable bindings and evaluates body expressions in that scope.

Examples:
  (let [x 5] x)                    ; Returns 5 (simple binding)
  (let [x 5 y 10] (+ x y))         ; Returns 15 (multiple bindings)
  (let [x 5 y (* x 2)] y)          ; Returns 10 (sequential binding, y uses x)
  (let [name "Alice"] (str "Hello, " name))  ; Returns "Hello, Alice"
  (let [x 1] (let [y 2] (+ x y)))  ; Returns 3 (nested let expressions)
  (let [x 5] (print "x is" x) (* x 2))  ; Returns 10 (multiple body expressions)

Notes:
  - Bindings are evaluated sequentially (let* semantics)
  - Later bindings can reference earlier ones
  - Variables are scoped to the let expression
  - Binding vector must have even number of elements
  - At least one body expression is required

See Also: define, fn"""


def handle_let_form(
    expression: List[Any], env: Environment, evaluate_fn: Callable
) -> Any:
    """Handles the (let [var1 init1 var2 init2 ...] body1 ...) special form (let* semantics)."""
    if len(expression) < 3:
        raise EvaluationError(
            "SyntaxError: 'let' requires a bindings vector and at least one body expression. Usage: (let [var val ...] body ...)"
        )

    bindings_form = expression[1]
    # Assuming the parser provides the [...] form as a Python list.
    if not isinstance(bindings_form, list):
        raise EvaluationError(
            f"SyntaxError: Bindings for 'let' must be a vector/list, got {type(bindings_form).__name__}. Usage: (let [var val ...] body ...)"
        )

    if len(bindings_form) % 2 != 0:
        raise EvaluationError(
            f"SyntaxError: Bindings in 'let' must be in symbol-value pairs. Found an odd number of elements in bindings vector: {bindings_form}. Usage: (let [var val ...] body ...)"
        )

    body_expressions = expression[2:]
    if not body_expressions:
        raise EvaluationError(
            "SyntaxError: 'let' must have at least one expression in its body."
        )

    # Create a new environment for the let bindings. For let*, initializers are evaluated
    # in an environment that includes preceding bindings from the same let.
    let_env = Environment(outer=env)

    for i in range(0, len(bindings_form), 2):
        symbol_node = bindings_form[i]
        if not isinstance(symbol_node, Symbol):
            raise EvaluationError(
                f"SyntaxError: Variable in 'let' binding must be a symbol, got {type(symbol_node).__name__}: '{symbol_node}' at index {i} in bindings vector."
            )

        init_expr = bindings_form[i + 1]

        # Evaluate the initializer in the current state of let_env (let* behavior)
        value = evaluate_fn(init_expr, let_env)

        # Define the symbol in the let_env, making it available for subsequent initializers
        let_env.define(symbol_node.name, value)

    # Evaluate body expressions in the final let_env
    result = None
    for body_expr in body_expressions:
        result = evaluate_fn(body_expr, let_env)

    return result
