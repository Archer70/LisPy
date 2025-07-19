from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from ..decorators import lispy_function, lispy_documentation
import threading
import time


@lispy_function("timeout")
def timeout(args, env):
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
            (then (fn [msg] (println msg))))
    """
    if len(args) < 1 or len(args) > 2:
        raise EvaluationError(
            f"SyntaxError: 'timeout' expects 1 or 2 arguments (ms [value]), got {len(args)}."
        )

    ms = args[0]
    value = args[1] if len(args) > 1 else None

    # Validate milliseconds argument
    if not isinstance(ms, (int, float)):
        raise EvaluationError(
            f"TypeError: 'timeout' milliseconds must be a number, got {type(ms).__name__}."
        )

    if ms < 0:
        raise EvaluationError(
            "ValueError: 'timeout' milliseconds cannot be negative."
        )

    # Create promise that will resolve after the timeout
    timeout_promise = LispyPromise()

    def timeout_resolver():
        """Resolve the promise after the specified delay."""
        try:
            # Sleep for the specified duration (convert ms to seconds)
            time.sleep(ms / 1000.0)
            timeout_promise.resolve(value)
        except Exception as e:
            timeout_promise.reject(f"timeout error: {str(e)}")

    # Start timeout in background thread
    thread = threading.Thread(target=timeout_resolver, daemon=True)
    thread.start()

    return timeout_promise


@lispy_documentation("timeout")
def timeout_doc():
    return """Function: timeout
Arguments: (timeout milliseconds [value])
Description: Creates a promise that resolves after a specified delay.

Examples:
  ; Basic timeout
  (timeout 1000)           ; => Promise resolves to nil after 1 second
  (timeout 500 "done")     ; => Promise resolves to "done" after 500ms
  
  ; With chaining
  (-> (timeout 1000 "ready")
      (then (fn [msg] (println msg))))
  
  ; Async delay
  (async
    (println "Starting...")
    (await (timeout 2000))
    (println "2 seconds later"))
  
  ; Racing with other operations
  (promise-race [(fetch-data)
                 (timeout 5000 (reject "timeout"))])

Notes:
  - Requires 1-2 arguments (milliseconds, optional value)
  - Milliseconds must be a non-negative number
  - Default resolve value is nil if not specified
  - Useful for delays, timeouts, and testing
  - Can be combined with promise-race for timeout patterns
  - Non-blocking - runs in background thread"""
