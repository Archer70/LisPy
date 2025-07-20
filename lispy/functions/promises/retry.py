import threading
import time

from lispy.closure import Function
from lispy.environment import Environment
from lispy.evaluator import evaluate
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import LispyPromise


@lispy_function("retry")
def retry(args, env):
    """Retry a function that may fail with exponential backoff.

    Usage: (retry operation max-attempts delay)

    Args:
        operation: Function to retry (must return a value or promise)
        max-attempts: Maximum number of attempts (must be positive integer)
        delay: Initial delay between attempts in milliseconds (must be non-negative)

    Returns:
        A promise that resolves with the operation's result if successful,
        or rejects with the final error if all attempts fail.

    Examples:
        ; Retry a simple operation
        (retry (fn [] (fetch-data)) 3 1000)
        ; => Tries up to 3 times with 1 second delays

        ; Retry with exponential backoff
        (retry unreliable-api-call 5 500)
        ; => Tries: 0ms, 500ms, 1000ms, 2000ms, 4000ms delays

        ; Handle both sync and async operations
        (retry (fn [] (if (< (random) 0.7) (throw "Failed") "Success")) 3 100)

        ; Thread-first usage:
        (-> (retry api-call 3 1000)
            (promise-then process-result)
            (on-reject handle-error))
    """
    if len(args) != 3:
        raise EvaluationError(
            f"SyntaxError: 'retry' expects 3 arguments (operation max-attempts delay), got {len(args)}."
        )

    operation = args[0]
    max_attempts = args[1]
    delay = args[2]

    # Validate operation argument
    is_user_defined_fn = isinstance(operation, Function)
    is_builtin_fn = callable(operation) and not is_user_defined_fn

    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError(
            f"TypeError: 'retry' first argument must be a function, got {type(operation).__name__}."
        )

    # Validate max_attempts argument
    if not isinstance(max_attempts, int):
        raise EvaluationError(
            f"TypeError: 'retry' second argument (max-attempts) must be an integer, got {type(max_attempts).__name__}."
        )

    if max_attempts < 1:
        raise EvaluationError(
            f"ValueError: 'retry' max-attempts must be positive, got {max_attempts}."
        )

    # Validate delay argument
    if not isinstance(delay, (int, float)):
        raise EvaluationError(
            f"TypeError: 'retry' third argument (delay) must be a number, got {type(delay).__name__}."
        )

    if delay < 0:
        raise EvaluationError(
            f"ValueError: 'retry' delay must be non-negative, got {delay}."
        )

    # Validate operation arity for user-defined functions (should be zero-argument)
    if is_user_defined_fn and len(operation.params) != 0:
        raise EvaluationError(
            f"TypeError: 'retry' operation must take 0 arguments, got {len(operation.params)}."
        )

    # Create promise for the retry operation
    retry_promise = LispyPromise()

    def execute_operation():
        """Execute the operation and return result or raise exception."""
        if is_user_defined_fn:
            # Call user-defined function
            call_env = Environment(outer=operation.defining_env)
            # No parameters to bind since it's a zero-argument function

            # Execute the function body
            result = None
            for expr in operation.body:
                result = evaluate(expr, call_env)
            return result
        else:
            # Call built-in function
            return operation([], env)

    def retry_loop():
        """Main retry logic running in background thread."""
        try:
            current_delay = delay
            last_error = None

            for attempt in range(max_attempts):
                try:
                    # Add delay before retry (except for first attempt)
                    if attempt > 0 and current_delay > 0:
                        time.sleep(current_delay / 1000.0)  # Convert ms to seconds

                    # Execute the operation
                    result = execute_operation()

                    # Handle the result
                    if isinstance(result, LispyPromise):
                        # Operation returned a promise - wait for it
                        while result.state == "pending":
                            time.sleep(0.001)  # Small sleep to avoid busy waiting

                        if result.state == "resolved":
                            retry_promise.resolve(result.value)
                            return
                        elif result.state == "rejected":
                            last_error = result.error
                            # Continue to next attempt
                        else:
                            # This shouldn't happen, but handle gracefully
                            last_error = f"Promise in unexpected state: {result.state}"
                    else:
                        # Operation returned a value directly - success!
                        retry_promise.resolve(result)
                        return

                except Exception as e:
                    # Operation threw an exception
                    last_error = str(e)
                    # Continue to next attempt

                # Exponential backoff for next attempt
                current_delay *= 2

            # All attempts failed - reject with the last error
            if last_error:
                retry_promise.reject(
                    f"RetryError: Failed after {max_attempts} attempts. Last error: {last_error}"
                )
            else:
                retry_promise.reject(
                    f"RetryError: Failed after {max_attempts} attempts with unknown error."
                )

        except Exception as e:
            # Unexpected error in retry logic itself
            retry_promise.reject(
                f"RetryError: Unexpected error in retry logic: {str(e)}"
            )

    # Start retry loop in background thread
    retry_thread = threading.Thread(target=retry_loop, daemon=True)
    retry_thread.start()

    return retry_promise


@lispy_documentation("retry")
def retry_documentation():
    return """Function: retry
Arguments: (retry operation max-attempts delay)
Description: Retries a function that may fail with exponential backoff delays.

The retry function attempts to execute an operation multiple times with
increasing delays between attempts (exponential backoff). If the operation
succeeds on any attempt, the promise resolves with the result. If all
attempts fail, the promise rejects with details about the final failure.

Arguments:
  - operation: Function to retry (must take 0 arguments)
  - max-attempts: Maximum number of attempts (positive integer)
  - delay: Initial delay between attempts in milliseconds (non-negative number)

Delay Pattern:
  - 1st attempt: immediate (no delay)
  - 2nd attempt: delay ms
  - 3rd attempt: delay * 2 ms
  - 4th attempt: delay * 4 ms
  - etc. (exponential backoff)

Examples:
  ; Basic retry with 3 attempts and 1 second initial delay
  (retry (fn [] (fetch-unreliable-data)) 3 1000)
  ; Attempts at: 0ms, 1000ms, 2000ms
  
  ; Retry API call with shorter delays
  (retry api-call 5 200)
  ; Attempts at: 0ms, 200ms, 400ms, 800ms, 1600ms
  
  ; Handle both successful and failed cases
  (-> (retry (fn [] (random-success-or-failure)) 3 500)
      (promise-then (fn [result] (println "Success:" result)))
      (on-reject (fn [error] (println "All attempts failed:" error))))
  
  ; Retry with immediate resolution (no delay needed)
  (retry (fn [] "always-works") 1 0)
  
  ; Complex operation with promise return
  (retry (fn [] (-> (fetch-data)
                    (promise-then validate-data)
                    (promise-then process-data))) 3 1000)

Error Handling:
  - Operation can throw exceptions or return rejected promises
  - All failure types are handled consistently
  - Final error includes attempt count and last error message
  - Unexpected retry logic errors are also handled gracefully

Use Cases:
  - Network requests that may fail intermittently
  - Database connections that may timeout
  - File operations that may encounter temporary locks
  - External API calls with rate limiting or temporary failures
  - Any operation where transient failures are expected

Notes:
  - Operation must be a zero-argument function
  - Operation can return values directly or promises
  - Uses exponential backoff to avoid overwhelming failing services
  - Runs asynchronously in background thread
  - Compatible with promise chaining and thread-first (->) operator
  - Similar to retry patterns in JavaScript/Node.js libraries
"""
