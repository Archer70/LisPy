# lispy_project/lispy/functions/map_q.py
from typing import List, Any
from ..exceptions import EvaluationError
from ..environment import Environment


def builtin_is_map_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a map, false otherwise. (is_map? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_map?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, dict) 