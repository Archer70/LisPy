import time
from typing import List, Any, Callable
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise


def documentation_await():
    """Returns documentation for the 'await' special form."""
    return """Special Form: await
Arguments: (await promise-expr)
Description: Waits for a promise to resolve and returns its resolved value.

Examples:
  (await (timeout 1000 "done"))           ; Waits 1 second, returns "done"
  (await (promise (fn [] (+ 1 2))))       ; Returns 3 after async execution
  (async (await (resolve "immediate")))   ; Returns "immediate" immediately
  (async 
    (define p (timeout 500 42))
    (await p))                            ; Define promise, then await it

Notes:
  - Can only be used with promise objects
  - Blocks execution until promise resolves or rejects
  - Returns the resolved value on success
  - Throws exception if promise rejects
  - Must be used within an async context
  - Integrates with async event loop when available

See Also: async, promise, timeout, resolve, reject"""


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
