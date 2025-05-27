# LisPy Evaluator

from .types import Symbol, Vector, LispyList
from .exceptions import EvaluationError # Updated import
from .environment import Environment # Import Environment
from .closure import Function # Import the new Function class
from .special_forms import special_form_handlers # Import the registry
from .tail_call import TailCall, is_tail_position, is_function_call, is_recursive_call # Import TCO support
from typing import List as TypingList, Any, Callable # Renamed typing.List to TypingList

# --- Helper Functions for Evaluation Logic ---

def _evaluate_with_tail_call_detection(expression: Any, env: Environment, current_function: Function, evaluate_fn: Callable) -> Any:
    """
    Evaluate an expression with tail call detection.
    
    This function is used when evaluating expressions in tail position to detect
    and optimize tail calls. It handles special forms that can contain tail calls
    (like 'if') and regular function calls.
    """
    # Handle self-evaluating types
    if isinstance(expression, (int, float, str, bool, dict, Function, Vector)) or expression is None:
        return expression
    
    # Handle symbols
    elif isinstance(expression, Symbol):
        return env.lookup(expression.name)
    
    # Handle lists (function calls and special forms)
    elif isinstance(expression, (list, LispyList)):
        if not expression:
            raise EvaluationError("Cannot evaluate an empty list as a function call or special form.")
        
        first_element = expression[0]
        
        # Handle 'if' special form with tail call optimization
        if isinstance(first_element, Symbol) and first_element.name == "if":
            if len(expression) < 3 or len(expression) > 4:
                raise EvaluationError("SyntaxError: 'if' requires 2 or 3 arguments. Usage: (if condition then-expr [else-expr])")
            
            condition = evaluate_fn(expression[1], env)
            
            if condition:
                # Evaluate then branch (potentially in tail position)
                return _evaluate_with_tail_call_detection(expression[2], env, current_function, evaluate_fn)
            elif len(expression) == 4:
                # Evaluate else branch (potentially in tail position)
                return _evaluate_with_tail_call_detection(expression[3], env, current_function, evaluate_fn)
            else:
                return None
        
        # Check for other special forms that might need tail call handling
        elif isinstance(first_element, Symbol):
            handler = special_form_handlers.get(first_element.name)
            if handler:
                # For now, delegate to the regular handler
                # TODO: Update special form handlers to support tail call detection
                return handler(expression, env, evaluate_fn)
        
        # Handle function calls
        # Check if this is a tail call to the current function
        if current_function and is_recursive_call(expression, current_function, env):
            # Evaluate arguments and return TailCall
            arg_exprs = expression[1:]
            tail_call_args = [evaluate_fn(arg, env) for arg in arg_exprs]
            return TailCall(current_function, tail_call_args)
        
        # Regular function call - evaluate normally
        return _evaluate_list_form_as_call(expression, env, evaluate_fn)
    
    else:
        raise EvaluationError(f"Cannot evaluate type: {type(expression).__name__}")

def _execute_user_defined_function(
    lisp_function: Function, 
    evaluated_args: "TypingList[Any]", # typing.List for the Python list of args
    operator_expr: Any, # For error messages
    evaluate_fn: Callable
) -> Any:
    """Helper to execute a user-defined Lisp function (Function object) with tail call optimization."""
    if len(evaluated_args) != len(lisp_function.params):
        fn_name_str = str(operator_expr) if isinstance(operator_expr, Symbol) else "<fn>"
        raise EvaluationError(
            f"ArityError: Function '{fn_name_str}' expects {len(lisp_function.params)} arguments, got {len(evaluated_args)}."
        )

    current_function = lisp_function
    current_args = evaluated_args
    
    # Trampoline loop for tail call optimization
    while True:
        # Create a new environment for the function call
        call_env = Environment(outer=current_function.defining_env)

        # Bind arguments to parameters in the new environment
        for param_symbol, arg_value in zip(current_function.params, current_args):
            call_env.define(param_symbol.name, arg_value)

        # Evaluate body expressions sequentially in the call environment
        result = None
        for i, body_expr in enumerate(current_function.body):
            if is_tail_position(i, len(current_function.body)):
                # This is the last expression - check for tail calls
                result = _evaluate_with_tail_call_detection(body_expr, call_env, current_function, evaluate_fn)
                
                if isinstance(result, TailCall):
                    # Tail call detected - continue loop with new function and args
                    current_function = result.function
                    current_args = result.args
                    break  # Break out of body evaluation loop, continue trampoline
                else:
                    # Regular result - return it
                    return result
            else:
                # Not in tail position - evaluate normally
                result = evaluate_fn(body_expr, call_env)
        
        # If we get here without a TailCall, return the result
        if not isinstance(result, TailCall):
            return result

