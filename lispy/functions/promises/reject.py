from typing import List, Any
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise


def builtin_reject(args: List[Any], env: Environment) -> LispyPromise:
    """Creates a rejected promise with the given error. (reject error)"""
    if len(args) != 1:
        raise EvaluationError(
            "SyntaxError: 'reject' expects 1 argument (error), got {}.".format(
                len(args)
            )
        )

    error = args[0]

    # Create a promise that's already rejected
    promise = LispyPromise()
    promise.reject(error)
    return promise


def documentation_reject() -> str:
    """Returns documentation for the reject function."""
    return """Function: reject
Arguments: (reject error)
Description: Creates a promise that is already rejected with the given error.

Examples:
  (reject "Something went wrong")       ; => Promise(rejected: "Something went wrong")
  (reject 404)                          ; => Promise(rejected: 404)
  (reject {:error "Not found"})         ; => Promise(rejected: {:error "Not found"})
  
  ; Using with await (throws error):
  (async
    (try
      (await (reject "Test error"))      ; This will throw
      (catch error
        (println "Caught:" error))))     ; => prints "Caught: Test error"
      
  ; Useful for error conditions:
  (defn-async validate-input [input]
    (if (valid? input)
      (resolve input)                    ; Success case
      (reject "Invalid input")))         ; Error case

Notes:
  - Requires exactly one argument (the error value)
  - Creates a promise in "rejected" state
  - Throws error when awaited (unless caught)
  - Useful for testing error handling
  - Good for conditional error creation
  - Can be mixed with normal promises in combinators
  - Error value can be any LisPy value (string, number, map, etc.)
  - Maintains consistent async error interface
  - Use with try/catch when awaiting
  - Rejected promises propagate through promise chains"""
