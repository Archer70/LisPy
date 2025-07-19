from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from lispy.closure import Function
from ..decorators import lispy_function, lispy_documentation


@lispy_function("on-reject")
def on_reject(args, env):
    """Handle promise rejection with a callback.

    Usage: (on-reject promise error-callback)

    Args:
        promise: A promise to handle errors for
        error-callback: Function to call with the rejection reason

    Returns:
        A new promise that resolves with the error-callback's return value
        if the original promise rejects, or resolves with the original value
        if it succeeds

    Examples:
        (on-reject (reject "error") (fn [err] (str "Handled: " err)))
        ; => Promise that resolves to "Handled: error"

        (on-reject (resolve 42) (fn [err] "not called"))
        ; => Promise that resolves to 42

        ; Thread-first style error handling:
        (-> (fetch-user-data)
            (then extract-user-name)
            (on-reject (fn [err] "Unknown User"))
            (then display-user-name))
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'on-reject' expects 2 arguments (promise error-callback), got {len(args)}."
        )

    promise, error_callback = args

    # Validate first argument is a promise
    if not isinstance(promise, LispyPromise):
        raise EvaluationError(
            f"TypeError: First argument to 'on-reject' must be a promise, got {type(promise).__name__}."
        )

    # Validate second argument is a function
    if not (callable(error_callback) or isinstance(error_callback, Function)):
        raise EvaluationError(
            f"TypeError: Second argument to 'on-reject' must be a function, got {type(error_callback).__name__}."
        )

    # Use the promise's catch method to handle errors
    return promise.catch(error_callback, env)


@lispy_documentation("on-reject")
def on_reject_doc():
    return """Function: on-reject
Arguments: (on-reject promise error-callback)
Description: Handles promise rejection with a callback, returning recovery value.

Examples:
  ; Basic error handling
  (on-reject (reject "error") (fn [err] (str "Handled: " err)))
  ; => Promise that resolves to "Handled: error"
  
  ; Success passes through unchanged
  (on-reject (resolve 42) (fn [err] "not called"))
  ; => Promise that resolves to 42
  
  ; Thread-first error handling chain
  (-> (fetch-user-data)
      (then extract-user-name)
      (on-reject (fn [err] "Unknown User"))
      (then display-user-name))
  
  ; Multiple error handlers
  (-> (risky-operation)
      (on-reject (fn [err] 
        (if (= err "network-error")
          (retry-operation)
          "fallback-value")))
  
  ; With async/await
  (async
    (let [result (await (on-reject (fetch-data)
                                   (fn [err] "default-data")))]
      (process result)))

Notes:
  - Requires exactly 2 arguments (promise, error-callback)
  - Error callback receives the rejection reason as its argument
  - If promise resolves, callback is not called and value passes through
  - If promise rejects, callback is called and its return value becomes new resolution
  - Essential for error recovery and graceful degradation
  - Can be chained with other promise operations
  - Similar to .catch() in JavaScript promises"""
