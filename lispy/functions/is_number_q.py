# lispy_project/lispy/functions/number_q.py
from typing import List, Any
from numbers import Number
from ..exceptions import EvaluationError
from ..environment import Environment


def builtin_is_number_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a number, false otherwise. (is_number? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_number?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    # Check for Number but exclude booleans (since bool is a subclass of int in Python)
    return isinstance(arg, Number) and not isinstance(arg, bool) 