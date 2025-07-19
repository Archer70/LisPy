from lispy.exceptions import EvaluationError
from lispy.closure import Function
from ..decorators import lispy_function, lispy_documentation
import threading
import time


@lispy_function("debounce")
def debounce(args, env):
    """Create a debounced version of a function.

    Usage: (debounce fn delay)

    Args:
        fn: Function to debounce
        delay: Delay in milliseconds

    Returns:
        A new function that will delay execution until delay ms have passed
        without being called again. If called again before delay expires,
        the previous call is cancelled and timer resets.

    Examples:
        (define search-debounced (debounce search-api 300))
        (search-debounced "query")    ; Will only execute if no more calls for 300ms
        
        ; Common use case for user input:
        (define handle-input (debounce 
                               (fn [text] (println "Searching for:" text))
                               500))
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'debounce' expects 2 arguments (fn delay), got {len(args)}."
        )

    fn = args[0]
    delay = args[1]

    # Validate function argument
    from lispy.evaluator import evaluate
    is_user_defined_fn = isinstance(fn, Function)
    is_builtin_fn = callable(fn) and not is_user_defined_fn
    
    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError(
            f"TypeError: 'debounce' first argument must be a function, got {type(fn).__name__}."
        )

    # Validate delay argument
    if not isinstance(delay, (int, float)):
        raise EvaluationError(
            f"TypeError: 'debounce' second argument (delay) must be a number, got {type(delay).__name__}."
        )

    if delay < 0:
        raise EvaluationError(
            f"ValueError: 'debounce' delay must be non-negative, got {delay}."
        )

    # State for the debounced function
    timer = {'current': None}
    
    def debounced_function(inner_args, inner_env):
        """The debounced version of the original function."""
        
        # Cancel any existing timer
        if timer['current'] is not None:
            timer['current'].cancel()
        
        def execute_original():
            """Execute the original function after delay."""
            try:
                if is_user_defined_fn:
                    # Call user-defined function
                    from lispy.environment import Environment
                    
                    # Validate argument count
                    if len(inner_args) != len(fn.params):
                        raise PromiseError(f"Debounced function expects {len(fn.params)} arguments, got {len(inner_args)}.")
                    
                    # Create new environment for function execution
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
                raise PromiseError(f"Debounced function execution failed: {e}")
            finally:
                # Clear the timer reference
                timer['current'] = None
        
        # Create new timer
        timer['current'] = threading.Timer(delay / 1000.0, execute_original)
        timer['current'].daemon = True
        timer['current'].start()
        
        # Debounced functions typically return None/nil immediately
        # The actual result happens asynchronously
        return None

    # Return the debounced function as a callable
    return debounced_function


@lispy_documentation("debounce")
def debounce_doc():
    return """Function: debounce
Arguments: (debounce fn delay)
Description: Creates a debounced version of a function that delays execution.

The debounced function will only execute after 'delay' milliseconds have passed
without being called again. If called again before the delay expires, the
previous call is cancelled and the timer resets.

Examples:
  ; Create a debounced search function
  (define search-debounced (debounce search-api 300))
  (search-debounced "query")    ; Executes after 300ms of no more calls
  
  ; Handle user input with debouncing
  (define handle-input (debounce 
                         (fn [text] (println "Processing:" text))
                         500))
  (handle-input "a")           ; Timer starts
  (handle-input "ab")          ; Previous call cancelled, timer resets
  (handle-input "abc")         ; Previous call cancelled, timer resets
  ; ... only the last call executes after 500ms
  
  ; Debounced button click protection
  (define save-data-debounced (debounce save-to-database 1000))
  
  ; Use with events or user interactions
  (define on-resize (debounce 
                      (fn [] (recalculate-layout))
                      250))

Use Cases:
  - Search input handling (wait for user to stop typing)
  - Button click protection (prevent double-clicks)
  - Window resize handlers (avoid excessive recalculation)
  - API call rate limiting
  - Form validation triggers

Notes:
  - First argument must be a function
  - Second argument must be a non-negative number (milliseconds)
  - Returns a new function with debounce behavior
  - Debounced function returns nil immediately
  - Original function executes asynchronously after delay
  - Each call to debounced function cancels any pending execution
  - Similar to JavaScript's debounce pattern
  - Thread-safe implementation using Python's threading.Timer
""" 