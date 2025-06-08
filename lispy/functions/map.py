from lispy.types import Vector
from lispy.closure import Function  # Import Function for user-defined procedures
from lispy.exceptions import EvaluationError
from lispy.evaluator import evaluate  # For evaluating user-defined function bodies
from lispy.environment import Environment  # Added import for Environment


def builtin_map(args, env):
    """Implementation of the (map vector procedure) LisPy function.
    Applies procedure to each element of vector and returns a new vector of the results.
    Usage: (map vector procedure)
    """
    if len(args) != 2:
        raise EvaluationError(
            f"SyntaxError: 'map' expects 2 arguments, got {len(args)}."
        )

    vec_arg = args[0]
    proc_arg = args[1]

    # Validate vec_arg type
    if not isinstance(vec_arg, Vector):
        raise EvaluationError(
            f"TypeError: First argument to 'map' must be a vector, got {type(vec_arg)}."
        )

    # Validate proc_arg type
    is_user_defined_fn = isinstance(proc_arg, Function)
    # Check if it's a Python callable but NOT a Function instance (i.e., a built-in)
    is_builtin_fn = callable(proc_arg) and not is_user_defined_fn

    if not (is_user_defined_fn or is_builtin_fn):
        raise EvaluationError(
            f"TypeError: Second argument to 'map' must be a procedure, got {type(proc_arg)}."
        )

    # Arity check for user-defined functions: they must accept exactly one argument for map
    if is_user_defined_fn:
        if len(proc_arg.params) != 1:
            fn_repr = repr(
                proc_arg
            )  # Provides a string representation like <UserDefinedFunction params:(...)>
            raise EvaluationError(
                f"ArityError: Procedure {fn_repr} passed to 'map' expects 1 argument, got {len(proc_arg.params)}."
            )
    # For built-in functions, arity errors will be caught during their execution if they don't match.

    result_vector_elements = []
    for item in vec_arg:  # vec_arg is already a LispyVector of evaluated items
        call_result = None
        if is_user_defined_fn:
            # Proc is a user-defined Function (closure)
            param_symbol = proc_arg.params[0]  # The single parameter Symbol
            # Create a new environment for the function call, extending its defining environment
            call_env = Environment(
                outer=proc_arg.defining_env
            )  # Changed to use Environment constructor
            call_env.define(
                param_symbol.name, item
            )  # Define the parameter in the new environment

            # Execute the function body: evaluate all expressions, result of the last one is returned
            for expr_in_body in proc_arg.body:
                call_result = evaluate(expr_in_body, call_env)
            result_vector_elements.append(call_result)

        elif is_builtin_fn:
            # Proc is a built-in Python callable
            # Built-ins in this LisPy expect a list of evaluated args and the current env
            try:
                call_result = proc_arg(
                    [item], env
                )  # Pass the item as a single-element list
                result_vector_elements.append(call_result)
            except EvaluationError as e:
                # Re-raise evaluation errors from the built-in, possibly adding context
                raise EvaluationError(
                    f"Error during 'map' applying built-in procedure to '{item}': {e}"
                )
            except Exception as e:
                # Catch other potential Python exceptions from the built-in's execution
                raise EvaluationError(
                    f"Unexpected error during 'map' applying built-in procedure to '{item}': {type(e).__name__} - {e}"
                )

    return Vector(result_vector_elements)
