from typing import List, Any
from lispy.environment import Environment
from lispy.exceptions import EvaluationError
from lispy.types import LispyPromise
from lispy.closure import Function
from lispy.evaluator import evaluate
from ..decorators import lispy_function, lispy_documentation


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
            # Call built-in function with no arguments
            return thunk([], env)

    return LispyPromise(executor)


@lispy_documentation("promise")
def promise_doc() -> str:
    """Returns documentation for the promise function."""
    return """Function: promise
Arguments: (promise function)
Description: Creates a promise that will execute the given function asynchronously.

Examples:
  ; Create a promise from a function
  (define my-promise (promise (fn [] (+ 1 2))))
  
  ; Create promise from an expensive computation
  (define slow-promise 
    (promise (fn [] 
               (print "Computing...") 
               (* 42 42))))
  
  ; Chain promises with then
  (-> (promise (fn [] 10))
      (then (fn [x] (* x 2)))
      (then (fn [x] (println "Result:" x))))

Notes:
  - Requires exactly 1 argument (a function)
  - The function must take 0 arguments
  - The function is executed asynchronously when the promise is resolved
  - Use 'then' to chain operations on promise results
  - Use 'resolve' and 'reject' for manual promise control"""
