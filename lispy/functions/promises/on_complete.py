from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from lispy.closure import Function
from ..decorators import lispy_function, lispy_documentation


@lispy_function("on-complete")
def on_complete(args, env):
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

    promise, cleanup_callback = args

    # Validate first argument is a promise
    if not isinstance(promise, LispyPromise):
        raise EvaluationError(
            f"TypeError: First argument to 'on-complete' must be a promise, got {type(promise).__name__}."
        )

    # Validate second argument is a function
    if not (callable(cleanup_callback) or isinstance(cleanup_callback, Function)):
        raise EvaluationError(
            f"TypeError: Second argument to 'on-complete' must be a function, got {type(cleanup_callback).__name__}."
        )

    # Create new promise that preserves original outcome but runs cleanup
    result_promise = LispyPromise()

    def execute_cleanup_and_preserve_outcome():
        """Execute cleanup callback and preserve original promise outcome."""
        try:
            # Execute cleanup callback (ignore its return value)
            if isinstance(cleanup_callback, Function):
                # User-defined LisPy function
                from lispy.environment import Environment
                from lispy.evaluator import evaluate

                # Create environment for function call
                call_env = Environment(outer=cleanup_callback.defining_env)
                
                # Bind parameter - cleanup callbacks typically take no meaningful argument
                if cleanup_callback.params:
                    call_env.define(cleanup_callback.params[0].name, None)

                # Execute function body
                for expr in cleanup_callback.body:
                    evaluate(expr, call_env)
            else:
                # Built-in function
                cleanup_callback([None], env)

        except Exception:
            # Ignore cleanup errors to preserve original promise outcome
            pass

        # Preserve original promise outcome
        if promise.state == "resolved":
            result_promise.resolve(promise.value)
        elif promise.state == "rejected":
            result_promise.reject(promise.error)

    # Set up to run cleanup when original promise settles
    if promise.state == "pending":
        # Promise still pending, attach callback
        promise.callbacks.append(execute_cleanup_and_preserve_outcome)
        promise.error_callbacks.append(execute_cleanup_and_preserve_outcome)
    else:
        # Promise already settled, run cleanup immediately
        execute_cleanup_and_preserve_outcome()

    return result_promise


@lispy_documentation("on-complete")
def on_complete_doc():
    return """Function: on-complete
Arguments: (on-complete promise cleanup-callback)
Description: Executes cleanup code regardless of promise outcome.

Examples:
  ; Basic cleanup
  (on-complete (resolve 42) (fn [_] (println "Cleanup")))
  ; => Promise that resolves to 42, after printing "Cleanup"
  
  ; Cleanup on error too
  (on-complete (reject "error") (fn [_] (println "Cleanup")))
  ; => Promise that rejects with "error", after printing "Cleanup"
  
  ; Resource management pattern
  (-> (open-connection)
      (then fetch-data)
      (then process-data)
      (on-reject handle-error)
      (on-complete (fn [_] (close-connection))))
  
  ; File handling with cleanup
  (-> (open-file "data.txt")
      (then read-contents)
      (then parse-data)
      (on-complete (fn [_] (close-file))))
  
  ; Multiple cleanup steps
  (-> (start-operation)
      (on-complete (fn [_] (stop-timer)))
      (on-complete (fn [_] (cleanup-temp-files)))
      (on-complete (fn [_] (log-completion))))

Notes:
  - Requires exactly 2 arguments (promise, cleanup-callback)
  - Cleanup callback is called regardless of success or failure
  - Original promise outcome (resolve/reject) is preserved
  - Cleanup callback errors are ignored to preserve original outcome
  - Essential for resource management and cleanup
  - Similar to finally block in try/catch
  - Can be chained multiple times for different cleanup tasks"""
