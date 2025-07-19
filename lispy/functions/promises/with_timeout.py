from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from ..decorators import lispy_function, lispy_documentation
from .timeout import timeout


@lispy_function("with-timeout")
def with_timeout(args, env):
    """Wrap a promise with a timeout and fallback value.

    Usage: (with-timeout promise timeout-ms fallback-value)

    Args:
        promise: The promise to wrap with timeout
        timeout-ms: Timeout in milliseconds
        fallback-value: Value to resolve with if timeout occurs

    Returns:
        A promise that resolves with either the original promise's value
        or the fallback value if timeout occurs

    Examples:
        (with-timeout (fetch-data) 5000 "default")
        ; => Resolves with fetch-data result or "default" after 5 seconds

        ; Thread-first usage:
        (-> (fetch-user-data user-id)
            (with-timeout 3000 "guest-user")
            (then render-user))

        ; Chaining multiple timeouts:
        (-> (primary-api-call)
            (with-timeout 2000 nil)
            (then (fn [result] (or result (backup-api-call)))))
    """
    if len(args) != 3:
        raise EvaluationError(
            f"SyntaxError: 'with-timeout' expects 3 arguments (promise timeout-ms fallback-value), got {len(args)}."
        )

    promise, timeout_ms, fallback_value = args

    # Validate first argument is a promise
    if not isinstance(promise, LispyPromise):
        raise EvaluationError(
            f"TypeError: First argument to 'with-timeout' must be a promise, got {type(promise).__name__}."
        )

    # Validate timeout argument
    if not isinstance(timeout_ms, (int, float)):
        raise EvaluationError(
            f"TypeError: Second argument to 'with-timeout' (timeout-ms) must be a number, got {type(timeout_ms).__name__}."
        )

    if timeout_ms < 0:
        raise EvaluationError(
            "ValueError: 'with-timeout' timeout-ms cannot be negative."
        )

    # Create a timeout promise that rejects with a special timeout signal
    timeout_promise = timeout([timeout_ms, "TIMEOUT_SIGNAL"], env)

    # Race the original promise against the timeout
    from .promise_race import promise_race
    race_result = promise_race([promise, timeout_promise], env)

    # Transform the race result to handle timeout case
    def handle_race_result(result):
        if result == "TIMEOUT_SIGNAL":
            return fallback_value
        return result

    return race_result.then(handle_race_result)


@lispy_documentation("with-timeout")
def with_timeout_doc():
    return """Function: with-timeout
Arguments: (with-timeout promise timeout-ms fallback-value)
Description: Wraps a promise with a timeout and fallback value.

Examples:
  ; Basic timeout with fallback
  (with-timeout (fetch-data) 5000 "default")
  ; => Resolves with fetch-data result or "default" after 5 seconds
  
  ; User data with guest fallback
  (with-timeout (fetch-user-data user-id) 3000 "guest-user")
  
  ; Thread-first usage
  (-> (fetch-user-data user-id)
      (with-timeout 3000 "guest-user")
      (then render-user))
  
  ; Chaining with fallback logic
  (-> (primary-api-call)
      (with-timeout 2000 nil)
      (then (fn [result] (or result (backup-api-call)))))
  
  ; With async/await
  (async
    (let [data (await (with-timeout (slow-operation) 1000 "timeout"))]
      (if (= data "timeout")
        (println "Operation timed out")
        (println "Got result:" data))))

Notes:
  - Requires exactly 3 arguments (promise, timeout-ms, fallback-value)
  - Timeout-ms must be a non-negative number
  - If promise resolves before timeout, returns original value
  - If timeout occurs first, returns fallback-value
  - Useful for providing defaults when operations are slow
  - Essential for resilient applications
  - Can be chained with other promise operations"""
