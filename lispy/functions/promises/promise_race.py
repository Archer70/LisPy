from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, LispyList, Vector
import threading
import time


def builtin_promise_race(args, env):
    """Race multiple promises and return the first one to settle.

    Usage: (promise-race collection)

    Args:
        collection: A vector or list of promises

    Returns:
        A promise that settles with the same value and state as
        the first promise to settle (resolve or reject)

    Examples:
        (promise-race [(timeout 100 "slow") (timeout 50 "fast")])
        ; => Promise that resolves to "fast"

        (async
          (let [result (await (promise-race [(resolve "immediate") (timeout 1000 "slow")]))]
            result)) ; => "immediate"
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'promise-race' expects 1 argument, got {len(args)}."
        )

    collection = args[0]

    # Validate collection is a list or vector
    if not isinstance(collection, (LispyList, Vector)):
        raise EvaluationError(
            f"TypeError: 'promise-race' argument must be a list or vector, got {type(collection)}."
        )

    # Validate all elements are promises
    for i, element in enumerate(collection):
        if not isinstance(element, LispyPromise):
            raise EvaluationError(
                f"TypeError: All elements must be promises, got {type(element)} at position {i}."
            )

    # Handle empty collection - return a promise that never settles
    if len(collection) == 0:
        # According to Promise.race([]) behavior in JavaScript,
        # this should return a promise that never settles
        return LispyPromise()  # Returns pending promise

    # Create the race promise
    race_promise = LispyPromise()

    def race_monitor():
        """Monitor all promises and settle with the first one to complete."""
        try:
            settled = False

            while not settled:
                # Check each promise to see if any have settled
                for i, promise in enumerate(collection):
                    if promise.state != "pending":
                        # First promise to settle wins
                        if promise.state == "resolved":
                            race_promise.resolve(promise.value)
                        elif promise.state == "rejected":
                            race_promise.reject(promise.error)
                        settled = True
                        return

                # Small sleep to avoid busy waiting
                time.sleep(0.001)

        except Exception as e:
            if not settled:
                race_promise.reject(e)

    # Start monitoring in background thread
    threading.Thread(target=race_monitor, daemon=True).start()

    return race_promise


def documentation_promise_race() -> str:
    """Returns documentation for the promise-race function."""
    return """Function: promise-race
Arguments: (promise-race collection)
Description: Returns a promise that settles with the first promise to settle (resolve or reject).

Examples:
  ; First to resolve wins
  (promise-race [(timeout 200 "slow") (timeout 50 "fast")])
  ; => Promise that resolves to "fast"
  
  ; First to reject wins too
  (promise-race [(timeout 200 "slow") (reject "error")])
  ; => Promise that rejects with "error"
  
  ; With immediate values
  (promise-race [(resolve "immediate") (timeout 1000 "delayed")])
  ; => Promise that resolves to "immediate"
  
  ; Timeout pattern
  (async
    (let [result (await (promise-race [
                          (fetch-data "user")
                          (timeout 5000 (reject "timeout"))]))]
      result)) ; => Either user data or timeout error
  
  ; Empty collection never settles
  (promise-race []) ; => Promise that stays pending forever

Notes:
  - Requires exactly 1 argument (a collection of promises)
  - All elements in collection must be promises
  - Returns promise that settles as soon as ANY input promise settles
  - Settlement type (resolve/reject) matches the first settled promise
  - Result value matches the first settled promise's value/error
  - Empty collection returns a promise that never settles
  - Other promises continue running but their results are ignored
  - Useful for timeouts, racing multiple data sources, fail-fast patterns
  - Common pattern: race actual operation vs timeout promise
  - Similar to Promise.race() in JavaScript
"""
