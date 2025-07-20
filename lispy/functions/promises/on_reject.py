from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from lispy.closure import Function
from lispy.functions.decorators import lispy_function, lispy_documentation

@lispy_function("on-reject")
def on_reject(args, env):
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'on-reject' expects 2 arguments (promise error-callback), got {len(args)}."
        )

    promise = args[0]
    error_callback = args[1]

    # Validate promise argument
    if not isinstance(promise, LispyPromise):
        raise EvaluationError(
            f"TypeError: 'on-reject' first argument must be a promise, got {type(promise).__name__}."
        )

    # Validate callback argument
    if not (isinstance(error_callback, Function) or callable(error_callback)):
        raise EvaluationError(
            f"TypeError: 'on-reject' second argument must be a function, got {type(error_callback).__name__}."
        )

    # Validate callback parameter count immediately for user-defined functions
    if isinstance(error_callback, Function):
        if len(error_callback.params) != 1:
            raise EvaluationError(
                f"TypeError: 'on-reject' callback must take exactly 1 argument, got {len(error_callback.params)}."
            )

    # Create wrapper function that handles LisPy function calls
    def lispy_error_callback(error):
        if isinstance(error_callback, Function):
            # User-defined LisPy function
            from lispy.environment import Environment
            from lispy.evaluator import evaluate

            # Create environment for function call
            call_env = Environment(outer=error_callback.defining_env)

            # Bind the parameter (already validated to be exactly one parameter)

            call_env.define(error_callback.params[0].name, error)

            # Execute function body
            result = None
            for expr in error_callback.body:
                result = evaluate(expr, call_env)
            return result
        else:
            # Built-in function
            return error_callback([error], env)

    # Use the promise's catch method with our wrapper
    return promise.catch(lispy_error_callback)


@lispy_documentation("on-reject")
def on_reject_documentation() -> str:
    """Returns documentation for the on-reject function."""
    return """Function: on-reject
Arguments: (on-reject promise error-callback)
Description: Handles promise rejection with a callback function.

Examples:
  (on-reject (reject "error") (fn [err] (str "Handled: " err)))
  ; => Promise that resolves to "Handled: error"
  
  (on-reject (resolve 42) (fn [err] "not called"))
  ; => Promise that resolves to 42 (error handler not called)
  
  ; Thread-first style error handling:
  (-> (fetch-user-data)
      (then extract-user-name)
      (on-reject (fn [err] "Unknown User"))
      (then (fn [name] (str "Hello, " name))))
  
  ; Multiple error handling strategies:
  (-> (risky-operation)
      (on-reject (fn [err] 
        (cond 
          (= err "network") "Offline mode"
          (= err "auth") "Please login"
          :else "Something went wrong"))))
          
  ; Error recovery with fallback data:
  (-> (fetch-from-cache)
      (on-reject (fn [_] (fetch-from-server)))
      (on-reject (fn [_] default-data)))

Notes:
  - Requires exactly two arguments (promise and error-callback)
  - Error-callback must be a function that takes exactly one argument
  - Returns a new promise that resolves with callback's return value on error
  - If original promise resolves, error-callback is not called
  - Error-callback receives the rejection reason (any LisPy value)
  - Supports both user-defined and built-in functions as callbacks
  - Works seamlessly with thread-first (->) operator
  - Essential for error recovery and graceful degradation
  - Can be chained multiple times for fallback strategies
  - If error-callback throws, returned promise is rejected with new error
  - Converts rejected promises to resolved promises (error recovery)
"""