def _execute_builtin_function(
    py_callable: Callable, 
    evaluated_args: "TypingList[Any]", # typing.List for the Python list of args
    operator_expr: Any # For error messages
) -> Any:
    """Helper to execute a Python callable that is a built-in function."""
    fn_name_str = str(operator_expr) if isinstance(operator_expr, Symbol) else repr(operator_expr)
    try:
        # Pass the list of evaluated arguments as a single argument
        return py_callable(evaluated_args)
    except EvaluationError: # Allow EvaluationErrors (like syntax/type errors from builtins) to propagate
        raise
    except Exception as e:
        # Catch other Python exceptions from the built-in and wrap them
        # This helps distinguish internal Python errors from LisPy EvaluationErrors made by builtins.
        raise EvaluationError(f"Error calling built-in function '{fn_name_str}': {type(e).__name__} - {e}")

def _apply_procedure(
    procedure: Any, 
    evaluated_args: "TypingList[Any]", # typing.List for the Python list of args
    operator_expr: Any, # For error messages
    evaluate_fn: Callable, # For user-defined function body evaluation
    env: Environment # For user-defined function lexical scope
) -> Any:
    """Applies a procedure (either user-defined Function or built-in Python callable)."""
    if isinstance(procedure, Function):
        return _execute_user_defined_function(procedure, evaluated_args, operator_expr, evaluate_fn)
    elif callable(procedure):
        return _execute_builtin_function(procedure, evaluated_args, operator_expr)
    else:
        raise EvaluationError(f"Object '{procedure}' is not a function or a recognized callable procedure. (Called with operator: '{operator_expr}')")

def _evaluate_list_form_as_call(expression: Any, env: Environment, evaluate_fn: Callable) -> Any:
    """Helper to evaluate a list form that is definitively a function call (not a special form)."""
    operator_expr = expression[0]
    arg_exprs = expression[1:]
    procedure = evaluate_fn(operator_expr, env)
    evaluated_args = [evaluate_fn(arg, env) for arg in arg_exprs]
    return _apply_procedure(procedure, evaluated_args, operator_expr, evaluate_fn, env)


# --- Main Evaluation Logic ---
def evaluate(expression: Any, env: Environment) -> Any:
    """Evaluates a LisPy expression (AST node) in a given environment."""
    if isinstance(expression, (int, float, str, bool, dict, Function, Vector)) or expression is None:
        # Self-evaluating types: numbers, strings, booleans, dicts (maps), Function objects, Vectors, None (nil)
        return expression
    elif isinstance(expression, Symbol):
        # Lookup symbol in the environment
        return env.lookup(expression.name)
    elif isinstance(expression, (list, LispyList)): # Keep `list` for tests, LispyList for parsed
        # If expression is an empty list (parsed from '()'), it should raise an error.
        if not expression:
            raise EvaluationError("EvaluationError: Cannot evaluate an empty list as a function call or special form.")

        first_element = expression[0]
        if isinstance(first_element, Symbol):
            handler = special_form_handlers.get(first_element.name)
            if handler:
                # Pass expression as is (could be list or LispyList)
                return handler(expression, env, evaluate)
        
        # Pass expression as is (could be list or LispyList)
        return _evaluate_list_form_as_call(expression, env, evaluate)
    else:
        # Unhandled expression type
        raise EvaluationError(f"Cannot evaluate type: {type(expression).__name__}")

