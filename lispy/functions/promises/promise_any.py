from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, LispyList, Vector
from ..decorators import lispy_function, lispy_documentation
import threading
import time


@lispy_function("promise-any")
def promise_any(args, env):
    """Resolve with the first promise to resolve, or reject if all reject.

    Usage: (promise-any collection)

    Args:
        collection: A vector or list of promises

    Returns:
        A promise that resolves with the value of the first promise to resolve,
        or rejects with a collection of all rejection reasons if all promises reject

    Examples:
        (promise-any [(reject "error1") (resolve "success") (reject "error2")])
        ; => Promise that resolves to "success"

        (promise-any [(reject "error1") (reject "error2") (reject "error3")])
        ; => Promise that rejects with ["error1" "error2" "error3"]
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'promise-any' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Validate that it's a collection
    if not isinstance(collection, (list, Vector, LispyList)):
        raise EvaluationError(
            f"TypeError: 'promise-any' expects a collection (list/vector), got {type(collection).__name__}."
        )

    # Extract promises from collection
    promises = list(collection)

    # Validate all items are promises
    for i, item in enumerate(promises):
        if not isinstance(item, LispyPromise):
            raise EvaluationError(
                f"TypeError: All items in collection must be promises, got {type(item).__name__} at position {i}."
            )

    # Handle empty collection - reject immediately
    if not promises:
        empty_promise = LispyPromise()
        empty_promise.reject("Empty collection provided to promise-any")
        return empty_promise

    # Create result promise
    result_promise = LispyPromise()

    def wait_for_any():
        """Wait for first promise to resolve or all to reject in background thread."""
        try:
            resolved_count = 0
            rejected_count = 0
            rejection_reasons = []

            # Continuously poll all promises
            while resolved_count == 0 and rejected_count < len(promises):
                resolved_count = 0
                rejected_count = 0
                rejection_reasons = []

                for promise in promises:
                    if promise.state == "resolved":
                        resolved_count += 1
                        # First resolution wins
                        result_promise.resolve(promise.value)
                        return
                    elif promise.state == "rejected":
                        rejected_count += 1
                        rejection_reasons.append(promise.error)

                # Small sleep to avoid busy waiting
                time.sleep(0.001)

            # If we get here, all promises rejected
            if rejected_count == len(promises):
                # Return rejection reasons in same collection type as input
                if isinstance(collection, Vector):
                    result_promise.reject(Vector(rejection_reasons))
                elif isinstance(collection, LispyList):
                    result_promise.reject(LispyList(rejection_reasons))
                else:
                    result_promise.reject(rejection_reasons)

        except Exception as e:
            result_promise.reject(f"promise-any error: {str(e)}")

    # Start background thread
    thread = threading.Thread(target=wait_for_any, daemon=True)
    thread.start()

    return result_promise


@lispy_documentation("promise-any")
def promise_any_doc():
    return """Function: promise-any
Arguments: (promise-any collection)
Description: Resolves with the first promise to resolve, or rejects if all reject.

Examples:
  ; First success wins
  (promise-any [(reject "error1") (resolve "success") (reject "error2")])
  ; => Promise that resolves to "success"
  
  ; All rejections collected
  (promise-any [(reject "error1") (reject "error2") (reject "error3")])
  ; => Promise that rejects with ["error1" "error2" "error3"]
  
  ; Immediate success
  (promise-any [(resolve "immediate") (timeout 1000 "slow")])
  ; => Promise that resolves to "immediate"
  
  ; With async/await
  (async
    (try
      (let [result (await (promise-any [(reject "fail") (resolve "win")]))]
        (println "Winner:" result))
      (catch errors
        (println "All failed:" errors))))

Notes:
  - Requires exactly 1 argument (a collection of promises)
  - Collection can be a list, vector, or LisPy list
  - All items in collection must be promises
  - Returns value of first promise to resolve
  - If all reject, returns collection of all rejection reasons
  - Empty collection immediately rejects
  - Useful for trying multiple fallback approaches
  - Opposite of promise-all (needs only one success)"""
