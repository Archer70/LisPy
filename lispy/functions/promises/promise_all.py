from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, LispyList, Vector
import threading
import time


def builtin_promise_all(args, env):
    """Wait for all promises in a collection to resolve.

    Usage: (promise-all collection)

    Args:
        collection: A vector or list of promises

    Returns:
        A promise that resolves with a collection of all resolved values,
        or rejects if any promise rejects

    Examples:
        (promise-all [(resolve 1) (resolve 2) (resolve 3)])
        ; => Promise that resolves to [1 2 3]

        (async
          (let [results (await (promise-all [(resolve "a") (resolve "b")]))]
            results)) ; => ["a" "b"]
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'promise-all' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Validate collection is a list or vector
    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: 'promise-all' argument must be a list or vector, got {type(collection).__name__}."
        )

    # Validate all elements are promises
    for i, element in enumerate(collection):
        if not isinstance(element, LispyPromise):
            raise EvaluationError(
                f"TypeError: All elements must be promises, got {type(element).__name__} at position {i}."
            )

    # Handle empty collection - resolve immediately with empty collection of same type
    if len(collection) == 0:
        result_type = Vector if isinstance(collection, Vector) else LispyList
        empty_promise = LispyPromise()
        empty_promise.resolve(result_type([]))
        return empty_promise

    # Create the promise-all promise
    all_promise = LispyPromise()

    def wait_for_all():
        """Wait for all promises to complete in a background thread."""
        try:
            results = []

            # Wait for each promise to complete
            for i, promise in enumerate(collection):
                # Poll until the promise completes
                while promise.state == "pending":
                    time.sleep(0.001)  # Small sleep to avoid busy waiting

                # Check if any promise rejected
                if promise.state == "rejected":
                    all_promise.reject(promise.error)
                    return

                # Collect the resolved value
                results.append(promise.value)

            # All promises resolved - return results in same collection type
            result_type = Vector if isinstance(collection, Vector) else LispyList
            all_promise.resolve(result_type(results))

        except Exception as e:
            all_promise.reject(e)

    # Start waiting in background thread
    threading.Thread(target=wait_for_all, daemon=True).start()

    return all_promise


def documentation_promise_all() -> str:
    """Returns documentation for the promise-all function."""
    return """Function: promise-all
Arguments: (promise-all collection)
Description: Waits for all promises in a collection to resolve and returns their results.

Examples:
  ; Basic usage with resolved promises
  (promise-all [(resolve 1) (resolve 2) (resolve 3)])
  ; => Promise that resolves to [1 2 3]
  
  ; Mixed with actual async operations  
  (async
    (let [results (await (promise-all [
                           (promise (fn [] (+ 1 2)))
                           (resolve 42)
                           (promise (fn [] (* 3 4)))]))]
      results)) ; => [3 42 12]
  
  ; Empty collection resolves immediately
  (promise-all []) ; => Promise that resolves to []
  (promise-all '()) ; => Promise that resolves to ()
  
  ; With async functions
  (async
    (let [promises [(fetch-data "user1") (fetch-data "user2")]
          results (await (promise-all promises))]
      results)) ; => ["data1" "data2"]

Notes:
  - Requires exactly 1 argument (a collection of promises)
  - All elements in collection must be promises
  - Returns a promise that resolves when ALL input promises resolve
  - Result collection type matches input type (vector -> vector, list -> list)
  - If ANY promise rejects, promise-all immediately rejects with that error
  - Empty collection resolves immediately to empty collection
  - Results are returned in the same order as input promises
  - Useful for waiting on multiple concurrent operations
  - Essential for coordinating parallel async work
  - Similar to Promise.all() in JavaScript
"""
