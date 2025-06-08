# lispy_project/lispy/functions/boolean_q.py
from typing import List, Any
from ..exceptions import EvaluationError
from ..environment import Environment


def builtin_is_boolean_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a boolean, false otherwise. (is_boolean? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_boolean?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, bool) 