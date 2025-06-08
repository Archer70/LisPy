# lispy_project/lispy/functions/vector_q.py
from typing import List, Any
from ..types import Vector
from ..exceptions import EvaluationError
from ..environment import Environment


def builtin_is_vector_q(args: List[Any], env: Environment) -> bool:
    """Returns true if the argument is a vector, false otherwise. (is_vector? value)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'is_vector?' expects 1 argument, got {len(args)}."
        )

    arg = args[0]
    return isinstance(arg, Vector) 