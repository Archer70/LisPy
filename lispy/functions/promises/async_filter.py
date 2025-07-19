"""
LisPy async-filter function - Concurrent async filtering following JavaScript patterns.

This function implements JavaScript's Array.filter() + Promise.all() pattern:
- Applies predicate to each element concurrently (not sequentially)
- Returns a promise that resolves to an array of elements where predicate was truthy
- Maintains original array order
- Fail-fast: if any predicate fails, the whole operation fails

Usage: (async-filter collection predicate)
"""

from lispy.closure import Function
from lispy.types import LispyPromise, Vector, LispyList
from lispy.exceptions import EvaluationError
from ..decorators import lispy_function, lispy_documentation
import threading


@lispy_function("async-filter")
def async_filter(args, env):
    """
    Async filter function - concurrent filtering with Promise.all semantics.

    Filters elements where predicate returns truthy, all predicates run concurrently.
    Follows JavaScript Array.filter() + Promise.all() pattern exactly.
    """
    # Validate argument count
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'async-filter' expects 2 arguments, got {len(args)}."
        )

    collection, predicate = args

    # Validate collection is a collection type
    if not isinstance(collection, (list, Vector, LispyList)):
        raise EvaluationError(
            f"TypeError: First argument to 'async-filter' must be a collection, got {type(collection).__name__}."
        )

    # Validate predicate is a function
    if not (callable(predicate) or isinstance(predicate, Function)):
        raise EvaluationError(
            f"TypeError: Second argument to 'async-filter' must be a function, got {type(predicate).__name__}."
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

    def execute_async_filter():
        """Execute async filtering in background thread."""
        try:
            # Step 1: Apply predicate to each item and collect promises
            predicate_promises = []
            
            for i, item in enumerate(items):
                # Execute predicate for this item
                if isinstance(predicate, Function):
                    # User-defined LisPy function
                    from lispy.environment import Environment
                    from lispy.evaluator import evaluate

                    call_env = Environment(outer=predicate.defining_env)
                    if predicate.params:
                        call_env.define(predicate.params[0].name, item)
                        if len(predicate.params) > 1:  # Index parameter
                            call_env.define(predicate.params[1].name, i)

                    # Execute function body
                    result = None
                    for expr in predicate.body:
                        result = evaluate(expr, call_env)
                    
                    # If result is a promise, use it; otherwise wrap in resolved promise
                    if isinstance(result, LispyPromise):
                        predicate_promises.append(result)
                    else:
                        resolved_promise = LispyPromise()
                        resolved_promise.resolve(result)
                        predicate_promises.append(resolved_promise)
                else:
                    # Built-in function
                    result = predicate([item, i], env)
                    
                    # If result is a promise, use it; otherwise wrap in resolved promise
                    if isinstance(result, LispyPromise):
                        predicate_promises.append(result)
                    else:
                        resolved_promise = LispyPromise()
                        resolved_promise.resolve(result)
                        predicate_promises.append(resolved_promise)

            # Step 2: Wait for all predicate promises to complete
            predicate_results = [None] * len(predicate_promises)
            completed_count = 0

            def check_completion():
                nonlocal completed_count
                completed_count += 1
                
                if completed_count == len(predicate_promises):
                    # All completed, check for any failures
                    for i, promise in enumerate(predicate_promises):
                        if promise.state == "rejected":
                            result_promise.reject(promise.error)
                            return
                        predicate_results[i] = promise.value

                    # All succeeded, filter based on predicate results
                    filtered_items = []
                    for i, (item, pred_result) in enumerate(zip(items, predicate_results)):
                        # Use LisPy truthiness
                        if pred_result is not None and pred_result is not False:
                            filtered_items.append(item)

                    # Resolve with filtered results in original collection type
                    if isinstance(collection, Vector):
                        result_promise.resolve(Vector(filtered_items))
                    elif isinstance(collection, LispyList):
                        result_promise.resolve(LispyList(filtered_items))
                    else:
                        result_promise.resolve(filtered_items)

            # Attach completion handlers to all promises
            for promise in predicate_promises:
                if promise.state == "pending":
                    promise.callbacks.append(check_completion)
                    promise.error_callbacks.append(check_completion)
                else:
                    # Already completed
                    check_completion()

        except Exception as e:
            result_promise.reject(f"async-filter error: {str(e)}")

    # Start execution in background thread
    thread = threading.Thread(target=execute_async_filter, daemon=True)
    thread.start()

    return result_promise


@lispy_documentation("async-filter")
def async_filter_doc():
    return """Function: async-filter
Arguments: (async-filter collection predicate)
Description: Filters elements where async predicate returns truthy value.

Examples:
  ; Filter even numbers concurrently
  (async-filter [1 2 3 4 5] (fn [x] (promise (fn [] (even? x)))))
  ; => Promise that resolves to [2 4]
  
  ; Concurrent validation
  (async-filter ["user1" "user2" "user3"] 
                (fn [id] (http-get (str "/api/validate/" id))))
  ; => Promise with array of valid users
  
  ; Mixed sync/async predicates
  (async-filter [1 2 3 4] 
                (fn [x] (if (> x 2)
                          (promise (fn [] (odd? x)))  ; Async for big numbers
                          (even? x))))               ; Sync for small
  ; => Promise that resolves to [2 3]
  
  ; With async/await
  (async
    (let [results (await (async-filter [1 2 3 4 5]
                                       (fn [x] (timeout 50 (> x 3)))))]
      (println "Filtered:" results))) ; => [4 5]

Notes:
  - Requires exactly 2 arguments (collection, predicate function)
  - Executes all predicates concurrently, not sequentially
  - Maintains original order of filtered elements
  - Fail-fast: if any predicate rejects, entire operation rejects
  - Predicate receives item and index as parameters
  - Result preserves collection type (vector in, vector out)
  - Empty collection resolves immediately to empty collection
  - Uses LisPy truthiness (nil and false are falsy, everything else truthy)"""
