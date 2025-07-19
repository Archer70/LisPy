from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from lispy.closure import Function
from ..decorators import lispy_function, lispy_documentation


@lispy_function("then")
def then(args, env):
    """Chain a callback to be executed when promise resolves.

    Usage: (then promise callback)

    Args:
        promise: A promise to chain from
        callback: Function to call with the resolved value

    Returns:
        A new promise that resolves with the callback's return value

    Examples:
        (then (resolve 42) (fn [x] (* x 2)))
        ; => Promise that resolves to 84

        (-> (resolve 10)
            (then (fn [x] (+ x 5)))
            (then (fn [x] (* x 2))))
        ; => Promise that resolves to 30

        (async
          (let [result (await (then (promise (fn [] 10))
                                    (fn [x] (+ x 5))))]
            result)) ; => 15
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'then' expects 2 arguments (promise callback), got {len(args)}."
        )

    promise, callback = args

    # Validate first argument is a promise
    if not isinstance(promise, LispyPromise):
        raise EvaluationError(
            f"TypeError: First argument to 'then' must be a promise, got {type(promise).__name__}."
        )

    # Validate second argument is a function
    if not (callable(callback) or isinstance(callback, Function)):
        raise EvaluationError(
            f"TypeError: Second argument to 'then' must be a function, got {type(callback).__name__}."
        )

    # Return a new promise that will chain from the original
    return promise.then(callback, env)


@lispy_documentation("then")
def then_doc():
    return """Function: then
Arguments: (then promise callback)
Description: Chains a callback to execute when a promise resolves.

Examples:
  ; Basic chaining
  (then (resolve 42) (fn [x] (* x 2)))
  ; => Promise that resolves to 84
  
  ; Multiple chains using threading
  (-> (resolve 10)
      (then (fn [x] (+ x 5)))
      (then (fn [x] (* x 2))))
  ; => Promise that resolves to 30
  
  ; Async computation chain
  (then (promise (fn [] (+ 1 2)))
        (fn [result] (* result 10)))
  ; => Promise that resolves to 30
  
  ; With async/await
  (async
    (let [result (await (then (resolve "hello")
                              (fn [s] (+ s " world"))))]
      (println result))) ; => "hello world"

Notes:
  - Requires exactly 2 arguments (promise, callback function)
  - Callback receives the resolved value as its argument
  - Returns a new promise with the callback's return value
  - If callback throws, the returned promise rejects
  - If original promise rejects, callback is not called
  - Essential for promise composition and chaining
  - Can be chained with threading macro (->)"""
