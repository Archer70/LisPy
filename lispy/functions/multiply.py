from typing import List, Any, Union
from ..exceptions import EvaluationError
from numbers import Number
# import math # Not strictly needed for multiply, but good if using math.prod later

Numeric = Union[int, float]

def builtin_multiply(args: List[Any]) -> Numeric:
    """Multiplies numbers. (* num1 num2 ...)
    If no arguments, returns 1 (identity for multiplication).
    """
    if not args:
        return 1 # Identity for multiplication
    
    product: Numeric = 1
    for i, arg in enumerate(args):
        if not isinstance(arg, Number):
            raise EvaluationError(f"TypeError: Argument {i+1} to '*' must be a number, got {type(arg).__name__}: '{arg}'")
        product *= arg
    return product 