# LisPy Evaluator

from typing import Any, Callable
from typing import List as TypingList

from .closure import Function
from .environment import Environment
from .exceptions import AssertionFailure, EvaluationError, UserThrownError
from .special_forms import special_form_handlers
from .tail_call import TailCall
from .types import LispyList, LispyMapLiteral, LispyPromise, Symbol, Vector

# Maximum recursion depth for regular function calls
MAX_RECURSION_DEPTH = 100


def _execute_user_defined_function(
    lisp_function: Function,
    evaluated_args: "TypingList[Any]",  # typing.List for the Python list of args
    operator_expr: Any,  # For error messages
    evaluate_fn: Callable,
    recursion_depth: int = 0,
) -> Any:
    """Helper to execute a user-defined Lisp function (Function object) with explicit recur support."""
    if len(evaluated_args) != len(lisp_function.params):
        fn_name_str = (
            str(operator_expr) if isinstance(operator_expr, Symbol) else "<fn>"
        )
        raise EvaluationError(
            f"ArityError: Function '{fn_name_str}' expects {len(lisp_function.params)} arguments, got {len(evaluated_args)}."
        )

    # Check recursion depth to enforce recur usage
    if recursion_depth > MAX_RECURSION_DEPTH:
        fn_name_str = (
            str(operator_expr) if isinstance(operator_expr, Symbol) else "<fn>"
        )
        raise EvaluationError(
            f"RecursionError: Function '{fn_name_str}' exceeded maximum recursion depth of {MAX_RECURSION_DEPTH}. "
            f"Use 'recur' for tail-recursive calls to avoid stack overflow."
        )

    current_function = lisp_function
    current_args = evaluated_args

    # Trampoline loop for explicit tail call optimization via recur
    while True:
        # Create a new environment for the function call
        call_env = Environment(outer=current_function.defining_env)

        # Bind the current function to a special variable for recur
        call_env.define("__current_function__", current_function)

        # Store recursion depth for nested calls
        call_env.define("__recursion_depth__", recursion_depth)

        # Bind arguments to parameters in the new environment
        for param_symbol, arg_value in zip(current_function.params, current_args):
            call_env.define(param_symbol.name, arg_value)

        # Evaluate body expressions sequentially in the call environment
        result = None
        for body_expr in current_function.body:
            result = evaluate_fn(body_expr, call_env)

            # Check if the result is a TailCall (from recur)
            if isinstance(result, TailCall):
                # Tail call detected - continue loop with new args
                current_args = result.args
                break  # Break out of body evaluation loop, continue trampoline

        # If we get here without a TailCall, return the result
        if not isinstance(result, TailCall):
            return result


def _execute_builtin_function(
    py_callable: Callable,
    evaluated_args: "TypingList[Any]",  # typing.List for the Python list of args
    operator_expr: Any,  # For error messages
    env: Environment,  # Added env parameter
) -> Any:
    """Helper to execute a Python callable that is a built-in function."""
    fn_name_str = (
        str(operator_expr) if isinstance(operator_expr, Symbol) else repr(operator_expr)
    )
    try:
        # Pass env to the built-in callable
        return py_callable(evaluated_args, env)
    except AssertionFailure:  # Added: Let AssertionFailure propagate directly
        raise
    except UserThrownError:  # Added: Let UserThrownError propagate directly
        raise
    except EvaluationError:
        raise
    except Exception as e:
        # Catch other Python exceptions from the built-in and wrap them
        # This helps distinguish internal Python errors from LisPy EvaluationErrors made by builtins.
        raise EvaluationError(
            f"Error calling built-in function '{fn_name_str}': {type(e).__name__} - {e}"
        )


