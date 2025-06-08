from typing import List, Any, Union
from ..exceptions import EvaluationError
from numbers import Number
from ..environment import Environment

Numeric = Union[int, float]


def builtin_modulo(args: List[Any], env: Environment) -> Numeric:
    """Calculates the modulo (remainder) of division. (% dividend divisor)
    Returns the remainder when dividend is divided by divisor.
    For multiple arguments, applies modulo left-to-right: (% a b c) = (% (% a b) c)
    """
    if len(args) < 2:
        raise EvaluationError("SyntaxError: '%' requires at least two arguments.")

    for i, arg in enumerate(args):
        if not isinstance(arg, Number):
            raise EvaluationError(
                f"TypeError: Argument {i + 1} to '%' must be a number, got {type(arg).__name__}: '{arg}'"
            )

    # Check for division by zero in subsequent arguments
    for i in range(1, len(args)):
        if args[i] == 0:
            raise EvaluationError(
                f"ZeroDivisionError: Modulo by zero (argument {i + 1})."
            )

    result: Numeric = args[0]  # Start with the first number
    for i in range(1, len(args)):
        result = result % args[i]

    return result
