# lispy_project/lispy/functions/nil_q.py
from typing import List, Any
from ..exceptions import EvaluationError
from ..environment import Environment


def builtin_is_nil_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is nil, false otherwise. (is_nil? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_nil?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return arg is None 