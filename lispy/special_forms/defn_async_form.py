from typing import List, Any, Callable
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, Symbol


def handle_defn_async_form(
    expression: List[Any], env: Environment, evaluate_fn: Callable
) -> None:
    """
    Handle the 'defn-async' special form.

    Usage: (defn-async name [params] body...)

    Defines an async function that returns a promise.
    """
    if len(expression) < 4:
        raise EvaluationError(
            "SyntaxError: 'defn-async' expects at least 3 arguments (name, params, body...), got {}.".format(
                len(expression) - 1
            )
        )

    name = expression[1]
    params = expression[2]
    body = expression[3:]

    # Validate function name
    if not isinstance(name, Symbol):
        raise EvaluationError(
            "TypeError: 'defn-async' function name must be a symbol, got {}.".format(
                type(name).__name__
            )
        )

    # Validate parameters (accept both lists and vectors)
    if not isinstance(params, (list, tuple)):
        raise EvaluationError(
            "TypeError: 'defn-async' parameters must be a list or vector, got {}.".format(
                type(params).__name__
            )
        )

    for param in params:
        if not isinstance(param, Symbol):
            raise EvaluationError(
                "TypeError: 'defn-async' parameter must be a symbol, got {}.".format(
                    type(param).__name__
                )
            )

    def async_function(call_args: List[Any], call_env: Environment) -> LispyPromise:
        """The actual async function that gets called."""
        # Validate argument count
        if len(call_args) != len(params):
            raise EvaluationError(
                f"SyntaxError: '{name.name}' expects {len(params)} arguments, got {len(call_args)}."
            )

        # Create promise that executes function body
        def executor():
            # Create new environment for function execution
            local_env = Environment(call_env)

            # Bind parameters to arguments
            for param, arg in zip(params, call_args):
                local_env.define(param.name, arg)

            # Evaluate function body
            result = None
            for expr in body:
                result = evaluate_fn(expr, local_env)

            return result

        return LispyPromise(executor)

    # Define the async function in the environment
    env.define(name.name, async_function)
    return None  # defn-async returns nil
