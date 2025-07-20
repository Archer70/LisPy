from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, LispyList, Vector, Symbol
from lispy.functions.map import hash_map
import threading
import time
from lispy.functions.decorators import lispy_function, lispy_documentation

@lispy_function("promise-all-settled")
def promise_all_settled(args, env):
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'promise-all-settled' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Validate collection is a list or vector
    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: 'promise-all-settled' argument must be a list or vector, got {type(collection)}."
        )

    # Validate all elements are promises
    for i, element in enumerate(collection):
        if not isinstance(element, LispyPromise):
            raise EvaluationError(
                f"TypeError: All elements must be promises, got {type(element)} at position {i}."
            )

    # Handle empty collection - resolve immediately with empty collection of same type
    if len(collection) == 0:
        result_type = Vector if isinstance(collection, Vector) else LispyList
        empty_promise = LispyPromise()
        empty_promise.resolve(result_type([]))
        return empty_promise

    # Create the all-settled promise
    all_settled_promise = LispyPromise()

    def wait_for_all_settled():
        """Wait for all promises to settle and collect their status objects."""
        try:
            results = []

            # Wait for each promise to settle (resolve or reject)
            for i, promise in enumerate(collection):
                # Poll until the promise settles
                while promise.state == "pending":
                    time.sleep(0.001)  # Small sleep to avoid busy waiting

                # Create status object based on settlement
                if promise.state == "resolved":
                    # Create fulfilled status object using hash-map with Symbol keys
                    status_obj = hash_map(
                        [
                            Symbol(":status"),
                            "fulfilled",
                            Symbol(":value"),
                            promise.value,
                        ],
                        env,
                    )
                elif promise.state == "rejected":
                    # Create rejected status object using hash-map with Symbol keys
                    status_obj = hash_map(
                        [
                            Symbol(":status"),
                            "rejected",
                            Symbol(":reason"),
                            promise.error,
                        ],
                        env,
                    )
                else:
                    # This should never happen, but handle gracefully
                    status_obj = hash_map(
                        [
                            Symbol(":status"),
                            "unknown",
                            Symbol(":error"),
                            f"Unexpected state: {promise.state}",
                        ],
                        env,
                    )

                results.append(status_obj)

            # All promises settled - return results in same collection type
            result_type = Vector if isinstance(collection, Vector) else LispyList
            all_settled_promise.resolve(result_type(results))

        except Exception as e:
            # This should rarely happen since we never reject, but handle gracefully
            all_settled_promise.reject(e)

    # Start waiting in background thread
    threading.Thread(target=wait_for_all_settled, daemon=True).start()

    return all_settled_promise


@lispy_documentation("promise-all-settled")
def promise_all_settled_documentation() -> str:
    """Returns documentation for the promise-all-settled function."""
    return """Function: promise-all-settled
Arguments: (promise-all-settled collection)
Description: Waits for all promises to settle and returns status objects for each.

Examples:
  ; Mixed success and failure
  (promise-all-settled [(resolve 1) (reject "error") (resolve 3)])
  ; => Promise that resolves to [
  ;      {:status "fulfilled" :value 1}
  ;      {:status "rejected" :reason "error"}
  ;      {:status "fulfilled" :value 3}
  ;    ]
  
  ; All successful
  (promise-all-settled [(resolve "a") (resolve "b") (resolve "c")])
  ; => Promise that resolves to [
  ;      {:status "fulfilled" :value "a"}
  ;      {:status "fulfilled" :value "b"} 
  ;      {:status "fulfilled" :value "c"}
  ;    ]
  
  ; All failures
  (promise-all-settled [(reject "err1") (reject "err2")])
  ; => Promise that resolves to [
  ;      {:status "rejected" :reason "err1"}
  ;      {:status "rejected" :reason "err2"}
  ;    ]
  
  ; With async operations
  (async
    (let [results (await (promise-all-settled [
                                           (timeout 100 "fast")
                (reject "error")
                (timeout 200 "slow")]))]
      ; Process each result
      (map (fn [result]
             (if (= (get result :status) "fulfilled")
               (get result :value)
               (get result :reason))) results)))
  
  ; Empty collection resolves immediately
  (promise-all-settled []) ; => Promise that resolves to []

Notes:
  - Requires exactly 1 argument (a collection of promises)
  - All elements in collection must be promises
  - NEVER rejects (unlike promise-all) - always resolves
  - Waits for ALL promises to settle (resolve or reject)
  - Result collection type matches input type (vector -> vector, list -> list)
  - Each result is a hash-map with :status and :value/:reason keys
  - :status is either "fulfilled" or "rejected"
  - Fulfilled promises have :value key with the resolved value
  - Rejected promises have :reason key with the error/rejection reason
  - Results are returned in the same order as input promises
  - Empty collection resolves immediately to empty collection
  - Useful for gathering all results regardless of success/failure
  - Perfect for graceful degradation and comprehensive error reporting
  - Similar to Promise.allSettled() in JavaScript (ES2020)
"""
