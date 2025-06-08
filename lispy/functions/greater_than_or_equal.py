from lispy.exceptions import EvaluationError
from numbers import Number
from lispy.environment import Environment
from typing import List, Any


def builtin_greater_than_or_equal(args: List[Any], env: Environment) -> bool:
    if len(args) != 2:
        raise EvaluationError("TypeError: >= requires exactly two arguments")

    arg1, arg2 = args[0], args[1]

    if not isinstance(arg1, Number):
        raise EvaluationError(
            f"TypeError: Argument 1 to '>=' must be a number, got {type(arg1).__name__}: '{arg1}'"
        )
    if not isinstance(arg2, Number):
        raise EvaluationError(
            f"TypeError: Argument 2 to '>=' must be a number, got {type(arg2).__name__}: '{arg2}'"
        )

    return arg1 >= arg2
