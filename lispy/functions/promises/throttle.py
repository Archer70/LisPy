from lispy.exceptions import EvaluationError
from lispy.closure import Function
from ..decorators import lispy_function, lispy_documentation
import threading
import time


@lispy_function("throttle")
def throttle(args, env):
    """Create a throttled version of a function (rate limiting).

    Usage: (throttle fn rate)

    Args:
        fn: Function to throttle
        rate: Minimum time between executions in milliseconds

    Returns:
        A new function that will execute at most once per rate period.
        The first call executes immediately. Subsequent calls within the
        rate period are ignored. After the rate period expires, the next
        call will execute immediately.

    Examples:
        (define api-throttled (throttle api-call 1000))
        (api-throttled "query")    ; Executes immediately
        (api-throttled "query2")   ; Ignored if within 1000ms
        
        ; Common use case for rate limiting:
        (define handle-scroll (throttle 
                                (fn [] (println "Scroll event"))
                                100))
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'throttle' expects 2 arguments (fn rate), got {len(args)}."
        )

    fn = args[0]
    rate = args[1]

    # Validate function argument
    from lispy.evaluator import evaluate
    is_user_defined_fn = isinstance(fn, Function)
    is_builtin_fn = callable(fn) and not is_user_defined_fn
    
    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError(
            f"TypeError: 'throttle' first argument must be a function, got {type(fn).__name__}."
        )

    # Validate rate argument
    if not isinstance(rate, (int, float)):
        raise EvaluationError(
            f"TypeError: 'throttle' second argument (rate) must be a number, got {type(rate).__name__}."
        )

    if rate < 0:
        raise EvaluationError(
            f"ValueError: 'throttle' rate must be non-negative, got {rate}."
        )

    # State for the throttled function
    state = {
        'last_execution_time': 0,
        'lock': threading.Lock()
    }
    
    def throttled_function(inner_args, inner_env):
        """The throttled version of the original function."""
        
        with state['lock']:
            current_time = time.time() * 1000  # Convert to milliseconds
            time_since_last = current_time - state['last_execution_time']
            
            # Check if enough time has passed since last execution
            if time_since_last >= rate:
                # Update last execution time
                state['last_execution_time'] = current_time
                
                # Execute the original function
                try:
                    if is_user_defined_fn:
                        # Call user-defined function
                        from lispy.environment import Environment
                        
                        # Validate argument count
                        if len(inner_args) != len(fn.params):
                            raise PromiseError(f"Throttled function expects {len(fn.params)} arguments, got {len(inner_args)}.")
                        
                        # Create new environment for function execution using the function's defining environment
                        call_env = Environment(outer=fn.defining_env)
                        
                        # Bind parameters to arguments
                        for param, arg in zip(fn.params, inner_args):
                            call_env.define(param.name, arg)
                        
                        # Execute function body
                        result = None
                        for expr in fn.body:
                            result = evaluate(expr, call_env)
                        return result
                    else:
                        # Call built-in function
                        return fn(inner_args, inner_env)
                except Exception as e:
                    # Re-raise as PromiseError to maintain error context
                    raise PromiseError(f"Throttled function execution failed: {e}")
            else:
                # Within rate period - ignore the call
                return None

    # Return the throttled function as a callable
    return throttled_function


@lispy_documentation("throttle")
def throttle_doc():
    return """Function: throttle
Arguments: (throttle fn rate)
Description: Creates a throttled version of a function that executes at most once per rate period.

The throttled function implements rate limiting by allowing execution only when
enough time has passed since the last execution. The first call always executes
immediately. Subsequent calls within the rate period are ignored completely.

Arguments:
  - fn: Function to throttle (must be callable)
  - rate: Minimum time between executions in milliseconds (non-negative number)

Behavior:
  - 1st call: Executes immediately
  - Subsequent calls: Ignored until rate period expires
  - After rate period: Next call executes immediately
  - No queuing or delayed execution (unlike debounce)

Examples:
  ; Basic throttling with 1 second rate limit
  (define api-throttled (throttle api-call 1000))
  (api-throttled "request1")    ; Executes immediately
  (api-throttled "request2")    ; Ignored (within 1000ms)
  ; ... wait 1000ms ...
  (api-throttled "request3")    ; Executes immediately
  
  ; Scroll event throttling
  (define handle-scroll (throttle 
                          (fn [] (println "Processing scroll"))
                          100))
  
  ; Button click protection
  (define save-throttled (throttle save-data 2000))
  (save-throttled)              ; Saves immediately
  (save-throttled)              ; Ignored (within 2 seconds)
  
  ; API rate limiting
  (define rate-limited-fetch (throttle 
                               (fn [url] (fetch-data url))
                               500))

Throttle vs Debounce:
  - Throttle: Rate limiting - executes at most once per period
  - Debounce: Delay execution until quiet period
  
  - Throttle: First call executes immediately
  - Debounce: First call is delayed
  
  - Throttle: Subsequent calls are ignored
  - Debounce: Subsequent calls reset the delay timer

Use Cases:
  - API rate limiting (respect rate limits)
  - Scroll/resize event handlers (performance optimization)
  - Button click protection (prevent rapid clicking)
  - Mouse move handlers (reduce event frequency)
  - Search suggestions (limit query frequency)
  - Auto-save functionality (don't save too often)

Notes:
  - First argument must be a function
  - Second argument must be a non-negative number (milliseconds)
  - Returns a new function with throttling behavior
  - Throttled function returns result for executed calls, nil for ignored calls
  - Thread-safe implementation using locks
  - No memory of ignored calls (unlike debounce which can cancel/reset)
  - Similar to rate limiting in JavaScript libraries
  - Complements debounce for different use cases
""" 