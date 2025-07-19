"""
LisPy async-map function - Concurrent async mapping following JavaScript patterns.

This function implements JavaScript's Array.map() + Promise.all() pattern:
- Maps each element through an async callback function
- Executes all operations concurrently (not sequentially)
- Returns a promise that resolves to an array of results
- Maintains original array order regardless of completion order
- Fail-fast: if any operation fails, the whole operation fails

Usage: (async-map collection callback)
"""

from lispy.closure import Function
from lispy.types import LispyPromise, Vector, LispyList
from lispy.exceptions import EvaluationError
from ..decorators import lispy_function, lispy_documentation
import threading


@lispy_function("async-map")
def async_map(args, env):
    """
    Async map function - concurrent mapping with Promise.all semantics.

    Maps each element through callback concurrently, returns promise of results.
    Follows JavaScript Array.map() + Promise.all() pattern exactly.
    """
    # Validate argument count
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'async-map' expects 2 arguments, got {len(args)}."
        )

    collection, callback = args

    # Validate collection is a collection type
    if not isinstance(collection, (list, Vector, LispyList)):
        raise EvaluationError(
            f"TypeError: First argument to 'async-map' must be a collection, got {type(collection).__name__}."
        )

    # Validate callback is a function
    if not (callable(callback) or isinstance(callback, Function)):
        raise EvaluationError(
            f"TypeError: Second argument to 'async-map' must be a function, got {type(callback).__name__}."
        )

    # Convert to list for easier processing
    items = list(collection)

    # Empty collection - return resolved promise with empty result
    if not items:
        result_promise = LispyPromise()
        if isinstance(collection, Vector):
            result_promise.resolve(Vector([]))
        elif isinstance(collection, LispyList):
            result_promise.resolve(LispyList([]))
        else:
            result_promise.resolve([])
        return result_promise

    # Create result promise
    result_promise = LispyPromise()

    def execute_async_map():
        """Execute async mapping in background thread."""
        try:
            # Step 1: Apply callback to each item and collect promises
            promises = []
            
            for i, item in enumerate(items):
                # Execute callback for this item
                if isinstance(callback, Function):
                    # User-defined LisPy function
                    from lispy.environment import Environment
                    from lispy.evaluator import evaluate

                    call_env = Environment(outer=callback.defining_env)
                    if callback.params:
                        call_env.define(callback.params[0].name, item)
                        if len(callback.params) > 1:  # Index parameter
                            call_env.define(callback.params[1].name, i)

                    # Execute function body
                    result = None
                    for expr in callback.body:
                        result = evaluate(expr, call_env)
                    
                    # If result is a promise, use it; otherwise wrap in resolved promise
                    if isinstance(result, LispyPromise):
                        promises.append(result)
                    else:
                        resolved_promise = LispyPromise()
                        resolved_promise.resolve(result)
                        promises.append(resolved_promise)
                else:
                    # Built-in function
                    result = callback([item, i], env)
                    
                    # If result is a promise, use it; otherwise wrap in resolved promise
                    if isinstance(result, LispyPromise):
                        promises.append(result)
                    else:
                        resolved_promise = LispyPromise()
                        resolved_promise.resolve(result)
                        promises.append(resolved_promise)

            # Step 2: Wait for all promises to complete (promise-all semantics)
            results = [None] * len(promises)
            completed_count = 0

            def check_completion():
                nonlocal completed_count
                completed_count += 1
                
                if completed_count == len(promises):
                    # All completed, check for any failures
                    for i, promise in enumerate(promises):
                        if promise.state == "rejected":
                            result_promise.reject(promise.error)
                            return
                        results[i] = promise.value

                    # All succeeded, resolve with results in original collection type
                    if isinstance(collection, Vector):
                        result_promise.resolve(Vector(results))
                    elif isinstance(collection, LispyList):
                        result_promise.resolve(LispyList(results))
                    else:
                        result_promise.resolve(results)

            # Attach completion handlers to all promises
            for promise in promises:
                if promise.state == "pending":
                    promise.callbacks.append(check_completion)
                    promise.error_callbacks.append(check_completion)
                else:
                    # Already completed
                    check_completion()

        except Exception as e:
            result_promise.reject(f"async-map error: {str(e)}")

    # Start execution in background thread
    thread = threading.Thread(target=execute_async_map, daemon=True)
    thread.start()

    return result_promise


@lispy_documentation("async-map")
def async_map_doc():
    return """Function: async-map
Arguments: (async-map collection callback)
Description: Maps each element through an async callback concurrently.

Examples:
  ; Map numbers to promises concurrently
  (async-map [1 2 3] (fn [x] (promise (fn [] (* x x)))))
  ; => Promise that resolves to [1 4 9]
  
  ; Concurrent HTTP requests
  (async-map ["user1" "user2" "user3"] 
             (fn [id] (http-get (str "/api/users/" id))))
  ; => Promise with array of user data
  
  ; Mixed sync/async operations
  (async-map [1 2 3 4] 
             (fn [x] (if (even? x)
                       (promise (fn [] (* x 2)))  ; Async for even
                       (* x 3))))                ; Sync for odd
  ; => Promise that resolves to [3 4 9 8]
  
  ; With async/await
  (async
    (let [results (await (async-map [1 2 3]
                                    (fn [x] (timeout 100 (* x 10)))))]
      (println "All done:" results))) ; => [10 20 30]

Notes:
  - Requires exactly 2 arguments (collection, callback function)
  - Executes all callbacks concurrently, not sequentially
  - Maintains original order regardless of completion order
  - Fail-fast: if any callback rejects, entire operation rejects
  - Callback receives item and index as parameters
  - Result preserves collection type (vector in, vector out)
  - Empty collection resolves immediately to empty collection
  - Follows JavaScript Array.map() + Promise.all() semantics"""
