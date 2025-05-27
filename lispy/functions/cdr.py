from typing import List, Any
from ..exceptions import EvaluationError

def builtin_cdr(args: List[Any]) -> List[Any]:
    """Returns all elements of a list except the first. (cdr list)"""
    if len(args) != 1:
        raise EvaluationError(f"SyntaxError: 'cdr' expects 1 argument (a list), got {len(args)}.")
    
    list_arg = args[0]

    if not isinstance(list_arg, list):
        raise EvaluationError(f"TypeError: 'cdr' expects its argument to be a list, got {type(list_arg).__name__}.")

    if not list_arg: # Empty list
        raise EvaluationError("RuntimeError: 'cdr' cannot operate on an empty list.")

    return list_arg[1:] 