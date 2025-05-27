from typing import List, Any
from ..types import Vector # For type checking
from ..exceptions import EvaluationError

def builtin_empty_q(args: List[Any]) -> bool:
    """Checks if a collection (list, vector, map, string) or nil is empty. (empty? collection)"""
    if len(args) != 1:
        raise EvaluationError(f"SyntaxError: 'empty?' expects 1 argument, got {len(args)}.")
    
    arg = args[0]
    
    if arg is None: # nil
        return True
    elif isinstance(arg, (list, Vector, str, dict)):
        return not bool(arg) # len(arg) == 0 works for these types
    else:
        type_name = type(arg).__name__
        # Special handling for Function type name for clarity in error
        if hasattr(arg, '__class__') and arg.__class__.__name__ == 'Function':
            type_name = "Function"
        raise EvaluationError(f"TypeError: 'empty?' expects a list, vector, map, string, or nil. Got {type_name}") 