from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise, LispyList, Vector
from ..decorators import lispy_function, lispy_documentation
import threading
import time


@lispy_function("promise-race")
def promise_race(args, env):
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

    # Validate that it's a collection
    if not isinstance(collection, (list, Vector, LispyList)):
        raise EvaluationError(
            f"TypeError: 'promise-race' expects a collection (list/vector), got {type(collection).__name__}."
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
        empty_promise.reject("Empty collection provided to promise-race")
        return empty_promise

    # Create result promise
    result_promise = LispyPromise()

    def race_promises():
        """Wait for first promise to settle in background thread."""
        try:
            # Continuously poll all promises until one settles
            while True:
                for promise in promises:
                    if promise.state != "pending":
                        # First promise to settle wins
                        if promise.state == "resolved":
                            result_promise.resolve(promise.value)
                        else:  # rejected
                            result_promise.reject(promise.error)
                        return

                # Small sleep to avoid busy waiting
                time.sleep(0.001)

        except Exception as e:
            result_promise.reject(f"promise-race error: {str(e)}")

    # Start background thread
    thread = threading.Thread(target=race_promises, daemon=True)
    thread.start()

    return result_promise


@lispy_documentation("promise-race")
def promise_race_doc():
    return """Function: promise-race
Arguments: (promise-race collection)
Description: Returns a promise that settles with the first promise to settle.

Examples:
  ; Race between fast and slow promises
  (promise-race [(timeout 100 "slow") (timeout 50 "fast")])
  ; => Promise that resolves to "fast"
  
  ; Immediate resolution wins
  (promise-race [(resolve "immediate") (timeout 1000 "slow")])
  ; => Promise that resolves to "immediate"
  
  ; First rejection wins
  (promise-race [(reject "error") (timeout 1000 "slow")])
  ; => Promise that rejects with "error"
  
  ; With async/await
  (async
    (let [winner (await (promise-race [(promise (fn [] (+ 1 2)))
                                       (resolve "quick")]))]
      (println "Winner:" winner)))

Notes:
  - Requires exactly 1 argument (a collection of promises)
  - Collection can be a list, vector, or LisPy list
  - All items in collection must be promises
  - Returns the value/error of the first promise to settle
  - Empty collection immediately rejects
  - Useful for timeouts and racing multiple approaches
  - First to settle (resolve OR reject) wins"""
