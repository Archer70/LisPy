import threading

from lispy.closure import Function
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import LispyPromise, List, Vector


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

    # Validate arguments
    if not isinstance(collection, (Vector, List)):
        raise EvaluationError(
            "TypeError: 'async-filter' expects a vector or list as first argument."
        )

    # Validate predicate type (can be user-defined function or built-in)
    is_user_defined_fn = isinstance(predicate, Function)
    is_builtin_fn = callable(predicate) and not is_user_defined_fn

    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError(
            "TypeError: 'async-filter' expects a function as second argument."
        )

    # Handle empty collection
    if len(collection) == 0:
        promise = LispyPromise()
        promise.resolve(Vector([]))
        return promise

    # Create the result promise
    result_promise = LispyPromise()

    try:
        predicate_results = []
        all_sync = True  # Track if all results are synchronous

        for element in collection:
            # Call the predicate function
            if is_user_defined_fn:
                # User-defined function - need to handle environment and parameters
                from lispy.environment import Environment
                from lispy.evaluator import evaluate

                if len(predicate.params) != 1:
                    raise EvaluationError(
                        f"ArityError: Function passed to 'async-filter' expects 1 argument, got {len(predicate.params)}."
                    )

                param_symbol = predicate.params[0]
                call_env = Environment(outer=predicate.defining_env)
                call_env.define(param_symbol.name, element)

                # Execute function body
                result = None
                for expr_in_body in predicate.body:
                    result = evaluate(expr_in_body, call_env)
            else:
                # Built-in function
                result = predicate([element], env)

            # Check if result is a promise
            if isinstance(result, LispyPromise):
                all_sync = False

            predicate_results.append(result)

        # If all results are synchronous, filter immediately
        if all_sync:
            filtered_elements = []
            for i, predicate_result in enumerate(predicate_results):
                if predicate_result:  # Truthy check
                    filtered_elements.append(collection[i])
            result_promise.resolve(Vector(filtered_elements))
        else:
            # Handle mixed sync/async results
            final_predicate_results = [None] * len(predicate_results)
            completed_count = [0]
            error_occurred = [False]
            lock = threading.Lock()

            def handle_completion():
                with lock:
                    if error_occurred[0]:
                        return
                    completed_count[0] += 1
                    if completed_count[0] == len(predicate_results):
                        # All predicates completed, now filter
                        filtered_elements = []
                        for i, predicate_result in enumerate(final_predicate_results):
                            if predicate_result:  # Truthy check
                                filtered_elements.append(collection[i])
                        result_promise.resolve(Vector(filtered_elements))

            def handle_error(error):
                with lock:
                    if not error_occurred[0]:
                        error_occurred[0] = True
                        result_promise.reject(error)

            # Process each predicate result
            for i, result in enumerate(predicate_results):
                if isinstance(result, LispyPromise):
                    # Async result - wait for it
                    def make_handlers(idx):
                        def success_handler(value):
                            final_predicate_results[idx] = value
                            handle_completion()

                        def error_handler(error):
                            handle_error(error)

                        return success_handler, error_handler

                    success_handler, error_handler = make_handlers(i)
                    result.then(success_handler)
                    result.catch(error_handler)
                else:
                    # Sync result - store immediately
                    final_predicate_results[i] = result
                    handle_completion()

    except Exception as e:
        result_promise.reject(str(e))

    return result_promise


@lispy_documentation("async-filter")
def async_filter_documentation() -> str:
    """Returns documentation for the async-filter function."""
    return """Function: async-filter
Arguments: (async-filter collection predicate)
Description: Filters elements where predicate returns truthy, all predicates run concurrently.

Examples:
  ; Basic concurrent filtering
  (await (async-filter [1 2 3 4 5] (fn [x] (timeout 100 (> x 3)))))
  ; => [4 5]
  
  ; Thread-first usage
  (-> [1 2 3 4 5 6]
      (async-filter (fn [x] (even? x)))
      (await))
  ; => [2 4 6]
  
  ; With async predicates
  (await (async-filter ["apple" "banana" "cherry"] 
                       (fn [s] (-> (fetch-word-length s)
                                   (promise-then (fn [len] (> len 5)))))))
  ; => ["banana" "cherry"]
  
  ; Error handling (fail-fast)
  (try
    (await (async-filter [1 2 3] (fn [x] 
                                   (if (= x 2) 
                                     (reject "error")
                                     (> x 1)))))
    (catch e (println "Error:" e)))

Notes:
  - First argument must be a vector or list
  - Second argument must be a function taking 1 parameter (predicate)
  - Returns a promise that resolves to a vector of filtered elements
  - All predicates start immediately (concurrent execution)
  - Results maintain original collection order
  - Fail-fast: if any predicate fails, whole operation fails
  - Elements are included if predicate returns truthy value
  - Follows JavaScript Array.filter() + Promise.all() semantics
  - Thread-first (->) operator compatible
"""
