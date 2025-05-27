from typing import List, Any
from ..exceptions import EvaluationError

def builtin_cons(args: List[Any]) -> List[Any]:
    """Prepends an item to a list. (cons item list)"""
    if len(args) != 2:
        raise EvaluationError(f"SyntaxError: 'cons' expects 2 arguments (item list), got {len(args)}.")
    
    item = args[0]
    list_arg = args[1]

    if not isinstance(list_arg, list):
        raise EvaluationError(f"TypeError: 'cons' expects its second argument to be a list, got {type(list_arg).__name__}.")

    return [item] + list_arg 