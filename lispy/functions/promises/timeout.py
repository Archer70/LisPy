from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
import threading
import time


def builtin_timeout(args, env):
    """Create a promise that resolves after a specified timeout.

    Usage: (timeout ms)
           (timeout ms value)

    Args:
        ms: Number of milliseconds to wait
        value: Optional value to resolve with (defaults to nil)

    Returns:
        A promise that resolves with the given value after the timeout

    Examples:
        (timeout 1000)           ; => Promise that resolves to nil after 1 second
        (timeout 500 "done")     ; => Promise that resolves to "done" after 500ms
        
        ; Thread-first usage:
        (-> (timeout 1000 "ready")
            (promise-then (fn [msg] (println msg))))
    """
    if len(args) < 1 or len(args) > 2:
        raise EvaluationError(
            f"SyntaxError: 'timeout' expects 1 or 2 arguments (ms [value]), got {len(args)}."
        )
    
    ms = args[0]
    value = args[1] if len(args) > 1 else None
    
    # Validate timeout argument
    if not isinstance(ms, (int, float)):
        raise EvaluationError(
            f"TypeError: 'timeout' first argument (ms) must be a number, got {type(ms).__name__}."
        )
    
    if ms < 0:
        raise EvaluationError(
            f"ValueError: 'timeout' ms must be non-negative, got {ms}."
        )
    
    # Create promise that resolves after timeout
    promise = LispyPromise()
    
    def timeout_handler():
        """Handle timeout by resolving the promise."""
        time.sleep(ms / 1000.0)  # Convert ms to seconds
        promise.resolve(value)
    
    # Start timeout in background thread
    timeout_thread = threading.Thread(target=timeout_handler, daemon=True)
    timeout_thread.start()
    
    return promise


def documentation_timeout() -> str:
    """Returns documentation for the timeout function."""
    return """Function: timeout
Arguments: (timeout ms [value])
Description: Creates a promise that resolves after a specified timeout.

Examples:
  (timeout 1000)                    ; => Promise resolving to nil after 1 second
  (timeout 500 "done")              ; => Promise resolving to "done" after 500ms
  (timeout 0 "immediate")           ; => Promise resolving immediately
  
  ; Thread-first usage:
  (-> (timeout 1000 "ready")
      (promise-then (fn [msg] (println msg))))
  
  ; Racing with timeout:
  (promise-race (vector
                  (slow-operation)
                  (timeout 5000 "timeout")))
  
  ; Delay in promise chains:
  (-> (fetch-data)
      (promise-then process-data)
      (promise-then (fn [_] (timeout 1000)))  ; Wait 1 second
      (promise-then (fn [_] (send-notification))))

Notes:
  - First argument must be a non-negative number (milliseconds)
  - Second argument is optional (defaults to nil)
  - Returns immediately with a pending promise
  - Promise resolves after the specified delay
  - Useful for delays, timeouts, and rate limiting
  - Works seamlessly with thread-first (->) operator
  - Similar to JavaScript's setTimeout but returns a promise
  - Can be used with promise-race for timeout patterns
""" 