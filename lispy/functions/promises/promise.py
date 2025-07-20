from typing import Any, List

from lispy.closure import Function
from lispy.environment import Environment
from lispy.evaluator import evaluate
from lispy.exceptions import EvaluationError
from lispy.functions.decorators import lispy_documentation, lispy_function
from lispy.types import LispyPromise


@lispy_function("promise")
def promise(args: List[Any], env: Environment) -> LispyPromise:
    """Creates a promise from a function. (promise function)"""
    if len(args) != 1:
        raise EvaluationError(
            "SyntaxError: 'promise' expects 1 argument (function), got {}.".format(
                len(args)
            )
        )

    thunk = args[0]

    # Validate that the argument is callable (either UserDefinedFunction or built-in)
    is_user_defined_fn = isinstance(thunk, Function)
    is_builtin_fn = callable(thunk) and not is_user_defined_fn

    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError(
            "TypeError: 'promise' argument must be a function, got {}.".format(
                type(thunk).__name__
            )
        )

    # Validate arity for user-defined functions (should be zero-argument)
    if is_user_defined_fn and len(thunk.params) != 0:
        raise EvaluationError(
            "TypeError: 'promise' function must take 0 arguments, got {}.".format(
                len(thunk.params)
            )
        )

    # Create a promise that executes the thunk
    def executor():
        if is_user_defined_fn:
            # Call user-defined function
            call_env = Environment(outer=thunk.defining_env)
            # No parameters to bind since it's a zero-argument function

            # Execute the function body
            result = None
            for expr_in_body in thunk.body:
                result = evaluate(expr_in_body, call_env)
            return result
        else:
            # Call built-in function
            return thunk([], env)

    return LispyPromise(executor)


@lispy_documentation("promise")
def promise_documentation() -> str:
    """Returns documentation for the promise function."""
    return """Function: promise
Arguments: (promise function)
Description: Creates a promise that executes the given function asynchronously.

Examples:
  (promise #(+ 1 2))                    ; => Promise(pending) -> Promise(resolved: 3)
  (promise #(slurp "file.txt"))         ; => Promise that reads file asynchronously
  (promise #(* 10 10))                  ; => Promise(pending) -> Promise(resolved: 100)
  
  ; Using with await:
  (async
    (let [result (await (promise #(+ 5 5)))]
      (println "Result:" result)))       ; => prints "Result: 10"
      
  ; Wrapping blocking operations:
  (defn-async fetch-data []
    (await (promise #(http-get "api.com"))))

Notes:
  - Requires exactly one argument (a function/lambda)
  - The function is executed in a background thread
  - Returns a Promise object immediately
  - Use with 'await' to wait for the result
  - Perfect for wrapping blocking operations
  - Essential building block for async programming
  - The function should be a zero-argument lambda (#(...))
  - Use with existing synchronous functions to make them async
  - Promises can be chained with then/catch methods
  - Execution starts immediately when promise is created"""
