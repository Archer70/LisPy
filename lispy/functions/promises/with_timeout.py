from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from lispy.functions.promises.timeout import builtin_timeout


def builtin_with_timeout(args, env):
    """Wrap a promise with a timeout and fallback value.

    Usage: (with-timeout promise fallback-value timeout-ms)

    Args:
        promise: The promise to wrap with timeout
        fallback-value: Value to resolve with if timeout occurs
        timeout-ms: Timeout in milliseconds

    Returns:
        A promise that resolves with either the original promise's value
        or the fallback value if timeout occurs

    Examples:
        (with-timeout (fetch-data) "default" 5000)
        ; => Resolves with fetch-data result or "default" after 5 seconds
        
        ; Thread-first usage:
        (-> (fetch-user-data user-id)
            (with-timeout "guest-user" 3000)
            (promise-then render-user))
            
        ; Chaining multiple timeouts:
        (-> (primary-api-call)
            (with-timeout nil 2000)
            (promise-then (fn [result] 
              (if result 
                result 
                (backup-api-call))))
            (with-timeout "fallback-data" 5000))
    """
    if len(args) != 3:
        raise EvaluationError(
            f"SyntaxError: 'with-timeout' expects 3 arguments (promise fallback-value timeout-ms), got {len(args)}."
        )
    
    promise = args[0]
    fallback_value = args[1]
    timeout_ms = args[2]
    
    # Validate promise argument
    if not isinstance(promise, LispyPromise):
        raise EvaluationError(
            f"TypeError: 'with-timeout' first argument must be a promise, got {type(promise).__name__}."
        )
    
    # Validate timeout argument
    if not isinstance(timeout_ms, (int, float)):
        raise EvaluationError(
            f"TypeError: 'with-timeout' third argument (timeout-ms) must be a number, got {type(timeout_ms).__name__}."
        )
    
    if timeout_ms < 0:
        raise EvaluationError(
            f"ValueError: 'with-timeout' timeout-ms must be non-negative, got {timeout_ms}."
        )
    
    # Create timeout promise that rejects with timeout signal
    timeout_promise = builtin_timeout([timeout_ms, "TIMEOUT_SIGNAL"], env)
    
    # Create new promise for the result
    result_promise = LispyPromise()
    
    # Track which promise resolves first
    resolved = [False]  # Use list for mutable reference
    
    def handle_original_resolution():
        """Handle resolution of the original promise."""
        if not resolved[0]:
            resolved[0] = True
            if promise.state == "resolved":
                result_promise.resolve(promise.value)
            elif promise.state == "rejected":
                result_promise.reject(promise.error)
    
    def handle_timeout_resolution():
        """Handle timeout resolution."""
        if not resolved[0]:
            resolved[0] = True
            result_promise.resolve(fallback_value)
    
    # Set up handlers for both promises
    if promise.state == "pending":
        promise.callbacks.append(handle_original_resolution)
    else:
        # Promise already settled
        handle_original_resolution()
        return result_promise
    
    if timeout_promise.state == "pending":
        timeout_promise.callbacks.append(handle_timeout_resolution)
    else:
        # Timeout already occurred (shouldn't happen with our implementation)
        handle_timeout_resolution()
    
    return result_promise


def documentation_with_timeout() -> str:
    """Returns documentation for the with-timeout function."""
    return """Function: with-timeout
Arguments: (with-timeout promise fallback-value timeout-ms)
Description: Wraps a promise with a timeout and fallback value.

Examples:
  (with-timeout (fetch-data) "default" 5000)
  ; => Resolves with fetch-data result or "default" after 5 seconds
  
  (with-timeout (slow-query) [] 2000)
  ; => Resolves with query result or empty list after 2 seconds
  
  ; Thread-first usage (timeout argument last for chaining):
  (-> (fetch-user-data user-id)
      (with-timeout "guest-user" 3000)
      (promise-then render-user))
  
  ; Multiple fallback layers:
  (-> (primary-api-call)
      (with-timeout nil 2000)           ; Fast timeout for primary
      (promise-then (fn [result] 
        (if result 
          result 
          (backup-api-call))))
      (with-timeout "fallback-data" 5000)) ; Longer timeout for backup
  
  ; Error handling with timeouts:
  (-> (risky-operation)
      (with-timeout "safe-default" 3000)
      (on-reject (fn [err] "error-fallback"))
      (promise-then process-result))

Notes:
  - First argument must be a promise
  - Second argument is the fallback value (any LisPy value)
  - Third argument is timeout in milliseconds (non-negative number)
  - Returns immediately with a new promise
  - If original promise resolves/rejects before timeout: uses original result
  - If timeout occurs first: resolves with fallback value
  - Timeout argument is last to enable thread-first chaining
  - Original promise errors are preserved (not converted to fallback)
  - Useful for preventing hanging operations with graceful degradation
  - Similar to Promise.race([promise, timeout]) but with automatic fallback
""" 