from typing import List, Any, Callable
from lispy.environment import Environment
from lispy.exceptions import EvaluationError, UserThrownError
from lispy.types import Symbol


def documentation_try():
    """Returns documentation for the 'try' special form."""
    return """Special Form: try
Arguments: (try body-expr (catch exception-var catch-body) (finally finally-body))
Description: Executes body with exception handling. Catch and finally blocks are optional.

Examples:
  (try (/ 10 0) (catch e "Error occurred"))     ; Returns "Error occurred"
  (try (+ 1 2) (catch e "Won't run"))           ; Returns 3
  (try (throw "oops") (catch e e))              ; Returns "oops"
  (try (print "hi") (finally (print "done")))  ; Prints both, returns nil
  (try 
    (if (< x 0) (throw "negative") x)
    (catch e (str "Error: " e)))                ; Conditional exception handling

Notes:
  - Body expression is always evaluated first
  - Catch block runs only if an exception occurs
  - Finally block always runs (if present)
  - Exception variable in catch block is bound to the thrown value
  - Both catch and finally are optional
  - Returns the value of the successful body or catch block

See Also: throw"""

def handle_try_form(
    expression: List[Any], env: Environment, evaluate_fn: Callable
) -> Any:
    """
    Handle the 'try' special form.

    Usage:
        (try body (catch error-binding handler-body))
        (try body (catch error-binding handler-body) (finally cleanup-body))
        (try body (finally cleanup-body))

    Executes body, catching any exceptions and optionally running cleanup.
    """
    if len(expression) < 2:
        raise EvaluationError(
            "SyntaxError: 'try' expects at least 1 argument (body), got {}.".format(
                len(expression) - 1
            )
        )

    try_body = expression[1]
    catch_clause = None
    finally_clause = None

    # Parse catch and finally clauses
    for clause in expression[2:]:
        if not isinstance(clause, list) or len(clause) < 1:
            raise EvaluationError(
                "SyntaxError: 'try' clauses must be lists starting with 'catch' or 'finally'."
            )

        clause_type = clause[0]
        if isinstance(clause_type, Symbol):
            if clause_type.name == "catch":
                if catch_clause is not None:
                    raise EvaluationError(
                        "SyntaxError: 'try' can only have one 'catch' clause."
                    )
                # Validate catch clause syntax upfront
                _validate_catch_clause(clause)
                catch_clause = clause
            elif clause_type.name == "finally":
                if finally_clause is not None:
                    raise EvaluationError(
                        "SyntaxError: 'try' can only have one 'finally' clause."
                    )
                # Validate finally clause syntax upfront
                _validate_finally_clause(clause)
                finally_clause = clause
            else:
                raise EvaluationError(
                    "SyntaxError: 'try' clauses must start with 'catch' or 'finally', got '{}'.".format(
                        clause_type.name
                    )
                )
        else:
            raise EvaluationError(
                "SyntaxError: 'try' clauses must start with 'catch' or 'finally'."
            )

    result = None
    exception_occurred = False

    try:
        # Execute the try body
        result = evaluate_fn(try_body, env)
    except Exception as e:
        exception_occurred = True

        if catch_clause is not None:
            # Handle the exception with the catch clause
            result = _handle_catch_clause(catch_clause, e, env, evaluate_fn)
        else:
            # No catch clause, re-raise the exception after finally
            if finally_clause is not None:
                _handle_finally_clause(finally_clause, env, evaluate_fn)
            raise
    finally:
        # Always execute finally clause if present
        if finally_clause is not None:
            _handle_finally_clause(finally_clause, env, evaluate_fn)

    return result


def _validate_catch_clause(catch_clause: List[Any]) -> None:
    """Validate catch clause syntax."""
    if len(catch_clause) < 3:
        raise EvaluationError(
            "SyntaxError: 'catch' expects at least 2 arguments (binding handler-body...), got {}.".format(
                len(catch_clause) - 1
            )
        )

    error_binding = catch_clause[1]
    if not isinstance(error_binding, Symbol):
        raise EvaluationError(
            "SyntaxError: 'catch' binding must be a symbol, got {}.".format(
                type(error_binding).__name__
            )
        )


def _validate_finally_clause(finally_clause: List[Any]) -> None:
    """Validate finally clause syntax."""
    if len(finally_clause) < 2:
        raise EvaluationError(
            "SyntaxError: 'finally' expects at least 1 argument (cleanup-body), got {}.".format(
                len(finally_clause) - 1
            )
        )


def _handle_catch_clause(
    catch_clause: List[Any],
    exception: Exception,
    env: Environment,
    evaluate_fn: Callable,
) -> Any:
    """Handle a catch clause by binding the exception and executing the handler."""
    # Syntax validation is done upfront, so we can assume valid structure
    error_binding = catch_clause[1]

    # Create new environment with exception bound
    catch_env = Environment(outer=env)

    # Determine what to bind based on exception type
    if isinstance(exception, UserThrownError):
        # For user-thrown exceptions, bind the actual thrown value
        catch_env.define(error_binding.name, exception.value)
    else:
        # For system exceptions, bind the exception message
        catch_env.define(error_binding.name, str(exception))

    # Execute handler body
    result = None
    for handler_expr in catch_clause[2:]:
        result = evaluate_fn(handler_expr, catch_env)

    return result


def _handle_finally_clause(
    finally_clause: List[Any], env: Environment, evaluate_fn: Callable
) -> None:
    """Handle a finally clause by executing the cleanup body."""
    # Syntax validation is done upfront, so we can assume valid structure
    # Execute finally body
    for cleanup_expr in finally_clause[1:]:
        evaluate_fn(cleanup_expr, env)
