from typing import List, Any, Union
from ..exceptions import EvaluationError
from numbers import Number
from ..environment import Environment

Numeric = Union[int, float]


def builtin_divide(args: List[Any], env: Environment) -> float:
    """Divides numbers. (/ num1 num2 ...)
    If no arguments or one argument, raises error.
    All results are floats.
    """
    if len(args) < 2:
        raise EvaluationError("SyntaxError: '/' requires at least two arguments.")

    for i, arg in enumerate(args):
        if not isinstance(arg, Number):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to '/' must be a number, got {type(arg).__name__}: '{arg}'"
            )

    # Check for division by zero in subsequent arguments
    for i in range(1, len(args)):
        if args[i] == 0:
            raise EvaluationError(
                f"ZeroDivisionError: Division by zero (argument {i + 1})."
            )

    result: float = float(args[0])  # Start with the first number as a float
    for i in range(1, len(args)):
        result /= float(args[i])
    return result
