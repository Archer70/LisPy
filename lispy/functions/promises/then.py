from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from lispy.closure import Function


def builtin_promise_then(args, env):
    """Chain a callback to be executed when promise resolves.

    Usage: (promise-then promise callback)

    Args:
        promise: A promise to chain from
        callback: Function to call with the resolved value

    Returns:
        A new promise that resolves with the callback's return value

    Examples:
        (then (resolve 42) (fn [x] (* x 2))) 
        ; => Promise that resolves to 84
        
        (-> (resolve 10)
            (then (fn [x] (+ x 5)))
            (then (fn [x] (* x 2))))
        ; => Promise that resolves to 30
        
        (async 
          (let [result (await (then (promise (fn [] 10)) 
                                    (fn [x] (+ x 5))))]
            result)) ; => 15
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'promise-then' expects 2 arguments (promise callback), got {len(args)}."
        )
    
    promise = args[0]
    callback = args[1]
    
    # Validate promise argument
    if not isinstance(promise, LispyPromise):
        raise EvaluationError(
            f"TypeError: 'promise-then' first argument must be a promise, got {type(promise).__name__}."
        )
    
    # Validate callback argument
    if not (isinstance(callback, Function) or callable(callback)):
        raise EvaluationError(
            f"TypeError: 'promise-then' second argument must be a function, got {type(callback).__name__}."
        )
    
    # Validate callback parameter count immediately for user-defined functions
    if isinstance(callback, Function):
        if len(callback.params) != 1:
            raise EvaluationError(
                f"TypeError: 'promise-then' callback must take exactly 1 argument, got {len(callback.params)}."
            )
    
    # Create wrapper function that handles LisPy function calls
    def lispy_callback(value):
        if isinstance(callback, Function):
            # User-defined LisPy function
            from lispy.environment import Environment
            from lispy.evaluator import evaluate
            
            # Create environment for function call
            call_env = Environment(outer=callback.defining_env)
            
            # Bind the parameter (already validated to be exactly one parameter)
            
            call_env.define(callback.params[0].name, value)
            
            # Execute function body
            result = None
            for expr in callback.body:
                result = evaluate(expr, call_env)
            return result
        else:
            # Built-in function
            return callback([value], env)
    
    # Use the promise's then method with our wrapper
    return promise.then(lispy_callback)


def documentation_promise_then() -> str:
    """Returns documentation for the then function."""
    return """Function: promise-then
Arguments: (promise-then promise callback)
Description: Chains a callback to be executed when a promise resolves.

Examples:
  (promise-then (resolve 42) (fn [x] (* x 2)))     ; => Promise that resolves to 84
  
  ; Thread-first style chaining:
  (-> (resolve 10)
      (promise-then (fn [x] (+ x 5)))              ; 15
      (promise-then (fn [x] (* x 2))))             ; 30
  
  ; With async/await:
  (async 
    (let [result (await (promise-then (fetch-data) process-data))]
      result))
      
  ; Error handling with on-reject:
  (-> (fetch-user-data)
      (promise-then extract-user-name)
      (on-reject (fn [err] "Unknown User")))

Notes:
  - Requires exactly two arguments (promise and callback)
  - Callback must be a function that takes exactly one argument
  - Returns a new promise with the transformed value
  - If callback throws an error, returned promise is rejected
  - Callback receives the resolved value of the input promise
  - Supports both user-defined and built-in functions as callbacks
  - Works seamlessly with thread-first (->) operator
  - Can be chained multiple times for data transformation pipelines
  - If callback returns a promise, it will be flattened (no nested promises)
  - Essential building block for functional async programming
""" 