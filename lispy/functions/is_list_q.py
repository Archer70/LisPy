# lispy_project/lispy/functions/list_q.py
from typing import List, Any
from ..types import LispyList
from ..exceptions import EvaluationError
from ..environment import Environment


def builtin_is_list_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a list, false otherwise. (is_list? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_list?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, LispyList) 