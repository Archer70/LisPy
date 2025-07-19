"""
LisPy async-reduce function - Sequential async reduction following JavaScript patterns.

This function implements JavaScript's Array.reduce() pattern with async support:
- Applies reducer function sequentially (not concurrently) since each step depends on previous
- Returns a promise that resolves to the final accumulated value
- Maintains sequential order (essential for reduce operations)
- Fail-fast: if any reducer fails, the whole operation fails

Usage: (async-reduce collection reducer initial-value)
"""

from lispy.closure import Function
from lispy.types import LispyPromise, Vector, LispyList
from lispy.exceptions import EvaluationError
from ..decorators import lispy_function, lispy_documentation
import threading


@lispy_function("async-reduce")
def async_reduce(args, env):
    """
    Async reduce function - sequential reduction with async support.
    
    Reduces collection to single value using async reducer function.
    Unlike map/filter, this must be sequential since each step depends on previous result.
    """
    # Validate argument count
    if len(args) != 3:
        raise EvaluationError(f"SyntaxError: 'async-reduce' expects 3 arguments, got {len(args)}.")
    
    collection, reducer, initial_value = args
    
    # Validate arguments
    if not isinstance(collection, (Vector, List)):
        raise EvaluationError("TypeError: 'async-reduce' expects a vector or list as first argument.")
    
    # Validate reducer type (can be user-defined function or built-in)
    is_user_defined_fn = isinstance(reducer, Function)
    is_builtin_fn = callable(reducer) and not is_user_defined_fn
    
    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError("TypeError: 'async-reduce' expects a function as second argument.")
    
    # Validate reducer arity for user-defined functions (should take 2 arguments: accumulator and current)
    if is_user_defined_fn and len(reducer.params) != 2:
        raise EvaluationError(f"ArityError: Function passed to 'async-reduce' expects 2 arguments, got {len(reducer.params)}.")
    
    # Handle empty collection - return initial value immediately
    if len(collection) == 0:
        promise = LispyPromise()
        promise.resolve(initial_value)
        return promise
    
    # Create the result promise
    result_promise = LispyPromise()
    
    def sequential_reduce():
        """Perform sequential reduction in background thread."""
        try:
            accumulator = initial_value
            
            for element in collection:
                # Call the reducer function with accumulator and current element
                if is_user_defined_fn:
                    # User-defined function - need to handle environment and parameters
                    from lispy.environment import Environment
                    from lispy.evaluator import evaluate
                    
                    acc_param = reducer.params[0]
                    curr_param = reducer.params[1]
                    call_env = Environment(outer=reducer.defining_env)
                    call_env.define(acc_param.name, accumulator)
                    call_env.define(curr_param.name, element)
                    
                    # Execute function body
                    result = None
                    for expr_in_body in reducer.body:
                        result = evaluate(expr_in_body, call_env)
                else:
                    # Built-in function
                    result = reducer([accumulator, element], env)
                
                # Handle async result
                if isinstance(result, LispyPromise):
                    # Wait for promise to resolve
                    while result.state == "pending":
                        import time
                        time.sleep(0.001)  # Small sleep to avoid busy waiting
                    
                    if result.state == "rejected":
                        result_promise.reject(result.error)
                        return
                    
                    accumulator = result.value
                else:
                    # Synchronous result
                    accumulator = result
            
            # All reductions completed successfully
            result_promise.resolve(accumulator)
            
        except Exception as e:
            result_promise.reject(str(e))
    
    # Start reduction in background thread
    threading.Thread(target=sequential_reduce, daemon=True).start()
    
    return result_promise


@lispy_documentation("async-reduce")
def async_reduce_doc():
    return """Function: async-reduce
Arguments: (async-reduce collection reducer initial-value)
Description: Reduces collection to single value using async reducer function, processing sequentially.

Examples:
  ; Basic sequential reduction
  (await (async-reduce [1 2 3 4] (fn [acc x] (+ acc x)) 0))
  ; => 10 (sum of all elements)
  
  ; With async reducer
  (await (async-reduce [1 2 3] (fn [acc x] (timeout 50 (+ acc (* x x)))) 0))
  ; => 14 (0 + 1² + 2² + 3² = 0 + 1 + 4 + 9)
  
  ; Thread-first usage
  (-> [1 2 3 4 5]
      (async-reduce (fn [acc x] (* acc x)) 1)
      (await))
  ; => 120 (factorial: 1 * 1 * 2 * 3 * 4 * 5)
  
  ; Building collections
  (await (async-reduce [1 2 3] (fn [acc x] (conj acc (* x 2))) []))
  ; => [2 4 6]
  
  ; With promise chaining
  (-> (async-reduce ["a" "b" "c"] 
                    (fn [acc s] (-> (timeout 10 s)
                                    (promise-then (fn [val] (str acc val)))))
                    "")
      (await))
  ; => "abc"

Notes:
  - First argument must be a vector or list
  - Second argument must be a function taking 2 parameters (accumulator, current)
  - Third argument is the initial value for the accumulator
  - Returns a promise that resolves to the final accumulated value
  - Processing is SEQUENTIAL (not concurrent) since each step depends on previous
  - Fail-fast: if any reducer fails, whole operation fails
  - Reducer can return either sync values or promises
  - Follows JavaScript Array.reduce() semantics with async support
  - Thread-first (->) operator compatible
""" 