# lispy_project/lispy/functions/count.py
from typing import List, Any
from ..types import Vector  # For type checking
from ..exceptions import EvaluationError
from ..environment import Environment  # Added Environment import


def builtin_count(args: List[Any], env: Environment) -> int:  # Added env parameter
    """Returns the number of items in a collection (list, vector, map, string) or 0 for nil. (count collection)"""
    if len(args) != 1:
        raise EvaluationError(
            f"SyntaxError: 'count' expects 1 argument, got {len(args)}."
        )

    arg = args[0]

    if arg is None:  # nil
        return 0
    elif isinstance(arg, (list, Vector, str, dict)):
        return len(arg)
    else:
        type_name = type(arg).__name__
        # Special handling for Function type name for clarity in error
        if hasattr(arg, "__class__") and arg.__class__.__name__ == "Function":
            type_name = "Function"  # Though count shouldn't be called on functions
        raise EvaluationError(
            f"TypeError: 'count' expects a list, vector, map, string, or nil. Got {type_name}"
        )
