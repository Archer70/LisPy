from typing import List, Any
from ..environment import Environment
from ..exceptions import EvaluationError
from ..closure import Function


def builtin_is_function_q(args: List[Any], env: Environment) -> bool:
    """Implementation of the (is_function? value) LisPy function.
    
    Returns true if the argument is a function (either user-defined or built-in), false otherwise.
    
    Args:
        args: List containing exactly one argument to check
        env: The current environment (unused but required by function signature)
    
    Returns:
        bool: True if the argument is a function, False otherwise
    
    Raises:
        EvaluationError: If incorrect number of arguments provided
    """
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_function?' expects 1 argument, got {len(args)}."
        )
    
    arg = args[0]
    
    # Check if it's a user-defined function (Function instance)
    if isinstance(arg, Function):
        return True
    
    # Check if it's a built-in function (Python callable)
    # We need to exclude types that are callable but not functions in the LisPy sense
    if callable(arg):
        # Exclude class types and other non-function callables
        if isinstance(arg, type):
            return False
        return True
    
    return False 