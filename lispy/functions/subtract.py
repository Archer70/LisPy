from typing import List, Any, Union
from ..exceptions import EvaluationError
from numbers import Number
from ..environment import Environment

Numeric = Union[int, float]

def builtin_subtract(args: List[Any], env: Environment) -> Numeric:
    """Subtracts numbers. (- num1 num2 ...)
    If one argument, returns its negation (- num).
    If no arguments, raises error.
    """
    if not args:
        raise EvaluationError("SyntaxError: '-' requires at least one argument.")

    for i, arg in enumerate(args):
        if not isinstance(arg, Number):
            raise EvaluationError(f"TypeError: Argument {i+1} to '-' must be a number, got {type(arg).__name__}: '{arg}'")

    if len(args) == 1:
        return -args[0]
    else:
        result: Numeric = args[0]
        for i in range(1, len(args)):
            result -= args[i]
        return result 