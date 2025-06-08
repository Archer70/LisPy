from typing import List, Any, Union
from ..exceptions import EvaluationError
from numbers import Number
from ..environment import Environment

Numeric = Union[int, float]


def builtin_max(args: List[Any], env: Environment) -> Numeric:
    """Returns the maximum of the given numbers. (max num1 num2 ...)"""
    if len(args) == 0:
        raise EvaluationError(
            f"SyntaxError: 'max' expects at least 1 argument, got 0."
        )

    # Validate all arguments are numbers and find maximum
    maximum = None
    for i, arg in enumerate(args):
        if not isinstance(arg, Number) or isinstance(arg, bool):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to 'max' must be a number, got {type(arg).__name__}: '{arg}'"
            )
        
        if maximum is None or arg > maximum:
            maximum = arg

    return maximum 