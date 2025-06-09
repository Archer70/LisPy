from typing import List, Any
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise


def builtin_resolve(args: List[Any], env: Environment) -> LispyPromise:
    """Creates a resolved promise with the given value. (resolve value)"""
    if len(args) != 1:
        raise EvaluationError("SyntaxError: 'resolve' expects 1 argument (value), got {}.".format(len(args)))
    
    value = args[0]
    
    # Create a promise that's already resolved
    promise = LispyPromise()
    promise.resolve(value)
    return promise


def documentation_resolve() -> str:
    """Returns documentation for the resolve function."""
    return """Function: resolve
Arguments: (resolve value)
Description: Creates a promise that is already resolved with the given value.

Examples:
  (resolve 42)                          ; => Promise(resolved: 42)
  (resolve "hello")                     ; => Promise(resolved: "hello")
  (resolve [1 2 3])                     ; => Promise(resolved: [1 2 3])
  
  ; Using with await (returns immediately):
  (async
    (let [result (await (resolve 100))]
      (println "Result:" result)))       ; => prints "Result: 100"
      
  ; Useful for testing or conditional async:
  (defn-async maybe-fetch [use-cache]
    (if use-cache
      (resolve cached-data)              ; Return cached data immediately
      (promise #(fetch-from-server))))   ; Actually fetch from server

Notes:
  - Requires exactly one argument (the value)
  - Creates a promise in "resolved" state
  - Returns immediately when awaited
  - Useful for testing async code
  - Good for conditional async operations
  - Can be mixed with pending promises in combinators
  - More efficient than promise when value is already available
  - Maintains consistent async interface
  - Can be used to convert sync values to async context""" 