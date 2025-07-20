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
from lispy.types import LispyPromise, Vector, List
from lispy.exceptions import EvaluationError
import threading
from lispy.functions.decorators import lispy_function, lispy_documentation


@lispy_function("async-map")
def async_map(args, env):
    # Validate argument count
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'async-map' expects 2 arguments, got {len(args)}."
        )

    collection, callback = args

    # Validate arguments
    if not isinstance(collection, (Vector, List)):
        raise EvaluationError(
            "TypeError: 'async-map' expects a vector or list as first argument."
        )

    # Validate callback type (can be user-defined function or built-in)
    is_user_defined_fn = isinstance(callback, Function)
    is_builtin_fn = callable(callback) and not is_user_defined_fn

    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError(
            "TypeError: 'async-map' expects a function as second argument."
        )

    # Handle empty collection
    if len(collection) == 0:
        promise = LispyPromise()
        promise.resolve(Vector([]))
        return promise

    # Create the result promise
    result_promise = LispyPromise()

    try:
        results = []
        all_sync = True  # Track if all results are synchronous

        for element in collection:
            # Call the callback function
            if is_user_defined_fn:
                # User-defined function - need to handle environment and parameters
                from lispy.environment import Environment
                from lispy.evaluator import evaluate

                if len(callback.params) != 1:
                    raise EvaluationError(
                        f"ArityError: Function passed to 'async-map' expects 1 argument, got {len(callback.params)}."
                    )

                param_symbol = callback.params[0]
                call_env = Environment(outer=callback.defining_env)
                call_env.define(param_symbol.name, element)

                # Execute function body
                result = None
                for expr_in_body in callback.body:
                    result = evaluate(expr_in_body, call_env)
            else:
                # Built-in function
                result = callback([element], env)

            # Check if result is a promise
            if isinstance(result, LispyPromise):
                all_sync = False

            results.append(result)

        # If all results are synchronous, resolve immediately
        if all_sync:
            result_promise.resolve(Vector(results))
        else:
            # Handle mixed sync/async results
            # For now, let's implement a simple version that waits for all promises
            final_results = [None] * len(results)
            completed_count = [0]
            error_occurred = [False]
            lock = threading.Lock()

            def handle_completion():
                with lock:
                    if error_occurred[0]:
                        return
                    completed_count[0] += 1
                    if completed_count[0] == len(results):
                        result_promise.resolve(Vector(final_results))

            def handle_error(error):
                with lock:
                    if not error_occurred[0]:
                        error_occurred[0] = True
                        result_promise.reject(error)

            # Process each result
            for i, result in enumerate(results):
                if isinstance(result, LispyPromise):
                    # Async result - wait for it
                    def make_handlers(idx):
                        def success_handler(value):
                            final_results[idx] = value
                            handle_completion()

                        def error_handler(error):
                            handle_error(error)

                        return success_handler, error_handler

                    success_handler, error_handler = make_handlers(i)
                    result.then(success_handler)
                    result.catch(error_handler)
                else:
                    # Sync result - store immediately
                    final_results[i] = result
                    handle_completion()

    except Exception as e:
        result_promise.reject(str(e))

    return result_promise


@lispy_documentation("async-map")
def async_map_documentation() -> str:
    """Returns documentation for the async-map function."""
    return """Function: async-map
Arguments: (async-map collection callback)
Description: Maps each element through callback concurrently, returns promise of results.

Examples:
  ; Basic concurrent mapping
  (await (async-map [1 2 3] (fn [x] (timeout 100 (* x 2)))))
  ; => [2 4 6]
  
  ; Thread-first usage
  (-> [1 2 3 4 5]
      (async-map (fn [x] (* x x)))
      (await))
  ; => [1 4 9 16 25]
  
  ; Error handling (fail-fast)
  (try
    (await (async-map [1 2 3] (fn [x] 
                                (if (= x 2) 
                                  (reject "error")
                                  x))))
    (catch e (println "Error:" e)))

Notes:
  - First argument must be a vector or list
  - Second argument must be a function taking 1 parameter
  - Returns a promise that resolves to a vector of results
  - All operations start immediately (concurrent execution)
  - Results maintain original collection order
  - Fail-fast: if any operation fails, whole operation fails
  - Follows JavaScript Array.map() + Promise.all() semantics
  - Thread-first (->) operator compatible
"""
