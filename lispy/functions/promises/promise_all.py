from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, LispyList, Vector
from ..decorators import lispy_function, lispy_documentation
import threading
import time


@lispy_function("promise-all")
def promise_all(args, env):
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

    # Validate that it's a collection
    if not isinstance(collection, (list, Vector, LispyList)):
        raise EvaluationError(
            f"TypeError: 'promise-all' expects a collection (list/vector), got {type(collection).__name__}."
        )

    # Extract promises from collection
    promises = list(collection)

    # Validate all items are promises
    for i, item in enumerate(promises):
        if not isinstance(item, LispyPromise):
            raise EvaluationError(
                f"TypeError: All items in collection must be promises, got {type(item).__name__} at position {i}."
            )

    # Create result promise
    result_promise = LispyPromise()

    def wait_for_all():
        """Wait for all promises to complete in background thread."""
        try:
            # If empty collection, resolve immediately with empty result
            if not promises:
                if isinstance(collection, Vector):
                    result_promise.resolve(Vector([]))
                elif isinstance(collection, LispyList):
                    result_promise.resolve(LispyList([]))
                else:
                    result_promise.resolve([])
                return

            # Wait for all promises to settle
            results = []
            for promise in promises:
                # Poll until promise settles
                while promise.state == "pending":
                    time.sleep(0.001)  # Small sleep to avoid busy waiting

                # If any promise rejected, reject the all promise
                if promise.state == "rejected":
                    result_promise.reject(promise.error)
                    return

                # Collect resolved value
                results.append(promise.value)

            # All promises resolved, return results in same collection type
            if isinstance(collection, Vector):
                result_promise.resolve(Vector(results))
            elif isinstance(collection, LispyList):
                result_promise.resolve(LispyList(results))
            else:
                result_promise.resolve(results)

        except Exception as e:
            result_promise.reject(f"promise-all error: {str(e)}")

    # Start background thread
    thread = threading.Thread(target=wait_for_all, daemon=True)
    thread.start()

    return result_promise


@lispy_documentation("promise-all")
def promise_all_doc():
    return """Function: promise-all
Arguments: (promise-all collection)
Description: Waits for all promises in a collection to resolve.

Examples:
  ; Wait for multiple promises
  (promise-all [(resolve 1) (resolve 2) (resolve 3)])
  ; => Promise that resolves to [1 2 3]
  
  ; Mixed with promise creation
  (promise-all [(promise (fn [] (+ 1 2)))
                (resolve "hello")
                (promise (fn [] (* 3 4)))])
  ; => Promise that resolves to [3 "hello" 12]
  
  ; With async/await
  (async
    (let [results (await (promise-all [(resolve "a") (resolve "b")]))]
      (println "All results:" results)))
  
  ; Error handling - if any promise rejects, all rejects
  (promise-all [(resolve 1) (reject "error") (resolve 3)])
  ; => Promise that rejects with "error"

Notes:
  - Requires exactly 1 argument (a collection of promises)
  - Collection can be a list, vector, or LisPy list
  - All items in collection must be promises
  - Result preserves collection type (vector in, vector out)
  - If any promise rejects, the entire promise-all rejects
  - Empty collection resolves immediately to empty collection
  - Useful for concurrent operations that all must succeed"""