def _apply_procedure(
    procedure: Any,
    evaluated_args: "TypingList[Any]",  # typing.List for the Python list of args
    operator_expr: Any,  # For error messages
    evaluate_fn: Callable,  # For user-defined function body evaluation
    env: Environment,  # For user-defined function lexical scope
) -> Any:
    """Applies a procedure (either user-defined Function or built-in Python callable)."""
    if isinstance(procedure, Function):
        # Get recursion depth from environment, default to 0
        recursion_depth = 0
        try:
            recursion_depth = env.lookup("__recursion_depth__")
        except EvaluationError:
            pass  # Not in a function call, start at 0

        return _execute_user_defined_function(
            procedure, evaluated_args, operator_expr, evaluate_fn, recursion_depth + 1
        )
    elif callable(procedure):
        # Pass env to _execute_builtin_function
        return _execute_builtin_function(procedure, evaluated_args, operator_expr, env)
    else:
        raise EvaluationError(
            f"Object '{procedure}' is not a function or a recognized callable procedure. (Called with operator: '{operator_expr}')"
        )


def _evaluate_list_form_as_call(
    expression: Any, env: Environment, evaluate_fn: Callable
) -> Any:
    """Helper to evaluate a list form that is definitively a function call (not a special form)."""
    operator_expr = expression[0]
    arg_exprs = expression[1:]
    procedure = evaluate_fn(operator_expr, env)
    evaluated_args = [evaluate_fn(arg, env) for arg in arg_exprs]
    return _apply_procedure(procedure, evaluated_args, operator_expr, evaluate_fn, env)


# --- Main Evaluation Logic ---
def _is_self_evaluating(expression: Any) -> bool:
    """Check if an expression evaluates to itself (self-evaluating)."""
    return (
        isinstance(expression, (int, float, str, bool, Function, Vector, LispyPromise))
        or expression is None
    )


def _dict_needs_evaluation(dictionary: dict, env: Environment) -> bool:
    """Check if a dictionary contains values that need evaluation."""
    for value in dictionary.values():
        if isinstance(value, LispyList):
            # Function calls definitely need evaluation
            return True
        elif isinstance(value, Symbol):
            # Symbols need evaluation (variables, function references, etc.)
            return True
        elif isinstance(value, dict):
            # Recursively check nested dictionaries
            if _dict_needs_evaluation(value, env):
                return True
        elif isinstance(value, Vector):
            # Check if vector contains function calls or symbols that need evaluation
            for item in value:
                if isinstance(item, Symbol):
                    return True
                elif isinstance(item, (LispyList, list)):
                    return True
                elif isinstance(item, dict) and _dict_needs_evaluation(item, env):
                    return True
    return False


def _evaluate_dict_values(dictionary: dict, env: Environment) -> dict:
    """Evaluate all values in a dictionary."""
    evaluated_dict = {}
    for key, value in dictionary.items():
        evaluated_dict[key] = evaluate(value, env)
    return evaluated_dict


def evaluate(expression: Any, env: Environment) -> Any:
    """Evaluates a LisPy expression (AST node) in a given environment."""
    # Handle map literals from source code (need value evaluation)
    if isinstance(expression, LispyMapLiteral):
        if _dict_needs_evaluation(expression, env):
            return _evaluate_dict_values(expression, env)
        else:
            # Convert to regular dict and return
            return dict(expression)

    # Handle runtime dictionaries (already evaluated, keep as-is)
    elif isinstance(expression, dict):
        return expression

    # Handle self-evaluating types
    elif _is_self_evaluating(expression):
        return expression

    # Handle symbol lookup
    elif isinstance(expression, Symbol):
        return env.lookup(expression.name)

    # Handle list expressions (function calls and special forms)
    elif isinstance(expression, (list, LispyList)):
        # If expression is an empty list (parsed from '()'), it should raise an error.
        if not expression:
            raise EvaluationError(
                "EvaluationError: Cannot evaluate an empty list as a function call or special form."
            )

        first_element = expression[0]
        if isinstance(first_element, Symbol):
            # Check if environment has custom special form handlers (for web-safe mode)
            handlers = getattr(env, "_special_form_handlers", special_form_handlers)
            handler = handlers.get(first_element.name)
            if handler:
                # Pass expression as is (could be list or LispyList)
                return handler(expression, env, evaluate)

        # Pass expression as is (could be list or LispyList)
        return _evaluate_list_form_as_call(expression, env, evaluate)

    # Unhandled expression type
    else:
        raise EvaluationError(f"Cannot evaluate type: {type(expression).__name__}")
