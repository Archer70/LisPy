from typing import List, Any, Union
from ..exceptions import EvaluationError
from numbers import Number

Numeric = Union[int, float]

def builtin_add(args: List[Any]) -> Numeric:
    """Adds a list of numbers. (+ num1 num2 ...)"""
    # args is now a list of the evaluated arguments
    if not args: # Handles (+)
        return 0 # Standard Lisp behavior for (+) is 0
    
    total: Numeric = 0
    # Check types and sum
    for i, arg in enumerate(args):
        if not isinstance(arg, Number):
            raise EvaluationError(f"TypeError: Argument {i+1} to '+' must be a number, got {type(arg).__name__}: '{arg}'")
        total += arg
    return total 