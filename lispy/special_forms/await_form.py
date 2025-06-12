import time
from typing import List, Any, Callable
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise


def handle_await_form(
    expression: List[Any], env: Environment, evaluate_fn: Callable
) -> Any:
    """
    Handle the 'await' special form.

    Usage: (await <promise-expression>)

    Waits for a promise to resolve and returns its value.
    """
    if len(expression) != 2:
        raise EvaluationError(
            "SyntaxError: 'await' expects exactly 1 argument (promise expression), got {}.".format(
                len(expression) - 1
            )
        )

    promise_expr = expression[1]
    promise = evaluate_fn(promise_expr, env)

    if not isinstance(promise, LispyPromise):
        raise EvaluationError(
            "TypeError: 'await' can only be used with promises, got {}.".format(
                type(promise).__name__
            )
        )

    # Get async context if available
    context = env.store.get("__async_context__")
    if context:
        # Register promise with context
        context.register_promise(promise)

    # Wait for promise to resolve
    while promise.state == "pending":
        time.sleep(0.001)  # Simple polling - could be improved with proper event loop

    if promise.state == "resolved":
        return promise.value
    elif promise.state == "rejected":
        raise EvaluationError(f"Promise rejected: {promise.error}")
    else:
        raise EvaluationError("Promise in unexpected state: {}".format(promise.state))
