from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
import threading
import time


def builtin_delay(args, env):
    """Create a promise that resolves after a specified delay.

    Usage: (delay milliseconds value)

    Args:
        milliseconds: Number of milliseconds to wait
        value: Value to resolve with after the delay

    Returns:
        A promise that resolves with the given value after the specified delay

    Examples:
        (delay 1000 "hello") ; => Promise that resolves to "hello" after 1 second
        
        (async 
          (let [result (await (delay 500 42))]
            result)) ; => 42 (after 500ms delay)
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'delay' expects 2 arguments, got {len(args)}."
        )

    milliseconds_arg = args[0]
    value = args[1]

    # Validate milliseconds is a number
    if not isinstance(milliseconds_arg, (int, float)):
        raise EvaluationError(
            f"TypeError: 'delay' first argument must be a number, got {type(milliseconds_arg)}."
        )

    milliseconds = float(milliseconds_arg)
    
    # Validate milliseconds is non-negative
    if milliseconds < 0:
        raise EvaluationError(
            f"ValueError: 'delay' milliseconds must be non-negative, got {milliseconds}."
        )

    # Create the delay promise
    delay_promise = LispyPromise()

    def delayed_resolve():
        """Resolve the promise after the specified delay."""
        try:
            # Convert milliseconds to seconds for time.sleep
            time.sleep(milliseconds / 1000.0)
            delay_promise.resolve(value)
        except Exception as e:
            delay_promise.reject(e)

    # Start the delay in a background thread
    threading.Thread(target=delayed_resolve, daemon=True).start()
    
    return delay_promise


def documentation_delay() -> str:
    """Returns documentation for the delay function."""
    return """Function: delay
Arguments: (delay milliseconds value)
Description: Creates a promise that resolves with the given value after a specified delay.

Examples:
  ; Basic delay usage
  (delay 1000 "hello") ; => Promise that resolves to "hello" after 1 second
  
  ; Using with async/await
  (async
    (let [result (await (delay 500 42))]
      (println result))) ; Prints 42 after 500ms
  
  ; Zero delay (immediate resolution)
  (delay 0 "immediate") ; => Promise that resolves immediately
  
  ; Using in promise-race for timeouts
  (async
    (let [result (await (promise-race [
                          (some-long-operation)
                          (delay 5000 "timeout")]))]
      result)) ; => Either operation result or "timeout" after 5 seconds

Notes:
  - Requires exactly 2 arguments (milliseconds and value)
  - Milliseconds must be a non-negative number
  - Value can be any LisPy value
  - Returns a promise that resolves after the specified delay
  - Delay is implemented using background threads
  - Useful for timeouts, testing async behavior, and delays in sequences
  - Zero milliseconds resolves immediately but still asynchronously
  - Similar to setTimeout() in JavaScript but returns a promise
""" 