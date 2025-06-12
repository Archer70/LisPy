from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, LispyList, Vector
import threading
import time


def builtin_promise_any(args, env):
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

    # Validate collection is a list or vector
    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: 'promise-any' argument must be a list or vector, got {type(collection)}."
        )

    # Validate all elements are promises
    for i, element in enumerate(collection):
        if not isinstance(element, LispyPromise):
            raise EvaluationError(
                f"TypeError: All elements must be promises, got {type(element)} at position {i}."
            )

    # Handle empty collection - reject immediately with appropriate error
    if len(collection) == 0:
        empty_promise = LispyPromise()
        empty_promise.reject(
            "AggregateError: All promises were rejected (empty collection)"
        )
        return empty_promise

    # Create the any promise
    any_promise = LispyPromise()

    def any_monitor():
        """Monitor all promises and resolve with first success or reject if all fail."""
        try:
            settled_count = 0
            rejection_reasons = [None] * len(collection)  # Track rejections in order
            resolved = False

            while not resolved and settled_count < len(collection):
                # Check each promise to see if any have resolved
                for i, promise in enumerate(collection):
                    if promise.state == "resolved" and not resolved:
                        # First successful resolution wins
                        any_promise.resolve(promise.value)
                        resolved = True
                        return
                    elif promise.state == "rejected" and rejection_reasons[i] is None:
                        # Track this rejection
                        rejection_reasons[i] = promise.error
                        settled_count += 1

                # If all promises have rejected, reject with aggregate error
                if settled_count == len(collection) and not resolved:
                    # Create aggregate error with all rejection reasons
                    # Preserve collection type for consistency
                    result_type = (
                        Vector if isinstance(collection, Vector) else LispyList
                    )
                    aggregate_error = f"AggregateError: All promises were rejected - {result_type(rejection_reasons)}"
                    any_promise.reject(aggregate_error)
                    return

                # Small sleep to avoid busy waiting
                time.sleep(0.001)

        except Exception as e:
            if not resolved:
                any_promise.reject(e)

    # Start monitoring in background thread
    threading.Thread(target=any_monitor, daemon=True).start()

    return any_promise


def documentation_promise_any() -> str:
    """Returns documentation for the promise-any function."""
    return """Function: promise-any
Arguments: (promise-any collection)
Description: Returns a promise that resolves with the first promise to resolve, ignoring rejections.

Examples:
  ; First to resolve wins (rejections ignored)
  (promise-any [(reject "error1") (resolve "success") (reject "error2")])
  ; => Promise that resolves to "success"
  
  ; All rejections result in aggregate error
  (promise-any [(reject "error1") (reject "error2") (reject "error3")])
  ; => Promise that rejects with aggregate error containing all reasons
  
  ; Immediate resolution wins
  (promise-any [(reject "error") (resolve "immediate") (timeout 1000 "delayed")])
  ; => Promise that resolves to "immediate"
  
  ; API fallback pattern
  (async
    (let [result (await (promise-any [
                          (fetch-data "primary-api")
                          (fetch-data "backup-api")
                          (fetch-data "fallback-api")]))]
      result)) ; => Data from first successful API
  
  ; Empty collection rejects immediately
  (promise-any []) ; => Promise that rejects with aggregate error

Notes:
  - Requires exactly 1 argument (a collection of promises)
  - All elements in collection must be promises
  - Returns promise that resolves with FIRST successful resolution
  - Rejections are ignored until all promises have been checked
  - Only rejects if ALL input promises reject (AggregateError)
  - Result value matches the first resolved promise's value
  - Empty collection immediately rejects with aggregate error
  - Other promises continue running but their results are ignored after first success
  - Useful for fallback patterns, redundant data sources, resilient operations
  - Common pattern: try multiple endpoints, use first successful response
  - Similar to Promise.any() in JavaScript (ES2021)
"""
