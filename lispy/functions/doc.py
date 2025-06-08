from typing import List, Any
from ..exceptions import EvaluationError
from ..environment import Environment


# Documentation registry - maps function names to their documentation functions
DOCUMENTATION_REGISTRY = {}


def register_documentation(function_name: str, doc_function):
    """Register a documentation function for a given function name."""
    DOCUMENTATION_REGISTRY[function_name] = doc_function


def builtin_doc(args: List[Any], env: Environment) -> str:
    """Returns documentation for a function. (doc function-name)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'doc' expects 1 argument, got {len(args)}."
        )

    # The argument should be a function or symbol representing a function
    func_arg = args[0]
    
    # Try to get the function name
    function_name = None
    
    # If it's a callable (built-in function), try to find its name
    if callable(func_arg):
        # Look through the environment to find the name bound to this function
        for name, value in env.store.items():
            if value is func_arg:
                function_name = name
                break
        
        # Also check parent environments
        if function_name is None:
            current_env = env.outer
            while current_env is not None:
                for name, value in current_env.store.items():
                    if value is func_arg:
                        function_name = name
                        break
                if function_name:
                    break
                current_env = current_env.outer
    
    if function_name is None:
        raise EvaluationError(
            f"TypeError: Unable to find documentation for the given function. "
            f"Make sure to pass a function reference like +, abs, etc."
        )
    
    # Look up documentation in registry
    if function_name in DOCUMENTATION_REGISTRY:
        doc_function = DOCUMENTATION_REGISTRY[function_name]
        return doc_function()
    else:
        return f"No documentation available for function '{function_name}'"


def documentation_doc() -> str:
    """Returns documentation for the doc function."""
    return """Function: doc
Arguments: (doc function)
Description: Returns documentation string for the specified function.

Examples:
  (doc +)       ; Returns documentation for the + function
  (doc abs)     ; Returns documentation for the abs function
  (doc doc)     ; Returns this documentation

Notes:
  - Pass the function itself, not a string
  - Use with print-doc to display formatted output
  - Returns a string that can be further processed""" 