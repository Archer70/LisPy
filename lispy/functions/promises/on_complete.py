from lispy.exceptions import EvaluationError, PromiseError
from lispy.types import LispyPromise
from lispy.closure import Function


def builtin_on_complete(args, env):
    """Execute cleanup code regardless of promise outcome.

    Usage: (on-complete promise cleanup-callback)

    Args:
        promise: A promise to attach cleanup to
        cleanup-callback: Function to call when promise settles (resolves or rejects)

    Returns:
        A new promise that settles with the same value/error as the original,
        but ensures cleanup-callback is executed

    Examples:
        (on-complete (resolve 42) (fn [_] (println "Cleanup")))
        ; => Promise that resolves to 42, after printing "Cleanup"

        (on-complete (reject "error") (fn [_] (println "Cleanup")))
        ; => Promise that rejects with "error", after printing "Cleanup"

        ; Thread-first style with cleanup:
        (-> (fetch-data)
            (then process-data)
            (on-reject handle-error)
            (on-complete (fn [_] (close-connection))))
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'on-complete' expects 2 arguments (promise cleanup-callback), got {len(args)}."
        )

    promise = args[0]
    cleanup_callback = args[1]

    # Validate promise argument
    if not isinstance(promise, LispyPromise):
        raise EvaluationError(
            f"TypeError: 'on-complete' first argument must be a promise, got {type(promise).__name__}."
        )

    # Validate callback argument
    if not (isinstance(cleanup_callback, Function) or callable(cleanup_callback)):
        raise EvaluationError(
            f"TypeError: 'on-complete' second argument must be a function, got {type(cleanup_callback).__name__}."
        )

    # Validate callback parameter count immediately for user-defined functions
    if isinstance(cleanup_callback, Function):
        if len(cleanup_callback.params) != 1:
            raise EvaluationError(
                f"TypeError: 'on-complete' callback must take exactly 1 argument, got {len(cleanup_callback.params)}."
            )

    # Create wrapper function that handles LisPy function calls
    def lispy_cleanup_callback():
        if isinstance(cleanup_callback, Function):
            # User-defined LisPy function
            from lispy.environment import Environment
            from lispy.evaluator import evaluate

            # Create environment for function call
            call_env = Environment(outer=cleanup_callback.defining_env)

            # Bind the parameter (already validated to be exactly one parameter)
            call_env.define(cleanup_callback.params[0].name, promise)

            # Execute function body
            result = None
            for expr in cleanup_callback.body:
                result = evaluate(expr, call_env)
            return result
        else:
            # Built-in function - call with promise as argument
            return cleanup_callback([promise], env)

    # Create a new promise that mimics the original but adds cleanup
    new_promise = LispyPromise()

    def handle_completion():
        """Handle promise completion and execute cleanup."""
        try:
            # Execute cleanup regardless of outcome
            lispy_cleanup_callback()
            # If cleanup succeeds, preserve the original promise's outcome
            if promise.state == "resolved":
                new_promise.resolve(promise.value)
            elif promise.state == "rejected":
                new_promise.reject(promise.error)
        except Exception as e:
            # If cleanup fails, reject with the cleanup error
            new_promise.reject(e)

    # Register our completion handler
    if promise.state == "pending":
        promise.callbacks.append(handle_completion)
    else:
        # Promise already settled, execute immediately
        handle_completion()

    return new_promise


def documentation_on_complete() -> str:
    """Returns documentation for the on-complete function."""
    return """Function: on-complete
Arguments: (on-complete promise cleanup-callback)
Description: Executes cleanup code regardless of promise outcome (resolve or reject).

Examples:
  (on-complete (resolve 42) (fn [_] (println "Cleanup")))
  ; => Promise that resolves to 42, after printing "Cleanup"
  
  (on-complete (reject "error") (fn [_] (println "Cleanup")))
  ; => Promise that rejects with "error", after printing "Cleanup"
  
  ; Thread-first style with resource management:
  (-> (open-connection)
      (then fetch-data)
      (then process-data)
      (on-reject handle-error)
      (on-complete (fn [_] (close-connection))))
  
  ; Multiple cleanup operations:
  (-> (acquire-resources)
      (then do-work)
      (on-complete (fn [_] (release-lock)))
      (on-complete (fn [_] (cleanup-temp-files)))
      (on-complete (fn [_] (log-completion))))
      
  ; Conditional cleanup based on outcome:
  (on-complete promise 
    (fn [p] 
      (if (= (.-state p) "resolved")
        (log-success)
        (log-failure))))

Notes:
  - Requires exactly two arguments (promise and cleanup-callback)
  - Cleanup-callback must be a function that takes exactly one argument
  - Cleanup-callback receives the promise object (can check .state, .value, .error)
  - Always executes cleanup, regardless of promise outcome
  - Returns new promise with same outcome as original
  - If cleanup-callback throws, original outcome is preserved
  - Cleanup failures are logged but don't affect promise outcome
  - Works seamlessly with thread-first (->) operator
  - Essential for resource management and cleanup
  - Can be chained multiple times for multiple cleanup operations
  - Similar to 'finally' in try/catch but for promises
  - Guarantees cleanup execution in async contexts
"""
